#!/usr/bin/python
from googletrans import Translator # To translate words
import pandas as pd # To create and csv file of newly formed dictionary
import nltk # For processing text
from nltk.tokenize import RegexpTokenizer # To tokenize words and remove punctuation
# To download images from google image search
from google_images_download import google_images_download
import os # To rename image files

from sys import argv # For the list of command line arguments passed
script, newLyricFile, knownWordsFile = argv

def GetUniqueWords(fileName):
    """Get a list of unique words from the provided text file"""
    
    with open(fileName, "r") as f:
        # Read file as one long string
        lines = f.read().replace('\n', ' ')
    
    # Convert to lower case
    lines = lines.lower()

    # Initialize tokenizer to remove punctuation
    tokenizer = RegexpTokenizer(r'\w+')
    linesTokenized = tokenizer.tokenize(lines)

    # Get unique words
    uniqueWordList = list(set(linesTokenized))
    
    return uniqueWordList


def ReadKnownWords(fileName):
    """Create a list of known words from the provided text file"""
    
    with open(fileName) as f:
        knownWords = f.read().splitlines()
        
    return knownWords


def TranslateWords(inputWords):
    """Returns a list of English translated words from given input words"""
    
    translatedWords = []
    translator = Translator();
    lang = 'es'
    for words in inputWords:
        translated = translator.translate(words, src=lang)
        translatedWords.append(translated.text)

    translatedWords = [x.lower() for x in translatedWords]
    return translatedWords


def CreateDictDf(newWords, translatedWords):
    """Create dataframe of Spanish words in one column and English words in 
    another column"""
    
    dictDf = pd.DataFrame(
    {'Spanish': newWords,
     'English': translatedWords
    })
    
    return dictDf


def DownloadImages(englishWords):
    """Download images from translated words"""

    response = google_images_download.googleimagesdownload() 

    for words in englishWords:
        arguments = {"keywords":words,"limit":1, "format":"png",
                     "no_directory":"output_directory", "prefix":words}   #creating list of arguments
        response.download(arguments)   #passing the arguments to the function


def RenameImgFiles(imgDirPath):
    """Rename downloaded image files"""
    
    files = os.listdir(imgDirPath)

    for file in files:

        temp = file.split()
        tempInd = temp.index('1.')
        del temp[tempInd:]

        newName = "".join(temp) + '.png'
        newName = newName.lower()
        os.rename(os.path.join(imgDirPath, file), os.path.join(imgDirPath, newName))


def ImgSyntaxAppender(lyricDf):
    """Add image html syntax to dataframe column"""
    
    imgFileName = lyricDf.English.str.replace(' ', '')
    englishAppend = "<img src='" + imgFileName + ".png' />"
    addSpace = " <br /> "
    lyricDf['English'] = lyricDf['English'] + addSpace + englishAppend
    return lyricDf


def SaveToCsv(lyricDf, outputFileName):
    lyricDf.to_csv(outputFileName + '.csv')

if __name__ == '__main__':
   
    # Specify path to images for renaming them later
    imgPath = '/home/sp/ankiPython/downloads'
    outputDf = newLyricFile.strip('.txt') + 'Vocab' # Name of output dictionary csv

    # Get unique words from input text file
    newWords = GetUniqueWords(newLyricFile)
    # Create a list of known words
    knownWordsList = ReadKnownWords(knownWordsFile)
    
    # Create list of new words not present in known words list 
    newUknWords = list(set(newWords) - set(knownWordsList))

    translatedWords = TranslateWords(newUknWords)

    df = CreateDictDf(newUknWords, translatedWords)

    DownloadImages(translatedWords)

    # Rename image files so it's easier to append to html syntax of card 
    RenameImgFiles(imgPath)

    df = ImgSyntaxAppender(df)

    knownWordsList = knownWordsList + newUknWords

    # Saves the file to be imported later using Anki desktop
    SaveToCsv(df, outputDf)

    # Append the new words to the known words file
    with open(knownWordsFile, 'a') as f:
        for item in newUknWords:
            f.write("%s\n" % item)
