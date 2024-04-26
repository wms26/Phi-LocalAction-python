# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiLocalLib.DecryptPgrLocalSave import DecryptSave  # 用来解密存档喵

# ---------------------- 定义赋值区 ----------------------

# savePath = 'EncryptJsonSave.xml'  # 存档文件路径喵
# outSave = 'DecryptJsonSave.xml'  # 解密后存档路径喵
savePath = 'com.PigeonGames.Phigros.v2.playerprefs.xml'  # 存档文件路径喵
outSave = 'DecryptSave.xml'  # 解密后存档路径喵

# ----------------------- 运行区 -----------------------

DecryptSave(savePath, outSave)  # 解密存档喵
