import os
import argparse
import json
import subprocess
from pathlib import Path

class Resampling:

    def __init__(self):
        self.debug = False
        self.ffmpeg_command = 'ffmpeg'
        self.ffmpeg_option = ''
        self.src_filetype = 'flac'
        self.out_filetype = 'flac'
        self.profile_json = 'config.json'


    def set_profile(self, profile):
        self.profile_json = profile
        return


    def configure(self):
        profile_path = os.path.split(__file__)[0] + os.sep + self.profile_json
        self.debug_print(profile_path)

        try:
            config_file = open(profile_path, 'r')
            config_data = json.load(config_file)
            self.debug_print(profile_path)

            self.debug = config_data['exec_options']['debug_option']
            self.ffmpeg_command = config_data['exec_options']['ffmpeg_path']
            self.debug_print(self.ffmpeg_command)

            self.ffmpeg_command = config_data['exec_options']['ffmpeg_path']
            self.src_filetype = config_data['input_options']['src_type'].lower()
            self.out_filetype = config_data['output_options']['out_type'].lower()
            self.debug_print('Input filetype  :' + self.src_filetype)
            self.debug_print('Output filetype :' + self.out_filetype)

            if self.out_filetype == 'flac':
                if config_data['output_options']['flac_options']['resampling']:
                    out_bit_depth = config_data['output_options']['flac_options']['resampling_options']['bit_depth']
                    out_sampling = config_data['output_options']['flac_options']['resampling_options']['sampling']
                    out_resampler = 'aresample=resampler=' + config_data['output_options']['flac_options']['resampling_options']['resampler']
                    ffmpeg_resample_option = ' '.join(['-sample_fmt', out_bit_depth, '-af', out_resampler, '-ar', out_sampling])
                    self.debug_print(ffmpeg_resample_option)
                    self.ffmpeg_option = ffmpeg_resample_option

                comp_level = config_data['output_options']['flac_options']['comp_level']
                ffmpeg_comp_option = ' '.join(['-compression_level', comp_level])
                self.ffmpeg_option = ' '.join([self.ffmpeg_option, ffmpeg_comp_option, '-c:v copy'])
                self.debug_print(self.ffmpeg_option)

            elif self.out_filetype == 'mp3':
                self.ffmpeg_option = ' '.join([self.ffmpeg_option, '-c:a', config_data['output_options']['mp3_options']['codec'], config_data['output_options']['mp3_options']['option_string'], '-c:v copy'])
                self.debug_print(self.ffmpeg_option)

            elif self.out_filetype == 'aac':
                self.ffmpeg_option = ' '.join([self.ffmpeg_option, '-c:a', config_data['output_options']['aac_options']['codec'], config_data['output_options']['aac_options']['option_string'], '-c:v copy'])
                self.debug_print(self.ffmpeg_option)

        except:
            print('Error')

        return


    def exec(self):
        target_file = '**/*.' + self.src_filetype
        filelist = Path(os.getcwd()).glob(target_file)
        out_dir = os.path.join(os.getcwd(), 'out')
        self.debug_print(out_dir)
        try:
            os.mkdir(out_dir)
        except:
            print('Output directory already exist')

        for file in filelist:
            try:
                in_filename = '\"' + file.name + '\"'
                out_filename = '\"' + 'out' + os.sep + file.name.rsplit('.', 1)[0] + '.' + self.out_filetype + '\"'
                shell_command = ' '.join([self.ffmpeg_command, '-i', in_filename, self.ffmpeg_option, out_filename])
                self.debug_print(shell_command)
                subprocess.run(shell_command, shell=True)
                continue
            except:
                print('Error')
        return


    def debug_print(self, string):
        if self.debug:
            print('DEBUG: ' + string)
        return


def main():
    parser = argparse.ArgumentParser(description='Convert multiple audio files using FFmpeg')
    parser.add_argument('-p', '--profile', type=str, default='', help='Specify pre-set config json file')
    args = parser.parse_args()

    resampler = Resampling()
    if len(args.profile) > 0:
        resampler.set_profile(args.profile)

    resampler.configure()
    resampler.exec()


if __name__ == "__main__":
    main()
