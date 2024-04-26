# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from json import dumps
from urllib.parse import unquote  # 用来URL解码喵
from xml.etree import ElementTree  # 用来解析xml文件喵

from PhiLocalLib.ActionLib import config, AESDecrypt  # 用来读取配置文件


# ---------------------- 定义赋值区 ----------------------


def DecryptSave(save_path: str, out_path: str):
    """解密存档xml文件喵\n
    save_path：存档xml文件路径喵\n
    out_path：解密的存档输出路径喵"""
    skip_keys = []  # 用来记录需要跳过加密的键喵

    saveTree = ElementTree.parse(save_path)  # 打开并解析存档文件喵
    saveData = saveTree.getroot()  # 进一步解析存档文件喵

    line = 1  # 定义一下起始行数喵，方便debug查错喵(方便查是哪一行数据引发的错误喵)
    for data in saveData.iter():
        line += 1  # 行数递增1喵
        if data.tag == 'map':  # emm...xml文件开头有个map标签喵，这里直接跳过喵
            pass

        elif data.tag == 'string':  # 判断标签是否为string，如果是则对其内容进行解密
            data.attrib['name'], skip = AESDecrypt(data.attrib.get('name', ''))
            if skip:
                data.text, _ = AESDecrypt(data.text)

            else:
                data.text = unquote(data.text)
                skip_keys.append(data.attrib.get('name', ''))

            print(f'[Info]{line}行\t类型喵：{data.tag}，标签喵：{data.attrib["name"]}，内容喵：{data.text}')

        elif data.tag == 'int':  # int类型的都没有加密喵，只经过了URL编码
            data.attrib['name'] = unquote(data.attrib.get('name', ''))
            data.attrib['value'] = data.attrib.get('value', '')
            print(f'[Info]{line}行\t类型喵：{data.tag}，标签喵：{data.attrib["name"]}，内容喵：{data.attrib["value"]}')

    saveTree.write(out_path, encoding='utf-8', xml_declaration=True, method='xml')
    print(f'\n[Info]写入文件成功喵！路径喵：{out_path}')

    with open('skip_keys.txt', mode='w', encoding='utf-8') as file:
        print(f'\n[Info]需要跳过的值已记录喵：\n{skip_keys}')
        file.write(dumps(skip_keys, ensure_ascii=False, indent=4))

# ----------------------- 运行区 ----------------------- (bushi)
