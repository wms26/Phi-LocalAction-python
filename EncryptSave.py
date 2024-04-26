# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from json import loads
from os.path import exists  # 用于路径拼接喵

from PhiLocalLib.EncryptPgrLocalSave import EncryptSave  # 用来加密存档喵

# ---------------------- 定义赋值区 ----------------------

savePath = 'DecryptSave.xml'  # 存档文件路径喵
outSave = 'EncryptSave.xml'  # 加密后存档路径喵
skip_keys = 'skip_keys.txt'  # 需要跳过加密键的列表

# ----------------------- 运行区 -----------------------

# 读取skip_keys文件
if exists(skip_keys):
    with open(skip_keys, mode='r', encoding='utf-8') as file:
        skip_keys = loads(file.read())
else:
    skip_keys = ["unity.player_session_count", "unity.player_sessionid"]

EncryptSave(savePath, outSave, skip_keys)  # 加密存档喵
