import os
import subprocess


def run_bpRNA(path_to_bpRNA_result, site_dir):
    # path to zohar's script
    bpRNA_path="/private6/Projects/Yeast_Itamar_10_2022/Fold_energy/bpRNA/run_bpRNA.sh"
    os.chdir(site_dir)
    p = subprocess.run([bpRNA_path, path_to_bpRNA_result], capture_output=True, text=True)
    # if the process fails
    assert not p.stdout, "bpRNA cant run file: " + path_to_bpRNA_result
    # create out file name
    out_f = path_to_bpRNA_result.split("/")[-1]
    # get rid of the dbn suffix
    out_f = remove_suffix(out_f, os.path.splitext(out_f)[1]) + ".st"
    return site_dir + out_f

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

site_dir = "/private10/Projects/Reut_Shelly/our_tool/data/sites_analysis/chr1_495166/default_tool/"
path_to_dbn_file = "/private10/Projects/Reut_Shelly/our_tool/data/sites_analysis/chr1_495166/default_tool/495166_default_tool_mxfolded.dbn"
st_path = run_bpRNA(path_to_dbn_file, site_dir)