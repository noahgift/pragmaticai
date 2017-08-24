"""
Listing 7.3
"""
import pandas as pd

nba = pd.read_csv("data/nba_2017_br.csv")
nba.describe()
