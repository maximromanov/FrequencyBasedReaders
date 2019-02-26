import os, re

## CSV includes the following columns:

## URI - uri, must be unique for each piece
## AUT - Author, if available (otherwise empty)
## DAT - Date
## SR1 - Source / Book title
## SR2 - Subsource / Book chapter
## TOP - Topic/Theme, if available (otherwise empty)
## TXT - Text (if title is available, add it to the head of the text as ## title ## ||)
## MCS1, MSC2, etc - if you have other metadata available, add it into additional columns after the listed ones. Please, provide description of additional metadata (important, if you want to use it )

def normalizeArabicLight(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("[يى]ء", "ئ", text)
    text = re.sub("ى", "ي", text)
    #text = re.sub("(ؤ)", "ء", text)
    #text = re.sub("(ئ)", "ء", text)
    #text = re.sub("(ء)", "", text)
    #text = re.sub("(ة)", "ه", text)
    return(text)

def deNoise(text):
    noise = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
    text = re.sub(noise, '', text)
    return(text)


arNormDict = {
    'آ' : 'ا',
    'ٱ' : 'ا',
    'أ' : 'ا',
    'إ' : 'ا',
    'ىء' : 'ء',
    'يء' : 'ء',
    'ى' : 'ي',
    'ؤ' : 'ء',
    'ئ' : 'ء',
    }

# define replacement with dictionaries
def dictReplace(text, dic):
    for k,v in dic.items():
        text = text.replace(k, v)
    return text

def dictReplaceRev(text, dic):
    for k,v in dic.items():
        text = text.replace(v,k)
    return text

def normalizeArabic(text):
    text = deNoise(text)
    text = dictReplace(text, arNormDict)
    return(text)

# REFORMATTING
def reformat(folder):
    alldata = []
    counter = 0
    f = "./raw/0748Dhahabi.TarikhIslam.Shamela0035100-ara1.mARk"
    
    with open(f, "r", encoding="utf8") as f1:
        text = f1.read()
        text = re.sub("\n~~", " ", text)
        text = text.split("\n#$#")

        for l in text:
            if "$BIO_" in l:
                counter += 1
                la = l.replace("\n", "||")
                #input(l.replace("\t", "\n#NEW#\t"))

                URI = la[:10]
                AUT = "al-Ḏahabī"
                DAT = "NA"
                SR1 = "Taʾrīḫ al-islām"
                SR2 = "NA"
                TOP = "BIO"
                TXT = la.replace("\n", "||")
                TXT = re.sub(" +", " ", TXT)
                TXT = deNoise(TXT)

                # REMOVE mARkdown elements
                TXT = re.sub("\d{6}-\d{3}#?|\$BIO_\w+\$|PageV\w+", "", TXT)
                TXT = re.sub("# --- [^#]+#", "# ", TXT)
                TXT = re.sub(" +", " ", TXT)
                
                #print(URI)
                #print(TXT_en)
                #print("\n\n")
                #input(TXT)

                new = "\t".join([URI, AUT, DAT, SR1, SR2, TOP, TXT])

                alldata.append(new)
                    
                    
    
    mainList = []
    mainList.append("\t".join(["URI", "AUT", "DAT", "SR1", "SR2", "TOP", "TXT", "TXT_En"]))
    mainList.extend(alldata)

    print(counter)

    mainList = "\n".join(mainList)
    with open("data_csv.txt", "w", encoding="utf8") as fz:
        fz.write(mainList)


reformat("./raw/")
