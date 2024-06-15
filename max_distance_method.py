import create_list_of_distance as l_dis

def get_output_max_distance_tool(dis_list, location_of_site):
    if len(dis_list) == 1:
        print("SITE OF INTEREST HAS NO SURROUNDING EDITING SITES")
        return 0, 0
    # call the func based on max distance
    best_by_max_dis = max_distance(dis_list, location_of_site)
    # chr = best_by_max_dis[4].split(": ")[1]
    start = int(best_by_max_dis[0].split(": ")[1])
    end = int(best_by_max_dis[1].split(": ")[1])
    return start, end

# chr added
# [loc, dis, chr]]
# there is a list of tuples for each site of interest. the first part contains the site's loc, the second contains the distance from our site of interest, the third contains the chr's name
# we should extract the maximal distance and return it as our chosen window
# changes: delete our_tuple and add variable of "tuple_sites_of_interest"
def max_distance(dis_list, location_of_site):
    max_tuple = max(dis_list, key= lambda x: x[1])
    min_tuple = min(dis_list, key= lambda x: x[1])
    max_scope = max_tuple[1]
    min_scope = min_tuple[1]
    if max_scope > 0 and min_scope > 0:
        start = location_of_site
        end = location_of_site + max_scope
        site = find_num_of_sites_in_scope(dis_list, max_scope)
    elif max_scope < 0 and min_scope < 0:
        start = location_of_site + min_scope
        end = location_of_site
        site = find_num_of_sites_in_scope(dis_list, min_scope)
    elif max_scope > 0 and min_scope < 0:
        start = location_of_site + min_scope
        end = location_of_site + max_scope
        site = find_num_of_sites_in_scope(dis_list, max_scope) + find_num_of_sites_in_scope(dis_list, min_scope)
    elif max_scope == 0:
        start = location_of_site + min_scope
        end = location_of_site
        site = find_num_of_sites_in_scope(dis_list, min_scope)
    elif min_scope == 0:
        start = location_of_site
        end = location_of_site + max_scope
        site = find_num_of_sites_in_scope(dis_list, max_scope)
    else:
        # max_scope < 0 and min_scope > 0
        raise Exception("ERROR: MIN SCOPE CAN'T BE BIGGER THAN MAX SCOPE!!!")
    scope = end - start
    chr = str(max_tuple[2])
    # site == num of sites in the current scope
    return ["start: " + str(start), "end: " + str(end), "scope: " + str(scope), "site: " + str(site), "chr: " + str(chr)]

# new
def find_num_of_sites_in_scope(dis_list, scope):
    # scope is positive (loc_site_of_interest is before site)
    # find the index of the current site
    ind_of_dis_zero = [dis_list.index(tupl) for tupl in dis_list if tupl[1] == 0]
    ind_of_cur_scope = [dis_list.index(tupl) for tupl in dis_list if tupl[1] == scope]
    # site == num of sites
    # print(dis_list)
    # print("ind_of_dis_zero ")
    # print(ind_of_dis_zero)

    # print("ind_of_dis_zero[0] " + ind_of_dis_zero[0])
    # print("ind_of_cur_scope ")
    # print(ind_of_cur_scope)
    # print("ind_of_cur_scope[0] " + ind_of_cur_scope[0])
    site = abs(int(ind_of_cur_scope[0]) - int(ind_of_dis_zero[0]))
    return site
