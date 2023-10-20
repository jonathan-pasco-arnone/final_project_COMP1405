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
    words = phrase.split()
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
            # Get q vector's tfidf
            # The tf-idf of this value is always -1
            q_vector = abs(math.log(1 + (words.count(word) / len(words)), 2) * -1)
            d_vector = abs(searchdata.get_tf_idf(file_link, word))
            numerator += q_vector * d_vector
            denominator_q += q_vector ** 2
            denominator_d += d_vector ** 2

        # If any of the words are in any of the documents then continue
        if denominator_d != 0:
            # If the boost is applied or not
            if boost:
                cosine_similarity = (searchdata.get_page_rank(file_link) * numerator
                      / (math.sqrt(denominator_q) * math.sqrt(denominator_d)))
            else:
                cosine_similarity = (numerator
                      / (math.sqrt(denominator_q) * math.sqrt(denominator_d)))
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
for dict in search('coconut fig cherry',False):
    print(dict["title"], dict["score"])