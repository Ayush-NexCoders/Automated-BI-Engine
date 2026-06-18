import pandas as pd

def load_dataset(file_path):

    try:

        df = pd.read_csv(file_path)

        print(f"[SUCCESS] Loaded {file_path}")

        return df

    except Exception as e:

        print(f"[ERROR] {file_path}")

        print(e)

        return None