from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ================= HOME =================
@app.route('/')
def index():

    conn = get_connection()

    anuncios = conn.execute("""
        SELECT * FROM anuncios
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template('index.html', anuncios=anuncios)


# ================= CREATE =================
@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        anunciante = request.form['anunciante']
        titulo = request.form['titulo']
        preco = request.form['preco']
        descricao = request.form['descricao']

        whatsapp = request.form['contato']
        whatsapp_link = f"https://wa.me/55{whatsapp}"

        # 🔥 validação da imagem (obrigatória)
        if 'imagem' not in request.files:
            return "Imagem obrigatória", 400

        file = request.files['imagem']

        if file.filename == '':
            return "Imagem obrigatória", 400

        filename = secure_filename(file.filename)

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        image_url = f"static/uploads/{filename}"

        conn = get_connection()

        conn.execute("""
            INSERT INTO anuncios (anunciante, titulo, descricao, preco, whatsapp, imagem)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (anunciante, titulo, descricao, preco, whatsapp_link, image_url))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)