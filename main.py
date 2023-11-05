import tkinter as tk
import asyncio
import requests
from tkinter import messagebox
from playsound import playsound
last_label_frame = None


def get_data(url):
    response = requests.get(url)
    data = dict(response.json()[0])

    return data


def word_description():
    global last_label_frame
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_input.get()}"
        audio_urls = []
        meanings = []
        data = get_data(url)
        for phonetic in data["phonetics"]:
            audio_urls.append(phonetic["audio"])

        for meaning in data["meanings"]:
            meanings.append(meaning)


        setData(audio_urls, meanings)

        word_input.delete(0, tk.END)
    except Exception:
        print(Exception)
        if(last_label_frame):
            last_label_frame.destroy()
        last_label_frame = create_labelList()
        word_input.delete(0, tk.END)
        messagebox.showinfo("No explain", "There is not response from API for the word")







def setData(audios, meanings):
    global frame_row, frame_column, last_label_frame

    frame_row = 0
    frame_column = 1

    if(last_label_frame):
        last_label_frame.destroy()


    labelFrame = create_labelList()
    labelFrame.configure(text=f"Word Explaining -- {word_input.get()}")
    last_label_frame = labelFrame
    print("audiossssss : ", audios)
    if (audios):
        for audio in audios:
            if (("-us" in audio) or ("-uk") in audio):
                sound_button = create_sound_button(labelFrame)
                sound_url = audio.strip()
                loop = asyncio.get_event_loop()
                sound_button.configure(command=lambda : loop.run_until_complete(play(sound_url)))
            else:
                pass

    async def play(url):
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(None, playsound, url)
        response = await future

    for meaning in meanings:
        label = tk.Label(labelFrame, text=meaning["partOfSpeech"])
        label.configure(font=("Comic Sans MS", 12, "bold"))
        label.pack()
        frame_row += 1
        for definition in meaning["definitions"]:
            label = tk.Label(labelFrame, text=definition["definition"])
            label.configure(font=("Helvetica", 10, "normal"))
            label.pack()
            frame_row += 1
        if(meaning != meanings[-1]):
            label = tk.Label(labelFrame, text="----------------------------------------------------------------")
            label.configure(font=("Helvetica", 10, "normal"))
            label.pack()




def create_labelList():
    label_list = tk.LabelFrame(app, text="Word Explaining", font='Helvetica 15')
    label_list.pack(pady=15)


    return label_list

def destroyData():
    global label_list
    label_list.destroy()


def create_sound_button(rootWidget):
    sound_button = tk.Button(rootWidget, text="Pronunciation")
    sound_button.pack()

    return sound_button




app = tk.Tk()
app.title("English Words")
app.geometry("1200x800")

i_label = tk.Label(text="Enter Word")
i_label.pack()

word_input = tk.Entry()
word_input.pack(padx=15)


play_button = tk.Button(app, text="Get info", command=word_description)
play_button.pack(pady=15)



app.mainloop()
