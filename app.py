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

    # Convierte el DataFrame a HTML
    table_html = df.to_html(classes='table table-striped')

    # Renderiza la plantilla HTML con los datos de la tabla
    return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run(debug=True)
