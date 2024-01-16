import argparse #do parsowania argumentów
import numpy as np
import random
import math
import time
from rich.progress import track
from PIL import Image,ImageDraw
parser = argparse.ArgumentParser(description='program 1')
parser.add_argument('J',type=float)
parser.add_argument('B',type=float)
parser.add_argument('beta',type=float)
parser.add_argument('n',type=int) #rozmiar siatki
parser.add_argument('l',type=int)#liczba kroków
parser.add_argument('-up',default=0.5,type=float) #gestosc spinu
parser.add_argument('-ob',help='plik obrazki') #to dodaje obowiązkowy argument
parser.add_argument('-anim',help='plik animacja')
parser.add_argument('-mag',help='plik magnetyzacja')
args=parser.parse_args() #to parsuje 

class stan:
  a=np.ones((args.n,args.n),dtype=int)
  def __init__(self):
    
    for i in range (args.n) :
        for e in range(args.n):
          if random.random() <= args.up:
              self.a[i,e]=1
          else:
             self.a[i,e]=-1
  def deltaE(self,i,e):
     size=args.n-1
     
     ip=i+1
     im=i-1
     ep=e+1
     em=e-1
     
     if i==size: #zapętlanie tabelki
       ip=0
     elif i==0:       
        ip=size
     if e==size:
        ep=0
     elif e==0:
        em=size
     
     Ej=-args.J*(self.a[i,em]+self.a[i,ep]+self.a[im,e]+self.a[ip,e])*(-self.a[i,e])- args.B*(-self.a[i,e])
     Ez=-args.J*(self.a[i,em]+self.a[i,ep]+self.a[im,e]+self.a[ip,e])*self.a[i,e]- args.B*self.a[i,e] #to jest - Ej bo tylko si jest odwrotne
     return Ej-Ez
  def mag(self):
      M=0.0
      for i in range (args.n) :
        for e in range(args.n):
           M=M+self.a[i,e]
      M=M/(args.n*args.n)
      return M
     
  
if args.mag:
   f = open(args.mag, "w") 
else:
   f=1 

images = []
s=stan()
#print(s.a)
ile=args.n*args.n
et=time.time()
for j in track(range(args.l),description="makroki postęp"):
 # if j%10==0:
   if args.ob:
     im=args.ob+str(j)+".PNG"
     #a= np.random.randint(255, size=(400, 400), dtype=np.uint8)
     a=np.uint8(np.copy(s.a)+1)
     a=a*255
     #print(a)
     obrazek=Image.fromarray(a)
     obrazek.save(im)
  # if args.anim:
   #  a=np.uint8(np.copy(s.a) +1)
     #a=a*255
     
    # obrazek=Image.fromarray(a)
    # images.append(obrazek)
      
      
   for i in range(ile):
     if i%args.n ==0:
         if args.anim:
             a=np.uint8(np.copy(s.a) +1)
             a=a*255     
             obrazek=Image.fromarray(a)
             images.append(obrazek)
     x=random.randint(0,args.n-1)
     y=random.randint(0,args.n-1)
     dE=s.deltaE(x,y) 
     if dE<0:
      #print(s.a[x,y])
      if s.a[x,y]==1:
        s.a[x,y]=-1
      else:
         s.a[x,y]=1
     elif random.random() > math.exp(-args.beta*dE) :
       if s.a[x,y]==1:
        s.a[x,y]=-1
       else:
         s.a[x,y]=1
   L=[str(j)+"\t"+str(s.mag())+"\n"]
   if  f !=1:
    f.writelines(L)
  
 # print(s.mag())
#print(s.a)
bt=time.time()
print(bt-et)
if args.anim:
   a=np.uint8(s.a+1)
   a=a*255
   obrazek=Image.fromarray(a)
   images.append(obrazek)
   images[0].save(args.anim,save_all=True,append_images=images, optimize=False, duration=2, loop=0)
if f!=1:
  f.close()