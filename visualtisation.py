import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the data
df_pays = pd.read_csv('ressources/Country-data.csv')

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Input(id='country-input', type='text', placeholder='Enter a country'),
    html.Div(id='histograms')
])

# Define the callback
@app.callback(
    Output('histograms', 'children'),
    Input('country-input', 'value')
)
def update_histograms(country):
    if country is None:
        country = ''

    bar_charts = []
    for column in ['child_mort', 'exports', 'health', 'imports', 'income', 'inflation']:
        df = df_pays.copy()
        df = df.sort_values(by=column, ascending=False)
        fig = px.bar(df, x='country', y=column, title=column)
        fig.update_traces(marker_line_width=[3 if x == country else 0 for x in df['country']],
                          marker_line_color='red')
        fig.update_layout(showlegend=False)
        bar_charts.append(dcc.Graph(figure=fig))

    return bar_charts

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)