# -*- coding: utf-8 -*-
"""
The goal of the script is to get a standard variable based on the strings in the input_name_list. 
The standard varaible name requires the string lower case with underscores connecting words. 
The difficulty lies that the strings in the input_name_list contains special characters, such as [m/s], |


"""




import re
input_name_list = ["Horn", "Velocity[m/s]","FNR","Status|Engine on"]
input_name_list_ = []
for input_name in input_name_list: 
    input_name = input_name.split("[")[0] # remove the unit by removing the part after [
    input_name = re.sub('[^a-zA-Z0-9]',"_",input_name) # subtitute all the special charaters with the underscore
    if input_name.isupper():
        # Keep the call capital word
        input_name_list_.append(input_name)# Add it into the list
    else:
        input_name = input_name.lower() # Convert the capital word into lower case 
        input_name_list_.append(input_name)
print (input_name_list_)
    #print(input_name)
    
