import yt_dlp
import os
from pathlib import Path
import zipfile

def list_playlist_videos(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            return info['entries']  # daftar video dari playlist
        else:
            return [info]  # single video

def estimate_file_size(url, format_limit="best[height<=1080]"):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        for f in formats[::-1]:
            if f.get('format_id') and f.get('height', 0) <= 1080:
                size = f.get('filesize') or f.get('filesize_approx') or 0
                if size:
                    return size / (1024 * 1024)  # dalam MB
        return None

def download_video(url, output_path="downloads", max_quality=1080):
    Path(output_path).mkdir(exist_ok=True)
    ydl_opts = {
        'format': f'bestvideo[height<={max_quality}]+bestaudio/best',
        'outtmpl': f'{output_path}/%(title).80s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, output_path="downloads"):
    Path(output_path).mkdir(exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title).80s.%(ext)s',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def zip_downloads(folder="downloads", zip_name="downloads.zip"):
    zip_path = Path(zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                arcname = os.path.relpath(path, folder)
                zipf.write(path, arcname)
    return zip_path

# === MAIN PROGRAM ===
if __name__ == "__main__":
    print("🎞️ YouTube Downloader - Versi Lengkap")

    video_url = input("🔗 Masukkan URL video atau playlist: ").strip()
    if not video_url:
        print("❌ URL tidak boleh kosong!")
        exit()

    items = list_playlist_videos(video_url)
    is_playlist = len(items) > 1

    if is_playlist:
        print(f"\n📃 Playlist terdeteksi: {len(items)} video ditemukan.")
        print("Tampilkan daftar:")
        for i, item in enumerate(items):
            title = item.get("title", "Tanpa Judul")
            print(f"{i+1}. {title}")
        choice = input("\n📥 Download semua? (y/n): ").strip().lower()
        if choice != 'y':
            selected = input("Ketik nomor video yang ingin didownload (pisahkan dengan koma): ")
            indexes = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
            items = [items[i] for i in indexes]

    print("\nPilih kualitas:")
    print("1. Video 1080p (default)")
    print("2. Video kualitas terbaik (4K jika ada)")
    print("3. Audio MP3")
    print("4. Video resolusi maksimal 720p (hemat kuota)")

    mode = input("Pilih (1-4): ").strip()

    for item in items:
        url = f"https://www.youtube.com/watch?v={item['id']}"
        title = item.get('title', 'Unknown')
        size = estimate_file_size(url)
        if size:
            print(f"\n🎬 {title} (estimasi {size:.2f} MB)")
        else:
            print(f"\n🎬 {title} (ukuran tidak diketahui)")

        try:
            if mode == "1":
                download_video(url, max_quality=1080)
            elif mode == "2":
                download_video(url, max_quality=4320)
            elif mode == "3":
                download_audio(url)
            elif mode == "4":
                download_video(url, max_quality=720)
            else:
                print("❌ Pilihan tidak valid.")
        except Exception as e:
            print(f"❌ Gagal download: {e}")

    zip_file = zip_downloads()
    print(f"\n📦 Semua file telah dijadikan ZIP: {zip_file}")
