#Basic Cards Format: [ID];[Title];[Text];[Image];[Extra];[Text to Image];[Image to Text];[Tags]
#Cloze Cards Format: [ID];[Title];[Text];[Image];[Extra];[Tags]
#TODO randomize the order of the relative keys
#TODO make the key signature cards an image of a key signature on a staff
#TODO add natural minor/aeolian cloze and major/ionian cloze? do it like the 6th/13th cards and the M6/M10 cards
#TODO finish extended chords cards? needed?
#TODO make cards for the scale degrees in slash chords and polychords? needed probably, would be nice?
#TODO write black keys that don't matter as enharmonic? (e.g. bebop scales?)
#TODO add chord substitution cards ala Jazz Theory Book
#TODO add more chord voicing cards (e.g. quartal voicings, rootless voicings, etc.)
#TODO make sure cards agree with https://newjazz.dk/Compendiums/scales_of_harmonies.pdf
#TODO also make sure they agree with https://www.newjazz.dk/Compendiums/Systematic_Scale_Chart.pdf
#TODO add cards for the chords mentioned in the jazz theory book and how they relate to their respective scales?
# card format [ID];[title];[front text];[front image];[back image];[back text];[tags]
count = 0
theoryCardsCloze = open("theoryCardsCloze.txt","w")
theoryCardsBasic = open("theoryCardsBasic.txt","w")
keysEnharmonicBlackKeys = ["C","C♯/D♭","D","D♯/E♭","E","F","F♯/G♭","G","G♯/A♭","A","A♯/B♭","B"]
orderOfAccidentals = ["B","E","A","D","G","C","F"]
degrees = ["I","II","III","IV","V","VI","VII"]
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

notes = ["C","D","E","F","G","A","B"]
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
    imageStr += (orangeStr+"\"></canvas>")
    return imageStr

def NumberWithSuffix(num):
    if num == 1:
        return "1st"
    elif num == 2:
        return "2nd"
    elif num == 3:
        return "3rd"
    else:
        return str(num)+"th"

def IsDegreeEnharmonic(notes):
    prevNoteNum = -1
    for n in range(len(notes)):
        note = notes[n]
        noteNum = -1
        noteAccidental = ""
        if note[0]=="♯" or note[0]=="♭" or note[0]=="Δ":
            noteAccidental = note[0]
            noteNum = int(note[1:])%7
        elif note[:3]=="sus":
            noteNum = int(note[3:])%7
        else:
            noteNum = int(note)%7
        noteNum *= 2
        if noteNum >= 8:
            noteNum -= 1
        if noteAccidental == "♯":
            noteNum += 1
        elif noteAccidental == "♭":
            noteNum -= 1
        if not (prevNoteNum==-1 or noteNum==prevNoteNum):
            return False
        prevNoteNum = noteNum
    return True

# TODO make it so that consecutive non-altered extensions with no previous non-altered extensions are invalid e.g. no 11(add13)
# TODO allow chords without the 7th (add9) (add11) (add13)
def chordExtensions(degrees):
    if len(degrees)==0:
        return [()]
    extensions = set()
    for extension in degrees[0]:
        for degree in chordExtensions(degrees[1:]):
            validExtension = True
            for extension1 in degree:
                if (
                        IsDegreeEnharmonic([extension,extension1])
                        or ("Δ" in extension and ("Δ" in extension1 or extension1=="6" or extension1=="7"))
                        or ("7" in extension and ("Δ" in extension1 or extension1=="6" or extension1=="9"))
                        or ("6" in extension and ("Δ" in extension1 or extension1=="7"))
                        or (extension=="9" and (extension1=="Δ11" or extension1=="Δ13"))
                        or (extension=="Δ9" and extension1=="11")
                        or (extension=="11" and extension1=="Δ13")
                        or (extension=="Δ11" and extension1=="13")
                ):
                    validExtension = False
            if validExtension == True:
                extensions.add(tuple([extension,*degree]))
            extensions.add(tuple([*degree]))
    return extensions

#TODO add a front image of the interval and a back image of the interval inverted?
intervalsInvert = ["P1","m2","M2","m3","M3","P4","TT","P5","m6","M6","m7","M7","P8","d2","A1","d3","A2","d4","A3","d5","A4","d6","A5","d7","A6","d8","A7"]
for interval in intervalsInvert:
    intervalType = ""
    invervalSize = ""
    if interval == "TT":
        intervalType = "TT"
        intervalSize = ""
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
    # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
    theoryCardsCloze.write("mt-inverted-intervals-"+interval+";Inverted Intervals;<span id=\"cloze1\">{{c1::"+interval+"}}</span><span id=\"cloze2\">{{c2::"+intervalType+intervalSize+"}}</span>;;;musictheory::intervals\n")

# modes
majorModeNames = ["ionian","dorian","phrygian","lydian","mixolydian","aeolian","locrian"]
harmonicMajorModeNames = ["harmonic major","dorian♭5","phrygian♭4","lydian♭3","mixolydian♭2","lydian-augmented♯2","locrian♭♭7"]
melodicMinorModeNames = ["melodic minor","dorian♭2","lydian-augmented","lydian-dominant","aeolian-dominant","half-diminished","altered"]
harmonicMinorModeNames = ["harmonic minor","locrian♯6","augmented-major","dorian♯4","phrygian-dominant","lydian♯2","super-locrian"]
pentatonicModeNames = ["major pentatonic","pentatonic mode 2","pentatonic mode 3","pentatonic mode 4","minor pentatonic"]
modeNameLists = [majorModeNames,harmonicMajorModeNames,melodicMinorModeNames,harmonicMinorModeNames,pentatonicModeNames]
modeTypeNames = ["major","harmonic major","melodic minor","harmonic minor","pentatonic"]
functionalTriadsMajor = ["","-","-","","","-","o"]
functionalTriadsHarmonicMajor = ["","o","-","-","","+","o"]
functionalTriadsMelodicMinor = ["-","-","+","","","o","o"]
functionalTriadsHarmonicMinor = ["-","o","+","-","+","+","o"]
functionalTriadsNaturalMinor = functionalTriadsMajor[5:]+functionalTriadsMajor[:5]
functional7thsMajor = ["Δ7","-7","-7","Δ7","7","-7","ø7"]
functional7thsHarmonicMajor = ["Δ7","ø7","-7","-Δ7","7","+Δ7","o7"]
functional7thsMelodicMinor = ["-Δ7","-7","+Δ7","7","7","ø7","ø7"]
functional7thsHarmonicMinor = ["-Δ7","ø7","+Δ7","-7","7","Δ7","o7"]
functional7thsNaturalMinor = functional7thsMajor[5:]+functional7thsMajor[:5]
modeFunctionalTriads = [functionalTriadsMajor,functionalTriadsHarmonicMajor,functionalTriadsMelodicMinor,functionalTriadsHarmonicMinor]
modeFunctional7ths = [functional7thsMajor,functional7thsHarmonicMajor,functional7thsMelodicMinor,functional7thsHarmonicMinor]
for modeName in range(len(modeNameLists)):
    for mode in range(len(modeNameLists[modeName])):
        modeDegrees = len(modeNameLists[modeName])
        # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
        if not "pentatonic" in modeNameLists[modeName][mode]:
            theoryCardsCloze.write("mt-modes-"+modeNameLists[modeName][mode]+";Modes;{{c1::"+modeNameLists[modeName][mode]+"}} is the {{c2::"+NumberWithSuffix(mode+1)+"}} mode of {{c3::"+modeTypeNames[modeName]+"}};;;musictheory::modes\n")
            # mode functional harmony cards
            for modeDegree in range(modeDegrees):
                scaleDegree = (mode+modeDegree)%7
                modeTriad = modeFunctionalTriads[modeName][scaleDegree]
                mode7th = modeFunctional7ths[modeName][scaleDegree]
                if modeTriad =="-" or modeTriad =="o":
                    chordFunction = degrees[modeDegree].lower()
                else:
                    chordFunction = degrees[modeDegree]
                # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
                theoryCardsCloze.write("mt-functional-triads-"+chordFunction+"-"+modeNameLists[modeName][mode]+";Functional Harmony;{{c1::"+modeTriad+"}} is the {{c2::"+chordFunction+"}} triad of "+modeNameLists[modeName][mode]+";;;musictheory::functionalharmony\n")
                theoryCardsCloze.write("mt-functional-7ths-"+chordFunction+"-"+modeNameLists[modeName][mode]+";Functional Harmony;{{c1::"+mode7th+"}} is the {{c2::"+chordFunction+"}} 7th chord of "+modeNameLists[modeName][mode]+";;;musictheory::functionalharmony\n")

# major and minor functional triads and sevenths
for scaleDegree in range(7):
# major functional triads and sevenths
    majorTriad = functionalTriadsMajor[scaleDegree]
    majorSeventh = functional7thsMajor[scaleDegree]
    minorTriad = functionalTriadsNaturalMinor[scaleDegree]
    minorSeventh = functional7thsNaturalMinor[scaleDegree]
    if majorTriad=="-" or majorTriad=="o":
        chordFunctionMajor = degrees[scaleDegree].lower()
    else:
        chordFunctionMajor = degrees[scaleDegree]
    if minorTriad=="-" or minorTriad=="o":
        chordFunctionMinor = degrees[scaleDegree].lower()
    else:
        chordFunctionMinor = degrees[scaleDegree]
    # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
    theoryCardsCloze.write("mt-functional-triads-"+chordFunctionMajor+"-major;Functional Harmony;{{c1::"+majorTriad+"}} is the {{c2::"+chordFunctionMajor+"}} triad of major;;;musictheory::functionalharmony\n")
    theoryCardsCloze.write("mt-functional-7ths-"+chordFunctionMajor+"-major;Functional Harmony;{{c1::"+majorSeventh+"}} is the {{c2::"+chordFunctionMajor+"}} 7th chord of major;;;musictheory::functionalharmony\n")
    theoryCardsCloze.write("mt-functional-triads-"+chordFunctionMinor+"-minor;Functional Harmony;{{c1::"+majorTriad+"}} is the {{c2::"+chordFunctionMinor+"}} triad of minor;;;musictheory::functionalharmony\n")
    theoryCardsCloze.write("mt-functional-7ths-"+chordFunctionMinor+"-minor;Functional Harmony;{{c1::"+majorSeventh+"}} is the {{c2::"+chordFunctionMinor+"}} 7th chord of minor;;;musictheory::functionalharmony\n")


keys = ["C","F","B♭","E♭","A♭","D♭","F♯","G♭","B","E","A","D","G"]
for x in range(len(keys)):
    keySignature = []
    if x<=5:
        for i in range(x):
            keySignature.append(orderOfAccidentals[i] + "♭")
    elif x==7:
        for i in range(x-1):
            keySignature.append(orderOfAccidentals[i] + "♭")
    if x>=8:
        for i in range(13-x):
            keySignature.append(orderOfAccidentals[6-i] + "♯")
    elif x==6:
        for i in range(12-x):
            keySignature.append(orderOfAccidentals[6-i] + "♯")

    majorList = []
    keyChrNum = ord(keys[x][0])
    for i in range(7):
        if keyChrNum+i == 72:
            keyChrNum -= 7
        note = chr(keyChrNum+i)
        for key in keySignature:
            if chr(keyChrNum+i) in key:
                note += key[-1]
        majorList += [note]
    minorList = []
    for i in range(5,12):
        minorList += [majorList[i%7]]
    harmonicMajorList = majorList[:5]+[AlterNote("flat",majorList[5])]+[majorList[6]]
    melodicMinorList = minorList[:5]+[AlterNote("sharp",minorList[5]),AlterNote("sharp",minorList[6])]
    harmonicMinorList = minorList[:6]+[AlterNote("sharp",minorList[6])]
    pentatonicList = majorList[:3]+majorList[4:6]

    # key signature cards
    keySignatureMajorOrdered = []
    keySignatureMinorOrdered = []
    for note in range(7):
        if majorList[note] in keySignature:
            keySignatureMajorOrdered += [majorList[note]]
        if minorList[note] in keySignature:
            keySignatureMinorOrdered += [minorList[note]]
    if "♯" in majorList[0] or "♭" in majorList[0]:
        keySignatureMajorOrdered += [majorList[0]]
    if "♯" in minorList[0] or "♭" in minorList[0]:
        keySignatureMinorOrdered += [minorList[0]]
    keySignatureString = ""
    for key in keySignature:
        keySignatureString += key+" "
    if keySignature == []:
        keySignatureString = "no sharps or flats "
    theoryCardsBasic.write("mt-key-signatures-key-major-"+majorList[0]+";Major Key Signatures;"+majorList[0]+" major;"+GetImage(majorList[0],majorList+[majorList[0]],keySignatureMajorOrdered)+";<img src=\""+majorList[0]+"major.png\">;TI;;musictheory::keysignatures\n")
    theoryCardsBasic.write("mt-key-signatures-signature-major-"+majorList[0]+";Major Key Signatures;<img src=\""+majorList[0]+"major.png\">;"+GetImage(majorList[0],majorList+[majorList[0]],keySignatureMajorOrdered)+";"+majorList[0]+" major;TI;;musictheory::keysignatures\n")
    theoryCardsBasic.write("mt-key-signatures-key-minor-"+minorList[0]+";Minor Key Signatures;"+minorList[0]+" minor;"+GetImage(minorList[0],minorList+[minorList[0]],keySignatureMinorOrdered)+";<img src=\""+majorList[0]+"major.png\">;TI;;musictheory::keysignatures\n")
    theoryCardsBasic.write("mt-key-signatures-signature-minor-"+minorList[0]+";Minor Key Signatures;<img src=\""+majorList[0]+"major.png\">;"+GetImage(minorList[0],minorList+[minorList[0]],keySignatureMinorOrdered)+";"+minorList[0]+" minor;TI;;musictheory::keysignatures\n")

    # relative keys cards
    # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
    theoryCardsCloze.write("mt-relative-minor-"+majorList[0]+";Relative Keys;<span id=\"cloze1\">{{c1::"+majorList[0]+"}} major</span><span id=\"cloze2\">{{c2::"+minorList[0]+"}} minor</span>;;;musictheory::relativekeys\n")

    # scale mode cards
    modeTypeLists = [majorList,harmonicMajorList,melodicMinorList,harmonicMinorList,pentatonicList]
    for modeType in range(len(modeTypeLists)):
        for mode in range(len(modeTypeLists[modeType])):
            modeList = []
            modeString = ""
            modeDegrees = len(modeTypeLists[modeType])
            for modeDegree in range(modeDegrees+1):
                modeNote = (mode+modeDegree)%len(modeTypeLists[modeType])
                modeList += [modeTypeLists[modeType][modeNote]]
                modeString += modeTypeLists[modeType][modeNote]+" "
            # scale mode notes cards
            # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
            if not majorList[0] == "F♯":
                theoryCardsBasic.write("mt-scalenotes-image"+modeList[0]+"-"+modeNameLists[modeType][mode]+";Scale Notes;"+modeList[0]+" "+modeNameLists[modeType][mode]+";"+GetImage(modeList[0],modeList,[])+";"+modeString[:-1]+";;IT;musictheory::scales\n")
            theoryCardsBasic.write("mt-scalenotes-ascending-"+modeList[0]+"-"+modeNameLists[modeType][mode]+";Scale Notes ASCENDING;"+modeList[0]+" "+modeNameLists[modeType][mode]+";"+GetImage(modeList[0],modeList,[])+";"+modeString[:-1]+";TI;;musictheory::scales\n")
            theoryCardsBasic.write("mt-scalenotes-descending-"+modeList[0]+"-"+modeNameLists[modeType][mode]+";Scale Notes DESCENDING;"+modeList[0]+" "+modeNameLists[modeType][mode]+";"+GetImage(modeList[0],modeList,[])+";"+modeString[:-1]+";TI;;musictheory::scales\n")
            #TODO have a whole 88 key piano image on the front and the scale name and ask what degree it is? Maybe not, too many cards (88 notes * 12 keys * 4 scales * 7 modes)
            # mode degrees cards
            for modeDegree in range(1,modeDegrees):
                # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
                if modeDegree==1 or modeDegree==3 or modeDegree==5:
                    theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(modeDegree+8)+"-"+modeList[0]+"-"+modeNameLists[modeType][mode]+";Scale Degrees;{{c1::"+modeList[modeDegree]+"}} is the "+NumberWithSuffix(modeDegree+8)+" of {{c3::"+modeList[0]+"}} "+modeNameLists[modeType][mode]+";"+GetImage(modeList[0],modeList[:-1]+modeList,["8va",modeList[modeDegree]])+";;musictheory::scaledegrees\n")
                theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(modeDegree+1)+"-"+modeList[0]+"-"+modeNameLists[modeType][mode]+";Scale Degrees;{{c1::"+modeList[modeDegree]+"}} is the {{c2::"+NumberWithSuffix(modeDegree+1)+"}} of {{c3::"+modeList[0]+"}} "+modeNameLists[modeType][mode]+";"+GetImage(modeList[0],modeList,[modeList[modeDegree]])+";;musictheory::scaledegrees\n")

    # other scale note cards
    insenList = [majorList[0],AlterNote("flat",majorList[1])]+majorList[3:5]+[AlterNote("flat",majorList[6]),majorList[0]]
    bebopDorianList = majorList[1:4]+[AlterNote("sharp",majorList[3])]+majorList[4:]+[majorList[0],majorList[1]]
    bebopDominantList = majorList[4:]+majorList[:4]+[AlterNote("sharp",majorList[3]),majorList[4]]
    bebopMajorList = majorList[:5]+[AlterNote("sharp",majorList[4])]+majorList[5:]+[majorList[0]]
    bebopMelodicMinorList = melodicMinorList[:5]+[AlterNote("sharp",melodicMinorList[4])]+melodicMinorList[5:]+[melodicMinorList[0]]
    halfWholeDiminishedList = [majorList[0],AlterNote("flat",majorList[1]),AlterNote("sharp",majorList[1]),majorList[2],AlterNote("sharp",majorList[3]),majorList[4],majorList[5],AlterNote("flat",majorList[6]),majorList[0]]
    wholeHalfDiminishedList = [majorList[0],majorList[1],AlterNote("flat",majorList[2]),majorList[3],AlterNote("flat",majorList[4]),AlterNote("flat",majorList[5]),AlterNote("flat",AlterNote("flat",majorList[6])),majorList[6],majorList[0]]
    wholeToneList = majorList[:3]+[AlterNote("sharp",majorList[3]),AlterNote("sharp",majorList[4]),AlterNote("flat",majorList[6]),majorList[0]]
    augmentedList = [majorList[0],AlterNote("sharp",majorList[1]),majorList[2],majorList[4],AlterNote("flat",majorList[5]),majorList[6],majorList[0]]
    bluesList = [majorList[0],AlterNote("flat",majorList[2]),majorList[3],AlterNote("sharp",majorList[3]),majorList[4],AlterNote("flat",majorList[6]),majorList[0]]
    scaleLists = [insenList,bebopDorianList,bebopDominantList,bebopMajorList,bebopMelodicMinorList,halfWholeDiminishedList,wholeHalfDiminishedList,wholeToneList,augmentedList,bluesList,majorList+[majorList[0]],minorList+[minorList[0]]]
    scaleNameLists = ["in-sen","bebop dorian","bebop dominant","bebop major","bebop melodic minor","half-whole diminished","whole-half diminished","whole-tone","augmented","blues","major","natural minor"]
    for scale in range(len(scaleLists)):
        scaleString = ""
        for note in range(len(scaleLists[scale])):
            scaleString += scaleLists[scale][note]+" "
        # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
        if not majorList[0] == "F♯":
            theoryCardsBasic.write("mt-scalenotes-image-"+scaleLists[scale][0]+"-"+scaleNameLists[scale]+";Scale Notes;"+scaleLists[scale][0]+" "+scaleNameLists[scale]+";"+GetImage(scaleLists[scale][0],scaleLists[scale],[])+";"+scaleString[:-1]+";;IT;musictheory::scales\n")
        theoryCardsBasic.write("mt-scalenotes-ascending-"+scaleLists[scale][0]+"-"+scaleNameLists[scale]+";Scale Notes ASCENDING;"+scaleLists[scale][0]+" "+scaleNameLists[scale]+";"+GetImage(scaleLists[scale][0],scaleLists[scale],[])+";"+scaleString[:-1]+";TI;;musictheory::scales\n")
        theoryCardsBasic.write("mt-scalenotes-descending-"+scaleLists[scale][0]+"-"+scaleNameLists[scale]+";Scale Notes DESCENDING;"+scaleLists[scale][0]+" "+scaleNameLists[scale]+";"+GetImage(scaleLists[scale][0],scaleLists[scale],[])+";"+scaleString[:-1]+";TI;;musictheory::scales\n")

    # intervals
    # TODO TODO
    intervalNamesPerfect = ["d","P","A"]
    intervalNamesMajor = ["d","m","M","A"]
    intervalModifiersPerfect = [-1,0,1]
    intervalModifiersMajor = [-2,-1,0,1]
    for interval in range(1,16):
        if interval==1 or interval==4 or interval==5 or interval==8 or interval==11 or interval==12 or interval==15:
            intervalNames = intervalNamesPerfect
            intervalModifiers = intervalModifiersPerfect
        else:
            intervalNames = intervalNamesMajor
            intervalModifiers = intervalModifiersMajor
        for i in range(len(intervalNames)):
            if intervalModifiers[i] == -2:
                intervalNote = AlterNote("flat",AlterNote("flat",majorList[(interval-1)%7]))
            elif intervalModifiers[i] == -1:
                intervalNote = AlterNote("flat",majorList[(interval-1)%7])
            elif intervalModifiers[i] == 0:
                intervalNote = majorList[(interval-1)%7]
            elif intervalModifiers[i] == 1:
                intervalNote = AlterNote("sharp",majorList[(interval-1)%7])

            if (interval==1 and intervalNames[i]=="P") or (interval==2 and intervalNames[i]=="d"):
                intervalImageList = [majorList[0]]
            elif interval*2+intervalModifiers[i] > 30:
                intervalImageList = [majorList[0],"8va","8va",intervalNote]
            elif interval*2+intervalModifiers[i] > 16:
                intervalImageList = [majorList[0],"8va",intervalNote]
            else:
                intervalImageList = [majorList[0],intervalNote]
            intervalImage = GetImage(majorList[0],intervalImageList,[])

            if not (intervalNames[i]=="d" and interval==1):
                if not (intervalNames[i] == "d" or intervalNames[i] == "A"):
                    theoryCardsBasic.write("mt-intervals-"+majorList[0]+"-"+intervalNames[i]+str(interval)+"-image;Intervals;"+intervalNames[i]+str(interval)+";"+intervalImage+";"+majorList[0]+" "+intervalNote+";;IT;musictheory::intervals\n")
                theoryCardsCloze.write("mt-intervals-"+majorList[0]+"-"+intervalNames[i]+str(interval)+";Intervals;{{c1::"+majorList[0]+"}} ~ "+intervalNames[i]+str(interval)+" ~ {{c2::"+intervalNote+"}};"+intervalImage+";;musictheory::intervals\n")

    theoryCardsBasic.write("mt-intervals-"+majorList[0]+"-TT-image;Intervals;TT;"+GetImage(majorList[0],[majorList[0],AlterNote("sharp",majorList[3])],[])+";"+majorList[0]+" "+AlterNote("sharp",majorList[3])+";;IT;musictheory::intervals\n")
    theoryCardsCloze.write("mt-intervals-"+majorList[0]+"-TT;Intervals;{{c1::"+majorList[0]+"}} ~ TT ~ {{c2::"+AlterNote("sharp",majorList[3])+"}};"+GetImage(majorList[0],[majorList[0],AlterNote("sharp",majorList[3])],[])+";;musictheory::intervals\n")


    # major scale degrees
    for i in range(1,7):
        sharpNote = AlterNote("sharp",majorList[i])
        flatNote = AlterNote("flat",majorList[i])
        # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
        theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(i+1)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+majorList[i]+"}} is the {{c2::"+NumberWithSuffix(i+1)+"}} of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+[majorList[0]],[majorList[i]])+";;musictheory::scaledegrees\n")
        if i==1 or i==3 or i==5:
            theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(i+8)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+majorList[i]+"}} is the "+NumberWithSuffix(i+8)+" of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+majorList+[majorList[0]],["8va",majorList[i]])+";;musictheory::scaledegrees\n")
        if i==1 or i==3:
            theoryCardsCloze.write("mt-scaledegrees-"+"#"+NumberWithSuffix(i+8)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+sharpNote+"}} is the {{c2::♯"+NumberWithSuffix(i+8)+"}} of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+majorList+[majorList[0]],["8va",sharpNote])+";;musictheory::scaledegrees\n")
            theoryCardsCloze.write("mt-scaledegrees-"+"#"+NumberWithSuffix(i+1)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+sharpNote+"}} is the ♯"+NumberWithSuffix(i+1)+" of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+[majorList[0]],[sharpNote])+";;musictheory::scaledegrees\n")
        if i==1 or i==5:
            theoryCardsCloze.write("mt-scaledegrees-"+"b"+NumberWithSuffix(i+8)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+flatNote+"}} is the {{c2::♭"+NumberWithSuffix(i+8)+"}} of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+majorList+[majorList[0]],["8va",flatNote])+";;musictheory::scaledegrees\n")
            theoryCardsCloze.write("mt-scaledegrees-"+"b"+NumberWithSuffix(i+1)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+flatNote+"}} is the ♭"+NumberWithSuffix(i+1)+" of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+[majorList[0]],[flatNote])+";;musictheory::scaledegrees\n")
        if i==4:
            theoryCardsCloze.write("mt-scaledegrees-"+"#"+NumberWithSuffix(i+1)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+sharpNote+"}} is the {{c2::♯"+NumberWithSuffix(i+1)+"}} of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+[majorList[0]],[sharpNote])+";;musictheory::scaledegrees\n")
            theoryCardsCloze.write("mt-scaledegrees-"+"b"+NumberWithSuffix(i+1)+"-"+majorList[0]+"-major;Scale Degrees;{{c1::"+flatNote+"}} is the {{c2::♭"+NumberWithSuffix(i+1)+"}} of {{c3::"+majorList[0]+"}} major;"+GetImage(majorList[0],majorList+[majorList[0]],[flatNote])+";;musictheory::scaledegrees\n")

    # minor scale degree cards
    for i in range(1,5):
        sharpNote = AlterNote("sharp",minorList[i])
        flatNote = AlterNote("flat",minorList[i])
        # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
        theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(i+1)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+minorList[i]+"}} is the {{c2::"+NumberWithSuffix(i+1)+"}} of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+[minorList[0]],[minorList[i]])+";;musictheory::scaledegrees\n")
        if i==1 or i==3:
            theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(i+8)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+minorList[i]+"}} is the "+NumberWithSuffix(i+8)+" of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+minorList+[minorList[0]],["8va",minorList[i]])+";;musictheory::scaledegrees\n")
        if i==3:
            theoryCardsCloze.write("mt-scaledegrees-"+"#"+NumberWithSuffix(i+8)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+sharpNote+"}} is the {{c2::♯"+NumberWithSuffix(i+8)+"}} of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+minorList+[minorList[0]],["8va",sharpNote])+";;musictheory::scaledegrees\n")
            theoryCardsCloze.write("mt-scaledegrees-"+"#"+NumberWithSuffix(i+1)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+sharpNote+"}} is the ♯"+NumberWithSuffix(i+1)+" of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+[minorList[0]],[sharpNote])+";;musictheory::scaledegrees\n")
        if i==1:
            theoryCardsCloze.write("mt-scaledegrees-"+"b"+NumberWithSuffix(i+8)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+flatNote+"}} is the {{c2::♭"+NumberWithSuffix(i+8)+"}} of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+minorList+[minorList[0]],["8va",flatNote])+";;musictheory::scaledegrees\n")
            theoryCardsCloze.write("mt-scaledegrees-"+"b"+NumberWithSuffix(i+1)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+flatNote+"}} is the ♭"+NumberWithSuffix(i+1)+" of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+[minorList[0]],[flatNote])+";;musictheory::scaledegrees\n")
        if i==4:
            theoryCardsCloze.write("mt-scaledegrees-"+"b"+NumberWithSuffix(i+1)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+flatNote+"}} is the {{c2::♭"+NumberWithSuffix(i+1)+"}} of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+[minorList[0]],[flatNote])+";;musictheory::scaledegrees\n")
            theoryCardsCloze.write("mt-scaledegrees-"+"#"+NumberWithSuffix(i+1)+"-"+minorList[0]+"-minor;Scale Degrees;{{c1::"+sharpNote+"}} is the {{c2::♯"+NumberWithSuffix(i+1)+"}} of {{c3::"+minorList[0]+"}} minor;"+GetImage(minorList[0],minorList+[minorList[0]],[sharpNote])+";;musictheory::scaledegrees\n")

    # natural minor scale degree cards
    for i in range(1,7):
        # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
        theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(i+1)+"-"+minorList[0]+"-natural-minor;Scale Degrees;{{c1::"+minorList[i]+"}} is the {{c2::"+NumberWithSuffix(i+1)+"}} of {{c3::"+minorList[0]+"}} natural minor;"+GetImage(minorList[0],minorList+[minorList[0]],[minorList[i]])+";;musictheory::scaledegrees\n")
        if i==1 or i==3 or i==5:
            theoryCardsCloze.write("mt-scaledegrees-"+NumberWithSuffix(i+8)+"-"+minorList[0]+"-natural-minor;Scale Degrees;{{c1::"+minorList[i]+"}} is the "+NumberWithSuffix(i+8)+" of {{c3::"+minorList[0]+"}} natural minor;"+GetImage(minorList[0],minorList+minorList+[minorList[0]],["8va",minorList[i]])+";;musictheory::scaledegrees\n")

    # guide tones cards
    guideToneNames = ["7","°7","-7","Δ7","-Δ7"]
    guideToneLists = [[majorList[2],AlterNote("flat",majorList[6])],[AlterNote("flat",majorList[2]),AlterNote("flat",AlterNote("flat",majorList[6]))],[AlterNote("flat",majorList[2]),AlterNote("flat",majorList[6])],[majorList[2],majorList[6]],[AlterNote("flat",majorList[2]),majorList[6]]]
    for chord in range(len(guideToneNames)):
        # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
        if not majorList[0] == "F♯":
            theoryCardsBasic.write("mt-guidetones-"+majorList[0]+"-"+guideToneNames[chord]+"-inversion-A;Guide Tones INVERSION A;"+majorList[0]+guideToneNames[chord]+";"+GetImage(majorList[0],guideToneLists[chord],[])+";"+guideToneLists[chord][0]+" "+guideToneLists[chord][1]+";TI;IT;musictheory::voicings\n")
            theoryCardsBasic.write("mt-guidetones-"+majorList[0]+"-"+guideToneNames[chord]+"-inversion-B;Guide Tones INVERSION B;"+majorList[0]+guideToneNames[chord]+";"+GetImage(majorList[0],guideToneLists[chord],[])+";"+guideToneLists[chord][1]+" "+guideToneLists[chord][0]+";TI;IT;musictheory::voicings\n")


    inversions = ["ROOT POSITION","1ST INVERSION","2ND INVERSION","3RD INVERSION"]
    # chord voicings with inversions cards
    # TODO add 7sus2, 7sus4, maj6, min6, 7b5, 7sus4, 9, +9, 7b9, 9b5, 7#9, 7#5b9, 7#5#9, m9, maj9, 6/9, minor6/9, minor9b5, 11, 13, 13b9, 13#11, 9#11? Should there be inversions cards or just normal position or as part of the extended chords generator?
    majorChordNotes = [majorList[0],majorList[2],majorList[4]]
    minorChordNotes = [minorList[0],minorList[2],minorList[4]]
    diminishedChordNotes = [majorList[6],majorList[1],majorList[3]]
    augmentedChordNotes = [melodicMinorList[2],melodicMinorList[4],melodicMinorList[6]]
    dominant7Notes = [majorList[4],majorList[6],majorList[1],majorList[3]]
    diminished7Notes = [harmonicMinorList[6],harmonicMinorList[1],harmonicMinorList[3],harmonicMinorList[5]]
    minor7Notes = [majorList[1],majorList[3],majorList[5],majorList[0]]
    major7Notes = [majorList[0],majorList[2],majorList[4],majorList[6]]
    halfDiminished7Notes = [majorList[6],majorList[1],majorList[3],majorList[5]]
    minorMajor7Notes = [melodicMinorList[0],melodicMinorList[2],melodicMinorList[4],melodicMinorList[6]]
    augmented7Notes = [melodicMinorList[2],melodicMinorList[4],melodicMinorList[6],AlterNote("flat",melodicMinorList[1])]
    augmentedMajor7Notes = [melodicMinorList[2],melodicMinorList[4],melodicMinorList[6],melodicMinorList[1]]
    chordNoteLists = [majorChordNotes,minorChordNotes,diminishedChordNotes,augmentedChordNotes,dominant7Notes,diminished7Notes,minor7Notes,major7Notes,halfDiminished7Notes,minorMajor7Notes,augmented7Notes,augmentedMajor7Notes]
    chordNames = ["","-","°","+","7","°7","-7","Δ7","ø7","-Δ7","+7","+Δ7"]
    for chord in range(len(chordNoteLists)):
        for inversion in range(len(chordNoteLists[chord])):
            chordList = []
            chordString = ""
            for degree in range(len(chordNoteLists[chord])):
                note = (inversion+degree)%len(chordNoteLists[chord])
                chordList += [chordNoteLists[chord][note]]
                chordString += chordNoteLists[chord][note]+" "
            # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
            if not majorList[0] == "F♯":
                theoryCardsBasic.write("mt-chordnotes-"+chordNoteLists[chord][0]+"-"+chordNames[chord]+"-"+inversions[inversion]+";Chord Notes "+inversions[inversion]+";"+chordList[0]+chordNames[chord]+";"+GetImage(chordList[0],chordList,[])+";"+chordString[:-1]+";TI;IT;musictheory::voicings\n")

    # other chord voicing cards
    sus2List = [majorList[0],majorList[1],majorList[4]]
    sus4List = [majorList[0],majorList[3],majorList[5]]
    sevenSus2List = [majorList[4],majorList[5],majorList[1],majorList[3]]
    sevenSus4List = [majorList[4],majorList[0],majorList[1],majorList[3]]
    major6List = [majorList[0],majorList[2],majorList[4],majorList[5]]
    minor6List = [melodicMinorList[0],melodicMinorList[2],melodicMinorList[4],melodicMinorList[5]]
    otherChordNoteLists = [sus2List,sus4List,sevenSus2List,sevenSus4List,major6List,minor6List]
    otherChordNames = ["sus2","sus4","7sus2","7sus4","6","-6"]
    for chord in range(len(otherChordNames)):
        chordList = []
        chordString = ""
        for note in range(len(otherChordNoteLists[chord])):
            chordList += [otherChordNoteLists[chord][note]]
            chordString += otherChordNoteLists[chord][note]+" "
        # card format [ID];[title];[front text];[front image];[back text];[back image];[back extra];[add reverse];[tags]
        if not majorList[0] == "F♯":
            theoryCardsBasic.write("mt-chordnotes-"+otherChordNoteLists[chord][0]+"-"+otherChordNames[chord]+";Chord Notes;"+chordList[0]+otherChordNames[chord]+";"+GetImage(chordList[0],chordList,[])+";"+chordString[:-1]+";TI;IT;musictheory::voicings\n")

    # extended chords
    # TODO add (add) and (omit) symbols when appropriate
    #chords = ["","-"]
    chords = [""]
    alterations5ths = ("♭5","♯5")
    extensions6ths = ("♭6","6")
    extensions7ths = ("7","Δ7")
    extensions9ths = ("♭9","9","♯9","Δ9")
    extensions11ths = ("11","♯11","Δ11")
    extensions13ths = ("♭13","13","Δ13")
    susModifiers = ("sus2","sus4")
    extensionTypes = [alterations5ths,extensions6ths,extensions7ths,extensions9ths,extensions11ths,extensions13ths,susModifiers]
    extensionSets = chordExtensions(extensionTypes)
    # TODO add (omit7) chords and (add9),(add11),(add13) chords without the 7th
    # TODO fix the notes list to make it have the right notes and be in order
    # TODO? organize alteredExtensions from lowest to highest?
    # if mainExtension == 9 or 11 or 13, print a second time with it as an (add9 or 11 or 13) for a chord without the 7th

majorList = ["C","D","E","F","G","A","B"]
for chord in chords:
    for extensionSet in extensionSets:
        mainExtension = ""
        alteredExtensions = []
        susExtension = ""
        addExtensions = []
        lowestMainExtensionNum = 5
        notesList = []
        notesString = ""
        for extension in extensionSet:
            if "Δ" in extension:
                mainExtension = extension
                notesList += majorList[6]
                if not int(extension[1:])-1 == 6:
                    notesList += majorList[int(extension[1:])-8]
                lowestMainExtensionNum = int(extension[1:])
            elif extension=="♭6":
                mainExtension = extension
                notesList += AlterNote("flat",majorList[5])
                lowestMainExtensionNum = int(extension[1:])
            elif "♭" in extension and not extension=="♭6":
                if int(extension[1:]) > 7:
                   notesList += [AlterNote("flat",majorList[int(extension[1:])-8])]
                else:
                   notesList += [AlterNote("flat",majorList[int(extension[1:])-1])]
                alteredExtensions += [extension]
            elif "♯" in extension:
                if int(extension[1:]) > 7:
                    notesList += [AlterNote("sharp",majorList[int(extension[1:])-8])]
                else:
                    notesList += [AlterNote("sharp",majorList[int(extension[1:])-1])]
                alteredExtensions += [extension]
            elif not "sus" in extension:
                if int(extension)<lowestMainExtensionNum or lowestMainExtensionNum==5:
                    mainExtension = extension
                    lowestMainExtensionNum = int(extension)
                else:
                    addExtensions += ["(add"+extension+")"]
                if int(extension) > 7:
                    notesList += [majorList[int(extension)-8]]
                else:
                    notesList += [majorList[int(extension)-1]]
        if mainExtension=="6" and "(add9)" in addExtensions:
            mainExtension = "6/9"
            addExtensions.remove("(add9)")

        if not lowestMainExtensionNum == 7:
            extensionString = mainExtension
        else:
            extensionString = AlterNote("flat",mainExtension)

        for i in range(0,lowestMainExtensionNum,2):
            j=i
            if j > 7:
                j-= 7
            notesList += [majorList[j]]
        if chord=="-":
            notesList[2] = AlterNote("flat",notesList[2])

        if "sus" in extension:
            notesList[1] = majorList[int(extension[3:])-1]
        if extension=="♭5":
            notesList[2] = AlterNote("flat",majorList[4])
        elif extension=="♯5":
            notesList[2] = AlterNote("sharp",majorList[4])

        extensionString += susExtension
        for alteredExtension in alteredExtensions:
            extensionString += "("+alteredExtension+")"
        for addExtension in addExtensions:
            extensionString += addExtension
        for note in notesList:
            notesString += note+" "
        count+=1
        #print(count,extensionSet,"the notes in a "+majorList[0]+chord+extensionString+" are "+notesString)
