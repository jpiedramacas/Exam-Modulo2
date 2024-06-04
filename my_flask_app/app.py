from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def presentacion():
    return render_template('presentacion.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        altura = request.form['altura']
        return f'Nombre: {nombre}, Apellido: {apellido}, Edad: {edad}, Altura: {altura}'
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
