import pandas as pd


def save_results(results, output_path):
    """
    Saves results to output file
    """

    df = pd.DataFrame(results)

    df.to_csv(output_path, index=False)

    print("Results saved to", output_path)