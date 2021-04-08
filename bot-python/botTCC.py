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
        print("Subjects:")
        for sub in self._subjects:
            print("  "+ sub)
        print("Tag: "+ self._titleLink)

class Subjects():
    def __init__(self):
        self._subs = []
    def addSub(self,subName):
        print(len(self._subs))
        if(len(self._subs)>0):
            for i in range(0,len(self._subs)):
                if self._subs[i]["name"] == subName:
                    self._subs[i]["freq"] = self._subs[i]["freq"] + 1
                else:
                    dt = {
                        "name": subName,
                        "freq": 1
                    }
                    self._subs.append(dt)
                    break
        else:
            dt = {
                "name": subName,
                "freq": 1
            }
            self._subs.append(dt)
    def printFreq(self):
        for sub in self._subs:
            print("Name: " + sub["name"] + " // Freq: " + str(sub["freq"]))
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
                            subjectsD.append(row[1].text)
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
    ocorrencias = Subjects()
    for a in dataList:
        for cat in a._subjects:
            print(cat)
            ocorrencias.addSub(str(cat))
    ocorrencias.printFreq()