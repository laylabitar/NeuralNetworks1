#!/usr/bin/env python
# coding: utf-8

# In[12]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import chart_studio
import chart_studio.plotly as py
import numpy as np
import plotly.graph_objs as go
from sklearn.metrics import mean_squared_error
import plotly.io as pio




# Set your Plotly Chart Studio credentials
username='layla123'
api_key='qzCAcE28n6jeMkmXS1Mn'

chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

app = dash.Dash(__name__)

# Generate noisy points resembling a parabola shape (fixed and not changing)
x_noise = np.arange(-10, 11, 0.1)
y_noise = 2 * x_noise**2 + np.random.normal(0, 10, len(x_noise))
df_noise = pd.DataFrame({'X': x_noise, 'Y': y_noise})

# Define the layout of the app
app.layout = html.Div([
    html.H1(id='title', children="Parabola with Coefficient Sliders and Noise"),
    dcc.Slider(
        id='a-slider',
        min=-10,
        max=10,
        step=0.1,
        value=2,
        marks={i: str(i) for i in range(-10, 11)},
        tooltip={'placement': 'top'},
        updatemode='drag'
    ),
    dcc.Slider(
        id='b-slider',
        min=-10,
        max=10,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(-10, 11)},
        tooltip={'placement': 'top'},
        updatemode='drag'
    ),
    dcc.Slider(
        id='c-slider',
        min=-10,
        max=10,
        step=0.1,
        value=0,
        marks={i: str(i) for i in range(-10, 11)},
        tooltip={'placement': 'top'},
        updatemode='drag'
    ),
    dcc.Graph(id='parabola-plot'),
])

# Calculate the MSE
def calculate_mse(a, b, c):
    x = pd.Series(x_noise)
    y_parabola = a * x**2 + b * x + c
    y_noise = df_noise['Y']
    mse = mean_squared_error(y_noise, y_parabola)  # Calculate MSE between noisy points and parabola
    return mse

# Define callback to update the plot and MSE in the title
@app.callback(
    [Output('parabola-plot', 'figure'),
     Output('title', 'children')],
    [Input('a-slider', 'value'),
     Input('b-slider', 'value'),
     Input('c-slider', 'value')]
)
def update_parabola_plot(a, b, c):
    x = pd.Series(x_noise)
    y_parabola = a * x**2 + b * x + c

    # Create a trace for the noisy points using go.Scatter
    noisy_points_trace = go.Scatter(
        x=x_noise,
        y=df_noise['Y'],
        mode='markers',
        name='Noise'
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_parabola, name='Parabola'))
    fig.add_trace(noisy_points_trace)

    mse = calculate_mse(a, b, c)

    return fig, f"Parabola with Coefficient Sliders and Noise - MSE: {mse:.4f}"


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
    # Publish the chart to Chart Studio


    


# In[ ]:




