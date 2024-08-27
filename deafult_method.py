import math

def get_output_default_tool(dis_list, location_of_site):
    # Call the function based on the default scope
    start, end = default_distance(dis_list, location_of_site)
    return start, end

# If there are no editing sites near the gene of interest
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

    for _, item in enumerate(dis_list):
        dis = item[1]
        if dis > 0 and dis < 10000:
            pos_dis_sum += dis
            num_of_close_pos_sites += 1
        if dis < 0 and dis > -10000:
            neg_dis_sum += dis
            num_of_close_neg_sites += 1

    # There are editing sites from both sides
    if num_of_close_pos_sites > 0 and num_of_close_neg_sites > 0:
        pos_dis_avg = pos_dis_sum / num_of_close_pos_sites
        neg_dis_avg = neg_dis_sum / num_of_close_neg_sites
        start = location_of_site + math.ceil(neg_dis_avg)
        end = location_of_site + math.floor(pos_dis_avg)

    # There are no editing sites on the positive side
    elif num_of_close_pos_sites == 0 and num_of_close_neg_sites > 0:
        print("in pos_dis_num == 0")
        neg_dis_avg = neg_dis_sum / num_of_close_neg_sites
        start = location_of_site + math.floor(neg_dis_avg)
        end = location_of_site + 30

    # There are no editing sites on the negative side
    elif num_of_close_pos_sites > 0 and num_of_close_neg_sites == 0:
        print("in neg_dis_sum == 0")
        pos_dis_avg = pos_dis_sum / num_of_close_pos_sites
        start = location_of_site - 30
        end = location_of_site + math.ceil(pos_dis_avg)

    # Default case where no close sites are found
    else:
        start = location_of_site - 500
        end = location_of_site + 500

    print(f"end - start after default_method {end - start}")
    return start, end
