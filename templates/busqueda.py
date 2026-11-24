from flask import Flask, render_template, request

app = Flask(__name__)

import pandas as pd
import os

ARCHIVO_EXCEL="alumnos.xlsx"

@app.route("/")
def formulario():
    return render_template("formulario.html")

@app.route("/buscar", methods=["POST"])
def buscar():

    dato=request.form["dato"].strip()

    if not os.path.exists("ARCHIVO_EXCEL"):
        return render_template(
            "formulario.html",
            mensaje="El archivo de Excel no existe"
        )

    df=pd.read_excel(ARCHIVO_EXCEL)

    resultado=df[
        df["Id"].astype(str).str.strip()==dato
    ]

    if resultado.empty:
        return render_template("formulario.html", mensaje="No se encotro ningun registro."
        )

    informacion=resultado.iloc[0].to_dict()

    return render_template(
        "formulario.html",
        informacion=informacion
    )

if __name__ == "__main__":
    app.run(debug=True)






