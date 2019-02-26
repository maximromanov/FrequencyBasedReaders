import os, re

def reformat(folder):
    lof = os.listdir(folder)
    transl = {}
    for f in lof:
        if f.startswith("_0"):
            with open(folder+f, "r", encoding="utf8") as ft:
                text = ft.read()
                vocab = text.split("##### GRAMMAR #####")[0].split("##### VOCAB REPORT #####")[1].strip()
                vocab = vocab.split("\n")
                for v in vocab:
                    if "::" in v:
                        t = v.split("::")
                        transl[t[0].strip()] = v.replace("::", ":-:")

    count = 0                       
    for f in lof:
        if f.startswith("00"):
            count += 1
            if count % 1000 == 0:
                print(count)
            with open(folder+f, "r", encoding="utf8") as fin:
                text = fin.read()
                for k,v in transl.items():
                    text = text.replace(k,v)

                with open(folder+f, "w", encoding="utf8") as fout:
                    fout.write(text)
            


reformat("./sections_man/")
print("Done!")
