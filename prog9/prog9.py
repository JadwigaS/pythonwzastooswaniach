import numpy as np
from bokeh.io import output_notebook, curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Slider, Div
from bokeh.util.hex import hexbin
from bokeh.transform import linear_cmap
from bokeh.palettes import all_palettes
from scipy.integrate import odeint


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
beta = Slider(start=0, end=1, value=0.5, step=0.01, title='beta', width=200)
gamma = Slider(start=0, end=1, value=0.5, step=0.01, title='gamma', width=200)
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
t = np.linspace(0, 10, 100)
S0=100
R0=0
I0=10
params=[B,y]
N0=[S0,R0,I0]
solved= odeint(diff,N0,t,args=(params,))
sw=fig.line(t, solved[:,0], color='green', legend_label='S', line_width=3)
rw=fig.line(t, solved[:,1], color='black', legend_label='R', line_width=3)
iw=fig.line(t, solved[:,2], color='red', legend_label='I', line_width=3)
def update(attr, old, new):
    t = np.linspace(0, 10, 100)
    B=beta.value
    y=gamma.value
    S0=100
    R0=0
    I0=10
    params=[B,y]
    N0=[S0,R0,I0]
    solved= odeint(diff,N0,t,args=(params,))
    
    sw.data_source.data=solved[:,0]
    rw.data_source.data=solved[:,1]
    iw.data_source.data=solved[:,2]
    

    

   

beta.on_change('value_throttled', update)
gamma.on_change('value_throttled', update)
curdoc().add_root(column(Div(text='<h1>Program 9</h1>'), row(column(beta,gamma), fig)))








