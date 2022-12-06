import pandas as pd
import json
import os

df = pd.read_csv("music.csv")

mood_list = ["Chill", "Party", "Romance", "Focus"]
bpm_range = {
    "Slow": (0, 120),
    "Fast": (120, 240), 
}

os.makedirs("features/csv_features", exist_ok=True)

for mood in mood_list:
    for bpm_mode in bpm_range.keys():
        songs = df[(df["mood"] == mood) & (df["bpm"] >= bpm_range[bpm_mode][0]) & (df["bpm"] <= bpm_range[bpm_mode][1])]
        new_df = []
        for song in songs.itertuples():
            with open(song[3], "r") as f:
                data = json.load(f)
                new_df.append([song[1],*data])
        new_df = pd.DataFrame(new_df, columns=["music_name", *["feature_"+str(i) for i in range(1280)]])
        new_df.to_csv(f"features/csv_features/{mood}-{bpm_mode}.csv", index=False)