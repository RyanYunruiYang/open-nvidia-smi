import argparse
from nvsmi.cli.commands import summary

def main():
    p = argparse.ArgumentParser(prog="nvidia-smi")
    subs = p.add_subparsers(dest="cmd", required=True)

    summary.attach_parser(subs)
    # topo.attach_parser(subs)
    # c2c.attach_parser(subs)
    # nvlink.attach_parser(subs)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
