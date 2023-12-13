import midiutil.MidiFile
import mido as m
from enum import Enum
import numpy as np

FILE_PATH = "christmas_songs/"

# Filnamn och vilket track som är melodin i respektive fil
CHRISTMAS_SONGS = {
    FILE_PATH + "chesnuts.mid": 1,
    FILE_PATH + "holy_night.mid": 1,
    FILE_PATH + "silent_night.mid": 0,
    FILE_PATH + "we_wish_you.mid": 0,
    FILE_PATH + "joy_to_the_world.mid": 2,
    FILE_PATH + "jingle_bell.mid": 2,
    FILE_PATH + "have_yourself.mid" : 3,
    FILE_PATH + "deck_the_halls.mid": 1,
    FILE_PATH + "rudolf.mid": 0,
    FILE_PATH + "let_it_snow.mid": 0,
    FILE_PATH + "last_christmas.mid": 0,
    # FILE_PATH + "carol_of_the_bells": ?
    FILE_PATH + "SantaBaby.mid": 1,
    FILE_PATH + "ChristmasDay.mid": 2,
    FILE_PATH + "SleighRide.mid": 5,
    FILE_PATH + "SantaClausIsComingToTown.mid": 1,
    FILE_PATH + "Christmas_Carols_-_White_Christmas.mid": 7,
    FILE_PATH + "Jose_Feliciano_-_Feliz_Navidad.mid": 1,
    FILE_PATH + "Christmas_Carols_-_Rockin_Around_The_Christmas_Tree.mid": 5,
    FILE_PATH + "Christmas_Carols_-_Rudolph_The_Red_Nosed_Reindeer.mid": 4,
    FILE_PATH + "Christmas_Carols_-_Little_Drummer_Boy.mid": 5,
    FILE_PATH + "Mariah_Carey_-_All_I_Want_For_Christmas_Is_You.mid": 5,
    FILE_PATH + "Christmas_Carols_-_The_Night_Before_Christmas.mid": 6,
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

def read_all(files: dict[str, int]) -> list[list[int]]:
    """Läser alla filer i 'files' och returnerar som en lista av listor."""
    return [read_midi(filename, track_nr) for filename, track_nr in files.items()]

def read_rythm(filename: str, track_nr: int) -> list[int]:
    """Öppnar midi-filen 'filenam' och tar fram rytmen ur track nr 'track_nr'.
    Returnerar en lista med duration för varje ton som ent """
    pass

def find_longest_note(files: dict[str: int]) -> int:
    for file, track_nr in files.items():
        mid = m.MidiFile(file)
        
        longest = 0
        
        for message in mid.tracks[track_nr]:
            if type(message) != m.Message:
                continue
            
            note_event = message.dict()
            if note_event["type"] == "note_on" and note_event["velocity"] == 0:
                if note_event["time"] > longest:
                    longest = note_event["time"]
                    
            if note_event["type"] == "note_off":
                if note_event["time"] > longest:
                    longest = note_event["time"]
                    
    return longest


def main():
    print(read_all(CHRISTMAS_SONGS))

if __name__ == "__main__":
    main()