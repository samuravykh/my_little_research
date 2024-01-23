import yaml
import pandahouse as ph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import rcParams
import plotly.express as px
import seaborn as sns

sns.set(
    font_scale=2, 
    style     ="whitegrid", 
    rc        = {'figure.figsize': (20, 7)}
)

with open("creds.yml", "r") as file:
    personal_creds = yaml.load(file, Loader=yaml.FullLoader)
    
#объявляем параметры подключения
connection = dict(database='default',
                  host='https://clickhouse.lab.karpov.courses',
                  user=personal_creds['user_value'],
                  password=personal_creds['some_value']
                 )

