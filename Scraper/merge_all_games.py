import pandas as pd
import os

season_string = '20142015'
game_path = './../data/filtered/%s/' % season_string
merged = pd.concat([pd.read_csv(os.path.join(game_path, f)) for f in os.listdir(game_path)]).fillna(0)

merged.to_csv('./../data/full_table%s.csv' % (season_string))