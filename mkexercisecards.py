exerciseCards = open("exerciseCards.txt","w")

variations = ["A","B"]
chordProgressions = ["2-5","5-1","2-5-1"]
pVoicings = ["rootless","shell","minor"]
cVoicings = ["rootless","shell"]
intervals = ["minor 2nd","perfect 4th","perfect 5th"]
notes = ["C","C♯/D♭","D","E♭","E","F","F♯/G♭","G","G♯/A♭","A","A♯/B♭","B"]
maj3rdsnotes = ["C","C♯/D♭","D","D♯/E♭"]
min3rdsnotes = ["C","C♯/D♭","D"]
maj2ndsnotes = ["C","C♯/D♭"]
invertableChords4 = ["o7","-7♭5","6","-6","+7","7sus4"]
invertableChords3 = ["","-","o","+","sus4"]
seventhChords = ["-7","7","Δ"]
inversions = ["root position","1st inversion","2nd inversion","3rd inversion"]
scales = ["major","dorian","phrygian","lydian","mixolydian","aeolian","locrian","harmonic major","dorian♭5","phrygian♭4","lydian♭3","mixolydian♭2","lydian augmented♯2","locrian♭♭7","bebop dorian","bebop mixolydian","bebop major","half-whole diminished","whole-half diminished","major pentatonic","minor pentatonic","blues","in-sen","whole-tone","natural minor","melodic minor","dorian♭2","lydian dugmented","lydian dominant","mixolydian♭6","locrian♯2","altered","harmonic minor","locrian♮6","augmented major","dorian♯4","phrygian dominant","lydian♯2","super-locrian","bebop melodic minor"]

for chordProgression in chordProgressions:
    for variation in variations:
        for note in maj3rdsnotes:
            exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving up major 3rds\n")
            exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving down major 3rds\n")
            for voicing in pVoicings:
                exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving up major 3rdss\n")
                exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving down major 3rds\n")
        for note in min3rdsnotes:
            exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving up minor 3rds\n")
            exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving down minor 3rds\n")
            for voicing in pVoicings:
                exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving up minor 3rds\n")
                exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving down minor 3rds\n")
        for note in maj2ndsnotes:
            exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving up major 2nds\n")
            exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving down major 2nds\n")
            for voicing in pVoicings:
                exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving up major 2nds\n")
                exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving down major 2nds\n")
        for note in notes:
            for interval in intervals:
                exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving up "+interval+"s\n")
                exerciseCards.write("Play a type "+variation+" "+chordProgression+" in "+note+" moving down "+interval+"s\n")
                for voicing in pVoicings:
                    exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving up "+interval+"s\n")
                    exerciseCards.write("Play a "+voicing+" type "+variation+" "+chordProgression+" in "+note+" moving down "+interval+"s\n")

for note in notes:
    for chord in invertableChords4:
        exerciseCards.write("Play all inversions of a "+note+chord+" chord going up\n")
        exerciseCards.write("Play all inversions of a "+note+chord+" chord going down\n")
    for chord in seventhChords:
        exerciseCards.write("Play all inversions of a "+note+chord+" chord going up\n")
        exerciseCards.write("Play all inversions of a "+note+chord+" chord going down\n")
    for chord in invertableChords3:
        exerciseCards.write("Play all inversions of a "+note+chord+" chord going up\n")
        exerciseCards.write("Play all inversions of a "+note+chord+" chord going down\n")


for scale in scales:
        exerciseCards.write("Play a "+note+" "+scale+" scale going up\n")
        exerciseCards.write("Play a "+note+" "+scale+" scale going down\n")
        exerciseCards.write("Play a "+note+" "+scale+" scale in contrary motion\n")

for note in maj3rdsnotes:
    for variation in variations:
        exerciseCards.write("Play a type "+variation+" rootless "+note+"7 moving up major 3rds\n")
        for chord in seventhChords:
            exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving up major 3rds\n")
            exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving down major 3rds\n")
    for chord in invertableChords4:
        exerciseCards.write("Play a root position "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down major 3rds\n")
    for chord in invertableChords3:
        exerciseCards.write("Play a root position "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down major 3rds\n")
    for chord in seventhChords:
        exerciseCards.write("Play a root position "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down major 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up major 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down major 3rds\n")

for note in min3rdsnotes:
    for variation in variations:
        exerciseCards.write("Play a type "+variation+" rootless "+note+"7 moving up minor 3rds\n")
        for chord in seventhChords:
            exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving up minor 3rds\n")
            exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving down minor 3rds\n")
    for chord in invertableChords4:
        exerciseCards.write("Play a root position "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down minor 3rds\n")
    for chord in invertableChords3:
        exerciseCards.write("Play a root position "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down minor 3rds\n")
    for chord in seventhChords:
        exerciseCards.write("Play a root position "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down minor 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up minor 3rds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down minor 3rds\n")

for note in maj2ndsnotes:
    for variation in variations:
        exerciseCards.write("Play a type "+variation+" rootless "+note+"7 moving up major 2nds\n")
        for chord in seventhChords:
            exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving up major 2nds\n")
            exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving down major 2nds\n")
    for chord in invertableChords4:
        exerciseCards.write("Play a root position "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down major 2nds\n")
    for chord in invertableChords3:
        exerciseCards.write("Play a root position "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down major 2nds\n")
    for chord in seventhChords:
        exerciseCards.write("Play a root position "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a root position "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 1st inversion "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down major 2nds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up major 2nds\n")
        exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down major 2nds\n")

for note in notes:
    for interval in intervals:
        for variation in variations:
            exerciseCards.write("Play a type "+variation+" rootless "+note+"7 moving up "+interval+"s\n")
            for chord in seventhChords:
                exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving up "+interval+"s\n")
                exerciseCards.write("Play a type "+variation+" shell "+note+chord+" moving down "+interval+"s\n")
        for chord in invertableChords4:
            exerciseCards.write("Play a root position "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a root position "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 1st inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 1st inversion "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down "+interval+"s\n")
        for chord in invertableChords3:
            exerciseCards.write("Play a root position "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a root position "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 1st inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 1st inversion "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down "+interval+"s\n")
        for chord in seventhChords:
            exerciseCards.write("Play a root position "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a root position "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 1st inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 1st inversion "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 2nd inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 2nd inversion "+note+chord+" moving down "+interval+"s\n")
            exerciseCards.write("Play a 3rd inversion "+note+chord+" moving up "+interval+"s\n")
            exerciseCards.write("Play a 3rd inversion "+note+chord+" moving down "+interval+"s\n")
