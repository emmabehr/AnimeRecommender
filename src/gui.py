import sys
import threading
from tkinter import *

import csv_util
from recommendation_engine_constants import DATA_PATH
import recommendation_engine_trainer as ml_trainer
import recommendation_engine as ml_engine

def toolsTrainEngineClicked(event):
    threading.Thread(target=trainEngine).start()

def trainEngine():
    ml_trainer.trainModel()

def getRecommendations(event):
    threading.Thread(target=fetchRecommendations).start()

def toggleActionInProgress(in_progress):
    state = DISABLED if in_progress else NORMAL
    anime_searchbox_button.config(state=state)
    tool_menu.entryconfig(0, state=state)

def fetchRecommendations():
    toggleActionInProgress(True)

    selected_anime = anime_searchbox.get()
    print(f"Search for similar anime to {selected_anime}")

    recommendation_list.delete(0, END)

    similar_animes = ml_engine.getSimilarAnimeByName(anime_searchbox.get())
    if similar_animes is None:
        print(f"Unable to find similar anime for {selected_anime}")
    else:
        for anime in similar_animes:
            if anime["anime_name"] != selected_anime:
                recommendation_list.insert(END, anime["anime_name"])
    
        print(f"Succesfully found similar anime to {selected_anime}")

    toggleActionInProgress(False)

def listAnimes(animes):
    anime_list.delete(0, END)

    for anime in animes:
        anime_list.insert(END, anime)

def filterAnimes(event):
    filtered_anime_list = []
    
    filter_by = anime_searchbox.get()
    my_rating = None
    if filter_by == "":
        filtered_anime_list = [anime["Name"] for anime in anime_info]
    else:
        for anime in anime_info:
            anime_name = anime["Name"]
            if filter_by.lower() in anime_name.lower():
                filtered_anime_list.append(anime_name)
                if filter_by.lower() == anime_name.lower():
                    my_rating = getMyAnimeRatingByName(anime_name)
    setMyRatingLabel(my_rating)

    listAnimes(filtered_anime_list)

def anime_list_clicked(event):
    populateSearchBox(anime_list)

def recommendation_list_clicked(event):
    populateSearchBox(recommendation_list)

def populateSearchBox(list_box):
    anime_name = list_box.get(list_box.curselection())
    my_rating = getMyAnimeRatingByName(anime_name)
    anime_searchbox.delete(0, END)
    anime_searchbox.insert(0, anime_name)
    setMyRatingLabel(my_rating)

def showRateAnimeClicked(event):
    anime_name = anime_searchbox.get()
    my_rating = getMyAnimeRatingByName(anime_name)
    showRateAnime(anime_searchbox.get(), my_rating)

def showRateAnime(anime, rating=5):
    if rating is None:
        rating = 5
    rate_anime_dialog = Toplevel(gui)
    rate_anime_dialog.geometry("300x250")

    rate_label = Label(rate_anime_dialog, text=f"Rate {anime}")
    rate_label.pack()

    rate_box = Spinbox(rate_anime_dialog, from_=0, to=10, textvariable=rating)
    rate_box.delete(0,"end")
    rate_box.insert(0,rating)
    rate_box.pack()
    
    submit_rating = Button(rate_anime_dialog, text= "Submit Rating", command= lambda:rate_anime(rate_box.get(), rate_anime_dialog))
    submit_rating.pack()

    close_rating_dialog = Button(rate_anime_dialog, text="Close", command=lambda:close_rate_dialog(rate_anime_dialog))
    close_rating_dialog.pack()

def close_rate_dialog(dialog):
   dialog.destroy()
def rate_anime(rating, dialog):
    anime_name = anime_searchbox.get()
    anime_id = getAnimeIdByName(anime_name)
    
    if not anime_id is None:
        my_anime_entry = getMyAnimeById(anime_id)

        if my_anime_entry is None:
            my_anime_entry = {"anime_id": anime_id, "rating": rating}
            my_animes.append(my_anime_entry)
        else:
            my_anime_entry["rating"] = rating

        csv_util.writeCSVFile(f"{DATA_PATH}/my_anime.csv", my_animes, ["anime_id", "rating"])
        setMyRatingLabel(rating)

    close_rate_dialog(dialog)

def getAnimeIdByName(anime_name):
    anime_id = None
    for anime in anime_info:
        if anime["Name"] == anime_name:
            anime_id = anime["MAL_ID"]
    return anime_id

def getMyAnimeById(anime_id):
    my_anime_entry = None
        
    for anime in my_animes:
        if anime["anime_id"] == anime_id:
            my_anime_entry = anime

    return my_anime_entry

def getMyAnimeRatingByName(anime_name):
    my_rating = None
    anime_id = getAnimeIdByName(anime_name)
    my_anime = getMyAnimeById(anime_id)
    if not my_anime is None:
        my_rating = int(my_anime["rating"])
    return my_rating

def setMyRatingLabel(rating=None):
    if rating is None:
        anime_rate_text.set("")
    else:
        anime_rate_text.set(f"My rating is: {rating}")

gui = Tk()
gui.title("Anime Recommender")
gui.geometry("600x400")

# menu
menu_bar = Menu(gui)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=gui.destroy)
menu_bar.add_cascade(label="File", menu=file_menu)

tool_menu = Menu(menu_bar, tearoff=0)
tool_menu.add_command(label="Train Engine", command=toolsTrainEngineClicked)
menu_bar.add_cascade(label="Tools", menu=tool_menu)

gui.config(menu=menu_bar)

top_frame = Frame(gui)
top_frame.pack()

# searchbox (and label)
anime_searchbox_frame = Frame(top_frame)
anime_searchbox_frame.pack()
anime_searchbox_label = Label(anime_searchbox_frame, text="Search for Anime Recommendations")
anime_searchbox_label.pack()

anime_searchbox = Entry(anime_searchbox_frame)
anime_searchbox.pack(fill="x")
anime_searchbox.bind("<KeyRelease>", filterAnimes)

anime_rate_text = StringVar()
anime_rate_label = Label(anime_searchbox_frame, textvariable=anime_rate_text)
anime_rate_label.pack()

anime_rate_button = Button(anime_searchbox_frame, text="Rate Anime")
anime_rate_button.pack()
anime_rate_button.bind("<Button-1>", showRateAnimeClicked)

anime_searchbox_button = Button(anime_searchbox_frame, text="Get Recommendations")
anime_searchbox_button.pack()
anime_searchbox_button.bind("<Button-1>", getRecommendations)

middle_frame = Frame(gui)
middle_frame.pack(fill=BOTH, expand=True)

# anime list (and scrollbar)
anime_list_frame = Frame(middle_frame)
anime_list_frame.pack(side=LEFT, fill=BOTH, expand=True)
anime_list = Listbox(anime_list_frame)
anime_list.pack(side=LEFT, fill=BOTH, expand=True)
anime_list_scrollbar = Scrollbar(anime_list_frame)
anime_list_scrollbar.pack(side=LEFT, fill=Y)

anime_list.config(yscrollcommand=anime_list_scrollbar.set)
anime_list_scrollbar.config(command=anime_list.yview)

anime_list.bind("<Double-Button-1>", anime_list_clicked)

# recommendation list (and scrollbar)
recommendation_list_frame = Frame(middle_frame)
recommendation_list_frame.pack(side=RIGHT, fill=BOTH, expand=True)
recommendation_list = Listbox(recommendation_list_frame)
recommendation_list.pack(side=LEFT, fill=BOTH, expand=True)
recommendation_list_scrollbar = Scrollbar(recommendation_list_frame)
recommendation_list_scrollbar.pack(side=LEFT, fill=Y)

recommendation_list.config(yscrollcommand=recommendation_list_scrollbar.set)
recommendation_list_scrollbar.config(command=recommendation_list.yview)

recommendation_list.bind("<Double-Button-1>", recommendation_list_clicked)

bottom_frame = Frame(gui)
bottom_frame.pack(fill=BOTH, expand=True)

#Info box
info_frame = Frame(bottom_frame)
info_frame.pack(side=TOP, fill=BOTH, expand=True)
info_box = Text(info_frame, wrap="word")
info_box.pack(side=LEFT, fill=BOTH, expand=True)
info_box_scrollbar = Scrollbar(info_frame)
info_box_scrollbar.pack(side=LEFT, fill=Y)

info_box.config(yscrollcommand=info_box_scrollbar.set, state="disabled")
info_box_scrollbar.config(command=info_box.yview)

#Allow print messages to be shown in the gui
def printToInfoBox(func):
    def inner(input):
        try:
            info_box.config(state="normal")
            info_box.insert(END, input)
            info_box.config(state="disabled")
            info_box.yview_moveto(1.0)
            return func(input)
        except:
            return func(input)
    return inner

sys.stdout.write=printToInfoBox(sys.stdout.write)

# Load anime data needed for GUI
anime_info = csv_util.readCSVFile(f"{DATA_PATH}/anime.csv")
my_animes = csv_util.readCSVFile(f"{DATA_PATH}/my_anime.csv")

# Fill Anime List
filterAnimes(None)

# Run GUI
gui.mainloop()