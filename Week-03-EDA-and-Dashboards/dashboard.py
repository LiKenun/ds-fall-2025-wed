#!/usr/bin/env python
# coding: utf-8

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
df = pd.read_csv('data/movie_ratings.csv')


print(df.info())
print(df.describe())
print(df.head())



df.isnull().sum()



df = df.dropna()
print(len(df))


st.set_page_config(
    page_title="Movie Ratings Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded")

with st.sidebar:
    st.title('🎬 Movie Ratings Dashboard')
    
    year_list = list(df['year'].unique())
    year_list = sorted([int(num) for num in year_list], reverse = True)

    selected_year = st.selectbox('Select a year', year_list, index=0)
    df_selected_year = df[df['year'] == selected_year]
    #df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    #selected_color_theme = st.selectbox('Select a color theme', color_theme_list)

def make_bar_chart(df, y, xlab, ylab, title, color = None):
    fig, ax = plt.subplots()
    ax.bar(df.index, df[y])
    ax.set_xlabel(xlab)
    ax.tick_params(axis='x', rotation=90)
    ax.set_ylabel(ylab)
    ax.set_title(title)
    #fig.set_facecolor(color)
    st.pyplot(fig)
# 1. What's the breakdown of genres for the movies that were rated?
# Bar chart: X-axis: Genres; Y-axis: Number of movies
one_df = df.groupby('genres').count()
one_df = one_df.drop('unknown')
one_df = one_df.sort_values(by='rating')


# 2. Which genres have the highest viewer satisfaction (highest ratings)? 
# Group genres in df by mean ratings, then graph
# Bar chart: x-axis: genre, y-axis: mean rating
two_df = df.groupby('genres')['rating'].mean()
two_df = two_df.to_frame()
two_df = two_df.drop('unknown')

# 3. How does mean rating change across movie release years?
# Create widget for genres to select and then specific line for each genre


def make_line_chart(df, x, y, xlab, ylab, color = None):
    st.line_chart(df, x = x, y = y, x_label = xlab, y_label = ylab, color = color)

# 4. What are the 5 best-rated movies that have at least 50 ratings? At least 150 ratings?
# A) Bar chart with x-axis as movie_name and y-axis as rating
# B) Selective Bar chart with widget to select year


col = st.columns(2, gap='medium')

with col[0]:
    make_bar_chart(one_df, 'rating', xlab = 'Genres', ylab = 'Number of movies', title = 'Number of movies per genre', color = 'lightgreen')


with col[1]:
    make_bar_chart(two_df, 'rating', xlab = 'Genres', ylab = 'Ratings', title = 'Higest rated genres')
    pass

col = st.columns(2, gap='medium')

with col[0]:
    pass

with col[1]:
    pass

