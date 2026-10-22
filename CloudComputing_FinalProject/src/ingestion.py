import pandas as pd

def load_dataset(file_path):
    """
    1. Python reads the raw NGSIM trajectory dataset
    2. Data is converted into a pandas dataframe
    3. A subset of that data using a range of [50,550] meters for the "Local_Y" column in the data is used (total 500 m segement as specified in our proposal)
    4. This becomes the in-memory database as described in our proposal
    """

    #The entire CSV data from NGSIM for US-101 Los Angeles, from 8:20 AM to 8:35 AM
    df = pd.read_csv("data/trajectories-0820am-0835am.csv")
    #The specific 500m
    segment_df = df[(df["Local_Y"] >= 50) & (df["Local_Y"] <= 550)]

    print("Dataset loaded")
    print("Rows:", len(segment_df))

    return segment_df