import argparse
import os
import ffmpeg
from os import path

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def convert_to_mp3(input, output, bitrate=96000, format="mp3"):
    print("Converting {} to {}...".format(input, output))
    (
        ffmpeg
            .input(input)
            .output(output, audio_bitrate=bitrate, format=format)
            .overwrite_output()
            .run(quiet=True)
    )
    print("Converted {} to {}.".format(input, output))


def build_output_path(root_dir, output_dir, intput_file, extension="mp4", should_flatten=False):
    root_parts = root_dir.split("/")
    sub_dir = None
    if len(root_parts) > 1:
        sub_dir = root_parts[-1]
        sub_dir = sub_dir.replace("/", "")
        sub_dir = sub_dir.replace(":", "")
        if not should_flatten:
            output_dir = path.join(output_dir, sub_dir)
            os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = output_dir
    out_filename = intput_file.replace(extension, "mp3")
    # Prefixes the file with the directory
    if should_flatten and sub_dir is not None:
        out_filename = "{} - {}".format(sub_dir, out_filename)
    return path.join(output_dir, out_filename)

def prefix_file(out_filename, prefix):
    # Prefixes the file with the sequence
    if prefix is not None:
        file_parts = out_filename.split("/")
        file_name = file_parts[-1]
        file_name_prefixed = "{:04} - {}".format(prefix, file_name)
        del file_parts[-1]
        out_filename = "/".join(file_parts) + "/" + file_name_prefixed
    return out_filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input dir with mp4 files", type=dir_path)
    parser.add_argument("-o", "--output", help="output dir with mp3 files", type=dir_path)
    parser.add_argument("-e", "--extension", help="extension", default="mp4")
    parser.add_argument("-f", "--flatten", help="flatten files into a single output dir. Adds directory into filename", action='store_true')
    args = parser.parse_args()
    count_files = 0
    total_files = 0

    input_path = args.input
    output_path = args.output
    extension = args.extension
    should_flatten = args.flatten

    files_to_convert = {}


    # Discover the files, builds a map with input -> output
    for root, dirs, files in os.walk(input_path, topdown=True):
        for filename in files:
            full_input_path = path.join(root, filename)
            if extension in filename:
                full_output_path = build_output_path(root, output_path, filename, extension, should_flatten)
                files_to_convert[full_input_path] = full_output_path

    # takes the set of files, sorts, prefixes and converts
    sorted_files = list(files_to_convert.keys())
    sorted_files.sort()
    for input_file in sorted_files:
        count_files += 1
        full_output_path = files_to_convert[input_file]
        full_output_path = prefix_file(full_output_path, count_files)
        convert_to_mp3(input=input_file, output=full_output_path)

    print("Completed Conversion of {} files.".format(len(sorted_files)))