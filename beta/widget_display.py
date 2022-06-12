import json
from tkinter import *
from tkinter import ttk

def warn(warning_message='', background='#4d0000', foreground='white'):
    root=Tk()
    root.geometry('400x200')
    root.config(background=background)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.overrideredirect(True)

    # https://stackoverflow.com/questions/14910858/how-to-specify-where-a-tkinter-window-opens
    # height and width for the Tk root
    w, h = 320, 100

    x_shift_percent, y_shift_percent = 80, 75

    # get screen width and height
    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2) + x_shift_percent*ws/200
    y = (hs/2) - (h/2) + y_shift_percent*hs/200

    # set the dimensions of the screen 
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    warning_message_label=Label(
        text=warning_message,
        font=('Segoe UI Semibold', 12),
        background=background,
        foreground=foreground
    )

    slider = ttk.Scale(
        root,
        from_=0,
        to=100,
        orient='vertical',  # horizontal
    )


    warning_message_label.grid(row=0, column=0, sticky='news')
    slider.grid(row=1, column=1, sticky='news')

    root.mainloop()

def current_song_information():
    # Song name, type, volume
    with open('../data/current-song-info.json') as fp:
        return json.load(fp)

if __name__ == '__main__':
    cur_song_info = current_song_information()
    warn(warning_message=cur_song_info['currentSongName'])
