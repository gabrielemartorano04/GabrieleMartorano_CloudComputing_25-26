def preprocess_data(df):
    """
    1. Sort records by Vehicle_ID and timestamp
    2. Remove missing values
    3. Reset indexing

    Sorting is required so vehicle trajectories are chronological.
    """

    # Sort by vehicle and time
    df = df.sort_values(by=["Vehicle_ID", "Frame_ID"])

    # Drop rows with missing values
    df = df.dropna()

    # Reset index
    df = df.reset_index(drop=True)

    print("Preprocessing complete")

    return df