#TODO add chord substitution cards ala Jazz Theory Book
#TODO add more chord voicing cards
#TODO make sure chord-scale cards agree with https://newjazz.dk/Compendiums/scales_of_harmonies.pdf
#TODO also make sure they agree with https://www.newjazz.dk/Compendiums/Systematic_Scale_Chart.pdf
#TODO add cards for the chords mentioned in the jazz theory book and how they relate to their respective scales?
#TODO add pentatonic scale modes?
import re
theoryCards = open("theoryCards.txt","w")
notes = ["C","D","E","F","G","A","B"]
keysEnharmonic = ["C","C♯/D♭","D","D♯/E♭","E","E♯/F","F♯/G♭","G","G♯/A♭","A","A♯/B♭","B/C♭"]
keysEnharmonicBlackKeys = ["C","C♯/D♭","D","D♯/E♭","E","F","F♯/G♭","G","G♯/A♭","A","A♯/B♭","B"]
sharpKeysMajor = ["G","D","A","E","B","F♯","C♯"]
flatKeysMajor = ["F","B♭","E♭","A♭","D♭","G♭","C♭"]
sharpKeysMinor = ["E","B","F♯","C♯","G♯","D♯","A♯"]
flatKeysMinor = ["D","G","C","F","B♭","E♭","A♭"]
majorKeys = ["C","F","B♭","E♭","A♭","D♭","F♯/G♭","B","E","A","D","G"]
minorKeys = ["A","D","G","C","F","B♭","D♯/E♭","G♯","C♯","F♯","B","E"]
orderOfAccidentals = ["B","E","A","D","G","C","F"]
modeDegrees = ["1st","2nd","3rd","4th","5th","6th","7th"]
modeDegreesExtended = ["9th","11th","13th"]
modeDegrees1 = ["2nd/9th","3rd","4th/11th","5th","6th/13th","7th"]
degrees = ["I","II","III","IV","V","VI","VII"]
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
    imageStr = "<canvas id=\"keyboard\" style=\"border:1px solid black\" data-tonic=\""+keyString+"\" data-highlight1=\""
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

intervalsInvert = ["P1","m2","M2","m3","M3","P4","TT","P5","m6","M6","m7","M7","P8","d2","A1","d3","A2","d4","A3","d5","A4","d6","A5","d7","A6","d8","A7"]
for interval in intervalsInvert:
    intervalType = ""
    invervalSize = ""
    if interval == "TT":
        intervalType = "TT"
        intervalSize = ""
    elif interval == "P1" or interval == "P8":
        intervalType = "P"
        intervalSize = interval[1]
    else:
        if interval[0] == "m":
            intervalType = "M"
        elif interval[0] == "M":
            intervalType = "m"
        elif interval[0] == "P":
            intervalType = "P"
        elif interval[0] == "d":
            intervalType = "A"
        elif interval[0] == "A":
            intervalType = "d"
        intervalSize = str(9-int(interval[1]))
    theoryCards.write("An inverted "+interval+" is a {{c1::"+intervalType+intervalSize+"}};;musictheory::intervals\n")


keys = ["C","F","A♯","B♭","D♯","E♭","G♯","A♭","C♯","D♭","F♯","G♭","B","C♭","E","A","D","G"]
for key in keys:
    majorKeyNum = -1
    minorKeyNum = -1
    majorKeyNum = keysContains(key, majorKeys)
    minorKeyNum = keysContains(key, minorKeys)
    if not majorKeyNum == -1:
        # key-signature cards
        majorKeyList = getKeySignature(key, majorKeyNum)

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
        hMajorList = majorList[:5]+[flatSixth]+[majorList[6]]

        # relative minor cards
        theoryCards.write(key+" major's relative minor is {{c1::"+sixth+"}} minor;;musictheory::relativekeys\n")

        dorianList = []
        phrygianList = []
        lydianList = []
        mixolydianList = []
        aeolianList = []
        locrianList = []
        dorianFlatFiveList = []
        phrygianFlatFourList = []
        lydianFlatThreeList = []
        mixolydianFlatTwoList = []
        lydianAugmentedSharpTwoList = []
        locrianDoubleFlatSevenList = []
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
            d = 1+i
            p = 2+i
            ly = 3+i
            m = 4+i
            a = 5+i
            lo = 6+i
            if d >= 7:
                d -= 7
            if p >= 7:
                p -= 7
            if ly >= 7:
                ly -= 7
            if m >= 7:
                m -= 7
            if a >= 7:
                a -= 7
            if lo >= 7:
                lo -= 7

            dorianList += [majorList[d]]
            phrygianList += [majorList[p]]
            lydianList += [majorList[ly]]
            mixolydianList += [majorList[m]]
            aeolianList += [majorList[a]]
            locrianList += [majorList[lo]]

            dorianFlatFiveList += [hMajorList[d]]
            phrygianFlatFourList += [hMajorList[p]]
            lydianFlatThreeList += [hMajorList[ly]]
            mixolydianFlatTwoList += [hMajorList[m]]
            lydianAugmentedSharpTwoList += [hMajorList[a]]
            locrianDoubleFlatSevenList += [hMajorList[lo]]

            majorString += majorList[i]+" "
            dorianString += majorList[d]+" "
            phrygianString += majorList[p]+" "
            lydianString += majorList[ly]+" "
            mixolydianString += majorList[m]+" "
            aeolianString += majorList[a]+" "
            locrianString += majorList[lo]+" "

            hMajorString += hMajorList[i]+" "
            dorianFlatFiveString += hMajorList[d]+" "
            phrygianFlatFourString += hMajorList[p]+" "
            lydianFlatThreeString += hMajorList[ly]+" "
            mixolydianFlatTwoString += hMajorList[m]+" "
            lydianAugmentedSharpTwoString += hMajorList[a]+" "
            locrianDoubleFlatSevenString += hMajorList[lo]+" "

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
        dorianImage = GetImage(dorianList[0],dorianList,[])
        phrygianImage = GetImage(phrygianList[0],phrygianList,[])
        lydianImage = GetImage(lydianList[0],lydianList,[])
        mixolydianImage = GetImage(mixolydianList[0],mixolydianList,[])
        aeolianImage = GetImage(aeolianList[0],aeolianList,[])
        locrianImage = GetImage(locrianList[0],locrianList,[])

        hMajorImage = GetImage(hMajorList[0],hMajorList,[])
        dorianFlatFiveImage = GetImage(dorianFlatFiveList[0],dorianFlatFiveList,[])
        phrygianFlatFourImage = GetImage(phrygianFlatFourList[0],phrygianFlatFourList,[])
        lydianFlatThreeImage = GetImage(lydianFlatThreeList[0],lydianFlatThreeList,[])
        mixolydianFlatTwoImage = GetImage(mixolydianFlatTwoList[0],mixolydianFlatTwoList,[])
        lydianAugmentedSharpTwoImage = GetImage(lydianAugmentedSharpTwoList[0],lydianAugmentedSharpTwoList,[])
        locrianDoubleFlatSevenImage = GetImage(locrianDoubleFlatSevenList[0],locrianDoubleFlatSevenList,[])

        theoryCards.write("the notes in the "+key+" major scale are {{c1::"+majorString+"}};"+majorImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+key+" ionian scale are {{c1::"+majorString+"}};"+majorImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+dorianList[0]+" dorian scale are {{c1::"+dorianString+"}};"+dorianImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+phrygianList[0]+" phrygian scale are {{c1::"+phrygianString+"}};"+phrygianImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+lydianList[0]+" lydian scale are {{c1::"+lydianString+"}};"+lydianImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+mixolydianList[0]+" mixolydian scale are {{c1::"+mixolydianString+"}};"+mixolydianImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+aeolianList[0]+" aeolian scale are {{c1::"+aeolianString+"}};"+aeolianImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+locrianList[0]+" locrian scale are {{c1::"+locrianString+"}};"+locrianImage+";musictheory::scales\n")

        theoryCards.write("the notes in the "+hMajorList[0]+" harmonic major scale are {{c1::"+hMajorString+"}};"+hMajorImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+dorianFlatFiveList[0]+" dorian♭5 scale are {{c1::"+dorianFlatFiveString+"}};"+dorianFlatFiveImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+phrygianFlatFourList[0]+" phrygian♭4 scale are {{c1::"+phrygianFlatFourString+"}};"+phrygianFlatFourImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+lydianFlatThreeList[0]+" lydian♭3 scale are {{c1::"+lydianFlatThreeString+"}};"+lydianFlatThreeImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+mixolydianFlatTwoList[0]+" mixolydian♭2 scale are {{c1::"+mixolydianFlatTwoString+"}};"+mixolydianFlatTwoImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+lydianAugmentedSharpTwoList[0]+" lydian augmented♯2 scale are {{c1::"+lydianAugmentedSharpTwoString+"}};"+lydianAugmentedSharpTwoImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+locrianDoubleFlatSevenList[0]+" locrian♭♭7 scale are {{c1::"+locrianDoubleFlatSevenString+"}};"+locrianDoubleFlatSevenImage+";musictheory::scales\n")

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
        theoryCards.write("the notes in the "+key+" bebop dorian scale are {{c1::"+bebopDorianString+"}};"+bebopDorianImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+key+" bebop dominant scale are {{c1::"+bebopDominantString+"}};"+bebopDominantImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+key+" bebop major scale are {{c1::"+bebopMajorString+"}};"+bebopMajorImage+";musictheory::scales\n")

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
        theoryCards.write("the notes in the "+key+" in-sen scale are {{c1::"+insenString+"}};"+insenImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+key+" major pentatonic scale are {{c1::"+majorPentatonicString+"}};"+majorPentatonicImage+";musictheory::scales\n")

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
        theoryCards.write("the notes in the "+key+" whole-tone scale are {{c1::"+wholeToneString+"}};"+wholeToneImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+key+" augmented scale are {{c1::"+augmentedString+"}};"+augmentedImage+";musictheory::scales\n")

        # major modes
        majorModes = [key+" ionian",second+" dorian",third+" phrygian",fourth+" lydian",fifth+" mixolydian",sixth+" aeolian",seventh+" locrian"]
        majorModeImages = [majorImage,dorianImage,phrygianImage,lydianImage,mixolydianImage,aeolianImage,locrianImage]
        for i in range(7):
            mode = modeDegrees[i]
            majorMode = majorModes[i]
            majorModeImage = majorModeImages[i]
            theoryCards.write("{{c1::"+majorMode+"}} is the "+mode+" mode of {{c2::"+key+" major}};"+majorModeImage+";musictheory::modes\n")

        # harmonic major modes
        harmonicMajorModes = [second+" dorian♭5",third+" phrygian♭4",fourth+" lydian♭3",fifth+" mixolydian♭2",flatSixth+" lydian augmented♯2",seventh+" locrian♭♭7"]
        harmonicMajorModeImages = [dorianFlatFiveImage,phrygianFlatFourImage,lydianFlatThreeImage,mixolydianFlatTwoImage,lydianAugmentedSharpTwoImage,locrianDoubleFlatSevenImage]
        for i in range(6):
            mode = modeDegrees[i+1]
            harmonicMajorMode = harmonicMajorModes[i]
            harmonicMajorModeImage = harmonicMajorModeImages[i]
            theoryCards.write("{{c1::"+harmonicMajorMode+"}} is the "+mode+" mode of {{c2::"+key+" harmonic major}};"+harmonicMajorModeImage+";musictheory::modes\n")
        
        # key signatures
        majorKeyString = ""
        for i in majorKeyList:
            majorKeyString += i+" "
        if majorKeyString == "":
            majorKeyString = "no sharps or flats"
        else:
            majorKeyString = majorKeyString[:-1]
        majorKeyImage = GetImage(key,majorList,majorKeyList)
        theoryCards.write("the key signature of {{c1::"+key+"}} major is {{c2::"+majorKeyString+"}};"+majorKeyImage+";musictheory::keysignatures\n")

        # major scale degree cards
        majorDegrees = {"♭2nd":flatSecond,"2nd":second,"♯2nd":sharpSecond,"3rd":third,"4th":fourth,"♯4th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth,"♭6th":flatSixth,"6th":sixth,"♭7th":flatSeventh,"7th":seventh,"♭9th":flatSecond,"9th":second,"♯9th":sharpSecond,"11th":fourth,"♯11th":sharpFourth,"♭13th":flatSixth,"13th":sixth}
        for degree in majorDegrees:
            degreeImage = GetImage(key,majorList,[majorDegrees[degree]])
            theoryCards.write("{{c1::"+majorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} major;"+degreeImage+";musictheory::scaledegrees\n")

        # major scale degrees 2nd cloze
        majorDegrees1 = {"♭2nd/♭9th":flatSecond,"2nd/9th":second,"♯2nd/♯9th":sharpSecond,"3rd":third,"4th/11th":fourth,"♯4th/♯11th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth,"♭6th/♭13th":flatSixth,"6th/13th":sixth,"♭7th":flatSeventh,"7th":seventh}
        for degree in majorDegrees1:
            degreeImage = GetImage(key,majorList,[majorDegrees1[degree]])
            theoryCards.write(majorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" major;"+degreeImage+";musictheory::scaledegrees\n")

        # major modes scale degree cards
        majorModes = [majorList,dorianList,phrygianList,lydianList,mixolydianList,aeolianList,locrianList]
        majorModeNames = ["ionian","dorian","phrygian","lydian","mixolydian","aeolian","locrian"]
        for i in range(7):
            majorMode = majorModes[i]
            majorModeName = majorModeNames[i]
            majorModeExtended = [majorMode[1],majorMode[3],majorMode[5]]
            for j in range(6):
                majorModeImage = GetImage(majorMode[0],majorMode,[majorMode[j+1]])
                theoryCards.write("{{c1::"+majorMode[j+1]+"}} is the "+modeDegrees[j+1]+" of {{c2::"+majorMode[0]+"}} "+majorModeName+";"+majorModeImage+";musictheory::scaledegrees\n")
                theoryCards.write(majorMode[j+1]+" is the {{c1::"+modeDegrees1[j]+"}} of "+majorMode[0]+" "+majorModeName+";"+majorModeImage+";musictheory::scaledegrees\n")
            for k in range(3):
                majorModeImageExtended = GetImage(majorMode[0],majorMode,[majorModeExtended[k]])
                theoryCards.write("{{c1::"+majorModeExtended[k]+"}} is the "+modeDegreesExtended[k]+" of {{c2::"+majorMode[0]+"}} "+majorModeName+";"+majorModeImageExtended+";musictheory::scaledegrees\n")


        # harmonic major modes scale degree cards
        harmonicMajorModes = [hMajorList,dorianFlatFiveList,phrygianFlatFourList,lydianFlatThreeList,mixolydianFlatTwoList,lydianAugmentedSharpTwoList,locrianDoubleFlatSevenList]
        harmonicMajorModeNames = ["harmonic major","dorian♭5","phrygian♭4","lydian♭3","mixolydian♭2","lydian augmented♯2","locrian♭♭7"]
        for i in range(7):
            harmonicMajorMode = harmonicMajorModes[i]
            harmonicMajorModeName = harmonicMajorModeNames[i]
            harmonicMajorModeExtended = [harmonicMajorMode[1],harmonicMajorMode[3],harmonicMajorMode[5]]
            for j in range(6):
                harmonicMajorModeImage = GetImage(harmonicMajorMode[0],harmonicMajorMode,[harmonicMajorMode[j+1]])
                theoryCards.write("{{c1::"+harmonicMajorMode[j+1]+"}} is the "+modeDegrees[j+1]+" of {{c2::"+harmonicMajorMode[0]+"}} "+harmonicMajorModeName+";"+harmonicMajorModeImage+";musictheory::scaledegrees\n")
                theoryCards.write(harmonicMajorMode[j+1]+" is the {{c1::"+modeDegrees1[j]+"}} of "+harmonicMajorMode[0]+" "+harmonicMajorModeName+";"+harmonicMajorModeImage+";musictheory::scaledegrees\n")
            for k in range(3):
                harmonicMajorModeImageExtended = GetImage(harmonicMajorMode[0],harmonicMajorMode,[harmonicMajorModeExtended[k]])
                theoryCards.write("{{c1::"+harmonicMajorModeExtended[k]+"}} is the "+modeDegreesExtended[k]+" of {{c2::"+harmonicMajorMode[0]+"}} "+harmonicMajorModeName+";"+harmonicMajorModeImageExtended+";musictheory::scaledegrees\n")

        # major functional triads
        functionalTriadsMajor = ["","-","-","","","-","o"]
        for i in range(7):
            chord = functionalTriadsMajor[i]
            if chord=="-" or chord=="ø":
                degree = degrees[i].lower()
            else:
                degree = degrees[i]
            chordList = []
            for j in range(0,6,2):
                n = i+j
                if n >= 7:
                    n -= 7
                chordList = chordList + [majorList[n]]
            majorTriadNote = majorList[i]
            majorTriadChordImage = GetImage(key, majorList+majorList, chordList)
            theoryCards.write("{{c1::"+majorTriadNote+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+key+"}} major;"+majorTriadChordImage+";musictheory::functionalharmony\n")

        # major functional 7th chords
        functional7thsMajor = ["Δ7","-7","-7","Δ7","7","-7","ø7"]
        for i in range(7):
            chord = functional7thsMajor[i]
            if chord=="-7" or chord=="ø7":
                degree = degrees[i].lower()
            else:
                degree = degrees[i]
            chordList = []
            for j in range(0,8,2):
                n = i+j
                if n > 6:
                    n -= 7
                chordList = chordList + [majorList[n]]
            major7thChordNote = majorList[i]
            major7thChordImage = GetImage(key, majorList+majorList, chordList)
            theoryCards.write("{{c1::"+major7thChordNote+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+key+"}} major;"+major7thChordImage+";musictheory::functionalharmony\n")

        # major modes functional triads
        for i in range(7):
            majorMode = majorModes[i]
            majorModeName = majorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = majorMode[j]
                chord = functionalTriadsMajor[m]
                if chord=="-" or chord=="o":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,6,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [majorMode[l]]
                chordImage = GetImage(majorMode[0],majorMode+majorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+majorMode[0]+"}} "+majorModeName+";"+chordImage+";musictheory::functionalharmony\n")

        # major modes functional 7th chords
        for i in range(7):
            majorMode = majorModes[i]
            majorModeName = majorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = majorMode[j]
                chord = functional7thsMajor[m]
                if chord=="-7" or chord=="ø7":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,8,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [majorMode[l]]
                chordImage = GetImage(majorMode[0],majorMode+majorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+majorMode[0]+"}} "+majorModeName+";"+chordImage+";musictheory::functionalharmony\n")

        # harmonic major modes functional triads
        functionalTriadsHarmonicMajor = ["","o","-","-","","+","o"]
        for i in range(7):
            harmonicMajorMode = harmonicMajorModes[i]
            harmonicMajorModeName = harmonicMajorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = harmonicMajorMode[j]
                chord = functionalTriadsHarmonicMajor[m]
                if chord=="-" or chord=="o":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,6,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [harmonicMajorMode[l]]
                chordImage = GetImage(harmonicMajorMode[0],harmonicMajorMode+harmonicMajorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+harmonicMajorMode[0]+"}} "+harmonicMajorModeName+";"+chordImage+";musictheory::functionalharmony\n")

        # harmonic major modes functional 7th chords
        functional7thsHarmonicMajor = ["Δ7","ø7","-7","-Δ7","7","+Δ7","o7"]
        for i in range(7):
            harmonicMajorMode = harmonicMajorModes[i]
            harmonicMajorModeName = harmonicMajorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = harmonicMajorMode[j]
                chord = functional7thsHarmonicMajor[m]
                if chord=="-7" or chord=="ø7" or chord=="o7" or chord=="-Δ7":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,8,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [harmonicMajorMode[l]]
                chordImage = GetImage(harmonicMajorMode[0],harmonicMajorMode+harmonicMajorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+harmonicMajorMode[0]+"}} "+harmonicMajorModeName+";"+chordImage+";musictheory::functionalharmony\n")


    if not minorKeyNum == -1:
        minorKeyList = getKeySignature(key, minorKeyNum)

        # 7 note minor scales
        minorList = getNotes(key, minorKeyList)

        flatSecond = AlterNote("flat",minorList[1])
        second = minorList[1]
        sharpSecond = AlterNote("sharp",minorList[1])
        third = minorList[2]
        sharpThird = AlterNote("sharp",minorList[2])
        flatFourth = AlterNote("flat",minorList[3])
        fourth = minorList[3]
        sharpFourth = AlterNote("sharp",minorList[3])
        flatFifth = AlterNote("flat",minorList[4])
        fifth = minorList[4]
        sharpFifth = AlterNote("sharp",minorList[4])
        flatSixth = AlterNote("flat",minorList[5])
        sixth = minorList[5]
        sharpSixth = AlterNote("sharp",minorList[5])
        diminishedSeventh = AlterNote("flat",minorList[6])
        seventh = minorList[6]
        sharpSeventh = AlterNote("sharp",minorList[6])
        mMinorList = minorList[:5]+[sharpSixth,sharpSeventh]
        hMinorList = minorList[:6]+[sharpSeventh]

        # key signatures
        minorKeyString = ""
        for k in minorKeyList:
            minorKeyString += k+" "
        if minorKeyString == "":
            minorKeyString = "no sharps or flats"
        else:
            minorKeyString = minorKeyString[:-1]
        minorKeyImage = GetImage(key,minorList,minorKeyList)
        theoryCards.write("the key signature of {{c1::"+key+"}} minor is {{c2::"+minorKeyString+"}};"+minorKeyImage+";musictheory::keysignatures\n")

        # relative major
        theoryCards.write(key+" minor's relative major is {{c1::"+third+"}} major;;musictheory::relativekeys\n")

        dorianFlatTwoList = []
        lydianAugmentedList = []
        lydianDominantList = []
        aeolianDominantList = []
        halfDiminishedList = []
        alteredList = []
        locrianSharpSixList = []
        augmentedMajorList = []
        dorianSharpFourList = []
        phrygianDominantList = []
        lydianSharpTwoList = []
        superLocrianList = []
        minorString = ""
        mMinorString = ""
        dorianFlatTwoString = ""
        lydianAugmentedString = ""
        lydianDominantString = ""
        aeolianDominantString = ""
        halfDiminishedString = ""
        alteredString = ""
        hMinorString = ""
        locrianSharpSixString = ""
        augmentedMajorString = ""
        dorianSharpFourString = ""
        phrygianDominantString = ""
        lydianSharpTwoString = ""
        superLocrianString = ""
        for i in range(7):
            d = 1+i
            p = 2+i
            ly = 3+i
            m = 4+i
            a = 5+i
            lo = 6+i
            if d >= 7:
                d -= 7
            if p >= 7:
                p -= 7
            if ly >= 7:
                ly -= 7
            if m >= 7:
                m -= 7
            if a >= 7:
                a -= 7
            if lo >= 7:
                lo -= 7

            dorianFlatTwoList += [mMinorList[d]]
            lydianAugmentedList += [mMinorList[p]]
            lydianDominantList += [mMinorList[ly]]
            aeolianDominantList += [mMinorList[m]]
            halfDiminishedList += [mMinorList[a]]
            alteredList += [mMinorList[lo]]

            locrianSharpSixList += [hMinorList[d]]
            augmentedMajorList += [hMinorList[p]]
            dorianSharpFourList += [hMinorList[ly]]
            phrygianDominantList += [hMinorList[m]]
            lydianSharpTwoList += [hMinorList[a]]
            superLocrianList += [hMinorList[lo]]

            minorString += minorList[i]+" "
            mMinorString += mMinorList[i]+" "
            dorianFlatTwoString += mMinorList[d]+" "
            lydianAugmentedString += mMinorList[p]+" "
            lydianDominantString += mMinorList[ly]+" "
            aeolianDominantString += mMinorList[m]+" "
            halfDiminishedString += mMinorList[a]+" "
            alteredString += mMinorList[lo]+" "

            hMinorString += hMinorList[i]+" "
            locrianSharpSixString += hMinorList[d]+" "
            augmentedMajorString += hMinorList[p]+" "
            dorianSharpFourString += hMinorList[ly]+" "
            phrygianDominantString += hMinorList[m]+" "
            lydianSharpTwoString += hMinorList[a]+" "
            superLocrianString += hMinorList[lo]+" "

        minorString = minorString[:-1]
        mMinorString = mMinorString[:-1]
        dorianFlatTwoString = dorianFlatTwoString[:-1]
        lydianAugmentedString = lydianAugmentedString[:-1]
        lydianDominantString = lydianDominantString[:-1]
        aeolianDominantString = aeolianDominantString[:-1]
        halfDiminishedString = halfDiminishedString[:-1]
        alteredString = alteredString[:-1]

        hMinorString = hMinorString[:-1]
        locrianSharpSixString = locrianSharpSixString[:-1]
        augmentedMajorString = augmentedMajorString[:-1]
        dorianSharpFourString = dorianSharpFourString[:-1]
        phrygianDominantString = phrygianDominantString[:-1]
        lydianSharpTwoString = lydianSharpTwoString[:-1]
        superLocrianString = superLocrianString[:-1]

        minorImage = GetImage(key,minorList,[])
        mMinorImage = GetImage(mMinorList[0],mMinorList,[])
        dorianFlatTwoImage = GetImage(dorianFlatTwoList[0],dorianFlatTwoList,[])
        lydianAugmentedImage = GetImage(lydianAugmentedList[0],lydianAugmentedList,[])
        lydianDominantImage = GetImage(lydianDominantList[0],lydianDominantList,[])
        aeolianDominantImage = GetImage(aeolianDominantList[0],aeolianDominantList,[])
        halfDiminishedImage = GetImage(halfDiminishedList[0],halfDiminishedList,[])
        alteredImage = GetImage(alteredList[0],alteredList,[])

        hMinorImage = GetImage(hMinorList[0],hMinorList,[])
        locrianSharpSixImage = GetImage(locrianSharpSixList[0],locrianSharpSixList,[])
        augmentedMajorImage = GetImage(augmentedMajorList[0],augmentedMajorList,[])
        dorianSharpFourImage = GetImage(dorianSharpFourList[0],dorianSharpFourList,[])
        phrygianDominantImage = GetImage(phrygianDominantList[0],phrygianDominantList,[])
        lydianSharpTwoImage = GetImage(lydianSharpTwoList[0],lydianSharpTwoList,[])
        superLocrianImage = GetImage(superLocrianList[0],superLocrianList,[])

        theoryCards.write("the notes in the "+key+" natural minor scale are {{c1::"+minorString+"}};"+minorImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+mMinorList[0]+" melodic minor scale are {{c1::"+mMinorString+"}};"+mMinorImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+dorianFlatTwoList[0]+" dorian♭2 scale are {{c1::"+dorianFlatTwoString+"}};"+dorianFlatTwoImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+lydianAugmentedList[0]+" lydian augmented scale are {{c1::"+lydianAugmentedString+"}};"+lydianAugmentedImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+lydianDominantList[0]+" lydian dominant scale are {{c1::"+lydianDominantString+"}};"+lydianDominantImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+aeolianDominantList[0]+" aeolian dominant scale are {{c1::"+aeolianDominantString+"}};"+aeolianDominantImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+halfDiminishedList[0]+" half diminished scale are {{c1::"+halfDiminishedString+"}};"+halfDiminishedImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+alteredList[0]+" altered scale are {{c1::"+alteredString+"}};"+alteredImage+";musictheory::scales\n")

        theoryCards.write("the notes in the "+hMinorList[0]+" harmonic minor scale are {{c1::"+hMinorString+"}};"+hMinorImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+locrianSharpSixList[0]+" locrian#6 scale are {{c1::"+locrianSharpSixString+"}};"+locrianSharpSixImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+augmentedMajorList[0]+" major augmented scale are {{c1::"+augmentedMajorString+"}};"+augmentedMajorImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+dorianSharpFourList[0]+" dorian#4 scale are {{c1::"+dorianSharpFourString+"}};"+dorianSharpFourImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+phrygianDominantList[0]+" phrygian dominant scale are {{c1::"+phrygianDominantString+"}};"+phrygianDominantImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+lydianSharpTwoList[0]+" lydian#2 scale are {{c1::"+lydianSharpTwoString+"}};"+lydianSharpTwoImage+";musictheory::scales\n")
        theoryCards.write("the notes in the "+superLocrianList[0]+" super-locrian scale are {{c1::"+superLocrianString+"}};"+superLocrianImage+";musictheory::scales\n")

        # bebop melodic minor scale
        bebopMMinorList = minorList[:6]+[sharpSixth,sharpSeventh]
        bebopMMinorString = ""
        for i in range(8):
            bebopMMinorString += bebopMMinorList[i] + " "
        bebopMMinorString = bebopMMinorString[:-1]
        bebopMMinorImage = GetImage(key,bebopMMinorList,[])
        theoryCards.write("the notes in the "+key+" bebop melodic minor scale are {{c1::"+bebopMMinorString+"}};"+bebopMMinorImage+";musictheory::scales\n")
        
        # melodic minor modes
        melodicMinorModes = [second+" dorian♭2",third+" lydian augmented",fourth+" lydian dominant",fifth+" aeolian dominant",sharpSixth+" half diminished",sharpSeventh+" altered"]
        melodicMinorModeImages = [dorianFlatTwoImage,lydianAugmentedImage,lydianDominantImage,aeolianDominantImage,halfDiminishedImage,alteredImage]
        for i in range(6):
            mode = modeDegrees[i+1]
            melodicMinorMode = melodicMinorModes[i]
            melodicMinorModeImage = melodicMinorModeImages[i]
            theoryCards.write("{{c1::"+melodicMinorMode+"}} is the "+mode+" mode of {{c2::"+key+" melodic minor}};"+melodicMinorModeImage+";musictheory::modes\n")

        # harmonic minor modes
        harmonicMinorModes = [second+" locrian♯6",third+" major augmented",fourth+" dorian♯4",fifth+" phrygian dominant",sixth+" lydian♯2",sharpSeventh+" super-locrian"]
        harmonicMinorModeImages = [locrianSharpSixImage,augmentedMajorImage,dorianSharpFourImage,phrygianDominantImage,lydianSharpTwoImage,superLocrianImage]
        for i in range(6):
            mode = modeDegrees[i+1]
            harmonicMinorMode = harmonicMinorModes[i]
            harmonicMinorModeImage = harmonicMinorModeImages[i]
            theoryCards.write("{{c1::"+harmonicMinorMode+"}} is the "+mode+" mode of {{c2::"+key+" harmonic minor}};"+harmonicMinorModeImage+";musictheory::modes\n")

        # minor scale degree cards
        minorDegrees = {"♭2nd":flatSecond,"2nd":second,"3rd":third,"4th":fourth,"♯4th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth,"♭9th":flatSecond,"9th":second,"11th":fourth,"♯11th":sharpFourth}
        for degree in minorDegrees:
            minorDegreeImage = GetImage(key,minorList,[minorDegrees[degree]])
            theoryCards.write("{{c1::"+minorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} minor;"+minorDegreeImage+";musictheory::scaledegrees\n")
        # minor scale degrees 2nd cloze
        minorDegrees1 = {"♭2nd/♭9th":flatSecond,"2nd/9th":second,"3rd":third,"4th/11th":fourth,"♯4th/♯11th":sharpFourth,"♭5th":flatFifth,"5th":fifth,"♯5th":sharpFifth}
        for degree in minorDegrees1:
            minorDegreeImage1 = GetImage(key,minorList,[minorDegrees1[degree]])
            theoryCards.write(minorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" minor;"+minorDegreeImage1+";musictheory::scaledegrees\n")
        # natural minor scale degree cards
        minorDegrees = {"6th":sixth,"7th":seventh,"13th":sixth}
        for degree in minorDegrees:
            naturalMinorDegreeImage = GetImage(key,minorList,[minorDegrees[degree]])
            theoryCards.write("{{c1::"+minorDegrees[degree]+"}} is the "+degree+" of {{c2::"+key+"}} natural minor;"+naturalMinorDegreeImage+";musictheory::scaledegrees\n")
        # natural minor scale degrees 2nd cloze
        minorDegrees1 = {"6th/13th":sixth,"7th":seventh}
        for degree in minorDegrees1:
            naturalMinorDegreeImage1 = GetImage(key,minorList,[minorDegrees1[degree]])
            theoryCards.write(minorDegrees1[degree]+" is the {{c1::"+degree+"}} of "+key+" natural minor;"+naturalMinorDegreeImage1+";musictheory::scaledegrees\n")

        # harmonic minor modes scale degree cards
        hMinorModes = [hMinorList,locrianSharpSixList,augmentedMajorList,dorianSharpFourList,phrygianDominantList,lydianSharpTwoList,superLocrianList]
        hMinorModeNames = ["harmonic minor","locrian#6","augmented major","dorian#4","phrygian dominant","lydian#2","super locrian"]
        for i in range(7):
            hMinorMode = hMinorModes[i]
            hMinorModeName = hMinorModeNames[i]
            hMinorModeExtended = [hMinorMode[1],hMinorMode[3],hMinorMode[5]]
            for j in range(6):
                hMinorModeImage = GetImage(hMinorMode[0],hMinorMode,[hMinorMode[j+1]])
                theoryCards.write("{{c1::"+hMinorMode[j+1]+"}} is the "+modeDegrees[j+1]+" of {{c2::"+hMinorMode[0]+"}} "+hMinorModeName+";"+hMinorModeImage+";musictheory::scaledegrees\n")
                theoryCards.write(hMinorMode[j+1]+" is the {{c1::"+modeDegrees1[j]+"}} of "+hMinorMode[0]+" "+hMinorModeName+";"+hMinorModeImage+";musictheory::scaledegrees\n")
            for k in range(3):
                hMinorModeImageExtended = GetImage(hMinorMode[0],hMinorMode,[hMinorModeExtended[k]])
                theoryCards.write("{{c1::"+hMinorModeExtended[k]+"}} is the "+modeDegreesExtended[k]+" of {{c2::"+hMinorMode[0]+"}} "+hMinorModeName+";"+hMinorModeImageExtended+";musictheory::scaledegrees\n")

        # melodic minor modes scale degree cards
        mMinorModes = [mMinorList,dorianFlatTwoList,lydianAugmentedList,lydianDominantList,aeolianDominantList,halfDiminishedList,alteredList]
        mMinorModeNames = ["melodic minor","dorian♭2","lydian augmented","lydian dominant","aeolian dominant","half diminished","altered list"]
        for i in range(7):
            mMinorMode = mMinorModes[i]
            mMinorModeName = mMinorModeNames[i]
            mMinorModeExtended = [mMinorMode[1],mMinorMode[3],mMinorMode[5]]
            for j in range(6):
                mMinorModeImage = GetImage(mMinorMode[0],mMinorMode,[mMinorMode[j+1]])
                theoryCards.write("{{c1::"+mMinorMode[j+1]+"}} is the "+modeDegrees[j+1]+" of {{c2::"+mMinorMode[0]+"}} "+mMinorModeName+";"+mMinorModeImage+";musictheory::scaledegrees\n")
                theoryCards.write(mMinorMode[j+1]+" is the {{c1::"+modeDegrees1[j]+"}} of "+mMinorMode[0]+" "+mMinorModeName+";"+mMinorModeImage+";musictheory::scaledegrees\n")
            for k in range(3):
                mMinorModeImageExtended = GetImage(mMinorMode[0],mMinorMode,[mMinorModeExtended[k]])
                theoryCards.write("{{c1::"+mMinorModeExtended[k]+"}} is the "+modeDegreesExtended[k]+" of {{c2::"+mMinorMode[0]+"}} "+mMinorModeName+";"+mMinorModeImageExtended+";musictheory::scaledegrees\n")

        # harmonic minor modes functional triads
        functionalTriadsHarmonicMinor = ["-","o","+","-","+","+","o"]
        for i in range(7):
            harmonicMinorMode = hMinorModes[i]
            harmonicMinorModeName = hMinorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = harmonicMinorMode[j]
                chord = functionalTriadsHarmonicMinor[m]
                if chord=="-" or chord=="o":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,6,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [harmonicMinorMode[l]]
                chordImage = GetImage(harmonicMinorMode[0],harmonicMinorMode+harmonicMinorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+harmonicMinorMode[0]+"}} "+harmonicMinorModeName+";"+chordImage+";musictheory::functionalharmony\n")

        # harmonic minor modes functional 7th chords
        functional7thsHarmonicMinor = ["-Δ7","ø7","+Δ7","-7","7","Δ7","o7"]
        for i in range(7):
            harmonicMinorMode = hMinorModes[i]
            harmonicMinorModeName = hMinorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = harmonicMinorMode[j]
                chord = functional7thsHarmonicMinor[m]
                if chord=="-7" or chord=="ø7" or chord=="o7" or chord=="-Δ7":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,8,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [harmonicMinorMode[l]]
                chordImage = GetImage(harmonicMinorMode[0],harmonicMinorMode+harmonicMinorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+harmonicMinorMode[0]+"}} "+harmonicMinorModeName+";"+chordImage+";musictheory::functionalharmony\n")

        # melodic minor modes functional triads
        functionalTriadsMelodicMinor = ["-","-","+","","","o","o"]
        for i in range(7):
            melodicMinorMode = mMinorModes[i]
            melodicMinorModeName = mMinorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = melodicMinorMode[j]
                chord = functionalTriadsMelodicMinor[m]
                if chord=="-" or chord=="o":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,6,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [melodicMinorMode[l]]
                chordImage = GetImage(melodicMinorMode[0],melodicMinorMode+melodicMinorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} triad of {{c3::"+melodicMinorMode[0]+"}} "+melodicMinorModeName+";"+chordImage+";musictheory::functionalharmony\n")

        # melodic minor modes functional 7th chords
        functional7thsMelodicMinor = ["-Δ7","-7","+Δ7","7","7","ø7","ø7"]
        for i in range(7):
            melodicMinorMode = mMinorModes[i]
            melodicMinorModeName = mMinorModeNames[i]
            for j in range(7):
                m = i+j
                if m >= 7:
                    m -= 7
                note = melodicMinorMode[j]
                chord = functional7thsMelodicMinor[m]
                if chord=="-7" or chord=="ø7" or chord=="o7" or chord=="-Δ7":
                    degree = degrees[j].lower()
                else:
                    degree = degrees[j]
                chordList = []
                for k in range(0,8,2):
                    l = j+k
                    if l >= 7:
                        l -= 7
                    chordList += [melodicMinorMode[l]]
                chordImage = GetImage(melodicMinorMode[0],melodicMinorMode+melodicMinorMode,chordList)
                theoryCards.write("{{c1::"+note+chord+"}} is the {{c2::"+degree+"}} 7th chord of {{c3::"+melodicMinorMode[0]+"}} "+melodicMinorModeName+";"+chordImage+";musictheory::functionalharmony\n")


    intervals = {"P1":0,"m2":1,"M2":2,"m3":3,"M3":4,"P4":5,"TT":6,"P5":7,"m6":8,"M6":9,"m7":10,"M7":11,"P8":12,"m9":13,"M9":14,"m10":15,"M10":16,"P11":17,"P12":19,"m13":20,"M13":21,"m14":22,"M14":23,"P15":24,"d2":0,"A1":1,"d3":2,"A2":3,"d4":4,"A3":5,"d5":6,"A4":6,"d6":7,"A5":8,"d7":9,"A6":10,"d8":11,"A7":12,"d9":12,"A8":13,"d10":14,"A9":15,"d11":16,"A10":17,"d12":18,"A11":18,"d13":19,"A12":20,"d14":21,"A13":22,"d15":23,"A14":24,"A15":25}
    for interval in intervals:
        keyIndex = keysContains(key, keysEnharmonicBlackKeys)
        keyEnharmonic = keysEnharmonicBlackKeys[keyIndex]
        intervalNum = intervals[interval]
        intervalAboveIndex = keyIndex+intervalNum
        while intervalAboveIndex >= 12:
            intervalAboveIndex -= 12
        intervalAbove = keysEnharmonicBlackKeys[intervalAboveIndex]
        if "/" in intervalAbove:
            noteAbove = intervalAbove.split("/")[1]
        else:
            noteAbove = intervalAbove
        if intervalNum < 13:
            intervalImage = GetImage(key,[key,noteAbove],[])
        else:
            intervalImage = GetImage(key,[key,"8va",noteAbove],[])
        theoryCards.write("{{c1::"+intervalAbove+"}} is a "+interval+" above {{c2::"+keyEnharmonic+"}};"+intervalImage+";musictheory::intervals\n")
        theoryCards.write("{{c1::"+keyEnharmonic+"}} is a "+interval+" below {{c2::"+intervalAbove+"}};"+intervalImage+";musictheory::intervals\n")

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
        theoryCards.write("{{c1::"+slashChordName+"::slash chord}} is equivalent to {{c2::"+eqChordName+"::chord name}} in traditional notation;"+slashChordImage+";musictheory::slashchords\n")

    if not majorKeyNum == -1:
        sharpFirst = AlterNote("sharp",key)
        flatSecond = AlterNote("flat",majorList[1])
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
        sharpFirst = AlterNote("sharp",key)
        flatSecond = AlterNote("flat",minorList[1])
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
    theoryCards.write("the notes in the "+key+" minor pentatonic scale are {{c1::"+minorPentatonicString+"}};"+minorPentatonicImage+";musictheory::scales\n")

    # blues scale
    bluesList = [key,flatThird,fourth,sharpFourth,fifth,flatSeventh]
    bluesString = ""
    for i in range(6):
        bluesString += bluesList[i]+" "
    bluesImage = GetImage(key,bluesList,[])
    bluesString = bluesString[:-1]
    theoryCards.write("the notes in the "+key+" blues scale are {{c1::"+bluesString+"}};"+bluesImage+";musictheory::scales\n")

    # diminished scales
    #TODO make it choose a different accidental if there is a double flat or double sharp
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
    theoryCards.write("the notes in the "+key+" half-whole diminished scale are {{c1::"+HWDiminishedString+"}};"+HWDiminishedImage+";musictheory::scales\n")
    theoryCards.write("the notes in the "+key+" whole-half diminished scale are {{c1::"+WHDiminishedString+"}};"+WHDiminishedImage+";musictheory::scales\n")

    # dominant7 diminished7 guide tones cards
    dominant7AGuideTones = GetImage(key,[third,flatSeventh],[])
    dominant7BGuideTones = GetImage(key,[flatSeventh,third],[])
    diminished7AGuideTones = GetImage(key,[flatThird,diminishedSeventh],[])
    diminished7BGuideTones = GetImage(key,[diminishedSeventh,flatThird],[])
    m7AGuideTones = GetImage(key,[flatThird,flatSeventh],[])
    M7AGuideTones = GetImage(key,[third,seventh],[])
    m7BGuideTones = GetImage(key,[flatSeventh,flatThird],[])
    M7BGuideTones = GetImage(key,[seventh,third],[])
    minorMajor7AGuideTonesImage = GetImage(key,[third,sharpSeventh],[])
    minorMajor7BGuideTonesImage = GetImage(key,[sharpSeventh,third],[])
    theoryCards.write("the guide tones of "+key+"7 in inversion A are {{c1::"+third+" and "+flatSeventh+"}} (in order from lowest to highest);"+dominant7AGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"7 in inversion B are {{c1::"+flatSeventh+" and "+third+"}} (in order from lowest to highest);"+dominant7BGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"o7 in inversion A are {{c1::"+flatThird+" and "+diminishedSeventh+"}} (in order from lowest to highest);"+diminished7AGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"o7 in inversion B are {{c1::"+diminishedSeventh+" and "+flatThird+"}} (in order from lowest to highest);"+diminished7BGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"-7 in inversion A are {{c1::"+flatThird+" and "+flatSeventh+"}} (in order from lowest to highest);"+m7AGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"Δ7 in inversion A are {{c1::"+third+" and "+seventh+"}} (in order from lowest to highest);"+M7AGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"-7 in inversion B are {{c1::"+flatSeventh+" and "+flatThird+"}} (in order from lowest to highest);"+m7BGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"Δ7 in inversion B are {{c1::"+seventh+" and "+third+"}} (in order from lowest to highest);"+M7BGuideTones+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"-Δ7 in inversion A are {{c1::"+third+" and "+sharpSeventh+"}} (in order from lowest to highest);"+minorMajor7AGuideTonesImage+";musictheory::voicings\n")
    theoryCards.write("the guide tones of "+key+"-Δ7 in inversion B are {{c1::"+sharpSeventh+" and "+third+"}} (in order from lowest to highest);"+minorMajor7BGuideTonesImage+";musictheory::voicings\n")

    inversions = ["root position","1st inversion","2nd inversion","3rd inversion"]
    # 3 note chord voicings  with inversions cards
    diminishedNotes = [key,flatThird,flatFifth]
    majorChordNotes = [key,third,fifth]
    augmentedChordNotes = [key,third,sharpFifth]
    minorChordNotes = [key,third,fifth]
    for i in range(3):
        diminishedString = ""
        diminishedList = []
        majorChordString = ""
        majorChordList = []
        augmentedChordString = ""
        augmentedChordList = []
        minorChordString = ""
        minorChordList = []
        inversion = inversions[i]
        for n in range(3):
            note = i+n
            if note>=3:
                note -= 3
            diminishedString += diminishedNotes[note]+" "
            diminishedList += [diminishedNotes[note]]
            majorChordString += majorChordNotes[note]+" "
            majorChordList += [majorChordNotes[note]]
            augmentedChordString += augmentedChordNotes[note]+" "
            augmentedChordList += [augmentedChordNotes[note]]
            minorChordString += minorChordNotes[note]+" "
            minorChordList += [minorChordNotes[note]]
        diminishedString = diminishedString[:-1]
        diminishedImage = GetImage(key,diminishedList,[])
        majorChordString = majorChordString[:-1]
        augmentedChordString = augmentedChordString[:-1]
        majorImage = GetImage(key,majorChordList,[])
        augmentedImage = GetImage(key,augmentedChordList,[])
        minorChordString = minorChordString[:-1]
        minorChordImage = GetImage(key,minorChordList,[])
        theoryCards.write("the notes in a "+key+"o chord in "+inversion+" are {{c2::"+diminishedString+"}} (in order from lowest to highest);"+diminishedImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+" chord in "+inversion+" are {{c1::"+majorChordString+"}} (in order from lowest to highest);"+majorImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+" augmented chord in "+inversion+" are {{c1::"+augmentedChordString+"}} (in order from lowest to highest);"+augmentedImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+"- chord in "+inversion+" are {{c2::"+minorChordString+"}} (in order from lowest to highest);"+minorChordImage+";musictheory::voicings\n")

    # 4 note chord voicing with inversions cards
    dominant7Notes = [key,third,fifth,flatSeventh]
    diminished7Notes = [key,flatThird,flatFifth,diminishedSeventh]
    minor7ChordNotes = [key,flatThird,fifth,flatSeventh]
    major7ChordNotes = [key,third,fifth,seventh]
    minor7FlatFiveChordNotes = [key,third,flatFifth,seventh]
    minorMajor7ChordNotes = [key,third,fifth,sharpSeventh]
    for i in range(4):
        dominant7String = ""
        diminished7String = ""
        dominant7List = []
        diminished7List = []
        minor7ChordString = ""
        minor7ChordList = []
        major7ChordString = ""
        major7ChordList = []
        minor7FlatFiveString = ""
        minor7FlatFiveList = []
        minorMajor7String = ""
        minorMajor7List = []
        inversion = inversions[i]
        for n in range(4):
            note = i+n
            if note >=4:
                note -= 4
            dominant7String += dominant7Notes[note]+" "
            dominant7List += [dominant7Notes[note]]
            diminished7String += diminished7Notes[note]+" "
            diminished7List += [diminished7Notes[note]]
            minor7ChordString += minor7ChordNotes[note]+" "
            minor7ChordList += [minor7ChordNotes[note]]
            major7ChordString += major7ChordNotes[note]+" "
            major7ChordList += [major7ChordNotes[note]]
            minor7FlatFiveString += minor7FlatFiveChordNotes[note]+" "
            minor7FlatFiveList += [minor7FlatFiveChordNotes[note]]
            minorMajor7String += minorMajor7ChordNotes[note]+" "
            minorMajor7List += [minorMajor7ChordNotes[note]]
        dominsnt7String = dominant7String[:-1]
        diminished7String = diminished7String[:-1]
        dominant7Image = GetImage(key,dominant7List,[])
        diminished7Image = GetImage(key,diminished7List,[])
        minor7ChordString = minor7ChordString[:-1]
        major7ChordString = major7ChordString[:-1]
        minor7FlatFiveString = minor7FlatFiveString[:-1]
        minorMajor7String = minorMajor7String[:-1]
        minor7FlatFiveImage = GetImage(key,minor7FlatFiveList,[])
        minorMajor7Image = GetImage(key,minorMajor7List,[])
        minor7Image = GetImage(key,minor7ChordList,[])
        major7Image = GetImage(key,major7ChordList,[])
        theoryCards.write("the notes in a "+key+"7 chord in "+inversion+" are {{c2::"+dominant7String+"}} (in order from lowest to highest);"+dominant7Image+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+"o7 chord in "+inversion+" are {{c2::"+diminished7String+"}} (in order from lowest to highest);"+diminished7Image+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+"-7 chord in "+inversion+" are {{c1::"+minor7ChordString+"}} (in order from lowest to highest);"+minor7Image+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+"Δ7 chord in "+inversion+" are {{c1::"+major7ChordString+"}} (in order from lowest to highest);"+major7Image+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+"-7♭5 chord in "+inversion+" are {{c1::"+minor7FlatFiveString+"}} (in order from lowest to highest);"+minor7FlatFiveImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a "+key+"-Δ7 chord in "+inversion+" are {{c1::"+minorMajor7String+"}} (in order from lowest to highest);"+minorMajor7Image+";musictheory::voicings\n")

    # rootless chord cards in A and B voicings
    rootlessInversions = ["A","","B"]
    rootlessiiNotes = [flatThird,fifth,flatSeventh,second]
    rootlessVNotes = [flatSeventh,second,third,sixth]
    rootlessINotes = [third,fifth,seventh,second]
    minorRootlessiiNotes = [third,flatFifth,seventh,flatSecond]
    minorRootlessVNotes = [seventh,flatSecond,sharpThird,sixth]
    minorRootlessINotes = [third,fifth,sharpSeventh,second]
    for i in range(0,3,2):
        rootlessiiString = ""
        rootlessiiList = []
        rootlessVString = ""
        rootlessVList = []
        rootlessIString = ""
        rootlessIList = []
        minorRootlessiiString = ""
        minorRootlessiiList = []
        minorRootlessVString = ""
        minorRootlessVList = []
        minorRootlessIString = ""
        minorRootlessIList = []
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
            minorRootlessiiString += minorRootlessiiNotes[note]+" "
            minorRootlessiiList += [minorRootlessiiNotes[note]]
            minorRootlessVString += minorRootlessVNotes[note]+" "
            minorRootlessVList += [minorRootlessVNotes[note]]
            minorRootlessIString += minorRootlessINotes[note]+" "
            minorRootlessIList += [minorRootlessINotes[note]]
        rootlessiiString = rootlessiiString[:-1]
        rootlessVString = rootlessVString[:-1]
        rootlessIString = rootlessIString[:-1]
        minorRootlessiiString = minorRootlessiiString[:-1]
        minorRootlessVString = minorRootlessVString[:-1]
        minorRootlessIString = minorRootlessIString[:-1]
        rootlessiiImage = GetImage(key,rootlessiiList,[])
        rootlessVImage = GetImage(key,rootlessVList,[])
        rootlessIImage = GetImage(key,rootlessIList,[])
        minorRootlessiiImage = GetImage(key,minorRootlessiiList,[])
        minorRootlessVImage = GetImage(key,minorRootlessVList,[])
        minorRootlessIImage = GetImage(key,minorRootlessIList,[])
        theoryCards.write("the notes in a type "+rootlessInversion+" rootless "+key+"-9 chord are {{c1::"+rootlessiiString+"}} (in order from lowest to highest);"+rootlessiiImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a type "+rootlessInversion+" rootless "+key+"13 chord are {{c1::"+rootlessVString+"}} (in order from lowest to highest);"+rootlessVImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a type "+rootlessInversion+" rootless "+key+"Δ9 chord are {{c1::"+rootlessIString+"}} (in order from lowest to highest);"+rootlessIImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a type "+rootlessInversion+" rootless "+key+"-7♭9♭5 chord are {{c2::"+minorRootlessiiString+"}} (in order from lowest to highest);"+minorRootlessiiImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a type "+rootlessInversion+" rootless "+key+"7♭9♭13 chord are {{c2::"+minorRootlessVString+"}} (in order from lowest to highest);"+minorRootlessVImage+";musictheory::voicings\n")
        theoryCards.write("the notes in a type "+rootlessInversion+" rootless "+key+"-Δ9 chord are {{c2::"+minorRootlessIString+"}} (in order from lowest to highest);"+minorRootlessIImage+";musictheory::voicings\n")

    # other chord voicing cards
    # 3 note chord voicing cards
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
    theoryCards.write("the notes in a "+key+"sus2 chord are {{c1::"+sus2String+"}} (in order from lowest to highest);"+sus2Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"sus4 chord are {{c1::"+sus4String+"}} (in order from lowest to highest);"+sus4Image+";musictheory::voicings\n")

    # 4 note chord voicing cards
    sevenSus2List = [key,second,fifth,flatSeventh]
    sevenSus4List = [key,fourth,fifth,flatSeventh]
    major6List = [key,third,fifth,sixth]
    rootless69List = [third,fifth,sixth,second]
    rootlessMajor13List = [seventh,second,third,sixth]
    minor6List = [key,third,fifth,sharpSixth]
    sevenSus2String = ""
    sevenSus4String = ""
    major6String = ""
    rootless69String = ""
    rootlessMajor13String = ""
    minor6String = ""
    for i in range(4):
        sevenSus2String += sevenSus2List[i]+" "
        sevenSus4String += sevenSus4List[i]+" "
        major6String += major6List[i]+" "
        rootless69String += rootless69List[i]+" "
        rootlessMajor13String += rootlessMajor13List[i]+" "
        minor6String += minor6List[i]+" "
    sevenSus2String = sevenSus2String[:-1]
    sevenSus4String = sevenSus4String[:-1]
    major6String = major6String[:-1]
    rootless69String = rootless69String[:-1]
    rootlessMajor13String = rootlessMajor13String[:-1]
    minor6String = minor6String[:-1]
    sevenSus2Image = GetImage(key,sevenSus2List,[])
    sevenSus4Image = GetImage(key,sevenSus4List,[])
    major6Image = GetImage(key,major6List,[])
    rootless69Image = GetImage(key,rootless69List,[])
    rootlessMajor13Image = GetImage(key,rootlessMajor13List,[])
    minor6Image = GetImage(key,minor6List,[])
    theoryCards.write("the notes in a "+key+"7sus2 chord are {{c1::"+sevenSus2String+"}} (in order from lowest to highest);"+sevenSus2Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"7sus4 chord are {{c1::"+sevenSus4String+"}} (in order from lowest to highest);"+sevenSus4Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"6 chord are {{c1::"+major6String+"}} (in order from lowest to highest);"+major6Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a type A rootless "+key+"6/9 chord are {{c1::"+rootless69String+"}} (in order from lowest to highest);"+rootless69Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a type B rootless "+key+"Δ13 chord are {{c1::"+rootlessMajor13String+"}} (in order from lowest to highest);"+rootlessMajor13Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"-6 chord are {{c1::"+minor6String+"}} (in order from lowest to highest);"+minor6Image+";musictheory::voicings\n")

    # 5 note chord voicing cards
    dominant9List = [key,third,fifth,flatSeventh,second]
    minor9List = [key,flatThird,fifth,flatSeventh,second]
    major9List = [key,third,fifth,seventh,second]
    sixNineList = [key,third,fifth,sixth,second]
    dominant9String = ""
    minor9String = ""
    major9String = ""
    sixNineString = ""
    for i in range(5):
        dominant9String += dominant9List[i]+" "
        minor9String += minor9List[i]+" "
        major9String += major9List[i]+" "
        sixNineString += sixNineList[i]+" "
    dominant9String = dominant9String[:-1]
    minor9String = minor9String[:-1]
    major9String = major9String[:-1]
    sixNineString = sixNineString[:-1]
    dominant9Image = GetImage(key,dominant9List,[])
    minor9Image = GetImage(key,minor9List,[])
    major9Image = GetImage(key,major9List,[])
    sixNineImage = GetImage(key,sixNineList,[])
    theoryCards.write("the notes in a "+key+"9 chord are {{c1::"+dominant9String+"}} (in order from lowest to highest);"+dominant9Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"-9 chord are {{c1::"+minor9String+"}} (in order from lowest to highest);"+minor9Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"Δ9 chord are {{c1::"+major9String+"}} (in order from lowest to highest);"+major9Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"6/9 chord are {{c1::"+sixNineString+"}} (in order from lowest to highest);"+sixNineImage+";musictheory::voicings\n")

    # 6 note chord voicing cards
    dominantSharp11List = [key,third,fifth,flatSeventh,second,sharpFourth]
    minor11List = [key,flatThird,fifth,flatSeventh,second,fourth]
    majorSharp11List = [key,third,fifth,seventh,second,sharpFourth]
    dominantSharp11String = ""
    minor11String = ""
    majorSharp11String = ""
    for i in range(6):
        dominantSharp11String += dominantSharp11List[i]+" "
        minor11String += minor11List[i]+" "
        majorSharp11String += majorSharp11List[i]+" "
    dominantSharp11String = dominantSharp11String[:-1]
    minor11String = minor11String[:-1]
    majorSharp11String = majorSharp11String[:-1]
    dominantSharp11Image = GetImage(key,dominantSharp11List,[])
    minor11Image = GetImage(key,minor11List,[])
    majorSharp11Image = GetImage(key,majorSharp11List,[])
    theoryCards.write("the notes in a "+key+"♯11 chord are {{c1::"+dominantSharp11String+"}} (in order from lowest to highest);"+dominantSharp11Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"-11 chord are {{c1::"+minor11String+"}} (in order from lowest to highest);"+minor11Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"Δ♯11 chord are {{c1::"+majorSharp11String+"}} (in order from lowest to highest);"+majorSharp11Image+";musictheory::voicings\n")

    # 7 note chord voicing cards
    dominant13Sharp11List = [key,third,fifth,flatSeventh,second,sharpFourth,sixth]
    minor13List = [key,flatThird,fifth,flatSeventh,second,fourth,sixth]
    major13Sharp11List = [key,third,fifth,seventh,second,sharpFourth,sixth]
    dominant13Sharp11String = ""
    minor13String = ""
    major13Sharp11String = ""
    for i in range(7):
        dominant13Sharp11String += dominant13Sharp11List[i]+" "
        minor13String += minor13List[i]+" "
        major13Sharp11String += major13Sharp11List[i]+" "
    dominant13Sharp11String = dominant13Sharp11String[:-1]
    minor13String = minor13String[:-1]
    major13Sharp11String = major13Sharp11String[:-1]
    dominant13Sharp11Image = GetImage(key,dominant13Sharp11List,[])
    minor13Image = GetImage(key,minor13List,[])
    major13Sharp11Image = GetImage(key,majorSharp11List,[])
    theoryCards.write("the notes in a "+key+"13♯11 chord are {{c1::"+dominant13Sharp11String+"}} (in order from lowest to highest);"+dominant13Sharp11Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"-13 chord are {{c1::"+minor13String+"}} (in order from lowest to highest);"+minor13Image+";musictheory::voicings\n")
    theoryCards.write("the notes in a "+key+"Δ13♯11 chord are {{c1::"+major13Sharp11String+"}} (in order from lowest to highest);"+major13Sharp11Image+";musictheory::voicings\n")

    # TODO maybe get rid of this
    # chord scales cards
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
        theoryCards.write("which scales can you play over a "+chordName+" chord?"+scalesStringCloze+";;musictheory::chordscales\n")
        theoryCards.write("which scales can you play over a "+chordName+" chord?"+scalesString+";;musictheory::chordscales\n")
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
        theoryCards.write("which chords can you play a "+scaleName+" over? "+chordsString+";;musictheory::chordscales\n")
        theoryCards.write("which chords can you play a "+scaleName+" over? "+chordsStringCloze+";;musictheory::chordscales\n")
