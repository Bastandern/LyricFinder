# LyricFinder - 命令行音乐聚合器

  

本项目是一个“多任务”、“多引擎”的命令行工具，专为音乐爱好者设计。它聚合了来自多个数据源（Genius.com, Wikipedia, TheAudioDB）的信息，并能智能识别本地音乐文件。

---

## 🚀 功能列表



- **歌词抓取 (`song`)**：从 Genius.com 抓取并打印歌词。

- **歌曲简介 (`info`)**：抓取并打印来自 Genius.com 的歌曲简介。

- **艺术家简介 (`info`)**：聚合来自 Wikipedia 的艺术家简介（自动请求简体中文）。

- **专辑封面 (`--art`)**：从 TheAudioDB 抓取并下载专辑封面到 `artworks/` 文件夹。

- **歌词保存 (`--save`)**：将抓取到的纯文本歌词保存到 `lyric/` 文件夹。

- **本地文件识别 (`local`)**：自动读取本地 `.mp3` 和 `.flac` 文件的元数据，并自动为你抓取歌词！

  

---

  

## 🛠️ 核心技术栈

  

* **基础框架:** `click` (用于 CLI 接口), `pyproject.toml` (用于打包)

* **网络抓取:** `requests`, `beautifulsoup4`

* **数据 API:** `wikipedia` (用于艺术家简介), TheAudioDB (用于封面)

* **本地文件:** `mutagen` (用于 .mp3/.flac 元数据), `pathlib` (用于文件路径处理)

  

---


## 📦 安装方法

  

1.  克隆本仓库:

    ```bash

    git clone [请在这里粘贴你自己的 GitHub 仓库 URL]

    cd lyricfinder-project

    ```

  

2.  创建并激活 `venv` 虚拟环境 (推荐使用 Python 3.9+)：

    ```bash

    # (Windows)

    py -3.9 -m venv venv

    .\venv\Scripts\activate

    ```

  

3.  以“可编辑模式”安装所有依赖和工具：

    ```bash

    pip install -e .

    ```

  

---

  

## 💡 使用示例

  

### 1. 抓取歌词、保存 .txt 并下载专辑封面


```bash

(venv)> lyricfinder song "Green Day" "American Idiot" --save --art

正在搜索 'Green Day - American Idiot' ...
--- American Idiot by Green Day ---

[Verse 1]
Don't wanna be an American idiot
Don't want a nation under the new media
And can you hear the sound of hysteria?
The subliminal mindfuck America
[Chorus]
Welcome to a new kind of tension
All across the alienation
Where everything isn't meant to be okay
Television dreams of tomorrow
We're not the ones who're meant to follow
For that's enough to argue
[Verse 2]
Well, maybe I'm the faggot America
I'm not a part of a redneck agenda
Now everybody do the propaganda
And sing along to the age of paranoia
[Chorus]
Welcome to a new kind of tension
All across the alienation
Where everything isn't meant to be okay
Television dreams of tomorrow
We're not the ones who're meant to follow
For that's enough to argue

[成功] 歌词已保存到: lyric\Green Day - American Idiot.txt
```
  
### 2. 获取“聚合”的歌曲/艺术家信息


```bash
(venv)> lyricfinder info "My Chemical Romance" "The Light Behind Your Eyes"
--- 正在聚合 'My Chemical Romance - The Light Behind Your Eyes' 的信息 ---
正在抓取 Genius.com (获取歌曲简介)...
正在抓取 Wikipedia (获取艺术家简介)...
--- 聚合报告 ---

--- 歌曲简介 (来自 Genius.com) ---
“The Light Behind Your Eyes” sees Gerard Way singing a letter to his daughter, Bandit Lee Way, reading similar to a suicide note. Though it could also feature MCR’s fourth studio album, Danger Days‘ lead…

--- 艺术家简介 (来自 Wikipedia) ---
我的另類羅曼史（英語：My Chemical Romance，簡稱MCR）是一組來自美國紐澤西的摇滚樂團，成立於2001年，解散於2013年，后于2019年10月31日宣布回归。在乐队的大部分时间，乐队由傑洛德·威（主唱）、麥基·威（貝斯手）、法蘭克·伊羅（節奏吉他）、雷·托羅（主吉他手）和鮑伯·布萊亞（鼓手）五人組成。樂團成員大多來自紐澤西，只有鼓手鮑伯·布萊亞來自芝加哥。

(来源: https://zh.wikipedia.org/wiki/%E6%88%91%E7%9A%84%E5%8F%A6%E9%A1%9E%E7%BE%85%E6%9B%BC%E5%8F%B2)
```

### 3. 自动识别本地 FLAC/MP3 文件

```bash
(venv)> lyricfinder local "E:\Music\The Cure - Pictures of You.flac"

正在读取文件: E:\Music\The Cure - Pictures of You.flac ...
成功识别! 艺术家: The Cure, 歌曲: Pictures Of You
正在搜索 'The Cure - Pictures Of You' 的歌词...
--- Pictures Of You by The Cure ---

[Verse 1]
I've been looking so long at these pictures of you
...
(歌词内容)
...
```