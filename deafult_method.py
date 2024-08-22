import math

def get_output_default_tool(dis_list, location_of_site):
    # call the func based on default scope
    start, end = default_distance(dis_list, location_of_site)
    return start, end

# if there are no editing site of the gene of 
def default_distance(dis_list, location_of_site):
    if len(dis_list) == 1:
        print("SITE OF INTEREST HAS NO SURROUNDING EDITING SITES - default is 1000")
        start = location_of_site - 500
        end = location_of_site + 500
        return start, end
    pos_dis_sum = 0
    num_of_close_pos_sites = 0
    neg_dis_sum = 0
    num_of_close_neg_sites = 0
    # print("loc: " + str(location_of_site))
    # print(f'pos dis {pos_dis_sum}, num of close positive sites: {num_of_close_pos_sites}')
    # print(f'neg dis {neg_dis_sum}, num of close negative sites: {num_of_close_neg_sites}')
    # _ = the item's index, item = the triplet: the current editing site location, the distance from the current editing site location and the chr
    for _, item in enumerate(dis_list):
        dis = item[1]
        if dis > 0 and dis < 10000:
            pos_dis_sum += dis
            num_of_close_pos_sites += 1
        if dis < 0 and dis > -10000:
            neg_dis_sum += dis
            num_of_close_neg_sites += 1
    # there are editing sites from both sides
    if pos_dis_sum != 0 and neg_dis_sum != 0:
        pos_dis_avg = pos_dis_sum / num_of_close_pos_sites
        neg_dis_avg = neg_dis_sum / num_of_close_neg_sites
        start = location_of_site + math.ceil(neg_dis_avg)
        end = location_of_site + math.floor(pos_dis_avg)

    # there are no editing sites in the positive side
    if pos_dis_sum == 0:
        print("in pos_dis_num == 0")
        neg_dis_avg = neg_dis_sum / num_of_close_neg_sites
        start = location_of_site + math.floor(neg_dis_avg)
        end = location_of_site + 20
     # there are no editing sites in the negative side
    if neg_dis_sum == 0:
        print ("in neg_dis_sum == 0")
        pos_dis_avg = pos_dis_sum / num_of_close_pos_sites
        start = location_of_site - 20
        end = location_of_site + math.ceil(pos_dis_avg)
    print(f"end - start after default_method {end - start}")
    return start, end
