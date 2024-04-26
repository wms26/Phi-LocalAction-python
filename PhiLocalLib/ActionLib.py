# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from base64 import b64decode, b64encode  # 用来base64编解码喵
from configparser import ConfigParser
from json import loads, dumps
from json.decoder import JSONDecodeError
from os.path import dirname, abspath, join, exists, split
from subprocess import Popen, PIPE
from urllib.parse import unquote, quote  # 用来URL编解码喵

from Crypto.Cipher import AES  # 用来AES加解密喵
from Crypto.Util import Padding  # 用来AES加解密时填充喵

# ---------------------- 定义赋值区 ----------------------

local_path = dirname(abspath(__file__))  # 获取当前脚本的绝对路径喵

# 定义AES CBC加密的密钥(key)和偏移值(iv)喵
aes_key = bytes.fromhex("627ff1942185e011c815e81e639b9a00001c766b826c29bd96578589f19a6fd6")
aes_iv = bytes.fromhex("be56167f83da3befeff81861a5c5f3cd")

config_path = join(local_path, 'config.ini')  # 配置文件的路径喵

# 解析配置文件喵
config_data = ConfigParser()
config_data.read(config_path, 'utf-8')


def config(key: str):
    """读取配置文件喵，可供使用的配置喵：\n
    java：java的相对路径喵\n
    check_file：文件存在检查喵(0为关1为开喵)\n
    (读取check建议使用config_check代替喵)"""
    return config_data['settings'].get(key)


def config_check(key: str):
    """读取配置文件中检查的文件列表喵，对应的值喵：\n
    adb_file：adb完整性检查列表喵\n
    java_file：java关键文件检查列表喵\n
    java_folder：java关键文件夹检查列表喵"""
    return config_data['check'].get(key)


check_file = config('check_file')  # 是否启用运行前文件检查喵(注意文件检查不完善也不可能完善喵)

adb_path = 'adb\\adb.exe'  # adb安卓调试桥的路径喵(用于获取ab备份包喵)
java_path = config('java')  # Java环境主程序的路径喵
abe_path = 'abe.jar'  # abe解包器的路径喵(用于ab解包喵)

adb_files = eval(config_check('adb_file'))  # adb工具必要的文件列表喵(理论上有且仅有这三个文件喵)
java_files = eval(config_check('java_file'))  # java环境必要的文件列表喵(随便写的喵，但是理论上这仨文件是必须存在的喵)
java_folders = eval(config_check('java_folder'))  # java环境必要的文件夹喵(随便写的喵，但是理论上这仨文件夹是必须存在的喵)

adb_path = join(local_path, adb_path)  # 将此模块绝对路径和adb路径拼接为adb的绝对路径喵
java_path = join(local_path, java_path)  # 将此模块绝对路径和java路径拼接为java的绝对路径喵
abe_path = join(local_path, abe_path)  # 将此模块绝对路径和abe路径拼接为abe的绝对路径喵


def check_files(mode: int = 0):  # 闲着没事做的一个极其简易的运行前文件检查喵
    """进行简易的文件检查喵。mode对应的操作喵：\n
    0：进行全部检查喵(默认喵)\n
    1：仅adb检查喵\n
    2：仅java检查喵\n
    3：仅abe检查喵"""
    if not exists(adb_path) and (mode == 0 or mode == 1):  # 检查adb主程序文件是否存在喵
        print('[Error]adb工具不见了喵！请检查adb_path变量或将adb工具移动到正确路径喵！')
        exit()

    elif not exists(java_path) and (mode == 0 or mode == 2):  # 检查java主程序是否存在喵
        print('[Error]java环境不见了喵！请检查java_path变量或将java环境移动到正确路径喵！')
        exit()

    elif not exists(abe_path) and (mode == 0 or mode == 3):  # 检查abe解包工具是否存在喵
        print('[Error]abe工具不见了喵！请检查abe_path变量或将abe工具移动到正确路径喵！')
        exit()

    else:  # 如果主程序都存在喵，再进行一次极其简易的运行环境依赖文件检查喵
        adb_list = [join(dirname(adb_path), i) for i in adb_files]  # 构建adb的检查文件列表喵
        java_list = [join(dirname(java_path), i) for i in java_files]  # 构建java的检查文件列表喵
        java_flist = [join(split(dirname(java_path))[0], i) for i in
                      java_folders]  # 构建java的检查文件夹列表喵
        adb = adb_list if (mode == 0 or mode == 1) else []
        java = (java_list + java_flist) if (mode == 0 or mode == 2) else []
        for file in adb + java:  # 全部检查一遍喵(注意这只是进行很简单的检查喵，不可能包含所有运行依赖文件)
            if not exists(file):  # 检查文件是否存在喵
                print(f'[Error]找不到文件喵！路径喵："{file}"')
                exit()


def runCmd(cmd: str, outError: bool = False, prError: bool = True):  # 运行命令并进行简单的判断和输出喵
    """运行cmd命令喵，可按需调整返回内容喵\n
    可用参数喵：\n
    cmd：要运行的命令喵\n
    outError：是否返回错误内容喵\n
    prError：是否打印错误到控制台喵"""
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)  # 运行命令喵
    out, err = process.communicate()  # 获取运行结果喵
    try:  # 先尝试使用utf-8解码喵(万恶的编码问题啊啊啊啊)
        output = out.decode('utf-8')
        error = err.decode('utf-8')
    except UnicodeDecodeError:  # 解码错误就换个编码再试喵
        output = out.decode('gbk')
        error = err.decode('gbk')

    if error != '':  # 如果错误不为空喵(不为空就是有错误喵)
        if prError:  # prError就是PrintError(打印错误)喵
            print("\n[Error]发生了错误喵：")
            print(error)  # 输出错误信息喵

        if outError:  # outError就是OutputError(输出错误)喵
            return error  # 返回错误以便进一步进行处理

        else:
            return None

    else:
        return output  # 没错误就输出执行结果喵


def adbCheck(doExit: bool = True):
    """检查设备有没有正确连接adb\n
    doExit：检查到未正确连接是否直接exit(默认为True)"""
    runCmd(adb_path + ' devices', prError=False)
    output = runCmd(adb_path + ' devices', outError=True)

    if output is not None and '\tdevice' not in output:  # 判断关键字是否存在于输出内容中喵，不存在就证明没有连接adb喵
        if 'unauthorized' in output:
            print('[Error]你没有允许本计算机对手机进行调试喵！')
            if doExit:
                exit()  # 输出完错误直接跑路喵(诶嘿)
            return False

        elif 'recovery' in output:
            print('[Error]喵？你怎么在Recovery模式啊喵？请重启到系统先喵！')
            if doExit:
                exit()  # 输出完错误直接跑路喵(诶嘿)
            return False

        else:
            print('[Error]没有任何设备连接到adb喵！')
            if doExit:
                exit()  # 输出完错误直接跑路喵(诶嘿)
            return False
    return True


def adbCmd(cmd: str):  # 我也不知道为什么要定义这个喵（
    """便捷(?)运行adb指令喵(?)\n
    cmd：运行adb时附带的参数喵"""
    return runCmd(adb_path + ' ' + cmd)


def is_dict(string: str):
    """用来判断一个字符串是否为'预期的'字典喵\n
    string：要判断的数据喵\n
    (预期的字典是类似'{'a': '123'}'的喵)"""
    try:
        loads(string)  # 尝试loads转换喵(但字符串'1'和浮点数0.1都可以正常转换喵，所以需要进一步判断喵)

    except JSONDecodeError:  # 出现JSONDecodeError错误则返回False喵
        return False

    except TypeError:
        dumps(string)
        return True

    try:
        int(string)  # 尝试转换为整数喵(字符串'1'和浮点数0.1都可以正常转换，但字符串'0.1'不能喵)
        return False  # 能转换就不是喵

    except ValueError:  # 不能转换就再进一步判断喵
        try:
            float(string)  # 尝试转换为浮点数喵(字符串'0.1'可以正常转换喵)
            return False  # 能转换就不是喵

        except ValueError:  # 都不能转换那就是'预期中的'字典喵
            pass

        return True


def AESDecrypt(data: str):
    """进行AES CBC解密喵\n
    会返回处理过的数据和是否解密成功的布尔值\n
    data：需要解密的数据喵"""
    decoded_string = unquote(data)  # URL解码喵
    try:
        encrypted_data = b64decode(decoded_string)  # Base64解码喵
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv).decrypt(encrypted_data)  # 创建一个AES解密的对象并解密喵
        decrypted_data = Padding.unpad(cipher, AES.block_size)  # 对解密后数据进行去填充喵
        return decrypted_data.decode('utf-8'), True  # 将解密后的二进制数据进行utf-8解码并返回喵，并返回True标识解密完成

    except ValueError:  # 如果解密错误喵，并且错误类型为ValueError喵
        return decoded_string, False  # 返回经过URL解码后的数据喵


def AESEncrypt(data: str):
    """进行AES CBC加密喵\n
    data：需要加密的字符串"""
    encode_data = data.encode('utf-8')  # utf-8编码为字节数据喵
    pad_data = Padding.pad(encode_data, AES.block_size)  # 填充数据准备AES CBC加密喵
    encrypt_data = AES.new(aes_key, AES.MODE_CBC, aes_iv).encrypt(pad_data)  # 加密并填充数据喵
    encoded_data = b64encode(encrypt_data)  # Base64编码并转换为字符串喵
    return quote(encoded_data).replace('/', '%2F')  # 对字符串进行URL编码并返回喵


def appIsRunning(package: str):
    """检测某个应用是否在运行喵\n
    package：要检查的应用包名喵"""
    adbCheck()

    output = runCmd(adb_path + ' shell dumpsys window windows', outError=True)  # 使用dumpsys获取系统的窗口信息喵

    if output is not None and package in output:
        return True  # 如果指定的包名包含在这一大堆信息里面喵，就证明正在运行喵

    else:
        return False  # 不在的话就没有在运行喵


def kill_adb():
    """把adb服务关掉避免文件占用"""
    runCmd(adb_path + ' kill-server')


# ----------------------- 运行区 -----------------------

if bool(check_file):  # 如果check_file的值大于0喵，则会进行文件检查喵
    check_files()
