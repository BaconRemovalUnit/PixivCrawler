from bs4 import BeautifulSoup
from os import mkdir,path
import requests
import time

def Crawl(output_folder):

    if not path.isdir(output_folder):
        mkdir(output_folder)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Referer':'https://www.pixiv.net/login.php?return_to=0'}

    #read all tags
    r = requests.get("http://www.pixiv.net/tags.php",headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    link_tags = soup.findAll("ul",{"class":"tag-list inline-list slash-separated"})
    links = link_tags[0].findAll("a",text=True)

    for i in links:
        tag = i.get("href")
        #open a new site
        for page in range(1,11):
            r = requests.get("http://www.pixiv.net/search.php?word="+str(tag.split("=")[1])+
                        "&p="+str(page),headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            link_tags = soup.findAll("a", {"class": "work _work "})
            for link in link_tags:
                image_link = str(link.get("href"))
                s = requests.get("http://www.pixiv.net"+image_link,headers=headers)
                broth = BeautifulSoup(s.text,'html.parser')
                image_wrapper = broth.findAll("a",{"data-title":"registerImage"})
                image = image_wrapper[0].findAll("img")[0]
                imgurl = image.get("src")
                replaceChar = ["\\","/","|",":","*","?","<",">","\"","."]
                imgname = str(image.get("title"))
                imgtype = str(imgurl).split(".")[len(str(imgurl).split("."))-1]
                for char in replaceChar:
                    imgname = imgname.replace(char,"-")
                #contains the image data

                file_name = output_folder+imgname+"."+imgtype
                if not path.isfile(file_name):  # if file exists
                    print("Downloading: ",imgname,".",imgtype)
                    with open(file_name, 'wb') as handle:
                        t = requests.get(imgurl,headers=headers,stream=True)
                        if t.status_code == 200:
                            for block in t.iter_content(1024):
                                handle.write(block)
                else:
                    print("File exists: ",imgname,".",imgtype)
                time.sleep(0.5)
                yield file_name


Crawl("./input/")