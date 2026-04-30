# YouTube → MP4 downloader (yt-dlp)

Downloads a YouTube video URL and produces an **MP4** (best video+audio, remuxed to mp4 when needed).

Use this only for videos you have the rights/permission to download and in compliance with YouTube’s Terms.

## Requirements

- Python 3
- `ffmpeg`
- `yt-dlp` (installed via `requirements.txt`)

## Setup

1. **Install FFmpeg:**
   - **macOS:** `brew install ffmpeg`
   - **Windows:** `winget install ffmpeg` (or download from [ffmpeg.org](https://ffmpeg.org/download.html))
   - **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg`

2. **Install Python dependencies:**
   ```bash
   cd /path/to/youtube
   python3 -m pip install -r requirements.txt
   ```

## Download

```bash
python3 ytdl_mp4.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Batch Download via Text File

You can download multiple videos by providing a text file containing the URLs.

1. **Create a file** named `url` (or any other name):
   ```bash
   touch url
   ```

2. **Add your links** to the file, one per line:
   ```text
   # Add your URLs below
   https://www.youtube.com/watch?v=VIDEO_ID_1
   https://www.youtube.com/watch?v=VIDEO_ID_2
   ```

3. **Run the script** and pass the file name as the argument:
   ```bash
   python3 ytdl_mp4.py url
   ```

*Note: Empty lines and lines starting with `#` are ignored. The script will sequentially download all valid URLs found in the file.*

Files go to `downloads/` by default.

### Options

- Choose output directory:

```bash
python3 ytdl_mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" -o /tmp/ytdl
```

- Custom filename template (using `yt-dlp` output template syntax):

```bash
python3 ytdl_mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" --filename-template "%(title).200B [%(id)s].%(ext)s"
```

- Also try to download subtitles (best-effort; rate limits like HTTP 429 won’t fail the video):

```bash
python3 ytdl_mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" --subtitles
```

- If you get `HTTP Error 403: Forbidden`, try using browser cookies (often required for age/login/rate-limited videos):

```bash
python3 ytdl_mp4.py "https://www.youtube.com/watch?v=VIDEO_ID" --cookies-from-browser safari
```

