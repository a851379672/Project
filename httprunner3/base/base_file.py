import os.path
import re
from common.settings import *
import datetime


def base_testfile():
    """
    文件格式：课程视频.mp4
    :return: file_name: 课程视频 2022-06-01 19:53:13.mp4
    """
    folder = [os.path.join(path_, filename) for path_, files, name_ in os.walk(FILE_PATH) for filename in files]
    file_name = [name for folder in folder for path, file, name in os.walk(folder) if name]
    num = 0
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H：%M：%S")
    for file_list in file_name:
        for file in file_list:
            old_name, file_type = os.path.splitext(file)
            raw_file = os.path.join(folder[num], old_name + file_type)
            try:
                new_file = os.path.join(folder[num], old_name.replace(
                    re.findall(r' (.*)', old_name)[0], date_time + file_type)
                                        )
            except IndexError:
                new_file = os.path.join(folder[num], old_name + ' ' + date_time + file_type)
            os.rename(raw_file, new_file)
        num += 1


if __name__ == '__main__':
    base_testfile()
