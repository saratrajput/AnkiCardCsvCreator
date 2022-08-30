"""
This module reads a txt file (usually made of lyrics) and creates an Anki deck
in the form of a csv file along with images. The images need to be manually
copied to the right location.

Author: Suraj Pattar
"""

import argparse
import logging
import os  # To rename image files
from sys import argv  # For the list of command line arguments passed

import nltk  # For processing text
import pandas as pd  # To create and csv file of newly formed dictionary

# To download images from google image search
from google_images_download import google_images_download
from googletrans import Translator  # To translate words
from nltk.tokenize import RegexpTokenizer  # To tokenize words and remove punctuation


# Initialize logging
log = logging.getLogger(__name__)
# Add filename='example.log' for logging to file
logging.basicConfig(level=logging.DEBUG)


def argument_parser():
    """
    Parse arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("input_path", type=str, help="Path to input text file.")
    parser.add_argument(
        "--known_words",
        type=str,
        default="../data/known_vocab.txt",
        help="Path to known words.",
    )
    return parser.parse_args()


def get_unique_words(file_name):
    """Get a list of unique words from the provided text file"""

    with open(file_name, "r") as f:
        # Read file as one long string
        lines = f.read().replace("\n", " ")

    # Convert to lower case
    lines = lines.lower()

    # Initialize tokenizer to remove punctuation
    tokenizer = RegexpTokenizer(r"\w+")
    lines_tokenized = tokenizer.tokenize(lines)

    # Get unique words
    unique_word_list = list(set(lines_tokenized))
    log.debug("Unique word list: {}".format(unique_word_list))

    return unique_word_list


def read_known_words(file_name):
    """Create a list of known words from the provided text file"""

    with open(file_name) as f:
        known_words = f.read().splitlines()

    return known_words


def translate_words(input_words):
    """Returns a list of English translated words from given input words"""

    translated_words = []
    translator = Translator()
    lang = "es"
    for word in input_words:
        log.debug(word)
        translated = translator.translate(word, src=lang)
        log.debug(translated.text)
        translated_words.append(translated.text)

    translated_words = [x.lower() for x in translated_words]
    return translated_words


def create_dict_df(new_words, translated_words):
    """Create dataframe of Spanish words in one column and English words in
    another column"""

    dictDf = pd.DataFrame({"Spanish": new_words, "English": translated_words})

    return dictDf


def download_images(english_words):
    """Download images from translated words"""

    log.info("Downloading images...")
    response = google_images_download.googleimagesdownload()
    log.debug("Response from download images: {}".format(response))

    for word in english_words:
        arguments = {
            "keywords": word,
            "limit": 1,
            "format": "png",
            "no_directory": "output_directory",
            "prefix": word,
        }  # creating list of arguments
        response.download(arguments)  # passing the arguments to the function


def rename_img_files(img_dir_path):
    """Rename downloaded image files"""

    files = os.listdir(img_dir_path)

    for file in files:

        temp = file.split()
        tempInd = temp.index("1.")
        del temp[tempInd:]

        newName = "".join(temp) + ".png"
        newName = newName.lower()
        os.rename(os.path.join(img_dir_path, file), os.path.join(img_dir_path, newName))


def image_syntax_appender(lyric_df):
    """Add image html syntax to dataframe column"""

    img_file_name = lyric_df.English.str.replace(" ", "")
    english_append = "<img src='" + img_file_name + ".png' />"
    add_space = " <br /> "
    lyric_df["English"] = lyric_df["English"] + add_space + english_append
    return lyric_df


def save_to_csv(lyric_df, output_file_name):
    lyric_df.to_csv(output_file_name + ".csv")


def main(args):
    """
    Implement the main function.
    """
    new_lyric_file = args.input_path
    known_words_file = args.known_words
    # Specify path to images for renaming them later
    img_path = "/home/sp/ankiPython/downloads"
    output_file_name = new_lyric_file.strip(".txt") + "Vocab"  # Name of output dictionary csv

    # Get unique words from input text file
    new_words = get_unique_words(new_lyric_file)
    # Create a list of known words
    known_words_list = read_known_words(known_words_file)

    # Create list of new words not present in known words list
    new_unknown_words = list(set(new_words) - set(known_words_list))

    translated_words = translate_words(new_unknown_words)

    df = create_dict_df(new_unknown_words, translated_words)

    download_images(translated_words)

    # Rename image files so it's easier to append to html syntax of card
    rename_img_files(img_path)

    df = image_syntax_appender(df)

    known_words_list = known_words_list + new_unknown_words

    # Saves the file to be imported later using Anki desktop
    save_to_csv(df, output_file_name)

    # Append the new words to the known words file
    with open(known_words_file, "a") as f:
        for item in new_unknown_words:
            f.write("%s\n" % item)


if __name__ == "__main__":
    args = argument_parser()
    main(args)
