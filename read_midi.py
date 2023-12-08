import midiutil.MidiFile
import mido as m
from enum import Enum

FILENAME = "mii.mid"
    

def read_midi(filename: str):
    mid = m.MidiFile(filename)
    # for i, track in enumerate(mid.tracks):
    #     print('Track {}: {}'.format(i, track.name))
    #     for msg in track:
    #         pass
    #         #print(msg)
    rythm_track: m.MidiTrack = mid.tracks[0]
    note_track: m.MidiTrack = mid.tracks[1]
    
    notes = []
    
    for message in note_track:
        if type(message) != m.Message:
            continue
        note = str(message).split(" ")
        
        if note[0] == "note_on":
            notes.append(int(note[2][5:]))
        
    return notes
    

def main():
    print(read_midi(FILENAME))

if __name__ == "__main__":
    main()