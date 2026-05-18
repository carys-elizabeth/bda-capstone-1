from pathlib import Path
import yt_dlp
import csv
import time
from multiprocessing import Pool


def download_video(url):
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s"
    }
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download([url])


def append_to_report(report_path, text):
    with open(report_path, "a", encoding="utf-8") as report:
        report.write(text)


def read_video_urls(csv_path):
    if report_path is None:
        report_path = Path(__file__).resolve().parents[1] / "reports" / "sequential_report.md"

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        start = time.perf_counter()
        for row in reader:
            download_video(row['url'])

        end = time.perf_counter()
        elapsed = end - start
        serial_time = round(elapsed, 2)
        print(f"Serial execution: {serial_time} seconds")
        append_to_report("reports/sequential_report.md", f"Serial execution: {serial_time} seconds\n")

def parallel_download_video(csv_path):

    urls = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['url'])

    start = time.perf_counter()
    with Pool() as pool:
        results = pool.map(download_video, urls)
    end = time.perf_counter()
    elapsed = end - start
        
    parallel_time = round(elapsed, 2)
    print(f"Parallel execution: {parallel_time} seconds")
    append_to_report("reports/sequential_report.md", f"Parallel execution: {parallel_time} seconds\n")
