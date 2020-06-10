# -*- coding: utf-8 -*-
import subprocess
import pathlib
import config

def upload(file: str):
    d = pathlib.Path(config.DIRECTORY)

    if '/' in file:
        parent = (file.rsplit('/', 1)[0])
    else:
        parent = ''

    src = str(d / file)
    dest = config.RCLONE_NAME + ':' + parent
    process_args = ['rclone', 'copy', '--create-empty-src-dirs', '--verbose', src, dest]
    print(process_args)
    
    try:
        p = subprocess.Popen(process_args)
        p.wait()
        if p.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print("failed. retry...")
        print(e)
        return False
