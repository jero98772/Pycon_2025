#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <vector>
#include <string>
#include <filesystem>
#include <fstream>
#include <sstream>
#include <thread>
#include <chrono>
#include <set>
#include <algorithm>
#include <pwd.h>
#include <sys/sysinfo.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

namespace fs = std::filesystem;

class ProcessInfo {
public:
    int pid;
    std::string user;
    std::string name;
    std::string status;
    long memory;
    double cpu_usage;

    ProcessInfo(int pid, std::string user, std::string name, std::string status, long memory, double cpu_usage)
        : pid(pid), user(user), name(name), status(status), memory(memory), cpu_usage(cpu_usage) {}

    std::map<std::string, pybind11::object> to_dict() const {
        return {
            {"pid", pybind11::cast(pid)},
            {"user", pybind11::cast(user)},
            {"name", pybind11::cast(name)},
            {"status", pybind11::cast(status)},
            {"memory", pybind11::cast(memory)},
            {"cpu_usage", pybind11::cast(cpu_usage)}
        };
    }
};

bool compareByCpuUsage(const ProcessInfo& a, const ProcessInfo& b) {
    return a.cpu_usage > b.cpu_usage;
}

bool compareByMemory(const ProcessInfo& a, const ProcessInfo& b) {
    return a.memory > b.memory;
}

class ProcessMonitor {
public:
    std::vector<ProcessInfo> getProcesses() {
        std::vector<ProcessInfo> processes;
        for (const auto& entry : fs::directory_iterator("/proc")) {
            if (entry.is_directory()) {
                const std::string pid_str = entry.path().filename().string();
                if (is_number(pid_str)) {
                    int pid = std::stoi(pid_str);
                    std::string user = getProcessUser(pid);
                    std::string name = getProcessName(pid);
                    std::string status = getProcessStatus(pid);
                    long memory = getProcessMemory(pid);
                    double cpu_usage = getProcessCpuUsage(pid);
                    processes.emplace_back(pid, user, name, status, memory, cpu_usage);
                }
            }
        }
        return processes;
    }

    void monitorProcesses(int interval_seconds) {
        std::set<int> previous_pids;
        while (true) {
            auto processes = getProcesses();
            std::sort(processes.begin(), processes.end(), compareByMemory);

            std::set<int> current_pids;
            for (const auto& process : processes) {
                current_pids.insert(process.pid);
                if (previous_pids.find(process.pid) == previous_pids.end()) {
                    std::cout << "Nuevo proceso detectado: | (ID) " << process.pid << " | (nombre) " << process.name << " | (Estado) " << process.status << std::endl;
                }
            }

            for (const auto& pid : previous_pids) {
                if (current_pids.find(pid) == current_pids.end()) {
                    std::cout << "<<Proceso terminado: " << pid << ">>" << std::endl;
                }
            }

            previous_pids = current_pids;
            std::this_thread::sleep_for(std::chrono::seconds(interval_seconds));
        }
    }

private:
    bool is_number(const std::string& s) {
        return !s.empty() && std::all_of(s.begin(), s.end(), ::isdigit);
    }

    std::string getProcessUser(int pid) {
        struct stat info;
        std::string path = "/proc/" + std::to_string(pid);
        if (stat(path.c_str(), &info) != 0) {
            return "Unknown";
        }
        struct passwd* pw = getpwuid(info.st_uid);
        return pw ? pw->pw_name : "Unknown";
    }

    std::string getProcessName(int pid) {
        std::ifstream comm_file("/proc/" + std::to_string(pid) + "/comm");
        std::string name;
        std::getline(comm_file, name);
        return name;
    }

    std::string getProcessStatus(int pid) {
        std::ifstream status_file("/proc/" + std::to_string(pid) + "/status");
        std::string line;
        while (std::getline(status_file, line)) {
            if (line.find("State:") == 0) {
                std::istringstream iss(line);
                std::string key, status;
                iss >> key >> status;
                return status;
            }
        }
        return "Unknown";
    }

    long getProcessMemory(int pid) {
        std::ifstream status_file("/proc/" + std::to_string(pid) + "/status");
        std::string line;
        while (std::getline(status_file, line)) {
            if (line.find("VmRSS:") == 0) {
                std::istringstream iss(line);
                std::string key;
                long memory;
                iss >> key >> memory;
                return memory;
            }
        }
        return 0;
    }

    double getProcessCpuUsage(int pid) {
        struct sysinfo sys_info;
        if (sysinfo(&sys_info) != 0) {
            return 0;
        }

        std::ifstream stat_file("/proc/" + std::to_string(pid) + "/stat");
        std::string line;
        std::getline(stat_file, line);
        std::istringstream iss(line);
        std::vector<std::string> stats;
        std::string stat;
        while (iss >> stat) {
            stats.push_back(stat);
        }

        if (stats.size() < 17) {
            return 0;
        }

        long total_time = std::stol(stats[13]) + std::stol(stats[14]);
        double seconds = sys_info.uptime - (std::stol(stats[21]) / sys_info.loads[0]);

        return (total_time / sysconf(_SC_CLK_TCK)) / seconds * 100;
    }
};

namespace py = pybind11;

PYBIND11_MODULE(process_monitor, m) {
    py::class_<ProcessInfo>(m, "ProcessInfo")
        .def(py::init<int, std::string, std::string, std::string, long, double>())
        .def("to_dict", &ProcessInfo::to_dict);

    py::class_<ProcessMonitor>(m, "ProcessMonitor")
        .def(py::init<>())
        .def("get_processes", &ProcessMonitor::getProcesses)
        .def("monitor_processes", &ProcessMonitor::monitorProcesses);
}
