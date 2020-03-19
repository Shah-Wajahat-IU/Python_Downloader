import sys
from tkinter import Tk, Label, Button, Entry, filedialog, TOP, X, DISABLED, NORMAL, END, messagebox, ttk, Frame, \
    VERTICAL, HORIZONTAL
from tkinter.ttk import Progressbar
from pytube import YouTube
from threading import Thread
import requests
from bs4 import BeautifulSoup

file_size = 0
finish = False
def progress(chunk=None, file_handle=None, remaining=None):
    file_downloaded = file_size - remaining
    # print(remaining)
    per = (file_downloaded / file_size) * 100
    btn.config(text="{:0.00f} % downloading".format(per))
    pro = Progressbar(frame2, length=425, orient=HORIZONTAL, maximum=100)
    pro.grid(row=1, column=1, sticky="nsew", padx=50)
    pro['value'] = "{:0.00f}".format(per)

    perLabel.config(text="{:0.00f} % downloading".format(per))


def Downloader():
    global file_size, pro, perLabel, frame2
    frame2 = Frame(frame1)
    frame2.pack(fill="x", expand=True)
    titleLabel = Label(frame2, text='',padx=5)
    titleLabel.grid(row=0, column=1,sticky="nsew")



    '''pro = Progressbar(frame2,length=425,orient=HORIZONTAL,maximum=100)
    pro.grid(row=1, column=1,sticky="nsew",padx=50)'''

    perLabel = Label(frame2, text='',padx=5)
    perLabel.grid(row=2, column=1)
    frame2.pack(fill="x", expand=True)
    try:
        path_directory = filedialog.askdirectory()
        video_url = url_entry.get()
        # print(video_url)
        if 'watch' in  video_url:
            youtube = YouTube(video_url, on_progress_callback=progress)
            btn.config(text='Please wait...', state=DISABLED)
            t = youtube.title
            titleLabel.config(text=t)
            video = youtube.streams.filter(progressive=True, file_extension='mp4', fps=30, ).first()
            file_size = video.filesize
            video.download(path_directory)
        else:
            page = requests.get(video_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            urlList = set()
            for a_tag in soup.findAll("a"):
                if a_tag.has_attr("href") and 'watch' in a_tag["href"]:
                    url = 'https://www.youtube.com' + a_tag['href']

                    urlList.add(url)
            print(len(urlList))

            btn.config(text='Please wait...', state=DISABLED)


            print(path_directory)
            for urls in urlList:
                print(urls)
                youtube = YouTube(urls, on_progress_callback=progress)
                t = youtube.title
                print(t)
                titleLabel.config(text=t)
                video = youtube.streams.filter(progressive=True, file_extension='mp4', fps=30, ).first()
                # video_Detail=youtube.streams.all()
                # print(video_Detail)
                file_size = video.filesize

                # print(file_size)
                video.download(path_directory)

        btn.config(text='Download Start', state=NORMAL)
        url_entry.delete(0, END)
        titleLabel.config(text='')
        perLabel.config(text='')
        pro.destroy()
        messagebox.showinfo("Done", "Downloaded Done")
    except Exception as e:
        print(e)
        btn.config(text='Download Start', state=NORMAL)
        url_entry.delete(0, END)
        titleLabel.config(text='')
        perLabel.config(text='')
        messagebox.showinfo("Done", "Downloaded Done")
        pro.destroy()
        sys.exit()

    #  display2.config(text=e)


def Download_Thread():
    global thread
    thread = Thread(target=Downloader)
    thread.start()


window = Tk()
window.title("Video Downloader")
frame1 = Frame(window)
frame1.pack(fill="both", expand=True)
rowFrame1 = Frame(frame1)
url_label = Label(rowFrame1, text="Enter Url")
url_label.grid(row=0, column=0, padx=10)
url_entry = Entry(rowFrame1)

url_entry.grid(row=0, column=1, ipadx=120)

btn = Button(rowFrame1, text='Download Start', command=Download_Thread)
btn.grid(row=0, column=3, padx=10)
#ext = Button(rowFrame1, text='Quit', command=Close_Window)
#ext.grid(row=1, column=3, padx=10)
rowFrame1.pack(fill="x")

'''display=Label(window,text='')
display.pack()
display2=Label(window,text='')
display.pack()'''

window.geometry("550x270")
window.mainloop()