# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiLocalLib.ActionLib import config  # 读取配置文件喵
from PhiLocalLib.EncryptPgrLocalSave import EncryptJsonSave  # 用来加密存档喵
import os.path  # 用于路径拼接喵
import json

# ---------------------- 定义赋值区 ----------------------

savePath = os.path.join(config('outpath'), 'DecryptSave.json')  # 存档文件路径喵
outSave = os.path.join(config('outpath'), 'EncryptJsonSave.xml')  # 加密后存档路径喵

# ----------------------- 运行区 -----------------------

if os.path.exists(os.path.join(config('outpath'), 'skip_keys.txt')):
    with open(os.path.join(config('outpath'), 'skip_keys.txt'), mode='r', encoding='utf-8') as file:
        skip_keys = json.loads(file.read())
else:
    skip_keys = ["unity.player_session_count", "unity.player_sessionid"]

EncryptJsonSave(savePath, outSave, skip_keys)  # 加密存档喵
