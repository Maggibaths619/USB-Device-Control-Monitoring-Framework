import subprocess
from modules.logger import get_logger

logger = get_logger("Enforcer")

class DeviceEnforcer:
    @staticmethod
    def block_device(instance_id):
        """
        Blocks the USB device using PowerShell Disable-PnpDevice.
        Requires the script to run as Administrator.
        """
        try:
            logger.warning(f"Attempting to block unauthorized device with Instance ID: {instance_id}")
            
            # The command uses -Confirm:$false to bypass the confirmation prompt.
            ps_command = f"Disable-PnpDevice -InstanceId '{instance_id}' -Confirm:$false"
            
            result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully blocked device: {instance_id}")
                return True
            else:
                logger.error(f"Failed to block device: {instance_id}. Error: {result.stderr.strip()}")
                return False
        except Exception as e:
            logger.error(f"Exception occurred while trying to block device: {str(e)}")
            return False

    @staticmethod
    def enable_device(instance_id):
        """
        Enables a blocked USB device.
        """
        try:
            logger.info(f"Attempting to enable device with Instance ID: {instance_id}")
            ps_command = f"Enable-PnpDevice -InstanceId '{instance_id}' -Confirm:$false"
            result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully enabled device: {instance_id}")
                return True
            else:
                logger.error(f"Failed to enable device: {instance_id}. Error: {result.stderr.strip()}")
                return False
        except Exception as e:
            logger.error(f"Exception occurred while trying to enable device: {str(e)}")
            return False
