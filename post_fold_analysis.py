import re

# the function will take the original numbering and change it to match the new numbering of the coloring software
def ReNumber_the_sequence(start, end, location_of_site):
    new_start = 1
    new_end = end - start 
    new_location_of_site = location_of_site - start
    return (new_start, new_end, new_location_of_site)

def parse_st_file(st_file, location_of_site):
        with open(st_file, "r") as bpf:
            data = bpf.readlines()
        regex = re.compile(r"(\s\d+\.\.\d+\s)")
        for line in data:
            if "segment" in line:
                l = regex.split(line)
                segment_and_length = l[0]
                split_segment_and_length = segment_and_length.split()
                segment = split_segment_and_length[0]
                length = split_segment_and_length[1]
                range1 = l[1].strip() 
                range1 = {
                    "start": int(range1.split(".")[0]), 
                    "end": int(range1.split(".")[-1]), 
                }
                range2 = l[3].strip()
                range2 = {
                    "start": int(range2.split(".")[0]),
                    "end": int(range2.split(".")[-1]),
                }
                # if the editing site is in that segmant
                if (range1["start"] <= location_of_site + 1 <= range1["end"]) or (
                    range2["start"] <= location_of_site + 1 <= range2["end"]
                ):
                    coords_of_segment = (
                        range1["start"],
                        range1["end"],
                        range2["start"],
                        range2["end"],
                    )
                    seqs_of_segment = (l[2], l[-1].strip("\n"))
                    return coords_of_segment or "default_coords", seqs_of_segment or "default_seqs", segment or "default_segment", length or "default_length"
        return coords_of_segment or "default_coords", seqs_of_segment or "default_seqs", segment or "default_segment", length or "default_length"

def extract_segment(start, end, st_path, location_of_site):
    new_start, new_end, new_location_of_site = ReNumber_the_sequence(start, end, location_of_site)
    print (f"the new start is : {new_start} ,the new end is: {new_end} ,the new location of site is: {new_location_of_site}")
    # coords of the location of site's segment
    coords_of_segment, seqs_of_segment, segment, length = parse_st_file(st_path, new_location_of_site)
    print (coords_of_segment, seqs_of_segment, segment, length)