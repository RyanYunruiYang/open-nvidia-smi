from typing import List
from nvsmi.models.models import GPUInfo, ProcessInfo


def format_summary(
    driver_version: str,
    cuda_version: str,
    gpus: List[GPUInfo],
    processes: List[ProcessInfo]
) -> str:
    print(f"hi")
    # Header
    lines = []
    lines.extend([
        "+-----------------------------------------------------------------------------------------+",
        f"| NVIDIA-SMI {driver_version:<22} Driver Version: {driver_version:<14} CUDA Version: {cuda_version:<9}|",
        "|-----------------------------------------+------------------------+----------------------+",
        "| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |",
        "| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |",
        "|                                         |                        |               MIG M. |",
        "|=========================================+========================+======================|"
    ])

    # Per-GPU lines
    for gpu in gpus:
        # Format bus ID if available
        try:
            raw = gpu.bus_id  # e.g. '0000:50:00.0'
            domain, rest = raw.split(':', 1)
            busid = domain.zfill(8) + ':' + rest
        except Exception:
            busid = "00000000:00:00.0"
        # GPU summary row 1: index, name, persistence, busid, display, ECC
        lines.append(
            f"|{gpu.index:>4}  {gpu.name:<31}Off |{busid:>19} Off |                  Off |"
        )
        lines.append(
            f"|{gpu.fan:>3}%{gpu.temp:>5}C    P2{gpu.power:>15}W /  300W |{gpu.mem_used:>8}MiB /{gpu.mem_total:>7}MiB |{gpu.util:>7}%      Default |"
        )
        lines.append(
            "|                                         |                        |                  N/A |"
        )
        lines.append(
            "+-----------------------------------------+------------------------+----------------------+"
        )

    # Processes section
    lines.append("\n+-----------------------------------------------------------------------------------------+")
    lines.append("| Processes:                                                                              |")
    lines.append("|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |")
    lines.append("|        ID   ID                                                               Usage      |")
    lines.append("|=========================================================================================|")
    if not processes:
        lines.append(
            "|  No running processes found                                                             |"
        )
    else:
        for p in processes:
            # TODO: Print MIG IDs as N/A
            lines.append(
                f"|{p.gpu:>5}   N/A  N/A{p.pid:>10}{p.type:>7}   {p.name:<38}{p.mem_usage:>14} |"
            )

    # Footer
    lines.append(
        "+-----------------------------------------------------------------------------------------+"
    )

    return "\n".join(lines)
