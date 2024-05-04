import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Data
df_pays = pd.read_csv('ressources/Country-data.csv')

column_names = df_pays.columns.tolist()
column_names.remove('country')

# Dropdown
dropdown_options = [{'label': col.replace('_', ' ').title(), 'value': col} for col in column_names]

# Dash application
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1('Country data',
            style={'textAlign': 'center',
                   'color': '#5151F6FF',
                   'font-family': 'Arial'
                   }
            ),
    html.Div([
        html.H3('Select the necessary information',
                style={'textAlign': 'center',
                       'color': 'black',
                       'font-family': 'Arial',
                       'textDecoration': 'underline'
                       }
                ),
        dcc.Input(
            id='country-input',
            type='text',
            placeholder='Enter a country',
            className='my-input'
        ),
        dcc.Dropdown(
            id='column-dropdown',
            options= dropdown_options,
            value='child_mort',
            clearable=False,
            className='my-dropdown'
        ),
        dcc.Slider(
            id='num-countries-slider',
            min=1,
            max=len(df_pays),
            value=10,
            className='my-slider'
        )
    ],
        style={'display': 'flex',
               'align-items': 'center',
               'flex-direction': 'column',
               'borderRadius': '10px',
               'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
               'padding': '10px',
               'margin': '20px',
               }
    ),
    html.Div(id='histograms')
])


@app.callback(
    Output('histograms', 'children'),
    Input('country-input', 'value'),
    Input('column-dropdown', 'value'),
    Input('num-countries-slider', 'value')
)
def update_histograms(country, column, num_countries):
    if country is None:
        country = ''

    df = df_pays.copy()
    df = df.sort_values(by=column, ascending=False).head(num_countries)
    fig = px.bar(df, x='country', y=column, title=column)
    fig.update_traces(marker_line_width=[3 if x == country else 0 for x in df['country']],
                      marker_line_color='red')
    fig.update_layout(showlegend=False)

    return dcc.Graph(figure=fig)


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
