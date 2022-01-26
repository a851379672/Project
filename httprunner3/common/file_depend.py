# -*- coding: utf-8 -*-
from settings import *
import re


class FileDepend:

    def __init__(self):
        """文件类型"""
        self.image_file = [
            '.png ', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
        self.audio_video_file = [
            '.mp3', '.mp4', '.mpg', '.mpeg', '.mpe', '.avi', '.rm', '.3gp', '.rmvb', '.wmv', '.mov', '.flv', '.mkv']
        self.document_file = [
            'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'rar', 'pdf', 'txt', 'epub'
        ]

        self.file_path = FILE_PATH

    def file_dispose(self, file_):
        """文件处理（文件读取后不关闭）"""
        if type(file_) == dict:
            return self.file_dict(file_)
        else:
            return self.file_content(file_)

    def check_type(self, file_):
        """
        检查字段内容类型
        :param file_: file_
        :return:
        """

        def image_file(x): return any(
            x.endswith(extension) for extension in self.image_file)

        def audio_video_file(x): return any(x.endswith(extension)
                                            for extension in self.audio_video_file)

        def document_file_file(x): return any(x.endswith(extension)
                                              for extension in self.document_file)

        try:
            if image_file(file_) or audio_video_file(file_) or document_file_file(file_):
                return True
        except AttributeError:
            return False

    def path_name(self, file_):
        """获取真实文件路径名称"""
        file_full_name = self.get_path(file_)
        return os.path.join(file_full_name[0], file_full_name[1])

    def file_name(self, file_):
        """获取真实文件名称"""
        file_full_name = self.get_path(file_)
        return file_full_name[1]

    def get_path(self, file_):
        """获取对象路径"""
        module, name = file_.split('/')
        file_names = name.split('.')[0]
        file_path = os.path.join(self.file_path, module)
        return file_path, [file for file in os.listdir(file_path) if file_names in file][0]

    def file_dict(self, file_):
        """
        字典内容文件处理
        :return: file_dict
        """
        file_params = {key: (None, value) for key, value in file_.items() if key != 'file'}
        file_params.update({'file': (self.file_name(file_['file']), open(self.path_name(file_['file']), 'rb'))})
        return file_params

    def file_content(self, file_):
        """
        文件内容处理
        :return: file_content
        """
        if self.check_type(file_):
            file = self.path_name(file_)
            return open(file, 'rb')

    def file_size(self, file_):
        """获取文件大小"""
        with open(self.path_name(file_), 'rb') as file:
            return file.__sizeof__()


def file_encryption(content, replace_data, method):
    """
    音视频文件加密上传，加密规则：md5（文件内容 + 文件名 + 文件大小）
    :param content: 加密内容
    :param replace_data: replace_data
    :param method: 加密方法
    :return:
    """
    import data_depend
    file_name = content.split(',')[0]
    data_depend = data_depend.DataDepend()
    object_ = data_depend.in_getattr('file_dispose')
    replace_copy = replace_data
    for method_file in content.split(','):
        if re.findall(r'(.*?)\(', method_file):
            function = re.findall(r'(.*?)\(', method_file)[0].strip()
            value = data_depend.getattr_(object_, function, file_name)
            replace_copy = replace_copy.replace(method_file.strip(), value.__str__())
        else:
            value = FileDepend().file_dispose(method_file)
            replace_copy = replace_copy.replace(method_file, value.__str__())
    object_ = data_depend.in_getattr(method)
    func_value = ''
    func_list = re.findall(r'\$md_5{(.*?)}', replace_copy)[0].split(',')
    for func in func_list:
        func_value += func
    value = data_depend.getattr_(object_, method, func_value)
    return replace_data.replace('$' + method + '{' + content + '}', value.__str__())


if __name__ == '__main__':
    file_depend = FileDepend()
    # =====================================================
    print(file_depend.file_dict(
        {'picSize': 512000, 'access_token': '7a4f5829780ef091b3d0cfa912a98c6b', 'file': 'exam/练习图标.jpg'}))
    print(f"文件大小：{file_depend.file_size('study/课程视频.mp4')}")
    print(f"文件路径：{file_depend.path_name('exam/试题音频.mp3')}")
    print(f"文件名称：{file_depend.file_name('exam/试题音频.mp3')}")
    print(f"文件读取：{file_depend.file_dispose('exam/试题音频.mp3')}")
