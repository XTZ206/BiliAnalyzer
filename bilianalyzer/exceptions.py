class AnalyzerException(Exception):
    """
    BiliAnalyzer 基类异常。
    """

    def __init__(self, msg: str = "出现了错误，但是未说明具体原因"):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg


class FileFormatException(AnalyzerException):
    def __init__(self, msg: str = "文件格式错误"):
        super(FileFormatException, self).__init__(msg)
        self.msg = msg


class FileNotSelectedException(AnalyzerException):
    def __init__(self, msg: str = "未指定文件路径错误"):
        super(FileNotSelectedException, self).__init__(msg)
        self.msg = msg


class FileModeException(AnalyzerException):
    def __init__(self, msg: str = "文件模式错误"):
        super(FileModeException, self).__init__(msg)
        self.msg = msg


class StorageException(AnalyzerException):
    def __init__(self, msg: str = "保存文件时发生错误"):
        super(StorageException, self).__init__(msg)
        self.msg = msg


class CheckingException(AnalyzerException):
    def __init__(self, msg: str = "参数未检查错误"):
        super(CheckingException, self).__init__(msg)
        self.msg = msg
