import csv_util

import numpy
import pandas
import tensorflow

def loadModel(model_path):
    model = tensorflow.keras.models.load_model(model_path)
    return model

def cleanupModel(model):
    if not model is None:
        tensorflow.keras.backend.clear_session()
        model = None

    return model
    

def extractModelWeights(name, model):
    weight_layer = model.get_layer(name)
    weights = weight_layer.get_weights()[0]
    weights = weights / numpy.linalg.norm(weights, axis = 1).reshape((-1, 1))
    return weights

def getClosestItems(item_id, item_count, weights):
    dists = numpy.dot(weights, weights[item_id])
    sorted_dists = numpy.argsort(dists)
    
    n = item_count + 1            
    closest = sorted_dists[-n:]
    return closest

def getFrame(data_frame, column, value):
        frame = data_frame[data_frame[column] == value]
        return frame

def getSimilarAnimeByName(anime_name):
    model = None
    try:
        model = loadModel("model")
        anime_weights = extractModelWeights("anime_embed", model)

        anime_df = pandas.read_csv("data/anime.csv", low_memory=True)
        anime_df = anime_df[["MAL_ID", "Name", "Genres"]]

        animeData = getFrame(anime_df, "Name", anime_name)
        anime_id = animeData["MAL_ID"].values[0]

        fetched_anime_list = csv_util.fetchCSVColumnValues("data/unique_anime_ids.csv", "anime_id")
        fetched_anime_id_index_map = {int(x): i for i, x in enumerate(fetched_anime_list)} # map user_id values to index of user_id
        fetched_anime_id_value_map = {i: int(x) for i, x in enumerate(fetched_anime_list)} # map index of user_id to user_id values

        anime_index_id = fetched_anime_id_index_map.get(anime_id)

        similar_anime_ids = getClosestItems(anime_index_id, 10, anime_weights)

        similar_animes = []

        for id in similar_anime_ids:
            anime_id = fetched_anime_id_value_map.get(id)
            anime_frame = getFrame(anime_df, "MAL_ID", anime_id)

            anime_name = anime_frame["Name"].values[0]
            genre = anime_frame["Genres"].values[0]

            similar_animes.append({"anime_id": anime_id, "anime_name": anime_name, "genre": genre})

        model = cleanupModel(model)
        return similar_animes

    except:
        print(f"{anime_name}!, Not Found in sampled Anime list")
        model = cleanupModel(model)