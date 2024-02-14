<div align="center">
<h1>Phi-LocalAction-python</h1>
使用python实现的phigros本地数据操作喵<br>
注意本项目已经猫化了喵，带有大量喵元素喵，介意者勿用喵！<br><br>

[![Github仓库喵](https://img.shields.io/badge/github-Phi--LA--py-red?style=for-the-badge&logo=Github)](https://github.com/wms26/PhigrosLocal)

<img src="https://counter.seku.su/cmoe?name=phi-local-py&theme=r34" title="喵喵喵~"/><br>

[![PhigrosLibrary](https://img.shields.io/badge/文酱-Phigros_Library-blue?style=for-the-badge&logo=Github)](https://github.com/7aGiven/PhigrosLibrary)
[![phi-plugin](https://img.shields.io/badge/废酱-phi--plugin-blue?style=for-the-badge&logo=github)](https://github.com/Catrong/phi-plugin)


[![Phi-LocalAction-python_v0.8beta-Alpha](https://img.shields.io/badge/Latest--release-Phi--LA--py__v0.8beta--Alpha-green?style=for-the-badge&logo=Github)](https://github.com/wms26/Phi-LocalAction-python/releases/download/v0.8beta-Alpha/Phi-LocalAction-python_v0.8beta-Alpha.zip)
</div>

## 声明喵：

本项目仅作为学习参考用喵，请勿用作违法用途喵！(虽然我也想不到能做什么违法的事情就是了喵)

编写本项目所需的资料和资源均源于互联网收集喵(所以本人就是一个废物喵，什么都要依靠互联网喵(bushi))

本项目的初衷仅仅是为了供学习参考使用喵，本人从未想过要破坏音游圈的游戏平衡喵！(目前修改本地存档的操作不可能完成，如果你是抱着该目的来的话请另寻他路喵)

## 环境准备喵！

1. 编写本项目时使用的是 **python3.9.13** 的喵，不能完全保证其他版本会不会出现问题喵，建议使用 **python>=3.9** 来运行喵~

2. 注意在使用本项目前要先安装`PhiLocalLib/requirement.txt`中的模块喵

3. abe的运行是需要 **java11** 环境的喵，本项目调用的是便携版 **java11(jdk11)** 的喵，需要自行[**下载**](https://www.oracle.com/java/technologies/downloads/#java11-windows)解压后放在 **PhiLocalLib** 下喵~

4. adb工具本项目仓库已经在 **PhiLocalLib** 文件夹下了喵，非必要不建议去换adb版本喵~

5. abe工具本项目仓库也已经有了喵，如果要自己下载的话可以去[**此处**](https://github.com/nelenkov/android-backup-extractor/releases)下载新版来替换 **PhiLocalLib** 下的 **abe.jar** 喵~

## 使用喵！

### 安装pyyaml库和pycryptodome库喵：(因为本项目配置文件用的是yaml)

直接运行喵：(用`pip`也可以的亚子喵(?))

```
pip3 install pyyaml pycryptodome lxml
```

或者如果想要一点仪式感也可以运行喵：

```
pip3 -r PhiLocalLib/requirement.txt
```

### <br>获取手机phigros本地存档喵：

```
python GetSave.py [nogetab]
```
`nogetab`：不获取ab文件喵，直接开始解包喵（**注意这个是方便debug的喵，不懂最好就别带这个参数**，只是在debug时已经获取过ab备份包时可以用来跳过获取喵）

注意在获取ab备份包时尽可能**不要输入密码喵**！（就算它给你输密码的地方也不要输先喵！除非是不输密码就不能备份的情况喵，要不然就不要输密码喵！避免发生奇奇怪怪的错误bug喵）

### <br>存档解密喵：

目前能解密存档所有数据喵，输出同原存档一样的xml格式文件喵

```
python DecryptSave.py
```

运行后会读取目录下的`com.PigeonGames.Phigros.v2.playerprefs.xml`存档喵，然后输出已解密的`DecryptSave.xml`文件喵

### <br>存档解析：

说是说解析喵，严格来讲并不完全是喵，所以可以说是将xml存档转换解析并整理归类输出为json文件喵，但是大部分数据条目因为其命名的难懂性所以不整理归类了喵（已经整理差不多了喵，剩下的整理了也没有什么大用了喵）

```
python FormatSave.py
```

运行后会读取目录下`DecryptSave.xml`已解密存档文件喵，然后经解析后输出`DecryptSave.json`文件喵

`DecryptSave.json`文件的数据结构可以参考`PhiLocalLib/FormatPgrLocalSave.py`中`game_save`的定义喵，也可以参考[JsonSave格式说明喵](./Json_Info.md)

### <br>获取sessionToken喵：

Mivik已经做了有手机版软件了喵，其他提取方法可以参考一下[Mivik的bot说明文档](https://mivik.moe/pgr-bot-help/)喵，要软件可以去[Mivik的频道](https://pd.qq.com/s/dxabi3law)喵，频道里面也有完整的bot可以用喵

```
python GetSession.py [noget]
```

`noget`：不获取userdata文件喵，直接读取.userdata（**注意这个是方便debug的喵，不懂最好就别带这个参数**，只是在debug时已经获取过userdata时可以用来跳过获取喵）

### 关于配置文件config.yaml：

直接拿编辑器打开`PhiLocalLib/config.yaml`就可以了喵，本喵认为那点注释足够说明清楚各项配置的用途了喵

## 未来计划功能喵！

- [ ] **存档提取喵：**(已模块化喵)(注释较为完整喵)
    - [x] 通过adb获取ab提取存档喵
    - [x] 防呆措施喵(bushi)
    - [ ] 可利用root权限直接提取存档喵(快了快了喵)


- [x] **存档解密喵：**(已模块化喵)(注释较为完整喵)
    - [x] 完全解密所有数据喵


- [x] **存档解析喵：**(已模块化喵)(注释较为完整喵)
  - [x] 简单归类整理各数据


- [ ] **存档修改喵：**(已废弃，后续不再更新此功能)
    - [ ] 经过测试，鸽游对本地存档似乎做了一些检查，所以修改本地存档基本不可能完成


- [ ] **其他喵：**
    - [x] fuck_adb(adb的文件占用是真的烦喵！(恼))
    - [x] 获取本地SessionToken喵
    - [x] 将各功能模块化喵(更方便使用喵，但是这可能得到以后才能真正完成喵)

## 喵喵喵~

此项目仅仅用于本地操作喵，云端操作可以看看[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)喵(本文档前面也留了链接喵)

喵！小小宣传一下[废酱](https://github.com/Catrong)的项目[Phi-Plugin](https://github.com/catrong/phi-plugin)，是一个适用于`Yunzai-Bot V3`的`Phigros`辅助插件喵！(本文档前面也留了链接喵)

介于本喵懒惰的性格喵，本项目也许应该可能大概会在未来也可能在现在某个时间突然停更或者消失喵(bushi)

(小声BB：我也不知道我为什么要写本地存档操作喵，就当是消遣吧喵。想专门搞这方面的大佬还是移步到[文酱](https://github.com/7aGiven)的项目[PhigrosLibrary](https://github.com/7aGiven/PhigrosLibrary)吧喵)

(快去给[文酱](https://github.com/7aGiven)和[废酱](https://github.com/Catrong)的项目点star喵！)
