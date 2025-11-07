import requests
from bs4 import BeautifulSoup
from pathlib import Path
import wikipedia

# 引擎一: Genius.com (用于歌词和简介)
def fetch_song_data(artist: str, song: str) -> dict:

    query = f"{artist} {song}".replace(' ', '-')
    url = f"https://genius.com/{query}-lyrics"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'genius.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(url, headers=headers) 
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        container = soup.find("div", attrs={"data-lyrics-container": "true"})
            
        if not container:
            if soup.find_all("a", string=lambda text: "sign in" in text.lower()):
                return {"status": "fail", "message": "错误: 抓取被 Genius.com 拦截。"}
            return {"status": "fail", "message": f"错误: 找不到歌曲 '{artist} - {song}' (404 或网站结构已改变)"}

        all_text = container.get_text(separator="\n").strip()
        lyrics_start_index = all_text.find('[')
        
        if lyrics_start_index == -1:
            lyrics_start_index = -1
            for i, line in enumerate(all_text.split('\n')):
                if line.strip() and line.strip()[0].isupper():
                    lyrics_start_index = all_text.find(line)
                    break
            if lyrics_start_index == -1:
                 return {"status": "fail", "message": "错误: 无法定位歌词的起始点。"}

        info_text = all_text[:lyrics_start_index].strip()
        lyrics_text = all_text[lyrics_start_index:].strip()
        
        info_delimiter = f"{song} Lyrics"
        if info_delimiter in info_text:
            real_info = info_text.split(info_delimiter, 1)[1]
        else:
            real_info = info_text
        
        final_info_lines = []
        for line in real_info.split('\n'):
            line = line.strip()
            if line and line.lower() != "read more":
                final_info_lines.append(line)
        final_info = "\n".join(final_info_lines)
        
        final_lyrics = "\n".join([line.strip() for line in lyrics_text.split('\n') if line.strip()])

        return {
            "status": "success",
            "info": final_info,
            "lyrics": final_lyrics
        }

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"status": "fail", "message": f"错误: 找不到歌曲 '{artist} - {song}' (404 Not Found)"}
        elif e.response.status_code == 403:
             return {"status": "fail", "message": "错误: Genius.com 拒绝了我们的访问 (403 Forbidden)。"}
        else:
            return {"status": "fail", "message": f"错误: HTTP 请求失败: {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": "fail", "message": f"错误: 网络请求失败: {e}"}


# 引擎二: Wikipedia (用于艺术家简介)
def fetch_artist_bio(artist_name: str) -> dict:

    try:
        try:
            wikipedia.set_lang("zh")
        except:
            wikipedia.set_lang("en")
        bio_summary = wikipedia.summary(artist_name, auto_suggest=True, sentences=3)
        page = wikipedia.page(artist_name, auto_suggest=True)
        return {"status": "success", "bio": bio_summary, "url": page.url}
    except wikipedia.exceptions.PageError:
        return {"status": "fail", "message": f"在维基百科上找不到艺术家 '{artist_name}'"}
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            bio_summary = wikipedia.summary(e.options[0], auto_suggest=False, sentences=3)
            page = wikipedia.page(e.options[0], auto_suggest=False)
            return {"status": "success", "bio": bio_summary, "url": page.url}
        except:
             return {"status": "fail", "message": f"在维基百科上对 '{artist_name}' 的搜索不明确"}
    except Exception as e:
        return {"status": "fail", "message": f"抓取维基百科时发生未知错误: {e}"}


# 引擎三: TheAudioDB (用于专辑封面) 
def fetch_album_art_url(artist: str, song: str) -> dict:

    try:
        api_url = f"https://www.theaudiodb.com/api/v1/json/2/searchtrack.php?s={artist}&t={song}"
        
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        if data and data.get('track'):
            track_data = data['track'][0]
            art_url = track_data.get('strTrackThumb') # "Thumb" = 缩略图
            
            if art_url:
                return {"status": "success", "url": art_url}
            else:
                return {"status": "fail", "message": "API 找到了歌曲，但没有提供封面 URL。"}
        else:
            return {"status": "fail", "message": "在 TheAudioDB 上找不到该歌曲。"}
            
    except requests.RequestException as e:
        return {"status": "fail", "message": f"调用 TheAudioDB API 时出错: {e}"}


# 图片下载器
def download_image(url: str, filepath: Path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return {"status": "success", "path": filepath}
    except requests.RequestException as e:
        return {"status": "fail", "message": f"下载图片失败: {e}"}