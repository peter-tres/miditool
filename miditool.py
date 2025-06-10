import pretty_midi
from collections import Counter
import os
import re
import json
import math
import glob

# Ensures the english note from the key.txt is stripped of anything
# extra we may have scraped.
def cleanup_english_note(s: str):
    split_idx = s.find('/')
    if split_idx > -1:
        s = s[split_idx+1::]
    s = s[0:3]
    s = re.sub('[^0-9a-zA-Z]+', '', s)
    s = "".join(s.split())
    return s


def add_to_songs_file(file):
    file_name = os.path.splitext(file)[0]

    with open("key.txt") as f:
        data = f.read()



    data = data.split('\n')
    data = [d.split('\t') for d in data]

    # Remove title header from key.txt
    data.pop(0)

    # Create mapping of key -> piano note and the note in plain english
    midi_note_mapping = {int(d[0]):[d[1], cleanup_english_note(d[2])] for d in data if len(d) > 3}

    midi_data = pretty_midi.PrettyMIDI(file)


    # Grab data from MIDI file.
    notes_and_timings = []
    durations = []
    for instrument in midi_data.instruments:
        if instrument.name == "Piano":
            for note in instrument.notes:
                pitch, timing = note.pitch, note.start
                notes_and_timings.append([pitch,timing])

                duration = note.end-note.start
                durations.append([duration,timing])


    # Sorting  the notes and timings seems strange right?
    # Since we're grabbing notes from the MIDI file directly you'd think
    # they'd already be in order! But actually, they're not always.
    # It's odd and likely some floating point error.
    # This is for sanity reasons.

    notes_sorted = sorted(notes_and_timings, key=lambda nt: nt[1])
    durations_sorted = sorted(durations,key=lambda nt:nt[1])
    

    only_notes = [note[0] for note in notes_sorted]
    only_durations = [duration[0] for duration in durations_sorted]

    # Build final sequence for export.
    final_sequence = [midi_note_mapping[note][1] for note  in only_notes]


    # Add song to json but preserve the songs that have already
    # been generated.
    song_name = file_name
    source_dict = {}

    if os.path.isfile("songs.json"):
        with open(f"songs.json", "r") as f:
            source_dict = json.load(f)

    source_dict.update({song_name:{}})
    source_dict[song_name].update({"sequence": final_sequence})
    source_dict[song_name].update({"durations": only_durations})


    # Write back.
    with open(f"songs.json", "w") as f:
        json.dump(source_dict, f, indent=2)

    pass



glob = glob.glob('*.mid')

print(glob)

for midi in glob:
    print(midi)
    add_to_songs_file(midi)