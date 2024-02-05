import numpy as np
from bokeh.io import output_notebook, curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Slider, Div
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap
from bokeh.palettes import all_palettes
from scipy.integrate import odeint
from bokeh.models import ColumnDataSource

def S_model( S,t,B,I):
    return -B*I*S
def R_model(I,t,y):
    return y*I
def I_model(S,t,B,I,y):
    return B*I*S-y*I
def diff(N,t,params):
    S,R,I = N
    B,y = params
    derivs=[S_model(S,t,B,I),R_model(I,t,y),I_model(S,t,B,I,y)]
    return derivs
beta = Slider(start=0, end=1, value=0.5, step=0.005, title='beta', width=200)
gamma = Slider(start=0, end=1, value=0.5, step=0.005, title='gamma', width=200)
fig = figure(
    #sizing_mode='stretch_width',
    width=800,
    aspect_ratio=2,
    title='Model SIR',
    x_axis_label='$$t$$',
    y_axis_label='$$N$$',
)
fig.grid.grid_line_dash = [6, 4]
fig.toolbar.logo = None
fig.toolbar.autohide = True
B=beta.value
y=gamma.value
t = np.linspace(0, 20, 1000)
S0=100
R0=0
I0=10
params=[B,y]
N0=[S0,R0,I0]
solved= odeint(diff,N0,t,args=(params,))
datas = {'x_values': t,   'y_values': solved[:,0]}
datar = {'x_values': t,   'y_values': solved[:,1]}
datai = {'x_values': t,   'y_values': solved[:,2]}
sources = ColumnDataSource(data=datas)
sourcer = ColumnDataSource(data=datar)
sourcei = ColumnDataSource(data=datai)
sw=fig.line( x='x_values', y='y_values',source=sources, color='green', legend_label='S', line_width=3)
rw=fig.line(x='x_values', y='y_values',source=sourcer, color='black', legend_label='R', line_width=3)
iw=fig.line(x='x_values', y='y_values',source=sourcei, color='red', legend_label='I', line_width=3)
def update(attr, old, new):
    t = np.linspace(0, 20, 1000)
    B=beta.value
    y=gamma.value
    S0=100
    R0=0
    I0=10
    params=[B,y]
    N0=[S0,R0,I0]
    solved= odeint(diff,N0,t,args=(params,))
    datas = {'x_values': t,   'y_values': solved[:,0]}
    datar = {'x_values': t,   'y_values': solved[:,1]}
    datai = {'x_values': t,   'y_values': solved[:,2]}
    
    sourcer.data=datar
    sourcei.data=datai
    sources.data=datas
    #sw.data_source.data=solved[:,0]
    #rw.data_source.data=solved[:,1]
    #iw.data_source.data=solved[:,2]
    

    

   

beta.on_change('value_throttled', update)
gamma.on_change('value_throttled', update)
curdoc().add_root(column(Div(text='<h1>Program 9</h1>'), row(column(beta,gamma), fig)))








