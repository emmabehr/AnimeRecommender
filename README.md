t anime recommendation engine using machine learning.

Dataset taken from: [MyAnimeList Database 2020] (https://www.kaggle.com/hernan4444/anime-recommendation-database-2020)

I use these csv files from the dataset and they should be placed in a folder called _data_ in the _src_ folder
- anime.csv
- animelist.csv

The user interface is written using Tkinter and allows the user to view and filter a list of anime, read from the CSV file, anime.csv. The user can choose a show and get recommendations for other anime they might like.
The recommendations come from training a neural network using anime ratings from the CSV file _animelist.csv_, the model is trained by taking rating information from users and the shows that they have rated. This allows the model to compare similar animes based on user ratings and other shows that they have given similar ratings to.
There are over 109 million rows in the _animelist.csv_ file (using all the data to train the Recommendation Engine would take over 400 hours on my local machine so the model on my local machine used only about 500,000 rows of data for training - if you want to you can improve accuracy over my model by using a larger amount of rows for the training - you can set this by adjusting the value of **DEFAULT_SAMPLE_FRACTION** in the _recommendation_engine_constants.py_ file - This selects the fraction of the data to use for training

## Autocomplete 
![gif showing the autocomplete in action](https://github.com/emmabehr/AnimeRecommender/blob/main/readmeimg/autocomplete.gif)

## Rating the Anime 
![gif showing how I rate the anime](https://github.com/emmabehr/AnimeRecommender/blob/main/readmeimg/rating.gif)

## Getting the recommendations
![gif showing the recommendations section populating](https://github.com/emmabehr/AnimeRecommender/blob/main/readmeimg/recommendations.gif)


