import requests
from bs4 import BeautifulSoup
import json
from os.path  import basename
from PIL import Image, ImageFilter
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
def akcja(nazwa):
         
         if(".png" in nazwa):
             miejsce='http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'+nazwa
             with open(basename(miejsce), "wb") as f:
                 img_data = requests.get(miejsce).content            
                 f.write(img_data)
             img=Image.open(nazwa)
             img=img.convert("L")
             img=img.filter(ImageFilter.GaussianBlur(radius = 9))
             img.save(nazwa)
if __name__ == '__main__':
    res = requests.get('http://www.if.pw.edu.pl/~mrow/dyd/wdprir/')
#print(res.status_code)
#print(res.headers)
#print(res.text)

    soup = BeautifulSoup(res.content,'html.parser')


    start = time.time()
    for link in soup.select('a', href=True):
    
        akcja(link['href'])
    end = time.time()
    print(end - start)
   

    start = time.time()
 

    with ProcessPoolExecutor(multiprocessing.cpu_count()) as ex:
       
        futures = [ex.submit(akcja,i['href']) for i in soup.select('a', href=True)] 
      
           
    end = time.time()
    print(end - start)