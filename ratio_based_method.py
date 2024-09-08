def get_output_ratio_based_tool(dis_list, location_of_site):
    # edge case: our site of interest has no other sites in its vicinity, thus folding it is irrelevant
    if len(dis_list) == 1:
        print("SITE OF INTEREST HAS NO SURROUNDING EDITING SITES")
        return 0,0
    # call the func based on best ratio
    # the output starts with scope
    min_positive = min_distance_for_positive(dis_list)
    min_negative = min_distance_for_negative(dis_list)
    best_ten = find_optimal_dis_in_scope_and_ratio(min_positive, min_negative)
    # the output starts with "start"
    new_combinations = new_ratio_combinations(best_ten, location_of_site)
    best_ratio_based_list = get_best_ratio(best_ten, new_combinations, location_of_site)
    # chr = best_ratio_based_list[5].split(": ")[1]
    start = int(best_ratio_based_list[0].split(": ")[1])
    end = int(best_ratio_based_list[1].split(": ")[1])
    return start, end

# dislist is made of [site (not of interest), scope, chr]
def min_distance_for_positive(dis_list):    
    # list of tuples containing scope and ratio of number of sites/ distance
    scope_ratio_num_of_editing_sites = []
    # for each scope, itearate the different editing sites
    for scope in range(0, 4000, 200):
        site_count = 0
        for _, site_dis_chr in enumerate(dis_list):
            # first is distance, sec is ratio, third is site, fourth is chr
            dis_of_specific_site = site_dis_chr[1]
            chr_of_specific_site = site_dis_chr[2]
            # check if the current site is in the scope checked
            if dis_of_specific_site <= scope and dis_of_specific_site > 0:
                site_count += 1
                ratio = site_count/scope
                # avoid duplicates
                if len(scope_ratio_num_of_editing_sites) != 0 and scope_ratio_num_of_editing_sites[-1][0] == "scope: " + str(scope):
                    scope_ratio_num_of_editing_sites[-1][1] = "ratio: " + str(ratio)
                    scope_ratio_num_of_editing_sites[-1][2] = "site: " + str(site_count)
                    scope_ratio_num_of_editing_sites[-1][3] = "chr: " + str(chr_of_specific_site)
                else: 
                    scope_ratio_num_of_editing_sites.append(["scope: " +str(scope), "ratio: " + str(ratio), "site: " + str(site_count), "chr: " + str(chr_of_specific_site)])
    return scope_ratio_num_of_editing_sites


def min_distance_for_negative(dis_list):
         # list of tuples cotaining scope and ratio of number of sites/ distance
    scope_ratio_num_of_editing_sites = []
    # for each scope, itearate the different editing sites
    for scope in range(0, -4000, -200):
        site_count = 0
        for _, site_dis_str in enumerate(dis_list):
            # first is distance, sec is ratio, third is 
            dis_of_specific_site = site_dis_str[1]
            chr_of_specific_site = site_dis_str[2]
            # check if the current site is in the scope checked
            if dis_of_specific_site >= scope and dis_of_specific_site < 0:
                site_count += 1
                ratio = -(site_count)/(scope)
                # avoid duplicates
                if len(scope_ratio_num_of_editing_sites) != 0 and scope_ratio_num_of_editing_sites[-1][0] == "scope: " + str(scope):
                    scope_ratio_num_of_editing_sites[-1][1] = "ratio: " + str(ratio)
                    scope_ratio_num_of_editing_sites[-1][2] = "site: " + str(site_count)
                    scope_ratio_num_of_editing_sites[-1][3] = "chr: " + str(chr_of_specific_site)
                else: 
                    scope_ratio_num_of_editing_sites.append(["scope: " +str(scope), "ratio: " + str(ratio), "site: " + str(site_count), "chr: " + str(chr_of_specific_site)])
    return scope_ratio_num_of_editing_sites

# find the ideal distance by first sort the list by the ratio and then return its matching window
def find_optimal_dis_in_scope_and_ratio(scope_ratio_num_of_editing_sites_p, scope_ratio_num_of_editing_sites_n):
    scope_ratio_num_of_editing_sites_p += scope_ratio_num_of_editing_sites_n
    n_p_sorted = sorted(scope_ratio_num_of_editing_sites_p, key=lambda x: float(x[1].split(': ')[1]))
    n_p_sorted_best_10 = n_p_sorted[len(n_p_sorted) - 10 :len(n_p_sorted)]
    return n_p_sorted_best_10

# chr added
# create different combinations of optimal scopes
# extract start, end
def new_ratio_combinations(n_p_sorted_best_10, location_of_site):
    combi_scopes_ratios_sites = []
    # create new combinations of scopes and ratios
    for item1 in n_p_sorted_best_10:
        for item2 in n_p_sorted_best_10:
            # multiply the different items only if they are not identical
            if item1 != item2:
                # the following variables are not affected by the scopes' negativity/ positivity
                scope1 = int(item1[0].split(": ")[1])
                scope2 = int(item2[0].split(": ")[1])
                chr = item1[3].split(": ")[1]
                # the start, end points are affectecd by the scopes' negativity/ positivity
                if scope1 > 0 and scope2 > 0:
                    start = location_of_site - 30
                    end = max(scope1, scope2) + location_of_site
                    # one scope contains the other scope
                    cur_num_site = max(int(item1[2].split(": ")[1]), int(item2[2].split(": ")[1]))
                if scope1 < 0 and scope2 < 0:
                    start = min(scope1, scope2) + location_of_site
                    end = location_of_site + 30
                    cur_num_site = min(int(item1[2].split(": ")[1]), int(item2[2].split(": ")[1]))
                # one of the item's scope is positive and the other one is negative
                if scope1 < 0 and scope2 > 0:
                    start = location_of_site + scope1
                    end = location_of_site + scope2
                    cur_num_site = int(item1[2].split(": ")[1]) + int(item2[2].split(": ")[1])
                if scope1 > 0 and scope2 < 0:
                    start = location_of_site + scope2
                    end = location_of_site + scope1
                    cur_num_site = int(item1[2].split(": ")[1]) + int(item2[2].split(": ")[1])
                # cur_scope is affected by scopes' signs, therefore assigned at the end of the function
                cur_scope = end - start
                cur_ratio = cur_num_site/cur_scope
                combi_scopes_ratios_sites.append(["start: " + str(start), "end: " + str(end), "scope: " +str(cur_scope), "ratio: " + str(cur_ratio), "site: " + str(cur_num_site), "chr: " + str(chr)])
    return combi_scopes_ratios_sites

# firstly, extract the best ratio from the combinations' list
# secondly, extract the best ratio from the best ten ratios list which was previously sorted
# compare the two of them
# return the best ratio
def get_best_ratio(n_p_sorted_best_10, combi_scopes_ratios_sites, location_of_site):
    combi_sorted = sorted(combi_scopes_ratios_sites, key=lambda x: float(x[3].split(': ')[1]))
    # extract the last item since the array is increasingly sorted
    best_from_combi = combi_sorted[len(combi_sorted) - 1]
    best_from_best_10 = n_p_sorted_best_10[len(n_p_sorted_best_10) - 1]
    site_best_from_best_10 = int(best_from_best_10[2].split(": ")[1]) 
    scope_best_from_best_10 = int(best_from_best_10[0].split(": ")[1])
    chr_best_from_best_10 = best_from_best_10[3].split(": ")[1]
    # if best scope > 0 
    if scope_best_from_best_10 > 0:
        start_best_from_best_10 = location_of_site - 30
        end_best_from_best_10 = location_of_site + scope_best_from_best_10
    # if best scope < 0 
    if scope_best_from_best_10 < 0:
        start_best_from_best_10 = location_of_site + scope_best_from_best_10
        end_best_from_best_10 = location_of_site + 30
    # compare ratio from the best combi and ratio from the best 10
    if float(best_from_combi[3].split(": ")[1]) >= float(best_from_best_10[1].split(": ")[1]):
        print("return best combi")
        return best_from_combi
    # if the ratio of best from best 10 is bigger
    else:
        print("the ratio of best from best 10 is bigger")
        ratio = float(best_from_best_10[1].split(": ")[1])
        return ["start: " + str(start_best_from_best_10), "end: " + str(end_best_from_best_10), "scope: " + str(scope_best_from_best_10), "ratio: " + str(ratio), "site: " + str(site_best_from_best_10), "chr: " + str(chr_best_from_best_10)]
    # zohar's get_sequence
