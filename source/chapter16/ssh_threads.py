#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter16/ssh_threads.py
# Running two remote commands simultaneously in different channels

import argparse, paramiko, threading

class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

def main(hostname, username):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(AllowAnythingPolicy())
    client.connect(hostname, username=username)  # password='')

    def read_until_EOF(fileobj):
        s = fileobj.readline()
        while s:
            print(s.strip())
            s = fileobj.readline()

    ioe1 = client.exec_command('echo One;sleep 2;echo Two;sleep 1;echo Three')
    ioe2 = client.exec_command('echo A;sleep 1;echo B;sleep 2;echo C')
    thread1 = threading.Thread(target=read_until_EOF, args=(ioe1[1],))
    thread2 = threading.Thread(target=read_until_EOF, args=(ioe2[1],))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Connect over SSH')
    parser.add_argument('hostname', help='Remote machine name')
    parser.add_argument('username', help='Username on the remote machine')
    args = parser.parse_args()
    main(args.hostname, args.username)
