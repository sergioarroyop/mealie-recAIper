import yt_dlp
import os

from lib.logger import logger as base_logger
from config.settings import YLTP_CONFIG

logger = base_logger.getChild(__name__)

def download_audio_from_url(url: str) -> dict | None:
    ydl_opts = {
        "format": YLTP_CONFIG.get("format"),
        "outtmpl": f"{YLTP_CONFIG['download_dir']}/%(title)s.%(ext)s",
        "quiet": YLTP_CONFIG.get("quiet"),
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        logger.info(f"💾 Downloading audio")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            audio_path = os.path.splitext(filename)[0] + ".mp3"
            
            metadata = {
                "title": info.get("title"),
                "description": info.get("description", ""),
                "thumbnail": info.get("thumbnail"),
                "audio_path": audio_path,
                "url": url
            }

            logger.info(f"✅ Audio downloaded: {metadata['title']}")
            return metadata
    except Exception as e:
        logger.error(f"❌ Error downloading the audio:\n{e}")
        raise