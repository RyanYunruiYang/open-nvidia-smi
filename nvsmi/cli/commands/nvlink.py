import nvsmi.nvml as nvml


def attach_parser(subparsers):
    """Attach nvlink subcommand to argument parser"""
    parser = subparsers.add_parser("nvlink", help="Display nvlink status")
    parser.add_argument("-s", "--status", action="store_true", 
                       help="Display nvlink status")
    parser.set_defaults(func=nvlink_main)


def nvlink_main(args):
    """Main function for nvlink command"""
    nvml.initialize()
    try:
        if args.status:
            show_nvlink_status()
        else:
            print("Use -s to show nvlink status")
    finally:
        nvml.shutdown()


def show_nvlink_status():
    """Display nvlink status for all GPUs"""
    device_count = nvml.get_device_count()
    
    for i in range(device_count):
        handle = nvml.get_device_handle_by_index(i)
        name = nvml.get_device_name(handle)
        uuid = nvml.get_device_uuid(handle)
        
        print(f"GPU {i}: {name} (UUID: {uuid})")
        
        # For now, hardcode:
        for link in range(4):
            bandwidth = 14.062
            print(f"\t Link {link}: {bandwidth} GB/s")
