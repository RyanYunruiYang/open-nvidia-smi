#!/usr/bin/env python3
"""
This script replicates basic output of `nvidia-smi` using NVIDIA's NVML library.
"""

from pynvml import (
    nvmlInit,
    nvmlShutdown,
    nvmlDeviceGetCount,
    nvmlDeviceGetHandleByIndex,
    nvmlSystemGetDriverVersion,
    nvmlDeviceGetName,
    nvmlDeviceGetMemoryInfo,
    nvmlDeviceGetUtilizationRates,
    nvmlDeviceGetTemperature,
    nvmlDeviceGetPowerUsage,
    nvmlDeviceGetFanSpeed,
    nvmlDeviceGetPciInfo,
    nvmlDeviceGetComputeRunningProcesses,
    nvmlSystemGetNVMLVersion,
    NVML_TEMPERATURE_GPU,
    NVMLError_NotFound,
)
import pynvml
import ctypes
import psutil
from datetime import datetime
import argparse




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


def run():
    # Part 0: print timestamp: Mon Jul 14 21:58:43 2025 
    timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    print(timestamp)

    # Initialize NVML
    nvmlInit()

    # PART ONE
    # Get driver version and CUDA Version
    v1 = nvmlSystemGetDriverVersion().decode()
    v2 = get_cuda_via_runtime()

    print(f"""+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI {v1}              Driver Version: {v1}      CUDA Version: {v2}     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|""")

    # Count GPUs, then query each for information
    gpu_count = nvmlDeviceGetCount()
    for i in range(gpu_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        name = nvmlDeviceGetName(handle).decode()
        mem_info = nvmlDeviceGetMemoryInfo(handle)
        util = nvmlDeviceGetUtilizationRates(handle)
        temp = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
        power = nvmlDeviceGetPowerUsage(handle) / 1000  # milliwatts to watts
        fan = nvmlDeviceGetFanSpeed(handle)

        used_mib = bytes_to_mib(mem_info.used)
        total_mib = bytes_to_mib(mem_info.total)

        # Pad BusID with 4 0s in front.
        raw_busid = nvmlDeviceGetPciInfo(handle).busId.decode() # 0000:50:00.0
        domain, rest = raw_busid.split(":", 1)
        busid = domain.zfill(8) + ":" + rest

        print(
f"""|{i:>4}  {name:<31}Off |{busid:>19} Off |                  Off |
|{fan:>3}%{temp:>5}C    P2{int(power):>15}W /  300W |{int(used_mib):>8}MiB /{int(total_mib):>7}MiB |{util.gpu:>7}%      Default |
|                                         |                        |                  N/A |  
+-----------------------------------------+------------------------+----------------------+"""
)

    # PART TWO
    # Print process information
    print("""
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|""")

    process_printed = False
    for gpu_index in range(gpu_count):
        try:
            procs = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
        except NVMLError_NotFound:
            comp_procs = []

        try:
            gfx_procs = pynvml.nvmlDeviceGetGraphicsRunningProcesses(handle)
        except NVMLError_NotFound:
            gfx_procs = []

        # Note: MIG instance IDs not handled here → print 'N/A'
        # Example:
# |    1   N/A  N/A    845093      C   ...pp-wjj/build/scratch/ring_allreduce       2360MiB |
        for p in procs:
            process_printed = True
            name = get_process_name(p.pid)
            mem  = f"{int(bytes_to_mib(p.usedGpuMemory))}MiB"
            print(f"|{gpu_index:>5}   {'N/A'}  {'N/A'}{p.pid:>10}{'C':>7}   {name:<38}{mem:>14} |")        

        for p in gfx_procs:
            process_printed = True
            name = get_process_name(p.pid)
            mem  = f"{int(bytes_to_mib(p.usedGpuMemory))}MiB"
            print(f"|{gpu_index:>5}   {'N/A'}  {'N/A'}{p.pid:>10}{'G':>7}   {name:<38}{mem:>14} |")        
        
    if not process_printed:
        print("""|  No running processes found                                                             |""")

    # Close off bottom
    print("""+-----------------------------------------------------------------------------------------+""")

    # Shutdown NVML
    nvmlShutdown()


if __name__ == "__main__":
    main()