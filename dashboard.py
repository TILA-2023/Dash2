import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import random
from wordcloud import WordCloud
import base64
from io import BytesIO

# Función para generar datos en tiempo real
def generar_datos():
    fechas = pd.date_range(start="2024-02-01", periods=30, freq="D")
    datos = pd.DataFrame({
        "Fecha": fechas,
        "Menciones Totales": [random.randint(100, 1500) for _ in range(30)],
        "Sentimiento Positivo": [random.randint(50, 800) for _ in range(30)],
        "Sentimiento Negativo": [random.randint(10, 500) for _ in range(30)],
        "Fake News Detectadas": [random.randint(0, 20) for _ in range(30)]
    })
    datos["Alerta Crisis"] = ["🚨" if (neg / total) > 0.25 else "✅" 
                               for neg, total in zip(datos["Sentimiento Negativo"], datos["Menciones Totales"])]
    return datos

# Función para generar la nube de palabras
def generar_nube():
    texto_tendencias = "sostenible lujo gastronomía experiencias playa aventura ecoturismo familiar vida-nocturna resorts relajación"
    wordcloud = WordCloud(width=400, height=200, background_color="white").generate(texto_tendencias)
    img = BytesIO()
    wordcloud.to_image().save(img, format="PNG")
    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()

# Inicializar la app Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Dashboard de Monitoreo de Medios en Tiempo Real"),
    
    dcc.Interval(id="intervalo", interval=5000, n_intervals=0),  # Actualización cada 5 segundos

    # Sección 1: Análisis de Competencia
    html.H3("📊 Comparación de Menciones entre Destinos Turísticos"),
    dcc.Graph(id="menciones-destinos"),

    # Sección 2: Sentimiento en Medios y Redes
    html.H3("📈 Tendencia de Sentimientos en Medios y Redes"),
    dcc.Graph(id="sentiment-trend"),

    # Sección 3: Tendencias Emergentes (Nube de palabras)
    html.H3("☁️ Tendencias Emergentes en Turismo"),
    html.Img(id="nube-palabras"),

    # Sección 4: Impacto de Campañas en Engagement
    html.H3("📊 Impacto de Campañas en Engagement"),
    dcc.Graph(id="impacto-campanas"),

    # Sección 5: Detección de Fake News
    html.H3("🛑 Detección de Fake News en Medios y Redes"),
    dcc.Graph(id="fake-news-bar"),

    # Sección 6: Alertas de Crisis
    html.H3("🚨 Alertas de Crisis de Reputación"),
    dcc.Graph(id="alertas-crisis"),
])

@app.callback(
    [Output("menciones-destinos", "figure"),
     Output("sentiment-trend", "figure"),
     Output("nube-palabras", "src"),
     Output("impacto-campanas", "figure"),
     Output("fake-news-bar", "figure"),
     Output("alertas-crisis", "figure")],
    [Input("intervalo", "n_intervals")]
)
def actualizar_graficos(n):
    datos = generar_datos()
    
    # Gráfico: Comparación de menciones entre destinos
    destinos = ["Quintana Roo", "Cancún", "Riviera Nayarit", "Tulum", "Los Cabos"]
    menciones_destinos = [random.randint(500, 1500) for _ in destinos]
    fig_menciones_destinos = px.bar(x=destinos, y=menciones_destinos, title="Menciones por Destino", labels={"x": "Destino", "y": "Menciones"})

    # Gráfico: Tendencia de Sentimientos
    fig_sentimiento = px.line(datos, x="Fecha", y=["Sentimiento Positivo", "Sentimiento Negativo"], 
                              title="📈 Sentimiento en Redes Sociales", labels={"value": "Cantidad de Menciones"})

    # Nube de palabras
    img_nube = generar_nube()

    # Gráfico: Impacto de Campañas
    campañas = ["Campaña A", "Campaña B", "Campaña C"]
    engagement_antes = [random.randint(500, 1000) for _ in campañas]
    engagement_despues = [antes + random.randint(200, 800) for antes in engagement_antes]
    fig_impacto = px.bar(x=campañas, y=[engagement_antes, engagement_despues], 
                         title="📊 Engagement Antes vs. Después", labels={"x": "Campañas", "y": "Engagement"},
                         barmode="group")

    # Gráfico: Fake News Detectadas
    fig_fake_news = px.bar(datos, x="Fecha", y="Fake News Detectadas", title="🛑 Fake News Detectadas")

    # Gráfico: Alertas de Crisis
    alertas = datos["Alerta Crisis"].value_counts()
    fig_alertas = px.bar(x=alertas.index, y=alertas.values, title="🚨 Alertas de Crisis de Reputación", labels={"x": "Estado", "y": "Número de Alertas"})

    return fig_menciones_destinos, fig_sentimiento, img_nube, fig_impacto, fig_fake_news, fig_alertas

if __name__ == "__main__":
    app.run_server(debug=True)
