# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiLocalLib.GetPgrUserdata import get_userdata  # 用来获取userdata文件喵
from PhiLocalLib.ActionLib import config  # 读取配置文件喵
import json  # 用来解析.userdata喵
import sys  # 获取传入的参数喵
import os  # 用来路径拼接喵

# ---------------------- 定义赋值区 ----------------------

arguments = sys.argv  # 获取调用脚本时的参数喵

# ----------------------- 运行区 -----------------------

if len(arguments) == 2 and arguments[1].lower() == 'noget':  # 我也不知道为什么要留一个用来跳过提取userdata的参数喵(也许会有人用吧喵)
    userdata_path = os.path.join(config('outpath'), config('userdata_name'))
else:
    userdata_path = get_userdata()  # "企图"获取userdata喵，保存为.userdata文件喵

with open(userdata_path, mode='r', encoding='utf-8') as file:  # 打开.userdata喵
    data = json.loads(file.read())  # 读取并解析.userdata喵
    print(f'[Info]你的sessionToken喵：{data["sessionToken"]}')  # 输出sessionToken喵
