from sense_hat import SenseHat
from flask import Flask


class GetProp():
    def __init__(self, senseHat: SenseHat):
        self._s = senseHat
        humidity = lambda: self._s.show_message(f"{self._s.get_humidity():.2} %")
        temperature = lambda: self._s.show_message(f"{self._s.get_temperature():.2} °C")
        pressure = lambda: self._s.show_message(f"{self._s.get_pressure():.2} mbar")
        self._props = [humidity, temperature, pressure]
        self._selector = 0

    def ShowProp(self):
        """Shows the value of the currently selected property"""
        self._props[self._selector]()

    def changeProp(self):
        """Switches to the next property"""
        self._selector = (self._selector + 1) % len(self._props)
        self._showSelection()
        
    def _showSelection(self):
        """Shows the selected property"""
        c = ''
        match self._selector:
            case 0:
                c = 'H'
            case 1:
                c = 'T'
            case 2:
                c = 'P'
        self._s.show_letter(c)
            


s = SenseHat()
prop = GetProp(s)

#TODO Move into new script if broken during sleep
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/temp")
def get_temp():
    return str(s.get_temperature())
@app.route("/pressure")
def get_pressure():
    return str(s.get_pressure())
@app.route("/humidity")
def get_humidity():
    return str(s.get_humidity())
    
while True:
    event = s.stick.wait_for_event(emptybuffer=True)
    if event is None:
        continue
    match event.direction:
        case "middle":
            prop.ShowProp()
        case "up":
            s.flip_v()
        case "right":
            s.flip_h()
        case "left":
            prop.changeProp()
        case "down":
            pass
            #change color?


