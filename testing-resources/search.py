""" Search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import os
import searchdata

CRAWL_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data"

def search(phrase, boost):
    """ Determines the top ten searchs for the query inputted """
    # Makes the file with all the inputed words
    word_file = open(CRAWL_PATH + "/../search_words.txt", "w+", encoding="utf8")
    word_file.writelines(phrase)
    word_file.seek(0)

    words = phrase.split()

    top_ten = []
    for folder_num, folder in enumerate(os.listdir(CRAWL_PATH)):
        file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        top_ten.append({})
        file_link = (file.readlines(0)[1]).strip()
        top_ten[folder_num]["url"] = file_link # File link
        file.seek(0) # Go back to the top of the file
        top_ten[folder_num]["title"] = (file.readlines(0)[0]).strip() # File title


        # Cosine Similarity
        numerator = 0
        denominator = 0
        for word in words:
            d_vector = searchdata.get_tf_idf(word, file_link)
            q_vector = searchdata.get_tf_idf(word, CRAWL_PATH + "/../search_words.txt")
            numerator += q_vector * d_vector
    


        



search("apple banana", True)