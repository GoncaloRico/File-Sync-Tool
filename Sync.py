import sys
import os
import shutil
import time
import hashlib


def main():
    source, replica, interval_seconds, log_directory = check_args()
    while True:
        log_file_path = create_log_file(log_directory)
        each_file(source, replica, log_file_path)
        print(
            f"Sync completed. Waiting {interval_seconds} seconds until the next sync...\n Press Ctrl+C to stop running."
        )
        time.sleep(interval_seconds)


def check_args():
    if len(sys.argv) <= 4:
        sys.exit(
            "Please make sure you input 4 arguments in the following order:\n - Source folder path\n - Replica folder path\n - Sync intervals\n - Log file path "
        )
    else:
        return (sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])


def create_log_file(log_directory):
    # Create the log file path using the specified directory and fixed file name
    log_file_path = os.path.join(log_directory, "Log.txt")
    return log_file_path


def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def copy(source, replica, log_file):
    try:
        copy_message = f"Copying Files from: {source} to: {replica}"
        print(copy_message)
        log_file.write(copy_message + "\n")
        shutil.copy(source, replica)
    except:
        copy_message = f"File Exists at: {replica}"
        print(copy_message)
        log_file.write(copy_message + "\n")


def each_file(source, replica, log_path):
    # Open the log file in append mode
    with open(log_path, "a") as log_file:
        for folderName, subfolders, filenames in os.walk(source):
            message = f"The current folder is {folderName}"
            log_file.write(message + "\n")
            for subfolder in subfolders:
                message = f"Subfolder of {folderName}: {subfolder}"
                log_file.write(message + "\n")
                try:
                    new_path = folderName.replace(source, replica)
                    os.makedirs(os.path.join(new_path, subfolder), exist_ok=True)
                except:
                    message = f"Folder Exists: {os.path.join(new_path, subfolder)}"
                    print(message)
                    log_file.write(message + "\n")
            for filename in filenames:
                new_path = folderName.replace(source, replica)
                src_file = os.path.join(folderName, filename)
                replica_file = os.path.join(new_path, filename)
                src_file_hash = calculate_file_hash(src_file)
                replica_file_hash = ""
                # If replica file exists, calculate its hash
                if os.path.exists(replica_file):
                    replica_file_hash = calculate_file_hash(replica_file)
                # If file does not exist in replica or hashes are different, update replica
                if (
                    not os.path.exists(replica_file)
                    or src_file_hash != replica_file_hash
                ):
                    copy(src_file, replica_file, log_file)
                    update_message = (
                        f"File {filename} updated in replica to match source."
                    )
                    print(update_message)
                    log_file.write(update_message + "\n")
                else:
                    message = f"File {filename} already exists and is up to date."
                    print(message)
                    log_file.write(message + "\n")
        # Check for deleted files in replica
        for root, dirs, files in os.walk(replica):
            for filename in files:
                replica_file = os.path.join(root, filename)
                src_file = replica_file.replace(replica, source)
                # If the corresponding file in the source does not exist, delete it from replica
                if not os.path.exists(src_file):
                    delete_message = (
                        f"Deleting File: {replica_file} (file deleted from source)"
                    )
                    print(delete_message)
                    log_file.write(delete_message + "\n")
                    os.remove(replica_file)


if __name__ == "__main__":
    main()
