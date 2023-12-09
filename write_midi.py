from midiutil import MIDIFile

def write_notes(notes, tempo, duration, track_name, file_name):
    mf = MIDIFile(1)
    track = 0
    time = 0
    mf.addTrackName(track, time, file_name)
    mf.addTempo(track, time, duration)
    channel = 0
    volume = 100
    for i in range(len(notes)):
        mf.addNote(track, channel, notes[i], i, duration, volume)
    
    with open(file_name, 'wb') as outf:
        mf.writeFile(outf)



notes = [40, 61, 64, 55 ,67 ,79 ,71, 63]

write_notes(notes, 120, 1,"Markov Music", "test.mid")  
