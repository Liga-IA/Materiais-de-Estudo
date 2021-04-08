import os
from pathlib import Path
from contextlib import redirect_stdout
from config import *
from tqdm import tqdm

class TCCData(object): 
    def __init__(self,subjects,title,url):
        self._subjects = subjects
        self._titleLink = '<a href="'+ str(url)+'" target="blank">'+str(title)+'</a>'
    def myPrint(self):
        a = "### "
        for sub in self._subjects:
            if(a == "### "):
                a = a + sub
            else:
                a = a + ", " + sub
        print("> " + a)
        print("> " + self._titleLink)

class Subjects():
    def __init__(self):
        self._subs = []
    def addSub(self,subName):
        #print(len(self._subs))
        if(len(self._subs)>0):
            achou = False
            for i in range(0,len(self._subs)):
                if self._subs[i]["name"].lower() == subName.lower():
                    self._subs[i]["freq"] = self._subs[i]["freq"] + 1
                    achou = True
                    break
            if(not achou):
                dt = {
                    "name": subName,
                    "freq": 1
                }
                self._subs.append(dt)
        else:
            dt = {
                "name": subName,
                "freq": 1
            }
            self._subs.append(dt)
    def printFreq(self):
        for sub in self._subs:
            print("Name: " + sub["name"] + " // Freq: " + str(sub["freq"]))
    def ordenar(self):
        if(len(self._subs)>0):
            for i in range (0,len(self._subs)-1):
                for j in range (i,len(self._subs)):
                    if self._subs[j]["freq"]>self._subs[i]["freq"]:
                        aux = self._subs[i]
                        self._subs[i] = self._subs[j]
                        self._subs[j] = aux
if __name__ == "__main__":
    driver = configuration()
    tcc_path = "./Arquivos/TCC"
    arqs = os.listdir(tcc_path)
    dataList = []
    with open('out.md', 'w',encoding="utf-8") as f:
        for arq in tqdm(arqs):
            arq = tcc_path +"/"+ arq
            meta = open(arq).read()
            url = meta.split("=")
            driver.get(url[1])
            subjectsD = []
            title = ""
            try:
                btn = driver.find_element_by_link_text('Mostrar registro completo')
                btn.click()
                rows = driver.find_elements_by_tag_name('tr')
                title = driver.find_element_by_class_name('ds-div-head').text
                
                for row in rows:
                    try:
                        row  = row.find_elements_by_tag_name('td')
                        #print(row[0].text)
                        if(row[0].text == 'dc.subject'):
                            t = row[1].text.split(". ")
                            for x in t:
                                n = x.split("; ")
                                for a in n:
                                    b = a.split(", ")
                                    for c in b:
                                        subjectsD.append(c)
                    except:
                        subjectsD
                
                
            except:
                infos = driver.find_elements_by_id("DocumentoTexto")
                title = infos[6].text
                txt = infos[7].text.split("\n")
                for a in txt:
                    subjectsD.append(a)
            subjects = "### "
            for s in subjectsD:
                if(subjects == "### "):
                    subjects =subjects+ s
                else:
                    subjects = subjects +", " + s
            with redirect_stdout(f):
                print(subjects)
                print('<a href="'+ str(url[1])+'" target="blank">'+str(title)+'</a>')
                print()
                print()
            dataList.append(TCCData(subjectsD,title,url[1]))
    driver.close()
    ocorrencias = Subjects()
    for a in dataList:
        for cat in a._subjects:
            #print(cat)
            ocorrencias.addSub(str(cat))
    ocorrencias.ordenar()
    ocorrencias.printFreq()
    subs = ocorrencias._subs
    i = 0
    with open('out-org.md', 'w',encoding="utf-8") as f:
        with redirect_stdout(f):
            while(len(subs)>0):
                
                aux = ocorrencias._subs[0]
                
                ocorrencias._subs.pop(0)
                if(aux["freq"]>1):
                    subset = []
                    j = 0
                    rems = []
                    for j in range(0,len(dataList)):
                        for k in range(0,len(dataList[j]._subjects)):
                            if dataList[j]._subjects[k].lower() == aux["name"].lower():
                                rems.append(j)
                                subset.append(dataList[j])
                    auxList = dataList
                    pops = 0
                    for num in rems:
                        auxList.pop(num-pops)
                        pops = pops + 1
                    dataList = auxList
                    if(len(subset)>0):
                        print("## "+ aux["name"])
                        for a in subset:
                            a.myPrint()
                        print()
                        print("--------------")
                        print()
                else:

                    tcc = None
                    for j in range(0,len(dataList)):
                        for k in range(0,len(dataList[j]._subjects)):
                            if dataList[j]._subjects[k].lower() == aux["name"].lower():
                                tcc = dataList[j]
                                dataList.pop(j)
                                break
                        if(tcc is not None):
                            print("## " + aux["name"])
                            tcc.myPrint()
                            print()
                            print("--------------")
                            print()
                            break
                        
                        
               
        

