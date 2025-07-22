from dataclasses import dataclass

@dataclass
class GPUInfo:
    """
    Holds summary information for a single GPU.

    Attributes:
        index: GPU index (0-based)
        name:  GPU model name string
        fan:   Fan speed percentage
        temp:  Temperature in Celsius
        power: Power usage in Watts
        mem_used:  Memory used in MiB
        mem_total: Total memory in MiB
        util:  GPU utilization percentage
    """
    index: int
    name: str
    bus_id: str
    fan: int
    temp: int
    power: int
    mem_used: int
    mem_total: int
    util: int

@dataclass
class ProcessInfo:
    """
    Holds information for a single GPU process.

    Attributes:
        gpu:       GPU index the process is running on
        pid:       Process ID
        type:      'C' for compute or 'G' for graphics
        name:      Executable or command name
        mem_usage: Memory usage string (e.g., "123MiB")
    """
    gpu: int
    pid: int
    type: str
    name: str
    mem_usage: str
