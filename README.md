# Project Brief: Spreadsheet Analysis

In this project you'll use Python to do very basic data analysis on a spreadsheet. The standard

project will use csv file that contains fake sales data. After completing the required tasks you are

free to change the csv file that you use.

## Required Tasks

These are the required tasks for this project. You should aim to complete these tasks before

adding your own ideas to the project.

1. Read the data from the spreadsheet

2. Collect all of the sales from each month into a single list

3. Output the total sales across all months


Please find my basic data analysis project [here](https://github.com/emmabehr/Python-mini-projects/tree/main/Day%2017%20-%20read%20csv%20file)

## Extended Tasks

For my extension project, I built anime recommendation engine using machine learning.

Dataset taken from: [MyAnimeList Database 2020] (https://www.kaggle.com/hernan4444/anime-recommendation-database-2020)

I use these csv files from the dataset and they should be placed in a folder called _data_ in the _src_ folder
- anime.csv
- animelist.csv

The user interface is written using Tkinter and allows the user to view and filter a list of anime, read from the CSV file, anime.csv. The user can choose a show and get recommendations for other anime they might like.

The recommendations come from training a neural network using anime ratings from the CSV file _animelist.csv_, the model is trained by taking rating information from users and the shows that they have rated. This allows the model to compare similar animes based on user ratings and other shows that they have given similar ratings to.

There are over 109 million rows in the _animelist.csv_ file (using all the data to train the Recommendation Engine would take over 400 hours on my local machine so the model on my local machine used only about 500,000 rows of data for training - if you want to you can improve accuracy over my model by using a larger amount of rows for the training - you can set this by adjusting the value of **DEFAULT_SAMPLE_FRACTION** in the _recommendation_engine_constants.py_ file - This selects the fraction of the data to use for training)
