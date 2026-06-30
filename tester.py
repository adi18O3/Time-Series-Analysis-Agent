from utils import (
    load_dataset,
    get_dataset_metadata
)

df = load_dataset("sample_data/sensor_data.csv")

metadata = get_dataset_metadata(df)

print(metadata)