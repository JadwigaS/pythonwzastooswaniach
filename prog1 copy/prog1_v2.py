#program ma zrobić histogram wystepującyhc słow w tekscie
import argparse #do parsowania argumentów

parser = argparse.ArgumentParser(description='program 1')
parser.add_argument('filename',help='nazwa plikudo czytania') #to dodaje obowiązkowy argument
parser.add_argument('-hi',default=10,type=int,help='ile słów wyświetla histogram') #to dodaje obowiązkowy argument
parser.add_argument('-m',default=0,type=int,help='minimalna długośsłowa') #to dodaje obowiązkowy argument


args=parser.parse_args() #to parsuje 

f=open(args.filename,'r')



#print( zawartosc)
x={}

for a in range(1000):
    zawartosc=f.readline()
    for i in zawartosc.split():
        
        if len(i) >= args.m:
            if i in x:
                x[i]=x[i]+1
            else:
                x[i]=1
    
   # print(a)

f.close()
h={}
iloscslowa=max(x.values())
a=0
#print(x)

while a <= args.hi:
    for i in x:
        if x[i]==iloscslowa:
          #  print(x[i])
            h[i]=x[i]
            a=a+1
          
    if a==args.hi:
        break
    iloscslowa=iloscslowa-1
   # print(iloscslowa)
    if iloscslowa==0:
        break


#print(max(x.values()))
#print(h)

from ascii_graph import Pyasciigraph
from ascii_graph import colors

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

graph = Pyasciigraph()
for line in  graph.graph('histogram', h.items()):
    print(line)