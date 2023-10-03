""" Matrix methods program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

import webdev

# Dictionary of all documents data
doc_data = {}
links = []

def crawl(seed):
    """ Parses the data from the seed provided as well as all of the connected links """
    doc_data.clear()
    links.append(seed)

    for weblink in links:
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
                edit_key = False

            # Determines if the current character is within the paragraph section
            if "<p>" == (doc_string[index - 3: index]):
                edit_text = True
            elif "</p>" == (doc_string[index: index + 4]):
                edit_text = False
                doc_data[new_key] = new_text

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
    print(len(links))
    print("\n\n\n\n\n")
    print(links)
    print("\n\n\n\n\n")
    return len(links)

crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
print(doc_data)