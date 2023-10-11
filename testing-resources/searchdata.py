""" Data required for search program """

# Created by: Jonathan Pasco-Arnone and Aidan Lalonde-Novales
# Created on: October 2023

# For cycling through the folders
import os
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
    return outgoing_links

def get_incoming_links(URL):
    """ Retrieves the outgoing links to a URL with reference to the seed URL from the crawl"""
    incoming_links = []
    # Cycles through each folder to check the outputs of each one
    for folder in os.listdir(CRAWL_PATH):
        file = open(CRAWL_PATH + "/" + folder + "/title_and_link.txt", "r", encoding="utf8")
        file_link = (file.readlines(0)[1]).strip()
        for link in get_outgoing_links(file_link):
            # If one of the outgoing links is the inputted URL
            # Then add it to the incoming links
            if link.strip() == URL:
                incoming_links.append(file_link.strip())
                break

    # If there are no incoming links then return None
    # The if statement is equivalent to "if incoming_links == []:"
    if not incoming_links:
        return None
    else:
        return incoming_links

def get_page_rank(URL):
    """ Gets the page rank of the url provided """

get_incoming_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html")
