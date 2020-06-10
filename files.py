import pathlib
import sqlite3
import config
import filehash
from typing import List, Tuple

def get_new_files() -> List[Tuple[str, str]]:
    d = pathlib.Path(config.DIRECTORY)
    files = d.glob('**/*')
    filenames = [
        str(f)[len(config.DIRECTORY):]
        for f in files
    ]

    ignore_file_patterns = set()
    for fn in d.glob('**/.gdignore'):
        fn: pathlib.Path
        with open(str(fn)) as f:
            for l in f:
                l:str
                if l.startswith('#'): continue
                for a in fn.parent.glob(l.strip()):
                    ignore_file_patterns.add(str(a)[len(config.DIRECTORY):])
                for a in fn.parent.glob(l.strip() + '/**/*'):
                    ignore_file_patterns.add(str(a)[len(config.DIRECTORY):])
    
    filenameset = set(filenames)
    filenameset.difference_update(ignore_file_patterns)
    filenames = list(filenameset)
    filenames.sort()

    with sqlite3.connect(config.DB_FILENAME) as conn:
        ret = []

        c = conn.cursor()
        c.execute('select * from files order by name')
        rows = c.fetchall()
        a = 0
        b = 0
        while a < len(rows) or b < len(filenames):
            if b < len(filenames):
                if filenames[b] in ignore_file_patterns or (d/filenames[b]).is_dir():
                    b += 1
                    continue

            s = 0 # 1: a advanced 0: normal -1: b advanced
            if a >= len(rows):
                s = 1
            elif b >= len(filenames):
                s = -1
            elif rows[a][0] > filenames[b]:
                s = 1
            elif rows[a][0] < filenames[b]:
                s = -1
            else:
                s = 0
            
            if s == 0:
                if filehash.get_file_hash(d / filenames[b]) != rows[a][1]:
                    ret.append((rows[a][0], 'M')) # modified
                a += 1
                b += 1
            elif s == -1: # deleted
                ret.append((rows[a][0], 'D'))
                a += 1
            elif s == 1: # new file
                ret.append((filenames[b], 'N'))
                b += 1
    return ret

def register_files(files: List[str]):
    d = pathlib.Path(config.DIRECTORY)
    with sqlite3.connect(config.DB_FILENAME) as conn:
        ret = []

        c = conn.cursor()

        for fn in files:
            h = filehash.get_file_hash(d / fn)

            if c.execute('select 1 from files where name=?', (fn,)).rowcount:
                c.execute('update files set hash=? where name=?', (h, fn))
            else:
                c.execute('insert into files set (hash) values (?) where name=?', (h, fn))

if __name__ == "__main__":
    #print(get_new_files())
    register_files(['麻布高校2年生　保健体育(新しくなります)/soccer-court.svg'])
