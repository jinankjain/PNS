#https://stackoverflow.com/questions/31666584/beutifulsoup-to-extract-all-external-resources-from-html

from bs4 import BeautifulSoup 
def find_list_resources (tag, attribute,soup):
   mylist = []
   for x in soup.findAll(tag):
       try:
           mylist.append(x[attribute])
       except KeyError:
           pass
   return(mylist)

with open('example-page.html', 'r') as html:
    soup = BeautifulSoup(html, "html.parser")

    image_src = find_list_resources('img',"src",soup)   
    script_src = find_list_resources('script',"src",soup)    
    css_link = find_list_resources("link","href",soup)
    video_src = find_list_resources("video","src",soup)         
    audio_src = find_list_resources("audio","src",soup) 
    iframe_src = find_list_resources("iframe","src",soup)
    embed_src = find_list_resources("embed","src",soup)
    object_data = find_list_resources("object","data",soup)         
    source_src = find_list_resources("source","src",soup)

    print iframe_src
