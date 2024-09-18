import os
import subprocess

def run_fold_script(bed_file_path, specific_bed_file_dir, bed_file_name):
    try:
        # Create output file path as output_{bed_file_name}.txt inside orig_site_dir
        output_file = os.path.join(specific_bed_file_dir, f"output_{bed_file_name}.txt")
        
        # # Ensure the specific_bed_file_dir exists (create if necessary)
        # os.makedirs(specific_bed_file_dir, exist_ok=True)
        
        # Prepare the command to run the fold.py script
        command = f"python /home/alu/aluguest/Reut_Shelly/vscode/code_shelly/LevanonProject/fold.py {bed_file_path} {specific_bed_file_dir} > {output_file} 2>&1"
        
        # Run the command
        subprocess.run(command, shell=True, check=True)
        
        print(f"Successfully processed {bed_file_path}. Output saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing {bed_file_path}: {str(e)}")

def run_on_directory(bed_files_dir, orig_site_parent_dir):
    # List all BED files in the directory
    bed_files = [f for f in os.listdir(bed_files_dir) if f.endswith('.bed')]
    
    # Process each BED file sequentially
    for bed_file in bed_files:
        bed_file_path = os.path.join(bed_files_dir, bed_file)
        
        # Create specific_bed_file_dir by using the bed file name without its extension
        bed_file_name = os.path.splitext(bed_file)[0]
        specific_bed_file_dir = os.path.join(orig_site_parent_dir, bed_file_name)
        
        # Ensure the specific_bed_file_dir exists (create if necessary)
        os.makedirs(specific_bed_file_dir, exist_ok=True)
        # Run fold.py for each BED file and redirect output to output_{bed_file_name}.txt
        run_fold_script(bed_file_path, specific_bed_file_dir, bed_file_name)

# Example usage
bed_files_dir = "/private10/Projects/Reut_Shelly/our_tool/data/convert_sites/sites_for_analysis/two_unprocesses_bed_files/"  # Directory containing your BED files
orig_site_parent_dir = "/private10/Projects/Reut_Shelly/our_tool/data/two_division_to_500_3/" # Parent directory for each orig_site_dir
run_on_directory(bed_files_dir, orig_site_parent_dir)