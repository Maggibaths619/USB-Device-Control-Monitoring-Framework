"""
main.py - USB Device Control & Monitoring Framework
Entry point. Requires Administrator privileges on Windows for device blocking.

Usage:
    python main.py              # Start monitoring
    python main.py --report     # Generate report from existing logs and exit
"""
import time
import sys
import ctypes
import argparse
import json
import os
from modules.logger import get_logger
from modules.policy_engine import PolicyEngine
from modules.usb_monitor import USBMonitor
from modules.enforcer import DeviceEnforcer
from modules.file_auditor import FileAuditor
from modules.reporter import Reporter
from modules.spoof_detector import SpoofDetector
from modules.notifier import (
    alert_authorized_device,
    alert_unauthorized_device,
    alert_spoofed_device
)

logger = get_logger("Main")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


class USBFramework:
    def __init__(self):
        self.policy_engine = PolicyEngine()
        self.file_auditor = FileAuditor()
        self.spoof_detector = SpoofDetector()
        self.notifications_enabled = self.policy_engine.get_setting("enable_notifications", True)
        self.spoof_detection_enabled = self.policy_engine.get_setting("enable_spoofing_detection", True)
        self.file_audit_enabled = self.policy_engine.get_setting("file_audit_on_allowed", True)
        self.report_on_exit = self.policy_engine.get_setting("report_on_exit", True)

        self.usb_monitor = USBMonitor(
            on_connect=self.on_device_connect,
            on_disconnect=self.on_device_disconnect
        )
        self.active_devices = {}
        self.state_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'active_devices.json')
        self._update_state_file()

    def _update_state_file(self):
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.active_devices.values()), f, indent=4)
        except Exception as e:
            logger.error(f"Failed to update state file: {e}")

    def on_device_connect(self, device_info):
        vid = device_info.get("vendor_id")
        pid = device_info.get("product_id")
        serial = device_info.get("serial_number")
        instance_id = device_info.get("instance_id")
        drive_letters = device_info.get("drive_letters", [])
        caption = device_info.get("caption", "Unknown Device")
        
        self.active_devices[instance_id] = device_info
        self._update_state_file()

        logger.info("=" * 60)
        logger.info(f"USB CONNECT EVENT")
        logger.info(f"  Device : {caption}")
        logger.info(f"  VID    : {vid}  |  PID: {pid}")
        logger.info(f"  Serial : {serial}")
        logger.info(f"  Drives : {drive_letters}")
        logger.info(f"  ID     : {instance_id}")
        logger.info("=" * 60)

        # ── Step 1: Check explicit blocklist first ─────────────────────
        if self.policy_engine.is_explicitly_blocked(vid, pid, serial):
            logger.warning(f"[BLOCKLISTED] Device VID:{vid} PID:{pid} is on the explicit blocklist.")
            DeviceEnforcer.block_device(instance_id)
            if self.notifications_enabled:
                alert_unauthorized_device(vid, pid, serial, caption)
            return

        # ── Step 2: Spoofing detection ─────────────────────────────────
        if self.spoof_detection_enabled:
            is_suspicious, reasons = self.spoof_detector.analyze(vid, pid, serial)
            if is_suspicious:
                logger.warning(f"[SPOOF ALERT] Blocking suspicious device. Reasons: {reasons}")
                DeviceEnforcer.block_device(instance_id)
                if self.notifications_enabled:
                    alert_spoofed_device(vid, pid, reasons)
                return

        # ── Step 3: Allowlist check ────────────────────────────────────
        if self.policy_engine.is_authorized(vid, pid, serial):
            logger.info(f"[AUTHORIZED] Device allowed: {caption}")
            if self.notifications_enabled:
                alert_authorized_device(caption, drive_letters)

            if self.file_audit_enabled:
                for letter in drive_letters:
                    drive_path = f"{letter}\\"
                    self.file_auditor.start_monitoring(drive_path)
        else:
            # ── Step 4: Unknown device — not on any list ───────────────
            logger.warning(f"[UNAUTHORIZED] Unknown device VID:{vid} PID:{pid} — blocking.")
            DeviceEnforcer.block_device(instance_id)
            if self.notifications_enabled:
                alert_unauthorized_device(vid, pid, serial, caption)

    def on_device_disconnect(self, device_info):
        instance_id = device_info.get("instance_id", "Unknown")
        if instance_id in self.active_devices:
            del self.active_devices[instance_id]
            self._update_state_file()
        logger.info(f"[DISCONNECT] Device removed: {instance_id}")

    def run(self):
        logger.info("========================================================")
        logger.info("   USB Device Control & Monitoring Framework            ")
        logger.info("   Initializing...                                      ")
        logger.info("========================================================")

        logger.info("[*] Starting USB Monitor... Press Ctrl+C to stop and generate report.")
        self.usb_monitor.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping framework on user request...")
            self.usb_monitor.stop()
            self.file_auditor.stop_all()
            
            # Clear state on exit
            self.active_devices = {}
            self._update_state_file()

            if self.report_on_exit:
                reporter = Reporter()
                report_path = reporter.generate_report()
                logger.info(f"[>] Session report saved to: {report_path}")

            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="USB Device Control & Monitoring Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              Start monitoring (requires Admin)
  python main.py --report     Generate a report from existing logs and exit
        """
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate a security report from existing log files and exit."
    )
    args = parser.parse_args()

    if args.report:
        reporter = Reporter()
        path = reporter.generate_report()
        print(f"Report generated: {path}")
        sys.exit(0)

    framework = USBFramework()
    framework.run()


if __name__ == "__main__":
    main()
