import click
from pathlib import Path
from lyricfinder import scraper 
from lyricfinder import local_tools

@click.group()
def cli():
    pass

@cli.command()
@click.argument('artist')
@click.argument('song')
@click.option('--save', is_flag=True, help='将歌词保存到 "lyric/" 文件夹')
@click.option('--art', is_flag=True, help='下载专辑封面到 "artworks/" 文件夹')
def song(artist, song, save, art):

    click.echo(f"正在搜索 '{artist} - {song}' ...")
    
    # 1. 调用 Genius.com (获取歌词)
    data = scraper.fetch_song_data(artist, song)
    
    if data["status"] == "fail":
        click.echo(data["message"])
        return

    lyrics_to_print = f"--- {song} by {artist} ---\n\n{data['lyrics']}"
    click.echo(lyrics_to_print)
    
    # 2. 处理 --save
    if save:
        lyrics_dir = Path("lyric")
        lyrics_dir.mkdir(parents=True, exist_ok=True)
        filename_txt = lyrics_dir / f"{artist} - {song}.txt"
        
        try:
            with open(filename_txt, 'w', encoding='utf-8') as f:
                f.write(data["lyrics"])
            click.echo(f"\n[成功] 歌词已保存到: {filename_txt}")
        except IOError as e:
            click.echo(f"\n[错误] 无法保存 .txt 文件: {e}")

    # 3. 处理 --art
    if art:
        click.echo(f"\n正在 TheAudioDB.com 上搜索专辑封面...")
        
        # (引擎 3) 调用 TheAudioDB API
        art_data = scraper.fetch_album_art_url(artist, song)
        
        if art_data["status"] == "success":
            art_url = art_data.get("url")
            click.echo(f"正在下载专辑封面: {art_url} ...")
            
            art_dir = Path("artworks")
            art_dir.mkdir(parents=True, exist_ok=True)
            filename_jpg = art_dir / f"{artist} - {song}.jpg"
            
            download_status = scraper.download_image(art_url, filename_jpg)
            
            if download_status["status"] == "success":
                click.echo(f"[成功] 专辑封面已保存到: {download_status['path']}")
            else:
                click.echo(f"[错误] 无法下载封面: {download_status['message']}")
        else:
            click.echo(f"\n[错误] 无法找到封面: {art_data['message']}")

@cli.command()
@click.argument('artist')
@click.argument('song')
def info(artist, song):

    click.echo(f"--- 正在聚合 '{artist} - {song}' 的信息 ---")
    
    # 1. 调用引擎 1 (Genius)
    click.echo("正在抓取 Genius.com (获取歌曲简介)...")
    genius_data = scraper.fetch_song_data(artist, song)
    
    # 2. 调用引擎 2 (Wikipedia)
    click.echo("正在抓取 Wikipedia (获取艺术家简介)...")
    wiki_data = scraper.fetch_artist_bio(artist)
    
    click.echo("--- 聚合报告 ---")
    
    # 3. 打印 Genius 报告
    click.echo("\n--- 歌曲简介 (来自 Genius.com) ---")
    if genius_data["status"] == "success":
        info_text = genius_data['info']
        final_info_lines = []
        for line in info_text.split('\n'):
            line = line.strip()
            if line and line.lower() != "read more":
                final_info_lines.append(line)
        
        click.echo("\n".join(final_info_lines))
    else:
        click.echo(f"(抓取失败: {genius_data['message']})")

    # 4. 打印 Wikipedia 报告
    click.echo("\n--- 艺术家简介 (来自 Wikipedia) ---")
    if wiki_data["status"] == "success":
        click.echo(wiki_data['bio'])
        click.echo(f"\n(来源: {wiki_data['url']})")
    else:
        click.echo(f"(抓取失败: {wiki_data['message']})")

@cli.command()
@click.argument('filepath', type=click.Path(exists=True, dir_okay=False))
def local(filepath):

    click.echo(f"正在读取文件: {filepath} ...")
    file_path = Path(filepath) 
    
    # 1. (调用模块 2) 读取元数据
    metadata = local_tools.get_metadata(file_path)
    
    if metadata["status"] == "fail":
        click.echo(metadata["message"])
        return
        
    artist = metadata["artist"]
    song = metadata["song"]
    
    click.echo(f"成功识别! 艺术家: {artist}, 歌曲: {song}")
    click.echo(f"正在搜索 '{artist} - {song}' 的歌词...")

    # 2. (调用模块 1) 复用爬虫引擎
    data = scraper.fetch_song_data(artist, song)
    
    if data["status"] == "fail":
        click.echo(data["message"])
        return
        
    # 3. 打印最终结果
    lyrics_to_print = f"--- {song} by {artist} ---\n\n{data['lyrics']}"
    click.echo(lyrics_to_print)

if __name__ == '__main__':
    cli()