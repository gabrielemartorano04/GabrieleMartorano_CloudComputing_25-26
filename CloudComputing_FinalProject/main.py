from src.ingestion import load_dataset
from src.preprocessing import preprocess_data
from src.window_segmentation import create_windows
from src.scenario_detection import classify_window
from src.output import save_results
from src.visualization import generate_scenario_gif

import pandas as pd


def main():

    dataset_path = "data/trajectories-0820am-0835am.csv"

    print("Loading dataset...")
    df = load_dataset(dataset_path)

    print("Preprocessing data...")
    df = preprocess_data(df)

    print("Creating sliding windows...")
    windows = create_windows(df)

    results = []

    print("Running scenario detection...")

    for window in windows:

        label = classify_window(window)

        result = {
            "start_frame": window["Frame_ID"].min(),
            "end_frame": window["Frame_ID"].max(),
            "num_vehicles": window["Vehicle_ID"].nunique(),
            "scenario": label
        }

        if len(results) % 1000 == 0 and len(results) > 0:
            print("Processed", len(results), "windows")

        results.append(result)

    print("Saving results...")
    save_results(results, "scenario_output.csv")

    print("Generating visualizations...")

    scenarios = pd.DataFrame(results)

    # scenarios we want to visualize
    target_scenarios = ["Car Following", "Lane Change", "Cut-In"]

    for scenario_type in target_scenarios:

        scenario_rows = scenarios[scenarios["scenario"] == scenario_type]

        if scenario_rows.empty:
            print("No scenario found for:", scenario_type)
            continue

        row = scenario_rows.iloc[0]

        start_frame = row["start_frame"]
        end_frame = row["end_frame"]

        output_file = f"{scenario_type.replace(' ', '_')}.gif"

        generate_scenario_gif(df, start_frame, end_frame, scenario_type, output_file)

        print("Generated:", output_file)


if __name__ == "__main__":
    main()