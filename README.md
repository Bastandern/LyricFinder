# 🎶 LyricFinder - 命令行音乐聚合器

## 简介

LyricFinder 是一个功能强大、速度极快的命令行工具（CLI），旨在快速获取歌曲歌词、艺术家简介和专辑封面。它聚合了多个在线数据源（Genius、Wikipedia 和 TheAudioDB），让你可以完全在终端中完成所有音乐信息检索工作，无需打开浏览器。

## ✨ 主要功能

- **歌词抓取 (`song`)**: 从 Genius.com 快速获取歌曲的完整歌词。
    
- **信息聚合 (`info`)**: 同时获取歌曲简介 (来自 Genius) 和艺术家简介 (来自 Wikipedia)。
    
- **本地文件支持 (`local`)**: 读取本地 MP3 或 FLAC 文件的 ID3 标签，自动搜索歌词。
    
- **附件下载**:
    
    - 使用 `--save` 选项将歌词保存为 `.txt` 文件。
        
    - 使用 `--art` 选项下载专辑封面图片。
        

## ⚠️ 重要提示：外网连接要求

**本工具的核心功能依赖于外部 API (Genius.com, Wikipedia, TheAudioDB.com) 进行数据抓取。因此，运行 LyricFinder 必须保证您的计算机能够连接到外部网络（外网）。**

## 🚀 安装与使用

你有两种方式安装和使用 LyricFinder：

### 选项 A: Python 环境安装 (推荐开发者使用)

确保你安装了 Python 3.8+ 并激活了虚拟环境。

1. **克隆仓库:**
    
    ```
    git clone [https://github.com/YourUsername/lyricfinder-project.git](https://github.com/YourUsername/lyricfinder-project.git)
    cd lyricfinder-project
    ```
    
2. **创建和激活虚拟环境:**
    
    ```
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate # macOS/Linux
    ```
    
3. **安装依赖:**
    
    ```
    pip install -e .
    ```
    
4. **运行帮助:**
    
    ```
    lyricfinder --help
    # 查看 song 命令的详细选项
    lyricfinder song --help 
    ```

  

#### 💡 使用示例

  

  

##### 1. 抓取歌词、保存 .txt 并下载专辑封面

  
  

```bash

  

(venv)> lyricfinder song "Green Day" "American Idiot" --save --art

  

正在搜索 'Green Day - American Idiot' ...

--- American Idiot by Green Day ---

  

[Verse 1]

Don't wanna be an American idiot

Don't want a nation under the new media

...

(歌词内容)

...

  

[成功] 歌词已保存到: lyric\Green Day - American Idiot.txt

```

##### 2. 获取“聚合”的歌曲/艺术家信息

  
  

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

  

##### 3. 自动识别本地 FLAC/MP3 文件

  

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

### 选项 B: Windows Executable (.exe) 文件使用 (推荐普通用户使用)

如果你是 Windows 用户，可以直接下载已打包的 `lyricfinder.exe` 文件，无需安装 Python 环境。

1. **下载文件:**
    
    - 从 [GitHub Releases 页面](https://www.google.com/search?q=https://github.com/YourUsername/lyricfinder-project/releases "null") 下载最新的 `lyricfinder.exe` 文件。
        
2. **使用方法 (命令行):**
    
    - **方法一 (简单但麻烦):** 导航到 `.exe` 所在的文件夹，然后在命令行运行它，例如：
        
        ```
        D:\Downloads> lyricfinder.exe song "Lady Gaga" "Bad Romance"
        ```
        
    - **方法二 (推荐: 设置PATH环境变量):** 将 `lyricfinder.exe` 所在的文件夹路径添加到你的系统环境变量 `PATH` 中。添加后，你就可以在**任何地方**直接运行命令：
        
        ```
        # 在任何文件夹下运行
        lyricfinder.exe info "Queen" "Bohemian Rhapsody"
        ```
        

#### 💻 命令示例

**提示:** 使用 `lyricfinder.exe <COMMAND> --help` 查看每个命令的详细选项（例如 `lyricfinder.exe song --help`）。

##### 1. 抓取歌词并下载封面 (`song`)

```
# 获取歌词，并下载封面到 artworks/ 文件夹
lyricfinder.exe song "Taylor Swift" "Cruel Summer" --art

# 获取歌词，并保存到 lyric/Mr. Brightside.txt 文件
lyricfinder.exe song "The Killers" "Mr. Brightside" --save

# 获取歌词，同时保存和下载封面
lyricfinder.exe song "Kendrick Lamar" "DNA." --save --art
```

##### 2. 聚合歌曲和艺术家信息 (`info`)

```
# 同时获取歌曲简介和艺术家简介
lyricfinder.exe info "Coldplay" "Fix You"
```

##### 3. 读取本地文件 (`local`)

```
# 读取本地 mp3 或 flac 文件的元数据，然后搜索歌词
lyricfinder.exe local "C:\Music\My Favorite Track.mp3"
```
