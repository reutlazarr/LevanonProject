# Define the path to your BED file
bed_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/all_sites_converted.bed"

# Dictionary to track end positions and their corresponding strands
end_positions = {}

# Open and read the file line by line
with open(bed_file_path, 'r') as file:
    for line in file:
        # Split each line by tab or whitespace
        fields = line.strip().split()
        chr_name, start, end, gene, dot, strand = fields
        
        # Check if the end position is already in the dictionary
        if end in end_positions:
            # Check if the strand is different
            if end_positions[end] != strand:
                print("Conflict found:")
                print(f"Previous line: {chr_name}\t{start}\t{end}\t{gene}\t{dot}\t{end_positions[end]}")
                print(f"Current line: {line.strip()}\n")
        else:
            # Store the strand for this end position
            end_positions[end] = strand
