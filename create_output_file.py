import os
from fold import united_main  # Import the function from fold.py

def run_fold_script(bed_file_path, orig_site_dir, bed_file_name):
    try:
        # Ensure the orig_site_dir exists (create if necessary)
        os.makedirs(orig_site_dir, exist_ok=True)
        
        # Create the output file path as output_{bed_file_name}.txt inside orig_site_dir
        output_file = os.path.join(orig_site_dir, f"output_{bed_file_name}.txt")

        # Optionally, you can redirect the print outputs from fold.py to the output file (if necessary)
        with open(output_file, 'w') as f:
            # Redirect standard output to the file
            print(f"Processing {bed_file_path}...", file=f)
            
            # Call the fold.py's united_main function with the paths
            united_main(bed_file_path, orig_site_dir)
        
        print(f"Successfully processed {bed_file_path}. Output saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing {bed_file_path}: {str(e)}")

def run_on_directory(bed_files_dir, orig_site_parent_dir):
    # List all BED files in the directory
    bed_files = [f for f in os.listdir(bed_files_dir) if f.endswith('.bed')]
    
    # Process each BED file sequentially
    for bed_file in bed_files:
        bed_file_path = os.path.join(bed_files_dir, bed_file)
        
        # Create orig_site_dir by using the bed file name without its extension
        bed_file_name = os.path.splitext(bed_file)[0]
        orig_site_dir = os.path.join(orig_site_parent_dir, bed_file_name)
        
        # Run fold.py for each BED file and redirect output to output_{bed_file_name}.txt
        run_fold_script(bed_file_path, orig_site_dir, bed_file_name)

# Example usage
bed_files_dir = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/unprocessed_bed_files/"  # Directory containing your BED files
orig_site_parent_dir = "/private10/Projects/Reut_Shelly/our_tool/data/division_to_500_1709/" # Parent directory for each orig_site_dir
run_on_directory(bed_files_dir, orig_site_parent_dir)
