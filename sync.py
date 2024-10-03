import argparse

def main():
    parser = argparse.ArgumentParser(description = "Synchronize two folders.")
    parser.add_argument("source", help = "Path to the source folder")
    parser.add_argument("replica", help = "Path to the replica folder")
    parser.add_argument("interval", type = int, help = "Synchronization interval in seconds")
    parser.add_argument("log_file", help = "Path to the log file")
    args = parser.parse_args()

    # Synchronization logic placeholder
    print(f"Source: {args.source}")
    print(f"Replica: {args.replica}")
    print(f"Interval: {args.interval} seconds")
    print(f"Log File: {args.log_file}")

    if __name__ == "__main__":
        main()

