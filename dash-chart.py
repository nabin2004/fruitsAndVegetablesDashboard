import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("cleaned_data.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Commodity Price Dashboard"),
    html.Label("Select Commodity:"),
    dcc.Dropdown(
        id='commodity-dropdown',
        options=[{'label': commodity, 'value': commodity} for commodity in df['Commodity'].unique()],
        value=df['Commodity'].unique()[0] 
    ),
    dcc.Graph(id='price-trend-graph')
])

@app.callback(
    Output('price-trend-graph', 'figure'),
    Input('commodity-dropdown', 'value')
)
def update_graph(selected_commodity):
    filtered_df = df[df['Commodity'] == selected_commodity]

    # Create the line plot
    fig = px.line(
        filtered_df,
        x='Date',
        y=['Minimum', 'Maximum', 'Average'],
        labels={'value': 'Price', 'variable': 'Price Type'},
        title=f"Price Trends for {selected_commodity}"
    )

    fig.update_layout(xaxis_title="Date", yaxis_title="Price", legend_title="Price Type")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
