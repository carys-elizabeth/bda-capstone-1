from pathlib import Path
import yt_dlp
import library
import csv


if __name__ == "__main__":
    #url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    #library.download_video(url)

    csv_path = Path("data/video_urls.csv")
    library.read_video_urls(csv_path)
    
    library.parallel_download_video(csv_path)

    library.video_metadata_extract(csv_path)