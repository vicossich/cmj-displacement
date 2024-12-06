
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import json

st.set_page_config(page_title="Mokapp",
    page_icon="",
    layout="wide")

####
@st.cache_data
def load_data(file):
    return pd.read_csv(file)
####

# image = Image.open('./static/images/MI_brand_Artboard 3_reverse-2spot.png'
st.markdown(
    """
    <style>

        /* import font */
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap');
        
        /* Apply Figtree font globally */
        html, body, [class*="css"] {
            font-family: 'Figtree', sans-serif !important;
        }

        /* hide decoration bar */
        #stDecoration {visibility: hidden;}

        /* sidebar bg_color */
        [data-testid="stSidebar"] {
            background-color: #2b2a3f; /* Replace with your preferred color */
        }

        /* sidebar logo */
        [data-testid="stSidebarHeader"] {
            background-image: url("https://raw.githubusercontent.com/vicossich/mk3d/main/mk_logo.png");
            background-repeat: no-repeat;
            background-size: contain; /* Adjust size to fit the sidebar */
            padding-top: 70px; /* Space to push content below the image */
            background-position: top center; /* Position image at the top center */
            margin:10px;
            background-color: #fff;
            border-radius: 100px;
        }

        /* Target the entire sidebar navigation container */
        [data-testid="stWidgetLabel"] {
            color: #fff !important; /* Force all text within the sidebar nav to white */
        }

        /* Style the links (default state) */
        [data-testid="stSidebarNavItems"] a {
            color: #fff !important; /* Text color white */
            text-decoration: none; /* Remove underline (optional) */
            background-color: transparent; /* Ensure no background */
            padding: 5px 10px; /* Add some padding for better hover effect */
            border-radius: 5px; /* Optional: Rounded edges */
        }

        [data-testid="stSidebarUserContent"]{
            padding-top: 0px;
        }



        /* change main area padding */
        div.st-emotion-cache-1jicfl2 {
            padding: 40px;
        }

        
    </style>
    """,
    unsafe_allow_html=True,
)
def foot_space_displacement_graph(vectors, mean_vector, rightSideLabel='Right', leftSideLabel='Left', ylabel='Antero-Posterior', xlabel='Lateral-Lateral'):
    traces = []
    Xs = []
    Ys = []

    # Create traces for each vector
    for index, vector in enumerate(vectors):
        x1, y1 = vector[0]['x'], vector[0]['y']
        x2, y2 = vector[1]['x'], vector[1]['y']

        Xs.extend([x1, x2])
        Ys.extend([y1, y2])

        # Add vector trace
        traces.append(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode='lines+markers',
            line=dict(color='#5CB0FF', width=4),
            marker=dict(
                size=[1, 30],
                color='#5CB0FF',
                symbol=['square', 'square']
            ),
            name=f'Rep {index + 1}',
            showlegend=True
        ))

        # Add text annotations
        traces.append(go.Scatter(
            x=[x2],
            y=[y2],
            mode='text',
            text=[str(index + 1)],
            textposition='middle center',
            textfont=dict(size=15, color='#ffffff'),
            showlegend=False,
            hoverinfo='none'
        ))

    # Calculate mean vector components
    mean_x = round(mean_vector['magnitude'] * np.cos(mean_vector['direction_radians']) * 10) / 10
    mean_y = round(mean_vector['magnitude'] * np.sin(mean_vector['direction_radians']) * 10) / 10

    # Add mean vector trace
    traces.append(go.Scatter(
        x=[0, mean_x],
        y=[0, mean_y],
        mode='lines+markers',
        line=dict(color='red', width=3),
        marker=dict(
            size=[1, 10],
            color='red',
            symbol=['circle', 'circle'],
            line=dict(color='#ffffff', width=2)
        ),
        name='mean',
        showlegend=True
    ))

    Xs.append(mean_x)
    Ys.append(mean_y)

    # Determine the maximum point for axis limits
    max_point = 1.2 * max(max(map(abs, Xs)), max(map(abs, Ys)))

    # Define layout settings
    layout = go.Layout(
        xaxis=dict(
            title=f'{xlabel} (cm)',
            range=[-max_point, max_point],
            zeroline=True,
            showgrid=True,
            zerolinewidth=1,
            zerolinecolor='#cccccc'
        ),
        yaxis=dict(
            title=f'{ylabel} (cm)',
            range=[max_point, -max_point],
            zeroline=True,
            showgrid=True,
            zerolinewidth=1,
            zerolinecolor='#cccccc'
        ),
        autosize=True,
        showlegend=True,
        legend=dict(x=0.8, y=0.01, bgcolor='rgba(255, 255, 255, 0)'),
        plot_bgcolor='#f9f9f9',
        margin=dict(l=50, r=50, t=25, b=40),

        images=[
            dict(
                source="https://raw.githubusercontent.com/vicossich/mk3d/main/mk_logo.png",
                xref="paper", yref="paper",
                x=0.90, y=0.9,
                sizex=0.15, sizey=0.15,
                xanchor="center", yanchor="middle"
            )
        ],
        annotations = [
            {
                "x": 0,
                "y": -0.9 * max_point,
                "text": "Posterior",
                "showarrow": False,
                "font": {"size": 12, "color": "gray"}
            },
            {
                "x": 0,
                "y": 0.9 * max_point,
                "text": "Anterior",
                "showarrow": False,
                "font": {"size": 12, "color": "gray"}
            },
            {
                "x": -0.8 * max_point,
                "y": 0,
                "text": rightSideLabel,
                "showarrow": False,
                "font": {"size": 12, "color": "gray"},
                "xanchor": "right"
            },
            {
                "x": 0.8 * max_point,
                "y": 0,
                "text": leftSideLabel,
                "showarrow": False,
                "font": {"size": 12, "color": "gray"},
                "xanchor": "left"
            }
        ]

    )


    # Plot figure
    fig = go.Figure(data=traces, layout=layout)
    return fig


#############
def plot_displacement_polar(magnitudes, labels,group_magnitude):
    """
    Plota um gráfico polar de deslocamento com base nas magnitudes e labels fornecidos.

    Args:
        magnitudes (list): Lista de magnitudes (valores entre 0 e 20).
        labels (list): Lista de labels de direções correspondentes ('Anterior', 'Posterior', etc.).

    Returns:
        None: Exibe o gráfico interativo.
    """
    # Mapeamento de ângulos para direções
    angle_map = {
        'Neutral': 0,
        'Anterior': 270,         # Alinhando com -90° (Sul)
        'Posterior': 90,         # Parte superior (Norte)
        'Left': 180,             # Esquerda
        'Right': 0,              # Direita
        'Anterior-Left': 225,    # Sul-Oeste
        'Anterior-Right': 315,   # Sul-Leste
        'Posterior-Left': 135,   # Norte-Oeste
        'Posterior-Right': 45    # Norte-Leste
    }

    # Converter os labels para ângulos
    angles = [angle_map[label] for label in labels]

    # Criar o gráfico polar
    fig = go.Figure()

    # Adicionar os pontos com magnitude
    fig.add_trace(go.Scatterpolar(
        r=magnitudes,
        theta=angles,
        mode='markers+text',
#         text=[f"{label} ({magnitude})" for label, magnitude in zip(labels, magnitudes)],
#         textposition="middle right",
        marker=dict(size=10, color='red', opacity=0.4)
    ))
    # 5CB0FF
    
    magnitudes_mean = round(np.array(magnitudes).mean(),1)
    fig.add_trace(go.Scatterpolar(
      name = "média individual",
      r = [magnitudes_mean]*360,
      theta = list(range(360)),
      mode='lines',
      line=dict(color='red', width=1)  # Definindo a cor do trace como vermelho

    ))

    fig.add_trace(go.Scatterpolar(
      name = "média groupo",
      r = [group_magnitude]*360,
      theta = list(range(360)),
      mode='lines',
      line=dict(color='green', width=1)  # Definindo a cor do trace como vermelho

    ))

    # Adicionar os rótulos das direções principais fora do círculo
    directions = {
        'Anterior': 270,  # Sul
        'Posterior': 90,  # Norte
        'Left': 180,      # Esquerda
        'Right': 0,       # Direita
        'Anterior-Left': 225,
        'Anterior-Right': 315,
        'Posterior-Left': 135,
        'Posterior-Right': 45
    }
    for direction, angle in directions.items():
        fig.add_trace(go.Scatterpolar(
            r=[24],  # Raio maior para rótulos fora do círculo
            theta=[angle],
            mode='text',
            # mode='lines',
            text=[direction],
            textfont=dict(size=10, color="black", family="Arial"),
            showlegend=False,
        ))

    # Configurar layout com escala de magnitude fixa entre 0 e 20
    fig.update_layout(
        polar=dict(
            bgcolor='#f9f9f9',       # Define a cor de fundo da área do radar
            angularaxis=dict(
                direction="clockwise",   # Sentido horário
                rotation=180,             # Rotacionando o gráfico para -90°
                tickmode="linear",
                dtick=45,                # Intervalo entre os ticks angulares
                ticklen=3,               # Comprimento dos ticks angulares
                tickwidth=1,             # Largura dos ticks angulares
                tickcolor='grey',        # Cor dos ticks angulares
                tickfont=dict(size=8),   # Tamanho da fonte dos ticks angulares
                gridcolor='lightgrey',   # Cor das linhas de grade angulares
                gridwidth=0.5,           # Largura das linhas de grade angulares
                showticklabels=False     # Ocultar labels dos ticks angulares
            ),
            radialaxis=dict(
                visible=True,
                range=[0, 25],
                showticklabels=True,
                ticks='outside',
                ticklen=3,               # Comprimento dos ticks radiais
                tickwidth=1,             # Largura dos ticks radiais
                tickcolor='grey',        # Cor dos ticks radiais
                tickfont=dict(size=8),   # Tamanho da fonte dos ticks radiais
                dtick=5,                 # Intervalo entre os ticks radiais
                gridcolor='lightgrey',   # Cor das linhas de grade radiais
                gridwidth=0.5            # Largura das linhas de grade radiais
            )
        ),
        showlegend=False,
        autosize=True,
        plot_bgcolor='#f9f9f9'
    )
    

    return fig


# Load data
data = load_data('output_vectors.csv')

# st.dataframe(data)
# Correct the JSON formatting in the 'vectors' column
# data['vectors'] = data['vectors'].apply(lambda x: x.replace("'", '"') if isinstance(x, str) else x)

# Sidebar for athlete selection
atleta = st.sidebar.selectbox(
    "Atleta", 
    list(data['name'].unique()), 
    key="atleta"
)

# Filter data for the selected athlete
filtered_data = data[data['name'] == atleta].copy()

# Convert dates to datetime explicitly using .loc to avoid warnings
filtered_data.loc[:, 'date'] = pd.to_datetime(filtered_data['date'])

# Get unique dates for dropdown selection
dates = sorted(filtered_data['date'].unique())


col1, col2, col3 = st.columns([1,3,2])

with col1:
    st.write(f'### {atleta}')


    # Dropdown for date selection
    selected_date = st.selectbox(
        "Select Date",
        options=dates,
        format_func=lambda x: x.strftime("%Y-%m-%d"),
        key="selected_date"
    )

    # Filter the data for the selected date
    date_filtered_data = filtered_data[filtered_data['date'] == selected_date]

with col2:

    # Display plot if there is data for the selected date
    if not date_filtered_data.empty:
        vectors = json.loads(date_filtered_data['vectors'].values[0])
        mean_vector = json.loads(date_filtered_data['mean_vector'].values[0])

        fig = foot_space_displacement_graph(vectors=vectors, mean_vector=mean_vector)

        st.plotly_chart(fig, use_container_width=True, key="time")
    else:
        st.warning("No data available for the selected date.")

with col3:
    # Exemplo de uso
    # Converter a coluna `mean_vector` de string JSON para dicionário
    filtered_data['mean_vector'] = filtered_data['mean_vector'].apply(json.loads)
    # Extrair todas as magnitudes em uma lista
    magnitudes = filtered_data['mean_vector'].apply(lambda x: x['magnitude']).tolist()
    # magnitudes = [1.5, 2.3, 0.8, 1.7, 2.0]

    # labels = ['Anterior-Left', 'Posterior-Right', 'Neutral', 'Anterior', 'Right']
    labels = filtered_data['direction'].values



    # Assuming 'data' is your DataFrame
    # Parse the 'mean_vector' column
    data['mean_vector'] = data['mean_vector'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

    # Safely extract 'magnitude' and calculate the mean
    data['magnitude'] = data['mean_vector'].apply(lambda x: x.get('magnitude') if isinstance(x, dict) else None)

    # Calculate the mean of 'magnitude', ignoring NaN values
    group_magnitude = data['magnitude'].mean().round(1)

    # st.write(group_magnitude)
    # group_magnitude = 10

    fig_radar = plot_displacement_polar(magnitudes=magnitudes,labels=labels,group_magnitude=group_magnitude)
    st.plotly_chart(fig_radar, use_container_width=True, key="space")



st.dataframe(filtered_data[['date','direction']].T)

st.write(filtered_data['direction'].value_counts())
