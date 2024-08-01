import re
import os

# the function will take the original numbering and change it to match the new numbering of the coloring software
def ReNumber_the_sequence(start, end, location_of_site):
    print ("old start: " , start)
    print("old end: ", end)
    print("old site: " , location_of_site)
    start = int(round(start))
    end = int(round(end))
    new_start = 1
    new_end = end - start + 1 
    print("new end: " , end)     
    new_location_of_site = location_of_site - start +1 
    print("new location of site:" , new_location_of_site)
    return (new_start, new_end, new_location_of_site)

def parse_st_file(st_file, location_of_site):
    # Initialize default values
    coords_of_segment = "default_coords"
    seqs_of_segment = "default_seqs"
    segment = "default_segment"
    length = "default_length"

    # Check if the file exists
    if not os.path.exists(st_file):
        print(f"Error: The file {st_file} does not exist.")
        return coords_of_segment, seqs_of_segment, segment, length
    # open the file
    with open(st_file, "r") as bpf:
        data = bpf.readlines()
    
    # regex: 123...456
    regex = re.compile(r"(\s\d+\.\.\d+\s)")
    for line in data:
        # if we are in the bottom part of the file which looks like this: "segment1 3bp 12..14 AGG 878..880 CCU"
        if "segment" in line:
            l = regex.split(line)    # split the line this way: ['segment1 3bp', ' 12..14 ', 'AGG', ' 878..880 ', 'CCU']
            segment_and_length = l[0] # 'segment1 3bp'
            split_segment_and_length = segment_and_length.split()
            segment = split_segment_and_length[0] # segment1
            length = split_segment_and_length[1] # 3bp
            range1 = l[1].strip() # remove spaces from '  12..14  '
            range1 = {
                "start": int(range1.split(".")[0]), # 12
                "end": int(range1.split(".")[-1]), # 14
            }
            range2 = l[3].strip() # same with the second range
            range2 = {
                "start": int(range2.split(".")[0]),
                "end": int(range2.split(".")[-1]),
            }
            # Check if the editing site is in that segment
            if (range1["start"] <= location_of_site + 1 <= range1["end"]) or (
                range2["start"] <= location_of_site + 1 <= range2["end"]
            ):
                # the requested segment
                coords_of_segment = (
                    range1["start"],
                    range1["end"],
                    range2["start"],
                    range2["end"],
                )
                seqs_of_segment = (l[2], l[-1].strip("\n")) # seqs_of_segment is ('AGG', 'CCU')
                break  # Ensures that you stop searching once a match is found

    return coords_of_segment, seqs_of_segment, segment, length

def extract_segment(start, end, st_path, location_of_site):
    new_start, new_end, new_location_of_site = ReNumber_the_sequence(start, end, location_of_site)
    print (f"the new start is : {new_start} ,the new end is: {new_end} ,the new location of site is: {new_location_of_site}")
    # coords of the location of site's segment
    coords_of_segment, seqs_of_segment, segment, length = parse_st_file(st_path, new_location_of_site)
    # convert_to_genomic_coords(coords_of_segment, seqs_of_segment, segment, length)
    print (coords_of_segment, seqs_of_segment, segment, length)

# def convert_to_genomic_coords(coords_of_segment, seqs_of_segment, segment, length):
