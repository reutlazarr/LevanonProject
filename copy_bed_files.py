import os
import shutil

# Paths to the directories
bed_files_dir = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/split_sites_to_500/"
dirs_path = "/private10/Projects/Reut_Shelly/our_tool/data/division_to_500/"
output_dir = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/unprocessed_bed_files/"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get list of BED files
bed_files = [f for f in os.listdir(bed_files_dir) if f.endswith('.bed')]

# Get list of directories
dirs = os.listdir(dirs_path)

# Extract BED file ranges
bed_file_ranges = [f.replace('sites_', '').replace('.bed', '').replace('_', '-') for f in bed_files]

# Extract matching directories in both possible formats (with "-" and "_")
dirs_dash = [d.replace('_', '-') for d in dirs]

# Find BED files without a matching directory
unmatched_bed_files = [f for f, r in zip(bed_files, bed_file_ranges) if r not in dirs_dash]

# Copy unmatched BED files to the output directory
for bed_file in unmatched_bed_files:
    src = os.path.join(bed_files_dir, bed_file)
    dst = os.path.join(output_dir, bed_file)
    shutil.copy(src, dst)
    print(f"Copied {bed_file} to {output_dir}")
