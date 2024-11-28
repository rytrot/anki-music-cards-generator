from bs4 import BeautifulSoup
import bs4
import requests

count = 0
verbCards = open("verbCards.txt","w")
#verbs = ["être","avoir","choir","déchoir","monter","retourner","sen-aller"]
verbs = ["etre","avoir","aimer","saimer","jouer","saluer","etudier","briller","gagner","creer","naviguer","placer","manger","ceder","regner","leguer","rapiecer","proteger","lever","peler","appeler","interpeller","acheter","jeter","payer","essuyer","employer","envoyer","finir","hair","aller","courir","mourir","dormir","servir","sentir","vetir","fuir","tenir","acquerir","bouillir","couvrir","cueillir","defaillir","faillir","ouir","gesir","recevoir","voir","prevoir","pourvoir","savoir","devoir","pouvoir","valoir","prevaloir","vouloir","emouvoir","asseoir","pleuvoir","falloir","seoir","surseoir","choir","echoir","dechoir","faire","extraire","taire","plaire","croire","boire","conduire","rire","dire","interdire","maudire","lire","ecrire","suffire","confire","rendre","prendre","repandre","peindre","craindre","joindre","coudre","moudre","resoudre","rompre","battre","mettre","vaincre","connaitre","naitre","repaitre","croitre","accroitre","conclure","suivre","vivre","clore","monter","arriver","entrer","retourner","tomber","rester","sendormir","sasseoir","se-lever","se-reveiller","sen-aller","senfuir"]

for verb in verbs:
    # get the web data
    htmlText = requests.get("https://conjugaison.bescherelle.com/verbes/"+verb).text
    soup = BeautifulSoup(htmlText, "lxml")
    infinitif = soup.find("span",class_="field").text.replace("’","'")
    print(infinitif)

    # for each voix
    if soup.find("ul",class_="active-passive") == None:
        voixNames = [soup.find("div",class_="no-passive")]
    else:
        voixNames = [soup.find("a",class_="active-set"),soup.find("a",class_="passive-set")]
    voixDivs = soup.find_all("div",class_="container-verbe")
    for v in range(len(voixNames)):
        voixName = voixNames[v].text
        voixDiv = voixDivs[v]

        # for each temps
        tempsNames = [soup.find("a",attrs={"aria-controls":"simple-"+voixName.split(" ")[1]}),soup.find("a",attrs={"aria-controls":"composes-"+voixName.split(" ")[1]})]
        tempsDivs = voixDiv.find_all("div",class_="tab-pane")
        for t in range(len(tempsNames)):
            tempsName = tempsNames[t].text
            tempsDiv = tempsDivs[t]

            # for each card (half of the page)
            cards = tempsDiv.find_all("div",class_="card-type")
            for card in cards:
                title1 = card.find("h4",class_="card-title").text
                title1 = title1[0]+title1[1:].lower()

                # for each subCard (subTitle eg. present)
                subCards = card.find_all("div",class_="card-verbe")
                for subCard in subCards:
                    title2 = subCard.find("h5",class_="card-title").text
                    conjugationsContent = subCard.find("div",class_="content-verbe")

                    # for each conjugation (e.g. je suis)
                    conjugations = subCard.find_all("p")
                    for c in range(len(conjugations)):
                        conjugation = conjugations[c]
                        # if the conjugation has no content it is invalid
                        validContents = False
                        for content in conjugation.contents:
                            if type(content) == bs4.element.Tag:
                                validContents = True

                        if validContents==True:
                        # get the pronoun
                            if conjugation.find("personal-pronoun") == None:
                                if title1 == "Impératif":
                                    if c == 0:
                                        prenomRaw = "(tu)"
                                    elif c == 1:
                                        prenomRaw = "(nous)"
                                    elif c == 2:
                                        prenomRaw = "(vous)"
                                else:
                                    prenomRaw = ""
                            else:
                                prenomRaw = conjugation.find("personal-pronoun").text.replace("’","'").strip()
                            if conjugation.find("reflexive-pronoun") == None:
                                prenomReflexive = ""
                            else:
                                prenomReflexive = conjugation.find("reflexive-pronoun").text.strip()

                            # get the raw verb
                            verbeRaw = conjugation.find("verb").text.strip()

                            # get auxiliaire or split them into two if they have an " ou " and are in the verb
                            if " ou " in verbeRaw:
                                auxiliaires = [verbeRaw.split(" ")[0],verbeRaw.split(" ")[2]]
                            elif conjugation.find("auxiliary") == None:
                                auxiliaires = [""]
                            else:
                                auxiliaires = [conjugation.find("auxiliary").text]
                            if len(conjugation.find_all("auxiliary")) == 2:
                                auxiliaire1 = conjugation.find_all("auxiliary")[1].text.strip()
                            else:
                                auxiliaire1 = ""

                            # get the verb or split them into two if they have a " / "
                            if "/" in verbeRaw:
                                verbes = verbeRaw.split(" / ")
                            elif " ou " in verbeRaw:
                                verbes = [verbeRaw.split(" ")[3]]
                            else:
                                verbes = [verbeRaw]

                            # for each auxiliaire and verb
                            for a in range(len(auxiliaires)):
                                auxiliaire = auxiliaires[a].strip()
                                for v in range(len(verbes)):
                                    verbeRare = verbes[v].strip()
                                    # if there is more than 1 verb, assign it as (type 1) or (type 2)
                                    if len(verbes) > 1:
                                        verbeType = " (type "+str(v+1)+")"
                                    else:
                                        verbeType = ""

                                    # if the auxiliaire is split by an " ou " the first one is avoir and the second one is être so remove any (e) or (s) from the verb on the first one
                                    if " ou " in verbeRaw:
                                        if a == 0:
                                            verbeRare = verbeRare.replace("(e)","")
                                            verbeRare = verbeRare.replace("(s)","")
                                            verbe = verbeRare
                                            ouAuxiliaire = " (avoir)"
                                        elif a==1:
                                            ouAuxiliaire = " (être)"
                                    else:
                                        ouAuxiliaire = ""


                                    # process the prenoms
                                    if prenomRaw == "il (elle)":
                                        if not ("(e)" in verbeRare or "(û, ue)" in verbeRare):
                                            qPrenoms = ["il","elle","on"]
                                            aPrenoms = ["il","elle","on"]
                                        else:
                                            qPrenoms = ["il","elle","(m) on","(f) on"]
                                            aPrenoms = ["il","elle","on","on"]
                                    elif prenomRaw == "qu'il (elle)":
                                        if not ("(e)" in verbeRare or "(û, ue)" in verbeRare):
                                            qPrenoms = ["qu'il","qu'elle","qu'on"]
                                            aPrenoms = ["qu'il","qu'elle","qu'on"]
                                        elif "(e)" in verbeRare:
                                                qPrenoms = ["qu'il","qu'elle","(m) qu'on","(f) qu'on"]
                                                aPrenoms = ["qu'il","qu'elle","qu'on","qu'on"]
                                    elif prenomRaw == "ils (elles)":
                                        qPrenoms = ["ils","elles"]
                                        aPrenoms = ["ils","elles"]
                                    elif prenomRaw == "qu'ils (elles)":
                                        qPrenoms = ["qu'ils","qu'elles"]
                                        aPrenoms = ["qu'ils","qu'elles"]
                                    elif prenomRaw=="(tu)" or prenomRaw=="(vous)" or prenomRaw=="(nous)":
                                        if "(e)" in verbeRare:
                                            qPrenoms = ["(m) "+prenomRaw,"(f) "+prenomRaw]
                                            aPrenoms = ["",""]
                                        else:
                                            qPrenoms = [prenomRaw]
                                            aPrenoms = [""]
                                    elif "j'" in prenomRaw or "je" in prenomRaw or "tu" in prenomRaw or "nous" in prenomRaw or "vous" in prenomRaw:
                                        if "(e)" in verbeRare or "(es)" in verbeRare or "(û, ue)" in verbeRare:
                                            qPrenoms = ["(m) "+prenomRaw,"(f) "+prenomRaw]
                                            aPrenoms = [prenomRaw,prenomRaw]
                                        else:
                                            qPrenoms = [prenomRaw]
                                            aPrenoms = [prenomRaw]
                                    elif prenomRaw == "":
                                        if "(e)" in verbeRare or "(es)" in verbeRare or "(s, se, s, ses)" in verbeRare or "(û, ue, us, ues)" in verbeRare:
                                            if "(s)" in verbeRare or "(s, se, s, ses)" in verbeRare or "(û, ue, us, ues)" in verbeRare:
                                                qPrenoms = ["(ms)","(mp)","(fs)","(fp)"]
                                                aPrenoms = ["","","",""]
                                            else:
                                                qPrenoms = ["(m)","(f)"]
                                                aPrenoms = ["",""]
                                        else:
                                            qPrenoms = [""]
                                            aPrenoms = [""]

                                    for p in range(len(qPrenoms)):
                                        qPrenom = qPrenoms[p]
                                        aPrenom = aPrenoms[p]

                                        if "j'" in qPrenom and (auxiliaire=="suis" or auxiliaire=="fus" or auxiliaire=="serai" or auxiliaire=="serais" or auxiliaire=="sois" or auxiliaire=="fusse"):
                                            qPrenom = qPrenom.replace("j'","je")
                                            aPrenom = aPrenom.replace("j'","je")

                                        masculin = False
                                        feminin = False
                                        pluriel = False
                                        singulier = False
                                        if "il" in qPrenom or "(m)" in qPrenom or "(ms)" in qPrenom or "(mp)" in qPrenom:
                                            masculin = True
                                        elif "elle" in qPrenom or "(f)" in qPrenom or "(fs)" in qPrenom or "(fp)" in qPrenom:
                                            feminin = True
                                        if "ils" in qPrenom or "elles" in qPrenom or "nous" in qPrenom or "vous" in qPrenom or "(mp)" in qPrenom or "(fp)" in qPrenom:
                                            pluriel = True
                                        elif not ("ils" in qPrenom or "elles" in qPrenom or "nous" in qPrenom or "vous" in qPrenom) or "(ms)" in qPrenom or "(fs)" in qPrenom:
                                            singulier = True

                                        if "(e)(s)" in verbeRare:
                                            if masculin and singulier:
                                                verbe = verbeRare.replace("(e)(s)","")
                                            elif masculin and pluriel:
                                                verbe = verbeRare.replace("(e)(s)","s")
                                            elif feminin and singulier:
                                                verbe = verbeRare.replace("(e)(s)","e")
                                            elif feminin and pluriel:
                                                verbe = verbeRare.replace("(e)(s)","es")
                                        elif "(e)" in verbeRare and not "(s)" in verbeRare:
                                            if masculin:
                                                verbe = verbeRare.replace("(e)","")
                                            elif feminin:
                                                verbe = verbeRare.replace("(e)","e")
                                        elif "(es)" in verbeRare:
                                            if masculin:
                                                verbe = verbeRare.replace("(es)","")
                                            if feminin:
                                                    verbe = verbeRare.replace("(es)","es")
                                        elif "(s, se, s, ses)" in verbeRare:
                                            if masculin:
                                                verbe = verbeRare.replace("s (s, se, s, ses)","s")
                                            elif feminin and singulier:
                                                verbe = verbeRare.replace("s (s, se, s, ses)","se")
                                            elif feminin and pluriel:
                                                verbe = verbeRare.replace("s (s, se, s, ses)","ses")
                                        elif "(û, ue)" in verbeRare:
                                            if masculin:
                                                verbe = verbeRare.replace("û (û, ue)","û")
                                            elif feminin:
                                                verbe = verbeRare.replace("û (û, ue)","ue")
                                        elif "(û, ue, us, ues)" in verbeRare:
                                            if masculin and singulier:
                                                verbe = verbeRare.replace("û (û, ue, us, ues)","û")
                                            elif masculin and pluriel:
                                                verbe = verbeRare.replace("û (û, ue, us, ues)","us")
                                            elif feminin and singulier:
                                                verbe = verbeRare.replace("û (û, ue, us, ues)","ue")
                                            elif feminin and pluriel:
                                                verbe = verbeRare.replace("û (û, ue, us, ues)","ues")
                                        else:
                                            verbe = verbeRare

                                        if not (aPrenom=="" or "j'" in aPrenom):
                                            aPrenomSpace = aPrenom+" "
                                        else:
                                            aPrenomSpace = aPrenom

                                        if not (auxiliaire=="" or auxiliaire[len(auxiliaire)-1]==" "):
                                            auxiliaireSpace = auxiliaire+" "
                                        else:
                                            auxiliaireSpace = auxiliaire

                                        if not (auxiliaire1=="" or auxiliaire1[len(auxiliaire1)-1]==" "):
                                            auxiliaire1Space = auxiliaire1+" "
                                        else:
                                            auxiliaire1Space = auxiliaire1

                                        if prenomReflexive=="nous" or prenomReflexive=="vous" or prenomReflexive=="me" or prenomReflexive=="te" or prenomReflexive=="se":
                                            prenomReflexiveSpace = prenomReflexive+" "
                                        else:
                                            prenomReflexiveSpace = prenomReflexive

                                        verbCards.write(voixName+"|"+tempsName+"|"+title1+"|"+title2+"|"+qPrenom+"|"+auxiliaire+"|"+infinitif+verbeType+";"+voixName+";"+tempsName+";"+title1+";"+title2+";"+qPrenom+ouAuxiliaire+" ("+infinitif+verbeType+");"+aPrenomSpace+prenomReflexiveSpace+auxiliaireSpace+auxiliaire1Space+verbe+";conjugaison::"+infinitif.replace(" ","")+"\n")
