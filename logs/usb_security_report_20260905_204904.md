# USB Device Control & Monitoring Framework
## Security Audit Report

| Field | Value |
|---|---|
| Generated On | 2026-09-05 20:49:04 |
| Total Log Lines Analysed | 198 |
| Authorized Connections | 0 |
| Blocked / Unauthorized | 12 |
| Spoofing Alerts | 12 |
| Disconnections Logged | 8 |
| File Events Audited | 0 |

---

## 🛑 Blocked / Unauthorized Devices

- `2026-09-05 20:20:56,178 - WARNING - [Enforcer] - Attempting to block unauthorized device with Instance ID: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:20:56,200 - WARNING - [Enforcer] - Attempting to block unauthorized device with Instance ID: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:20:58,699 - INFO - [Enforcer] - Successfully blocked device: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:20:58,722 - INFO - [Enforcer] - Successfully blocked device: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:23,981 - WARNING - [Enforcer] - Attempting to block unauthorized device with Instance ID: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:24,148 - WARNING - [Enforcer] - Attempting to block unauthorized device with Instance ID: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:24,377 - WARNING - [Enforcer] - Attempting to block unauthorized device with Instance ID: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:24,495 - WARNING - [Enforcer] - Attempting to block unauthorized device with Instance ID: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:27,372 - INFO - [Enforcer] - Successfully blocked device: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:27,388 - INFO - [Enforcer] - Successfully blocked device: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:27,424 - INFO - [Enforcer] - Successfully blocked device: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:27,987 - INFO - [Enforcer] - Successfully blocked device: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`

---

## 🚨 Spoofing / BadUSB Alerts

- `2026-09-05 20:20:56,178 - WARNING - [SpoofDetector] - SPOOFING ALERT for VID:None PID:None Serial:None | Reasons: MISSING VID/PID: Device did not report a Vendor or Product ID.`
- `2026-09-05 20:20:56,178 - WARNING - [Main] - [SPOOF ALERT] Blocking suspicious device. Reasons: ['MISSING VID/PID: Device did not report a Vendor or Product ID.']`
- `2026-09-05 20:20:56,200 - WARNING - [SpoofDetector] - SPOOFING ALERT for VID:None PID:None Serial:None | Reasons: MISSING VID/PID: Device did not report a Vendor or Product ID.`
- `2026-09-05 20:20:56,200 - WARNING - [Main] - [SPOOF ALERT] Blocking suspicious device. Reasons: ['MISSING VID/PID: Device did not report a Vendor or Product ID.']`
- `2026-09-05 20:47:23,976 - WARNING - [SpoofDetector] - SPOOFING ALERT for VID:None PID:None Serial:None | Reasons: MISSING VID/PID: Device did not report a Vendor or Product ID.`
- `2026-09-05 20:47:23,980 - WARNING - [Main] - [SPOOF ALERT] Blocking suspicious device. Reasons: ['MISSING VID/PID: Device did not report a Vendor or Product ID.']`
- `2026-09-05 20:47:24,145 - WARNING - [SpoofDetector] - SPOOFING ALERT for VID:None PID:None Serial:None | Reasons: MISSING VID/PID: Device did not report a Vendor or Product ID.`
- `2026-09-05 20:47:24,146 - WARNING - [Main] - [SPOOF ALERT] Blocking suspicious device. Reasons: ['MISSING VID/PID: Device did not report a Vendor or Product ID.']`
- `2026-09-05 20:47:24,377 - WARNING - [SpoofDetector] - SPOOFING ALERT for VID:None PID:None Serial:None | Reasons: MISSING VID/PID: Device did not report a Vendor or Product ID.`
- `2026-09-05 20:47:24,377 - WARNING - [Main] - [SPOOF ALERT] Blocking suspicious device. Reasons: ['MISSING VID/PID: Device did not report a Vendor or Product ID.']`
- `2026-09-05 20:47:24,495 - WARNING - [SpoofDetector] - SPOOFING ALERT for VID:None PID:None Serial:None | Reasons: MISSING VID/PID: Device did not report a Vendor or Product ID.`
- `2026-09-05 20:47:24,495 - WARNING - [Main] - [SPOOF ALERT] Blocking suspicious device. Reasons: ['MISSING VID/PID: Device did not report a Vendor or Product ID.']`

---

## ✅ Authorized Device Connections

*No authorized devices connected during this period.*

---

## 📁 File Activity on Authorized Drives

*No file activity recorded.*

---

## 🔌 Device Disconnections

- `2026-09-05 20:20:51,353 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:20:51,429 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:21:01,019 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:21:01,096 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:29,658 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:29,735 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:29,845 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`
- `2026-09-05 20:47:30,433 - INFO - [Main] - [DISCONNECT] Device removed: USBSTOR\DISK&VEN_SANDISK&PROD_CRUZER_BLADE&REV_1.00\03001531022421122223&0`

---

*Report generated by USB Device Control & Monitoring Framework.*
