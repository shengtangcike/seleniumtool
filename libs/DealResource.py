import os
import re
def write_resourse(par,value):
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),
                                    'resourse/resource.txt')
    config_file_path = config_file_path.replace("\\", "/")
    path_res = config_file_path
    f1 = open(path_res, "r", encoding="utf-8")
    datas = f1.readlines()
    # 读取文件
    for i in range(len(datas)):
        datas[i] = datas[i].split("    ")
        if datas[i][0] == par:
            datas[i][-1] = value + "\n"
        datas[i] = "    ".join(datas[i])
    f1.close()
    # 重新写入
    datas = "".join(datas)
    f2 = open(path_res, "w", encoding="utf-8")
    f2.write(datas)
    f2.close()

def read_resource(par):
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),
                                    'resourse/resource.txt')
    config_file_path = config_file_path.replace("\\", "/")
    path_res = config_file_path
    f1 = open(path_res, "r", encoding="utf-8")
    datas = f1.readlines()
    # 读取文件
    value = "不存在变量%s" % par
    for i in range(len(datas)):
        datas[i] = datas[i].split("    ")
        a = datas[i][0]
        if datas[i][0] == par:
            value = datas[i][-1]
    f1.close()
    value = value.replace("\n", "")
    return value

def regular(regex, content, index=1):
    regex = str(regex)
    content = str(content)
    '''
    :param regex: ex,正则表达式,ex,验证码：(.+?)，
    :param content: 字符串
    :param index:
    :return: 根据正则表达式的值提取的内容
    '''
    search_result = '0'
    search = re.compile(regex)
    message = search.search(content)
    if message:
        search_result = message.group(index)
    return search_result
if __name__=="__main__":
    write_resourse("${theborrowerphone_pwd}","a1234567")
    a = read_resource("${theborrowerphone_pwd}")
    print(a)
