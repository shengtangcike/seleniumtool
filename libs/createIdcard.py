from datetime import date
from datetime import timedelta
import random,os

class CreateIdCard(object):
    def __init__(self):
        pass
    def getdistrictcode(self):
        codelist = []
        codecity = []
        current_path = os.path.abspath(__file__)
        resoursepath = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + "."),'districtcode.txt')
        resoursepath = resoursepath.replace("\\", "/")
        print(resoursepath)
        file = open(resoursepath,"r",encoding="utf-8")
        lines = file.readlines()  # 逐行读取
        for line in lines:
            if line.lstrip().rstrip().strip() != '' and (line.lstrip().rstrip().strip())[:6][-2:] != '00':
                # 如果每行中去重后不为空，并且6位数字中最后两位不为00，则添加到列表里。（最后两位为00时为省份或地级市代码）
                codelist.append(line[:6])
                codecity.append(line[10:])

        return codelist,codecity

    def gennerator(self):
        codelist = self.getdistrictcode()[0]
        id = codelist[random.randint(0, len(codelist))]  # 地区项
        id = id + str(random.randint(1970, 1998))  # 年份项
        da = date.today() + timedelta(days=random.randint(1, 365))  # 月份和日期项
        id = id + da.strftime('%m%d')
        id = id + str(random.randint(100, 300))  # ，顺序号简单处理

        i = 0
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                     '10': '2'}  # 校验码映射
        for i in range(0, len(id)):
            count = count + int(id[i]) * weight[i]
        id = id + checkcode[str(count % 11)]  # 算出校验码
        return id


if __name__ == '__main__':
    a = CreateIdCard()
    idcard = a.gennerator()
    print(idcard)
