# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhigrosLocal.GetPgrUserdata import get_userdata
from PhigrosLocal.ActionLib import config
import json
import sys
import os

# ---------------------- 定义赋值区 ----------------------

arguments = sys.argv  # 获取调用脚本时的参数喵

# ----------------------- 运行区 -----------------------

if len(arguments) == 2 and arguments[1].lower() == 'noget':  # 我也不知道为什么要留一个用来跳过提取userdata的参数喵(也许会有人用吧喵)
    userdata_path = os.path.join(config('outpath'), config('userdata_name'))
else:
    userdata_path = get_userdata()  # "企图"获取userdata喵，保存为.userdata文件喵

with open(userdata_path, mode='r', encoding='utf-8') as file:  # 打开.userdata
    data = json.loads(file.read())  # 读取并解析.userdata
    print(f'[Info]你的sessionToken喵：{data["sessionToken"]}')  # 输出sessionToken
