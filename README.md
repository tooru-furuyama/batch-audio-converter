# Batch Audio Converter
- Convert multiple music files in the same directory using FFmpeg.

## Use case scenarios
- Multiple audio files are stored in a folder (e.g. album)
- Convert multiple audio files
  - Convert multiple wave files (e.g. ripped album from Audio CD) to FLAC, MP3 or AAC audio files
  - Convert High Resolution audio files (e.g. 24-bit / 192 kHz) to lower resolution audio files (e.g. 24-bit / 48 kHz)

## Pre-requisite
- Python 3 is installed on the host
- FFmpeg is installed somewhere on the host (FFmpeg path should be configured within the config.json file)
- Parameters are configured within config.json file

## Usage
> python .\audio-converter.py

specify pre-configured JSON file
> python .\audio-converter.py -p preset_mp3.json

specify input file type (overwrite profile setting)
> python .\audio-converter.py -i wav

specify output file type (overwrite profile setting)
> python .\audio-converter.py -o mp3

## Update History
### 2022-02-27
- Added Multiprocessing support
- Additional command line option - Added support to specify input/output filetypes through command line
- Code improvements

### 2022-02-20
- Added MP3 and AAC support
- Additional command line option - Added support for non-default config file through command line
- Code improvements

### 2022-02-15
- Initial Commit
