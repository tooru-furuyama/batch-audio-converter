import os
import argparse
import json
import subprocess
from pathlib import Path

class Resampling:

    def __init__(self):
        self.__debug = False
        self.__ffmpeg_command = 'ffmpeg'
        self.__ffmpeg_options = ''
        self.__src_filetype = ''
        self.__out_filetype = ''
        self.__profile_json = 'config.json'


    def set_profile(self, profile):
        self.__profile_json = profile
        return

    def set_input_filetype(self, in_filetype):
        self.__src_filetype = in_filetype.lower()
        self.__debug_print__('Input filetype  :' + self.__src_filetype)
        return

    def set_output_filetype(self, out_filetype):
        self.__out_filetype = out_filetype.lower()
        self.__debug_print__('Output filetype :' + self.__out_filetype)
        return


    def configure(self):
        profile_path = os.path.split(__file__)[0] + os.sep + self.__profile_json
        self.__debug_print__(profile_path)

        try:
            config_file = open(profile_path, 'r')
            config_data = json.load(config_file)
            self.__debug_print__(profile_path)

            self.__debug = config_data['exec_options']['debug_option']
            self.__ffmpeg_command = config_data['exec_options']['ffmpeg_path']
            self.__debug_print__(self.__ffmpeg_command)

            self.__ffmpeg_command = config_data['exec_options']['ffmpeg_path']
            if not len(self.__src_filetype) > 0:
                self.__src_filetype = config_data['input_options']['src_type'].lower()
            if not len(self.__out_filetype) > 0:
                self.__out_filetype = config_data['output_options']['out_type'].lower()

            self.__debug_print__('Input filetype  :' + self.__src_filetype)
            self.__debug_print__('Output filetype :' + self.__out_filetype)

            if self.__out_filetype == 'flac':
                if config_data['output_options']['flac_options']['resampling']:
                    out_bit_depth = config_data['output_options']['flac_options']['resampling_options']['bit_depth']
                    out_sampling = config_data['output_options']['flac_options']['resampling_options']['sampling']
                    out_resampler = 'aresample=resampler=' + config_data['output_options']['flac_options']['resampling_options']['resampler']
                    ffmpeg_resample_option = ' '.join(['-sample_fmt', out_bit_depth, '-af', out_resampler, '-ar', out_sampling])
                    self.__debug_print__(ffmpeg_resample_option)
                    self.__ffmpeg_options = ffmpeg_resample_option

                comp_level = config_data['output_options']['flac_options']['comp_level']
                ffmpeg_comp_option = ' '.join(['-compression_level', comp_level])
                self.__ffmpeg_options = ' '.join([self.__ffmpeg_options, ffmpeg_comp_option, '-c:v copy'])
                self.__debug_print__(self.__ffmpeg_options)

            elif self.__out_filetype == 'mp3':
                self.__ffmpeg_options = ' '.join([self.__ffmpeg_options, '-c:a', config_data['output_options']['mp3_options']['codec'], config_data['output_options']['mp3_options']['option_string'], '-c:v copy'])
                self.__debug_print__(self.__ffmpeg_options)

            elif self.__out_filetype == 'aac':
                self.__ffmpeg_options = ' '.join([self.__ffmpeg_options, '-c:a', config_data['output_options']['aac_options']['codec'], config_data['output_options']['aac_options']['option_string'], '-c:v copy'])
                self.__debug_print__(self.__ffmpeg_options)

        except:
            print('Error')

        return


    def exec(self):
        target_file = '*.' + self.__src_filetype
        filelist = Path(os.getcwd()).glob(target_file)
        self.__debug_print__(filelist)
        out_dir = os.path.join(os.getcwd(), 'out')
        self.__debug_print__(out_dir)
        if not os.path.exists(out_dir):
            try:
                os.mkdir(out_dir)
            except:
                print('Output directory creation failed')

        for file in filelist:
            try:
                in_filename = '\"' + file.name + '\"'
                out_filename = '\"' + 'out' + os.sep + file.name.rsplit('.', 1)[0] + '.' + self.__out_filetype + '\"'
                shell_command = ' '.join([self.__ffmpeg_command, '-i', in_filename, self.__ffmpeg_options, out_filename])
                self.__debug_print__(shell_command)
                subprocess.run(shell_command, shell=True)
                continue
            except:
                print('Error')
        return


    def __debug_print__(self, dbg_data):
        if self.__debug:
            print('DEBUG: ', end='')
            print(dbg_data)
        return


def main():
    parser = argparse.ArgumentParser(description='Convert multiple audio files using FFmpeg')
    parser.add_argument('-p', '--profile', type=str, default='', help='Specify pre-set config json file')
    parser.add_argument('-i', '--input_filetype', type=str, default='', help='Specify input filetype')
    parser.add_argument('-o', '--output_filetype', type=str, default='', help='Specify output filetype (flac, mp3 or aac).')
    args = parser.parse_args()

    resampler = Resampling()
    if len(args.profile) > 0:
        resampler.set_profile(args.profile)
    if len(args.input_filetype) > 0:
        resampler.set_input_filetype(args.input_filetype)
    if len(args.output_filetype) > 0:
        resampler.set_output_filetype(args.output_filetype)

    resampler.configure()
    resampler.exec()


if __name__ == "__main__":
    main()
