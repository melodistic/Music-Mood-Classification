import pandas as pd
from yt_dlp import YoutubeDL
import os

def download_video(video_id, path,title):
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': False,
        'keepvideo': False,
        'outtmpl': os.path.join(path,str(title)+'.%(ext)s')
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + video_id])
def main():
    os.makedirs('song', exist_ok=True)
    os.makedirs('song/Anxious', exist_ok=True)
    os.makedirs('song/Chill', exist_ok=True)
    os.makedirs('song/Focus', exist_ok=True)
    os.makedirs('song/Party', exist_ok=True)
    os.makedirs('song/Romance', exist_ok=True)
    os.makedirs('song/Sad', exist_ok=True)
    df = pd.read_csv("song_list.csv")
    for _, row in df.iterrows():
        download_video(row['id'], './song/'+row['mood'],row['title'])
    

if __name__ == "__main__":
    main()