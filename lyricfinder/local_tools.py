# lyricfinder/local_tools.py
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen import MutagenError

def get_metadata(filepath: Path) -> dict:

    artist = None
    song = None
    
    try:
        file_ext = filepath.suffix.lower()

        if file_ext == '.mp3':
            try:
                audio = EasyID3(filepath)
                artist = audio.get('artist', [None])[0]
                song = audio.get('title', [None])[0]
            except (ImportError, Exception):
                audio = MP3(filepath)
                artist = audio.get('TPE1', [None])[0]
                song = audio.get('TIT2', [None])[0]
        
        elif file_ext == '.flac':
            audio = FLAC(filepath)
            artist = audio.get('artist', [None])[0]
            song = audio.get('title', [None])[0]
        
        else:
            return {"status": "fail", "message": f"不支持的文件格式: '{file_ext}'。 (目前只支持 .mp3 和 .flac)"}
            
    except MutagenError as e:
        return {"status": "fail", "message": f"无法读取音频文件元数据: {e}"}
    except Exception as e:
        return {"status": "fail", "message": f"处理文件时出错: {e}"}

    if not artist or not song:
        return {
            "status": "fail",
            "message": f"音频文件 '{filepath.name}' 中缺少 '艺术家' 或 '歌曲名' 元数据标签。"
        }
        
    return {
        "status": "success",
        "artist": str(artist),
        "song": str(song)
    }