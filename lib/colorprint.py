import os
import sys

class Color:
    # 定义彩色字体
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'

def cprint(text,style:Color=Color.WHITE,isstr:bool=False):
    """ 定义彩色输出函数 """
    if isstr:
        if sys.stdout.isatty():
            return style+str(text)+"\033[0m"
        else:
            return str(text)
    if sys.stdout.isatty():
        print(f"{style}{str(text)}\033[0m")
    else:
        print(str(text))

def create_clickable_link(url):

    """ 定义cmd跳转链接 """
    if len(url)>60:
        s_url = url[:60]+"..."
        return f"\033]8;;{url}\a{s_url}\033]8;;\a"
        
    return f"\033]0m;;{url}\a{url}\033]8;;\a"
    # return url

os_columns = os.get_terminal_size().columns
def zone_print(color):
    def wapper(func):
        def inner_wapper():
            line = "*"*os_columns
            cprint(line,color)
            print("\n")
            func()
            print("\n")
            cprint(line,color)
        return inner_wapper
    return wapper

if __name__ == "__main__":
    @zone_print(Color.BLUE)
    def func():
        print("hello")

    func()