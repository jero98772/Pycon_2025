import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const ProcessList = () => {
    const [processes, setProcesses] = useState([]);

    useEffect(() => {
        const socket = io('http://localhost:5000');
        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('update', (data) => {
            setProcesses(data);
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    return (
        <div>
            <h1>Current Processes</h1>
            <table>
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>User</th>
                        <th>Name</th>
                        <th>Status</th>
                        <th>Memory</th>
                        <th>CPU Usage</th>
                    </tr>
                </thead>
                <tbody>
                    {processes.map(process => (
                        <tr key={process.pid}>
                            <td>{process.pid}</td>
                            <td>{process.user}</td>
                            <td>{process.name}</td>
                            <td>{process.status}</td>
                            <td>{process.memory} KB</td>
                            <td>{process.cpu_usage}%</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ProcessList;
