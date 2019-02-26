import re, os
import datetime
startTime = datetime.datetime.now()


print("Generating a frequency-based reader...")

# generale a frequency list for all the vocabulary in the corpus
def freqList(folder):
    print("\tcreating a freqlist from: %s" % folder)
    counter = 0
    freqList = {}
    with open(folder+"data_csv.txt", "r", encoding="utf8") as fa:
        next(fa)
        for l in fa:
            counter += 1
            if counter % 100000 == 0:
                print(counter)
            vocab = l.split("\t")[6]
            vocab = re.sub("\d|\W", " ", vocab)
            vocab = re.sub("\s+", " ", vocab).strip()
            vocab = vocab.split(" ")

            for i in vocab:
                if i in freqList:
                    freqList[i] = freqList[i]+1
                else:
                    freqList[i] = 1

    freqListNew = []
    for k,v in freqList.items():
        freqListNew.append("%09d\t%s" % (v,k))

    freqListNew = sorted(freqListNew, reverse = True)
    
    with open(folder+"data_vocab_freq.txt", "w", encoding="utf8") as fz:
        fz.write("\n".join(freqListNew))

def modFreqList(folder):
    modFreqList = []
    modFreqs = []
    with open(folder+"data_vocab_freq.txt", "r", encoding="utf8") as fa:
        fa = fa.read().split("\n")
        for l in fa:
            la = l.split("\t")
            num = int(la[0])
            # flattening:
            #1# 1s - no change : 415
            #2# 10s - no change : 415
            #3# 100s - no change : gives 1,224 ranks
            #+# 1,000s - no change : gives 4,811 ranks
            #5# 10,000 > to 1,000s : gives 6,428 ranks
            #6# 100,000 > to 10,000s : 6,539 ranks
            #.# etc.
            if len(str(num)) > 4:
                flattenedFreq = round(num, -1*(len(str(num))-2))
                #print(l)
                #print(num)
                #print(flattenedFreq)
                #input()
            else:
                flattenedFreq = num
            modFreqList.append("%09d\t%s" % (int(flattenedFreq), l))
            modFreqs.append("%09d" % (int(flattenedFreq)))

    modFreqs = sorted(list(set(modFreqs)), reverse=True)
    modFreqsDic = {}
    count = 0
    for fr in modFreqs:
        count += 1
        modFreqsDic[fr] = "%09d" % count

    modFreqListNew = []
    for l in modFreqList:
        #input(l)
        mf = l.split("\t")[0]
        newL = modFreqsDic[mf] + "\t" + l
        #input(newL)
        modFreqListNew.append(newL)

    freqListNew = sorted(modFreqListNew)
    with open(folder+"data_vocab_freq_mod.txt", "w", encoding="utf8") as fz:
        fz.write("\n".join(freqListNew))
        
### generate ranking list ("inverted frequency list")
##def rankingList(folder):
##    print("\tcreating a rankingList from: %s" % folder)
##    ranking = []
##    counter = 0
##    with open(folder+"data_vocab_freq.txt", "r", encoding="utf8") as fa:
##        fa = fa.read().split("\n")
##        for l in fa:
##            counter += 1
##            l = l.split("\t")
##            lnew = l[1] + "\t" + \
##                   "%d) " % counter + \
##                   l[1] + " - {:,}".format(int(l[0]))
##            ranking.append(lnew)
##
##    rankList = "\n".join(ranking)
##    with open(folder+"data_vocab_rank.txt", "w", encoding="utf8") as fz:
##        fz.write(rankList)

def rankDict(folder):
    ranking = {}
    with open(folder+"data_vocab_freq_mod.txt", "r", encoding="utf8") as fa:
        for l in fa:
            l = l.split("\t")
            word = l[3].replace("\n", "")
            ranking[word] = int(l[0])
            #input(ranking)
    return(ranking)

def calcRankForStory(listOfVocabRanks):
    rank = sum(listOfVocabRanks)/float(len(listOfVocabRanks))
    rank = "%040d" % int(rank * 10000000000 * 10000000000 * 10000000000)
    return(rank)    
                
def generateRankingForTexts(folder):
    counter = 0
    ranking = rankDict(folder)
    rankList = []
    with open(folder+"data_csv.txt", "r", encoding="utf8") as fa:
        next(fa)
        for l in fa:
            counter += 1
            if counter % 10000 == 0:
                print("% 10d" % counter)
##            if counter == 1000:
##                break
            l = l.split("\t")
            uri = l[0]
            txt = l[6]
            #print(txt)
            txt = re.sub("\d|\W", " ", txt)
            txt = re.sub("\s+", " ", txt).strip()
            txt = txt.split(" ")
            
            txtNumberList = []
            for v in txt:
                #print(v)
                try:
                    txtNumberList.append(ranking[v])
                except:
                    input("%s --- not found" % v)
                    txtNumberList.append("0")
            txtRank = calcRankForStory(txtNumberList)
            rankingLine = str(txtRank) + "\t" + \
                          uri + "\t" + \
                          "%010d\t" % len(txtNumberList) + \
                          " ".join(map(str, txtNumberList))

            rankList.append(rankingLine)

    rankList = sorted(rankList, reverse=False)
    rankList = "\n".join(rankList)

    with open(folder+"data_csv_ranking.txt", "w", encoding="utf8") as fz:
        fz.write(rankList)

def generateTxtDic(folder):
    txtDic = {}
    with open(folder+"data_csv.txt", "r", encoding="utf8") as fa:
        next(fa)
        for i in fa:
            uri = i.split("\t")[0]
            txtDic[uri] = i
    print("txtDic has been generated...")
    return(txtDic)

def vocRankDic(folder):
    vocRanks = {}
    with open(folder+"data_vocab_freq_mod.txt", "r", encoding="utf8") as fa:
        for i in fa:
            i = i.replace("\n", "")
            i = i.split("\t")
            vocRanks[i[3]] = "#%s# %s (%s)" % (i[0], i[3], "{:,}".format(int(i[2])))
            #input(vocRanks)
    print("vocRankDic has been generated...")
    return(vocRanks)
            
def formatForManualReview(folder):
    # read text data
    vocRanks = vocRankDic(folder)
    txtDic = generateTxtDic(folder)
    
    # read ranking
    counter = 0
    reader = []

    countShorties = 0
    countSuitable = 0
    
    with open(folder+"data_csv_ranking.txt", "r", encoding="utf8") as fa:
        for i in fa:
            uri = i.split("\t")[1]

            words = int(i.split("\t")[2])

            if words >= minLength:
                countSuitable += 1
                #input(i.split("\t"))

                txtLen = int(i.split("\t")[2])
                if txtLen >= 10:
                    counter += 1
                    story = txtDic[uri].split("\t")
                    story[0] = "# URI # " + story[0] + " # TAG"
                    story[1] = "# AUT # " + story[1]
                    story[2] = "# DAT # " + story[2]
                    story[3] = "# SR1 # " + story[3]
                    story[4] = "# SR2 # " + story[4]
                    story[5] = "# TOP # " + story[5]
                    story[6] = "# TXT #\n" + story[6].replace("||", "\n")
                    header = "##### NEXT STORY ###################################\n"
                    header = header + "# RAN # %09d-%s.txt\n" % (counter, uri)

                    # vocabulary report
                    vocab = story[6]
                    vocab = re.sub("\d|\W|[a-zA-Z]+", " ", vocab)
                    vocab = re.sub("\s+", " ", vocab).strip()
                    vocab = vocab.split(" ")
                    vocab = list(set(vocab))
                    
                    vocList = []
                    for v in vocab:
                        try:
                            vocList.append(vocRanks[v])
                        except:
                            print("Faulty vocab item: %s" % v)

                    vocList = sorted(vocList, reverse=False)
                    vocList = "\n".join(vocList)
                    vHeader = "##### VOCAB REPORT #####\n"

                    # reformat text for readability
                    txt = header + "\n".join(story) + vHeader + vocList + "\n\n"
                    txt = txt + "\n##### GRAMMAR #####\n\n[Test Text]\n\n"
                    txt = txt + "\n##### CULTURE #####\n\n[Test Text]\n\n"
                    txt = txt + "\n##### MANUSCR #####\n\n[Relative Path to Image]\n\n"
                    
                    txt = re.sub(" \|\| ", "\n", txt)
                    txt = re.sub(";;", " ## ", txt)
                    txt = re.sub("# TXT # ## ", "# TXT #\n## ", txt)
                    txt = re.sub(" +", " ", txt)
                    
                    reader.append(txt)

            else:
                countShorties += 1
                #print(i.split("\t"))
                #input(words)
            
    print("%d were shorter than minLength of %d" % (countShorties, minLength))
    print("%d were included" % (countSuitable))

    print(len(reader))

    # combine into a new text file
    with open(folder+"data_txt_manual.txt", "w", encoding="utf8") as fz:
        fz.write("\n".join(reader))

    if not os.path.exists(folder+"sections_man/"):
        os.makedirs(folder+"sections_man/")

    count = 0
    for i in reader:
        count += 1
        fileName = re.search(r"# RAN # (.*?\.txt)\n", i).group(1)
        with open(folder+"sections_man/"+fileName, "w", encoding="utf8") as ft:
            ft.write(i)
        if count == 10000:
            break
         
## RUNNING FROM HERE

minLength = 40 # It may be a god idea to exclude the first quartile (25% of shortest items)

def main(folder):
    freqList(folder)
    modFreqList(folder)
    generateRankingForTexts(folder)
    formatForManualReview(folder)


##multiple = ["./Persian_Epic_Poetry_02/",
##            "./Persian_Epic_Poetry_04/",
##            "./Persian_Epic_Poetry_05/",
##            "./Persian_Epic_Poetry_10/",
##            "./Persian_Epic_Poetry_15/",
##            "./Persian_Epic_Poetry_20/"]
##
##
##for m in multiple:
##    main(m)

#main("./PersianPoetry/")
#main("./hadith/")
main("./tarikh_islam/")
#main("./sharq_awsat/")
#main("./test/")

print("Processing time: " + str(datetime.datetime.now()-startTime))
print("Tada!")


##Tarikh al-islam
##
##    Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
##    7.00    35.00    50.00    91.66    81.00 17950.00 
