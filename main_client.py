import tkinter as tk

#from constants import *

with open("./constants.txt", "r") as f:
    lns = f.readlines()
    for l in lns:
    #    print(l)
        exec(l)

from PIL import ImageTk, Image
import numpy as np
from pyautogui import screenshot
import socket
from helpers import send_msg, receive_msg

# import torch

"""HOW TO BUILD: (base) leon@leon-desktop:/media/leon/2tbssd/cic_gui_clean$ 
pyinstaller --onefile --windowed main_client.py"""

# import torchxrayvision as xrv


# TEST_IMG = "/home/leon/Pictures/img_lights.jpg"

# def analyse_arr(arr):
#    model = xrv.models.DenseNet(weights='all')
#    arr = arr[:, :, 0]
#    inp = torch.tensor(arr, dtype=torch.float).unsqueeze(0).unsqueeze(0)
#    probs = model(inp)
#    return probs


pathologies = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 'Edema', 'Emphysema', 'Fibrosis',
               'Effusion', 'Pneumonia', 'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', 'Hernia', 'Lung Lesion',
               'Fracture', 'Lung Opacity', 'Enlarged Cardiomediastinum']


class Application(tk.Frame):
    def __init__(self, socket_: socket.socket, master=None, **config):
        super().__init__(master)
        self.master = master
        self.socket = socket_
        self.array = None
        self.config(config)  # change config of Application here..
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.status = tk.Label(self, text="Status idle")
        self.status.pack(side='top')
        self.hi_there = tk.Button(self)
        self.hi_there['text'] = "ANALYSE"
        self.hi_there['command'] = self.say_hi
        self.hi_there['fg'] = 'red'
        self.hi_there.pack(side='top')

        self.send_screen_button = tk.Button(self, text="Send screenshot", bg="white",
                                            command=lambda: self.send_screenshot())
        self.send_screen_button.pack(side="top")

        # self.display_image_button = tk.Button(self, text="Display image", bg="white",
        #                                      command=lambda: self.display_image_arr())
        # self.display_image_button.pack(side="top")

        self.quit = tk.Button(master=self, text='QUIT', fg='red', bg='blue',
                              command=self.master.destroy)  # first arg is master!, fg is text color!
        self.quit.pack(side='bottom')

    def display_screenshot(self):
        self.im = ImageTk.PhotoImage(screenshot())  # screenshot())  # Image.fromarray(screenshot()))
        if hasattr(self, 'panel'):  # destroy existing panel..
            self.panel.destroy()
        self.panel = tk.Label(self,
                              image=self.im)  # NEEDS TO BE SELF- you need to keep the reference,
        # if it disappears (due to function return) it will not work
        self.panel.pack(fill='both', expand='yes')

    def display_array(self, array):
        self.array = array
        print(self.array.shape)
        self.im = ImageTk.PhotoImage(
            image=Image.fromarray(array))  # self.array))  # screenshot())  # Image.fromarray(screenshot()))
        if hasattr(self, 'panel'):  # destroy existing panel..
            self.panel.destroy()
        self.panel = tk.Label(self,
                              image=self.im)  # NEEDS TO BE SELF- you need to keep the reference,
        # if it disappears (due to function return) it will not work
        self.panel.pack(fill='both', expand='yes')

    def send_screenshot(self):
        self.status['text'] = "sending screenshot..."
        self.status.update()
        screen = np.array(screenshot())
        self.status['text'] = "screenshot taken and converted \n sending screenshot... "
        self.status.update()
        send_msg(self.socket, screen)
        msg = receive_msg(self.socket)
        self.status['text'] = "recieved from server: " + msg
        self.array = receive_msg(self.socket)
        try:
            self.display_array(self.array)
        except:
            print("failed to display array")
            pass
        self.status['text'] += "\n"
        probs = receive_msg(self.socket)
        path = dict()
        for idp, p in enumerate(pathologies):
           path[p] = probs[0, idp]
        sort = sorted(path.items(), key=lambda x: x[1], reverse=True)
        txt = str()
        for p, no in sort:
           txt += str(p) + "  " + str(no) + "\n"
        self.status['text'] +=txt



    def say_hi(self):
        return
        # print("hi world")
        # if self.array is not None:
        #    probs = analyse_arr(self.array)
        # path = dict()
        # probs = probs.detach().cpu().numpy()
        # for idp, p in enumerate(xrv.datasets.default_pathologies):
        #    path[p] = probs[0, idp]
        # sort = sorted(path.items(), key=lambda x: x[1], reverse=True)
        # txt = str()
        # for p, no in sort:
        #    txt += str(p) + "  " + str(no) + "\n"
        # self.hi_there.config(text=txt)  # config doesnt override existing configs..


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_opt['TCP_IP'], server_opt['TCP_PORT']))
    root = tk.Tk()
    app = Application(master=root, bg='blue', socket_=s)
    app.mainloop()
