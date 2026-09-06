import subprocess
import wmi

def unblock_all():
    c = wmi.WMI()
    print("Scanning for disabled USBSTOR devices...")
    disabled_devices = []
    
    # Query all USBSTOR devices
    for dev in c.query("SELECT * FROM Win32_PnPEntity WHERE PNPDeviceID LIKE 'USBSTOR%'"):
        # ConfigManagerErrorCode 22 means disabled
        if dev.ConfigManagerErrorCode == 22:
            print(f"Found disabled device: {dev.Caption} ({dev.PNPDeviceID})")
            disabled_devices.append(dev.PNPDeviceID)

    if not disabled_devices:
        print("No disabled USB devices found.")
        return

    for instance_id in disabled_devices:
        print(f"Enabling {instance_id}...")
        cmd = f'powershell -Command "Enable-PnpDevice -InstanceId \'{instance_id}\' -Confirm:$false"'
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Successfully re-enabled {instance_id}")
            else:
                print(f"Failed to enable {instance_id}: {result.stderr}")
        except Exception as e:
            print(f"Error enabling {instance_id}: {e}")

if __name__ == '__main__':
    unblock_all()
