""" Search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import os
import searchdata

CRAWL_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data"
SEARCH_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data/search_words"

def search(phrase, boost):
    """ Determines the top ten searchs for the query inputted """

    # Creates temporary folder for the words to be held in
    os.mkdir(SEARCH_PATH)
    seacrh_title = open(SEARCH_PATH + "/title_and_link.txt", "w+", encoding="utf8")
    # This is so the search data program can access the data for tf-idf calculations
    seacrh_title.write(" \nsearch")
    seacrh_title.close()
    
    # Makes the file with all the inputed words
    word_file = open(SEARCH_PATH + "/file_text.txt", "w+", encoding="utf8")
    word_file.writelines(phrase)
    word_file.close()    

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
            q_vector = searchdata.get_tf_idf(word, "search")
            numerator += q_vector * d_vector
    
    # Removes the temporary directory and all the files included
    if os.path.exists(SEARCH_PATH):
        for file in os.listdir(SEARCH_PATH):
            os.remove(SEARCH_PATH + "/" + str(file))
        os.rmdir(SEARCH_PATH)
    


        



search("apple banana", True)