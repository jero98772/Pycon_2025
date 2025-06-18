python -m venv env
source env/bin/activate
pip install fastapi uvicorn websockets jinja2 
gcc -o packet_capture sniffer.c
sudo setcap cap_net_raw+eip ./packet_capture 
 