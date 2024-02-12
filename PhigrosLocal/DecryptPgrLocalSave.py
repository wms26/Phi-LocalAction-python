# 萌新写的代码，可能不是很好，但是已经尽可能注释了，希望各位大佬谅解=v=
import xml.etree.ElementTree as ET
import base64
import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util import Padding
import json
import re

# 定义AES CBC加密的密钥(key)和偏移值(iv)
key = bytes.fromhex("627ff1942185e011c815e81e639b9a00001c766b826c29bd96578589f19a6fd6")
iv = bytes.fromhex("be56167f83da3befeff81861a5c5f3cd")

savePath = '../com.PigeonGames.Phigros.v2.playerprefs.xml'  # 存档文件路径
saveData = ET.parse(savePath).getroot()  # 解析存档文件

# 定义一个字典用于存储解密后数据
game_save = {
    'info': {},  # pgr的亿些信息，乱七八糟
    'record': {},  # 打歌的记录
    'key': {'single': {},  # 在实际解密后带0key头，对应单曲解锁
            'collection': {},  # 在实际解密后带1key头，对应收藏品解锁
            'illustration': {},  # 在实际解密后带2key头，对应曲绘解锁
            'avatar': {},  # 在实际解密后带3key头，对应头像解锁
            'other': {}  # 防止往后版本出现新的键，用于存储无法解析的键
            },
    'grade': {},
    'lock': {},
    'other': {}  # 防止往后版本出现新的键，用于存储无法解析的键
}


def AESDecrypt(string):  # 进行AES CBC解密
    decoded_string = urllib.parse.unquote(string)  # URL解码
    try:
        encrypted_data = base64.b64decode(decoded_string)  # Base64解码
        cipher = AES.new(key, AES.MODE_CBC, iv).decrypt(encrypted_data)  # 创建一个AES解密的对象
        decrypted_data = Padding.unpad(cipher, AES.block_size)  # 对解密后数据进行去填充
        return decrypted_data.decode('utf-8')  # 将解密后的二进制数据进行utf-8解码并返回
    except ValueError:  # 如果解密错误，并且错误类型为ValueError，则
        return decoded_string  # 返回经过URL解码后的数据


def is_dict(string):  # 用来判断一个字符串是否为'预期中的'字典(预期的字符串是那种'{'a': '123'}'这种的)
    try:
        json.loads(string)  # 尝试转换为字典(但字符串'1'和浮点数0.1都可以正常转换，所以需要进一步判断)
    except json.decoder.JSONDecodeError:  # 出现JSONDecodeError错误则返回False
        return False
    try:
        int(string)  # 尝试转换为整数(字符串'1'和浮点数0.1都可以正常转换，但字符串'0.1'不能)
        return False  # 能转换就不是
    except ValueError:  # 不能转换就再进一步判断
        try:
            float(string)  # 尝试转换为浮点数(字符串'0.1'可以正常转换)
            return False  # 能转换就不是
        except ValueError:  # 都不能转换那就是'预期中的'字典
            pass
        return True


i = 1  # 定义一下起始行数，方便debug查错(方便查是哪一行数据引发的错误)
for element in saveData.iter():  # 遍历存档文件里面的对象(应该是叫做对象吧？)
    i += 1  # 行数递增1
    if element.tag == 'string':  # 判断标签是否为'string'，如果是则对其内容进行解密
        attrib_str = AESDecrypt(element.attrib.get('name', ''))  # 取标签'name=**...'的值并解密
        text_str = AESDecrypt(element.text)  # 取该元素的内容
        # if 'key' in attrib_str:
        if re.match(r'^\d+key*.', attrib_str):
            if '0key' in attrib_str:
                game_save['key']['single'][attrib_str.replace('0key', '')] = text_str
            elif '1key' in attrib_str:
                game_save['key']['collection'][attrib_str.replace('1key', '')] = text_str
            elif '2key' in attrib_str:
                game_save['key']['illustration'][attrib_str.replace('2key', '')] = text_str
            elif '3key' in attrib_str:
                game_save['key']['avatar'][attrib_str.replace('3key', '')] = text_str
            else:
                if is_dict(text_str):
                    game_save['record'][attrib_str] = text_str
                else:
                    game_save['key']['other'][attrib_str] = text_str
        elif is_dict(text_str):
            # else:
            game_save['record'][attrib_str] = text_str
        else:
            if 'Grade' in attrib_str:
                text_str = AESDecrypt(element.text)
                game_save['grade'][attrib_str] = text_str
            elif 'lock' in attrib_str:
                text_str = AESDecrypt(element.text)
                game_save['lock'][attrib_str] = text_str
            else:
                game_save['other'][str(attrib_str)] = str(text_str)

    elif element.tag == 'int':
        attrib_str = urllib.parse.unquote(element.attrib.get('name', ''))
        text_str = element.attrib.get('value', '')
        game_save['info'][attrib_str] = text_str

    elif element.tag == 'map':
        attrib_str = None
        text_str = None
    else:
        attrib_str = urllib.parse.unquote(element.attrib.get('name', ''))
        if attrib_str is not None:
            text_str = element.text
            game_save['other'][attrib_str] = text_str
    print(f"{i}  类型: {element.tag}, 标签: {attrib_str}, 内容: {text_str}")

print('setting：\n' + str(game_save['info']))
print('record：\n' + str(game_save['record']))
for keyName in game_save['key'].keys():
    print(f'key({keyName})：\n' + str(game_save['key'][keyName]))
print('other：\n' + str(game_save['other']))

save_json = open('../DecryptSave.json', mode='w', encoding='utf-8')
sava_data = json.dumps(game_save, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
save_json.write(sava_data)
