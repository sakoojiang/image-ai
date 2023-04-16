import  os
def markdownDict():
    dict={}
    basepath="markdowns"
    with os.scandir(basepath) as entries:
        for entry in entries:
            with open(entry.path,encoding='utf-8') as file:
                content=file.read()
                tmps=content.split("--split--")
                i=0
                for tmp in tmps:
                   key=entry.name.replace(".md","")
                   dict[key+str(i)]=tmp
                   i+=1
    return dict


dict=markdownDict()
