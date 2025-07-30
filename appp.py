import streamlit as st
import yt_dlp
import os
import zipfile
from pathlib import Path

DOWNLOAD_DIR = "downloads"

st.set_page_config(page_title="jefri download yt", layout="centered")
st.title("📥 jefri download yt")

# == Fungsi ==
def list_playlist_entries(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            return info['entries']
        else:
            return [info]

def estimate_file_size(info, max_quality):
    for f in info.get("formats", []):
        if f.get("height") and f["height"] <= max_quality and f.get("filesize"):
            return round(f["filesize"] / (1024 * 1024), 2)
    return None

def download_video(url, quality="1080p"):
    max_res = int(quality.replace("p", "")) if "p" in quality else 1080
    ydl_opts = {
        "format": f"bestvideo[height<={max_res}]+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title).80s.%(ext)s",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title).80s.%(ext)s",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def zip_all_downloads():
    zip_path = Path("downloads.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(DOWNLOAD_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, DOWNLOAD_DIR)
                zf.write(full_path, arcname)
    return zip_path

# == UI ==
url = st.text_input("🔗 Masukkan URL video atau playlist")
quality = st.selectbox("🎞️ Pilih Kualitas", ["1080p", "4K", "720p (hemat)", "MP3"])
download_all = st.checkbox("📋 Download semua video (jika playlist)?", value=True)

if st.button("🚀 Mulai Download") and url:
    Path(DOWNLOAD_DIR).mkdir(exist_ok=True)
    with st.spinner("🔄 Mengambil data..."):
        try:
            entries = list_playlist_entries(url)
            st.success(f"Ditemukan {len(entries)} video")
            for entry in entries:
                video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                title = entry.get("title", "Tanpa Judul")
                info = entry
                size = estimate_file_size(info, max_quality=2160 if quality == "4K" else 1080)
                st.write(f"📽️ **{title}** — {size or '??'} MB")

                try:
                    if quality == "MP3":
                        download_audio(video_url)
                    else:
                        res_limit = 2160 if quality == "4K" else int(quality.replace("p", ""))
                        download_video(video_url, f"{res_limit}p")
                    st.success(f"✅ Berhasil download: {title}")
                except Exception as e:
                    st.warning(f"⚠️ Gagal download {title}: {e}")

            zip_path = zip_all_downloads()
            with open(zip_path, "rb") as f:
                st.download_button("📦 Unduh Semua (ZIP)", f, file_name="downloads.zip")

        except Exception as e:
            st.error(f"❌ Gagal: {e}")
