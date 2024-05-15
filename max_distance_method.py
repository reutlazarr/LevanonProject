import pre_fold as first

def get_output_max_distance_tool(dis_list, location_of_site):
    if len(dis_list) == 1:
        print("SITE OF INTEREST HAS NO SURROUNDING EDITING SITES")
        return
    # call the func based on max distance
    best_by_max_dis = first.max_distance(dis_list, location_of_site)
    # chr = best_by_max_dis[4].split(": ")[1]
    start = int(best_by_max_dis[0].split(": ")[1])
    end = int(best_by_max_dis[1].split(": ")[1])
    return start, end