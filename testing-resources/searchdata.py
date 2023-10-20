""" Data required for search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

# For cycling through the folders
import os
import math
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
            break
    if outgoing_links != None:
        for index in range(len(outgoing_links)):
            outgoing_links[index] = outgoing_links[index].strip()

    return outgoing_links

def get_incoming_links(URL):
    """ Retrieves the outgoing links to a URL with reference to the seed URL from the crawl """
    incoming_links = None
    # Cycles through each folder to check the outputs of each one
    for folder in os.listdir(CRAWL_PATH):
        current_file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        link = (current_file.readlines(0)[1]).strip()

        # If the title and link file is the same as the inputed link
        # Then it is the right folder
        if link == URL:
            link_file = open(CRAWL_PATH + "/" + folder + "/incoming_links.txt", "r", encoding="utf8")
            incoming_links = link_file.readlines()
            break

    if incoming_links != None:
        for index in range(len(incoming_links)):
            incoming_links[index] = incoming_links[index].strip()
    
    return incoming_links

def get_page_rank(URL):
    """ Gets the page rank of the url provided """
    # The main matrix of the problem
    probability_matrix = []
    basic_vector = [[]]
    alpha = 0.1

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
        probability_matrix[index].extend(len(os.listdir(CRAWL_PATH)) * [alpha / len(os.listdir(CRAWL_PATH))])

        for website in incoming_links:
            probability_matrix[index][links[website]] = chance_per_page * (1 - alpha) + alpha / len(os.listdir(CRAWL_PATH))

    vector_b = [[]]
    euclidean_distance = 1
    # Euclidean distance testor
    while euclidean_distance > 0.0001:
        vector_b = basic_vector
        basic_vector = matmult.mult_matrix(basic_vector, probability_matrix)
        euclidean_distance = matmult.euclidean_dist(vector_b, basic_vector)

    return basic_vector[0][links[URL]]

def get_idf(word):
    """ gets the inverse document frequency of the word provided """
    # initialize variables
    total_docs = 0
    docs_with_word = 0

    # get total number of documents
    for folder in os.listdir(CRAWL_PATH):
        file = open(CRAWL_PATH + "/" + folder + "/file_text.txt", "r", encoding="utf8")
        total_docs += 1
        # get 1 + total number of documents that word appears in
        if word in file.read():
            docs_with_word += 1
        # close file (good practice)
        file.close()

    # return 0 if word doesn't appear, else return
    # log base two of total docs / 1 + docs with word
    if docs_with_word == 0:
        return 0
    return math.log((total_docs / (1 + docs_with_word)), 2)

def get_tf(word, URL):
    """ gets the term frequency of the word provided in the document provided """
    # initialize variables
    total_words = 0
    time_word_appears = 0
    folder_num = -1

    # create a lsit for crawler_data folders and sort it (using lamba algorithm)
    dir_search = sorted(os.listdir(CRAWL_PATH), key=lambda x: int(x))

    # get the matching file_text.txt for the url
    for count in dir_search:
        file = open(CRAWL_PATH + "/" + str(count) + "/title_and_link.txt", "r", encoding="utf8")
        line = file.readlines()
        if (line[1].strip()) == URL:
            folder_num = count
            break
        file.close()

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

def get_tf_idf(word, URL):
    """ Gets the tf-idf weight of the word provided in the document provided """
    return math.log((1 + get_tf(word, URL)), 2) * get_idf(word)

print(get_page_rank("http://people.scs.carleton.ca/~davidmckenney/fruits/N-56.html"))
print("Should be 0.001455568622482555")
# print(get_page_rank("https://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))