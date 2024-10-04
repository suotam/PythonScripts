# Folder Sync

A Python script to synchronize two folders one-way, ensuring the replica folder mirrors the source folder. Includes periodic synchronization and detailed logging.

## Features

- One-way synchronization from source to replica.
- Periodic syncing at user-defined intervals.
- Logs file operations to both console and a log file.
- Command-line configurable paths and intervals.

## Usage

```bash
python sync.py <source_folder> <replica_folder> <sync_interval_in_seconds> <log_file_path>