## Json存档文件格式说明喵：

本喵感觉也没什么好说明的喵，看完下面这个结构和注释多少也都知道个大概了喵

```
{
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
```

当然info里面也有挺多键的喵：

```
# info部分的键对应用处列表喵(取于FormatPgrLocalSave.py喵)

'NumOfMoney *',  # data的键喵
'LastChapter *',  # 最后停留的章节喵
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

```

关于全头像ID和全曲绘ID列表可以去[文酱](https://github.com/7aGiven)的另一个项目[Phigros_Resource](https://github.com/7aGiven/Phigros_Resource/)里面看看哦喵！(记得点上star防止迷路哦喵！)

