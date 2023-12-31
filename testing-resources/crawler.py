""" Web crawling method program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import json
# OS is just so I can make folders from inside the program
import os
import webdev

# constant so I don't have to type out the path every time
CRAWL_PATH = "/workspaces/final_project_COMP1405/testing-resources/crawler_data/"

def crawl(seed):
    """ Parses the data from the seed provided into a more useful set of files """

    # Clears the data from any previous crawls
    if os.path.exists(CRAWL_PATH):
        for folder in os.listdir(CRAWL_PATH):
            for file in os.listdir(CRAWL_PATH + str(folder)):
                os.remove(CRAWL_PATH + str(folder) + "/" + str(file))
            os.rmdir(CRAWL_PATH + str(folder))
        os.rmdir(CRAWL_PATH)
    if os.path.exists("/workspaces/final_project_COMP1405/testing-resources/page_rank_file.txt"):
        os.remove("/workspaces/final_project_COMP1405/testing-resources/page_rank_file.txt")
    if os.path.exists("/workspaces/final_project_COMP1405/testing-resources/idf.txt"):
        os.remove("/workspaces/final_project_COMP1405/testing-resources/idf.txt")
    if os.path.exists("/workspaces/final_project_COMP1405/testing-resources/link_locations.txt"):
        os.remove("/workspaces/final_project_COMP1405/testing-resources/link_locations.txt")

    os.mkdir(CRAWL_PATH)
    link_locations = {}
    link_locations[seed] = 0
    links = []
    links.append(seed)

    word_per_doc = {}

    folder_num = 0
    for weblink in links:
        # Make a new folder for the new link
        os.mkdir(CRAWL_PATH + str(folder_num))
        doc_string = webdev.read_url(weblink)

        # The "edit" variables are used in the following while loop to indicate whether the loop
        # should start/end adding to the title/text/link of the new key/paragraph/url
        edit_key = False
        edit_text = False
        edit_links = False
        new_key = ""
        new_text = ""
        new_link = ""
        index = 0
        while index != len(doc_string):

            # Determines if the current character is within the title section
            if "<title>" == (doc_string[index - 7: index]):
                edit_key = True
            elif "</title>" == (doc_string[index: index + 8]):
                # Adds the title and link of the website to a file
                file = open(CRAWL_PATH + str(folder_num)
                            + "/title_and_link.txt", "w", encoding="utf8")
                file.write(new_key + "\n" + weblink + "\n")
                file.close()
                edit_key = False

            # Determines if the current character is within the paragraph section
            if "<p>" == (doc_string[index - 3: index]):
                edit_text = True
            elif "</p>" == (doc_string[index: index + 4]):
                # Adds the text of the website to a file
                file = open(CRAWL_PATH + str(folder_num)
                            + "/file_text.txt", "w", encoding="utf8")
                file.write(new_text)
                file.close()
                edit_text = False

                # Creates a list with no duplicates of every word in the file
                all_words = list(dict.fromkeys(new_text.split()))
                for word in all_words:
                    if word_per_doc.get(word) is None:
                        word_per_doc[word] = 1
                    else:
                        word_per_doc[word] += 1

            # Determines if the current character is the start of a link
            if "<a href=\"" == (doc_string[index - 9: index]):
                edit_links = True

                # Goes through each character in the link backwards until it finds the source link
                # Aka it will erase each character at the end of the url until it reaches a /
                new_link += weblink
                new_link_index = len(new_link) - 1
                while new_link_index >= 0:
                    if new_link[new_link_index] == "/":
                        break
                    new_link = new_link[:len(new_link) - 1]
                    new_link_index -= 1

                # Checks if the link is a relative link
                # If so, then skip the ./ of the link
                if doc_string[index: index + 2] == "./":
                    index += 2

            # If the link is at the end AND the link is currently be generated
            # then the new link will stop generating
            elif "\">" == (doc_string[index: index + 2]) and edit_links:

                # Adds the links of the website to a file
                # The use of "a" instead of "w" is so that I can add additional links instead of
                # just overwriting the whole document every time
                file = open(CRAWL_PATH + str(folder_num)
                      + "/page_links.txt", "a", encoding="utf8")
                file.write(new_link + "\n")
                file.close()

                edit_links = False
                # Will add link if it is not already in the list
                if new_link not in links:
                    links.append(new_link)
                    link_locations[new_link] = len(links) - 1
                new_link = ""

            if edit_links:
                new_link += doc_string[index]


            # Adds to the key and values
            if edit_key:
                new_key += doc_string[index]
            if edit_text:
                new_text += doc_string[index]

            index += 1
        folder_num += 1

    # Adds the incoming links file
    for folder in os.listdir(CRAWL_PATH):
        current_link_file = open(CRAWL_PATH + str(folder)
              + "/title_and_link.txt", "r", encoding="utf8")
        current_link = current_link_file.readlines()[1].strip()
        file = open(CRAWL_PATH + str(folder) + "/page_links.txt", "r", encoding="utf8")
        outgoing_links = file.readlines()
        for next_link in outgoing_links:
            # Adds incoming link
            incoming_link_file = open(CRAWL_PATH + str(link_locations[current_link])
                + "/incoming_links.txt", "a", encoding="utf8")
            incoming_link_file.write(next_link)

        current_link_file.close()
        file.close()
    
    # Puts the dictionary into a file
    link_locations_file = open(CRAWL_PATH + "../" + "link_locations.txt", "w")
    json.dump(link_locations, link_locations_file)
    link_locations_file.close()

    idf_file = open(CRAWL_PATH + "../" + "idf.txt", "w")
    json.dump(word_per_doc, idf_file)
    idf_file.close()

    return len(links)
