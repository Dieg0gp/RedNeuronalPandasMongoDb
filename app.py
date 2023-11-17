from flask import Flask, render_template
import pymongo
import pandas as pd

app = Flask(__name__)

# Configura la conexión a tu base de datos MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://diegogupa:rRWKGNvUeWeMKJng@cluster0.kjtpgpi.mongodb.net/")
db = client["Prueba1"]
collection = db["usuarios"]

@app.route('/')
def index():
    
    # Recupera los datos de MongoDB y conviértelos a un DataFrame de pandas
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))

    # Convierte la columna 'hora' a formato datetime
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S', errors='coerce')

    # Extrae la hora de cada entrada
    df['hora'] = df['hora'].dt.hour

    # Elimina filas con valores nulos
    df = df.dropna(subset=['hora'])

    # Agrupa por hora y cuenta la cantidad de registros
    horas_activas = df['hora'].value_counts().sort_index()

    # Convierte el resultado a un DataFrame
    df_horas_activas = pd.DataFrame({'Hora': horas_activas.index, 'Cantidad': horas_activas.values})

    # Convierte el DataFrame a HTML
    table_html = df_horas_activas.to_html(classes='table table-striped')

    # Renderiza la plantilla HTML con los datos de la tabla
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run(debug=True)

    """  ---- Ver todas las tablas ----
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))

    # Convierte el DataFrame a HTML
    table_html = df.to_html(classes='table table-striped')
    """

    """ --- Para Ver por hora 
    # Recupera los datos de MongoDB y conviértelos a un DataFrame de pandas
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))

    # Convierte la columna 'hora' a formato datetime
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S', errors='coerce')

    # Extrae la hora de cada entrada
    df['hora'] = df['hora'].dt.hour

    # Elimina filas con valores nulos
    df = df.dropna(subset=['hora'])

    # Agrupa por rango de hora y cuenta la cantidad de registros
    bins = [0, 6, 12, 18, 24]  # Define los límites de los rangos de horas
    labels = ['0-6', '6-12', '12-18', '18-24']  # Etiquetas para los rangos
    df['rango_hora'] = pd.cut(df['hora'], bins=bins, labels=labels, include_lowest=True)

    # Agrupa por rango de hora y cuenta la cantidad de registros
    horas_activas = df['rango_hora'].value_counts().sort_index()

    # Convierte el resultado a un DataFrame
    df_horas_activas = pd.DataFrame({'Rango de Hora': horas_activas.index, 'Cantidad': horas_activas.values})

    # Convierte el DataFrame a HTML
    table_html = df_horas_activas.to_html(classes='table table-striped')

    # Renderiza la plantilla HTML con los datos de la tabla
    return render_template('index.html', table=table_html)
    """