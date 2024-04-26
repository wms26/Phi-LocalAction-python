# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from lxml import etree  # 用来解析xml文件喵

from PhiLocalLib.ActionLib import AESEncrypt, AESDecrypt

# ---------------------- 定义赋值区 ----------------------

# 定义AES CBC加密的密钥(key)和偏移值(iv)喵
key = bytes.fromhex("627ff1942185e011c815e81e639b9a00001c766b826c29bd96578589f19a6fd6")
iv = bytes.fromhex("be56167f83da3befeff81861a5c5f3cd")


def ModifySave(infile, outfile, name, string, skip=False):
    saveTree = etree.parse(infile)  # 打开并解析存档文件喵
    saveData = saveTree.getroot()  # 进一步解析存档文件喵

    key_name = AESEncrypt(name)
    print(f'[Info]定位的键喵：{name}  =>  {key_name}')

    et_list = saveData.xpath(f'//string[@name="{key_name}"]')
    print(f'[Info]定位结果喵：')

    for et in et_list:
        print(f'{et.text}  =>  {AESDecrypt(et.text)[0]}')

    print(f'\n[Info]共定位到{len(et_list)}个结果喵！')
    if len(et_list) > 0 and not skip:
        print(f'[Warn]注意喵！定位到的结果大于一个喵，如果继续修改则会将会更新全部值喵！')
        while True:
            YorN = input(f'[Action]是否要进行修改喵？(Y / N): ')
            if YorN.lower() == 'y':
                break
            elif YorN.lower() == 'n':
                print('[Info]那就不改了吧喵！')
                exit()

    print(f'[Info]处理结果喵：')
    for et in et_list:
        et.text = AESEncrypt(string)
        print(f'{string}  =>  {AESEncrypt(string)}')

    # 获取原始XML声明
    original_declaration = str(saveTree.docinfo.xml_version) + " encoding='" + str(
        saveTree.docinfo.encoding) + "' standalone='" + str(saveTree.docinfo.standalone) + "'"

    saveTree.write(outfile, pretty_print=True, xml_declaration=original_declaration, encoding='utf-8', standalone='yes')


# ----------------------- 运行区 ----------------------- (bushi)

if __name__ == '__main__':
    ModifySave('../com.PigeonGames.Phigros.v2.playerprefs.xml', '../awa.xml', 'NumOfMoney1', '18', True)
