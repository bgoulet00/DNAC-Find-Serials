# DNAC-Find-Serials
search Cisco DNA Center for serial numbers

# Locating a single serial in the DNAC GUI is a simple tasks but if there are a half dozen or more it can be manually tedious
# This scrip takes an input file serials.csv with a single column A containing serials numbers to search for
# It will search the DNA center inventory for those serials numbers and output the finding to file serials-found.csv
# serials-found.csv will have the serials listed in column A and the device where found in column B
# In addition to the output file, the findings will be printed interactively to the screen

# deleloped with Python 3.6 
