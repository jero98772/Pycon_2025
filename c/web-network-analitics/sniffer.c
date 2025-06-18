#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <netinet/ip_icmp.h>
#include <net/ethernet.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/if_ether.h>
#include <time.h>
#include <unistd.h>
#include <signal.h>
#include <netdb.h>

// Protocol definitions
#define ICMP 1
#define TCP  6
#define UDP  17

// Packet counter
static int packet_count = 0;

// Get hostname from IP address
char* get_hostname(struct in_addr addr) {
    struct hostent *host_entry;
    static char hostname[100];
    
    host_entry = gethostbyaddr(&addr, sizeof(addr), AF_INET);
    
    if (host_entry != NULL) {
        strcpy(hostname, host_entry->h_name);
    } else {
        strcpy(hostname, inet_ntoa(addr));
    }
    
    return hostname;
}

// Process packet and write simplified output
void process_packet(unsigned char* buffer, int size, FILE* output_file) {
    struct ethhdr *eth = (struct ethhdr *)buffer;
    struct iphdr *iph = (struct iphdr*)(buffer + sizeof(struct ethhdr));
    
    packet_count++;
    
    struct sockaddr_in source, dest;
    memset(&source, 0, sizeof(source));
    memset(&dest, 0, sizeof(dest));
    source.sin_addr.s_addr = iph->saddr;
    dest.sin_addr.s_addr = iph->daddr;
    
    char *src_hostname = get_hostname(source.sin_addr);
    char *dst_hostname = get_hostname(dest.sin_addr);
    
    fprintf(output_file, "Packet %d: %s -> %s, Src MAC: %.2X:%.2X:%.2X:%.2X:%.2X:%.2X, Dst MAC: %.2X:%.2X:%.2X:%.2X:%.2X:%.2X, Protocol: %d %s\n",
        packet_count,
        inet_ntoa(source.sin_addr),
        inet_ntoa(dest.sin_addr),
        eth->h_source[0], eth->h_source[1], eth->h_source[2],
        eth->h_source[3], eth->h_source[4], eth->h_source[5],
        eth->h_dest[0], eth->h_dest[1], eth->h_dest[2],
        eth->h_dest[3], eth->h_dest[4], eth->h_dest[5],
        iph->protocol,
        src_hostname
    );
}

// Handler for timeout
void handle_timeout(int sig) {
    printf("\nCapture completed. Exiting...\n");
    exit(0);
}

void print_usage() {
    printf("Usage: ./packet_capture -t <seconds> -o <output_file>\n");
    printf("  -t <seconds>    : Duration to capture packets\n");
    printf("  -o <output_file>: File to save captured packets (optional, default: capture.txt)\n");
}

int main(int argc, char *argv[]) {
    int sock_raw;
    int timeout_seconds = 0;
    char output_filename[256] = "capture.txt";
    FILE *output_file;
    int opt;
    
    // Parse command line arguments
    while ((opt = getopt(argc, argv, "t:o:h")) != -1) {
        switch (opt) {
            case 't':
                timeout_seconds = atoi(optarg);
                break;
            case 'o':
                strcpy(output_filename, optarg);
                break;
            case 'h':
            default:
                print_usage();
                return 1;
        }
    }
    
    if (timeout_seconds <= 0) {
        printf("Error: Valid capture duration must be specified with -t flag\n");
        print_usage();
        return 1;
    }
    
    // Create raw socket
    sock_raw = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sock_raw < 0) {
        perror("Socket creation failed");
        return 1;
    }
    
    // Open output file
    output_file = fopen(output_filename, "w");
    if (output_file == NULL) {
        perror("Failed to open output file");
        close(sock_raw);
        return 1;
    }
    
    // Set timeout handler
    signal(SIGALRM, handle_timeout);
    alarm(timeout_seconds);
    
    unsigned char *buffer = (unsigned char *)malloc(65536);
    struct sockaddr saddr;
    int saddr_len = sizeof(saddr);
    
    printf("Starting packet capture for %d seconds...\n", timeout_seconds);
    printf("Output will be saved to %s\n", output_filename);
    
    while (1) {
        int buflen = recvfrom(sock_raw, buffer, 65536, 0, &saddr, (socklen_t *)&saddr_len);
        if (buflen < 0) {
            continue;
        }
        process_packet(buffer, buflen, output_file);
        fflush(output_file); // Ensure data is written immediately
    }
    
    // Clean up (will not reach here normally due to alarm signal)
    fclose(output_file);
    close(sock_raw);
    free(buffer);
    return 0;
}