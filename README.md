The tool generates a json with a queue of notes that are meant to be played in sequence with associated durations for each note.

To use this, you must first generate the key file. One is provided but the script I wrote to scrape it from the site I got it from is also included.

Do what you want with this. I used it to make this game:

https://peter-tres.itch.io/



Scrape tool dependencies:
BeautifulSoup
Selenium

MIDI tool dependencies:
pretty_midi

Realistically, MIDIs can be weird a lot of the times I noticed. This only
grabs certain instrument tracks (pianos mainly).

I used the midis from this site mainly: https://bitmidi.com/