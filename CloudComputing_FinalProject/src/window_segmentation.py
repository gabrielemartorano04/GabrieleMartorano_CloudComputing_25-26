def create_windows(df, window_size=50):

    """
    Create 5-second sliding windows based on frames.

    Instead of grouping by vehicle, we group by time frames
    so that each window contains ALL vehicles present during
    that 5-second period. This allows cut-in detection which was not possible before.
    """
    windows = []

    frames = sorted(df["Frame_ID"].unique())

    for i in range(len(frames) - window_size):

        start = frames[i]
        end = frames[i + window_size]

        window = df[
            (df["Frame_ID"] >= start) &
            (df["Frame_ID"] <= end)
        ]

        windows.append(window)

    return windows