import time
def phone_time():
    '''
    :return: 生成类手机号字符串
    '''
    pt = str(time.time())
    pt = pt.split(".")
    phone_time = pt[0] + pt[1][0]
    print(phone_time)
    return phone_time