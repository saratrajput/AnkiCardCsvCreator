# Anki Deck Creator Helper 

It contains a python script and a couple of linux commands to help in quickly
creating Anki decks with embedded pictures.

Best use case scenario is to use song lyrics file as input of target language. 
## Installation

### Requirements
* Linux
* Python 3.3 and up
* NLTK
* google-images-download
* googletrans
* pandas

## Usage

```python
python createVocab.py inputFile.txt knownWords.txt
```

If there are no known words, provide an empty .txt file.

Input language for translator can be changed within createVocab.py.
## Development
```
$ virtualenv -p <python3Location> <foobar>
$ . foobar/bin/activate
$ pip install -r requirements.txt
```
