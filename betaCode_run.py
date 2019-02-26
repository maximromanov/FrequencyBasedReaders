import os, re
import betaCode, betaCodeTables

# convert AH to CE (only years)
def AHCE(ah):
    ce = int(ah)-(int(ah)/33)+622
    return(int(ce))

def processAHdates(text):
    # convert AH periods to CE only
    for d in re.finditer(r"@\d+-\d+TOCE", text):
        print(d.group())
        ah = d.group()[1:-4].split("-")
        ce1 = AHCE(ah[0])
        ce2 = AHCE(ah[1])
        ahcePeriod = "%s–%s CE" % (ce1, ce2)
        text = text.replace(d.group(), ahcePeriod)
        
    # convert AH periods into AH/CE format
    for d in re.finditer(r"@\d+-\d+AH", text):
        print(d.group())
        ah = d.group()[1:-2].split("-")
        ce1 = AHCE(ah[0])
        ce2 = AHCE(ah[1])
        ahcePeriod = "%s–%s AH / %s–%s CE" % (ah[0], ah[1], ce1, ce2)
        text = text.replace(d.group(), ahcePeriod)
        
    # convert AH dates into AH/CE format
    for d in re.finditer(r"@\d+AH", text):
        print(d.group())
        ah = d.group()
        ce = AHCE(ah[1:-2])
        ahce = "%s/%s CE" % (ah[1:-2], ce)
        text = text.replace(d.group(), ahce)
    return(text)

def translitFile(file):
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
        for i in re.finditer(r"@@.*?@@", text):
            print(i.group())
            iNew = betaCode.betacodeToTranslit(i.group())
            text = text.replace(i.group(), iNew[2:-2])

        text = processAHdates(text)
        with open(file, "w", encoding="utf8") as f:
            f.write(text)
        print("To Translit: %s has been processed..." % file)

def processArabicQuotes(file):
    with open(file, "r", encoding="utf8") as f:
        text = f.read()
        for i in re.finditer(r"(<!--@@.*?-->\n)(<p class=\"arabic\">.*?</p>)?", text):
            print(i.group(1)[6:-4])
            iNew = betaCode.betacodeToArabic(i.group(1)[6:-4])
            text = text.replace(i.group(), "%s<p class=\"arabic\">%s</p>" % (i.group(1), iNew))
        with open(file, "w", encoding="utf8") as f:
            f.write(text)
        print("To Arabic: %s has been processed..." % file)

postsFolder = "./"

def processRelevant(mainFolder):
    for path, subdirs, files in os.walk(mainFolder):
       for file in files:
           if file.startswith(tuple(["_0"])):
               print(file)
               f = os.path.join(path, file)
               translitFile(f)
               #processArabicQuotes(f)

processRelevant(postsFolder)
