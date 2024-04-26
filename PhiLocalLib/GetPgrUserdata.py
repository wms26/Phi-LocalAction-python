# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from os.path import dirname, abspath, join, getsize

from PhiLocalLib.ActionLib import adbCheck, adbCmd

# ---------------------- 定义赋值区 ----------------------

local_path = dirname(abspath(__file__))  # 获取当前脚本的绝对路径喵

package_name = 'com.PigeonGames.Phigros'  # Phigros的应用包名喵
adb_path = join(local_path, 'adb\\adb.exe')  # 将此模块绝对路径和adb路径拼接为adb的绝对路径喵，adb安卓调试桥的路径喵
userdata_minsize = 1 * 1024  # 正确userdata大小的最小阈值喵(乘1024是因为os库获取到的以字节为单位喵)
userdata_path = f'/sdcard/Android/data/{package_name}/files/.userdata'


def get_userdata(out_path: str, doExit: bool = True):
    """使用adb获取phigros的.userdata喵\n
    out_path：输出userdata的路径喵\n
    doExit：在发送错误时是否自动退出喵"""
    adbCheck()

    print(f'[Info]正在提取手机Phigros的userdata喵，路径喵："{userdata_path}"')
    output = adbCmd(f'pull {userdata_path} {out_path}')
    print(output)

    data_size = getsize(out_path)
    if data_size <= userdata_minsize:
        print(
            f'[Error]获取到的.userdata大小不足{userdata_minsize / 1024}KB喵！仅有{data_size / 1024}KB喵(共{data_size}字节喵)！')
        print('[Info]请再试几次喵，如果多次出现次错误请附带日志反馈喵！')
        if doExit:
            exit()  # 输出完错误直接跑路喵(诶嘿)

    print(f'[Info]提取完成喵！路径喵："{out_path}"')
