import pandas as pd
import numpy as np
import os

'''
NOTE: The aplication will look for matching strings to iterate AFTER the first aplication window.

'''

def load_data(filepath, sep=None):

    '''
    Loads CSV data with optional parameters.
       
    Args:
        filepath (str): Path to the dataset.
        sep (str, optional): Column separator.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
        pd.errors.ParserError: If parsing fails.
    
    '''
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found {filepath}")
     
    try:
        if sep is not None:
            return pd.read_csv(filepath, sep = sep)
        return pd.read_csv(filepath)
    except Exception as e:
        raise RecursionError(f"Failed to load data. {filepath}")
        

def anime_processor(df):

    """
    Processes DataFrame and creates new columns. 

    Args:
        df = pd.DataFrame()

    Returns:
        data = pd.DataFrame()
    """
    
    data = df.copy()
    
    # matching iterable.
    data.rename({"score_10_count": "score_010_count"}, axis = 1, inplace = True)

    scores = np.flip(np.arange(2, 11))

    high = []
    medium = []
    low = []

    for i in scores:
        if i >= 8: 
            high.append(f"score_0{i}_count")
        if 4 < i < 8 :
            medium.append(f"score_0{i}_count")
        if 1 < i < 5: 
            low.append(f"score_0{i}_count")

    # value assignment.
    data['scores_good'] = data.loc[:,high].sum(axis=1)
    data["scores_medium"] = data.loc[:,medium].sum(axis=1)
    data["scores_low"] = data.loc[:,low].sum(axis=1)

    # columns creation.
    data["ratio_rank"] = (data["scores_low"] / data["scores_medium"]  / data["scores_good"]).rank()
    data.fillna({"ratio_rank": 0}, inplace = True)
    data["ratio_rank"] = data["ratio_rank"].astype(int)


    data["start_date"] = pd.to_datetime(data["start_date"]).dt.year
    data.rename(columns={'start_date': 'year'}, inplace = True)
    data.fillna({'year': 0}, inplace = True)

    # Avoiding convergence before filling NaN's.
    data["year"] = data["year"].astype(int)

    data = data[['title','studios', 'genres', 'ratio_rank', 'completed_count', 'year', 'anime_id']]
    
    data.columns = data.columns.str.capitalize()
    
    return data

def recomendation_processor(df):
    """
    Processes DataFrame. 

    Args:
        df = pd.DataFrame()

    Returns:
        data = pd.DataFrame()
    """
    
    data = df.copy()
    
    data = data[["animeA", "animeB", "num_recommenders"]]

    data.fillna({'num_recommenders': 0}, inplace = True)

    data.columns = data.columns.str.capitalize()

    return data

def exporter(df, name):
    """
    Exports CSV file to folder. 

    Args:
        df = pd.DataFrame()
        name = name to export.
    Return:
        NONE

    """
    data = df.copy()
    data.to_csv(name)

def main():
    anime_info = load_data("anime_info.csv", "\t")
    anime_rec = load_data("user_recomendations.csv", "\t")
    anime_info_processed = anime_processor(anime_info)
    anime_rec_processed = recomendation_processor(anime_rec)
    exporter(anime_info_processed, "anime_info_processed.csv")
    exporter(anime_rec_processed, "anime_rec_processed.csv")

if __name__ == "__main__":
    main()

