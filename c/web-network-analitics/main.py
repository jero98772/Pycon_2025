from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import asyncio
import json
import os
from collections import Counter
from typing import List, Dict
import re

app = FastAPI()

# Set up templates directory for serving the HTML
templates = Jinja2Templates(directory="templates")


# Connection manager for WebSockets
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Packet processing
class PacketAnalyzer:
    def __init__(self):
        self.ip_counter = Counter()
        self.protocol_counter = Counter()
        self.current_packet_id = 0

    def parse_packet_line(self, line):
        pattern = r'Packet (\d+): ([\d\.]+) -> ([\d\.]+), Src MAC: ([\w:]+), Dst MAC: ([\w:]+), Protocol: (\d+) (.+)'
        match = re.match(pattern, line)
        
        if match:
            packet_id, src_ip, dst_ip, src_mac, dst_mac, protocol, hostname = match.groups()
            
            # Update counters
            self.ip_counter[src_ip] += 1
            self.protocol_counter[protocol] += 1
            
            return {
                "id": packet_id,
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_mac": src_mac,
                "dst_mac": dst_mac,
                "protocol": protocol,
                "hostname": hostname
            }
        return None

    def get_ip_counts(self, top_n=10):
        return dict(self.ip_counter.most_common(top_n))
    
    def get_protocol_counts(self):
        # Map protocol numbers to names for better readability
        protocol_names = {
            '1': 'ICMP',
            '6': 'TCP',
            '17': 'UDP',
            '128': 'Other'
        }
        
        result = {}
        for proto, count in self.protocol_counter.items():
            name = protocol_names.get(proto, f"Protocol {proto}")
            result[name] = count
        
        return result

packet_analyzer = PacketAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Handle client commands
            try:
                message = json.loads(data)
                if message.get("action") == "start_capture":
                    duration = message.get("duration", 30)
                    # Start capture in a separate task
                    asyncio.create_task(run_packet_capture(duration))
                    
            except json.JSONDecodeError:
                # Simple ping or non-JSON message
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def run_packet_capture(duration: int):
    """Run the packet capture program as a subprocess"""
    await manager.broadcast(json.dumps({
        "type": "status",
        "message": f"Starting packet capture for {duration} seconds..."
    }))
    
    # Reset counters for new capture
    packet_analyzer.ip_counter.clear()
    packet_analyzer.protocol_counter.clear()
    
    # Run the packet capture program
    try:
        # Remove old capture file if it exists
        if os.path.exists("capture.txt"):
            os.remove("capture.txt")
            
        # Start the process
        process = await asyncio.create_subprocess_shell(
            f"./packet_capture -t {duration} -o capture.txt",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for the program to start and create the file
        await asyncio.sleep(1)
        
        # Start reading the file as it's being written
        await manager.broadcast(json.dumps({
            "type": "status",
            "message": f"Capturing packets... ({duration} seconds remaining)"
        }))
        
        # Set up file monitoring
        await monitor_capture_file(duration)
        
    except Exception as e:
        await manager.broadcast(json.dumps({
            "type": "status",
            "message": f"Error: {str(e)}"
        }))

async def monitor_capture_file(duration: int):
    """Monitor the capture file for new data"""
    start_time = asyncio.get_event_loop().time()
    file_position = 0
    
    # Create empty file if it doesn't exist yet
    if not os.path.exists("capture.txt"):
        open("capture.txt", "w").close()
    
    while asyncio.get_event_loop().time() - start_time < duration + 2:  # Add 2 sec buffer
        try:
            with open("capture.txt", "r") as f:
                f.seek(file_position)
                new_lines = f.readlines()
                file_position = f.tell()
                
                for line in new_lines:
                    if line.strip():
                        packet = packet_analyzer.parse_packet_line(line.strip())
                        if packet:
                            # Send packet info to all connected clients
                            await manager.broadcast(json.dumps({
                                "packet": packet,
                                "ip_counts": packet_analyzer.get_ip_counts(),
                                "protocol_counts": packet_analyzer.get_protocol_counts()
                            }))
            
            # Update status with remaining time
            elapsed = asyncio.get_event_loop().time() - start_time
            remaining = max(0, int(duration - elapsed))
            if remaining % 5 == 0 or remaining <= 5:  # Update every 5 seconds or during final countdown
                await manager.broadcast(json.dumps({
                    "type": "status",
                    "message": f"Capturing packets... ({remaining} seconds remaining)"
                }))
                
            await asyncio.sleep(0.5)  # Check for updates every 0.5 seconds
            
        except Exception as e:
            print(f"Error reading capture file: {e}")
            await asyncio.sleep(1)
    
    await manager.broadcast(json.dumps({
        "type": "status",
        "message": "Packet capture completed. Ready for next capture."
    }))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)