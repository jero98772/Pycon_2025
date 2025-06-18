# 🚀 Process Monitor Web Application

A web application to monitor system processes using Flask, React, and WebSockets, with a backend powered by C++ and pybind11.

![](https://github.com/jero98772/processamonito/blob/main/pictures/1.png)

## 🌟 Features

- 🖥️ Real-time process monitoring
- 📊 Process details: PID, User, Name, Status, Memory, CPU Usage
- 🔄 Auto-updating UI with WebSockets
- 🌐 Cross-origin resource sharing enabled

## 🛠️ Installation

### Prerequisites

- Python 3.x
- Flask
- Flask-CORS
- Flask-SocketIO
- pybind11
- C++14 compatible compiler
- Node.js & npm (for React frontend)

### Backend Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/jero98772/processamonito.git
    cd processamonito/backend
    ```

2. Install Python dependencies:

    ```sh
    pip install flask flask-cors flask-socketio pybind11
    ```

3. Compile the C++ code(Yes compile c++ code):

    ```sh
    python setup.py build_ext --inplace

    ```

4. Run the Flask app:

    ```sh
    python main.py
    ```

### Frontend Setup

1. Navigate to the frontend directory:

    ```sh
    cd ../frontend
    ```

2. Install npm dependencies:

    ```sh
    npm install
    ```

3. Start the React app:

    ```sh
    npm start
    ```

## 📂 Project Structure

```
process-monitor-webapp/
│
├── backend/
│   ├── app.py                   # Flask backend
│   ├── process_monitor.cpp      # C++ code with pybind11 bindings
│   └── process_monitor.so       # Compiled shared object
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js               # Main React component
│   │   └── ...                  # Other React components and files
│   ├── package.json             # npm configuration
│   └── ...                      # Other frontend files
│
├── README.md
└── ...
```

## 🌐 API Endpoints

### GET /api/processes

Returns a list of current system processes.

```json
[
    {
        "pid": 1234,
        "user": "root",
        "name": "bash",
        "status": "S",
        "memory": 1024,
        "cpu_usage": 0.5
    },
    ...
]
```

## 🧩 Usage

1. Start the Flask backend.
2. Start the React frontend.
3. Open your browser and navigate to `http://localhost:3000`.
4. Enjoy real-time process monitoring! 🎉

## 🤝 Contributing

Feel free to open issues or create pull requests. Contributions are welcome!

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

[EDY](https://github.com/evalenciEAFIT), teacher of opresives systems


---

Happy coding! 💻✨

---
