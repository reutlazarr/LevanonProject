import create_list_of_distance as l_dis
def get_output_default_tool(dis_list, location_of_site):
    # call the func based on default scope
    start, end = l_dis.default_distance(dis_list, location_of_site)
    return start, end