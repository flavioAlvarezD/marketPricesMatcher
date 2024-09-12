from flask import Flask, render_template, request, redirect, url_for
import plotly.graph_objects as go
import os
from io import BytesIO
import base64
import pandas as pd

app = Flask(__name__)

# Configurar la carpeta de subida de archivos
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

GENERATED_FOLDER = 'generatedFiles'
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER

for existingFile in os.listdir(app.config['GENERATED_FOLDER']):
    os.remove(os.path.join(app.config['GENERATED_FOLDER'], existingFile))


# Definir el filtro b64encode
def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

# Registrar el filtro en la aplicación Flask
app.jinja_env.filters['b64encode'] = b64encode

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No se ha subido ningún archivo"
        
        file = request.files['file']

        if file.filename == '':
            return "Nombre de archivo vacío"

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded.xlsx')

            file.save(filepath)

            # Ejecutar el script de análisis de datos
            from dataCleansing import dataSummary

            # Generar gráficos solo si los datos están disponibles
            try:
                counts = dataSummary['didWeWon'].value_counts()
                labels = ['Perdedor', 'Ganador']
                sizes = counts
                colors = ['cornflowerblue', 'gold']
                fig_pie = go.Figure(data=[go.Pie(labels=labels, values=sizes)])
                fig_pie.update_traces(textfont_size=20, marker=dict(colors=colors, line=dict(color='#000000', width=2)))

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
            except KeyError:
                # Si los datos no están disponibles, asigna `None`
                img_pie = None
                img_rank = None
                img_price = None

            for existingFile in os.listdir(app.config['UPLOAD_FOLDER']):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], existingFile))

            return render_template('index.html', 
                                   tabla_resumen=dataSummary.to_html(classes='table table-striped', index=False), 
                                   img_pie=img_pie, 
                                   img_rank=img_rank, 
                                   img_price=img_price)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
