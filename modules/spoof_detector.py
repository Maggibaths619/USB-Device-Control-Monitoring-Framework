import re
from modules.logger import get_logger

logger = get_logger("SpoofDetector")

# Known suspicious patterns that suggest a spoofed or emulated USB device.
# Real devices usually have serial numbers that are alphanumeric and consistent.
SUSPICIOUS_SERIAL_PATTERNS = [
    r'^0{6,}$',           # All zeros
    r'^f{6,}$',           # All Fs (common firmware default)
    r'^123456',           # Generic test serials
    r'^AAAAAA',           # Repeated trivial characters
    r'^[0-9]{1,3}$',      # Too-short numeric serial (real ones are usually longer)
]

# VID:PID pairs known to be associated with BadUSB or attack platforms
# Source: public threat intelligence lists
KNOWN_BADUSB_FINGERPRINTS = [
    {"vendor_id": "1234", "product_id": "5678", "note": "Generic BadUSB emulation"},
    {"vendor_id": "03eb", "product_id": "2042", "note": "Rubber Ducky (Hak5)"},
    {"vendor_id": "16d0", "product_id": "0753", "note": "MalDuino"},
    {"vendor_id": "f055", "product_id": "9800", "note": "O.MG Cable"},
]


class SpoofDetector:
    def __init__(self):
        self.suspicious_patterns = [re.compile(p, re.IGNORECASE) for p in SUSPICIOUS_SERIAL_PATTERNS]

    def _check_serial_suspicious(self, serial_number):
        """Checks if the serial number matches known suspicious patterns."""
        if not serial_number:
            return False, "No serial number reported"
        for pattern in self.suspicious_patterns:
            if pattern.match(serial_number):
                return True, f"Serial number '{serial_number}' matches suspicious pattern: {pattern.pattern}"
        return False, None

    def _check_known_badusb(self, vendor_id, product_id):
        """Checks if VID:PID matches a known BadUSB/attack hardware fingerprint."""
        vid = (vendor_id or "").lower()
        pid = (product_id or "").lower()
        for fp in KNOWN_BADUSB_FINGERPRINTS:
            if fp["vendor_id"].lower() == vid and fp["product_id"].lower() == pid:
                return True, fp["note"]
        return False, None

    def analyze(self, vendor_id, product_id, serial_number):
        """
        Analyzes a device for spoofing or impersonation indicators.
        Returns a tuple: (is_suspicious: bool, reasons: list[str])
        """
        reasons = []

        # Check 1: Known BadUSB hardware fingerprints
        is_badusb, note = self._check_known_badusb(vendor_id, product_id)
        if is_badusb:
            reasons.append(f"KNOWN BADUSB DEVICE: {note}")

        # Check 2: Suspicious serial number
        is_sus_serial, serial_reason = self._check_serial_suspicious(serial_number)
        if is_sus_serial:
            reasons.append(f"SUSPICIOUS SERIAL: {serial_reason}")

        # Check 3: No VID or PID at all (device hiding its identity)
        if not vendor_id or not product_id:
            reasons.append("MISSING VID/PID: Device did not report a Vendor or Product ID.")

        is_suspicious = len(reasons) > 0

        if is_suspicious:
            logger.warning(
                f"SPOOFING ALERT for VID:{vendor_id} PID:{product_id} Serial:{serial_number} "
                f"| Reasons: {'; '.join(reasons)}"
            )
        else:
            logger.info(
                f"Spoof check PASSED for VID:{vendor_id} PID:{product_id} Serial:{serial_number}"
            )

        return is_suspicious, reasons
