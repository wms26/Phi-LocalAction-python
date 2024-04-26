# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiLocalLib.FormatPgrLocalSave import FormatSave  # 用来解密存档喵

# ---------------------- 定义赋值区 ----------------------

savePath = 'DecryptSave.xml'  # 解密存档路径喵
outSave = 'DecryptSave.json'  # 整理后存档路径喵

# ----------------------- 运行区 -----------------------

FormatSave(savePath, outSave)  # 整理存档喵
