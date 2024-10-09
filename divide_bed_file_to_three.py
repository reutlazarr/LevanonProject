import os

def split_bed_file(bed_file_path):
    # Get the original directory and base name of the bed file
    bed_dir = os.path.dirname(bed_file_path)
    bed_base_name = os.path.basename(bed_file_path)

    # Output filenames for each part
    output_file_1 = os.path.join(bed_dir, "1-40000.bed")
    output_file_2 = os.path.join(bed_dir, "40001-80000.bed")
    output_file_3 = os.path.join(bed_dir, "80001-126096.bed")
    
    # Read the original BED file
    with open(bed_file_path, 'r') as bed_file:
        lines = bed_file.readlines()

    # Get the number of lines
    total_lines = len(lines)

    # Define split points
    split_1 = 40000
    split_2 = 80000

    # Write the first part (lines 1-40000)
    with open(output_file_1, 'w') as output_1:
        output_1.writelines(lines[:split_1])

    # Write the second part (lines 40001-80000)
    with open(output_file_2, 'w') as output_2:
        output_2.writelines(lines[split_1:split_2])

    # Write the third part (lines 80001-126096)
    with open(output_file_3, 'w') as output_3:
        output_3.writelines(lines[split_2:])

    print(f"File split into: \n{output_file_1} \n{output_file_2} \n{output_file_3}")

# Example usage
bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/all_sites_converted.bed"  # Replace with the path to your BED file
split_bed_file(bed_file_path)
