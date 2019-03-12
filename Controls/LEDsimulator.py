class LED():

  def __init__(self, redpin, greenpin, bluepin):
    self.redpin = redpin
    self.greenpin = greenpin
    self.bluepin = bluepin
    self.redpwm = 0
    self.greenpwm = 0
    self.bluepwm = 0
    self.bright = 1
    self.color = 0
