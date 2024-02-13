# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from Crypto.Cipher import AES  # 用来AES解密喵
from Crypto.Util import Padding  # 用来AES解密后去填充喵
import xml.etree.ElementTree as ET  # 用来解析xml文件喵
import base64  # 用来base64解码喵
import urllib.parse  # 用来URL解码喵

# ---------------------- 定义赋值区 ----------------------

# 定义AES CBC加密的密钥(key)和偏移值(iv)喵
key = bytes.fromhex("627ff1942185e011c815e81e639b9a00001c766b826c29bd96578589f19a6fd6")
iv = bytes.fromhex("be56167f83da3befeff81861a5c5f3cd")


def AESDecrypt(string):  #
    """进行AES CBC解密喵，"""
    decoded_string = urllib.parse.unquote(string)  # URL解码喵
    try:
        encrypted_data = base64.b64decode(decoded_string)  # Base64解码喵
        cipher = AES.new(key, AES.MODE_CBC, iv).decrypt(encrypted_data)  # 创建一个AES解密的对象并解密喵
        decrypted_data = Padding.unpad(cipher, AES.block_size)  # 对解密后数据进行去填充喵
        return decrypted_data.decode('utf-8')  # 将解密后的二进制数据进行utf-8解码并返回喵

    except ValueError:  # 如果解密错误喵，并且错误类型为ValueError喵
        return decoded_string  # 返回经过URL解码后的数据喵


def DecryptSave(infile, outfile):
    saveTree = ET.parse(infile)  # 打开并解析存档文件喵
    saveData = saveTree.getroot()  # 进一步解析存档文件喵

    line = 1  # 定义一下起始行数喵，方便debug查错喵(方便查是哪一行数据引发的错误喵)
    for data in saveData.iter():
        line += 1  # 行数递增1喵
        if data.tag == 'map':  # emm...xml文件开头有个map标签喵，这里直接跳过喵
            pass
        elif data.tag == 'string':  # 判断标签是否为string，如果是则对其内容进行解密
            data.attrib['name'] = AESDecrypt(data.attrib.get('name', ''))
            data.text = AESDecrypt(data.text)
            print(f'[Info]{line}  类型喵：{data.tag}，标签喵：{data.attrib["name"]}，内容喵：{data.text}')
        elif data.tag == 'int':  # int类型的都没有加密喵，只经过了URL编码
            data.attrib['name'] = urllib.parse.unquote(data.attrib.get('name', ''))
            data.attrib['value'] = data.attrib.get('value', '')
            print(f'[Info]{line}  类型喵：{data.tag}，标签喵：{data.attrib["name"]}，内容喵：{data.attrib["value"]}')

    saveTree.write(outfile)
    print(f'\n[Info]写入文件成功喵！路径喵：{outfile}')

# ----------------------- 运行区 ----------------------- (bushi)
