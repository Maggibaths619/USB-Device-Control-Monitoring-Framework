import json
import os
from modules.logger import get_logger

logger = get_logger("PolicyEngine")

class PolicyEngine:
    def __init__(self, config_path=None):
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            self.config_path = os.path.join(base_dir, 'config', 'allowlist.json')
        else:
            self.config_path = config_path

        self.authorized_devices = []
        self.blocked_devices = []
        self.settings = {}
        self.load_policy()

    def load_policy(self):
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                self.authorized_devices = data.get('authorized_devices', [])
                self.blocked_devices = data.get('blocked_devices', [])
                self.settings = data.get('settings', {})
                logger.info(
                    f"Policy loaded: {len(self.authorized_devices)} authorized, "
                    f"{len(self.blocked_devices)} explicitly blocked."
                )
        except FileNotFoundError:
            logger.error(f"Policy file not found: {self.config_path}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding policy file: {self.config_path}")

    def save_policy(self):
        """Persist changes to the policy file."""
        try:
            data = {
                "authorized_devices": self.authorized_devices,
                "blocked_devices": self.blocked_devices,
                "settings": self.settings
            }
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("Policy file saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save policy: {e}")

    def get_setting(self, key, default=True):
        return self.settings.get(key, default)

    def _match_device(self, device_list, vid, pid, serial=None):
        """Generic matcher for both allowlist and blocklist."""
        vid = (vid or "").lower()
        pid = (pid or "").lower()
        sn = (serial or "").upper()

        for device in device_list:
            auth_vid = device.get('vendor_id', '').lower()
            auth_pid = device.get('product_id', '').lower()

            if auth_vid == vid and auth_pid == pid:
                auth_sn = device.get('serial_number', '').upper()
                if auth_sn and auth_sn != "N/A":
                    if sn == auth_sn:
                        return True
                else:
                    return True
        return False

    def is_explicitly_blocked(self, vendor_id, product_id, serial_number=None):
        """Returns True if the device is on the explicit blocklist."""
        result = self._match_device(self.blocked_devices, vendor_id, product_id, serial_number)
        if result:
            logger.warning(f"Device VID:{vendor_id} PID:{product_id} found on BLOCKLIST.")
        return result

    def is_authorized(self, vendor_id, product_id, serial_number=None):
        """Returns True if the device is on the allowlist."""
        return self._match_device(self.authorized_devices, vendor_id, product_id, serial_number)

    def add_authorized_device(self, vendor_id, product_id, serial_number="N/A", description="Manually Added"):
        entry = {
            "vendor_id": vendor_id.lower(),
            "product_id": product_id.lower(),
            "serial_number": serial_number.upper() if serial_number != "N/A" else "N/A",
            "description": description
        }
        self.authorized_devices.append(entry)
        self.save_policy()
        logger.info(f"Added to allowlist: {entry}")

    def remove_authorized_device(self, vendor_id, product_id):
        before = len(self.authorized_devices)
        self.authorized_devices = [
            d for d in self.authorized_devices
            if not (d.get('vendor_id', '').lower() == vendor_id.lower()
                    and d.get('product_id', '').lower() == product_id.lower())
        ]
        removed = before - len(self.authorized_devices)
        if removed:
            self.save_policy()
            logger.info(f"Removed {removed} device(s) VID:{vendor_id} PID:{product_id} from allowlist.")
        return removed

    def add_blocked_device(self, vendor_id, product_id, serial_number="N/A", description="Manually Blocked"):
        entry = {
            "vendor_id": vendor_id.lower(),
            "product_id": product_id.lower(),
            "serial_number": serial_number.upper() if serial_number != "N/A" else "N/A",
            "description": description
        }
        self.blocked_devices.append(entry)
        self.save_policy()
        logger.info(f"Added to blocklist: {entry}")
