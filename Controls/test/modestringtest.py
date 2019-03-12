#!/usr/bin/python3
# *-* coding: utf-8 *-*

class poop():

  def function1(self,x):
      x = x.split(',')
      x = list(map(int,x))
      print("This is function1, here is x: ",x)

  def function2(self):
      print("Function2")

  def run(self):
    x = ["function1","function2"]
    y = ['1,2,3',None]
    func = []
    for z in x:
      func.append(getattr(self,z))
    for i in range(len(func)):
      print(i)
      if y[i] is not None:
        print("if")
        func[i](y[i])
      else:
        print('else')
        func[i]()

if __name__ == "__main__":
    turd = poop()
    turd.run()
