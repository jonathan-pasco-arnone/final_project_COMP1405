""" Matrix methods program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import webdev
# OS is just so I can make folders from inside the program
import os, shutil

def crawl(seed):
    """ Parses the data from the seed provided into a more useful set of files """

    # Clears the data from any previous crawls
    if os.path.exists("/workspaces/final_project_COMP1405/testing-resources/crawler_data"):
        shutil.rmtree("/workspaces/final_project_COMP1405/testing-resources/crawler_data")
    os.mkdir("/workspaces/final_project_COMP1405/testing-resources/crawler_data")
    links = []
    links.append(seed)

    folder_num = 0
    for weblink in links:
        os.mkdir("/workspaces/final_project_COMP1405/testing-resources/crawler_data/" + str(folder_num))
        doc_string = webdev.read_url(weblink)

        # The "edit" variables are use in the following while loop to indicate whether the loop
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
                # Adds the title of the website to a file
                file = open("/workspaces/final_project_COMP1405/testing-resources/crawler_data/" + str(folder_num) + "/page_title.txt", "w")
                file.write(new_key)
                file.close()
                edit_key = False

            # Determines if the current character is within the paragraph section
            if "<p>" == (doc_string[index - 3: index]):
                edit_text = True
            elif "</p>" == (doc_string[index: index + 4]):
                # Adds the text of the website to a file
                file = open("/workspaces/final_project_COMP1405/testing-resources/crawler_data/" + str(folder_num) + "/file_text.txt", "w")
                file.write(new_text)
                file.close()
                edit_text = False

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
                file = open("/workspaces/final_project_COMP1405/testing-resources/crawler_data/" + str(folder_num) + "/page_links.txt", "a")
                file.write(new_link + "\n")
                file.close()

                edit_links = False
                # Will add link if it is not already in the list
                if not (new_link in links):
                    links.append(new_link)
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
    return len(links)

crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")