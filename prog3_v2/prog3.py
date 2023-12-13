import functools
import time
import numpy
class ObjectDecorator:
     def __init__(self, func):
      self.func = func
      self.counter = 0
      self.times=list()
     def __call__(self,*args, **kwargs):
         start_time = time.perf_counter()    
         self.func(*args, **kwargs)
         end_time = time.perf_counter()      
         run_time = end_time - start_time    
         print(f"Finished {self.func.__name__!r} in {run_time:.4f} secs")
         self.counter+=1
         self.times.append(run_time)
     def statystyki(self):
         print("max="+str(max(self.times)))
         print("min="+str(min(self.times)))
         print("avg="+str(numpy.average(self.times)))
         print("stdev="+str(numpy.std(self.times)))

             
         
@ObjectDecorator
def my_function():
    print("Hello World!")
    numpy.ones((5000,50000))
my_function()
my_function()
my_function()
my_function()
my_function()
my_function.statystyki()