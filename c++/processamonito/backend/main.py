from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import process_monitor
import time
from threading import Thread, Event

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

thread = Thread()
thread_stop_event = Event()

class ProcessMonitorThread(Thread):
    def __init__(self):
        self.delay = 5
        super(ProcessMonitorThread, self).__init__()

    def get_processes(self):
        monitor = process_monitor.ProcessMonitor()
        return monitor.get_processes()

    def run(self):
        while not thread_stop_event.is_set():
            processes = self.get_processes()
            socketio.emit('update', [process.to_dict() for process in processes])
            time.sleep(self.delay)

@app.route('/api/processes', methods=['GET'])
def get_processes():
    processes = process_monitor.get_processes()
    return jsonify([process.to_dict() for process in processes])

@socketio.on('connect')
def handle_connect():
    global thread
    print('Client connected')
    if not thread.is_alive():
        thread = ProcessMonitorThread()
        thread.start()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
