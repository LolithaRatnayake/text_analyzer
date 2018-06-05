#!/usr/bin/env python3
import argparse
import re
import os


def parse_file(filename, black_list=[]):
    """Read the file and returns a dictionary of words used in the file.
    Optionally can give list of words to omit the analysis

    Keyword arguments:
    filename -- name of the file that needs to be read
    black_list -- list of words to exclude from the analysis
    """

    words = {}

    #adds empty search results, single quote without letters around it to black_list
    black_list.extend(['',"'"])
    try:
        with open(filename) as f:
            #iterating the file line by line and parse to reduce memory consumption when reading large files
            for line in f:
                #executes a regular expression to filter out words. Used \' to get words like "we'll".
                #Didn't use "\w" metacharacter because it includes 0-9 and _ (only parsing simple english words). 
                temp_list = re.findall(r'([a-zA-Za\']+)',line)
                for word in temp_list:
                    #omits words from black_list
                    if word not in black_list:
                        if word in words.keys():
                            words[word] += 1
                        else:
                            words[word] = 1

    except IOError:
        print("reading {} has failed!".format(filename))
        raise
    return words


def transpose(source_dic, min_frequency=1):
    """Transpose the given dictionary key values.
    It can omit the source dictionary values that are less than the given min_frequency.
    Return the new dictionary

    Keyword arguments:
    source_dic -- dictionary that needs to be transposed
    min_frequency -- Minimum boundary of occurance to show (default value is 1)
    """

    transposed = {}

    for key in source_dic.keys():
        value = source_dic[key] #assigned to variable to reduce multiple lookup in dictionary
        if value >= min_frequency :
            if value in transposed.keys():
                transposed[value].append(key)
            else:
                transposed[value] = [key,]

    return transposed

def print_dictionary(frequency_dic):
    """Prints out dictionary in degrading order by keys

    Keyword arguments:
    frequency_dic -- dictionary that needs to be printed
    """
    for index in sorted(frequency_dic, reverse=True):
        print("\"{}\" word(s) has occured {} times in the text".format(",".join(frequency_dic[index]), index))


def extract_black_list(filename):
    """extract key words to be blacklisted from given text file that each word is seperated by comma

    Keyword arguments:
    filename -- file that contains blacklisted words
    """
    try:
        with open(filename) as f:
            #used list comprehension as it is a simple function
            #used strip method to avoid \n characters
            return [word.strip() for line in f.readlines() for word in line.split(',')]

    except IOError:
        print("reading {} has failed!".format(filename))
        raise

def validate_filepath(filepath):
    """Throws exception if given filepath is not valid

    Keyword arguments:
    filepath -- file path to be validated
    """
    if not os.path.exists(filepath):
        raise ValueError("File doesn't exists!")
        if not os.path.isfile(filepath):
            raise ValueError("Given file name is not a file. Perhaps it might be a directory.")
            if not os.access(filepath, os.R_OK):
                raise ValueError("Given file doesn't have read permission!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a given text and print out the frequency of words.\n\r' \
                                     +'Optionally can omit words in given comma seperated text file and mention lower limit of the frequency of words. \n\n\r' \
                                     +'Usage : python parser.py name_of_the_text.txt --min_occur 2 --blacklist_file blacklist.txt')
    parser.add_argument("text_file", help="File path with file name that you need to parse.")
    parser.add_argument("--min_occur", type=int, help='Minimum occurances of a single words to be reported.', default=1)
    parser.add_argument("--blacklist_file", help='File path with name that contains the list of words sperated by commas to avoid analysing.', default=None)
    args = parser.parse_args()

    validate_filepath(args.text_file)
    if args.blacklist_file:
        validate_filepath(args.blacklist_file)
        blacklist = extract_black_list(args.blacklist_file)
        parsed_txt = parse_file(args.text_file, blacklist)
        to_print = transpose(parsed_txt, args.min_occur)
        print_dictionary(to_print)

    else:
        parsed_txt = parse_file(args.text_file)
        to_print = transpose(parsed_txt, args.min_occur)
        print_dictionary(to_print)
    
