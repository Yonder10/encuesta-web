from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurar acceso a Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1-hCdyD-dzBvffK_p-vt4WzsumXiegvnE5Z9PHYgtf6A").sheet1

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta principal (muestra y procesa el formulario)
@app.route("/", methods=["GET", "POST"])
def encuesta():
    if request.method == "POST":
        nombre = request.form["nombre"].upper()
        correo = request.form["correo"].upper()
        edad = request.form["edad"]
        opinion = request.form["opinion"].upper()

        from datetime import datetime
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        fila = [nombre, correo, edad, opinion, fecha]
        sheet.append_row(fila)

        return render_template("form.html", mensaje="✅ ¡Gracias por responder!")
    
    return render_template("form.html")

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(debug=True)