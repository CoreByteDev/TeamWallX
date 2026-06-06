import sys
import time
import usb.core
import usb.util

# Apple Vendor ID and standard pongoOS Product ID
APPLE_VENDOR_ID = 0x05ac
PONGO_PRODUCT_ID = 0x4141

def send_pongo_command(device, command_string):
    """Sends a plain text instruction directly to the pongoOS terminal shell."""
    cmd_bytes = (command_string + "\n").encode('utf-8')
    try:
        # Request type 0x21, Request 1 sends string characters over USB control transfer
        device.ctrl_transfer(0x21, 1, 0, 0, cmd_bytes)
        time.sleep(0.15)  # Short delay for pongo to register the input buffer
        print(f"[>] Command sent: {command_string}")
    except Exception as e:
        print(f"[-] Failed to send command '{command_string}': {e}")

def upload_binary(device, file_path):
    """Prepares the device memory and pipes the binary payload across the USB bulk endpoint."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"[-] Failed to read file {file_path}: {e}")
        return False

    print(f"[*] Initializing connection buffers for {len(data)} byte payload...")
    # Request 4 clears the current transfer states and signals a data stream incoming
    device.ctrl_transfer(0x21, 4, 0, 0, 0)
    
    print("[*] Streaming data down Endpoint 2...")
    try:
        # Bulk write to Endpoint 2 is the standard transmission path for custom KPF modules
        device.write(2, data, timeout=15000)
        print("[+] Upload complete!")
        return True
    except usb.core.USBError as e:
        print(f"[-] USB upload failed: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 loader.py <path_to_kpf.bin>")
        return

    payload_path = sys.argv[1]

    print("[*] Scanning USB buses for TeamWallX Target Device...")
    dev = usb.core.find(idVendor=APPLE_VENDOR_ID, idProduct=PONGO_PRODUCT_ID)
    
    if dev is None:
        print("[-] Target not found. Ensure your hardware exploit pushed the device into pongoOS mode!")
        return

    # Claim the interface
    dev.set_configuration()
    print("[+] Interface claimed. Connected to pongoOS environment.")

    # Tell pongoOS to expect an external binary module load
    send_pongo_command(dev, "modload")

    # Upload the target payload 
    if upload_binary(dev, payload_path):
        print("[*] Executing payload patches...")
        
        # Issue boot execution command
        send_pongo_command(dev, "bootx")
        print("[+] Script sequence completed successfully.")

if __name__ == "__main__":
    main()
