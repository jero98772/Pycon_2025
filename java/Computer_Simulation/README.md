# Computer Simulation

This project contains a frontend application built with React and a backend application written in Python. The instructions below will guide you through setting up and running both the frontend and backend applications.

## Prerequisites

Before you begin, ensure you have the following software installed on your system:

- Node.js and npm (for the React frontend)
- Python 3.x and pip (for the Python backend)

## Getting Started

Follow these steps to set up and run the applications.

### Frontend

1. Navigate to the `frontend` directory:
    ```bash
    cd src/frontend
    ```

2. Install the dependencies:
    ```bash
    npm install
    ```

3. Start the React application:
    ```bash
    npm start
    ```

### Backend

1. Navigate to the `backend` directory:
    ```bash
    cd src/backend
    ```

2. Install the Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Python script:
    ```bash
    python main.py
    ```

## Running the Applications

Once you have set up both the frontend and backend, you can run them simultaneously.

1. Open a terminal window and follow the steps in the "Frontend" section to start the React application.
2. Open another terminal window and follow the steps in the "Backend" section to run the Python script.

## Sample Input

```plaintext
1110101010101010
0001101010101010
...
```

This file should contain binary instructions, each line representing one instruction.

### Sample Output

```plaintext
go register A
ALU
registerA: 32767
registerD: 0
ram: 0
finish
```

## Additional Information

- Ensure that the frontend and backend applications are running on different ports to avoid conflicts.
- If you encounter any issues, refer to the documentation of the respective technologies or seek help from online communities.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

