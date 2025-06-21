import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

# Example usage:
# df = load_data('data/pricing_data.csv')
