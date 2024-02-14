# 萌新写的代码喵，可能不是很好喵，但是已经尽可能注释了喵，希望各位大佬谅解喵=v=
# ----------------------- 导包区 -----------------------
from PhiLocalLib.ActionLib import is_dict
import xml.etree.ElementTree as ET
import json
import re

# ---------------------- 定义赋值区 ----------------------

# 定义一个字典用于存储解析后数据喵
game_save = {
    'info': {},  # pgr的一些数值喵(?)
    'int': {},  # pgr中int类型的数据喵，不建议乱动喵！
    'record': {},  # 打歌的记录喵(c：Full Combo，s：分数，a：ACC)
    'key': {
        'single': {},  # 实际带0key头喵，对应单曲解锁喵
        'collection': {},  # 实际带1key头喵，对应收藏品解锁喵
        'illustration': {},  # 实际带2key头喵，对应曲绘解锁喵
        'avatar': {},  # 实际带3key头喵，对应头像解锁喵
        'other': {}  # 防止往后版本出现新的键喵，用于存储无法解析的键喵
    },
    'open': {},  # 实际带CollectionTextOpened尾喵，对应收藏品打开情况喵
    'grade': {},  # 实际带Grade尾喵，对应部分歌曲的IN解锁喵
    'lock': {},  # 对应一些歌曲的解锁和关于第八章的解锁喵
    'now': {  # 用来记录你在每章节停留的歌曲喵
        'id': {},  # 曲名喵
        'song': {}  # 歌曲id喵(?)
    },
    'other': {}  # 防止往后版本出现新的键喵，用于存储无法解析的键喵(目前包含大量乱七八糟的键喵)
}

key_pattern = r'^(\d)key.*'
keys = ('single', 'collection', 'illustration', 'avatar')

info_pattern = (  # info部分的正则匹配列表
    r'^NumOfMoney\d',  # data的键喵
    r'^LastChapter.*',  # 最后停留的章节喵
    'chordSupport',  # 多押辅助
    'aPfCisOn',  # AP/FC指示
    'HitFXVolume',  # 打击音效音量
    'hitFxIsOn',  # 打击音效
    'noteScale',  # 按键缩放
    'chartMirror',  # 谱面镜像
    'autoSync',  # 自动同步
    'selfIntro',  # 自我介绍
    'offset',  # 谱面延迟
    'UserIllustrationKeyName',  # 背景曲绘
    'UserIconKeyName',  # 头像
    'PlayerIdAppear',  # 展示用户id(右上角点头像出现那个)
    'lastSyncTime',  # 最后同步时间
    'IsFirstRun',  # 是否是首次运行
    'AlreadyShowCollectionTip',  # 是否展示过收藏品Tip
    'ChallengeModeRank',  # 课题分
    'PromoRizlineAppointmentRead',  # 是否宣传过Rizline(都给我去玩!)
    'bright',  # 背景亮度
    'musicVolume',  # 音乐音量
    'chapter8Passed',  # 第八章通过
    'ReadLanota1',  # 读取Lanota收藏品(解锁两首AT)
)


def FormatSave(infile, outfile):  # 这就是一坨烂屎喵(确信喵)
    """整理并输出json格式文件喵\n
    infile：已解密存档文件喵\n
    outfile：整理后json文件喵"""
    saveTree = ET.parse(infile)  # 打开并解析存档文件喵
    saveData = saveTree.getroot()  # 进一步解析存档文件喵

    line = 1  # 定义一下起始行数喵，方便debug查错喵(方便查是哪一行数据引发的错误喵)
    for data in saveData.iter():  # 遍历存档文件里面的对象喵(应该是叫做对象吧喵？)
        line += 1  # 行数递增1
        if data.tag == 'map':  # emm...xml文件开头有个map标签喵，这里直接跳过喵
            attrib_str = None
            text_str = None

        elif data.tag == 'string':  # 判断标签是否为string喵
            attrib_str = data.attrib.get('name', '')  # 取标签name的值
            text_str = data.text  # 取该元素的内容喵

            if re.match(r'^\dkey.*', attrib_str):  # 用来分类带key头的喵
                head_int = int(re.findall(key_pattern, attrib_str)[0])
                if head_int < len(keys) and len(keys) - head_int <= len(keys):  # 单曲解锁喵
                    game_save['key'][keys[head_int]][attrib_str.replace(str(head_int) + 'key', '')] = text_str

                else:  # 希望这个键永远是空的喵(确信喵)
                    game_save['key']['other'][attrib_str] = text_str

            elif is_dict(text_str):  # 打歌记录喵
                game_save['record'][attrib_str] = text_str

            elif re.match(r'.*CollectionTextOpened$', attrib_str):  # 收藏品打开情况喵
                game_save['open'][attrib_str.replace('CollectionTextOpened', '')] = text_str

            elif re.match(r'.*Grade$', attrib_str):  # 部分歌曲的IN难度解锁喵
                game_save['grade'][attrib_str.replace('Grade', '')] = text_str

            elif 'lock' in attrib_str:  # 对应一些歌曲的解锁和第八章的解锁喵
                game_save['lock'][attrib_str] = text_str

            elif re.match(r'^Now.*', attrib_str):  # 每章节停留的歌曲
                if re.match(r'^NowSongId.*', attrib_str):  # 曲名
                    game_save['now']['id'][attrib_str] = text_str

                elif re.match(r'^NowSong.*', attrib_str):  # 歌曲id
                    game_save['now']['song'][attrib_str] = text_str

                else:
                    game_save['now'][attrib_str] = text_str

            else:  # 太抽象了喵，不想解析了喵（
                for pattern in info_pattern:  # 遍历正则匹配规则喵（
                    if re.match(pattern, attrib_str):
                        game_save['info'][attrib_str] = text_str
                        break

                else:
                    game_save['other'][attrib_str] = text_str

        elif data.tag == 'int':  # int类型的看起来都是一些数值喵(?)
            attrib_str = data.attrib.get('name', '')
            text_str = data.attrib.get('value', '')
            game_save['int'][attrib_str] = text_str

        else:  # 没归类的全部丢到other去喵
            attrib_str = data.attrib.get('name', '')
            if attrib_str is not None:
                text_str = data.text
                game_save['other'][attrib_str] = text_str

            else:
                text_str = None

        print(f"[Info]{line}  类型喵: {data.tag}, 标签喵: {attrib_str}, 内容喵: {text_str}")

    with open(outfile, mode='w', encoding='utf-8') as file:
        file.write(json.dumps(game_save, sort_keys=True, ensure_ascii=False, indent=4))
        print(f'\n[Info]写入文件成功喵！路径喵：{outfile}')
        file.close()

# ----------------------- 运行区 ----------------------- (bushi)
