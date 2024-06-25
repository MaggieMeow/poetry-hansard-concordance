import json
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

with open('global_concordance_dict.json', 'r') as file:
    global_concordance_dict = json.load(file)

# Initialize the Dash app
app = dash.Dash(__name__)
server=app.server

app.layout = html.Div([
    dcc.Dropdown(
        id='placename-dropdown',
        options=[{'label': placename, 'value': placename} for placename in sorted(global_concordance_dict.keys())],
        placeholder='Select a Placename'
    ),
    dash_table.DataTable(
        id='concordance-table',
        columns=[
            {'name': 'Index', 'id': 'index'},
            {'name': 'Year', 'id': 'year'},
            {'name': 'Before', 'id': 'before'},
            {'name': 'Key Phrase', 'id': 'key_phrase', 'presentation': 'markdown'},
            {'name': 'After', 'id': 'after'}
        ],
        style_cell={
            'textAlign': 'center', 
            'padding': '10px', 
            'whiteSpace': 'normal', 
            'height': 'auto',
            'maxWidth': '400px',
            },
        style_data_conditional=[
            {
                'if': {'column_id': 'key_phrase'},
                'fontWeight': 'bold',
                'color': 'red'
            }
        ],
        style_as_list_view=True,
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        }
    )
])

@app.callback(
    Output('concordance-table', 'data'),
    Input('placename-dropdown', 'value')
)

def update_table(selected_placename):
    data = []
    if selected_placename:
        years = global_concordance_dict.get(selected_placename, {})
        sorted_years = sorted(years.keys(), key=lambda x: int(x))  # Sort years numerically
        for year in sorted_years:
            concordance_entries = years[year]
            for entry in concordance_entries:
                line = entry['line']
                parts = line.split(selected_placename.upper(), 1)
                data.append({
                    'index': entry['index'],
                    'year': year,
                    'before': parts[0],
                    'key_phrase': f"**{selected_placename}**",
                    'after': parts[1] if len(parts) > 1 else ''
                })
    return data

if __name__ == '__main__':
    app.run_server(debug=True)
