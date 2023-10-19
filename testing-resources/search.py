""" Search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import math
import os
import searchdata

CRAWL_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data"

def search(phrase, boost):
    """ Determines the top ten searchs for the query inputted """
    words = phrase.split()

    top_ten = []
    for folder_num, folder in enumerate(os.listdir(CRAWL_PATH)):
        file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        file_link = (file.readlines(0)[1]).strip()

        cosine_similarity = 0.0
        numerator = 0.0
        denominator_q = 0.0
        denominator_d = 0.0
        # Cosine Similarity
        for word in words:
            # Get q vector's tfidf
            # The idf of this value is always 1/2, so the log base 2 of 1/2 = -1
            q_vector = math.log(words.count(word) / len(words), 2) * -1
            d_vector = searchdata.get_tf_idf(word, file_link)
            numerator += q_vector * d_vector
            denominator_q += q_vector ** 2
            denominator_d += d_vector **2
        
        # If any of the words are in any of the documents then continue
        if denominator_d != 0:
            # If the boost is applied or not
            if boost:
                cosine_similarity = (searchdata.get_page_rank(file_link) * numerator / (math.sqrt(denominator_q) * math.sqrt(denominator_d)))
            else:
                cosine_similarity = (numerator / (math.sqrt(denominator_q) * math.sqrt(denominator_d)))

        # Place the new files cosine similarity into the list in the correct spot
        highest_index = 0
        lowest_index = len(top_ten) - 1

        midpoint = int(lowest_index / 2)
        full_range = lowest_index - highest_index + 1
        print("Full range", full_range)

        while full_range > 1:
            full_range = lowest_index - highest_index

            # If the new cosine similarity is greater than or equal to the current one on the list
            if top_ten[midpoint]["score"] <= cosine_similarity:
                lowest_index = midpoint

            # If the value is greater than the middle of the list
            else:
                lowest_index = midpoint

            # Calculates the midpoint of the range (rounded down)
            midpoint = int((highest_index + lowest_index) / 2)
            print("midpoint", midpoint)

        # Does the final check to see if it should go on the top of of the list
        # ie. the midpoint is a the top currently
        # if top_ten[midpoint]["score"] < cosine_similarity:
        #     midpoint += 1

        top_ten.insert(midpoint, {})
        top_ten[midpoint]["url"] = file_link
        file.seek(0)
        top_ten[midpoint]["title"] = file.readlines(0)[0].strip()
        top_ten[midpoint]["score"] = cosine_similarity
        print(file_link)
        print("\n\n\n")
        for row in top_ten:
            print(row)
        print("\n\n\n")
        



    return top_ten
    


        



search("apple banana grape fig", True)