from midiutil import MIDIFile


#Create MIDI object
mf = MIDIFile(1)

#only one track
track = 0

#Start at the beginning
time = 0

mf.addTrackName(track, time, "Markov Music")
mf.addTempo(track, time, 120)

channel = 0
volume = 100

pitch = 60
time = 0
duration = 4
mf.addNote(track, channel, pitch, time, duration, volume)

with open("test.mid", 'wb') as outf:
    mf.writeFile(outf)
