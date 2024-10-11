import pretty_midi
import numpy as np
from collections import Counter
import os
import re
import json
import math
import glob


def custom_round(f: float):
    nearest = round(f / 0.2) *0.2

    if nearest == 0.0:
        nearest = math.ceil(f/0.2) * 0.2

    return nearest


def add_to_songs_file(file):
    file_name = os.path.splitext(file)[0]

    with open("out.txt") as f:
        data = f.read()



    data = data.split('\n')

    data = [d.split('\t') for d in data]

    data.pop(0)

    midi_note_mapping = {int(d[0]):[d[1], d[2]] for d in data if len(d) > 3}


    for idx,key in enumerate(midi_note_mapping):
        value = midi_note_mapping[key]
        piano_note, english_note = value

        split_idx = english_note.find('/')
        if split_idx > -1:
            english_note = english_note[split_idx+1::]
        english_note = english_note[0:3]
        english_note = re.sub('[^0-9a-zA-Z]+', '', english_note)
        english_note = "".join(english_note.split())
        midi_note_mapping[key] = [piano_note, english_note]


    midi_data = pretty_midi.PrettyMIDI(file)

    notes_and_timings = []
    durations = []
    for instrument in midi_data.instruments:
        if instrument.name == "Piano":
            for note in instrument.notes:
                pitch, timing = note.pitch, note.start
                notes_and_timings.append([pitch,timing])

                duration = note.end-note.start
                durations.append([duration,timing])





    notes_sorted = sorted(notes_and_timings, key=lambda nt: nt[1])
    durations_sorted = sorted(durations,key=lambda nt:nt[1])

    only_notes = [note[0] for note in notes_sorted]
    only_durations = [duration[0] for duration in durations_sorted]




    final_sequence = [midi_note_mapping[note][1] for note  in only_notes]


    song_name = file_name

    source_dict = {}

    if os.path.isfile("songs.json"):
        with open(f"songs.json", "r") as f:
            source_dict = json.load(f)

    source_dict.update({song_name:{}})
    source_dict[song_name].update({"sequence": final_sequence})
    source_dict[song_name].update({"durations": only_durations})

    with open(f"songs.json", "w") as f:
        json.dump(source_dict, f, indent=2)

    pass



glob = glob.glob('*.mid')

print(glob)

for midi in glob:
    print(midi)
    add_to_songs_file(midi)