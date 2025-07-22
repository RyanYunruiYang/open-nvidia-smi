import datetime 
import ctypes 
import psutil

def bytes_to_mib(bytes_val):
    """Convert bytes to MiB."""
    return bytes_val / 1024 / 1024

def get_cuda_via_runtime():
    # on Linux
    libcudart = ctypes.CDLL("libcudart.so")
    version = ctypes.c_int()
    # cudaRuntimeGetVersion(&version)
    libcudart.cudaRuntimeGetVersion(ctypes.byref(version))
    raw = version.value
    major = raw // 1000
    minor = (raw % 1000) // 10
    return f"{major}.{minor}"


def get_process_name(pid):
    try:
        p = psutil.Process(pid)
        cmd = p.cmdline()
        return cmd[0] if cmd else "<unknown>"
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "<unknown>"
    
def get_timestamp():
    return datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
