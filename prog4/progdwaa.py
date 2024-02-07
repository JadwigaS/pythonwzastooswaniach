import argparse #do parsowania argumentów
import numpy as np
import random
import math
import time
from numba import jit
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

#class stan:
a=np.ones((args.n,args.n),dtype=int)
for i in range (args.n) :
   for e in range(args.n):
      if random.random() <= args.up:
         a[i,e]=1
      else:
         a[i,e]=-1
size=args.n-1
n=size+1
J=args.J
B=args.B
@jit(nopython=True)    
def deltaE(i,e):        
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
     
    Ej=-J*(a[i,em]+a[i,ep]+a[im,e]+a[ip,e])*(-a[i,e])- B*(-a[i,e])
    Ez=-J*(a[i,em]+a[i,ep]+a[im,e]+a[ip,e])*a[i,e]- B*a[i,e] #to jest - Ej bo tylko si jest odwrotne
    return Ej-Ez
def deltaEslow(i,e):
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
     
    Ej=-J*(a[i,em]+a[i,ep]+a[im,e]+a[ip,e])*(-a[i,e])- B*(-a[i,e])
    Ez=-J*(a[i,em]+a[i,ep]+a[im,e]+a[ip,e])*a[i,e]- B*a[i,e] #to jest - Ej bo tylko si jest odwrotne
    return Ej-Ez

@jit(nopython=True) 
def mag():
      M=0.0
      for i in range (n) :
        for e in range(n):
           M=M+a[i,e]
      M=M/(n*n)
      return M
def magslow():
      M=0.0
      for i in range (n) :
        for e in range(n):
           M=M+a[i,e]
      M=M/(n*n)
      return M

  
if args.mag:
   f = open(args.mag, "w") 
else:
   f=1 

images = []
#s=stan()
#print(s.a)
ile=args.n*args.n
et=time.time()
for j in track(range(args.l),description="makroki postęp"):
 # if j%10==0:
   if args.ob:
     im=args.ob+str(j)+".PNG"
     #a= np.random.randint(255, size=(400, 400), dtype=np.uint8)
     an=np.uint8(np.copy(a)+1)
     an=an*255
     #print(a)
     obrazek=Image.fromarray(an)
     obrazek.save(im)
       
   for i in range(ile):
     if i%args.n ==0:
         if args.anim:
             an=np.uint8(np.copy(a) +1)
             an=an*255     
             obrazek=Image.fromarray(an)
             images.append(obrazek)
     x=random.randint(0,args.n-1)
     y=random.randint(0,args.n-1)
     dE=deltaE(x,y) 
     if dE<0:
      #print(s.a[x,y])
      if a[x,y]==1:
        a[x,y]=-1
      else:
         a[x,y]=1
     elif random.random() > math.exp(-args.beta*dE) :
       if a[x,y]==1:
        a[x,y]=-1
       else:
         a[x,y]=1
   L=[str(j)+"\t"+str(mag())+"\n"]
   if  f !=1:
    f.writelines(L)
  
 # print(s.mag())
#print(s.a)
bt=time.time()
if args.anim:
   an=np.uint8(a+1)
   an=an*255
   obrazek=Image.fromarray(an)
   images.append(obrazek)
   images[0].save(args.anim,save_all=True,append_images=images, optimize=False, duration=2, loop=0)
if f!=1:
  f.close()
ct=time.time()

print("czas wykonania ="+ str(bt-et) )
print("zapis animacji =" + str(ct-bt))
et=time.time()
for j in track(range(args.l),description="makroki postęp"):
 
       
   for i in range(ile):
     if i%args.n ==0:
         if args.anim:
             an=np.uint8(np.copy(a) +1)
             an=an*255     
             obrazek=Image.fromarray(an)
             images.append(obrazek)
     x=random.randint(0,args.n-1)
     y=random.randint(0,args.n-1)
     dE=deltaEslow(x,y) 
     if dE<0:
      #print(s.a[x,y])
      if a[x,y]==1:
        a[x,y]=-1
      else:
         a[x,y]=1
     elif random.random() > math.exp(-args.beta*dE) :
       if a[x,y]==1:
        a[x,y]=-1
       else:
         a[x,y]=1
   L=[str(j)+"\t"+str(magslow())+"\n"]
   if  f !=1:
    f.writelines(L)
  
 # print(s.mag())
#print(s.a)
bt=time.time()
print("czas wykonania bez numby ="+ str(bt-et) )
## dla paramatrów  n=100 l=1000 t_wyk = 50.11628794670105, bez numby t= 245.12046813964844