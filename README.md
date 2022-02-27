# Batch Audio Converter
- Convert multiple music files in the same directory using FFmpeg.

## Use case scenarios
- Convert multiple wave files (e.g. ripped album from Audio CD) to FLAC, MP3 or AAC audio files
- Convert High Resolution (e.g. 24-bit / 192 kHz) audio files to lower resolution audio files (e.g. 24-bit / 96 kHz)

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
- Code improvements - Applied "private" attribute for internal variables
- Command line improvements - Added support to specify input/output filetypes through command line

### 2022-02-20
- Code improvements - Applied Class
- Added MP3 and AAC support
- Command line improvements - Added support for non-default config file through command line

### 2022-02-15
- Initial Commit
