import pre_fold as first
def get_output_ratio_based_tool(dis_list, location_of_site):
    # edge case: our site of interest has no other sites in its vicinity, thus folding it is irrelevant
    if len(dis_list) == 1:
        print("SITE OF INTEREST HAS NO SURROUNDING EDITING SITES")
        return
    # call the func based on best ratio
    # the output starts with scope
    min_positive = first.min_distance_for_positive(dis_list)
    min_negative = first.min_distance_for_negative(dis_list)
    best_ten = first.find_optimal_dis_in_scope_and_ratio(min_positive, min_negative)
    # the output starts with "start"
    new_combinations = first.new_ratio_combinations(best_ten, location_of_site)
    best_ratio_based_list = first.get_best_ratio(best_ten, new_combinations, location_of_site)
    # chr = best_ratio_based_list[5].split(": ")[1]
    start = int(best_ratio_based_list[0].split(": ")[1])
    end = int(best_ratio_based_list[1].split(": ")[1])
    return start, end