# Typesetting selected texts into a nice LaTeX-based PDF

import os, re
import betaCode_run

latexFolder   = "latex/"
itemsFolder   = "sections_man/"

itemTemplate  = "reader-mac-arabxetex-template-item.tex"
wholeTemplate = "reader-mac-arabxetex-template.tex"


def createLaTeXfolder(folder):
    if not os.path.exists(folder+latexFolder):
        os.makedirs(folder+latexFolder)

def reformatItem(item, template):
    # general find/replace in the item
    item = re.sub(r"\bpn\b", r"\\textit{personal name}", item)
    
    # @ITEMNAME@
    src = re.search(r"# RAN # (.*)\n", item).group(1)
    rnk = int(re.search(r"# RAN # (\d+)", item).group(1))
    itemname = "Biography, Rank \# %d" % (rnk)
    template = template.replace("@ITEMNAME@", itemname)

    # @ITEMCODE@
    src = re.search(r"# SR1 # (.*)\n", item).group(1)
    ids = re.search(r"# RAN # (.*\.txt)", item).group(1)
    itemcode = "%s (%s)" % (src, ids)
    template = template.replace("@ITEMCODE@", itemcode)

    # @ARABICTEXT@    
    arabictext = item.split("##### VOCAB REPORT #####")[0].split("# TXT #\n")[1].strip()
    template = template.replace("@ARABICTEXT@", arabictext)


    # @GRAMMAR@
    grammar = item.split("##### CULTURE #####")[0].split("##### GRAMMAR #####")[1].strip()
    template = template.replace("@GRAMMAR@", grammar)
    
    # @CULTURE@
    culture = item.split("##### MANUSCR #####")[0].split("##### CULTURE #####")[1].strip()
    template = template.replace("@CULTURE@", culture)

    # @VOCAB@ "%s) \mbox{\textarab{%s}} --- %s;\\ \n" % (rank, token, transl)
    # @FREQREPORT@ # "%s) \mbox{\textarab{%s}} (%s);\\ \n" % (rank, token, freq)

    vocabRaw = item.split("##### GRAMMAR #####")[0].split("##### VOCAB REPORT #####")[1].strip()
    vocabRaw = vocabRaw.split("\n")
    vocab = []
    freqreport = []

    vt = '%d) \\mbox{\\textarab{%s}} --- %s;\\\\'
    ft = '%d) \\mbox{\\textarab{%s}} %s;\\\\'
    
    # rank, token, transl, freq
    for v in vocabRaw:
        if "::" in v:
            v = v.split("::")
            transl = v[1]
            v = v[0].strip().split(" ")
            rank = int(v[0][1:-1])
            token = v[1]
            freq = v[2]

            vocab.append(vt % (rank, token, transl))
            freqreport.append(ft % (rank, token, freq))

        else:
            if ":+:" in v:
                v = v.split(":-:")[0] # for already translated itemt that are to be excluded
            else:
                v = v
            v = v.strip().split(" ")
            rank = int(v[0][1:-1])
            token = v[1]
            freq = v[2]
            
            freqreport.append(ft % (rank, token, freq))
        
    template = template.replace("@VOCAB@", "\n".join(vocab))
    template = template.replace("@FREQREPORT@", "\n".join(freqreport))
    

    #print(template)
    #input(item)

    return(template)


def reformat(folder):
    os.system("python3 "+folder+"b.generateBetaCode.py")

    createLaTeXfolder(folder)
    with open(folder+wholeTemplate, "r", encoding="utf8") as f1:
        whole = f1.read()
        with open(folder+latexFolder+"reader.tex", "w", encoding="utf8") as f9:
            f9.write(whole)
        
    with open(folder+itemTemplate, "r", encoding="utf8") as f1:
        template = f1.read()

        lof = os.listdir(folder+itemsFolder)
        allItems = []
        for f in lof:
            if f.startswith("_0"):
                with open(folder+itemsFolder+f, "r", encoding="utf8") as ft:
                    item = ft.read()
                    item = reformatItem(item, template)
                    allItems.append(item)

        with open(folder+latexFolder+"items.tex", "w", encoding="utf8") as f9:
            f9.write("\n\n\n".join(allItems))

    #os.system("xelatex.exe -synctex=1 -interaction=nonstopmode %s" % (folder+latexFolder+"reader.tex"))

                
reformat("./tarikh_islam/")

print("Done!")
        
        
