from tkinter import *
import csv_util

animes = csv_util.fetchCSVColumnValues("data/anime.csv", "Name")

def getRecommendations(event):
    # replace this code with call to recommendation engine
    recommendation_list.insert(END, anime_searchbox.get())

def listAnimes(animes):
    anime_list.delete(0, END)

    for anime in animes:
        anime_list.insert(END, anime)

def filterAnimes(event):
    filtered_anime_list = []
    
    filter_by = anime_searchbox.get()

    if filter_by == "":
        filtered_anime_list = animes
    else:
        for anime in animes:
            if filter_by.lower() in anime.lower():
                filtered_anime_list.append(anime)

    listAnimes(filtered_anime_list)

def populateSearchBox(event):
    anime_searchbox.delete(0, END)
    anime_searchbox.insert(0, anime_list.get(anime_list.curselection()))

gui = Tk()
gui.title("Anime Recommender")
gui.geometry("500x300")

# searchbox (and label)
anime_searchbox_frame = Frame(gui)
anime_searchbox_frame.pack()
anime_searchbox_label = Label(anime_searchbox_frame, text="Search for Anime Recommendations")
anime_searchbox_label.pack()
anime_searchbox = Entry(anime_searchbox_frame)
anime_searchbox.pack(fill="x")
anime_searchbox.bind("<KeyRelease>", filterAnimes)
anime_searchbox_button = Button(anime_searchbox_frame, text="Get Recommendations")
anime_searchbox_button.pack()
anime_searchbox_button.bind("<Button-1>", getRecommendations)


# anime list (and scrollbar)
anime_list_frame = Frame(gui)
anime_list_frame.pack(side=LEFT, fill=BOTH, expand=True)
anime_list = Listbox(anime_list_frame)
anime_list.pack(side=LEFT, fill=BOTH, expand=True)
anime_list_scrollbar = Scrollbar(anime_list_frame)
anime_list_scrollbar.pack(side=LEFT, fill=Y)

anime_list.config(yscrollcommand=anime_list_scrollbar.set)
anime_list_scrollbar.config(command=anime_list.yview)

anime_list.bind("<Double-Button-1>", populateSearchBox)

# recommendation list (and scrollbar)
recommendation_list_frame = Frame(gui)
recommendation_list_frame.pack(side=RIGHT, fill=BOTH, expand=True)
recommendation_list = Listbox(recommendation_list_frame)
recommendation_list.pack(side=LEFT, fill=BOTH, expand=True)
recommendation_list_scrollbar = Scrollbar(recommendation_list_frame)
recommendation_list_scrollbar.pack(side=LEFT, fill=Y)

recommendation_list.config(yscrollcommand=recommendation_list_scrollbar.set)
recommendation_list_scrollbar.config(command=recommendation_list.yview)

listAnimes(animes)

# Run GUI
gui.mainloop()