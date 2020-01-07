# preparation
import pandas as pd

emg_dataframe = (
    pd.read_csv("../../data/emgs.csv")
    .query('filename == "12kg_H2_3"')["delt_ant"]
    .values
)

# solution
above_average = emg_dataframe[emg_dataframe > emg_dataframe.mean()]
mu = above_average.mean()
sigma = above_average.std()
(above_average > mu + sigma).sum() + (above_average < mu - sigma).sum()
