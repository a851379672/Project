import os.path
import re
from settings import *


def base_testfile():
    """
    文件格式：课程视频_0.mp4
    :return: file_name: 课程视频_1.mp4
    """
    folder = [os.path.join(paths, filename) for paths, files, name in os.walk(FILE_PATH) for filename in files]
    file_name = [name for folder in folder for path, file, name in os.walk(folder) if name]
    num = 0
    for file_list in file_name:
        for file in file_list:
            old_name, format_ = os.path.splitext(file)
            file_num = int(re.findall(r'_(\d+)+', f'{old_name}')[0])
            re_name = old_name.replace(str(file_num), str(file_num + 1))
            os.rename(fr'{folder[num]}\{old_name + format_}', fr'{folder[num]}\{re_name + format_}')
        num += 1


if __name__ == '__main__':
    base_testfile()
