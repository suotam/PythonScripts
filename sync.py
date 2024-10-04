import argparse
import logging
import hashlib
import os
import shutil
import time
from datetime import datetime

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        logging.error(f"File not found for MD5 calculation: {file_path}")
        return None
    
def sync_folders(source, replica):
    logging.info("Synchronization started")

    # Ensure replica folder exists
    if not os.path.exists(replica):
        os.makedirs(replica)
        logging.info(f"Replica folder created: {replica}")

    # Sync all files and folders from source to replica
    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        replica_root = os.path.join(replica, rel_path)

        # Create directories in replica if they don't exist
        for dir in dirs:
            replica_dir = os.path.join(replica_root, dir)
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                logging.info(f"Directory created: {replica_dir}")

        # Copy or update files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_root, file)

            # Copy the file if it doesn't exist in the replica
            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"File copied: {source_file} -> {replica_file}")
            else:
                # Compare MD5 hashes if the file already exists
                source_md5 = calculate_md5(source_file)
                replica_md5 = calculate_md5(replica_file)
                if source_md5 and replica_md5 and source_md5 != replica_md5:
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"File updated: {source_file} -> {replica_file}")

    # Remove files and folders in replica that are not in source
    for root, dirs, files in os.walk(replica, topdown=False):
        rel_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, rel_path)

        # Remove files
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_root, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"File removed: {replica_file}")

        # Remove directories
        for dir in dirs:
            replica_dir = os.path.join(root, dir)
            source_dir = os.path.join(source_root, dir)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                logging.info(f"Directory removed: {replica_dir}")

    logging.info("Synchronization completed!")

def periodic_sync(source, replica, interval):
    while True:
        sync_folders(source, replica)
        time.sleep(interval)



def setup_logging(log_file):
    # Log to a file
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a'
    )
    # Log to the console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    args = parser.parse_args()

    setup_logging(args.log_file)
    logging.info("Synchronization script started")
    logging.info(f"Source: {args.source}")
    logging.info(f"Replica: {args.replica}")
    logging.info(f"Interval: {args.interval} seconds")

    periodic_sync(args.source, args.replica, args.interval)


if __name__ == "__main__":
        main()

