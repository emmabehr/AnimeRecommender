# AnimeRecommender
Anime recommendation engine using machine learning.  Final project for my CFG class. 

dataset taken from: [MyAnimeList Database 2020] (https://www.kaggle.com/hernan4444/anime-recommendation-database-2020) - This should be extracted and the csv files put in a folder called _data_ in the _src_ folder

over 109 million rows in the animelist.csv dataset (using this whole dataset to train the Recomendation Engine would take over 400 hours on my local machine so the model on my local machine used only about 500,000 rows of data for training - if you have the resources/time you could improve accuracy over my model by using a larger amount of rows for the training - you can set this by adjusting the value of DEFAULT_SAMPLE_FRACTION in the recommendation_engine_constants.py file - This selects the fraction of the data to use for training)