# 3D File System with Flask and Three.js

This project and a proof of concept of implements a 3D file system visualization using Flask for the backend API and Three.js for the frontend visualization. It connects to the operating system's API to retrieve file system information and presents it in an interactive 3D environment.

With the absolute path we know what files and folders are there, for each folder and file we display a 3D Cube

We pass the data from python flask, (will be very similar with fastapi and django, and other webframeworks in other languages to pass the data to the fronend)

The url will be our absolute path

From js we get that data and do animations with threejs, rotate the camara, make add names to the cubics , make them clickable

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/jero98772/3Dfilesystem
   cd 3Dfilesystem
   ```

2. Install Flask (if not already installed):
   ```bash
   pip install Flask
   ```

## Usage

1. Start the Flask server:
   ```bash
   python main.py
   ```

2. Open your web browser and go to `http://localhost:5000` to view the 3D file system visualization.

## Pictures


![](https://github.com/jero98772/3Dfilesystem/blob/main/pictures/2024-07-09-092439_1920x1080_scrot.png)
![](https://github.com/jero98772/3Dfilesystem/blob/main/pictures/2024-07-09-094901_1920x1080_scrot.png)

## Features

- **Interactive 3D Visualization:** Utilizes Three.js to create an interactive and visually appealing representation of the file system.
- **Backend API:** Flask serves as the backend to connect with the operating system's API and retrieve file system information.
- **File Navigation:** Users can navigate through directories, view file details, and interact with files and folders in the 3D environment.

## Technologies Used

- **Flask:** Python web framework used for building the backend API.
- **Three.js:** JavaScript library for creating 3D graphics in the browser.
- **Operating System API:** Interface with the OS to retrieve file system data.

## Contributing

Contributions are welcome! Fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the [GPLv3 License]().

