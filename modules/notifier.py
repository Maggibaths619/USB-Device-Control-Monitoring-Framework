"""
notifier.py - Windows toast notification module for the USB Framework.

Uses winotify (preferred) or falls back to a MessageBox via ctypes.
Install: pip install winotify
"""
import os
from modules.logger import get_logger

logger = get_logger("Notifier")

APP_NAME = "USB Security Monitor"
ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "usb_icon.ico")


def _notify_winotify(title, message, severity="warning"):
    from winotify import Notification, audio
    icon = ICON_PATH if os.path.exists(ICON_PATH) else ""
    toast = Notification(
        app_id=APP_NAME,
        title=title,
        msg=message,
        icon=icon,
        duration="long"
    )
    if severity == "critical":
        toast.set_audio(audio.LoopingAlarm, loop=False)
    toast.show()


def _notify_messagebox(title, message):
    """Fallback: display a standard Windows message box."""
    import ctypes
    MB_ICONWARNING = 0x30
    ctypes.windll.user32.MessageBoxW(0, message, title, MB_ICONWARNING)


def send_notification(title, message, severity="warning", use_popup_fallback=False):
    """
    Send a desktop notification.

    Args:
        title (str): Notification title.
        message (str): Notification body.
        severity (str): 'info', 'warning', or 'critical'.
        use_popup_fallback (bool): If True, show a blocking MessageBox on failure.
    """
    try:
        _notify_winotify(title, message, severity)
        logger.info(f"Notification sent: [{severity.upper()}] {title}")
    except ImportError:
        logger.warning("winotify not installed. Falling back to console log only.")
        if use_popup_fallback:
            try:
                _notify_messagebox(title, message)
            except Exception as e:
                logger.error(f"MessageBox fallback also failed: {e}")
    except Exception as e:
        logger.error(f"Notification failed: {e}")


def alert_unauthorized_device(vid, pid, serial, caption="Unknown Device"):
    send_notification(
        title="⚠️ Unauthorized USB Detected & Blocked",
        message=f"Device: {caption}\nVID: {vid}  PID: {pid}\nSerial: {serial}\nDevice has been BLOCKED.",
        severity="critical"
    )


def alert_spoofed_device(vid, pid, reasons):
    reason_str = "; ".join(reasons)
    send_notification(
        title="🚨 Suspected USB Spoofing Detected",
        message=f"VID: {vid}  PID: {pid}\nReasons: {reason_str}",
        severity="critical"
    )


def alert_authorized_device(caption, drive_letters):
    drives = ", ".join(drive_letters) if drive_letters else "N/A"
    send_notification(
        title="✅ Authorized USB Connected",
        message=f"Device: {caption}\nDrive(s): {drives}\nFile auditing started.",
        severity="info"
    )
