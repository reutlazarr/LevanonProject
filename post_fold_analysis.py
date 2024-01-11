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
                pattern_of_bp = re.compile(r"(\d+)bp")
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
                    match = pattern_of_bp.match(line)
                    if match:
                         stem_length =  match.group(1)
                    else:
                         print("no bp found")
                    return (coords_of_segment, seqs_of_segment, stem_length)
        # if we our editng site is in any segment
        return (0, 0)

def main_analysis(start, end, st_path, location_of_site):
    new_start, new_end, new_location_of_site = ReNumber_the_sequence(start, end, location_of_site)
    coords_of_segment, seqs_of_segment, stem_length = parse_st_file(st_path, new_location_of_site)





