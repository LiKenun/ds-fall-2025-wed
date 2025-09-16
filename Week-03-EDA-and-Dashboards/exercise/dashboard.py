from data_extractor import load_data, remove_missing_values_and_duplicates, analyze_genres_breakdown, find_best_rated_movies, analyze_genres_highest_viewer_satisfaction_ratings, analyze_rating_by_year
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="MovieLens Dashboard",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_cached_data():
    """Load and cache the data"""
    return load_data("../data/movie_ratings.csv")

def main():
    st.title("🎬 Movie Ratings Analysis Dashboard")
    st.markdown("### Analyzing movie ratings from the MovieLens dataset")
    
    # Load data
    df = load_cached_data()
    df = remove_missing_values_and_duplicates(df)
    
    # Sidebar controls
    st.sidebar.header("Analysis Parameters")
    min_threshold = st.sidebar.slider("Minimum Sample Threshold", 10, 200, 50)
    min_movie_ratings = st.sidebar.selectbox("Min Ratings for Best Movies", [50, 100, 150], index=0)
    
    # Dataset overview
    with st.expander("📊 Dataset Overview"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Ratings", f"{len(df):,}")
        with col2:
            st.metric("Unique Users", f"{df['user_id'].nunique():,}")
        with col3:
            st.metric("Unique Movies", f"{df['movie_id'].nunique():,}")
        with col4:
            st.metric("Rating Range", f"{df['rating'].min()} - {df['rating'].max()}")
        
        st.dataframe(df.head(), use_container_width=True)
    
    # Question 1: Genre Breakdown
    st.header("1️⃣ Genre Breakdown")
    genre_breakdown = analyze_genres_breakdown(df, min_threshold)
    
    if genre_breakdown is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_bar = px.bar(
                x=genre_breakdown.values,
                y=genre_breakdown.index,
                orientation='h',
                title=f"Movies by Genre (min {min_threshold} movies)",
                labels={'x': 'Number of Movies', 'y': 'Genre'}
            )
            fig_bar.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(
                values=genre_breakdown.values,
                names=genre_breakdown.index,
                title="Genre Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Question 2: Genre Satisfaction
    st.header("2️⃣ Genre Satisfaction (Highest Ratings)")
    genre_satisfaction = analyze_genres_highest_viewer_satisfaction_ratings(df)
    
    if genre_satisfaction is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            top_genres = genre_satisfaction.head(15)
            fig_satisfaction = px.bar(
                x=top_genres.index,
                y=top_genres['mean'],
                title=f"Top 15 Genres by Average Rating (min {min_threshold} ratings)",
                labels={'x': 'Genre', 'y': 'Average Rating'}
            )
            fig_satisfaction.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_satisfaction, use_container_width=True)
        
        with col2:
            st.subheader("Genre Statistics")
            st.dataframe(genre_satisfaction, use_container_width=True)
    
    # Question 3: Rating by Year
    st.header("3️⃣ Rating Trends by Movie Release Year")
    yearly_stats = analyze_rating_by_year(df)
    
    if yearly_stats is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_line = px.line(
                x=yearly_stats.index,
                y=yearly_stats['avg_rating'],
                title="Average Rating by Release Year",
                labels={'x': 'Release Year', 'y': 'Average Rating'}
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            fig_bar_year = px.bar(
                x=yearly_stats.index,
                y=yearly_stats['num_unique_movies'],
                title="Number of Movies by Release Year",
                labels={'x': 'Release Year', 'y': 'Number of Movies'}
            )
            st.plotly_chart(fig_bar_year, use_container_width=True)
    
    # Question 4: Best Rated Movies
    st.header("4️⃣ Best Rated Movies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top 5 Movies (≥{min_movie_ratings} ratings)")
        best_movies = find_best_rated_movies(df, top_n=5)
        if best_movies is not None:
            st.dataframe(best_movies, use_container_width=True)
    
    with col2:
        st.subheader("Top 5 Movies (≥150 ratings)")
        best_movies_150 = find_best_rated_movies(df, top_n=150)
        if best_movies_150 is not None:
            st.dataframe(best_movies_150, use_container_width=True)

if __name__ == "__main__":
    main()