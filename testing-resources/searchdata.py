""" Data required for search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

# For cycling through the folders
import os
import matmult

CRAWL_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data"

def get_outgoing_links(URL):
    """ Retrieves the outgoing links from a URL """
    outgoing_links = None
    for folder in os.listdir(CRAWL_PATH):
        current_file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        link = (current_file.readlines(0)[1]).strip()

        # If the title and link file is the same as the inputed link
        # Then it is the right folder
        if link == URL:
            link_file = open(CRAWL_PATH + "/" + folder + "/page_links.txt", "r", encoding="utf8")
            outgoing_links = link_file.readlines()
    return outgoing_links

def get_incoming_links(URL):
    """ Retrieves the outgoing links to a URL with reference to the seed URL from the crawl"""
    incoming_links = []
    # Cycles through each folder to check the outputs of each one
    for folder in os.listdir(CRAWL_PATH):
        file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        file_link = (file.readlines(0)[1]).strip()
        for link in get_outgoing_links(file_link):
            # If one of the outgoing links is the inputted URL
            # Then add it to the incoming links
            if link.strip() == URL:
                incoming_links.append(file_link.strip())
                break

    # If there are no incoming links then return None
    # The if statement is equivalent to "if incoming_links == []:"
    if not incoming_links:
        return None
    else:
        return incoming_links

def get_page_rank(URL):
    """ Gets the page rank of the url provided """
    # The main matrix of the problem
    probability_matrix = []
    basic_vector = [[]]

    # Holds each link as the key
    # Holds each value as the row in the matrix
    links = {}

    # Generates the amount of rows needed (aka the amount of websites atatched to the seed)
    for folder in os.listdir(CRAWL_PATH):
        file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        file_link = (file.readlines(0)[1]).strip()
        links[file_link] = len(probability_matrix)
        probability_matrix.append([])
        basic_vector[0].append(0)
    
    if links.get(URL) is None:
        return -1
    
    basic_vector[0][0] = 1

    # Fills out the probability matrix with all the values
    for index, key in enumerate(links.keys()):
        incoming_links = get_incoming_links(key)
        chance_per_page = 1 / len(incoming_links)

        for website in links.keys():
            if website in incoming_links:
                probability_matrix[index].append(chance_per_page)
            else:
                probability_matrix[index].append(0)
    
    alpha = 0.1

    # Multiiply matrix by 1 - alpha 
    probability_matrix = matmult.mult_scalar(probability_matrix, 1 - alpha)

    # Add probability matrix with a matrix of equal size that has a 1 in (amount of rows) value
    # This second matrix will be multiplied by alpha
    for row_index, row in enumerate(probability_matrix):
        for column_index, value in enumerate(row):
            probability_matrix[row_index][column_index] += + alpha / len(probability_matrix)
    
    vector_b = [[]]
    euclidean_distance = 1
    # Euclidean distance testor
    while euclidean_distance > 0.0001:
        vector_b = basic_vector
        basic_vector = matmult.mult_matrix(basic_vector, probability_matrix)
        euclidean_distance = matmult.euclidean_dist(vector_b, basic_vector)
    
    return basic_vector[0][links[URL]]


print(get_page_rank("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html"))
