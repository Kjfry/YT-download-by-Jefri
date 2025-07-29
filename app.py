import yt_dlp
import os
from pathlib import Path

def download_youtube_video(url, output_path="downloads"):
    """
    Download video YouTube dengan resolusi penuh
    
    Args:
        url (str): URL video YouTube
        output_path (str): Folder untuk menyimpan video
    """
    
    # Buat folder download jika belum ada
    Path(output_path).mkdir(exist_ok=True)
    
    # Konfigurasi yt-dlp
    ydl_opts = {
        'format': 'best[height<=1080]',  # Ambil kualitas terbaik hingga 1080p
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Template nama file
        'noplaylist': True,  # Hanya download satu video, bukan playlist
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ambil info video terlebih dahulu
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown')
            
            print(f"Judul: {title}")
            print(f"Channel: {uploader}")
            print(f"Durasi: {duration//60}:{duration%60:02d}")
            print("Memulai download...")
            
            # Download video
            ydl.download([url])
            print(f"✓ Download selesai! Video disimpan di folder '{output_path}'")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def download_best_quality(url, output_path="downloads"):
    """
    Download dengan kualitas terbaik yang tersedia (termasuk 4K jika ada)
    """
    
    Path(output_path).mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'best',  # Ambil kualitas terbaik tanpa batasan
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            
            # Tampilkan format yang tersedia
            formats = info.get('formats', [])
            print(f"Judul: {title}")
            print("Format tersedia:")
            for f in formats[-5:]:  # Tampilkan 5 format terakhir (biasanya kualitas terbaik)
                height = f.get('height', 'Audio')
                ext = f.get('ext', '')
                filesize = f.get('filesize', 0)
                size_mb = filesize / (1024*1024) if filesize else 'Unknown'
                print(f"  - {height}p {ext} ({size_mb:.1f} MB)" if isinstance(size_mb, float) else f"  - {height}p {ext}")
            
            print("\nMemulai download dengan kualitas terbaik...")
            ydl.download([url])
            print(f"✓ Download selesai!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def download_audio_only(url, output_path="downloads"):
    """
    Download audio saja (MP3)
    """
    
    Path(output_path).mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Mengunduh audio...")
            ydl.download([url])
            print("✓ Audio berhasil diunduh!")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Contoh penggunaan
if __name__ == "__main__":
    # Ganti dengan URL video yang ingin didownload
    video_url = input("Masukkan URL YouTube: ").strip()
    
    if not video_url:
        print("URL tidak boleh kosong!")
        exit()
    
    print("\nPilih opsi download:")
    print("1. Video 1080p (recommended)")
    print("2. Video kualitas terbaik (4K jika tersedia)")
    print("3. Audio saja (MP3)")
    
    choice = input("Pilih (1-3): ").strip()
    
    if choice == "1":
        download_youtube_video(video_url)
    elif choice == "2":
        download_best_quality(video_url)
    elif choice == "3":
        download_audio_only(video_url)
    else:
        print("Pilihan tidak valid!")