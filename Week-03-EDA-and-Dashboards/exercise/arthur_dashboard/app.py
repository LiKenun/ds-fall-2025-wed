import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

#Load the data
df = pd.read_csv('../../data/movie_ratings.csv')

#Explore the dataset
print(df.info())
print(df.describe())
print(df.head())

# Sidebar Filters
st.sidebar.header("Filters")
age_range = st.sidebar.slider("Select Age Range", 0, 100, (18, 50))
min_ratings = st.sidebar.selectbox("Minimum Ratings Threshold", [50, 100, 150])
selected_genres = st.sidebar.multiselect("Select Genres", df['genres'].str.split('|').explode().unique())

# Filter Data
filtered_df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])]
if selected_genres:
    filtered_df = filtered_df[filtered_df['genres'].str.contains('|'.join(selected_genres))]

# Question 1: Breakdown of Genres
st.header("Breakdown of Genres")
st.write("This chart shows the distribution of genres for the movies that were rated.")
genre_counts = filtered_df['genres'].str.split('|').explode().value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax, palette='viridis')
ax.set_title("Genre Distribution")
ax.set_xlabel("Ratings Count")
ax.set_ylabel("Genre")
st.pyplot(fig)

# Question 2: Highest Viewer Satisfaction by Genre
st.header("Highest Viewer Satisfaction by Genre")
st.write("This chart shows the average rating for each genre.")
genre_ratings = filtered_df.explode('genres').groupby('genres')['rating'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=genre_ratings.values, y=genre_ratings.index, ax=ax, palette='coolwarm')
ax.set_title("Average Rating by Genre")
ax.set_xlabel("Average Rating")
ax.set_ylabel("Genre")
st.pyplot(fig)

# Question 3: Mean Rating Across Movie Release Years
st.header("Mean Rating Across Movie Release Years")
st.write("This chart shows how the mean rating changes across movie release years.")
yearly_ratings = filtered_df.groupby('year')['rating'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=yearly_ratings, x='year', y='rating', marker='o', ax=ax)
ax.set_title("Mean Rating Over Years")
ax.set_xlabel("Year")
ax.set_ylabel("Mean Rating")
st.pyplot(fig)

# Question 4: Best-Rated Movies
st.header("Best-Rated Movies")
st.write("This table shows the best-rated movies with at least the selected number of ratings.")
movie_ratings = filtered_df.groupby('title').agg({'rating': ['mean', 'count']})
movie_ratings.columns = ['mean_rating', 'rating_count']
movie_ratings = movie_ratings[movie_ratings['rating_count'] >= min_ratings].sort_values(by='mean_rating', ascending=False).head(5)
st.write(movie_ratings)