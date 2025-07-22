"""
Light wrapper over pynvml (for now).
"""

import ctypes
import pynvml

def initialize():
    """Initialize NVML library"""
    pynvml.nvmlInit()


def shutdown():
    """Shutdown NVML library"""
    pynvml.nvmlShutdown()


def get_driver_version():
    """Get driver version string. Example: 550.90.07"""
    return pynvml.nvmlSystemGetDriverVersion()


def get_nvml_version():
    """Get NVML version string"""
    return pynvml.nvmlSystemGetNVMLVersion()


def get_device_count():
    """Get number of GPU devices"""
    return pynvml.nvmlDeviceGetCount()


def get_device_handle_by_index(index):
    """Get device handle by index"""
    return pynvml.nvmlDeviceGetHandleByIndex(index)


def get_device_name(handle):
    """Get device name string"""
    return pynvml.nvmlDeviceGetName(handle)


def get_device_uuid(handle):
    """Get device UUID string"""
    return pynvml.nvmlDeviceGetUUID(handle)


def get_device_memory_info(handle):
    """Get device memory information (total, free, used)"""
    return pynvml.nvmlDeviceGetMemoryInfo(handle)


def get_device_utilization_rates(handle):
    """Get device GPU and memory utilization rates"""
    return pynvml.nvmlDeviceGetUtilizationRates(handle)


def get_device_temperature(handle, sensor_type):
    """Get device temperature for specified sensor"""
    return pynvml.nvmlDeviceGetTemperature(handle, sensor_type)


def get_device_power_usage(handle):
    """Get device power usage in milliwatts"""
    return pynvml.nvmlDeviceGetPowerUsage(handle)


def get_device_fan_speed(handle):
    """Get device fan speed percentage"""
    return pynvml.nvmlDeviceGetFanSpeed(handle)


def get_device_pci_info(handle):
    """Get device PCI information"""
    return pynvml.nvmlDeviceGetPciInfo(handle)


def get_device_compute_running_processes(handle):
    """Get running compute processes on device"""
    try:
        return pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
    except Exception as e:
        print(f"Error getting compute running processes: {e}")
        # If no processes found or other error, return empty list
        return []


def get_device_graphics_running_processes(handle):
    """Get running graphics processes on device"""
    try:
        return pynvml.nvmlDeviceGetGraphicsRunningProcesses(handle)
    except Exception as e:
        print(f"Error getting graphics running processes: {e}")
        # If no processes found or other error, return empty list
        return []


def get_device_nvlink_state(handle, link):
    """Get NvLink state for specified link (placeholder implementation)"""
    # Note: This is a placeholder since pynvml nvlink functions may not be available
    # in all versions. In a real implementation, you would use:
    # return pynvml.nvmlDeviceGetNvLinkState(handle, link)
    return None


def get_device_nvlink_version(handle, link):
    """Get NvLink version for specified link (placeholder implementation)"""
    # Note: This is a placeholder since pynvml nvlink functions may not be available
    # in all versions. In a real implementation, you would use:
    # return pynvml.nvmlDeviceGetNvLinkVersion(handle, link)
    return None


def get_nvlink_link_count(handle):
    """Get number of NvLink links on device (placeholder implementation)"""
    # Note: This is a placeholder since pynvml nvlink functions may not be available
    # in all versions. For now, return 0 (no links detected)
    return 0


def get_device_nvlink_utilization(handle, link, counter):
    """Get NvLink utilization counter (placeholder implementation)"""
    # Note: This is a placeholder since pynvml nvlink functions may not be available
    # in all versions. In a real implementation, you would use:
    # return pynvml.nvmlDeviceGetNvLinkUtilizationCounter(handle, link, counter)
    return None, None


def get_device_max_nvlink_bandwidth(handle, link):
    """Get max NvLink bandwidth for a link (estimated)"""
    try:
        # For NVLink 2.0 (common on A6000), bandwidth is typically 14.062 GB/s per link
        # For NVLink 3.0 (A100), it's 28.125 GB/s per link
        # Since we can't easily determine the exact version, we'll use 14.062 as default
        return 14.062
    except Exception as e:
        return 0.0


# Constants from pynvml
NVML_TEMPERATURE_GPU = pynvml.NVML_TEMPERATURE_GPU
NVML_FEATURE_ENABLED = pynvml.NVML_FEATURE_ENABLED
NVML_FEATURE_DISABLED = pynvml.NVML_FEATURE_DISABLED