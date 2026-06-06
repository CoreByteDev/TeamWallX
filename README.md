# TeamWallX Pongo Loader

A lightweight Python script to communicate with pongoOS over USB, send custom Kernel Patchfinders (KPF), and boot jailbroken iOS environments. 

## Prerequisites

Before running the loader, you need to install system dependencies for USB communication.

### macOS
Install libusb using Homebrew:
brew install libusb

### Linux (Ubuntu/Debian)
Install libusb-dev:
sudo apt update
sudo apt install libusb-1.0-0-dev

### Python Dependencies
Install the required python library:
pip install pyusb

## Repository Structure

Ensure your local folder layout matches this structure:
├── loader.py
├── requirements.txt
└── bin/
    └── checkra1n-kpf.bin

## How to Use

1. Run your checkm8 exploit tool to kick the target device into DFU and load the pongoOS shell.
2. Ensure the iPhone screen displays the pongoOS text/logo interface.
3. Open your terminal, navigate to this project folder, and run the script:

sudo python3 loader.py bin/checkra1n-kpf.bin

*Note: sudo is required on Linux systems to grant Python direct permission to access the raw USB interface.*

## Project Flow
* Connects to Apple USB Vendor ID (0x05ac) and pongoOS Product ID (0x4141).
* Issues the modload command to prepare the environment.
* Streams the target .bin file across Endpoint 2 via bulk write.
* Fires the bootx instruction to execute patches and boot the OS.

 Made By CoreByteDev
