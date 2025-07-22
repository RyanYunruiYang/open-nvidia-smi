import argparse
from commands.summary import run as run_summary

def parse_args():
    p = argparse.ArgumentParser(
        description="nvsmi: an open-source implementation of nvidia-smi"
    )
    p.add_argument(
        "-q", "--query",
        action="store_true",
        help="detailed info"
    )
    return p.parse_args()

def main():
    args = parse_args()


    run_summary()

if __name__ == "__main__":
    main()
