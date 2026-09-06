# 🔒 USB Device Control & Monitoring Framework

A Python-based cybersecurity tool for Windows that detects, monitors, and restricts unauthorized USB device activity in real-time.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Policy Management](#policy-management)
- [Architecture](#architecture)
- [Security Techniques](#security-techniques)

---

## Overview

USB-based attacks remain one of the most common physical and insider threats:

- **BadUSB** — Microcontrollers emulating keyboards or network adapters
- **Data exfiltration** — Copying sensitive files to removable storage
- **Malware introduction** — Auto-running malicious payloads
- **Device spoofing** — Impersonating trusted USB hardware

This framework provides a real-time defense layer by monitoring USB connections, enforcing a device policy (allowlist + blocklist), auditing file transfers, and generating security reports.

---

## Features

| Feature | Description |
|---|---|
| 🔌 **Real-time USB Detection** | Polls Windows WMI every 2 seconds to detect device connections/removals |
| ✅ **Allowlist Enforcement** | Devices on the allowlist (by VID, PID, Serial) are permitted |
| 🛑 **Blocklist Enforcement** | Devices explicitly on the blocklist are blocked immediately |
| 🚫 **Auto-Block Unauthorized** | Unknown devices not on any list are automatically blocked via PowerShell |
| 🕵️ **Spoof Detection** | Analyzes serial numbers and VID:PID against known BadUSB fingerprints |
| 📁 **File Transfer Auditing** | Tracks file create/modify/delete/move on authorized USB drives |
| 🔔 **Windows Notifications** | Toast notifications for blocked, spoofed, and authorized devices |
| 📄 **Security Report** | Generates a Markdown audit report on exit |
| ⚙️ **Policy CLI** | Command-line tool to manage allowlist and blocklist |

---

## Project Structure

```
USB Device Control & Monitoring Framework/
│
├── config/
│   └── allowlist.json          # Policy: authorized + blocked devices + settings
│
├── logs/                       # Auto-generated at runtime
│   ├── usb_audit.log           # Rolling log file (5MB max, 3 backups)
│   └── usb_security_report_*.md # Session security reports
│
├── modules/
│   ├── __init__.py
│   ├── enforcer.py             # PowerShell-based device blocking
│   ├── file_auditor.py         # watchdog-based file activity monitoring
│   ├── logger.py               # Centralized logging (file + console)
│   ├── notifier.py             # Windows toast notifications (winotify)
│   ├── policy_engine.py        # Allowlist/blocklist CRUD + validation
│   ├── reporter.py             # Security report generation
│   ├── spoof_detector.py       # BadUSB fingerprinting + serial analysis
│   └── usb_monitor.py          # WMI USB event polling thread
│
├── main.py                     # Application entry point
├── manage_policy.py            # CLI policy manager
├── install.bat                 # One-click dependency installer
├── start_monitor.bat           # Start monitoring (prompts for Admin)
└── requirements.txt
```

---

## Requirements

- **OS**: Windows 10 / 11
- **Python**: 3.8+
- **Privileges**: Administrator (required for device blocking)

### Python Dependencies
```
wmi
pywin32
watchdog
winotify
```

---

## Installation

**1. Clone / download the project.**

**2. Run the installer (double-click or from terminal):**
```bat
install.bat
```

Or manually:
```bash
pip install -r requirements.txt
```

---

## Usage

### Start the Monitor

> ⚠️ **Must run as Administrator** for device blocking to work.

**Option A** — Double-click `start_monitor.bat` (Right-click → Run as Administrator)

**Option B** — Administrator PowerShell/CMD:
```bash
python main.py
```

**Option C** — Generate report from existing logs without starting the monitor:
```bash
python main.py --report
```

**Stop the monitor** with `Ctrl+C`. A security report is automatically generated in `logs/`.

### What You'll See

```
2026-09-05 19:45:01 - INFO - ╔══════════════════════════════╗
2026-09-05 19:45:01 - INFO - ║  USB Device Control Framework ║
2026-09-05 19:45:01 - INFO - ╚══════════════════════════════╝
2026-09-05 19:45:01 - INFO - 🔍 Starting USB Monitor...
2026-09-05 19:45:42 - INFO - USB CONNECT EVENT
2026-09-05 19:45:42 - INFO -   Device : Kingston DataTraveler 3.0
2026-09-05 19:45:42 - INFO -   VID    : 0951  |  PID: 1666
2026-09-05 19:45:42 - INFO -   Serial : E0D55EA573D3F141392A0065
2026-09-05 19:45:42 - INFO - [AUTHORIZED] Device allowed: Kingston DataTraveler 3.0
2026-09-05 19:46:10 - INFO - [FILE CREATED] E:\Documents\report.pdf
```

---

## Policy Management

Use `manage_policy.py` to manage your device policy without editing JSON manually.

### View all devices
```bash
python manage_policy.py list
```

### Add a device to the allowlist
```bash
python manage_policy.py add-allow --vid 0951 --pid 1666 --serial ABCDEF123456 --desc "My Kingston USB"
```

### Remove a device from the allowlist
```bash
python manage_policy.py remove-allow --vid 0951 --pid 1666
```

### Add a device to the blocklist
```bash
python manage_policy.py add-block --vid 03eb --pid 2042 --desc "Hak5 Rubber Ducky"
```

### View current settings
```bash
python manage_policy.py show-settings
```

---

## Architecture

```
                ┌─────────────────────────────────┐
                │          main.py (Orchestrator)  │
                └────────────┬────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────▼──────┐ ┌────▼────┐  ┌──────▼──────┐
       │ usb_monitor  │ │ policy  │  │   notifier   │
       │  (WMI Thread)│ │ engine  │  │  (Toasts)   │
       └──────┬───────┘ └────┬────┘  └─────────────┘
              │              │
    ┌─────────▼──┐   ┌───────▼──────────┐
    │   spoof    │   │    enforcer       │
    │  detector  │   │ (PowerShell Block)│
    └────────────┘   └──────────────────┘
              │
       ┌──────▼──────┐
       │ file_auditor │
       │  (watchdog)  │
       └──────┬───────┘
              │
       ┌──────▼───────┐
       │    logger    │──► logs/usb_audit.log
       │   reporter   │──► logs/usb_security_report_*.md
       └──────────────┘
```

---

## Security Techniques

| Technique | Implementation |
|---|---|
| Device Fingerprinting | Vendor ID + Product ID + Serial Number extraction via WMI |
| Allowlist Policy | JSON-based policy enforced at connection time |
| Blocklist Policy | Explicit deny list checked before allowlist |
| BadUSB Detection | VID:PID matched against known attack hardware database |
| Serial Analysis | Regex-based detection of suspicious/forged serial numbers |
| Hardware Enforcement | `Disable-PnpDevice` PowerShell command via subprocess |
| File Auditing | `watchdog` library monitors create/modify/delete/move events |
| SHA-256 Hashing | Available in `file_auditor.py` for file integrity verification |
| Audit Logging | Rotating log files (5MB max, 3 backups) |
| Security Reporting | Markdown reports summarizing all session events |

---

## Learning Outcomes

Working through this project teaches you:
- How USB devices communicate with Windows via WMI/PnP
- How attackers abuse USB (BadUSB, data theft, HID attacks)
- Allowlist/blocklist policy design for endpoint security
- File system auditing techniques
- Hardware-level enforcement using PowerShell from Python
- Real-world Blue Team monitoring concepts
