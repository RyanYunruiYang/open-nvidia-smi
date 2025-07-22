import argparse
from nvsmi.cli.commands import summary, nvlink

def main():
    p = argparse.ArgumentParser(prog="nvidia-smi")

    # # --- global args (id, filename, loop, etc.) ---
    # parser.add_argument("-i", "--id", help="GPU index/UUID")
    # parser.add_argument("-f", "--filename", help="output file")
    # parser.add_argument("-l", "--loop", type=int, help="loop interval (s)")
    # parser.add_argument("-q", "--query", action="store_true",
    #                     help="full GPU attribute dump")
    # parser.add_argument("-d", "--display", help="selective fields",
    #                     choices=[...])

    subs = p.add_subparsers(dest="cmd", required=True)
    summary.attach_parser(subs)
    nvlink.attach_parser(subs)
    # TODO: add other subcommands
    # - topo, c2c, drain, clocks, vgpu, mig, boost-slider
    # - power-hint, conf-compute, power-smoothing, power-profiles, encodersessions

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
