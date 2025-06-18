# web-network-analitics


![Packet Sniffer](https://raw.githubusercontent.com/jero98772/web-network-analitics/refs/heads/main/docs/pictures/1.png)

## Overview
This project is a real-time packet sniffer and analyzer built using FastAPI, WebSockets, and a C-based packet capture utility. It allows users to capture and analyze network packets, displaying results in a web dashboard with real-time updates and visualizations.

## Features
- **Real-time packet capture** using a custom C-based sniffer.
- **WebSockets integration** for live updates.
- **FastAPI backend** for efficient handling of requests and WebSocket connections.
- **Jinja2 templating** for serving dynamic HTML pages.
- **Chart.js integration** for visualizing captured network data.
- **Packet analysis** including most frequent source IPs and protocol distribution.

## Installation
### Prerequisites
- Python 3.8+
- GCC (for compiling the packet sniffer)
- Linux (required for raw socket access)

### Setup
```sh
# Clone the repository
git clone https://github.com/yourusername/packet-sniffer.git
cd packet-sniffer

# Create and activate virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install fastapi uvicorn websockets jinja2

# Compile the packet sniffer
gcc -o packet_capture sniffer.c
sudo setcap cap_net_raw+eip ./packet_capture
```

## Usage
### Running the Server
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```
### Accessing the Web Interface
Open a browser and navigate to:
```
http://localhost:8000
```

### Starting a Packet Capture Session
1. Set the capture duration in seconds.
2. Click the **Start Capture** button.
3. View real-time updates and visualizations.

## File Structure
```
packet-sniffer/
│── main.py                # FastAPI backend and WebSocket manager
│── sniffer.c              # C-based packet capture utility
│── templates/
│   └── index.html         # Web dashboard
│── static/
│   └── styles.css         # Stylesheets
│── README.md              # Documentation
```

## API Endpoints
| Method | Endpoint  | Description |
|--------|----------|-------------|
| `GET`  | `/`      | Serves the web dashboard |
| `WS`   | `/ws`    | WebSocket connection for real-time packet updates |

## Technologies Used
- **FastAPI** for backend API and WebSockets
- **Jinja2** for HTML templating
- **WebSockets** for real-time communication
- **Chart.js** for data visualization
- **C (GCC)** for low-level packet capture

## Contributing
Feel free to submit issues or pull requests to improve this project.

## License
This project is licensed under the GLPv3 License.

