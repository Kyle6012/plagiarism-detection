import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
import base64
import json

def create_dashboard(flask_app):
    dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')

    dash_app.layout = html.Div([
        html.H1("Plagiarism Detection Dashboard"),
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'
            }
        ),
        html.Div(id='output-data-upload'),

        html.Div([
            html.Div([
                html.H3("Similarity Scores"),
                dcc.Graph(id='similarity-graph')
            ], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                html.H3("AI-Generated Content Probability"),
                dcc.Graph(id='ai-gauge')
            ], style={'width': '49%', 'display': 'inline-block'})
        ])
    ])

    @dash_app.callback(
        [Output('similarity-graph', 'figure'),
         Output('ai-gauge', 'figure'),
         Output('output-data-upload', 'children')],
        [Input('upload-data', 'contents')],
        [State('upload-data', 'filename')]
    )
    def update_output(contents, filename):
        if contents is None:
            return {}, {}, ""

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        files = {'file': (filename, decoded, content_type)}
        response = requests.post("http://127.0.0.1:5000/analyze", files=files)

        if response.status_code != 200:
            return {}, {}, f"Error: {response.text}"

        data = response.json()

        # Similarity Graph
        similarity_fig = go.Figure(go.Bar(
            x=data.get('similarities', []),
            y=data.get('labels', []),
            orientation='h'
        ))

        # AI Gauge
        ai_prob = data.get('ai_generated_probability', 0)
        ai_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = ai_prob * 100,
            title = {'text': "AI Probability"},
            gauge = {'axis': {'range': [None, 100]}}
        ))

        return similarity_fig, ai_gauge, f"File '{filename}' processed."

    return dash_app
