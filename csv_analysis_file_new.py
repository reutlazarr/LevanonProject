import os
import pandas as pd 
import csv
# 1 create the df 
def create_empty_df():
    general_df = pd.DataFrame(columns=['segment length', 'complementary strand base', '-30', '-29', '-28', '-27', '-26', '-25', '-24', '-23', '-22', '-21', '-20', '-19', '-18', '-17', '-16', '-15', '-14', '-13', '-12', '-11', '-10', '-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0 - site feature', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'])
    return general_df
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

# 2 change pos_of_editing_site based on the genome so that it would fit the file index


def extract_start_and_end_position(pos_of_editing_site, range_of_interest):
    # the interesting part - probably 40 bases for each site
    start_position = pos_of_editing_site - range_of_interest
    end_position = pos_of_editing_site + range_of_interest
    return start_position, end_position

# the func's output is two lists in which the first one is the sites evolving bases and the second one is the site's structures
# it uses "iterate string"
# 2 - create a df and insert each value in it
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
    # if os.path.exists(csv_file_path) and not overwrite:
    #     raise FileExistsError(f"File '{csv_file_path}' already exists. Set 'overwrite=True' to overwrite.")
    # Create the DataFrame with column names
    df_in_csv_file = pd.DataFrame(columns=column_names)
    # Save the DataFrame to a CSV file
    df_in_csv_file.to_csv(csv_file_path, index=False)
    return df_in_csv_file

def fill_df_with_data(pos_of_editing_site, csv_file_path, list_of_features, df_in_csv_file):
    m_count, s_count, h_count, i_count, e_count, b_count = categorize_features(list_of_features)
    # call function that extracts nuc's structural feature
    new_row = {
    "editing location site": pos_of_editing_site,
    # list_of_featurs[pos_of_editing_site - location of first base in segment]
    "editing site feature": list_of_features[pos_of_editing_site],
    "segment size": "call itamar's func",
    "number of I": i_count,
    "number of S": s_count,
    "number of H": h_count,
    "number of E": e_count,
    "number of B": b_count,
    "number of M": m_count,
    "editing site base": "-",
    "editing base on the other strand": "-"
}
    # Append the new row to the DataFrame
    df_in_csv_file = df_in_csv_file.append(new_row, ignore_index = True) 
    # Write the updated DataFrame back to the CSV file
    df_in_csv_file.to_csv(csv_file_path, index=False)
    return df_in_csv_file


# def adjacent_bases(pos_of_editing_site):

# iterate list_of_seq, list_of_features and count how many feature of each type there are
def categorize_features(list_of_features):
# m_count = s_count = h_count = i_count = e_count = b_count = 0
    m_count = h_count = i_count = e_count = b_count = 0
    s_count = 0
    for letter in list_of_features:
        if letter == "M":
            m_count += 1
        if letter == "S":
            s_count += 1 
        if letter == "H":
            h_count += 1
        if letter == "I":
            i_count += 1
        if letter == "E":
            e_count += 1
        if letter == "B":
            b_count += 1
    return m_count, s_count, h_count, i_count, e_count, b_count

def create_csv_file_path(dir_path, file_name):
    complete_path = os.path.join(dir_path, file_name)
    return complete_path

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
    dir_path = "/private10/Projects/Reut_Shelly/our_tool/data/sites_of_interest_analysis/chr1_10003145/default_tool/"
    file_name = "csv_file.csv"
    csv_file_path = create_csv_file_path(dir_path, file_name)
    
    # create df structure
    df_in_csv_file = create_df_structure(csv_file_path, overwrite=False)
    # fill df with data, based on list of features
    fill_df_with_data(pos_of_editing_site, csv_file_path, list_of_features, df_in_csv_file)

def mini_main():
    print(create_empty_df())

mini_main()

