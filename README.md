# YouTube → MP4 downloader (yt-dlp)

Downloads a YouTube video URL and produces an **MP4** (best video+audio, remuxed to mp4 when needed).

Use this only for videos you have the rights/permission to download and in compliance with YouTube’s Terms.

## Requirements

- Python 3
- `ffmpeg`
- `yt-dlp` (installed via `requirements.txt`)

## Setup

```bash
cd /Users/iaa/Work/youtube
python3 -m pip install -r requirements.txt
brew install ffmpeg
```

## Download

```bash
python3 ytdl_mp4.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Or read URLs from a text file (one per line), e.g. a file named `url`:

```bash
python3 ytdl_mp4.py url
```

Empty lines and lines starting with `#` are ignored. It will sequentially download all valid URLs in the file.

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

