from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket

import jpype
import jpype.imports
from jpype.types import *

app = FastAPI()
jpype.startJVM(classpath=['javafiles'])

# Import Java classes
ROM = jpype.JClass('ROM')
RAM = jpype.JClass('RAM')
CPU = jpype.JClass('CPU')
ALU = jpype.JClass('ALU')

# Create ROM and RAM instances
rom = ROM(8, 16)
sizeram = 32767
ram = RAM(sizeram)

FILE="rom.txt"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust to your frontend's URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def writetxt(name,content):
    """
    writetxt(name,content) , write in txt file something  
    """
    content =str(content)
    with open(name, 'w') as file:
        file.write(content)
        file.close()

def readfilestr(name):
    """
    readtxtstr(name) , return txt content as string
    """
    content = ""
    with open(name, 'r') as file:
        for i in file.readlines():
            content += str(i).replace("\n","")
    return content

def contains_only_binary_chars(s):
    for char in s:
        if char in "10\n":
            return False
    return True


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Wait for incoming message from the websocket client (React app)
        message = await websocket.receive_text()
        if contains_only_binary_chars(message):
            message="Sorry the input must be just 1 and 0"
        else:
            writetxt(FILE,message)        
            try:
                rom.loadRomFromFile(FILE)
                cpu = CPU(rom, ram)
                message=cpu.executeInstructions()
            except:
                message="Sorry the input must be just 1 and 0"

        # Process the message or send it back, depending on your needs
        await websocket.send_text(f"Received: {message}")

# Start the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
#jpype.shutdownJVM()
