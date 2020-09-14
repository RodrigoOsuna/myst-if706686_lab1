
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: visualizations.py : python script with data visualization functions                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import numpy as np
import time
import pandas as pd
import yfinance as yf
from os import listdir, path
from os.path import isfile, join
from datetime import datetime
from datetime import timedelta


def pasiva(inv_pasiva):

    # defnimos el dataframe en donde se ira guardando
    df_pasiva = pd.DataFrame({"Dates": inv_pasiva['Dates'], "Capital": inv_pasiva['Capital'], "Rend": 0, "Rend Acum": 0})

    # Calculo de rendimientos
    for i in range(1, len(df_pasiva)):
        # rend precio_actual-precio anterior/ precio actual
        df_pasiva.loc[i, "Rend"] = (df_pasiva.loc[i, 'Capital'] - df_pasiva.loc[i - 1, 'Capital']) / df_pasiva.loc[
            i - 1, 'Capital']
        # rendimientos acumuladopues
        df_pasiva.loc[i, "Rend Acum"] = df_pasiva.loc[i, 'Rend'] + df_pasiva.loc[i - 1, 'Rend Acum']
    return df_pasiva

