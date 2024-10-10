import pretty_midi
import numpy as np
from collections import Counter






midi_data = pretty_midi.PrettyMIDI("ffx.mid")




notes_and_timings = []

for instrument in midi_data.instruments:
    if instrument.name == "Piano":
        for note in instrument.notes:
            pitch, timing = note.pitch, note.start

            notes_and_timings.append([pitch,timing])





notes_sorted = sorted(notes_and_timings, key=lambda nt: nt[1])

only_notes = []


for note in notes_sorted:
    note,timing = note
    only_notes.append(note)







