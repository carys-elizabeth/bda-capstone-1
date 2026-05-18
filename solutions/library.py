from pathlib import Path
import yt_dlp
import csv
import time
from multiprocessing import Pool


def download_video(url):
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "socket_timeout": 30,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])
        return {
            "url" : url,
            "status": "success",
            "error" : "",
        }
    except Exception as error:
        return {
            "url": url,
            "status": "failed",
            "error": str(error),
        }

def append_to_report(report_path, text):
    with open(report_path, "a", encoding="utf-8") as report:
        report.write(text)


def read_video_urls(csv_path, report_path=None):
    if report_path is None:
        report_path = Path(__file__).resolve().parents[1] / "reports" / "sequential_report.md"

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        results = []
        start = time.perf_counter()
        for row in reader:
            result = download_video(row['url'])
            results.append(result)
        
        successful_downloads = 0
        failed_downloads = 0
        for result in results:
            if result["status"] == "failed":
                print("Failed:", result["url"])
                print("Error:", result["error"])
                append_to_report("reports/sequential_report.md", f"Failed: {result['url']}\nError: {result['error']}\n")
                failed_downloads += 1
            else: 
                successful_downloads += 1
        append_to_report("reports/sequential_report.md", f"Successful downloads: {successful_downloads}\n")
        append_to_report("reports/sequential_report.md", f"Failed downloads: {failed_downloads}\n")

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

    resultslist = []

    start = time.perf_counter()
    with Pool() as pool:
        results = pool.map(download_video, urls)
        resultslist.extend(results)

    end = time.perf_counter()
    elapsed = end - start

    successful_downloads = 0
    failed_downloads = 0 
    for result in resultslist:
        if result["status"] == "failed":
            print("Failed:", result["url"])
            print("Error:", result["error"])
            append_to_report("reports/sequential_report.md", f"Failed downloads: {result['url']}\nError: {result['error']}\n")
            failed_downloads += 1
        else:
            successful_downloads += 1
    append_to_report("reports/sequential_report.md", f"Successful downloads: {successful_downloads}\n")
    append_to_report("reports/sequential_report.md", f"Failed downloads: {failed_downloads}\n")


    parallel_time = round(elapsed, 2)
    print(f"Parallel execution: {parallel_time} seconds")
    append_to_report("reports/sequential_report.md", f"Parallel execution: {parallel_time} seconds\n")

def video_metadata_extract(csv_path):
    urls = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['url'])

    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "socket_timeout": 30,
        "quiet": True,
        "skip_download": True,
    }

    metadata_rows = []
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        for url in urls:
            info = ydl.extract_info(url, download=False)
            
            metadata ={
                    "title": info.get("title"),
                    "duration": info.get("duration"),
                    "uploader": info.get("uploader"),
                    "view_count": info.get("view_count"),
                    "ext": info.get("ext"),
                    "url": url
                }

            metadata_rows.append(metadata)
    
    with open("data/video_metadata.csv", "w", newline="") as file:
        fieldnames = ['title', 'duration', 'uploader', 'view_count', 'ext', 'url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(metadata_rows)

