import os
import re
import shutil

import youtube_dl
from imutils import paths

def download(playlist_url, download_dir='downloaded'):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded\\%(title)s.%(ext)s',
        'ignoreerrors': True,
        'playliststart': 88,
        'playlistend': 214,
        # 'playlist_items' [],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',}],
    }

    youtube_dl.YoutubeDL(options).download([playlist_url])


def rename_and_move(download_dir, music_dir):
    for file_path in paths.list_files(download_dir, validExts=('.mp3')):
        print('>>> Old file:', file_path)
        dir_name, base_name = file_path.rsplit(os.sep, 1)
        file_name, ext = os.path.splitext(base_name)

        file_name = re.sub(r'\(.*(audio|lyric|official|video|mv|m_v).*\)', '', file_name, flags=re.IGNORECASE)
        file_name = re.sub(r'\[.*(audio|lyric|official|video|mv|m_v).*\]', '', file_name, flags=re.IGNORECASE)

        if '-' in file_name:
            artist_name, song_name = [name.strip() for name in file_name.split('-', 1)]
            new_file_name = ' - '.join([song_name, artist_name])
        else:
            new_file_name = file_name

        new_dir_name = dir_name.replace(download_dir, music_dir)
        new_file_path = os.path.join(new_dir_name, new_file_name + ext)

        if not os.path.exists(new_file_path):
            os.rename(file_path, new_file_path)
            print('>>> New file:', new_file_path)
        else:
            print('>>> File existed:', new_file_path)

# playlist_url = 'https://www.youtube.com/playlist?list=PLzp-YFqxu55FuIbr2VZR98ev_-9-BbZ1M'
download_dir = 'downloaded'
music_dir = 'music'

# download(playlist_url)

rename_and_move(download_dir, music_dir)
