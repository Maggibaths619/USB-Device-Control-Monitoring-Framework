"""
manage_policy.py - CLI tool to manage the USB allowlist and blocklist.

Usage:
    python manage_policy.py list
    python manage_policy.py add-allow  --vid 0951 --pid 1666 [--serial ABCDEF] [--desc "My USB"]
    python manage_policy.py add-block  --vid 1234 --pid 5678 [--desc "Bad Device"]
    python manage_policy.py remove-allow --vid 0951 --pid 1666
    python manage_policy.py show-settings
"""
import argparse
import sys
import json
import os

# Reconfigure stdout to UTF-8 so Unicode/emoji prints correctly on Windows terminals.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Adjust path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from modules.policy_engine import PolicyEngine


def cmd_list(engine, args):
    print("\n" + "="*60)
    print("  [ALLOW]  AUTHORIZED DEVICES (Allowlist)")
    print("="*60)
    if not engine.authorized_devices:
        print("  (empty)")
    for i, d in enumerate(engine.authorized_devices, 1):
        print(f"  [{i}] {d.get('description', 'N/A')}")
        print(f"       VID: {d.get('vendor_id')}  PID: {d.get('product_id')}  Serial: {d.get('serial_number', 'N/A')}")

    print("\n" + "="*60)
    print("  [BLOCK]  BLOCKED DEVICES (Blocklist)")
    print("="*60)
    if not engine.blocked_devices:
        print("  (empty)")
    for i, d in enumerate(engine.blocked_devices, 1):
        print(f"  [{i}] {d.get('description', 'N/A')}")
        print(f"       VID: {d.get('vendor_id')}  PID: {d.get('product_id')}  Serial: {d.get('serial_number', 'N/A')}")
    print()


def cmd_add_allow(engine, args):
    engine.add_authorized_device(
        vendor_id=args.vid,
        product_id=args.pid,
        serial_number=args.serial or "N/A",
        description=args.desc or "Manually Added"
    )
    print(f"[ADDED] VID:{args.vid} PID:{args.pid} added to allowlist.")


def cmd_add_block(engine, args):
    engine.add_blocked_device(
        vendor_id=args.vid,
        product_id=args.pid,
        serial_number=args.serial or "N/A",
        description=args.desc or "Manually Blocked"
    )
    print(f"[BLOCKED] VID:{args.vid} PID:{args.pid} added to blocklist.")


def cmd_remove_allow(engine, args):
    removed = engine.remove_authorized_device(args.vid, args.pid)
    if removed:
        print(f"[REMOVED] VID:{args.vid} PID:{args.pid} removed from allowlist ({removed} entry/entries).")
    else:
        print(f"[WARNING] No matching device VID:{args.vid} PID:{args.pid} found in allowlist.")


def cmd_show_settings(engine, args):
    print("\n" + "="*60)
    print("  [SETTINGS]   CURRENT SETTINGS")
    print("="*60)
    for key, val in engine.settings.items():
        print(f"  {key}: {val}")
    print()


def build_parser():
    parser = argparse.ArgumentParser(
        description="USB Framework Policy Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    subparsers.add_parser("list", help="List all authorized and blocked devices.")

    # add-allow
    p_add_allow = subparsers.add_parser("add-allow", help="Add a device to the allowlist.")
    p_add_allow.add_argument("--vid", required=True, help="Vendor ID (4-char hex, e.g. 0951)")
    p_add_allow.add_argument("--pid", required=True, help="Product ID (4-char hex, e.g. 1666)")
    p_add_allow.add_argument("--serial", default="N/A", help="Serial number (optional)")
    p_add_allow.add_argument("--desc", default="Manually Added", help="Description")

    # add-block
    p_add_block = subparsers.add_parser("add-block", help="Add a device to the blocklist.")
    p_add_block.add_argument("--vid", required=True, help="Vendor ID")
    p_add_block.add_argument("--pid", required=True, help="Product ID")
    p_add_block.add_argument("--serial", default="N/A", help="Serial number (optional)")
    p_add_block.add_argument("--desc", default="Manually Blocked", help="Description")

    # remove-allow
    p_rem = subparsers.add_parser("remove-allow", help="Remove a device from the allowlist.")
    p_rem.add_argument("--vid", required=True, help="Vendor ID")
    p_rem.add_argument("--pid", required=True, help="Product ID")

    # show-settings
    subparsers.add_parser("show-settings", help="Display current framework settings.")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    engine = PolicyEngine()

    dispatch = {
        "list": cmd_list,
        "add-allow": cmd_add_allow,
        "add-block": cmd_add_block,
        "remove-allow": cmd_remove_allow,
        "show-settings": cmd_show_settings,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(engine, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
