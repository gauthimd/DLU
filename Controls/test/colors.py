import re #regular expressions

class Color():

  def __init__(self, hexcode): #hexcode is string of from '#ae32ff' 
    try: #if the hexcode fails, you get nuthin
      match = re.match(r'#[0-9A-Fa-f]{6}', hexcode)
      code =  match.group()
      red = int(code[1:3],16)
      green = int(code[3:5],16)
      blue = int(code[5:],16)
      self.redpwm = int(red*16.059)   #Convert 8 bits to 12 bits 
      self.greenpwm = int(green*16.059)   
      self.bluepwm = int(blue*16.059)
    except: pass
