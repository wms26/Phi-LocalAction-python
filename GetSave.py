# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from ToolsLib.GetPgrLocalSave import get_ab, unpack_ab, unzip_save, kill_adb  # 导入用来提取存档的函数喵
import sys  # 用于接受命令行参数喵

# ---------------------- 定义赋值区 ----------------------

ab_pwd = ''  # 如果ab备份包设置了密码喵，请在此处设置喵
arguments = sys.argv  # 获取调用脚本时的参数喵
check_run = 0  # 是否跳过phigros是否正在运行检测喵

# ----------------------- 运行区 -----------------------

if len(arguments) == 1 or arguments[1].lower() != 'nogetab':  # 我也不知道为什么要留一个用来跳过提取ab备份包的参数喵(也许会有人用吧喵)
    get_ab(check_run)  # "企图"获取ab备份包喵，保存为ab文件喵
    kill_adb()

unpack_ab(ab_pwd)  # 解包ab备份包喵，保存为压缩包喵
unzip_save()  # 从解包后的压缩包里面提取出存档文件喵，保存为xml文件喵
