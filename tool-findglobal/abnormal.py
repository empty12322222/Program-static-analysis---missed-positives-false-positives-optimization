import sys

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """全局异常处理器"""
    print("解析失败")
    # 可以选择是否打印堆栈跟踪或其他信息