import wmi
import pythoncom
import re
import time
from threading import Thread
from modules.logger import get_logger

logger = get_logger("USBMonitor")


class USBMonitor(Thread):
    def __init__(self, on_connect, on_disconnect):
        super().__init__()
        self.daemon = True
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.running = True
        self.known_devices = set()

    def extract_vid_pid_serial(self, device_id):
        """
        Extracts VID, PID, and Serial from a PNPDeviceID string.
        Handles both:
          - USB\\VID_0781&PID_5567\\ABCDEF      (USB hub layer)
          - USBSTOR\\DISK&VEN_...\\SERIAL&0      (USBSTOR layer)
        """
        vid, pid, serial = None, None, None

        vid_match = re.search(r'VID_([0-9A-Fa-f]{4})', device_id, re.IGNORECASE)
        if vid_match:
            vid = vid_match.group(1)

        pid_match = re.search(r'PID_([0-9A-Fa-f]{4})', device_id, re.IGNORECASE)
        if pid_match:
            pid = pid_match.group(1)

        # Serial is the last backslash-separated segment, minus any trailing &0
        parts = device_id.split('\\')
        if len(parts) >= 3:
            last = parts[-1].split('&')[0]   # strip trailing &0, &MI_00, etc.
            if last and not last.startswith('MI_'):
                serial = last

        return vid, pid, serial

    def lookup_usb_vid_pid(self, c, serial):
        """
        For USBSTOR devices the DiskDrive PNPDeviceID has no VID_/PID_.
        Query only USB-class PnP entities (much faster than scanning all entities)
        and match by serial number to get the VID and PID.
        """
        if not serial:
            return None, None
        try:
            # Targeted WQL query — only USB VID/PID devices, not the full PnP list
            usb_entities = c.query(
                "SELECT PNPDeviceID FROM Win32_PnPEntity "
                "WHERE PNPDeviceID LIKE 'USB%VID_%'"
            )
            for pnp in usb_entities:
                pnp_id = pnp.PNPDeviceID or ''
                if serial.upper() in pnp_id.upper():
                    vid_m = re.search(r'VID_([0-9A-Fa-f]{4})', pnp_id, re.IGNORECASE)
                    pid_m = re.search(r'PID_([0-9A-Fa-f]{4})', pnp_id, re.IGNORECASE)
                    if vid_m and pid_m:
                        return vid_m.group(1), pid_m.group(1)
        except Exception as e:
            logger.error(f"VID/PID lookup error: {e}")
        return None, None

    def get_device_info(self, c, drive):
        vid, pid, serial = self.extract_vid_pid_serial(drive.PNPDeviceID)
        if not vid or not pid:
            vid, pid = self.lookup_usb_vid_pid(c, serial)
        drive_letters = []
        for partition in drive.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                drive_letters.append(logical_disk.DeviceID)
        return {
            "vendor_id": vid,
            "product_id": pid,
            "serial_number": serial,
            "instance_id": drive.PNPDeviceID,
            "drive_letters": drive_letters,
            "caption": drive.Caption
        }

    def run(self):
        logger.info("Starting USB Monitor Thread...")
        pythoncom.CoInitialize()

        c = wmi.WMI()

        # Snapshot devices already connected at startup and process them
        for drive in c.Win32_DiskDrive(InterfaceType="USB"):
            self.known_devices.add(drive.PNPDeviceID)
            device_info = self.get_device_info(c, drive)
            logger.info(f"[BASELINE] USB Device Found: {device_info['caption']}")
            self.on_connect(device_info)

        logger.info(f"Baseline: {len(self.known_devices)} USB drive(s) processed at startup.")

        while self.running:
            try:
                current_devices = set()
                usb_drives = c.Win32_DiskDrive(InterfaceType="USB")

                for drive in usb_drives:
                    current_devices.add(drive.PNPDeviceID)

                    if drive.PNPDeviceID not in self.known_devices:
                        device_info = self.get_device_info(c, drive)
                        logger.info(
                            f"New USB Device Detected: {device_info['caption']} "
                            f"(VID:{device_info['vendor_id']} PID:{device_info['product_id']} Serial:{device_info['serial_number']})"
                        )
                        self.on_connect(device_info)

                # Detect disconnected devices
                for removed_device in self.known_devices - current_devices:
                    logger.info(f"[DISCONNECT] USB Device removed: {removed_device}")
                    self.on_disconnect({"instance_id": removed_device})

                self.known_devices = current_devices

            except Exception as e:
                logger.error(f"Error in USB Monitor loop: {str(e)}")

            time.sleep(2)  # Poll every 2 seconds

    def stop(self):
        self.running = False
