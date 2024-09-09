from flask import Flask, render_template
import plotly.graph_objects as go
from io import BytesIO
import base64

app = Flask(__name__)

# Definir el filtro b64encode
def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

# Registrar el filtro en la aplicación Flask
app.jinja_env.filters['b64encode'] = b64encode

@app.route('/')
def index():
    # Ejecutar el script app.py
    from dataCleansing import dataSummary

    # Gráfico de la pie chart
    counts = dataSummary['didWeWon'].value_counts()
    labels = ['Perdedor', 'Ganador']
    sizes = counts
    colors = ['cornflowerblue', 'gold']
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
    fig_pie.update_traces(textfont_size=20, marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    
    # Gráfico de promedio de ranking
    avg_rank = round(dataSummary['ourStoreRank'].mean())
    fig_rank = go.Figure(go.Indicator(
        mode="number",
        value=avg_rank,
        title={"text": "Average market ranking", "font": {"size": 23, "color": "black"}},
        number={"font": {"size": 80, "color": "black"}},
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={"reference": 10, "relative": True, "position": "top", "font": {"size": 14, "color": "green"}}
    ))
    fig_rank.update_layout(
        height=170,
        width=280,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='gold',
        font=dict(family="Arial", color="black")
    )
    
    # Gráfico de diferencia de precios
    avg_diff_price = round(dataSummary['priceDifference'].mean())
    fig_price = go.Figure(go.Indicator(
        mode="number",
        value=avg_diff_price,
        title={"text": "Average price difference vs rival stores", "font": {"size": 23, "color": "black"}},
        number={"valueformat": ",.2f", "prefix": "$", "font": {"size": 80, "color": "black"}},
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={"reference": 10, "relative": True, "position": "top", "font": {"size": 14, "color": "green"}},
    ))
    fig_price.update_layout(
        height=170,
        width=450,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='cornflowerblue',
        font=dict(family="Arial", color="black")
    )

    img_pie = BytesIO(fig_pie.to_image(format='png')).getvalue()
    img_rank = BytesIO(fig_rank.to_image(format='png')).getvalue()
    img_price = BytesIO(fig_price.to_image(format='png')).getvalue()
    return render_template('index.html', 
                           tabla_resumen=dataSummary.to_html(classes='table table-striped', index=False), 
                           img_pie=img_pie, 
                           img_rank=img_rank, 
                           img_price=img_price)

if __name__ == '__main__':
    app.run(debug=True)