import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
import pandas as pd
from apps.health_records.models import HealthRecord

# Registrar la app en django_plotly_dash
app = DjangoDash('HealthGuardDash')

# Definir la estructura del layout
layout_content = html.Div([
    html.Div([
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Presión Arterial', 'value': 'bp'},
                {'label': 'Frecuencia Cardíaca', 'value': 'hr'},
                {'label': 'Glucosa en Sangre', 'value': 'glucose'},
                {'label': 'Índice de Masa Corporal (IMC)', 'value': 'bmi'},
            ],
            value='bp',
            clearable=False,
            style={
                'backgroundColor': '#1f2937',
                'color': '#000000',
                'borderRadius': '6px',
            }
        ),
    ], style={'marginBottom': '20px'}),
    
    dcc.Graph(
        id='health-graph',
        config={'displayModeBar': False, 'responsive': True},
        style={'height': '380px'}
    )
], style={'padding': '10px'})

# Asignar la estructura al atributo layout de la app
app.layout = layout_content # type: ignore     


@app.callback(
    Output('health-graph', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_graph(selected_metric):
    records = HealthRecord.objects.all().order_by('recorded_at')
    fig = go.Figure()

    if not records.exists():
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a0aec0'),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[{
                'text': 'No hay datos registrados aún',
                'xref': 'paper', 'yref': 'paper',
                'showarrow': False,
                'font': {'size': 16, 'color': '#a0aec0'}
            }]
        )
        return fig

    # Construir dataframe con los registros
    data = []
    for r in records:
        bmi = None
        if r.weight_kg and r.height_cm:
            bmi = round(r.weight_kg / ((r.height_cm / 100) ** 2), 2)
        
        data.append({
            'recorded_at': r.recorded_at.strftime('%d/%m %H:%M'),
            'systolic_bp': r.systolic_bp,
            'diastolic_bp': r.diastolic_bp,
            'heart_rate': r.heart_rate,
            'blood_glucose': r.blood_glucose,
            'bmi': bmi
        })

    df = pd.DataFrame(data)

    if selected_metric == 'bp':
        fig.add_trace(go.Scatter(
            x=df['recorded_at'], y=df['systolic_bp'],
            mode='lines+markers', name='Sistólica',
            line=dict(color='#00d2ff', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=df['recorded_at'], y=df['diastolic_bp'],
            mode='lines+markers', name='Diastólica',
            line=dict(color='#00f2fe', width=3),
            marker=dict(size=8)
        ))
        title = 'Evolución de Presión Arterial (mmHg)'

    elif selected_metric == 'hr':
        fig.add_trace(go.Scatter(
            x=df['recorded_at'], y=df['heart_rate'],
            mode='lines+markers', name='Ritmo Cardíaco',
            line=dict(color='#ff4b1f', width=3),
            marker=dict(size=8)
        ))
        title = 'Evolución de Frecuencia Cardíaca (BPM)'

    elif selected_metric == 'glucose':
        fig.add_trace(go.Scatter(
            x=df['recorded_at'], y=df['blood_glucose'],
            mode='lines+markers', name='Glucosa',
            line=dict(color='#f8b500', width=3),
            marker=dict(size=8)
        ))
        title = 'Evolución de Glucosa en Sangre (mg/dL)'

    elif selected_metric == 'bmi':
        fig.add_trace(go.Scatter(
            x=df['recorded_at'], y=df['bmi'],
            mode='lines+markers', name='IMC',
            line=dict(color='#11998e', width=3),
            marker=dict(size=8)
        ))
        title = 'Evolución del Índice de Masa Corporal (IMC)'

    fig.update_layout(
        title=dict(text=title, font=dict(color='#ffffff', size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#a0aec0'),
        xaxis=dict(
            gridcolor='#2d3748',
            zerolinecolor='#2d3748',
            tickfont=dict(color='#a0aec0')
        ),
        yaxis=dict(
            gridcolor='#2d3748',
            zerolinecolor='#2d3748',
            tickfont=dict(color='#a0aec0')
        ),
        margin=dict(l=30, r=30, t=50, b=40),
        legend=dict(font=dict(color='#ffffff'))
    )

    return fig