""" Data required for search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import json
import os
import math
import matmult

CRAWL_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data"

def get_outgoing_links(URL):
    """ Retrieves the outgoing links from a URL """
    outgoing_links = None

    file = open(CRAWL_PATH + "/../link_locations.txt", "r", encoding="utf8")
    link_dict = json.load(file)
    
    if link_dict.get(URL) is not None:
        main_file = open(CRAWL_PATH + "/" + str(link_dict[URL]) + "/page_links.txt", "r", encoding="utf8")
        outgoing_links = main_file.readlines()

    if outgoing_links is not None:
        index = 0
        while index != len(outgoing_links):
            outgoing_links[index] = outgoing_links[index].strip()
            index += 1

    return outgoing_links

def get_incoming_links(URL):
    """ Retrieves the outgoing links to a URL with reference to the seed URL from the crawl """
    incoming_links = None

    file = open(CRAWL_PATH + "/../link_locations.txt", "r", encoding="utf8")
    link_dict = json.load(file)
    
    if link_dict.get(URL) is not None:
        main_file = open(CRAWL_PATH + "/" + str(link_dict[URL]) + "/incoming_links.txt", "r", encoding="utf8")
        incoming_links = main_file.readlines()

    if incoming_links is not None:
        index = 0
        while index != len(incoming_links):
            incoming_links[index] = incoming_links[index].strip()
            index += 1

    return incoming_links

def get_page_rank(URL):
    """ Gets the page rank of the url provided """
    # Gets all the links
    file = open(CRAWL_PATH + "/../link_locations.txt", "r", encoding="utf8")
    links = json.load(file)
    if links.get(URL) is None:
        return -1

    # Check if the page ranks have already been calculated
    if os.path.exists(CRAWL_PATH + "/../" + "page_rank_file.txt"):
        all_ranks_file = open(CRAWL_PATH + "/../" + "page_rank_file.txt", "r")
        ranks = json.load(all_ranks_file)
        return ranks[0][links[URL]]

    else:
        # The main matrix of the problem
        probability_matrix = []
        basic_vector = [[]]
        alpha = 0.1

        # Generates the amount of rows needed (aka the amount of websites attached to the seed)
        counter = 0
        while counter != len(os.listdir(CRAWL_PATH)):
            probability_matrix.append([])
            basic_vector[0].append(0)
            counter += 1

        if links.get(URL) is None:
            return -1

        basic_vector[0][0] = 1

        # Fills out the probability matrix with all the values
        for index, key in enumerate(links.keys()):
            incoming_links = get_incoming_links(key)
            chance_per_page = 1 / len(incoming_links)
            probability_matrix[index].extend(len(os.listdir(CRAWL_PATH))
                * [alpha / len(os.listdir(CRAWL_PATH))])

            for website in incoming_links:
                probability_matrix[index][links[website]] = (chance_per_page
                    * (1 - alpha) + alpha / len(os.listdir(CRAWL_PATH)))

        vector_b = [[]]
        euclidean_distance = 1
        # Euclidean distance testor
        while euclidean_distance > 0.0001:
            vector_b = basic_vector
            basic_vector = matmult.mult_matrix(basic_vector, probability_matrix)
            euclidean_distance = matmult.euclidean_dist(vector_b, basic_vector)
        
        page_rank_file = open(CRAWL_PATH + "/../" + "page_rank_file.txt", "w")
        json.dump(basic_vector, page_rank_file)
        page_rank_file.close()

        return basic_vector[0][links[URL]]

def get_idf(word):
    """ gets the inverse document frequency of the word provided """
    # Gets all the links
    file = open(CRAWL_PATH + "/../idf.txt", "r", encoding="utf8")
    idf_values = json.load(file)
    if idf_values.get(word) is None:
        return 0
    return math.log((len(os.listdir(CRAWL_PATH)) / (1 + idf_values[word])), 2)

def get_tf(URL, word):
    """ gets the term frequency of the word provided in the document provided """
    # initialize variables
    total_words = 0
    time_word_appears = 0
    folder_num = -1

    file = open(CRAWL_PATH + "/../link_locations.txt", "r", encoding="utf8")
    link_dict = json.load(file)

    if link_dict.get(URL) is not None:
        folder_num = link_dict[URL]

    # returns 0 if folder_num was not found
    if folder_num == -1:
        return 0

    with open(CRAWL_PATH + "/" + str(folder_num) + "/file_text.txt", 'r', encoding="utf8") as file:
        # make a list of all the words in the file
        word_list = file.read().split()
        # get total number of words in document
        total_words = len(word_list)
        # get number of times word appears in document
        time_word_appears = word_list.count(word)

    # return number of times word appears in document / total number of words in document
    return time_word_appears / total_words

def get_tf_idf(URL, word):
    """ Gets the tf-idf weight of the word provided in the document provided """
    return math.log((1 + get_tf(URL, word)), 2) * get_idf(word)
