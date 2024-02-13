# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
import subprocess
import os
import yaml

# ---------------------- 定义赋值区 ----------------------

local_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的绝对路径喵

config_name = 'config.yaml'
config_path = os.path.join(local_path, config_name)
with open(config_path, mode='r', encoding='utf-8') as config:
    config_data = yaml.safe_load(config)
    config.close()
    del config


def config(key):
    """读取配置文件喵，可供使用的配置喵：\n
    package：phigros对应的包名喵\n
    adb：adb的相对路径喵\n
    java：java的相对路径喵\n
    abe：abe的相对路径喵\n
    save：存档xml文件在解包压缩包里面的路径喵\n
    check_file：文件存在检查喵(0为关1为开喵)\n
    check：检查的文件列表喵\n
    (读取check建议使用config_check代替喵)"""
    return config_data.get(key)


def config_check(key):
    """读取配置文件中检查的文件列表喵，对应的值喵：\n
    adb_file：adb完整性检查列表喵\n
    java_file：java关键文件检查列表喵\n
    java_folder：java关键文件夹检查列表喵"""
    return config_data['check'].get(key)


check_file = config('check_file')  # 是否启用运行前文件检查喵(注意文件检查不完善也不可能完善喵)

adb_path = config('adb')  # adb安卓调试桥的路径喵(用于获取ab备份包喵)
java_path = config('java')  # Java环境主程序的路径喵
abe_path = config('abe')  # abe解包器的路径喵(用于ab解包喵)

adb_files = config_check('adb_file')  # adb工具必要的文件列表喵(理论上有且仅有这三个文件喵)
java_files = config_check('java_file')  # java环境必要的文件列表喵(随便写的喵，但是理论上这仨文件是必须存在的喵)
java_folders = config_check('java_folder')  # java环境必要的文件夹喵(随便写的喵，但是理论上这仨文件夹是必须存在的喵)

adb_path = os.path.join(local_path, adb_path)  # 将此模块绝对路径和adb路径拼接为adb的绝对路径喵
java_path = os.path.join(local_path, java_path)  # 将此模块绝对路径和java路径拼接为java的绝对路径喵
abe_path = os.path.join(local_path, abe_path)  # 将此模块绝对路径和abe路径拼接为abe的绝对路径喵


def check_files(mode=0):  # 闲着没事做的一个极其简易的运行前文件检查喵
    """进行简易的文件检查喵。mode对应的操作喵：\n
    0：进行全部检查喵(默认喵)\n
    1：仅adb检查喵\n
    2：仅java检查喵\n
    3：仅abe检查喵"""
    if not os.path.exists(adb_path) and (mode == 0 or mode == 1):  # 检查adb主程序文件是否存在喵
        print('[Error]adb工具不见了喵！请检查adb_path变量或将adb工具移动到正确路径喵！')
        exit()

    elif not os.path.exists(java_path) and (mode == 0 or mode == 2):  # 检查java主程序是否存在喵
        print('[Error]java环境不见了喵！请检查java_path变量或将java环境移动到正确路径喵！')
        exit()

    elif not os.path.exists(abe_path) and (mode == 0 or mode == 3):  # 检查abe解包工具是否存在喵
        print('[Error]abe工具不见了喵！请检查abe_path变量或将abe工具移动到正确路径喵！')
        exit()

    else:  # 如果主程序都存在喵，再进行一次极其简易的运行环境依赖文件检查喵
        adb_list = [os.path.join(os.path.dirname(adb_path), i) for i in adb_files]  # 构建adb的检查文件列表喵
        java_list = [os.path.join(os.path.dirname(java_path), i) for i in java_files]  # 构建java的检查文件列表喵
        java_flist = [os.path.join(os.path.split(os.path.dirname(java_path))[0], i) for i in
                      java_folders]  # 构建java的检查文件夹列表喵
        adb = adb_list if (mode == 0 or mode == 1) else []
        java = (java_list + java_flist) if (mode == 0 or mode == 2) else []
        for file in adb + java:  # 全部检查一遍喵(注意这只是进行很简单的检查喵，不可能包含所有运行依赖文件)
            if not os.path.exists(file):  # 检查文件是否存在喵
                print(f'[Error]找不到文件喵！路径喵："{file}"')
                exit()


def runCmd(cmd, outerr=False, prerr=True):  # 运行命令并进行简单的判断和输出喵
    """运行cmd命令喵，可按需调整返回内容喵\n
    可用参数喵：\n
    cmd：要运行的命令喵\n
    outerr：是否返回错误内容喵\n
    prerr：是否打印错误到控制台喵"""
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # 运行命令喵
    out, err = process.communicate()  # 获取运行结果喵
    try:  # 先尝试使用utf-8解码喵(万恶的编码问题啊啊啊啊)
        output = out.decode('utf-8')
        error = err.decode('utf-8')
    except UnicodeDecodeError:  # 解码错误就换个编码再试喵
        output = out.decode('gbk')
        error = err.decode('gbk')

    if error != '':  # 如果错误不为空喵(不为空就是有错误喵)
        if prerr:  # prerr就是PrintError(打印错误)喵
            print("\n[Error]发生了错误喵：")
            print(error)  # 输出错误信息喵

        if outerr:  # outerr就是OutputError(输出错误)喵
            return error  # 返回错误以便进一步进行处理

        else:
            return None

    else:
        return output  # 没错误就输出执行结果喵


def adbCheck(doexit=True):
    """检查设备有没有正确连接adb\n
    doexit：检查到未正确连接是否直接exit(默认为True)"""
    runCmd(adb_path + ' devices', prerr=False)
    output = runCmd(adb_path + ' devices', outerr=True)

    if output is not None and '\tdevice' not in output:  # 判断关键字是否存在于输出内容中喵，不存在就证明没有连接adb喵
        if 'unauthorized' in output:
            print('[Error]你没有允许本计算机对手机进行调试喵！')
            if doexit:
                exit()  # 输出完错误直接跑路喵(诶嘿)
            return False

        elif 'recovery' in output:
            print('[Error]喵？你怎么在Recovery模式啊喵？请重启到系统先喵！')
            if doexit:
                exit()  # 输出完错误直接跑路喵(诶嘿)
            return False

        else:
            print('[Error]没有任何设备连接到adb喵！')
            if doexit:
                exit()  # 输出完错误直接跑路喵(诶嘿)
            return False
    return True


def adbCmd(cmd):  # 我也不知道为什么要定义这个喵（
    """便捷(?)运行adb指令喵(?)\n
    cmd：运行adb时附带的参数喵"""
    return runCmd(adb_path + ' ' + cmd)


# ----------------------- 运行区 -----------------------

if check_file > 0:  # 如果check_file的值大于0喵，则会进行文件检查喵
    check_files()
