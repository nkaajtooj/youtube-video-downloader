#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def read_urls(path: Path) -> list[str]:
    urls: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    if not urls:
        raise ValueError(f"No URL(s) found in file: {path}")
    return urls


def run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Download a YouTube URL to MP4 using yt-dlp (requires ffmpeg)."
    )
    parser.add_argument(
        "url_or_file",
        help="YouTube video URL OR path to a text file containing URL(s) (one per line)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="downloads",
        help="Directory to write files into (default: downloads/)",
    )
    parser.add_argument(
        "--filename-template",
        default="%(title).200B [%(id)s].%(ext)s",
        help="yt-dlp output template (default: title + id)",
    )
    parser.add_argument(
        "--subtitles",
        action="store_true",
        help="Also download subtitles (best-effort; failures won't fail the video download)",
    )
    parser.add_argument(
        "--cookies-from-browser",
        default=None,
        help="Pass through to yt-dlp --cookies-from-browser (e.g. chrome, firefox, safari)",
    )
    args = parser.parse_args(argv)

    urls: list[str]
    candidate = Path(args.url_or_file).expanduser()
    if candidate.exists() and candidate.is_file():
        try:
            urls = read_urls(candidate)
        except Exception as e:
            print(f"Error: failed to read URL from file '{candidate}': {e}", file=sys.stderr)
            return 2
    else:
        urls = [args.url_or_file]

    ytdlp_cmd: list[str]
    if shutil.which("yt-dlp") is not None:
        ytdlp_cmd = ["yt-dlp"]
    else:
        # If installed via pip but scripts dir isn't on PATH, this still works.
        ytdlp_cmd = [sys.executable, "-m", "yt_dlp"]

    if shutil.which("ffmpeg") is None:
        print("Error: ffmpeg not found. Install ffmpeg first (e.g. `brew install ffmpeg`).", file=sys.stderr)
        return 2

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    def build_cmd(url: str, extra: list[str]) -> list[str]:
        # Prefer MP4 container. If best streams are not MP4, remux to MP4.
        # This does not re-encode unless required by source/container constraints.
        cmd: list[str] = [
            *ytdlp_cmd,
            url,
            "--no-playlist",
            "--format",
            "bv*+ba/b",
            "--merge-output-format",
            "mp4",
            "--output",
            str(out_dir / args.filename_template),
            "--restrict-filenames" if False else "--no-restrict-filenames",
        ]

        if args.cookies_from_browser:
            cmd += ["--cookies-from-browser", args.cookies_from_browser]

        cmd += extra
        return cmd

    def build_subs_cmd(url: str, extra: list[str]) -> list[str]:
        cmd = build_cmd(url, extra)
        # Don't redownload media; just fetch subs alongside the already-downloaded file.
        cmd += [
            "--skip-download",
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs",
            "en.*,-live_chat",
        ]
        return cmd

    try:
        any_failed = False
        module_hint_printed = False
        for url in urls:
            # First attempt: default behavior
            completed = subprocess.run(build_cmd(url, []), check=False)
            # Common hardening for 403s: try a different YouTube player client.
            if completed.returncode != 0:
                completed = subprocess.run(
                    build_cmd(url, ["--extractor-args", "youtube:player_client=android"]),
                    check=False,
                )

            if completed.returncode != 0:
                if (
                    not module_hint_printed
                    and completed.returncode == 1
                    and ytdlp_cmd[:2] == [sys.executable, "-m"]
                ):
                    print(
                        "yt-dlp failed to run via Python module. If it's not installed, run:\n"
                        f"  {sys.executable} -m pip install -r requirements.txt",
                        file=sys.stderr,
                    )
                    module_hint_printed = True
                any_failed = True
                continue

            if args.subtitles:
                subs_completed = subprocess.run(build_subs_cmd(url, []), check=False)
                if subs_completed.returncode != 0:
                    # Common hardening for 403/429 when fetching subs: try alternate client.
                    subs_completed = subprocess.run(
                        build_subs_cmd(url, ["--extractor-args", "youtube:player_client=android"]),
                        check=False,
                    )
                if subs_completed.returncode != 0:
                    print(
                        "Warning: subtitle download failed (often due to rate-limits like HTTP 429). "
                        "The video download still succeeded.",
                        file=sys.stderr,
                    )

        if any_failed:
            return 1
        return 0
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))

