""" Search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import json
import math
import os
import searchdata

CRAWL_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data"

def search(phrase, boost):
    """ Determines the top ten searchs for the query inputted """
    all_words = phrase.split()
    # Creates a list with no duplicates of every word in the phrase
    words = list(dict.fromkeys(all_words))
    top_ten = []

    for folder in os.listdir(CRAWL_PATH):
        file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        file_link = (file.readlines(0)[1]).strip()

        # Cosine Similarity
        cosine_similarity = 0.0
        numerator = 0.0
        denominator_q = 0.0
        denominator_d = 0.0
        for word in words:
            tf_q = all_words.count(word) / len(all_words)
            q_value = math.log(1 + tf_q, 2) * searchdata.get_idf(word)
            d_value = searchdata.get_tf_idf(file_link, word)
            numerator += q_value * d_value
            denominator_q += q_value * q_value
            denominator_d += d_value * d_value

        # If any of the words are in any of the documents then continue
        if denominator_d != 0:
            # If the boost is applied or not
            if boost:
                cosine_similarity = (searchdata.get_page_rank(file_link) * numerator / ((denominator_q ** 0.5) * (denominator_d ** 0.5)))
            else:
                cosine_similarity = (numerator / ((denominator_q ** 0.5) * (denominator_d ** 0.5)))
        # Place the new file's cosine similarity into the list in the correct spot
        placement_location = 0
        for index, dictionary in enumerate(top_ten):
            if dictionary["score"] < cosine_similarity:
                placement_location = index
                break
            if len(top_ten) - 1 == index:
                placement_location = len(top_ten)

        # If this cosine similarity is in the top ten
        # Building all the parts of the dictionary
        top_ten.insert(placement_location, {})
        top_ten[placement_location]["url"] = file_link
        file.seek(0)
        top_ten[placement_location]["title"] = file.readlines(0)[0].strip()
        top_ten[placement_location]["score"] = cosine_similarity
        file.close()


    # 10 is the max the list should hold
    counter = len(top_ten) - 10
    while counter > 0:
        del top_ten[:1]
        counter -= 1
    return top_ten

# for dic in search('pear lime pear fig coconut',True):
#     print(dic["title"], dic["score"])