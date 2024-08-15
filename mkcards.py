#TODO add chord substitution cards ala Jazz Theory Book
#TODO add more chord voicing cards
#TODO? add augmented scale?
#TODO make sure chord-scale cards agree with https://newjazz.dk/Compendiums/scales_of_harmonies.pdf
import re
theoryCardsImg = open("theoryCardsImg.txt","w")
theoryCards = open("theoryCards.txt","w")
notes = ["C","D","E","F","G","A","B"]
keysEnharmonic = ["C","C♯/D♭","D","D♯/E♭","E","F","F♯/G♭","G","G♯/A♭","A","A♯/B♭","B/C♭"]
sharpKeysMajor = ["G","D","A","E","B","F♯","C♯"]
flatKeysMajor = ["F","B♭","E♭","A♭","D♭","G♭","C♭"]
sharpKeysMinor = ["E","B","F♯","C♯","G♯","D♯","A♯"]
flatKeysMinor = ["D","G","C","F","B♭","E♭","A♭"]
majorKeys = ["C","F","B♭","E♭","A♭","D♭","F♯/G♭","B","E","A","D","G"]
minorKeys = ["A","D","G","C","F","B♭","D♯/E♭","G♯","C♯","F♯","B","E"]
orderOfAccidentals = ["B","E","A","D","G","C","F"]
modeDegrees = ["2nd","3rd","4th","5th","6th","7th"]
def keysContains(key, keyList):
    keyNum = -1
    for k in keyList:
        if key == k:
            keyNum = keyList.index(k)
        elif "/" in k:
            for l in k.split("/"):
                if key == l:
                    keyNum = keyList.index(k)
    return keyNum

def getKeySignature(key, keyNum):
    keyList = []
    if keyNum<=4 or (keyNum<=7 and key[-1]=="♭"):
        for i in range(keyNum):
            keyList.append(orderOfAccidentals[i] + "♭")
    if keyNum>=8 or (keyNum>=5 and (key[-1]=="♯" or key == "B")):
        for i in range(12-keyNum):
            keyList.append(orderOfAccidentals[6-i] + "♯")
    return keyList

def getNotes(key, keySignature):
    notesList = []
    keyChrNum = ord(key[0])
    for i in range(7):
        if keyChrNum+i == 72:
            keyChrNum -= 7
        note = chr(keyChrNum+i)
        for k in keySignature:
            if note in k:
                accidental = k[-1]
                note += accidental
        notesList.append(note)
    return notesList

def AlterNote(alteration, note):
    if alteration == "sharp":
        if note[-1] == "♭":
            note = note[0]
        else:
            note += "♯"
    elif alteration == "flat":
        if note[-1] == "♯":
            note = note[0]
        else:
            note += "♭"
    return note

scaleDegrees = {"I":0,"♭II":1,"II":2,"♯II":3,"♭III":3,"III":4,"IV":5,"♯IV":6,"♭V":6,"V":7,"♯5":8,"♭VI":8,"VI":9,"♯VI":10,"♭VII":10,"VII":11}
def getDegree(key,degree):
    degree = degree.upper()
    keyIndex = keysContains(key, keysEnharmonic)
    degreeNum = scaleDegrees[degree]
    degreeIndex = keyIndex+degreeNum
    while degreeIndex > 11:
        degreeIndex -=12
    scaleDegree = keysEnharmonic[degreeIndex]
    if "/" in scaleDegree:
        if "♭" in degree and "♭" in scaleDegree:
            scaleDegree = scaleDegree.split("/")[1]
        elif "♯" in degree and "♯" in scaleDegree:
            scaleDegree = scaleDegree.split("/")[0]
        elif "♭" in scaleDegree and "♯" in scaleDegree and key in flatKeysMajor:
            scaleDegree = scaleDegree.split("/")[1]
        elif "♭" in scaleDegree and "♯" in scaleDegree and key in sharpKeysMajor:
            scaleDegree = scaleDegree.split("/")[0]
        elif key == "C♭" or key == "G♭":
            scaleDegree = scaleDegree.split("/")[1]
        else:
            scaleDegree = scaleDegree.split("/")[0]
    return scaleDegree

def GetImageString(key):
    if key[1:]=="♭":
        if key[0]=="C":
            return "B"
        elif key[0]=="F":
            return "E"
        else:
            return (key[0]+"b")
    elif key[1:]=="♯":
        if key[0] == "B":
            return "C"
        elif key[0] == "E":
            return "F"
        else:
            return notes[notes.index(key[0])+1]+"b"
    elif key[1:]=="♭♭":
        if key[0] == "C":
            return "Bb"
        elif key[0] == "F":
            return "Eb"
        else:
            return notes[notes.index(key[0])-1]
    elif key[1:]=="♯♯":
        if key[0] == "B":
            return "Db"
        elif key[0] == "E":
            return "Gb"
        else:
            return notes[notes.index(key[0])+1]
    else:
        return key

def GetImage(key,blueList,orangeList):
    keyString = GetImageString(key)
    imageStr = ";<canvas id=\"keyboard\" style=\"border:1px solid black\" data-tonic=\""+keyString+"\" data-highlight1=\""
    blueStr = ""
    orangeStr = ""
    for key in blueList:
        blueStr += GetImageString(key)
        blueStr += ","
    if not blueStr == "":
        blueStr = blueStr[:-1]
    imageStr += (blueStr+"\" data-highlight2=\"")
    for key in orangeList:
        orangeStr += GetImageString(key)
        orangeStr += ","
    if not orangeStr == "":
        orangeStr = orangeStr[:-1]
    imageStr += (orangeStr+"\"/>")
    return imageStr

keys = ["C","F","A♯","B♭","D♯","E♭","G♯","A♭","C♯","D♭","F♯","G♭","B","C♭","E","A","D","G"]
for key in keys:
    majorKeyNum = -1
    minorKeyNum = -1
    majorKeyNum = keysContains(key, majorKeys)
    minorKeyNum = keysContains(key, minorKeys)
    if not majorKeyNum == -1:
        # key-signature cards
        majorKeyList = getKeySignature(key, majorKeyNum)

        # relative minor cards
        relativeMinor = getDegree(key,"VI")
        if  keysContains(relativeMinor,minorKeys) != -1:
            theoryCards.write("the relative minor of "+key+" major is {{c1::"+relativeMinor+"}} minor;musictheory::relativekeys\n")


        # 7 note major scales
        # major + modes, harmonic major + modes
        majorList = getNotes(key, majorKeyList)
        flatSecond = AlterNote("flat",majorList[1]) 
        second = majorList[1]
        sharpSecond = AlterNote("sharp",majorList[1])
        flatThird = AlterNote("flat",majorList[2])
        third = majorList[2]
        flatFourth = AlterNote("flat",majorList[3])
        fourth = majorList[3]
        sharpFourth = AlterNote("sharp",majorList[3])
        flatFifth = AlterNote("flat",majorList[4])
        fifth = majorList[4]
        sharpFifth = AlterNote("sharp",majorList[4])
        flatSixth = AlterNote("flat",majorList[5])
        sixth = majorList[5]
        sharpSixth = AlterNote("sharp",majorList[5])
        flatSeventh = AlterNote("flat",majorList[6])
        seventh = majorList[6]
        # major modes
        dorianList = majorList[:2]+[flatThird]+majorList[3:6]+[flatSeventh]
        phrygianList = [key,flatSecond,flatThird]+majorList[3:5]+[flatSixth,flatSeventh]
        lydianList = majorList[:3]+[sharpFourth]+majorList[4:]
        mixolydianList = majorList[:6]+[flatSeventh]
        aeolianList = majorList[:2]+[flatThird]+majorList[3:5]+[flatSixth,flatSeventh]
        locrianList = [key,flatSecond,flatThird,fourth,flatFifth,flatSixth,flatSeventh]
        # harmonic major modes
        hMajorList = majorList[:5]+[flatSixth]+[majorList[6]]
        dorianFlatFiveList = majorList[:2]+[flatThird,fourth,flatFifth,sixth,flatSeventh]
        phrygianFlatFourList = [key,flatSecond,flatThird,flatFourth,fifth,flatSixth,flatSeventh]
        lydianFlatThreeList = majorList[:2]+[flatThird]+[sharpFourth]+majorList[4:]
        mixolydianFlatTwoList = [key, flatSecond]+majorList[2:6]+[flatSeventh]
        lydianAugmentedSharpTwoList = [key,sharpSecond,third,sharpFourth,sharpFifth]+majorList[5:]
        locrianDoubleFlatSevenList = [key,flatSecond,flatThird,fourth,flatFifth,flatSixth]+[AlterNote("flat",flatSeventh)]
        majorString = ""
        dorianString = ""
        phrygianString = ""
        lydianString = ""
        phrygianString = ""
        mixolydianString = ""
        aeolianString = ""
        locrianString = ""
        hMajorString = ""
        dorianFlatFiveString = ""
        phrygianFlatFourString = ""
        lydianFlatThreeString = ""
        mixolydianFlatTwoString = ""
        lydianAugmentedSharpTwoString = ""
        locrianDoubleFlatSevenString = ""
        for i in range(7):
            majorString += majorList[i]+" "
            dorianString += dorianList[i]+" "
            phrygianString += phrygianList[i]+" "
            lydianString += lydianList[i]+" "
            mixolydianString += mixolydianList[i]+" "
            aeolianString += aeolianList[i]+" "
            locrianString += locrianList[i]+" "
            hMajorString += hMajorList[i]+" "
            dorianFlatFiveString += dorianFlatFiveList[i]+" "
            phrygianFlatFourString += phrygianFlatFourList[i]+" "
            lydianFlatThreeString += lydianFlatThreeList[i]+" "
            mixolydianFlatTwoString += mixolydianFlatTwoList[i]+" "
            lydianAugmentedSharpTwoString += lydianAugmentedSharpTwoList[i]+" "
            locrianDoubleFlatSevenString += locrianDoubleFlatSevenList[i]+" "
        majorString = majorString[:-1]
        dorianString = dorianString[:-1]
        phrygianString = phrygianString[:-1]
        lydianString = lydianString[:-1]
        mixolydianString = mixolydianString[:-1]
        aeolianString = aeolianString[:-1]
        locrianString = locrianString[:-1]
        hMajorString = hMajorString[:-1]
        dorianFlatFiveString = dorianFlatFiveString[:-1]
        phrygianFlatFourString = phrygianFlatFourString[:-1]
        lydianFlatThreeString = lydianFlatThreeString[:-1]
        mixolydianFlatTwoString = mixolydianFlatTwoString[:-1]
        lydianAugmentedSharpTwoString = lydianAugmentedSharpTwoString[:-1]
        locrianDoubleFlatSevenString = locrianDoubleFlatSevenString[:-1]
        majorImage = GetImage(key,majorList,[])
        dorianImage = GetImage(key,dorianList,[])
        phrygianImage = GetImage(key,phrygianList,[])
        lydianImage = GetImage(key,lydianList,[])
        mixolydianImage = GetImage(key,mixolydianList,[])
        aeolianImage = GetImage(key,aeolianList,[])
        locrianImage = GetImage(key,locrianList,[])
        hMajorImage = GetImage(key,hMajorList,[])
        dorianFlatFiveImage = GetImage(key,dorianFlatFiveList,[])
        phrygianFlatFourImage = GetImage(key,phrygianFlatFourList,[])
        lydianFlatThreeImage = GetImage(key,lydianFlatThreeList,[])
        mixolydianFlatTwoImage = GetImage(key,mixolydianFlatTwoList,[])
        lydianAugmentedSharpTwoImage = GetImage(key,lydianAugmentedSharpTwoList,[])
        locrianDoubleFlatSevenImage = GetImage(key,locrianDoubleFlatSevenList,[])
        theoryCardsImg.write("the notes in the "+key+" major scale are {{c1::"+majorString+"}}"+majorImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" dorian scale are {{c1::"+dorianString+"}}"+dorianImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" phrygian scale are {{c1::"+phrygianString+"}}"+phrygianImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" lydian scale are {{c1::"+lydianString+"}}"+lydianImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" mixolydian scale are {{c1::"+mixolydianString+"}}"+mixolydianImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" aeolian scale are {{c1::"+aeolianString+"}}"+aeolianImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" locrian scale are {{c1::"+locrianString+"}}"+locrianImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" harmonic major scale are {{c1::"+hMajorString+"}}"+hMajorImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" dorian♭5 scale are {{c1::"+dorianFlatFiveString+"}}"+dorianFlatFiveImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" phrygian♭4 scale are {{c1::"+phrygianFlatFourString+"}}"+phrygianFlatFourImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" lydian♭3 scale are {{c1::"+lydianFlatThreeString+"}}"+lydianFlatThreeImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" mixolydian♭2 scale are {{c1::"+mixolydianFlatTwoString+"}}"+mixolydianFlatTwoImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" lydian augmented♯2 scale are {{c1::"+lydianAugmentedSharpTwoString+"}}"+lydianAugmentedSharpTwoImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" locrian♭♭7 scale are {{c1::"+locrianDoubleFlatSevenString+"}}"+locrianDoubleFlatSevenImage+";musictheory::scales\n")

        # 8 note scales
        # half-whole diminished, bebop dorian, bebop dominant, bebop major
        bebopDorianList = majorList[:2]+[flatThird,flatFourth]+majorList[3:6]+[flatSeventh]
        bebopDominantList = majorList[:6] + [flatSeventh,seventh]
        bebopMajorList = majorList[:5] + [flatSixth] + majorList[5:]
        bebopDorianString = ""
        bebopDominantString = ""
        bebopMajorString = ""
        for i in range(8):
            bebopDorianString += bebopDorianList[i]+" "
            bebopDominantString += bebopDominantList[i]+" "
            bebopMajorString += bebopMajorList[i]+" "
        bebopDorianString = bebopDorianString[:-1]
        bebopDominantString = bebopDominantString[:-1]
        bebopMajorString = bebopMajorString[:-1]
        bebopDorianImage = GetImage(key,bebopDorianList,[])
        bebopDominantImage = GetImage(key,bebopDominantList,[])
        bebopMajorImage = GetImage(key,bebopMajorList,[])
        theoryCardsImg.write("the notes in the "+key+" bebop dorian scale are {{c1::"+bebopDorianString+"}}"+bebopDorianImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" bebop dominant scale are {{c1::"+bebopDominantString+"}}"+bebopDominantImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" bebop major scale are {{c1::"+bebopMajorString+"}}"+bebopMajorImage+";musictheory::scales\n")

        # 5 note scales
        # major pentatonic, in-sen
        insenList = [key, flatSecond]+majorList[3:5]+[flatSeventh]
        majorPentatonicList = [key,second,third,fifth,sixth]
        insenString = ""
        majorPentatonicString = ""
        for i in range(5):
            insenString += insenList[i]+" "
            majorPentatonicString += majorPentatonicList[i]+" "
        insenString = insenString[:-1]
        majorPentatonicString = majorPentatonicString[:-1]
        insenImage = GetImage(key,insenList,[])
        majorPentatonicImage = GetImage(key,majorPentatonicList,[])
        theoryCardsImg.write("the notes in the "+key+" in-sen scale are {{c1::"+insenString+"}}"+insenImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" major pentatonic scale are {{c1::"+majorPentatonicString+"}}"+majorPentatonicImage+";musictheory::scales\n")

        # 6 note scales
        # whole-tone scale, augmented scale
        wholeToneList = majorList[:3]+[sharpFourth, sharpFifth, flatSeventh]
        augmentedList = [key,sharpSecond,third,fifth,flatSixth,seventh]
        wholeToneString = ""
        augmentedString = ""
        for i in range(6):
            wholeToneString += wholeToneList[i] + " "
            augmentedString += augmentedList[i] + " "
        wholeToneString = wholeToneString[:-1]
        augmentedString = augmentedString[:-1]
        wholeToneImage = GetImage(key,wholeToneList,[])
        augmentedImage = GetImage(key,augmentedList,[])
        theoryCardsImg.write("the notes in the "+key+" whole-tone scale are {{c1::"+wholeToneString+"}}"+wholeToneImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" augmented scale are {{c1::"+augmentedString+"}}"+augmentedImage+";musictheory::scales\n")

        # major modes
        majorModes = [second+" dorian",third+" phrygian",fourth+" lydian",fifth+" mixolydian",sixth+" aeolian",seventh+" locrian"]
        majorModeImages = [dorianImage,phrygianImage,lydianImage,mixolydianImage,aeolianImage,locrianImage]
        for i in range(6):
            mode = modeDegrees[i]
            majorMode = majorModes[i]
            majorModeImage = majorModeImages[i]
            theoryCardsImg.write("{{c1::"+majorMode+"}} is the "+mode+" mode of {{c2::"+key+" major}}"+majorModeImage+";musictheory::modes\n")

        # harmonic major modes
        harmonicMajorModes = [second+" dorian♭5",third+" phrygian♭4",fourth+" lydian♭3",fifth+" mixolydian♭2",flatSixth+" lydian augmented♯2",seventh+" locrian♭♭7"]
        harmonicMajorModeImages = [dorianFlatFiveImage,phrygianFlatFourImage,lydianFlatThreeImage,mixolydianFlatTwoImage,lydianAugmentedSharpTwoImage,locrianDoubleFlatSevenImage]
        for i in range(6):
            mode = modeDegrees[i]
            harmonicMajorMode = harmonicMajorModes[i]
            harmonicMajorModeImage = harmonicMajorModeImages[i]
            theoryCardsImg.write("{{c1::"+harmonicMajorMode+"}} is the "+mode+" mode of {{c2::"+key+" harmonic major}}"+harmonicMajorModeImage+";musictheory::modes\n")
        
        # key signatures
        majorKeyString = ""
        for i in majorKeyList:
            majorKeyString += i+" "
        if majorKeyString == "":
            majorKeyString = "no sharps or flats"
        else:
            majorKeyString = majorKeyString[:-1]
        majorKeyImage = GetImage(key,majorList,majorKeyList)
        theoryCardsImg.write("the key signature of {{c1::"+key+"}} major is {{c2::"+majorKeyString+"}}"+majorKeyImage+";musictheory::keysignatures\n")

        # major scale degree cards
        majorDegrees = {"♭2nd":flatSecond,"2nd":second,"♯2nd":sharpSecond,"3rd":third,"4th":fourth,"♯4th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth,"♭6th":flatSixth,"6th":sixth,"♭7th":flatSeventh,"7th":seventh,"♭9th":flatSecond,"9th":second,"♯9th":sharpSecond,"11th":fourth,"♯11th":sharpFourth,"♭13th":flatSixth,"13th":sixth}
        for degree in majorDegrees:
            degreeImage = GetImage(key,majorList,[majorDegrees[degree]])
            theoryCardsImg.write("{{c1::"+majorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} major"+degreeImage+";musictheory::scaledegrees\n")
        # major scale degrees 2nd cloze
        majorDegrees1 = {"♭2nd/♭9th":flatSecond,"2nd/9th":second,"♯2nd/♯9th":sharpSecond,"3rd":third,"4th/11th":fourth,"♯4th/♯11th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth,"♭6th/♭13th":flatSixth,"6th/13th":sixth,"♭7th":flatSeventh,"7th":seventh}
        for degree in majorDegrees1:
            degreeImage = GetImage(key,majorList,[majorDegrees1[degree]])
            theoryCardsImg.write(majorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" major"+degreeImage+";musictheory::scaledegrees\n")

        # major triad chord functional harmony
        majorDegrees = ["I","ii","iii","IV","V","vi","vii"]
        functionalTriadsMajor = ["","-","-","","","-","o"]
        for i in range(len(majorDegrees)):
            degree = majorDegrees[i]
            majorTriad = functionalTriadsMajor[i]
            chordList = []
            for j in range(0,6,2):
                n = i+j
                if n > 6:
                    n -= 7
                chordList = chordList + [majorList[n]]
            majorTriadNote = majorList[i]
            majorTriadChordImage = GetImage(key, majorList+majorList, chordList)
            theoryCardsImg.write("{{c1::"+majorTriadNote+majorTriad+"}} is the {{c2::"+degree+"}} triad of {{c3::"+key+"}} major"+majorTriadChordImage+";musictheory::functionalharmony\n")

        # major 7th chord functional harmony
        majorDegrees = ["I","ii","iii","IV","V","vi","vii"]
        functional7thsMajor = ["Δ7","-7","-7","Δ7","7","-7","o7"]
        for i in range(len(majorDegrees)):
            degree = majorDegrees[i]
            major7thChord = functional7thsMajor[i]
            chordList = []
            for j in range(0,8,2):
                n = i+j
                if n > 6:
                    n -= 7
                chordList = chordList + [majorList[n]]
            major7thChordNote = majorList[i]
            major7thChordImage = GetImage(key, majorList+majorList, chordList)
            theoryCardsImg.write("{{c1::"+major7thChordNote+major7thChord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+key+"}} major"+major7thChordImage+";musictheory::functionalharmony\n")


        # major guide tones cards
        m7AGuideTones = GetImage(key,[flatThird,flatSeventh],[])
        M7AGuideTones = GetImage(key,[third,seventh],[])
        m7BGuideTones = GetImage(key,[flatSeventh,flatThird],[])
        M7BGuideTones = GetImage(key,[seventh,third],[])
        theoryCardsImg.write("the guide tones of "+key+"-7 in inversion A are {{c1::"+flatThird+" and "+flatSeventh+"}} (in order from lowest to highest)"+m7AGuideTones+";musictheory::voicings\n")
        theoryCardsImg.write("the guide tones of "+key+"Δ7 in inversion A are {{c1::"+third+" and "+seventh+"}} (in order from lowest to highest)"+M7AGuideTones+";musictheory::voicings\n")
        theoryCardsImg.write("the guide tones of "+key+"-7 in inversion B are {{c1::"+flatSeventh+" and "+flatThird+"}} (in order from lowest to highest)"+m7BGuideTones+";musictheory::voicings\n")
        theoryCardsImg.write("the guide tones of "+key+"Δ7 in inversion B are {{c1::"+seventh+" and "+third+"}} (in order from lowest to highest)"+M7BGuideTones+";musictheory::voicings\n")

        # 3 note major chord voicings cards
        # major augmented
        inversions = ["root position","first inversion","second inversion","third inversion"]
        majorChordNotes = [key,third,fifth]
        augmentedChordNotes = [key,third,sharpFifth]
        for i in range(3):
            majorChordString = ""
            majorChordList = []
            augmentedChordString = ""
            augmentedChordList = []
            inversion = inversions[i]
            for n in range(3):
                note=i+n
                if note>=3:
                    note-=3
                majorChordString += majorChordNotes[note]+" "
                majorChordList += [majorChordNotes[note]]
                augmentedChordString += augmentedChordNotes[note]+" "
                augmentedChordList += [augmentedChordNotes[note]]
            majorChordString = majorChordString[:-1]
            augmentedChordString = augmentedChordString[:-1]
            majorImage = GetImage(key,majorChordList,[])
            augmentedImage = GetImage(key,augmentedChordList,[])
            theoryCardsImg.write("the notes in a "+key+" chord in "+inversion+" are {{c1::"+majorChordString+"}} (in order from lowest to highest)"+majorImage+";musictheory::voicings\n")
            theoryCardsImg.write("the notes in a "+key+" augmented chord in "+inversion+" are {{c1::"+augmentedChordString+"}} (in order from lowest to highest)"+augmentedImage+";musictheory::voicings\n")

        # 4 note major chord voicing cards
        # minor7 major7
        minor7ChordNotes = [key,flatThird,fifth,flatSeventh]
        major7ChordNotes = [key,third,fifth,seventh]
        for i in range(4):
            minor7ChordString = ""
            minor7ChordList = []
            major7ChordString = ""
            major7ChordList = []
            inversion = inversions[i]
            for n in range(4):
                note = i+n
                if note>=4:
                    note -=4
                minor7ChordString += minor7ChordNotes[note]+" "
                minor7ChordList += [minor7ChordNotes[note]]
                major7ChordString += major7ChordNotes[note]+" "
                major7ChordList += [major7ChordNotes[note]]
            minor7ChordString = minor7ChordString[:-1]
            major7ChordString = major7ChordString[:-1]
            minor7Image = GetImage(key,minor7ChordList,[])
            major7Image = GetImage(key,major7ChordList,[])
            theoryCardsImg.write("the notes in a "+key+"-7 chord in "+inversion+" are {{c1::"+minor7ChordString+"}} (in order from lowest to highest)"+minor7Image+";musictheory::voicings\n")
            theoryCardsImg.write("the notes in a "+key+"Δ7 chord in "+inversion+" are {{c1::"+major7ChordString+"}} (in order from lowest to highest)"+major7Image+";musictheory::voicings\n")

        # rootless chord cards in A and B voicings
        # minor9 dominant13 major9
        rootlessInversions = ["A","","B"]
        rootlessiiNotes = [flatThird,fifth,flatSeventh,second]
        rootlessVNotes = [flatSeventh,second,third,sixth]
        rootlessINotes = [third,fifth,seventh,second]
        for i in range(0,3,2):
            rootlessiiString = ""
            rootlessiiList = []
            rootlessVString = ""
            rootlessVList = []
            rootlessIString = ""
            rootlessIList = []
            rootlessInversion = rootlessInversions[i]
            for n in range(4):
                note = i+n
                if note>=4:
                    note -=4
                rootlessiiString += rootlessiiNotes[note]+" "
                rootlessiiList += [rootlessiiNotes[note]]
                rootlessVString += rootlessVNotes[note]+" "
                rootlessVList += [rootlessVNotes[note]]
                rootlessIString += rootlessINotes[note]+" "
                rootlessIList += [rootlessINotes[note]]
            rootlessiiString = rootlessiiString[:-1]
            rootlessVString = rootlessVString[:-1]
            rootlessIString = rootlessIString[:-1]
            rootlessiiImage = GetImage(key,rootlessiiList,[])
            rootlessVImage = GetImage(key,rootlessVList,[])
            rootlessIImage = GetImage(key,rootlessIList,[])
            theoryCardsImg.write("the notes in a type "+rootlessInversion+" rootless "+key+"-9 chord are {{c1::"+rootlessiiString+"}} (in order from lowest to highest)"+rootlessiiImage+";musictheory::voicings\n")
            theoryCardsImg.write("the notes in a type "+rootlessInversion+" rootless "+key+"13 chord are {{c1::"+rootlessVString+"}} (in order from lowest to highest)"+rootlessVImage+";musictheory::voicings\n")
            theoryCardsImg.write("the notes in a type "+rootlessInversion+" rootless "+key+"Δ9 chord are {{c1::"+rootlessIString+"}} (in order from lowest to highest)"+rootlessIImage+";musictheory::voicings\n")

        # extended major chord voicing cards
        # 4 note extended major chords
        major6List = [key,third,fifth,sixth]
        rootless69List = [third,fifth,sixth,second]
        rootlessMajor13List = [seventh,second,third,sixth]
        major6String = ""
        rootless69String = ""
        rootlessMajor13String = ""
        for i in range(4):
            major6String += major6List[i]+" "
            rootless69String += rootless69List[i]+" "
            rootlessMajor13String += rootlessMajor13List[i]+" "
        major6String = major6String[:-1]
        rootless69String = rootless69String[:-1]
        rootlessMajor13String = rootlessMajor13String[:-1]
        major6Image = GetImage(key,major6List,[])
        rootless69Image = GetImage(key,rootless69List,[])
        rootlessMajor13Image = GetImage(key,rootlessMajor13List,[])
        theoryCardsImg.write("the notes in a "+key+"6 chord are {{c1::"+major6String+"}} (in order from lowest to highest)"+major6Image+";musictheory::voicings\n")
        theoryCardsImg.write("the notes in a type A rootless "+key+"6/9 chord are {{c1::"+rootless69String+"}} (in order from lowest to highest)"+rootless69Image+";musictheory::voicings\n")
        theoryCardsImg.write("the notes in a type B rootless "+key+"Δ13 chord are {{c1::"+rootlessMajor13String+"}} (in order from lowest to highest)"+rootlessMajor13Image+";musictheory::voicings\n")

        # 5 note extended major chords
        minor9List = [key,flatThird,fifth,flatSeventh,second]
        major9List = [key,third,fifth,seventh,second]
        sixNineList = [key,third,fifth,sixth,second]
        minor9String = ""
        major9String = ""
        sixNineString = ""
        for i in range(5):
            minor9String += minor9List[i]+" "
            major9String += major9List[i]+" "
            sixNineString += sixNineList[i]+" "
        minor9String = minor9String[:-1]
        major9String = major9String[:-1]
        sixNineString = sixNineString[:-1]
        minor9Image = GetImage(key,minor9List,[])
        major9Image = GetImage(key,major9List,[])
        sixNineImage = GetImage(key,sixNineList,[])
        theoryCardsImg.write("the notes in a "+key+"-9 chord are {{c1::"+minor9String+"}} (in order from lowest to highest)"+minor9Image+";musictheory::voicings\n")
        theoryCardsImg.write("the notes in a "+key+"Δ9 chord are {{c1::"+major9String+"}} (in order from lowest to highest)"+major9Image+";musictheory::voicings\n")
        theoryCardsImg.write("the notes in a "+key+"6/9 chord are {{c1::"+sixNineString+"}} (in order from lowest to highest)"+sixNineImage+";musictheory::voicings\n")

        # 6 note extended major chords
        minor11List = [key,flatThird,fifth,flatSeventh,second,fourth]
        majorSharp11List = [key,third,fifth,seventh,second,sharpFourth]
        minor11String = ""
        majorSharp11String = ""
        for i in range(6):
            minor11String += minor11List[i]+" "
            majorSharp11String += majorSharp11List[i]+" "
        minor11String = minor11String[:-1]
        majorSharp11String = majorSharp11String[:-1]
        minor11Image = GetImage(key,minor11List,[])
        majorSharp11Image = GetImage(key,majorSharp11List,[])
        theoryCardsImg.write("the notes in a "+key+"-11 chord are {{c1::"+minor11String+"}} (in order from lowest to highest)"+minor11Image+";musictheory::voicings\n")
        theoryCardsImg.write("the notes in a "+key+"Δ♯11 chord are {{c1::"+majorSharp11String+"}} (in order from lowest to highest)"+majorSharp11Image+";musictheory::voicings\n")

        # 7 note extended major chords
        minor13List = [key,flatThird,fifth,flatSeventh,second,fourth,sixth]
        major13Sharp11List = [key,third,fifth,seventh,second,sharpFourth,sixth]
        minor13String = ""
        major13Sharp11String = ""
        for i in range(7):
            minor13String += minor13List[i]+" "
            major13Sharp11String += major13Sharp11List[i]+" "
        minor13String = minor13String[:-1]
        major13Sharp11String = major13Sharp11String[:-1]
        minor13Image = GetImage(key,minor13List,[])
        major13Sharp11Image = GetImage(key,majorSharp11List,[])
        theoryCardsImg.write("the notes in a "+key+"-13 chord are {{c1::"+minor13String+"}} (in order from lowest to highest)"+minor13Image+";musictheory::voicings\n")
        theoryCardsImg.write("the notes in a "+key+"Δ13♯11 chord are {{c1::"+major13Sharp11String+"}} (in order from lowest to highest)"+major13Sharp11Image+";musictheory::voicings\n")

    if not minorKeyNum == -1:
        minorKeyList = getKeySignature(key, minorKeyNum)

        # 7 note minor scales
        minorList = getNotes(key, minorKeyList)

        flatSecond = AlterNote("flat",minorList[1])
        second = minorList[1]
        sharpSecond = AlterNote("sharp",minorList[1])
        third = minorList[2]
        naturalThird = AlterNote("sharp",minorList[2])
        sharpThird = AlterNote("sharp",minorList[2])
        flatFourth = AlterNote("flat",minorList[3])
        fourth = minorList[3]
        sharpFourth = AlterNote("sharp",minorList[3])
        flatFifth = AlterNote("flat",minorList[4])
        fifth = minorList[4]
        sharpFifth = AlterNote("sharp",minorList[4])
        flatSixth = AlterNote("flat",minorList[5])
        sixth = minorList[5]
        naturalSixth = AlterNote("sharp",minorList[5])
        sharpSixth = AlterNote("sharp",minorList[5])
        diminishedSeventh = AlterNote("flat",minorList[6])
        seventh = minorList[6]
        naturalSeventh = AlterNote("sharp",minorList[6])
        sharpSeventh = AlterNote("sharp",minorList[6])

        # key signatures
        minorKeyString = ""
        for k in minorKeyList:
            minorKeyString += k+" "
        if minorKeyString == "":
            minorKeyString = "no sharps or flats"
        else:
            minorKeyString = minorKeyString[:-1]
        minorKeyImage = GetImage(key,minorList,minorKeyList)
        theoryCardsImg.write("the key signature of {{c1::"+key+"}} minor is {{c2::"+minorKeyString+"}}"+minorKeyImage+";musictheory::keysignatures\n")
        # relative major
        if key in sharpKeysMinor:
            relativeMajor = getDegree(key,"♯II")
        else:
            relativeMajor = getDegree(key,"♭III")
        if  keysContains(relativeMajor,majorKeys) != -1:
            theoryCards.write("the relative major of "+key+" minor is {{c1::"+relativeMajor+"}} major;musictheory::relativekeys\n")

        # melodic minor modes
        mMinorList = minorList[:5]+[naturalSixth,naturalSeventh]
        dorianFlatTwoList = [key,flatSecond,third]+minorList[3:5]+[naturalSixth]+[minorList[6]]
        lydianAugmentedList = minorList[:2]+[naturalThird,sharpFourth,sharpFifth,naturalSixth,naturalSeventh]
        lydianDominantList = minorList[:2]+[naturalThird,sharpFourth,fifth,naturalSixth,minorList[6]]
        aeolianDominantList = minorList[:2]+[naturalThird]+minorList[3:7]
        halfDiminishedList = minorList[:4]+[flatFifth]+minorList[5:7]
        alteredList = [key,flatSecond,sharpSecond,flatFourth,flatFifth]+minorList[5:7]
        # harmonic minor modes
        hMinorList = minorList[:6]+[naturalSeventh]
        locrianNaturalSixList = [key,flatSecond]+minorList[2:4]+[flatFifth,naturalSixth]+[minorList[6]]
        augmentedMajorList = minorList[:2]+[naturalThird,fourth,sharpFifth,naturalSixth,naturalSeventh]
        dorianSharpFourList = minorList[:3]+[sharpFourth,fifth,naturalSixth,seventh]
        phrygianDominantList = [key,flatSecond,naturalThird]+minorList[3:7]
        lydianSharpTwoList = [key,sharpSecond,naturalThird,sharpFourth,fifth,naturalSixth,naturalSeventh]
        superLocrianList = [key,flatSecond,third,flatFourth,flatFifth,sixth,diminishedSeventh]
        minorString = ""
        hMinorString = ""
        mMinorString = ""
        dorianFlatTwoString = ""
        lydianAugmentedString = ""
        lydianDominantString = ""
        aeolianDominantString = ""
        halfDiminishedString = ""
        alteredString = ""
        locrianNaturalSixString = ""
        augmentedMajorString = ""
        dorianSharpFourString = ""
        phrygianDominantString = ""
        lydianSharpTwoString = ""
        superLocrianString = ""
        for i in range(7):
            minorString += minorList[i]+" "
            hMinorString += hMinorList[i]+" "
            mMinorString += mMinorList[i]+" "
            dorianFlatTwoString += dorianFlatTwoList[i]+" "
            lydianAugmentedString += lydianAugmentedList[i]+" "
            lydianDominantString += lydianDominantList[i]+" "
            aeolianDominantString += aeolianDominantList[i]+" "
            halfDiminishedString += halfDiminishedList[i]+" "
            alteredString += alteredList[i]+" "
            locrianNaturalSixString += locrianNaturalSixList[i]+" "
            augmentedMajorString += augmentedMajorList[i]+" "
            dorianSharpFourString += dorianSharpFourList[i]+" "
            phrygianDominantString += phrygianDominantList[i]+" "
            lydianSharpTwoString += lydianSharpTwoList[i]+" "
            superLocrianString += superLocrianList[i]+" "
        minorString = minorString[:-1]
        hMinorString = hMinorString[:-1]
        mMinorString = mMinorString[:-1]
        dorianFlatTwoString = dorianFlatTwoString[:-1]
        lydianAugmentedString = lydianAugmentedString[:-1]
        lydianDominantString = lydianDominantString[:-1]
        aeolianDominantString = aeolianDominantString[:-1]
        halfDiminishedString = halfDiminishedString[:-1]
        alteredString = alteredString[:-1]
        locrianNaturalSixString = locrianNaturalSixString[:-1]
        augmentedMajorString = augmentedMajorString[:-1]
        dorianSharpFourString = dorianSharpFourString[:-1]
        phrygianDominantString = phrygianDominantString[:-1]
        lydianSharpTwoString = lydianSharpTwoString[:-1]
        superLocrianString = superLocrianString[:-1]
        minorImage = GetImage(key,minorList,[])
        hMinorImage = GetImage(key,hMinorList,[])
        mMinorImage = GetImage(key,mMinorList,[])
        dorianFlatTwoImage = GetImage(key,dorianFlatTwoList,[])
        lydianAugmentedImage = GetImage(key,lydianAugmentedList,[])
        lydianDominantImage = GetImage(key,lydianDominantList,[])
        aeolianDominantImage = GetImage(key,aeolianDominantList,[])
        halfDiminishedImage = GetImage(key,halfDiminishedList,[])
        alteredImage = GetImage(key,alteredList,[])
        locrianNaturalSixImage = GetImage(key,locrianNaturalSixList,[])
        augmentedMajorImage = GetImage(key,augmentedMajorList,[])
        dorianSharpFourImage = GetImage(key,dorianSharpFourList,[])
        phrygianDominantImage = GetImage(key,phrygianDominantList,[])
        lydianSharpTwoImage = GetImage(key,lydianSharpTwoList,[])
        superLocrianImage = GetImage(key,superLocrianList,[])
        theoryCardsImg.write("the notes in the "+key+" natural minor scale are {{c1::"+minorString+"}}"+minorImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" melodic minor scale are {{c1::"+mMinorString+"}}"+mMinorImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" dorian♭2 scale are {{c1::"+dorianFlatTwoString+"}}"+dorianFlatTwoImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" lydian augmented scale are {{c1::"+lydianAugmentedString+"}}"+lydianAugmentedImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" lydian dominant scale are {{c1::"+lydianDominantString+"}}"+lydianDominantImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" aeolian dominant scale are {{c1::"+aeolianDominantString+"}}"+aeolianDominantImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" half diminished scale are {{c1::"+halfDiminishedString+"}}"+halfDiminishedImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" altered scale are {{c1::"+alteredString+"}}"+alteredImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" harmonic minor scale are {{c1::"+hMinorString+"}}"+hMinorImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" locrian♮6 scale are {{c1::"+locrianNaturalSixString+"}}"+locrianNaturalSixImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" augmented major scale are {{c1::"+augmentedMajorString+"}}"+augmentedMajorImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" dorian#4 scale are {{c1::"+dorianSharpFourString+"}}"+dorianSharpFourImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" phrygian dominant scale are {{c1::"+phrygianDominantString+"}}"+phrygianDominantImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" lydian#2 scale are {{c1::"+lydianSharpTwoString+"}}"+lydianSharpTwoImage+";musictheory::scales\n")
        theoryCardsImg.write("the notes in the "+key+" super-locrian scale are {{c1::"+superLocrianString+"}}"+superLocrianImage+";musictheory::scales\n")

        # bebop melodic minor scale
        bebopMMinorList = minorList[:6]+[naturalSixth,naturalSeventh]
        bebopMMinorString = ""
        for i in range(8):
            bebopMMinorString += bebopMMinorList[i] + " "
        bebopMMinorString = bebopMMinorString[:-1]
        bebopMMinorImage = GetImage(key,bebopMMinorList,[])
        theoryCardsImg.write("the notes in the "+key+" bebop melodic minor scale are {{c1::"+bebopMMinorString+"}}"+bebopMMinorImage+";musictheory::scales\n")
        
        # melodic minor modes
        melodicMinorModes = [second+" dorian♭2",third+" lydian augmented",fourth+" lydian dominant",fifth+" aeolian dominant",naturalSixth+" half diminished",naturalSeventh+" altered"]
        melodicMinorModeImages = [dorianFlatTwoImage,lydianAugmentedImage,lydianDominantImage,aeolianDominantImage,halfDiminishedImage,alteredImage]
        for i in range(6):
            mode = modeDegrees[i]
            melodicMinorMode = melodicMinorModes[i]
            melodicMinorModeImage = melodicMinorModeImages[i]
            theoryCardsImg.write("{{c1::"+melodicMinorMode+"}} is the "+mode+" mode of {{c2::"+key+" melodic minor}}"+melodicMinorModeImage+";musictheory::modes\n")

        # harmonic minor modes
        harmonicMinorModes = [second+" locrian♮6",third+" augmented major",fourth+" dorian♯4",fifth+" phrygian dominant",sixth+" lydian♯2",naturalSeventh+" super-locrian"]
        harmonicMinorModeImages = [locrianNaturalSixImage,augmentedMajorImage,dorianSharpFourImage,phrygianDominantImage,lydianSharpTwoImage,superLocrianImage]
        for i in range(6):
            mord = modeDegrees[i]
            harmonicMinorMode = harmonicMinorModes[i]
            harmonicMinorModeImage = harmonicMinorModeImages[i]
            theoryCardsImg.write("{{c1::"+harmonicMinorMode+"}} is the "+mode+" mode of {{c2::"+key+" harmonic minor}}"+harmonicMinorModeImage+";musictheory::modes\n")

        # minor scale degree cards
        minorDegrees = {"♭2nd":flatSecond,"2nd":second,"3rd":third,"4th":fourth,"♯4th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth,"♭9th":flatSecond,"9th":second,"11th":fourth,"♯11th":sharpFourth}
        for degree in minorDegrees:
            degreeImage = GetImage(key,minorList,[minorDegrees[degree]])
            theoryCardsImg.write("{{c1::"+minorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} minor"+degreeImage+";musictheory::scaledegrees\n")
        # minor scale degrees 2nd cloze
        minorDegrees1 = {"♭2nd/♭9th":flatSecond,"2nd/9th":second,"3rd":third,"4th/11th":fourth,"♯4th/♯11th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth}
        for degree in minorDegrees1:
            degreeImage = GetImage(key,minorList,[minorDegrees1[degree]])
            theoryCardsImg.write(minorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" minor"+degreeImage+";musictheory::scaledegrees\n")
        # natural minor scale degree cards
        minorDegrees = {"6th":sixth,"7th":seventh,"13th":sixth}
        for degree in minorDegrees:
            degreeImage = GetImage(key,minorList,[minorDegrees[degree]])
            theoryCardsImg.write("{{c1::"+minorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} natural minor"+degreeImage+";musictheory::scaledegrees\n")
        # natural minor scale degrees 2nd cloze
        minorDegrees1 = {"6th/13th":sixth,"7th":seventh}
        for degree in minorDegrees1:
            degreeImage = GetImage(key,minorList,[minorDegrees1[degree]])
            theoryCardsImg.write(minorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" natural minor"+degreeImage+";musictheory::scaledegrees\n")
        # harmonic minor scale degree cards
        minorDegrees = {"6th":sixth,"7th":sharpSeventh,"13th":sixth}
        for degree in minorDegrees:
            degreeImage = GetImage(key,hMinorList,[minorDegrees[degree]])
            theoryCardsImg.write("{{c1::"+minorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} harmonic minor"+degreeImage+";musictheory::scaledegrees\n")
        # harmonic minor scale degrees 2nd cloze
        minorDegrees1 = {"6th/13th":sixth,"7th":sharpSeventh}
        for degree in minorDegrees1:
            degreeImage = GetImage(key,hMinorList,[minorDegrees1[degree]])
            theoryCardsImg.write(minorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" harmonic minor"+degreeImage+";musictheory::scaledegrees\n")
        # melodic minor scale degree cards
        minorDegrees = {"6th":sharpSixth,"7th":sharpSeventh,"13th":sharpSixth}
        for degree in minorDegrees:
            degreeImage = GetImage(key,hMinorList,[minorDegrees[degree]])
            theoryCardsImg.write("{{c1::"+minorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} melodic minor"+degreeImage+";musictheory::scaledegrees\n")
        # melodic minor scale degrees 2nd cloze
        minorDegrees1 = {"6th/13th":sharpSixth,"7th":sharpSeventh}
        for degree in minorDegrees1:
            degreeImage = GetImage(key,hMinorList,[minorDegrees1[degree]])
            theoryCardsImg.write(minorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" melodic minor"+degreeImage+";musictheory::scaledegrees\n")

        # natural minor triads functional harmony
        nMinorDegrees = ["i","ii","III","iv","v","VI","VII"]
        nMinorFunctionalChords = ["-","o","","-","-","",""]
        for i in range(len(nMinorDegrees)):
            degree = nMinorDegrees[i]
            chord = nMinorFunctionalChords[i]
            chordList = []
            for j in range(0,6,2):
                n = i+j
                if n >= 7:
                    n -= 7
                chordList = chordList + [minorList[n]]
            note = minorList[i]
            chordImage = GetImage(key,minorList+minorList,chordList)
            theoryCardsImg.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+key+"}} natural minor"+chordImage+";musictheory::functionalharmony\n")
        # natural minor 7th chord functional harmony
        nMinorDegrees = ["i","ii","III","iv","v","VI","VII"]
        nMinorFunctionalChords = ["-7","-7♭5","Δ7","-7","-7","Δ7","7"]
        for i in range(len(nMinorDegrees)):
            degree = nMinorDegrees[i]
            chord = nMinorFunctionalChords[i]
            chordList = []
            for j in range(0,8,2):
                n = i+j
                if n >= 7:
                    n -= 7
                chordList = chordList + [minorList[n]]
            note = minorList[i]
            chordImage = GetImage(key,minorList+minorList,chordList)
            theoryCardsImg.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+key+"}} natural minor"+chordImage+";musictheory::functionalharmony\n")
        # harmonic minor triad functional harmony
        hMinorDegrees = ["i","ii","III","iv","V","VI","vii"]
        hMinorFunctionalChords = ["-","o","+","-","","","o"]
        for i in range(len(hMinorDegrees)):
            degree = hMinorDegrees[i]
            chord = hMinorFunctionalChords[i]
            chordList = []
            for j in range(0,6,2):
                n = i+j
                if n >= 7:
                    n -= 7
                chordList = chordList + [hMinorList[n]]
            note = hMinorList[i]
            chordImage = GetImage(key,hMinorList+hMinorList,chordList)
            theoryCardsImg.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+key+"}} harmonic minor"+chordImage+";musictheory::functionalharmony\n")
        # harmonic minor 7th chord functional harmony
        hMinorDegrees = ["i","ii","III","iv","V","VI","vii"]
        hMinorFunctionalChords = ["-Δ7","-7♭5","Δ7♯5","-7","7","Δ7","o7"]
        for i in range(len(hMinorDegrees)):
            degree = hMinorDegrees[i]
            chord = hMinorFunctionalChords[i]
            chordList = []
            for j in range(0,8,2):
                n = i+j
                if n >= 7:
                    n -= 7
                chordList = chordList + [hMinorList[n]]
            note = hMinorList[i]
            chordImage = GetImage(key,hMinorList+hMinorList,chordList)
            theoryCardsImg.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+key+"}} harmonic minor"+chordImage+";musictheory::functionalharmony\n")
        # melodic minor triad functional harmony
        mMinorDegrees = ["i","ii","III","IV","V","vi","vii"]
        mMinorFunctionalChords = ["-","-","+","","","o","o"]
        for i in range(len(mMinorDegrees)):
            degree = mMinorDegrees[i]
            chord = mMinorFunctionalChords[i]
            chordList = []
            for j in range(0,6,2):
                n = i+j
                if n >= 7:
                    n -= 7
                chordList = chordList + [mMinorList[n]]
            note = mMinorList[i]
            chordImage = GetImage(key,mMinorList+mMinorList,chordList)
            theoryCardsImg.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+key+"}} melodic minor"+chordImage+";musictheory::functionalharmony\n")
        # melodic minor 7th chord functional harmony
        mMinorDegrees = ["i","ii","III","IV","V","vi","vii"]
        mMinorFunctionalChords = ["-Δ7","-7","Δ7♯5","7","7","-7♭5","-7♭5"]
        for i in range(len(mMinorDegrees)):
            degree = mMinorDegrees[i]
            chord = mMinorFunctionalChords[i]
            chordList = []
            for j in range(0,8,2):
                n = i+j
                if n >= 7:
                    n -= 7
                chordList = chordList + [mMinorList[n]]
            note = mMinorList[i]
            chordImage = GetImage(key,mMinorList+mMinorList,chordList)
            theoryCardsImg.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+key+"}} melodic minor"+chordImage+";musictheory::functionalharmony\n")

        # minor guide tones cards
        minorMajor7AGuideTonesImage = GetImage(key,[third,naturalSeventh],[])
        minorMajor7BGuideTonesImage = GetImage(key,[naturalSeventh,third],[])
        theoryCardsImg.write("the guide tones of "+key+"-Δ7 in inversion A are {{c1::"+third+" and "+naturalSeventh+"}} (in order from lowest to highest)"+minorMajor7AGuideTonesImage+";musictheory::voicings\n")
        theoryCardsImg.write("the guide tones of "+key+"-Δ7 in inversion B are {{c1::"+naturalSeventh+" and "+third+"}} (in order from lowest to highest)"+minorMajor7BGuideTonesImage+";musictheory::voicings\n")

        # 3 note minor chord voicings cards
        # minor
        inversions = ["root position","first inversion","second inversion","third inversion"]
        minorChordNotes = [key,third,fifth]
        for i in range(3):
            minorChordString = ""
            minorChordList = []
            inversion = inversions[i]
            for n in range(3):
                note = i+n
                if note>=3:
                    note-=3
                minorChordString += minorChordNotes[note]+" "
                minorChordList += [minorChordNotes[note]]
            minorChordString = minorChordString[:-1]
            minorChordImage = GetImage(key,minorChordList,[])
            theoryCardsImg.write("the notes in a "+key+"- chord in "+inversion+" are {{c2::"+minorChordString+"}} (in order from lowest to highest)"+minorChordImage+";musictheory::voicings\n")

        # 4 note minor chord voicing cards
        # minor7b5 minor-major7
        minor7FlatFiveChordNotes = [key,third,flatFifth,seventh]
        minorMajor7ChordNotes = [key,third,fifth,naturalSeventh]
        for i in range(4):
            minor7FlatFiveString = ""
            minor7FlatFiveList = []
            minorMajor7String = ""
            minorMajor7List = []
            inversion = inversions[i]
            for n in range(4):
                note = i+n
                if note>=4:
                    note -= 4
                minor7FlatFiveString += minor7FlatFiveChordNotes[note]+" "
                minor7FlatFiveList += [minor7FlatFiveChordNotes[note]]
                minorMajor7String += minorMajor7ChordNotes[note]+" "
                minorMajor7List += [minorMajor7ChordNotes[note]]
            minor7FlatFiveString = minor7FlatFiveString[:-1]
            minorMajor7String = minorMajor7String[:-1]
            minor7FlatFiveImage = GetImage(key,minor7FlatFiveList,[])
            minorMajor7Image = GetImage(key,minorMajor7List,[])
            theoryCardsImg.write("the notes in a "+key+"-7♭5 chord in "+inversion+" are {{c1::"+minor7FlatFiveString+"}} (in order from lowest to highest)"+minor7FlatFiveImage+";musictheory::voicings\n")
            theoryCardsImg.write("the notes in a "+key+"-Δ7 chord in "+inversion+" are {{c1::"+minorMajor7String+"}} (in order from lowest to highest)"+minorMajor7Image+";musictheory::voicings\n")

        # rootless minor chord voicing cards
        # minor7b5b9 dominant7b9b13 minor-major9
        rootlessInversions = ["A","","B"]
        minorRootlessiiNotes = [third,flatFifth,seventh,flatSecond]
        minorRootlessVNotes = [seventh,flatSecond,naturalThird,sixth]
        minorRootlessINotes = [third,fifth,naturalSeventh,second]
        for i in range(0,3,2):
            minorRootlessiiString = ""
            minorRootlessiiList = []
            minorRootlessVString = ""
            minorRootlessVList = []
            minorRootlessIString = ""
            minorRootlessIList = []
            rootlessInversion = rootlessInversions[i]
            minorRootlessiiString = ""
            minorRootlessVString = ""
            minorRootlessIString = ""
            rootlessInversion = rootlessInversions[i]
            for n in range(4):
                note = i+n
                if note >= 4:
                    note -= 4
                minorRootlessiiString += minorRootlessiiNotes[note]+" "
                minorRootlessiiList += [minorRootlessiiNotes[note]]
                minorRootlessVString += minorRootlessVNotes[note]+" "
                minorRootlessVList += [minorRootlessVNotes[note]]
                minorRootlessIString += minorRootlessINotes[note]+" "
                minorRootlessIList += [minorRootlessINotes[note]]
            minorRootlessiiString = minorRootlessiiString[:-1]
            minorRootlessVString = minorRootlessVString[:-1]
            minorRootlessIString = minorRootlessIString[:-1]
            minorRootlessiiImage = GetImage(key,minorRootlessiiList,[])
            minorRootlessVImage = GetImage(key,minorRootlessVList,[])
            minorRootlessIImage = GetImage(key,minorRootlessIList,[])
            theoryCardsImg.write("the notes in a type "+rootlessInversion+" rootless "+key+"-7♭9♭5 chord are {{c2::"+minorRootlessiiString+"}} (in order from lowest to highest)"+minorRootlessiiImage+";musictheory::voicings\n")
            theoryCardsImg.write("the notes in a type "+rootlessInversion+" rootless "+key+"7♭9♭13 chord are {{c2::"+minorRootlessVString+"}} (in order from lowest to highest)"+minorRootlessVImage+";musictheory::voicings\n")
            theoryCardsImg.write("the notes in a type "+rootlessInversion+" rootless "+key+"-Δ9 chord are {{c2::"+minorRootlessIString+"}} (in order from lowest to highest)"+minorRootlessIImage+";musictheory::voicings\n")

        # extended minor chord voicing cards
        # minor6 minor6/9 minor9b13
        # 4 note chords
        minor6List = [key,third,fifth,naturalSixth]
        minor6String = ""
        for i in range(4):
            minor6String += minor6List[i]+" "
        minor6String = minor6String[:-1]
        minor6Image = GetImage(key,minor6List,[])
        theoryCardsImg.write("the notes in a "+key+"-6 chord are {{c1::"+minor6String+"}} (in order from lowest to highest)"+minor6Image+";musictheory::voicings\n")

    intervals = {"minor 2nd":1,"major 2nd":2,"minor 3rd":3,"major 3rd":4,"perfect 4th":5,"tritone":6,"perfect 5th":7,"minor 6th":8,"major 6th":9,"minor 7th":10,"major 7th":11,"minor 9th":13,"major 9th":14,"minor 10th":15,"major 10th":16,"perfect 11th":17,"perfect 12th":19,"minor 13th":20,"major 13th":21,"minor 14th":22,"major 14th":23,"perfect 15th":24,"diminished 2nd":0,"augmented 1st":1,"diminishd 3rd":2,"augmented 2nd":3,"diminished 4th":4,"augmented 3rd":5,"diminished 5th":6,"augmented 4th":6,"diminished 6th":7,"augmented 5th":8,"diminished 7th":9,"augmented 6th":10,"diminished 8th":11,"augmented 7th":12,"diminished 9th":12,"augmented 8th":13,"diminished 10th":14,"augmented 9th":15,"diminished 11th":16,"augmented 10th":17,"diminished 12th":18,"augmented 11th":18,"diminished 13th":19,"augmented 12th":20,"diminished 14th":21,"augmented 13th":22,"diminished 15th":23,"augmented 14th":24,"augmented 15th":25}
    for interval in intervals:
        keyIndex = keysContains(key, keysEnharmonic)
        intervalNum = intervals[interval]
        intervalAboveIndex = keyIndex+intervalNum
        while intervalAboveIndex > 11:
            intervalAboveIndex -=12
        intervalAbove = keysEnharmonic[intervalAboveIndex]
        if "/" in intervalAbove:
            noteAbove = intervalAbove.split("/")[1]
        else:
            noteAbove = intervalAbove
        intNotesList = [key,noteAbove]
        intervalImage = GetImage(key,intNotesList,[])
        theoryCardsImg.write("{{c1::"+intervalAbove+"}} is a "+interval+" above {{c2::"+key+"}}"+intervalImage+";musictheory::intervals\n")
        theoryCardsImg.write("{{c1::"+key+"}} is a "+interval+" below {{c2::"+intervalAbove+"}}"+intervalImage+";musictheory::intervals\n")

    slashChords = {"[♭II]/[I]":"[♭II]Δ or [I]sus♭9♭13","[II]/[I]":"[I]Δ♯4","[♭III]/[I]":"[I]-7","[III]/[I]":"[I]Δ♯5","[IV]/[I]":"[IV]","[♭V]/[I]":"[I]7♭9","[V]/[I]":"[I]Δ","[♭VI]/[I]":"[♭VI]","[VI]/[I]":"[I]7♭9","[♭VII]/[I]":"[I]sus","[VII]/[I]":"[I]Δ♯4♯9"}
    for slashChord in slashChords:
        slashChordName = slashChord
        eqChordName = slashChords[slashChord]
        slashChordDegrees = re.findall("\[(.+?)\]",slashChord)
        triadI = slashChordDegrees[0]
        triadINote = getDegree(key, triadI)
        triadIIINote = getDegree(triadINote,"III")
        triadVNote = getDegree(triadINote,"V")
        triadList = [triadINote,triadIIINote,triadVNote]
        for slashChordDegree in slashChordDegrees:
            slashChordDegreeNote = getDegree(key, slashChordDegree)
            slashChordName = re.sub("^(.*?)\[.+?\]","\g<1>"+slashChordDegreeNote,slashChordName)
        eqChordDegrees = re.findall("\[(.+?)\]",eqChordName)
        for eqChordDegree in eqChordDegrees:
            eqChordDegreeNote = getDegree(key, eqChordDegree)
            eqChordName = re.sub("^(.*?)\[.+?\]","\g<1>"+eqChordDegreeNote,eqChordName)
        slashChordImage = GetImage(triadINote,[key,"8va"]+triadList,[])
        theoryCardsImg.write("{{c1::"+slashChordName+"::slash chord}} is equivalent to {{c2::"+eqChordName+"::chord name}} in traditional notation"+slashChordImage+";musictheory::slashchords\n")

    if not majorKeyNum == -1:
        second = majorList[1]
        flatThird = AlterNote("flat",majorList[2])
        third = majorList[2]
        fourth = majorList[3]
        sharpFourth = AlterNote("sharp",majorList[3])
        flatFifth = AlterNote("flat",majorList[4])
        fifth = majorList[4]
        flatSixth = AlterNote("flat",majorList[5])
        sixth = majorList[5]
        diminishedSeventh = AlterNote("flat",AlterNote("flat",majorList[6]))
        flatSeventh = AlterNote("flat",majorList[6])
        seventh = majorList[6]
    elif not minorKeyNum == -1:
        second = minorList[1]
        flatThird = minorList[2]
        third = AlterNote("sharp",minorList[2])
        fourth = minorList[3]
        sharpFourth = AlterNote("sharp",minorList[3])
        flatFifth = AlterNote("flat",minorList[4])
        fifth = minorList[4]
        sixth = AlterNote("sharp",minorList[5])
        diminishedSeventh = AlterNote("flat",minorList[6])
        flatSeventh = minorList[6]
        seventh = AlterNote("sharp",minorList[6])

    # minor pentatonic scales
    minorPentatonicList = [key,flatThird,fourth,fifth,flatSeventh]
    minorPentatonicString = ""
    for i in range(5):
        minorPentatonicString += minorPentatonicList[i]+" "
    minorPentatonicString = minorPentatonicString[:-1]
    minorPentatonicImage = GetImage(key,minorPentatonicList,[])
    theoryCardsImg.write("the notes in the "+key+" minor pentatonic scale are {{c1::"+minorPentatonicString+"}}"+minorPentatonicImage+";musictheory::scales\n")

    # blues scale
    bluesList = [key,flatThird,fourth,sharpFourth,fifth,flatSeventh]
    bluesString = ""
    for i in range(6):
        bluesString += bluesList[i]+" "
    bluesImage = GetImage(key,bluesList,[])
    bluesString = bluesString[:-1]
    theoryCardsImg.write("the notes in the "+key+" blues scale are {{c1::"+bluesString+"}}"+bluesImage+";musictheory::scales\n")

    # diminished scales
    HWDiminishedList = [key, flatSecond, sharpSecond, third, sharpFourth, fifth, sixth, flatSeventh]
    WHDiminishedList = [key,second,flatThird,fourth,flatFifth,flatSixth,diminishedSeventh,seventh]
    HWDiminishedString = ""
    WHDiminishedString = ""
    for i in range(8):
        HWDiminishedString += HWDiminishedList[i]+" "
        WHDiminishedString += WHDiminishedList[i]+" "
    HWDiminishedString = HWDiminishedString[:-1]
    WHDiminishedString = WHDiminishedString[:-1]
    HWDiminishedImage = GetImage(key,HWDiminishedList,[])
    WHDiminishedImage = GetImage(key,WHDiminishedList,[])
    theoryCardsImg.write("the notes in the "+key+" half-whole diminished scale are {{c1::"+HWDiminishedString+"}}"+HWDiminishedImage+";musictheory::scales\n")
    theoryCardsImg.write("the notes in the "+key+" half-whole diminished scale are {{c1::"+WHDiminishedString+"}}"+WHDiminishedImage+";musictheory::scales\n")

    # dominant7 diminished7 guide tones cards
    dominant7AGuideTones = GetImage(key,[third,flatSeventh],[])
    dominant7BGuideTones = GetImage(key,[flatSeventh,third],[])
    diminished7AGuideTones = GetImage(key,[flatThird,diminishedSeventh],[])
    diminished7BGuideTones = GetImage(key,[diminishedSeventh,flatThird],[])
    theoryCardsImg.write("the guide tones of "+key+"7 in inversion A are {{c1::"+third+" and "+flatSeventh+"}} (in order from lowest to highest)"+dominant7AGuideTones+";musictheory::voicings\n")
    theoryCardsImg.write("the guide tones of "+key+"7 in inversion B are {{c1::"+flatSeventh+" and "+third+"}} (in order from lowest to highest)"+dominant7BGuideTones+";musictheory::voicings\n")
    theoryCardsImg.write("the guide tones of "+key+"o7 in inversion A are {{c1::"+flatThird+" and "+diminishedSeventh+"}} (in order from lowest to highest)"+diminished7AGuideTones+";musictheory::voicings\n")
    theoryCardsImg.write("the guide tones of "+key+"o7 in inversion B are {{c1::"+diminishedSeventh+" and "+flatThird+"}} (in order from lowest to highest)"+diminished7BGuideTones+";musictheory::voicings\n")

    # 3 note diminished chord voicings cards
    # diminished inversions
    inversions = ["root position","1st inversion","2nd inversion","3rd inversion"]
    diminishedNotes = [key,flatThird,flatFifth]
    for i in range(3):
        diminishedString = ""
        diminishedList = []
        inversion = inversions[i]
        for n in range(3):
            note = i+n
            if note>=3:
                note -= 3
            diminishedString += diminishedNotes[note]+" "
            diminishedList += [diminishedNotes[note]]
        diminishedString = diminishedString[:-1]
        diminishedImage = GetImage(key,diminishedList,[])
        theoryCardsImg.write("the notes in a "+key+"o chord in "+inversion+" are {{c2::"+diminishedString+"}} (in order from lowest to highest)"+diminishedImage+";musictheory::voicings\n")

    # 4 note chord voicing cards
    # dominant7 diminished7 inversions
    dominant7Notes = [key,third,fifth,flatSeventh]
    diminished7Notes = [key,flatThird,flatFifth,diminishedSeventh]
    for i in range(4):
        dominant7String = ""
        diminished7String = ""
        dominant7List = []
        diminished7List = []
        inversion = inversions[i]
        for n in range(4):
            note = i+n
            if note >=4:
                note -= 4
            dominant7String += dominant7Notes[note]+" "
            dominant7List += [dominant7Notes[note]]
            diminished7String += diminished7Notes[note]+" "
            diminished7List += [diminished7Notes[note]]
        dominsnt7String = dominant7String[:-1]
        diminished7String = diminished7String[:-1]
        dominant7Image = GetImage(key,dominant7List,[])
        diminished7Image = GetImage(key,diminished7List,[])
        theoryCardsImg.write("the notes in a "+key+"7 chord in "+inversion+" are {{c2::"+dominant7String+"}} (in order from lowest to highest)"+dominant7Image+";musictheory::voicings\n")
        theoryCardsImg.write("the notes in a "+key+"o7 chord in "+inversion+" are {{c2::"+diminished7String+"}} (in order from lowest to highest)"+diminished7Image+";musictheory::voicings\n")

    # other chord voicing cards
    sus2List = [key,second,fifth]
    sus4List = [key,fourth,fifth]
    sus2String = ""
    sus4String = ""
    for i in range(3):
        sus2String += sus2List[i]+" "
        sus4String += sus4List[i]+" "
    sus2String = sus2String[:-1]
    sus4String = sus4String[:-1]
    sus2Image = GetImage(key,sus2List,[])
    sus4Image = GetImage(key,sus4List,[])
    theoryCardsImg.write("the notes in a "+key+"sus2 chord are {{c1::"+sus2String+"}} (in order from lowest to highest)"+sus2Image+";musictheory::voicings\n")
    theoryCardsImg.write("the notes in a "+key+"sus4 chord are {{c1::"+sus4String+"}} (in order from lowest to highest)"+sus4Image+";musictheory::voicings\n")

    sevenSus2List = [key,second,fifth,flatSeventh]
    sevenSus4List = [key,fourth,fifth,flatSeventh]
    sevenSus2String = ""
    sevenSus4String = ""
    for i in range(4):
        sevenSus2String += sevenSus2List[i]+" "
        sevenSus4String += sevenSus4List[i]+" "
    sevenSus2String = sevenSus2String[:-1]
    sevenSus4String = sevenSus4String[:-1]
    sevenSus2Image = GetImage(key,sevenSus2List,[])
    sevenSus4Image = GetImage(key,sevenSus4List,[])
    theoryCardsImg.write("the notes in a "+key+"7sus2 chord are {{c1::"+sevenSus2String+"}} (in order from lowest to highest)"+sevenSus2Image+";musictheory::voicings\n")
    theoryCardsImg.write("the notes in a "+key+"7sus4 chord are {{c1::"+sevenSus4String+"}} (in order from lowest to highest)"+sevenSus4Image+";musictheory::voicings\n")

    dominant9List = [key,third,fifth,flatSeventh,second]
    dominant9String = ""
    for i in range(5):
        dominant9String += dominant9List[i]+" "
    dominant9String = dominant9String[:-1]
    dominant9Image = GetImage(key,dominant9List,[])
    theoryCardsImg.write("the notes in a "+key+"9 chord are {{c1::"+dominant9String+"}} (in order from lowest to highest)"+dominant9Image+";musictheory::voicings\n")

    dominantSharp11List = [key,third,fifth,flatSeventh,second,sharpFourth]
    dominantSharp11String = ""
    for i in range(6):
        dominantSharp11String += dominantSharp11List[i]+" "
    dominantSharp11String = dominantSharp11String[:-1]
    dominantSharp11Image = GetImage(key,dominantSharp11List,[])
    theoryCardsImg.write("the notes in a "+key+"♯11 chord are {{c1::"+dominantSharp11String+"}} (in order from lowest to highest)"+dominantSharp11Image+";musictheory::voicings\n")

    dominant13Sharp11List = [key,third,fifth,flatSeventh,second,sharpFourth,sixth]
    dominant13Sharp11String = ""
    for i in range(7):
        dominant13Sharp11String += dominant13Sharp11List[i]+" "
    dominant13Sharp11String = dominant13Sharp11String[:-1]
    dominant13Sharp11Image = GetImage(key,dominant13Sharp11List,[])
    theoryCardsImg.write("the notes in a "+key+"13♯11 chord are {{c1::"+dominant13Sharp11String+"}} (in order from lowest to highest)"+dominant13Sharp11Image+";musictheory::voicings\n")

    chords = {"[I]": ["[I] major","[I] lydian"],
          "[I]-": ["[I] melodic minor","[I] bebop melodic minor","[IV] pentatonic","[III] in-sen"],
          # major modes
          "[I]Δ": ["[I] major","[I] bebop major","[I] pentatonic","[II] pentatonic","[V] pentatonic","[III] minor pentatonic","[VI] minor pentatonic","[III] in-sen","[VI] blues scale","[III] blues scale"],
          "[II]-7": ["[II] dorian","[II] bebop dorian","[I] pentatonic","[IV] pentatonic","[V] pentatonic","[II] minor pentatonic","[III] minor pentatonic","[VI] minor pentatonic","[III] in-sen","[II] blues scale","[III] blues scale","[VI] blues scale"],
          "[III]sus♭9": ["[III] phrygian","[III] dorian♭2","[V] pentatonic","[III] in-sen"],
          "[IV]Δ♯4": ["[IV] lydian","[III] in-sen"],
          "[V]7": ["[V] mixolydian","[V] bebop dominant","[V] pentatonic","[I] minor pentatonic","[II] minor pentatonic","[III] minor pentatonic""[V] minor pentatonic","[I] blues scale","[II] blues scale","[III] blues scale","[V] blues scale","[III] in-sen"],
          "[V]7sus": ["[V] mixolydian","[III] in-sen"],
          "[VI]-♭6": ["[VI] aeolian","[III] in-sen"],
          "[VII]7ø": ["[VII] locrian","[VII] half diminished","[V] pentatonic","[III] in-sen"],
          # melodic minor modes
          "[I]7-Δ": ["[I] melodic minor","[I] bebop melodic minor","[IV] pentatonic","[II] in-sen"],
          "[III]Δ♯5": ["[III] lydian augmented","[IV] pentatonic","[II] in-sen"],
          "[IV]7♯11": ["[IV] lydian dominant","[IV] pentatonic","[II] in-sen"],
          "[I]-Δ/[V]": ["[V] aeolian dominant","[IV] pentatonic","[II] in-sen"],
          "[VII]alt": ["[VII] altered","[IV] pentatonic","[II] in-sen"],
          # symmetric scales
          "[V]7♭9": ["[V] half-whole diminished"],
          "[I]o": ["[I] whole-half diminished"],
          "[V]7♯5": ["[V] whole-tone"],
          # slash chords
          "[♭II]/[I]": ["[I] phrygian","[I] locrian"],
          "[II]/[I]": ["[I] lydian"],
          "[♭III]/[I]": ["[I] dorian"],
          "[III]/[I]": ["[I] lydian augmented"],
          "[IV]/[I]": ["[IV] major"],
          "[♭V]/[I]": ["[I] altered","[I] half-whole diminished"],
          "[V]/[I]": ["[I] major"],
          "[♭VI]/[I]": ["[♭VI] major"],
          "[VI]/[I]": ["[I] half-whole diminished"],
          "[♭VII]/[I]": ["[I] mixolydian"],
          "[VII]/[I]": ["[I] whole-half diminished"]}
    for chord in chords:
        chordName = chord
        chordDegrees = re.findall("\[(.+?)\]",chord)
        for chordDegree in chordDegrees:
            chordDegreeNote = getDegree(key, chordDegree)
            chordName = re.sub("^(.*?)\[.+?\]","\g<1>"+chordDegreeNote,chordName)
        scalesString = ""
        scalesStringCloze = ""
        count = 0
        for scale in chords[chord]:
           count += 1
           scaleDegree = re.findall("\[(.+?)\]",scale)[0]
           scaleDegreeNote = getDegree(key,scaleDegree)
           scalesStringCloze += "{{c"+str(count)+":"+re.sub("\[.+?\]",scaleDegreeNote,scale)+"}}, "
           scalesString += re.sub("\[.+?\]",scaleDegreeNote,scale)+", "
        scalesString = scalesString[:-2]
        scalesStringCloze = scalesStringCloze[:-2]
        theoryCards.write("which scales can you play over a "+chordName+" chord?"+scalesStringCloze+";musictheory::chordscales\n")
        theoryCards.write("which scales can you play over a "+chordName+" chord?"+scalesString+";musictheory::chordscales\n")

    scales = {# major modes
          "[I] major":["[I]Δ","[I]","[I]/[V]","[V]/[I]","[I]/[III]"],
          "[II] dorian":["[II]-7","[IV]/[II]"],
          "[III] phrygian":["[III]sus♭9","[IV]/[III]"],
          "[IV] lydian":["[IV]Δ♯4","[IV]","[V]/[IV]"],
          "[V] mixolydian":["[V]7","[V]sus","[IV]/[V]"],
          "[VI] aeolian":["[VI]-♭6"],
          "[VII] locrian":["[VII]ø","[I]/[VII]"],
          # melodic minor modes
          "[I] melodic minor":["[I]-Δ"],
          "[II] dorian♭2":["[II]sus♭9"],
          "[I] lydian augmented":["[I]Δ♯5","[III]/[I]"],
          "[IV] lydian dominant":["[IV]7♯11"],
          "[V] aeolian dominant":["[I]-Δ/[V]"],
          "[VI] half diminished":["[VI]ø"],
          "[VII] altered":["[VII]alt","[IV]/[VII]"],
          # symmetric scales
          "[I] half-whole diminished":["[I]7♭9","[♭V]/[I]","[VI]/[I]"],
          "[I] whole-half diminished":["[I]o","[VII]/[I]"],
          "[V] whole-tone":["[V]7♯5"],
          # bebop scales
          "[I] bebop major":["[I]Δ"],
          "[II] bebop dorian":["[II]-7"],
          "[V] bebop dominant":["[V]7"],
          "[I] bebop melodic minor":["[I]-Δ"],
          # pentatonic scales
          "[I] pentatonic":["[II]-7","[VI]-7","[V]-7","[I]7","[IV]Δ","[I]Δ","[♭VII]","[V]-Δ","[VI]sus♭9","[VII]Δ♯5","[I]7♯11","[V]-Δ/[II]","[III]ø","[♭V]alt"],
          "[I] minor pentatonic":["[I]7","[IV]7","[V]7","[IV]-7","[I]-7","[♭VII]-7","[♭III]7","[♭III]Δ","[♭VI]Δ"],
          "[I] blues scale":["[I]7","[IV]7","[V]7","[IV]-7","[I]-7","[♭VII]-7","[♭III]7","[♭III]Δ","[♭VI]Δ"],
          "[III] in-sen scale":["[I]Δ","[II]-7","[III]sus♭9","[IV]Δ♯4","[V]7","[V]sus","[VI]-♭6","[VII]ø","[II]-Δ","[IV]Δ♯5","[V]7♯11","[II]-Δ/[VI]","[♭II]alt"]}
    for scale in scales:
        scaleName = ""
        scaleDegree = re.findall("\[(.+?)\]",scale)[0]
        scaleDegreeNote = getDegree(key,scaleDegree)
        scaleName = re.sub("\[.+?\]",scaleDegreeNote,scale)
        chordsStringCloze = ""
        chordsString = ""
        count = 0
        for chord in scales[scale]:
            count += 1
            chordName = chord
            chordDegrees = re.findall("\[(.+?)\]",chord)
            for chordDegree in chordDegrees:
                chordDegreeNote = getDegree(key, chordDegree)
                chordName = re.sub("^(.*?)\[.+?\]","\g<1>"+chordDegreeNote,chordName)
            chordsStringCloze += "{{c"+str(count)+":"+chordName+"}}, "
            chordsString += chordName+", "
        chordsString = chordsString[:-2]
        chordsStringCloze = chordsStringCloze[:-2]
        theoryCards.write("which chords can you play a "+scaleName+" over?"+chordsString+";musictheory::chordscales\n")
        theoryCards.write("which chords can you play a "+scaleName+" over?"+chordsStringCloze+";musictheory::chordscales\n")
