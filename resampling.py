import os, json, subprocess
from pathlib import Path

debug = False
ffmpeg_command = 'ffmpeg'
ffmpeg_option = ''
src_filetype = '.flac'
out_filetype = '.flac'

def config():
    global debug, ffmpeg_command, ffmpeg_option, src_filetype, out_filetype

    config_file = open('config.json','r')
    config_data = json.load(config_file)

    debug = config_data['exec_options']['debug_option']
    ffmpeg_command = config_data['exec_options']['ffmpeg_path']
    out_bit_depth = config_data['output_options']['bit_depth']
    out_sampling = config_data['output_options']['sampling']
    out_resampler = 'aresample=resampler=' + config_data['output_options']['resampler']
    comp_level = config_data['output_options']['comp_level']
    out_filetype = config_data['output_options']['out_type']
    ffmpeg_comp_option = ' '.join(['-compression_level', comp_level])
    ffmpeg_resample_option = ' '.join(['-sample_fmt', out_bit_depth, '-af', out_resampler, '-ar', out_sampling])
    ffmpeg_option = ' '.join(['-c:v copy', ffmpeg_comp_option, ffmpeg_resample_option])
    src_filetype = config_data['source_type']['src_type']
    return

def resample():
    target_file = '**/*' + src_filetype
    filelist = Path(os.getcwd()).glob(target_file)
    for file in filelist:
        try:
            in_filename = '\"' + file.name + '\"'
            out_filename = '\"' + 'out' + os.sep + file.name.rsplit('.', 1)[0] + out_filetype + '\"'
            shell_command = ' '.join([ffmpeg_command, '-i', in_filename, ffmpeg_option, out_filename])
            debug_print(shell_command)
            subprocess.run(shell_command, shell=True)
            continue
        except:
            print('Error')
    return

def debug_print(param):
    if debug:
        print(param)
    return

def main():
    config()
    resample()

if __name__ == "__main__":
    main()
