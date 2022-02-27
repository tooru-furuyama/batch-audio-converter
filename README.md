# Batch Audio Converter
Convert music files in the same directory using FFmpeg.

## Use case scenarios
- Convert multiple wave files (e.g. ripped album from Audio CD) to FLAC, MP3 or AAC audio files
- Convert High Resolution (e.g. 24-bit / 192 kHz) audio files to lower resolution audio files (e.g. 24-bit / 96 kHz)

## Pre-requisite
- Python 3 is installed on the host
- Install FFmpeg somewhere on the host
- Parameters are configured within config.json file

## Usage:
> python .\audio-converter.py

Or specify pre-configured JSON file

> python .\audio-converter.py -p preset_mp3.json
