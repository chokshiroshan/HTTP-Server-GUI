import http.server,socketserver,os,socket,qrcode,random,time
import PySimpleGUI as sg
import threading
layout = [
              [sg.Text('Select Directory:'), sg.FolderBrowse()],
              [sg.Image('i.jpg',key='img')],
              [sg.Button(button_text='Create Server')]
             ]
window = sg.Window('HTTP Server', layout)

class server(object):
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        httpd = socketserver.TCPServer(("", PORT), Handler)
        httpd.serve_forever()


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_port():
    return random.randint(8000, 8100)

def create_qr():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('http://'+ IP +':'+str(PORT))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("image.jpg")

def set_path():
    web_dir = os.path.join(os.path.dirname(__file__), values['Browse'])
    os.chdir(web_dir)



while True:
    event, values = window.Read()
    IP = get_ip()
    PORT = get_port()

    Handler = http.server.SimpleHTTPRequestHandler
    try:
        create_qr()
        window.Element('img').Update('image.jpg')
        if values['Browse'] == '':
            break
        set_path()
    except:
        PORT = get_port()
        create_qr()
        window.Element('img').Update('image.jpg')
        if values['Browse'] == '':
            break
        set_path()

    print("serving at port", PORT)
    print(IP+':'+str(PORT))

    s = server()



