"""Batch convert all .wav files under assets/audio/ to .mp3 using ffmpeg."""

import subprocess
import sys
from pathlib import Path

AUDIO_DIR = Path(__file__).parent / "assets" / "audio"
BITRATE = "192k"


def main():
    wav_files = sorted(AUDIO_DIR.rglob("*.wav"))
    if not wav_files:
        print("No .wav files found.")
        return

    total = len(wav_files)
    failed = []

    for i, wav in enumerate(wav_files, 1):
        mp3 = wav.with_suffix(".mp3")
        rel = wav.relative_to(AUDIO_DIR)
        print(f"[{i}/{total}] {rel} → {mp3.name}")

        result = subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav), "-b:a", BITRATE, str(mp3)],
            capture_output=True,
        )

        if result.returncode != 0:
            print(f"  ERROR: {result.stderr.decode().strip()}")
            failed.append(wav)
        else:
            wav.unlink()

    print(f"\nDone. {total - len(failed)}/{total} converted.")
    if failed:
        print("Failed:")
        for f in failed:
            print(f"  {f}")
        sys.exit(1)


if __name__ == "__main__":
    main()
