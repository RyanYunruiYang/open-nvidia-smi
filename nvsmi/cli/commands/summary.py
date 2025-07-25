import argparse
import time
import nvsmi.utils as utils
import nvsmi.nvml as nvml
from nvsmi.formatter.text.summary import format_summary
import nvsmi.models.models as models

def attach_parser(subparsers):
    p = subparsers.add_parser(
        "summary",
        help="show overall GPU summary (default if no subcommand given)"
    )
    # Flag options
    p.add_argument('-i', '--id', type=int, help="Target a specific GPU.")
    p.add_argument('-f', '--filename', help="Log to the specific file, rather than to stdout.")
    p.add_argument('-l', '--loop', type=int, help="Probe until Ctrl+C at specified second interval.")
    p.set_defaults(func=run_summary)

def run_summary(args):
    nvml.initialize()
    try:
        while True: # in case of loop flag
            # --- versions ---
            drv_ver = nvml.get_driver_version()       # e.g. "515.65.01"
            cuda_ver = utils.get_cuda_via_runtime()   # e.g. "11.7"

            # --- per-GPU stats ---
            gpus = []
            count = nvml.get_device_count()
            for idx in range(count):
                # --id flag
                if args.id is not None and idx != args.id:
                    continue

                h = nvml.get_device_handle_by_index(idx)
                name = nvml.get_device_name(h)
                bus_id = nvml.get_device_pci_info(h).busId
                mem = nvml.get_device_memory_info(h)                   # has .used, .total in bytes
                util = nvml.get_device_utilization_rates(h)            # has .gpu (%)
                temp = nvml.get_device_temperature(h, nvml.NVML_TEMPERATURE_GPU)                  # GPU temp in °C
                power = nvml.get_device_power_usage(h) / 1000         # mW → W
                fan   = nvml.get_device_fan_speed(h)                   # %

                gpus.append(models.GPUInfo(
                    index     = idx,
                    name      = name,
                    fan       = fan,
                    bus_id    = bus_id,
                    temp      = temp,
                    power     = int(power),
                    mem_used  = int(utils.bytes_to_mib(mem.used)),
                    mem_total = int(utils.bytes_to_mib(mem.total)),
                    util      = util.gpu
                ))

            # --- process list ---
            processes = []
            for idx in range(count):
                h = nvml.get_device_handle_by_index(idx)
                for p in nvml.get_device_compute_running_processes(h):
                    # list_processes should return objects with .pid, .usedGpuMemory, .type ('C'/'G')
                    proc_name = utils.get_process_name(p.pid)
                    mem_mb    = int(utils.bytes_to_mib(p.usedGpuMemory))
                    processes.append(models.ProcessInfo(
                        gpu       = idx,
                        pid       = p.pid,
                        type      = "C",
                        name      = proc_name,
                        mem_usage = f"{mem_mb}MiB"
                    ))
                for p in nvml.get_device_graphics_running_processes(h):
                    # list_processes should return objects with .pid, .usedGpuMemory, .type ('C'/'G')
                    proc_name = utils.get_process_name(p.pid)
                    mem_mb    = int(utils.bytes_to_mib(p.usedGpuMemory))
                    processes.append(models.ProcessInfo(
                        gpu       = idx,
                        pid       = p.pid,
                        type      = "G",
                        name      = proc_name,
                        mem_usage = f"{mem_mb}MiB"
                    ))

            print(f"processes: {processes}")
            # --- print it all ---
            summary = format_summary(
                driver_version = drv_ver,
                cuda_version   = cuda_ver,
                gpus           = gpus,
                processes      = processes
            )

            # --filename flag
            if args.filename:
                with open(args.filename, 'w') as f:
                    f.write(summary)
            else:
                print(summary)

            # --loop flag
            if args.loop:
                time.sleep(args.loop)
            else:
                break
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        nvml.shutdown()
