import pathlib
import hashlib
from typing import Union

BLOCK_SIZE = hashlib.new('md5').block_size * 0x800


def get_file_hash(path: Union[str, pathlib.Path]):
    path = str(path)

    h = hashlib.new('md5')
    
    with open(path,'rb') as f:
        BinaryData = f.read(BLOCK_SIZE)

        # データがなくなるまでループします
        while BinaryData:

            # ハッシュオブジェクトに追加して計算します。
            h.update(BinaryData)

            # データの続きを読み込む
            BinaryData = f.read(BLOCK_SIZE)
    return h.hexdigest()
