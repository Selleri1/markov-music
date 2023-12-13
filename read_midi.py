import mido as m
from write_midi import *
import numpy as np

FILE_PATH = "christmas_songs/"

# Filnamn och vilket track samt tonart som melodin är i i respektive fil
CHRISTMAS_SONGS = {
    FILE_PATH + "chesnuts.mid": (1, "F"),
    FILE_PATH + "holy_night.mid": (1, "C"),
    FILE_PATH + "silent_night.mid": (0, "D"),
    FILE_PATH + "we_wish_you.mid": (0, "C"),
    FILE_PATH + "joy_to_the_world.mid": (2, "E"),
    FILE_PATH + "jingle_bell.mid": (2, "G"),
    FILE_PATH + "have_yourself.mid" : (3, "G"),
    FILE_PATH + "deck_the_halls.mid": (1, "D"),
    FILE_PATH + "rudolf.mid": (0, "C"),
    FILE_PATH + "let_it_snow.mid": (0, "F"),
    FILE_PATH + "last_christmas.mid": (0, "D"),
    # FILE_PATH + "carol_of_the_bells":( , "e")?
    FILE_PATH + "SantaBaby.mid": (1, "F"),
    FILE_PATH + "ChristmasDay.mid": (2, "F"),
    FILE_PATH + "SleighRide.mid": (5, "G"),
    FILE_PATH + "SantaClausIsComingToTown.mid": (1, "C"),
    FILE_PATH + "Christmas_Carols_-_White_Christmas.mid": (7, "C"),
    FILE_PATH + "Jose_Feliciano_-_Feliz_Navidad.mid": (1, "C"),
    FILE_PATH + "Christmas_Carols_-_Rockin_Around_The_Christmas_Tree.mid": (5, "A"),
    FILE_PATH + "Christmas_Carols_-_Rudolph_The_Red_Nosed_Reindeer.mid": (4, "C"),
    FILE_PATH + "Christmas_Carols_-_Little_Drummer_Boy.mid": (5, "F"),
    FILE_PATH + "Mariah_Carey_-_All_I_Want_For_Christmas_Is_You.mid": (5, "G"),
    FILE_PATH + "Christmas_Carols_-_The_Night_Before_Christmas.mid": (6, "C"),
}

def transpose_to_c(song: list[int], key: str) -> list[int]:
    """Tar sånger som en lista av integers samt deras tonart som en string och transponerar
    dem till tonarten C."""
    # Hur mycket melodin ska transponeras beroende på vilken tonart den är i
    TRANSPOSE_TO_C = {
        "C" : 0,
        "D" : -2,
        "E" : -4,
        "F" : -5,
        "G" : -7,
        "A" : -9,
        "B" : -11,
    }
    transpose = TRANSPOSE_TO_C[key]
    return [note + transpose for note in song]

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

def read_rhythm(filename: str, track_nr: int) -> list[int]:
    """Öppnar midi-filen 'filenam' och tar fram rytmen ur track nr 'track_nr'.
    Returnerar en lista med duration för varje ton som ent """
    mid = m.MidiFile(filename)

    tempo = [message for message in mid if message.type == 'set_tempo']
    tempo_times_time_duration = [meta_message.tempo for meta_message in tempo]
    #tempo_time = [meta_message.time for meta_message in tempo]
    #beats_per_minute = (60000000 * sum(tempo_time)) / (sum(tempo_times_time_duration) / len(tempo_times_time_duration))
    beats_per_minute = 60000000/tempo_times_time_duration[0]
    durations = []
    counter = 0
    for message in mid.tracks[track_nr]:
            if type(message) != m.Message:
                continue
            note_event = message.dict()        
            if note_event["type"] == "note_off" or note_event["type"] == "note_on":
                if note_event["type"] == "note_off" and message.time != 0.0:
                    durations.append(message.time)
                elif note_event["type"] == "note_on" and message.time != 0.0:
                    if counter%2:
                        durations.append(message.time)
                    counter += 1
    #print(list(map(lambda notelength: (notelength/beats_per_minute), durations)))
    return list(map(lambda notelength: (notelength/beats_per_minute), durations))

def read_all(files: dict[str, tuple[int, str]]) -> list[list[int]]:
    """Läser alla filer i 'files' och returnerar som en lista av listor."""
    return [read_midi(filename, track_and_key[0]) for filename, track_and_key in files.items()]

def read_all_transposed(files: dict[str, tuple[int, str]]) -> list[list[int]]:
    """Läser alla filer i 'files' och returnerar som en lista av listor med låtarna transponerade nedåt till tonarten C."""
    return [transpose_to_c(read_midi(filename, track_and_key[0]), track_and_key[1]) for filename, track_and_key in files.items()]

def read_all_transposed_rhythm(files: dict[str, tuple[int, str]]) -> tuple[list[list[int]], list[list[float]]]:
    """Läser alla filer i 'files' och returnerar dels en lista av listor med noterna i varje låt och dels en lista av listor med rytmerna i varje låt.
    Låtarna är transponerade till tonarten C."""
    songs_notes = []
    songs_rythms = []
    
    for filename, track_and_key in files.items():
        songs_notes.append(transpose_to_c(read_midi(filename, track_and_key[0]), track_and_key[1]))
        songs_rythms.append(read_rhythm(filename, track_and_key[0]))
        
    return songs_notes, songs_rythms


def find_longest_note(files: dict[str: tuple[int, str]]) -> int:
    """Tar ett dictionary med filer och deras information (se CHRISTMAS_SONGS) och returnerar
    den längsta tonen i någon av låtarna."""
    for file, item in files.items():
        track_nr = item[0]
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


def find_hi_lo_pitch(songs: list[list[int]]) -> tuple[int]:
    """Tar en lista av låtar (varje låt är en lista av integers) och returnerar lägsta och högsta
    tonerna hittade i någon av låtarna."""
    lowest = 127
    highest = 0
    for song in songs:
        
        for note in song:
            if note < lowest:
                lowest = note
            if note > highest:
                highest = note

    return lowest, highest

def test():
    #print(read_all(CHRISTMAS_SONGS))
    #print(read_midi(FILE_PATH+"holy_night.mid", 1))
    #print(find_longest_note(CHRISTMAS_SONGS))
    # write_notes(read_midi(FILE_PATH+"jingle_bell.mid", 2), 120, 1, "test", "not_trans_test.mid")
    # write_notes(transpose_to_c(read_midi(FILE_PATH+"jingle_bell.mid", 2), "G"), 120, 1, "test", "trans_test.mid")
    #read_rhythm(FILE_PATH+"SantaBaby.mid", 1)
    print(read_all_transposed_rhythm(CHRISTMAS_SONGS))

if __name__ == "__main__":
    test()
