# iris.py
from flask import Flask, render_template, Markup, make_response
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)
sliders = ""
sliders_elem = ""
db = {}
stream_html = ""


@app.route("/")
def index():
    return render_template("index.html", sliders_elem=Markup(sliders_elem), stream_html=Markup(stream_html))


@app.route("/sliders.js")
def sliderjs():
    resp = make_response(sliders)
    resp.mimetype = "text/javascript"
    return resp


# Round-trip latency
@socketio.on("rt_ping")
def rt_response():
    emit("rt_pong")


@socketio.on("update")
def update(message):
    name = message["object"]
    low = float(message["values"][0])
    high = float(message["values"][1])

    db[name] = [int(round(low)), int(round(high))]

    # print(round("Double slider \"" + name + "\" reported: " + low + ", " + high)


# @param name Name of slider (ASCII only and no spaces)
# @param min Lower bound
# @param max Higher bound
def slider(name, min, max):
    global sliders, sliders_elem

    low_bound = (max - min) / 2 - 10
    high_bound = (max - min) / 2 + 10

    sliders_elem += "<p>" + name + "</p><div id='" + name + "_elem'></div><br>"
    sliders += """
            const """ + name + """_sldr = document.getElementById(\"""" + name + """_elem\");
            
            noUiSlider.create(""" + name + """_sldr, {
                start: [""" + str(low_bound) + """, """ + str(high_bound) + """],
                connect: true,
                range: {
                    'min': """ + str(min) + """,
                    'max': """ + str(max) + """
                }
            });
            
            """ + name + """_sldr.noUiSlider.on('update', function (values) {
                socket.emit("update", {
                    "object": '""" + name + """',
                    "values": values,
                })
            });
        """

    db[name] = [int(round(low_bound)), int(round(high_bound))]  # Update data the first time


# url of mjpeg stream or other video src
def stream(url):
    global stream_html
    stream_html += """
    <div class="grid-item">
        <img src=\"""" + url + """\" alt="">
    </div>"""


# Get a value from the db
def get(name):
    return db[name]


# Start the server in a new thread
def serve(**kwargs):
    server = threading.Thread(target=socketio.run, args=[app], kwargs=kwargs)
    server.start()
