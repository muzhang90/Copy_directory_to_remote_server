# Directory copy

## Goal

As JTAC engineer, sometimes we need to copy customer log, live data and core dumps to a linux server to share with engineering team. 
This script is keen to reduce the operation cost to automate this process.

## How to use

This script takes 4 arguments:
  local_directory: The absolute path of the directory that is ready to copy. 
  remote_path: remote server IP and the absolute path the data will be copied to. In format of "remote_ip:path"
  username
  password
  
  
The script will be executed in below order:

  1.Compress the local directory into a tar file.
  2.Copy the tar file to remote server and put it under the remote path.
  3.Un-tar the file.
  
