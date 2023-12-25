from sense_hat import SenseHat
from flask import Flask
from threading import Thread


class GetProp():
    def __init__(self, senseHat: SenseHat):
        self._s = senseHat
        humidity = lambda: self._s.show_message(f"{self._s.get_humidity():.4} %")
        temperature = lambda: self._s.show_message(f"{self._s.get_temperature():.4} °C")
        pressure = lambda: self._s.show_message(f"{self._s.get_pressure():.4} mbar")
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
            
def mainLoop(s: SenseHat):
    prop = GetProp(s)
    s.clear()
    s.show_message("HEY!", scroll_speed=0.05)
    print("start mainLoop")
    while True:
        event = s.stick.wait_for_event(emptybuffer=True)
        if event is None:
            print(f"event: {event} is None!!!")
            continue
        match event.direction:
            case "middle":
                print("pressed middle")
                prop.ShowProp()
            case "up":
                #TODO replace with accelerometer
                print("pressed up")
                s.flip_v()
            case "right":
                #TODO replace with accelerometer
                print("pressed right")
                s.flip_h()
            case "left":
                print("pressed left")
                prop.changeProp()
            case "down":
                print("pressed down")
                pass
                #change color?
            case _:
                print("default case!?")

app = Flask(__name__)
s = SenseHat()
s.low_light = True

@app.route("/")
def hello_world():
    return """
            <p>Hello, World!</p>
            <p><a href="/temp">Temperature</a></p>
            <p><a href="/pressure">Pressure</a></p>
            <p><a href="/humidity">Humidity</a></p>
            """

@app.route("/temp")
def get_temp():
    return f"{s.get_temperature():.6} °C"
@app.route("/pressure")
def get_pressure():
    return f"{s.get_pressure():.6} mbar"
@app.route("/humidity")
def get_humidity():
    return f"{s.get_humidity():.6} %"
@app.route("/msg/<text>")
def msg(text:str):
    #t = Thread(target=s.show_message, args=[text])
    #t.start()
    s.show_message(text,scroll_speed=0.05)
    return text

t2 = Thread(target=mainLoop, args=[s])
t2.start()

#app.run(host="0.0.0.0")
t1 = Thread(target=app.run, kwargs={'host': "0.0.0.0"})
t1.start()
