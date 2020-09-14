
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
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


def funcfechas(archivos):

    i_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]
    return i_fechas

# ----------------------------------------------------------------------------------------------------------------

def functickers(archivos,data_archivos):

    tickers = []
    for i in archivos:
        l_tickers = list(data_archivos[i]['Ticker'])
        [tickers.append(i + '.MX') for i in l_tickers]
    global_tickers = np.unique(tickers).tolist()

    global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
    global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
    global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

    [global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'KOFUBL.MX', 'BSMXB.MX']]

    return global_tickers

# ---------------------------------------------------------------------------------------------

def funcdesdatos(global_tickers):


    inicio = time.time()

    data = yf.download(global_tickers, start="2018-01-30", end="2020-08-22", actions=False,
                       group_by="close", interval='1d', auto_adjust=False, prepost=False, threads=True)

    print('se tardo', round(time.time() - inicio, 2), 'segundos')
    return data

# ----------------------------------------------------------------------------------------------------------------

def funccierres(data,global_tickers):


    data_close = pd.DataFrame({i: data[i]['Close'] for i in global_tickers})
    return data_close




def funcfechacierre(data_close,i_fechas):

    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(i_fechas)))

    return ic_fechas


def funcprecio(data_close , ic_fechas):

    precios = data_close.iloc[[int(np.where(data_close.index.astype(str) == i)[0]) for i in ic_fechas]]

    precios = precios.reindex(sorted(precios.columns), axis=1)
    return precios


def funcdatosposi(eliminar,data_archivos,archivos,precios,k,c):


    pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]
    i_activos = list(pos_datos[pos_datos['Ticker'].isin(eliminar)].index)
    pos_datos.drop(i_activos, inplace=True)

    pos_datos.reset_index(inplace=True, drop=True)
    pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')


    pos_datos['Precios'] = (np.array([precios.iloc[0, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]))
    capital=pos_datos['Peso (%)'] * k
    pos_datos['Capital'] = capital - capital * c

    pos_datos['Titulos'] = pos_datos['Capital'] // pos_datos['Precios']

    pos_datos['Postura'] = pos_datos['Precios'] * pos_datos['Titulos']

    pos_datos['Comisiones'] = np.round(pos_datos['Precios'] * c * pos_datos['Titulos'], 2)

    return pos_datos


def funcpasiva(ic_fechas,pos_datos,precios,Cash,inv_pasiva):


    for i in range(len(ic_fechas)):
        pos_datos['Precios'] = (
            np.array([precios.iloc[i, precios.columns.to_list().index(j)] for j in pos_datos['Ticker']]))
        pos_datos['Comision'] = 0
        pos_datos['Postura'] = pos_datos['Precios'] * pos_datos['Titulos']
        inv_pasiva['Capital'].append(pos_datos['Postura'].sum() + Cash)
        inv_pasiva['Dates'].append(ic_fechas[i])
    return inv_pasiva
