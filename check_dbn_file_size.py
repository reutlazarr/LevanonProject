import os

def process_directories(root_dir, output_file_path):
    with open(output_file_path, 'w') as output_file:
        # Write the first headline
        output_file.write("dbn size is 0:\n")

        # Iterate through all subdirectories in the root directory
        for root, dirs, files in os.walk(root_dir):
            fa_file = None
            dbn_file = None
            st_file_found = False
            
            for file in files:
                if file.endswith('.fa'):
                    fa_file = os.path.join(root, file)
                elif file.endswith('.dbn'):
                    dbn_file = os.path.join(root, file)
                elif file.endswith('.st'):
                    st_file_found = True
            
            # Check if .dbn file size is 0
            if fa_file and dbn_file and os.path.getsize(dbn_file) == 0:
                with open(fa_file, 'r') as fa:
                    first_line = fa.readline().strip()
                output_file.write(f'{os.path.basename(root)}: {first_line}\n')
        
        # Write the second headline
        output_file.write("\nst is not created:\n")
        
        # Iterate again to check for missing .st files
        for root, dirs, files in os.walk(root_dir):
            fa_file = None
            st_file_found = False
            
            for file in files:
                if file.endswith('.fa'):
                    fa_file = os.path.join(root, file)
                elif file.endswith('.st'):
                    st_file_found = True
            
            # If .st file is not found, write the first line of .fa file
            if fa_file and not st_file_found:
                with open(fa_file, 'r') as fa:
                    first_line = fa.readline().strip()
                output_file.write(f'{os.path.basename(root)}: {first_line}\n')

# Example usage:
root_directory = "/private10/Projects/Reut_Shelly/our_tool/data/sites_analysis_shelly_2308/"
output_file = "/private10/Projects/Reut_Shelly/our_tool/data/sites_analysis_shelly_2308/problematic_sites.txt"
process_directories(root_directory, output_file)
