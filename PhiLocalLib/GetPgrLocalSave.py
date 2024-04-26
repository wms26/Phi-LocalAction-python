# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from os import makedirs
from os.path import dirname, abspath, join, getsize, basename  # 目录和路径及文件的操作
from shutil import move, rmtree  # 用于在解压时临时目录的操作
from tarfile import TarError
from tarfile import open as tarOpen  # 解压解包后的压缩包文件
from zlib import decompress

from PhiLocalLib.ActionLib import config, runCmd, appIsRunning

# ---------------------- 定义赋值区 ----------------------

local_path = dirname(abspath(__file__))  # 获取当前脚本的绝对路径喵

ab_minSize = 1 * 1024  # 正确ab备份包大小的最小阈值喵(乘1024是因为os库获取到的以字节为单位喵)

package_name = 'com.PigeonGames.Phigros'  # Phigros的应用包名喵
adb_path = join(local_path, 'adb\\adb.exe')  # 将此模块绝对路径和adb路径拼接为adb的绝对路径喵，adb安卓调试桥的路径喵(用于获取ab备份包喵)
java_path = join(local_path, config('java'))  # 将此模块绝对路径和java路径拼接为java的绝对路径喵，Java环境主程序的路径喵
abe_path = join(local_path, 'abe.jar')  # 将此模块绝对路径和abe路径拼接为abe的绝对路径喵，abe解包器的路径喵(用于ab解包喵)
save_path = 'apps/com.PigeonGames.Phigros/sp/com.PigeonGames.Phigros.v2.playerprefs.xml'  # 存档文件在压缩包中的路径喵(用于解压提取出存档喵)


def get_ab(ab_path: str, check_run: bool = True, doExit: bool = True):
    """通过adb获取ab备份包喵\n
    ab_path：AB备份包的输出路径喵\n
    check_run：是否启用应用运行检查喵(默认为True喵)\n
    doExit：在发生错误时是否自动退出喵(默认为True喵)\n
    (check_run就是appIsRunning()喵)\n
    (注：会返回一个字典喵，包含ab_path和package_name喵)"""
    print('[Info]注意：获取phigros的ab备份包需要使phigros处于运行状态喵！')

    if check_run and appIsRunning(package_name) is False:  # 判断phigros是否在运行喵，如果check_run不为0则跳过检测喵
        print('[Error]尚未检测到phigros正在运行喵！检测包名：' + package_name)
        if doExit:
            exit()  # 输出完错误直接跑路喵(诶嘿)

    print('[Info]正在获取phigros的ab备份包喵，将会弹出窗口来输入密码喵(如果可以不输入就空着喵，密码自己要记得喵！)')
    print(runCmd(adb_path + f' backup -f {ab_path} {package_name}'))  # 使用adb获取phigros的ab备份包，并且会返回错误信息喵

    ab_size = getsize(ab_path)  # 获取ab备份包的大小喵

    if ab_size <= ab_minSize:  # 如果大小小于最小阈值喵，证明没有正确获取到ab备份包喵
        print(f'[Error]获取到的ab备份包大小不足{ab_minSize / 1024}KB！仅有{ab_size / 1024}KB喵(共{ab_size}字节喵)！')
        print(
            '[Info]这可能是因为phigros并没有在正常运行喵，请在重新打开phigros之后再试一遍喵！(若多次出现此错误喵，请尝试更换adb版本后再试喵)')
        if doExit:
            exit()  # 输出完错误直接跑路喵(诶嘿)

    else:
        print(f'[Info]获取成功喵，保存路径为"{ab_path}"')
        return {'ab_path': ab_path, 'package_name': package_name}  # 我也不知道为什么要返回这样子的数据喵，也许以后会有人用到喵(?)


def unpack_ab_java(ab_path: str, out_path: str, pwd='', doExit=True):
    """使用abe解包ab备份包喵\n
    ab_path：AB备份包的路径喵\n
    out_path：tar解包文件输出路径喵\n
    pwd：ab备份包的密码喵(默认为空喵)\n
    doExit：在发生错误时是否自动退出喵\n
    (注意喵：abe运行需要java环境支持)"""
    print('[Info]正在解包ab备份包喵，路径喵：' + ab_path)

    # 使用abe进行解包喵，并且会返回错误信息喵，同时不输出错误信息到控制台喵(这个特性很迷喵，解包成功了也会输出到error里面去喵)
    output = runCmd(f"{java_path} -jar {abe_path} unpack {ab_path} {out_path} {pwd}", True, False)

    if 'bytes written to' in output:  # 判断解包成功关键字是否包含在输出结果中喵
        print(f'[Info]解包完毕喵！保存路径喵："{out_path}"')

    elif 'password not specified' in output:  # 如果输出包含'password not specified'关键字那就是ab包已被加密但未指定密码喵
        print('\n[Error]发生了错误喵：\n' + output)
        while True:
            ab_passwd = input('[Action]ab包已加密喵！请输入设置的密码喵：')
            if ab_passwd == '':
                print('[Error]输入的密码为空喵！请正确输入密码喵！')
            else:
                break

        unpack_ab_java(ab_path, out_path, ab_passwd)

    elif 'bad key is used' in output:  # 如果输出包含'bad key is used'关键字那就是密码错误喵
        print('\n[Error]发生了错误喵：\n' + output)
        print(f'[Error]解包发生错误喵！指定的密码不正确喵！文件路径：{ab_path}')
        while True:
            ab_passwd = input('[Action]指定的密码错误喵！请输入正确的密码喵：')
            if ab_passwd == '':
                print('[Error]输入的密码为空喵！请正确输入密码喵！')
            else:
                break

        unpack_ab_java(ab_path, out_path, ab_passwd)

    else:
        print('\n[Error]发生了错误喵：\n' + output)
        print(f'[Error]解包发生错误喵！如果在获取ab备份包时设置了密码喵，请指定该密码再试喵！')
        print(f'java路径：{java_path}，abe路径喵：{abe_path}，文件路径喵：{ab_path}，输出路径喵：{out_path}')
        if doExit:
            exit()  # 输出完错误直接跑路喵(诶嘿)


def unpack_ab(ab_path: str, tar_path: str):
    """解包ab备份包喵\n
    ab_path：ab备份包的路径喵\n
    tar_path: 输出tar的路径\n
    (注意喵：本函数仅能解包无加密的ab备份包喵！)"""
    print('[Info]注意喵：本函数仅能解包无加密的ab备份包喵！')
    print('[Info]正在解包ab备份包喵，路径喵：' + ab_path)

    with open(ab_path, 'rb') as file:  # 打开ab备份包
        file.seek(24)
        ab_data = file.read()

    unzip_data = decompress(ab_data)  # 使用zlib进行解压缩

    with open(tar_path, 'wb') as file:  # 写入解压缩后的数据
        file.write(unzip_data)
    print(f'[Info]解包完毕喵！保存路径喵："{tar_path}"')


def unzip_save(tar_path: str, out_path: str):
    """提取解包后的压缩包中的存档喵\n
    tar_path：解包输出的tar压缩包路径喵\n
    out_path：存档输出的路径喵"""
    try:
        with tarOpen(tar_path, "r:") as tar:
            if save_path in tar.getnames():  # 检查要提取的文件是否在tar压缩包中喵
                makedirs(join(out_path, 'temp'))  # 创建临时目录喵
                tar.extract(save_path, join(out_path, 'temp'))  # 提取存档文件到临时目录内喵
                move(str(join(out_path, 'temp', save_path)), str(join(out_path, basename(save_path))))  # 移动存档到保存目录喵
                rmtree(join(out_path, 'temp'))  # 删除临时目录喵
                print(f'[Info]存档"{save_path}"喵，已解压至："{out_path}"')

            else:
                print(f"[Error]在压缩包中未找到存档文件喵：'{save_path}'")
                exit()

    except TarError as e:
        print(f"[Error]提取文件时发生错误喵: {e}")
        exit()

# ----------------------- 运行区 ----------------------- (bushi)
