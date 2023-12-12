from midiutil import MIDIFile

def write_notes(notes, tempo, duration, track_name, file_name):
    """Takes a list of pitches and writes them to a file"""
    mf = MIDIFile(1)
    track = 0       #Only one track
    time = 0        #Start at 0
    mf.addTrackName(track, time, file_name)
    mf.addTempo(track, time, tempo)
    channel = 0
    volume = 100
    for i in range(len(notes)):
        mf.addNote(track, channel, notes[i], i, duration, volume)       #Adds all notes after eachother in order of list
    
    with open(file_name, 'wb') as outf:         #Writes to file 
        mf.writeFile(outf)



 
