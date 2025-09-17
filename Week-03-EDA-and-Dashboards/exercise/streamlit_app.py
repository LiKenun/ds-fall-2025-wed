import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

print("To run this Streamlit app, use the following command:")
print(r"streamlit run Week-03-EDA-and-Dashboards/exercise/homework-jack-kaplan-week-03.py")

st.set_page_config(
    page_title="Movie Ratings Analysis",
    page_icon="X",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

data_path = "Week-03-EDA-and-Dashboards/data/movie_ratings.csv"
df = pd.read_csv(data_path)

# Remove year from movie title with format "Movie Title (Year)"
df['year'] = df['title'].str.extract(r'\((\d{4})\)').astype(float)
df['title'] = df['title'].str.replace(r'\s*\(\d{4}\)$', '', regex=True)

# Fixing movie titles to avoid "Jungle Book, The" type issues
df['title'] = df['title'].str.replace(r', The$', '', regex=True)
df['title'] = df['title'].str.replace(r', A$', '', regex=True)
df['title'] = df['title'].str.replace(r', An$', '', regex=True)

# Drop ratings where movie title or genre is 'unknown'
df = df[df['title'].str.lower() != 'unknown']
df = df[df['genres'].str.lower() != 'unknown']


# Goals:
# Breakdown of genre for rates movies
# Genres with highest ratings
# Mean rating over time over years
# 5 best rated movies with n many ratings

# Goal 1: Breakdown of genre for rated movies
st.subheader("Genre Distribution")
genre_counts = df['genres'].value_counts().head(20)
fig_genre = px.bar(x=genre_counts.index, y=genre_counts.values, orientation='v',
                   title="Top 20 Genres by Number of Ratings")
fig_genre.update_layout(xaxis_title="Genre", yaxis_title="Number of Ratings")
st.plotly_chart(fig_genre)

# Goal 2: Genres with highest ratings
st.subheader("Highest Rated Genres")
genre_ratings = df.groupby('genres')['rating'].agg(['mean', 'count']).reset_index()
min_genre_ratings = st.number_input("Minimum number of ratings per genre", min_value=1, max_value=1000, value=100, step=1)
genre_ratings = genre_ratings[genre_ratings['count'] >= min_genre_ratings]
genre_ratings_sorted = genre_ratings.sort_values('mean', ascending=False).head(10)

fig_ratings = px.bar(genre_ratings_sorted, x='genres', y='mean', orientation='v',
                     title=f"Top 10 Genres by Average Rating (Min. {min_genre_ratings} ratings)")
fig_ratings.update_layout(
    xaxis_title="Genre",
    yaxis_title="Average Rating",
    yaxis=dict(range=[0, 5])
)
st.plotly_chart(fig_ratings)

# Goal 3: Mean rating over time over years
st.subheader("Average Rating Trends Over Time")
yearly_ratings = df.groupby('year')['rating'].mean().reset_index()
yearly_ratings = yearly_ratings.dropna()

fig_time = px.line(yearly_ratings, x='year', y='rating',
                   title="Average Movie Rating by Year")
fig_time.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Rating",
    yaxis=dict(range=[0, 5])
)
st.plotly_chart(fig_time)

# Goal 4: 5 best rated movies with n many ratings
st.subheader("Top 5 Best Rated Movies")
min_ratings = st.number_input("Minimum number of ratings", min_value=1, max_value=10000, value=50, step=1)

# Group by both title and year to keep year info
movie_stats = df.groupby(['title', 'year'])['rating'].agg(['mean', 'count']).reset_index()
movie_stats = movie_stats[movie_stats['count'] >= min_ratings]
top_movies = movie_stats.sort_values('mean', ascending=False).head(5)

# Combine title and year for display
top_movies['title_year'] = top_movies['title'] + " (" + top_movies['year'].astype(int).astype(str) + ")"

fig_top = px.bar(top_movies, x='title_year', y='mean', orientation='v',
                 title=f"Top 5 Movies by Average Rating (Min. {min_ratings} ratings)")
fig_top.update_layout(
    xaxis_title="Movie Title",
    yaxis_title="Average Rating",
    yaxis=dict(range=[0, 5])
)
st.plotly_chart(fig_top)

# Display the data table
st.write("Movie Details:")
top_movies_display = top_movies[['title', 'year', 'mean', 'count']].round(2)
top_movies_display.columns = ['Title', 'Year', 'Average Rating', 'Number of Ratings']
st.dataframe(top_movies_display)