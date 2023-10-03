""" Matrix methods program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import webdev

# Dictionary of all documents data
doc_data = {}
links = []
doc_string = ""

def crawl(seed):
    doc_data.clear()
    doc_string = webdev.read_url(seed)
    if doc_string == "":
        return 0
    
    print(doc_string)

    # Used in the following while loop to indicate whether the while loop should start
    # adding to the string that represents a new link
    edit_links = False
    new_link = ""
    current_index = 0
    while current_index != len(doc_string):
        # Determines if the current character is the start of a link
        if "<a href=\"" == (doc_string[current_index - 9: current_index]):
            edit_links = True
        # If the link is at the end AND the link is currently be generated
        # then the new link will stop generating
        elif "\">" == (doc_string[current_index: current_index + 2]) and edit_links:
            edit_links = False
            links.append(new_link)
            new_link = ""
        
        if edit_links:
            new_link += doc_string[current_index]
        current_index += 1
    print(links)



    edit_key = False # Used in the following while loop to indicate whether the while loop should start adding to the title of the new key
    edit_text = False
    index = 0
    new_key = ""
    new_text = ""
    while index != len(doc_string):

        # Determines if the current character is within the title section
        if "<title>" == (doc_string[index - 7: index]):
            edit_key = True
        elif "</title>" == (doc_string[index: index + 8]):
            edit_key = False

        # Determines if the current character is within the paragraph section
        if "<p>" == (doc_string[index - 3: index]):
            edit_text = True
        elif "</p>" == (doc_string[index: index + 4]):
            edit_text = False

        # Adds to the key and values
        if edit_key:
            new_key += doc_string[index]
        if edit_text:
            new_text += doc_string[index]

        index += 1
    
    return 5

crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")