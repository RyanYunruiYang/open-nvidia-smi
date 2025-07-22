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
    return pynvml.nvmlSystemGetDriverVersion().decode()


def get_nvml_version():
    """Get NVML version string"""
    return pynvml.nvmlSystemGetNVMLVersion().decode()


def get_device_count():
    """Get number of GPU devices"""
    return pynvml.nvmlDeviceGetCount()


def get_device_handle_by_index(index):
    """Get device handle by index"""
    return pynvml.nvmlDeviceGetHandleByIndex(index)


def get_device_name(handle):
    """Get device name string"""
    return pynvml.nvmlDeviceGetName(handle).decode()


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


# Constants from pynvml
NVML_TEMPERATURE_GPU = pynvml.NVML_TEMPERATURE_GPU