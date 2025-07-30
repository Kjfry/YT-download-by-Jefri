import streamlit as st
import yt_dlp
import os
from pathlib import Path

# ===== FUNGSI: Ambil Info Video Tanpa Download =====
def get_video_info(url):
    ydl_opts = {"quiet": True, "skip_download": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Tanpa Judul"),
                "uploader": info.get("uploader", "Tidak diketahui"),
                "duration": info.get("duration", 0),
                "thumbnail": info.get("thumbnail", ""),
                "url": url
            }
    except Exception as e:
        st.error(f"❌ Tidak bisa ambil info video: {e}")
        return None

# ===== FUNGSI-FUNGSI DOWNLOAD =====
def download_video(url, mode="1080p", output_path="downloads"):
    Path(output_path).mkdir(exist_ok=True)
    
    if mode == "1080p":
        ydl_opts = {
            'format': 'best[height<=1080]',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'noplaylist': True,
        }
    elif mode == "best":
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'noplaylist': True,
        }
    elif mode == "audio":
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
    else:
        st.error("Mode tidak dikenali.")
        return
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            st.success(f"✓ Selesai! File disimpan di folder `{output_path}`")
    except Exception as e:
        st.error(f"❌ Gagal mengunduh: {e}")

# ===== UI STREAMLIT =====
st.set_page_config(page_title="YouTube Downloader", page_icon="📥")
st.title("📥 YouTube Downloader by @BangkitKubur")

video_url = st.text_input("🔗 Masukkan URL YouTube di sini")

if video_url:
    info = get_video_info(video_url)
    if info:
        st.markdown("### 📺 Preview Video")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info["thumbnail"], use_column_width=True)
        with col2:
            dur_m, dur_s = divmod(info["duration"], 60)
            st.markdown(f"**Judul:** {info['title']}")
            st.markdown(f"**Channel:** {info['uploader']}")
            st.markdown(f"**Durasi:** {dur_m} menit {dur_s} detik")
        
        st.markdown("---")
        st.markdown("### ⬇️ Pilih Format Download")

        col_v1, col_v2, col_a = st.columns(3)
        if col_v1.button("🎥 Video 1080p"):
            download_video(video_url, mode="1080p")
        if col_v2.button("💎 Best Quality (4K+)"):
            download_video(video_url, mode="best")
        if col_a.button("🎧 Audio MP3"):
            download_video(video_url, mode="audio")
