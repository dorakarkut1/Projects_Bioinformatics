import tkinter as tk
from pytube import YouTube
import os 
import subprocess

window = tk.Tk()
window.title("Youtube video downloader application")
frame_a = tk.Frame()


greeting = tk.Label(text="Welcome to youtube Downloader Application", font="Comic 15 italic")
greeting.pack()
enter = tk.StringVar()
enter.set("Enter the link below and choose file type")
tk.Entry(window, textvariable=enter, width=40).pack()
link = tk.StringVar()
tk.Entry(frame_a, textvariable=link, width=40).pack(side='left')

frame_a.pack()

def mp4tomp3():
    yt = YouTube(link.get())
    video = yt.streams.first()
    parent_dir= r'C:\Users\dorak\Desktop'
    video.download(parent_dir)
    default_filename = video.default_filename
    new_filename = list(default_filename )
    new_filename = ''.join(new_filename[:-3]) + 'mp3'
    subprocess.run([
        'ffmpeg',
        '-i', os.path.join(parent_dir, default_filename),
        os.path.join(parent_dir, new_filename)
    ])
    os.remove(os.path.join(parent_dir, default_filename))

def download():

    try:
        file_type = variable.get()
        enter.set("Downloading...")
        window.update()
        print(file_type)
        if file_type != 'MP4':
            mp4tomp3()
        else:
            YouTube(link.get()).streams.first().download()
            print(YouTube(link.get()).streams.first().download())
        link.set("Video downloaded successfully")
        enter.set(" ")
    except Exception as e:
        enter.set("Mistake")
        window.update()
        link.set("Enter correct link")
        
OPTIONS = [
"MP3",
"MP4"
]
variable = tk.StringVar(frame_a)
variable.set(OPTIONS[0]) # default value
w = tk.OptionMenu(frame_a, variable, *OPTIONS)
w.pack(side='left')
frame_a.pack()  
tk.Button(window, text="Download video", command=download).pack()

window.mainloop()







