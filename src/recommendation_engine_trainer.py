import csv_util
import recommendation_engine_constants as ml

import pandas
import numpy

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, BatchNormalization, Dense, Activation

def getTrainingDataFrame(
    training_file=ml.DEFAULT_TRAINING_FILE, 
    columns_to_read=ml.DEFAULT_COLUMNS_TO_READ, 
    num_rows_to_fetch=ml.DEFAULT_NUM_ROWS_TO_FETCH, 
    low_memory_mode=ml.DEFAULT_LOW_MEMORY_MODE,
    sample_size=ml.DEFAULT_SAMPLE_FRACTION,
    sample_seed=ml.DEFAULT_SAMPLE_RANDOM_STATE):

    if num_rows_to_fetch >= 0:
        training_df = pandas.read_csv(training_file, usecols=columns_to_read, nrows=num_rows_to_fetch, low_memory=low_memory_mode)
    else:
        training_df = pandas.read_csv(training_file, usecols=columns_to_read, low_memory=low_memory_mode)

    if sample_size > 0:
        training_df = training_df.sample(frac=sample_size, replace=True, random_state=sample_seed)
        
    return training_df

def scaleColumn(data_frame, column):
    min_value = min(data_frame[column])
    max_value = max(data_frame[column])

    scale_rating = lambda rating: (rating - min_value) / (max_value - min_value)

    data_frame[column] = data_frame[column].apply(scale_rating).values.astype(numpy.float64)
    return data_frame

def getModel(user_count, anime_count):
    user_input = Input(name="user", shape=[1])
    user_embed = Embedding(user_count, 128, name="user_embed")(user_input)

    anime_input = Input(name="anime", shape=[1])
    anime_embed = Embedding(anime_count, 128, name="anime_embed")(anime_input)

    output = Dot(2, normalize=True)([user_embed, anime_embed])
    output = Flatten()(output)
    output = BatchNormalization()(output)
    output = Dense(1)(output)
    output = Activation("sigmoid")(output)

    model = Model([user_input, anime_input], output)

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=["accuracy"]
    )

    return model
    
def trainModel(
    epoch_count=ml.DEFAULT_EPOCH_COUNT, 
    model_path=ml.MODEL_PATH, 
    data_path=ml.DATA_PATH):

    training_df = getTrainingDataFrame()
    training_df = scaleColumn(training_df, "rating")

    unique_anime_ids = training_df["anime_id"].unique().tolist()
    anime_id_index_map = {x: i for i, x in enumerate(unique_anime_ids)} # map user_id values to index of user_id
    anime_count = len(unique_anime_ids)

    unique_user_ids = training_df["user_id"].unique().tolist()
    user_id_index_map = {x: i for i, x in enumerate(unique_user_ids)} # map user_id values to index of user_id
    user_count = len(unique_user_ids)

    training_df["anime"] = training_df["anime_id"].map(anime_id_index_map)
    training_df["user"] = training_df["user_id"].map(user_id_index_map)

    model = getModel(user_count, anime_count)
    x1 = tf.convert_to_tensor(training_df["user"], dtype=tf.float32, name="user")
    x2 = tf.convert_to_tensor(training_df["anime"], dtype=tf.float32, name="anime")
    y1 = tf.convert_to_tensor(training_df["rating"], dtype=tf.float32, name="rating")
    model.fit([x1,x2], y1, epochs=epoch_count)
    
    model.save(model_path)
    csv_util.saveListToCSVFile(data_path + "/unique_anime_ids.csv", unique_anime_ids, "anime_id")
    csv_util.saveListToCSVFile(data_path + "/unique_user_ids.csv", unique_user_ids, "user_id")