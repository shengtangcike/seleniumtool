'''
模拟键鼠,用来解决廊坊银行密码控件在UI自动化中的输入问题
参考文档
https://blog.csdn.net/sheng_lianfeng/article/details/7209995
'''
from ctypes import *
import time
import os
import win32api


class op_keyboard():

    def __init__(self):
        parentDirPath = os.path.dirname(os.path.abspath(__file__))
        path = parentDirPath + ("\\DD94687.64.dll")  # 这个dll是当前路径下面的
        # print(path)
        self.dd_dll = windll.LoadLibrary(path)

        # DD虚拟码，可以用DD内置函数转换。
        self.vk = {'5': 205, 'c': 503, 'n': 506, 'z': 501, '3': 203, '1': 201, 'd': 403, '0': 210, 'l': 409, '8': 208, 'w': 302,
                'u': 307, '4': 204, 'e': 303, '[': 311, 'f': 404, 'y': 306, 'x': 502, 'g': 405, 'v': 504, 'r': 304, 'i': 308,
                'a': 401, 'm': 507, 'h': 406, '.': 509, ',': 508, ']': 312, '/': 510, '6': 206, '2': 202, 'b': 505, 'k': 408,
                '7': 207, 'q': 301, "'": 411, '\\': 313, 'j': 407, '`': 200, '9': 209, 'p': 310, 'o': 309, 't': 305, '-': 211,
                '=': 212, 's': 402, ';': 410}
        # 需要组合shift的按键。
        self.vk2 = {'"': "'", '#': '3', ')': '0', '^': '6', '?': '/', '>': '.', '<': ',', '+': '=', '*': '8', '&': '7', '{': '[', '_': '-',
                '|': '\\', '~': '`', ':': ';', '$': '4', '}': ']', '%': '5', '@': '2', '!': '1', '(': '9'}

    def down_up(self, code):
        # 进行一组按键。(1：按下；2：抬起)

        self.dd_dll.DD_key(self.vk[code], 1)
        self.dd_dll.DD_key(self.vk[code], 2)
        time.sleep(0.5)
    def tab(self):
        self.dd_dll.DD_key(300, 1)
        self.dd_dll.DD_key(300, 2)
        time.sleep(2)
    def entry(self):
        self.dd_dll.DD_key(313, 1)
        self.dd_dll.DD_key(313, 2)
        time.sleep(2)
    def dd(self, i):  # 自己可以定义各种操作
        # 500是shift键码。
        if i.isupper():
            # 如果想输入大写，先按下shift,再输入字母，然后松掉shift。
            # 按下抬起。
            self.dd_dll.DD_key(500, 1)
            self.down_up(i.lower())
            self.dd_dll.DD_key(500, 2)
            time.sleep(0.2)

        elif i in '~!@#$%^&*()_+{}|:"<>?':
            # 输入特殊字符一样的道理。
            self.dd_dll.DD_key(500, 1)
            self.down_up(self.vk2[i])
            self.dd_dll.DD_key(500, 2)
            time.sleep(0.3)
        else:
            # 输入常规的字符
            self.down_up(i.lower())
            time.sleep(0.5)
    def click(self,x,y,off_1 = True,off_2 = True):
        '''模拟鼠标，位置在鼠标位置'''
        self.dd_dll.DD_mov(x,y)
        time.sleep(0.2)
        if off_1:
            self.dd_dll.DD_btn(1)
        if off_2:
            self.dd_dll.DD_btn(2)
        time.sleep(0.3)

    def shifang(self):
        win32api.FreeLibrary(self.dd_dll._handle)

if __name__ == "__main__":
    op = op_keyboard()
    op.down_up(300)
    # for i in '123456':
    #     op.dd(i)
    # op.shifang()
