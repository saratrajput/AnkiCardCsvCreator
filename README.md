# Anki Deck Creator Helper 

It contains a python script and a couple of linux commands to help in quickly
creating Anki decks with embedded pictures.

Best use case scenario is to use song lyrics file as input of target language. 

Here's an example card:

![Example Card](https://github.com/saratrajput/AnkiCardCsvCreator/blob/master/images/lyricVocabExample.png)

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

The following bash commands are to resize the images to 400x300 which reduces
the size of the image and makes them easily viewable.

```bash
$ for file in *
$ do convert $file -resize 400x300 $file
$ done
```

Now, these downloaded images can be copied to collection.media folder.

[How to find collection.media folder](https://superuser.com/questions/963526/where-does-anki-store-media)

## Development
```
$ virtualenv -p <python3Location> <foobar>
$ . foobar/bin/activate
$ pip install -r requirements.txt
```
