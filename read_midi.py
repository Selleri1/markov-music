import midiutil.MidiFile
import mido as m
from enum import Enum

FILE_PATH = "christmas_songs/"

# Filnamn och vilket track som är melodin i respektive fil
FILES = {
    "chesnuts.mid": 1,
    "holy_night.mid": 1,
}

def read_midi(filename: str, track_nr: int) -> list[int]:
    """Öppnar midi-filen 'filename' och tar fram tonerna ur track nr 'track_nr'.
    Returnerar en lista med tonerna som tal. T.ex. är C4 (middle-c) lika med 60."""
    # Öppna fil
    mid = m.MidiFile(filename)
    
    notes = []
    
    # Varje track består av messages. Gå igenom alla messages i track nr 'track_nr'
    for message in mid.tracks[track_nr]:
        # Behåll bara meddelanden av typen m.Message (de som innehåller info om vilka toner som ska spelas)
        if type(message) != m.Message:
            continue
        
        note_event = message.dict()        
        if note_event["type"] == "note_on" and note_event["velocity"] != 0:
            note = note_event["note"]
            notes.append(note)
            
    return notes
    

def main():
    for filename, track in FILES.items():
        print(read_midi(FILE_PATH + filename, track))

if __name__ == "__main__":
    main()