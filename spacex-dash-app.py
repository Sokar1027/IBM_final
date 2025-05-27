# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown', 
                                             options=[
                                                    {'label':'All sites', 'value':'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value':'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value':'VAFB SLC-4E'}],
                                             value='ALL',
                                             placeholder='Select a launch site here',
                                             searchable=True),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                               


                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min=0, max=10000, step=1000,
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'))

def update_pie_chart(entered_site):
    return get_pie_chart(entered_site)

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']==1]
        df_grouped = filtered_df.groupby('Launch Site').size().reset_index(name='successes')
        fig = px.pie(df_grouped, values='successes',
        names='Launch Site',
        title='success rate for ALL launch sites')
        return fig 
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        df_grouped = filtered_df.groupby('class').size().reset_index(name='count')
        df_grouped['class'] = df_grouped['class'].map({0: 'Failure', 1: 'Success'})
        fig = px.pie(df_grouped,values='count',
        names='class',
        title=f'success vs failure for {entered_site}')
        return fig 

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])

def update_scatter_plot(entered_site, payload_range):
    return get_scatter_plot(entered_site, payload_range)


def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

                                
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Run the app
if __name__ == '__main__':
    app.run()
