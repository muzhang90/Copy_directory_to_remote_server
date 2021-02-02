import argparse
import os.path
import tarfile
import paramiko
import sys



class Copy:

    def __init__(self,loc_dir,remote_path,username,passwd):
        try:
            if os.path.exists(loc_dir) and os.path.isdir(loc_dir):
                self.loc_dir=loc_dir
            else:
                raise OSError


        except OSError as e:
            print('The input directory is not valid, please check')
            sys.exit()

        self.remote_server,self.remote_dir=remote_path.split(':')
        self.username=username
        self.passwd=passwd
        self.full_fname_out=''

        self.fname_out='textzip.tar.gz'
        print('Zipping the directory now...')
        self.compress_file_relative()
        print('Zipping  Done!')
        self.copy()
        print('Selected direction has been copied to remote location and unzipped. ')

    def compress_file_relative(self):
        cur_path=os.getcwd()
        #fname_out='textzip.tar.gz'
        self.full_fname_out=os.path.join(cur_path,self.fname_out)
        full_path_in=self.loc_dir
        os.chdir(full_path_in)
        tar=tarfile.open(self.full_fname_out,'w:gz')
        for root, dir, files in os.walk(full_path_in):
            for file in files:

                fullpath=file
                tar.add(fullpath,recursive=False)
        tar.close()
        os.chdir(cur_path)


    def copy(self):

        try:

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(hostname=self.remote_server, username=self.username, password=self.passwd)
            '''
            Check if the remote direction exists, if not,, create one.
            
            Pending.
            '''
            file_client = ssh_client.open_sftp()
            full_remote_path = self.remote_dir + '/' + self.fname_out
            file_client.put(self.fname_out, self.remote_dir + '/' + self.fname_out)
            command = f'tar -C {self.remote_dir} -zxvf {full_remote_path}'
            #print(command)

            file_client.close()
            stdin, stdout, stderr = ssh_client.exec_command(command)

            '''
            Paramiko how to login user shell?
        
        
        
            '''
            output = stdout.read().decode('utf-8').split('\n')

            ssh_client.close()
            #print(output)
        except Exception as e:
            print('Connect to remote server failed, please check the reachibility')
            sys.exit()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('local_dir',type=str, help='local dir')
    parser.add_argument('remote_location',type=str, help='remote location, format: sever_ip:location')
    parser.add_argument('user_name',type=str, help='username')
    parser.add_argument('passwd',type=str, help='passwd')
    args = parser.parse_args()

    Copy(args.local_dir,args.remote_location,args.user_name,args.passwd)