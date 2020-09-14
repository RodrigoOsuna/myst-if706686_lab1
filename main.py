
import data as dt
import visualizations as vis
import functions as fn
import pandas as pd
from os.path import isfile, join
from os import listdir, path

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)



k = 1000000
c = 0.00125
eliminar = ['KOFL', 'KOFUBL', 'BSMXB', 'MXN', 'USD']
abspath = path.abspath('NAFTRAC_holdings/')

archivos = dt.ordenararchivos(abspath)


data_archivos= dt.limpiararchivos(archivos)


i_fechas= fn.funcfechas(archivos)

global_tickers = fn.functickers(archivos,data_archivos)


data = fn.funcdesdatos(global_tickers)

data_close = fn.funccierres(data,global_tickers)

ic_fechas = fn.funcfechacierre(data_close,i_fechas)

precios = fn.funcprecio(data_close,ic_fechas)

pos_datos = fn.funcdatosposi(eliminar,data_archivos,archivos,precios,k,c)

Cash = k - pos_datos['Postura'].sum() - pos_datos['Comisiones'].sum()


inv_pasiva = {'Dates': ['2018-01-30'], 'Capital': [k]}

inv_pasiva =fn.funcpasiva(ic_fechas,pos_datos,precios,Cash,inv_pasiva)


df_pasiva=vis.pasiva(inv_pasiva)
