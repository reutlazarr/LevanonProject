import os

def find_empty_svg_files(base_dir, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".svg"):
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) == 0:
                        f.write(file_path + '\n')

base_directory = "/private10/Projects/Reut_Shelly/our_tool/data/multi_100"
output_file = "empty_svg_files.txt"
find_empty_svg_files(base_directory, output_file)
