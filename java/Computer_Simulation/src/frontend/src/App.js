import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [receivedMessage, setReceivedMessage] = useState('');
  const [connected, setConnected] = useState(false);
  const [socketError, setSocketError] = useState('');

  // Establish WebSocket connection
  const socket = new WebSocket('ws://localhost:8000/ws');

  // Handle connection open
  socket.onopen = () => {
    setConnected(true);
    setSocketError('');
  };

  // Handle connection close
  socket.onclose = () => {
    setConnected(false);
  };

  // Handle errors
  socket.onerror = (error) => {
    setSocketError('WebSocket error: ' + error);
  };

  // Handle messages from the server
  socket.onmessage = (event) => {
    console.log('Message from server:', event.data);
    setReceivedMessage(event.data); // Update receivedMessage state with event.data
  };

  // Function to send message to server
  const sendMessage = () => {
    socket.send(inputText);
    setInputText('');
  };

  return (
    <div className="app-container">
      <div className="panel">
        <div className="header">
          <h1 className="title">Industrial WebSocket Communication</h1>
          <div className={`status ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? 'Connected' : 'Disconnected'}
          </div>
        </div>
        <div className="content">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={8}
            placeholder="0000000000000000
1111110000010000
0000000000000001
1111000010010000
0000000000010001
1110000010010000
0000000000000010
1110001100001000"
            className="input-field"
          />
          <button onClick={sendMessage} className="send-button">
            Send
          </button>
          {socketError && <div className="error">{socketError}</div>}
        </div>
      </div>
      <div className="message-panel">
        <h2 className="subtitle">Received Message:</h2>
        <div className="message-content">{receivedMessage}</div>
      </div>
    </div>
  );
}

export default App;
