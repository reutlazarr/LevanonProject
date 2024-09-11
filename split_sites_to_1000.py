import os

def split_bed_file(bed_file_path, output_dir, lines_per_file=200):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(bed_file_path, 'r') as bed_file:
        bed_file.readline()  # Skip the header line
        file_count = 0
        line_count = 0
        lines_buffer = []

        for line in bed_file:
            lines_buffer.append(line)
            line_count += 1

            # Once we have enough lines, save them to a new file
            if line_count % lines_per_file == 0:
                file_count += 1
                output_file_path = os.path.join(output_dir, f"sites_{file_count*lines_per_file - lines_per_file + 1}_{file_count*lines_per_file}.bed")
                with open(output_file_path, 'w') as output_file:
                    output_file.writelines(lines_buffer)
                lines_buffer = []

        # Write remaining lines if any
        if lines_buffer:
            file_count += 1
            output_file_path = os.path.join(output_dir, f"sites_{file_count*lines_per_file - lines_per_file + 1}_{line_count}.bed")
            with open(output_file_path, 'w') as output_file:
                output_file.writelines(lines_buffer)

# Example usage:
bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/all_sites_converted.bed"
output_dir = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/split_sites_to_200/"
split_bed_file(bed_file_path, output_dir)