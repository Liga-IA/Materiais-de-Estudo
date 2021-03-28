import os
from pathlib import Path
from contextlib import redirect_stdout
from config import *


if __name__ == "__main__":
    driver = configuration()
    tcc_path = "./Arquivos/TCC"
    arqs = os.listdir(tcc_path)
    with open('out.md', 'w',encoding="utf-8") as f:
        with redirect_stdout(f):
            for arq in arqs:
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
                    for i in range(7,len(infos)-1):
                        subjectsD.append(infos[i].text)
                subjects = "### "
                for s in subjectsD:
                    if(subjects == "### "):
                        subjects =subjects+ s
                    else:
                        subjects = subjects +", " + s
                print(subjects)
                print('<a href="'+ str(url[1])+'" target="blank">'+str(title)+'</a>')
                print()
                print()
            