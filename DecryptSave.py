# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiLocalLib.ActionLib import config  # 读取配置文件喵
from PhiLocalLib.DecryptPgrLocalSave import DecryptSave  # 用来解密存档喵
import os.path  # 用于路径拼接喵

# ---------------------- 定义赋值区 ----------------------

# savePath = os.path.join(config('outpath'), 'EncryptJsonSave.xml')  # 存档文件路径喵
# outSave = os.path.join(config('outpath'), 'DecryptJsonSave.xml')  # 解密后存档路径喵
savePath = os.path.join(config('outpath'), 'com.PigeonGames.Phigros.v2.playerprefs.xml')  # 存档文件路径喵
outSave = os.path.join(config('outpath'), 'DecryptSave.xml')  # 解密后存档路径喵

# ----------------------- 运行区 -----------------------

DecryptSave(savePath, outSave)  # 解密存档喵
