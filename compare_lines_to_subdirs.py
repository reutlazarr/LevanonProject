import os
import csv

def count_tool_subdirs(dir_path):
    # Initialize counters for subdirectories
    ratio_based_tool_count = 0
    default_tool_count = 0
    max_distance_tool_count = 0

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(dir_path):
        # Count the tool subdirectories
        if 'ratio_based_tool' in dirs:
            ratio_based_tool_count += 1
        if 'default_tool' in dirs:
            default_tool_count += 1
        if 'max_distance_tool' in dirs:
            max_distance_tool_count += 1

    return ratio_based_tool_count, default_tool_count, max_distance_tool_count

def count_csv_lines(csv_file_path):
    # Count the number of lines in a CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        line_count = sum(1 for row in reader)  # Sum lines
    return line_count

# Provide the directory path and two CSV file paths
dir_path = "/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/"  # Replace with your directory path
final_df = "/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/final_df.csv"  # Replace with your first CSV file path
no_segment = "/private10/Projects/Reut_Shelly/our_tool/data/969-40000_no_multi/no_segment_df.csv"  # Replace with your second CSV file path

# Count tool subdirectories
ratio_based_count, default_count, max_distance_count = count_tool_subdirs(dir_path)
dirs_sum = ratio_based_count + default_count + max_distance_count

# Count CSV lines
csv1_lines = count_csv_lines(final_df)
csv2_lines = count_csv_lines(no_segment)

# Output the results
print(f"'ratio_based_tool' subdirectories: {ratio_based_count}")
print(f"'default_tool' subdirectories: {default_count}")
print(f"'max_distance_tool' subdirectories: {max_distance_count}")

print(f"sum of dirs {dirs_sum}")
print(f"Lines in {final_df}: {csv1_lines}")
print(f"Lines in {no_segment}: {csv2_lines}")
