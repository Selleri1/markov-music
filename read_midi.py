import midiutil.MidiFile
import mido as m
from enum import Enum

FILENAME = "chesnuts.mid"

# Filnamn och vilket track som är melodin i respektive fil
FILES = {
    "chesnuts.mid": 1,
    "holy-night.mid": 1
}

def read_midi(filename: str, track: int):
    mid = m.MidiFile(filename)
    # for i, track in enumerate(mid.tracks):
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         pass
    #         #print(msg)
    rythm_track: m.MidiTrack = mid.tracks[0]
    note_track: m.MidiTrack = mid.tracks[1]
    
    #tracks = []
    #for track in mid.tracks:
    notes = []
    for message in mid.tracks[track]:
        if type(message) != m.Message:
            continue
        note = str(message).split(" ")
        
        print(note)
        if note[0] == "note_on" and int(note[3][9:])==0:
            notes.append(int(note[2][5:]))
            
    return notes
    

def main():
    print(read_midi(FILENAME, 1))

if __name__ == "__main__":
    main()