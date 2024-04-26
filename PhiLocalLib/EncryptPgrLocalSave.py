# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from json import loads
from urllib.parse import quote  # 用来URL编码喵
from xml.dom import minidom as minidom  # 用来格式化xml数据
from xml.etree import ElementTree  # 用来解析xml文件喵

from PhiLocalLib.ActionLib import is_dict, AESEncrypt

# ---------------------- 定义赋值区 ----------------------

# 定义AES CBC加密的密钥(key)和偏移值(iv)喵
key = bytes.fromhex("627ff1942185e011c815e81e639b9a00001c766b826c29bd96578589f19a6fd6")
iv = bytes.fromhex("be56167f83da3befeff81861a5c5f3cd")


def EncryptSave(save_path: str, out_path: str, skip_keys: list):
    """用来加密xml存档喵\n
    save_path：已解密的xml存档文件喵\n
    out_path：加密后的xml存档文件喵\n
    skip_keys：在加密时需要跳过加密的键列表喵"""
    saveTree = ElementTree.parse(save_path)  # 打开并解析存档文件喵
    saveData = saveTree.getroot()  # 进一步解析存档文件喵

    line = 0  # 定义一下起始行数喵，方便debug查错喵(方便查是哪一行数据引发的错误喵)
    for data in saveData.iter():
        line += 1  # 行数递增1喵
        if data.tag == 'map':  # emm...xml文件开头有个map标签喵，这里直接跳过喵
            pass

        elif data.tag == 'string':  # 判断标签是否为string喵，如果是则对其内容进行加密喵
            if data.attrib.get('name', '') not in skip_keys:  # 如果该键在排除列表里喵，则跳过加密喵
                data.attrib['name'] = AESEncrypt(data.attrib.get('name', ''))
                data.text = AESEncrypt(data.text)

            else:
                data.attrib['name'] = quote(data.attrib.get('name', '')).replace('/', '%2F')

            print(f'[Info]{line}  类型喵：{data.tag}，标签喵：{data.attrib["name"]}，内容喵：{data.text}')

        elif data.tag == 'int':  # int类型的都没有加密喵，只经过了URL编码喵
            data.attrib['name'] = quote(data.attrib.get('name', '')).replace('/', '%2F')
            data.attrib['value'] = data.attrib.get('value', '')
            print(f'[Info]{line}  类型喵：{data.tag}，标签喵：{data.attrib["name"]}，内容喵：{data.attrib["value"]}')

    saveTree.write(out_path, xml_declaration=True, method='xml', encoding='utf-8')
    print(f'\n[Info]写入文件成功喵！路径喵：{out_path}')


def EncryptJsonSave(save_path: str, out_path: str, skip_keys: list):
    """用来加密json存档喵\n
    save_path：已解密的xml存档文件喵\n
    out_path：加密后的xml存档文件喵\n
    skip_keys：在加密时需要跳过加密的键列表喵\n
    (注意喵：使用本函数加密后的存档很可能不能正常使用喵)"""
    direct_encrypt = ['info', 'record', 'lock', 'other']  # 直接加密的键列表喵
    key_heads = {  # key键下头部对应键列表喵
        'single': '0key',
        'collection': '1key',
        'illustration': '2key',
        'avatar': '3key'
    }

    key_tail = {  # 一些尾部带特定内容的键列表喵
        'open': 'CollectionTextOpened',
        'grade': 'Grade'
    }

    saveRoot = ElementTree.Element('map')  # 创建一个根元素map喵

    with open(save_path, mode='r', encoding='utf-8') as file:  # 读取待加密的json存档文件喵
        saveData = loads(file.read())
        file.close()  # 随手关闭文件的好习惯喵~

    for keys_name in direct_encrypt:  # 遍历前面直接加密的键列表喵
        for name in saveData[keys_name]:  # 遍历键下面所有键喵
            if name not in skip_keys:  # 判断当前键是否在跳过加密的列表中喵
                string_et = ElementTree.SubElement(saveRoot, 'string', {'name': AESEncrypt(name)})
                string_et.text = AESEncrypt(saveData[keys_name][name])

            else:  # 如果在的话就跳过加密喵，仅进行URL编码喵
                string_et = ElementTree.SubElement(saveRoot, 'string', {'name': quote(name).replace('/', '%2F')})
                string_et.text = saveData[keys_name][name]

    for tail_name in key_tail.keys():  # 遍历尾部带特定内容的键列表喵
        for name in saveData[tail_name]:  #
            string_et = ElementTree.SubElement(saveRoot, 'string', {'name': AESEncrypt(name + key_tail[tail_name])})
            string_et.text = AESEncrypt(saveData[tail_name][name])

    for key_name in saveData['int']:
        attrib = {'name': quote(key_name).replace('/', '%2F'), 'value': saveData['int'][key_name]}
        ElementTree.SubElement(saveRoot, 'int', attrib)

    for key_head in saveData['key']:
        for name in saveData['key'][key_head]:
            string_et = ElementTree.SubElement(saveRoot, 'string', {'name': AESEncrypt(key_heads[key_head] + name)})
            string_et.text = AESEncrypt(saveData['key'][key_head][name])

    for keys_name in saveData['now']:
        if is_dict(saveData['now'][keys_name]):
            for name in saveData['now'][keys_name]:
                string_et = ElementTree.SubElement(saveRoot, 'string', {'name': AESEncrypt(name)})
                string_et.text = AESEncrypt(saveData['now'][keys_name][name])
        else:
            string_et = ElementTree.SubElement(saveRoot, 'string', {'name': AESEncrypt(keys_name)})
            string_et.text = AESEncrypt(saveData['now'][keys_name])

    with open(out_path, mode='w', encoding='utf-8') as file:
        data = minidom.parseString(ElementTree.tostring(saveRoot, encoding='utf-8')).toprettyxml(indent='    ')
        file.write(data)
        file.close()

# ----------------------- 运行区 ----------------------- (bushi)
