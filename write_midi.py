from midiutil import MIDIFile


notes = [60, 62, 64, 65, 67, 69, 71, 73]

#Create MIDI object
mf = MIDIFile(1)

#Only one track
track = 0

#Start at the beginning
time = 0

mf.addTrackName(track, time, "Markov Music")
mf.addTempo(track, time, 120)

channel = 0
volume = 100
duration = 1

for i in range(len(notes)):
    mf.addNote(track, channel, notes[i], i, duration, volume) 

with open("test.mid", 'wb') as outf:
    mf.writeFile(outf)
