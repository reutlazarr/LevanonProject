import pandas as pd 
import csv
# split the file's lines and define the file
def process_st_file_by_lines(st_file):
    # open the st file
    with open(st_file, 'r') as file:
        # read the entire file and split it to different lines 
        all_file = file.read().split('\n')
        # first linE
    name = all_file[0]
    # Second line
    seq_length = all_file[1]
    # annotation[2] is irrelevant since it is the page number
    # the actual sequence (line 4)
    cur_sequence = all_file[3]
    # the dot bracket part (line 5)
    cur_structure = all_file[4]
    # E S I etc
    features = all_file[5]
    return name, seq_length, cur_sequence, cur_structure, features

def extract_start_and_end_position(pos_of_editing_site, range_of_interest):
    # the interesting part - probably 40 bases for each site
    start_position = pos_of_editing_site - range_of_interest
    end_position = pos_of_editing_site + range_of_interest
    return start_position, end_position
# the func's output is two lists in which the first one is the sites evolving bases and the second one is the site's structures
# it uses "iterate string"
def create_list_of_features(cur_sequence, features, start_position, end_position):   
    list_of_seq_empty = []
    list_of_features_empty = []
    list_of_seq = iterate_string(cur_sequence, start_position, end_position, list_of_seq_empty)
    list_of_features = iterate_string(features, start_position, end_position, list_of_features_empty)
    return list_of_seq, list_of_features


def iterate_string(string_to_iterate, start, end, list_to_add):
    for i in range(start, end + 1):
        list_to_add.append(string_to_iterate[i])
    return list_to_add

def extract_feature_of_editing_site():
    pass 


def check_strand_identity(coords_of_segment):
    return start_of_first_strand, end_of_first_strand, start_of_sec_strand, end_of_sec_strand, editing_on_first_strand, editing_on_sec_strand

# create the data frame general structure 
def create_df_structure(csv_file_path, overwrite=False):
    # Specify the column names
    column_names = ["editing location site", "number of I", "number of S", "number of H", "number of E", "number of B", "number of M", "editing site base", "editing base on the other strand"]
    # Check if the file already exists
    if os.path.exists(csv_file_path) and not overwrite:
        raise FileExistsError(f"File '{csv_file_path}' already exists. Set 'overwrite=True' to overwrite.")
    # Create the DataFrame with column names
    df = pd.DataFrame(columns=column_names)
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)

def fill_df_with_data(csv_file_path, list_of_features):
    m_count, s_count, h_count, i_count, e_count, b_count = categorize_features(list_of_features)
    # call function that extracts nuc's structural feature
    # @@ - we need to add editing location feature!!!
    new_row = {
    "editing location site": "example",
    "number of I": i_count,
    "number of S": s_count,
    "number of H": h_count,
    "number of E": e_count,
    "number of B": b_count,
    "number of M": m_count
}
    # Append the new row to the DataFrame
    df = df.append(new_row, ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    df.to_csv(csv_file_path, index=False)
    return df


# iterate list_of_seq, list_of_features and count how many feature of each type there are
def categorize_features(list_of_features):

    for char in list_of_features:
        if char == "m":
            m_count += 1
        if char == "s":
            s_count +=1 
        if char == "h":
            h_count += 1
        if char == "i":
            i_count += 1
        if char == "e":
            e_count += 1
        if char == "b":
            b_count += 1
    return m_count, s_count, h_count, i_count, e_count, b_count

def create_csv_file_path():

def mini_main():
    # the relevant st_file
    st_file_path = "/private10/Projects/Reut_Shelly/our_tool/data/sites_of_interest_analysis/chr1_10003145/default_tool/10003145_default_tool_mxfolded.st"
    pos_of_editing_site = 100
    range_of_interest = 40
    # split st_file by lines
    name, seq_length, cur_sequence, cur_structure, features = process_st_file_by_lines(st_file_path)
    # extract start position and end position
    # extract list of features, list of seq
    start_position, end_position = extract_start_and_end_position(pos_of_editing_site, range_of_interest)
    list_of_seq, list_of_features = create_list_of_features(cur_sequence, features, start_position, end_position)
    # create csv file path
    csv_file_path = "some_csv_file_path"
    # create df structure
    create_df_structure(csv_file_path, overwrite=False)
    # fill df with data, based on list of features
    fill_df_with_data(csv_file_path, list_of_features)
