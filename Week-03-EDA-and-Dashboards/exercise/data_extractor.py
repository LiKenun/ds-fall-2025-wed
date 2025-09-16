import pandas as pd
import sys

def load_data(file_path: str) -> pd.DataFrame:
    try:
        print(f"Loading dataset from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"✅ Dataset loaded successfully!")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found!")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"❌ Error: File '{file_path}' is empty!")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading dataset: {str(e)}")
        sys.exit(1)
        
    return df

def display_dataframe_info(df: pd.DataFrame):
    print("\nDataFrame Info:")
    print(df.info())
    print("\nFirst 5 Rows:")
    print(df.head())
    print("\nSummary Statistics:")
    print(df.describe())
    print("\nMissing Values:")
    print(df.isnull().sum())

def remove_missing_values_and_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    initial_shape = df.shape
    df_cleaned = df.dropna().drop_duplicates()
    final_shape = df_cleaned.shape
    print(f"\nRemoved {initial_shape[0] - final_shape[0]} rows with missing values or duplicates.")
    return df_cleaned

def analyze_genres_breakdown(df: pd.DataFrame, min_threshold: int = 100):  
    # What's the breakdown of genres for the movies that were rated?  
    if 'genres' not in df.columns:
        print("❌ Error: 'genres' column not found in DataFrame.")
        return
    movies_with_genres = df[["movie_id", "title", "genres"]].drop_duplicates()
    print(f"\nTotal unique movies: {movies_with_genres['movie_id'].nunique()}")
    genres_series = movies_with_genres['genres'].str.split('|').explode()
    genre_counts = genres_series.value_counts()

    genres_below_threshold = genre_counts[genre_counts < min_threshold]
    genres_above_threshold = genre_counts[genre_counts >= min_threshold]

    final_breakdown = genres_above_threshold.copy()
    if len(genres_below_threshold) > 0:
        other_count = genres_below_threshold.sum()
        final_breakdown['Other'] = other_count
    
    # Sort by count descending
    final_breakdown = final_breakdown.sort_values(ascending=False)
    
    for genre, count in final_breakdown.items():
        percentage = (count / movies_with_genres['movie_id'].nunique()) * 100
        print(f"{genre:<20}: {count:>4} movies ({percentage:>5.1f}%)")
    
    return final_breakdown

def analyze_genres_highest_viewer_satisfaction_ratings(df: pd.DataFrame):
    # Which genres have the highest viewer satisfaction (highest ratings)? 

    # get viewer satisfaction ratings by genre and sort descending by mean rating
    if 'genres' not in df.columns or 'rating' not in df.columns:
        print("❌ Error: 'genres' or 'rating' column not found in DataFrame.")
        return

    genre_satisfaction = df[df['genres'].notna()].explode('genres').groupby('genres')['rating'].agg(['mean', 'count']).round(3)
    genre_satisfaction = genre_satisfaction.sort_values(by='mean', ascending=False)
    print("\nGenre Viewer Satisfaction Ratings:")
    return genre_satisfaction

def analyze_rating_by_year(df: pd.DataFrame):
    yearly_stats = df.groupby("year").agg({
        'rating': ['mean'],
        'movie_id': pd.Series.nunique
    }).round(3)

    yearly_stats.columns = ['avg_rating', "num_unique_movies"]

    print("\nYearly Rating Statistics:")
    print(yearly_stats)

    return yearly_stats


def find_best_rated_movies(df: pd.DataFrame, top_n: int = 10):
    if 'rating' not in df.columns or 'title' not in df.columns:
        print("❌ Error: 'rating' or 'title' column not found in DataFrame.")
        return
    
    top_movies = df.groupby('title')['rating'].mean().sort_values(ascending=False).head(top_n)

    return top_movies