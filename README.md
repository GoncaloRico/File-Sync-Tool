# File Synchronization Tool
This Python script provides a simple file synchronization solution between a source folder and a replica folder. It compares files in the source and replica directories, copies new or modified files to the replica, and deletes files from the replica if they have been deleted from the source.

## Prerequisites
Python 3.x installed on your system.

## How to Use
1. Clone the Repository:
   
```
git clone https://github.com/GoncaloRico/File-Sync-Tool.git
cd file-synchronization-tool
```

2. Run the Script:

To run the script, execute the following command in your terminal or command prompt:

```
python sync.py <source-folder> <replica-folder> <sync-interval-seconds> <log-directory>
```

Replace "source-folder" with the path of the source folder you want to synchronize.

Replace "replica-folder" with the path of the replica folder where files will be copied.

"sync-interval-seconds" is the time interval (in seconds) between synchronization attempts.

"log-directory" is the path where the log file will be created.

Example:

```
python sync.py /path/to/source-folder /path/to/replica-folder 3600 /path/to/log-directory
```

3. Stopping the Program:

The program will run indefinitely, synchronizing files at the specified intervals. To stop the program, press Ctrl+C in the terminal or command prompt.

## Notes
- Ensure that the specified source and replica folders exist before running the script.
- The log file ("Log.txt") will be created in the specified log directory. If the directory does not exist, the script will attempt to create it.

Feel free to modify the script or incorporate it into your projects as needed. For any issues or questions, please create an issue in the repository. Happy syncing!
