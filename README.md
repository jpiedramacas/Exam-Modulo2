# Desarrollo de Aplicación Web con Flask en AWS

## Tabla de Contenidos
1. [Configuración del Entorno de Desarrollo](#1-configuración-del-entorno-de-desarrollo)
2. [Desarrollo de la Aplicación Web](#2-desarrollo-de-la-aplicación-web)
3. [Pruebas y Depuración](#3-pruebas-y-depuración)
4. [Distribución y Documentación](#4-distribución-y-documentación)
5. [Entrega](#entrega)

## 1. Configuración del Entorno de Desarrollo

### 1.1 Crear una Instancia EC2

1. **Crear una instancia EC2:**
    - Ve a **Servicios > EC2** y selecciona **Lanzar instancia**.
    - Elige la AMI de **Amazon Linux 2**.
    - Selecciona el tipo de instancia, **t2.micro**.
    - Crea un nuevo par de claves o usa uno existente y guarda el archivo `.pem`.
    - Configura el almacenamiento predeterminado y haz clic en **Revisar y lanzar**.

2. **Configurar grupos de seguridad:**
    - En **EC2 > Grupos de seguridad**.
    - Selecciona el grupo de seguridad asociado a tu instancia.
    - Añade una regla de entrada para permitir el tráfico en los puertos 8080, 5000 y 3306 (MySQL).

### 1.2 Conectarse a la Instancia EC2

1. **Desde un Cloud9 nos conectamos a nuestro EC2:**
    - Tenemos que tener el archivo `.pem` de nuestro EC2 en Cloud9.
    - Conéctate a la instancia usando SSH:
        ```sh
        chmod 400 archivo.pem
        ssh -i archivo.pem ec2-user@<tu-instancia-public-ip>
        ```

### 1.3 Instalar Python y Herramientas de Desarrollo

1. **Actualizar el sistema:**
    ```sh
    sudo yum update -y
    ```

2. **Instalar Python y pip:**
    ```sh
    sudo yum install python3 -y
    sudo yum install python3-pip -y
    ```

## 2. Desarrollo de la Aplicación Web

### 2.1 Instalación y Configuración de Flask

1. **Instalar Flask:**
    ```sh
    pip3 install Flask
    ```

2. **Crear la estructura del proyecto:**
    ```sh
    mkdir my_flask_app
    cd my_flask_app
    mkdir templates
    ```

3. **Crear el archivo `app.py`:**
    ```python
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
    ```

4. **Crear la plantilla `presentacion.html`:**
    ```html
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Examen del Modulo 2</title>
        <style>
            body {
                text-align: center;
                padding: 50px;
            }
        </style>
    </head>
    <body>
        <h1>Bienvenido</h1>
        <p>Para este examen 04/06/2024 es para mostrar el uso de Flask.</p>
        <p>Haga clic en el botón para ir al formulario:</p>
        <a href="/formulario"><button>Ir al Formulario</button></a>
    </body>
    </html>
    ```

5. **Crear la plantilla `formulario.html`:**
    ```html
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Formulario 002</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                font-family: Arial, sans-serif;
            }
            form {
                text-align: center;
                margin-top: 20px;
            }
            label {
                margin-bottom: 10px;
                display: block;
            }
            input {
                margin-bottom: 10px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                background-color: #007bff;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <form method="POST" action="/formulario">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required><br>
            <label for="apellido">Apellido:</label>
            <input type="text" id="apellido" name="apellido" required><br>
            <label for="edad">Edad:</label>
            <input type="number" id="edad" name="edad" required><br>
            <label for="altura">Altura:</label>
            <input type="number" id="altura" name="altura" required><br>
            <button type="submit">Enviar</button>
        </form>
    </body>
    </html>
    ```

### 2.2 Ejecutar la Aplicación

1. **Ejecutar la aplicación:**
    ```sh
    sudo python3 app.py
    ```

2. **Visitar la aplicación en tu navegador:**
    - Abre tu navegador y visita `http://<tu-instancia-public-ip>:8080/`.

## 3. Pruebas y Depuración

### 3.1 Desarrollo de Casos de Prueba

1. **Crear el archivo `test_app.py`:**
    ```python
    import unittest
    from app import app

    class TestApp(unittest.TestCase):

        def setUp(self):
            # Configurar la aplicación antes de cada prueba
            self.app = app.test_client()
            self.app.testing = True

        def test_presentacion(self):
            # Probar la página de presentación
            response = self.app.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bienvenido', response.data)

        def test_formulario(self):
            # Probar el formulario
            response = self.app.post('/formulario', data=dict(nombre='John', apellido='Doe', edad='30', altura='180'))
            self.assertIn(b'Nombre: John, Apellido: Doe, Edad: 30, Altura: 180', response.data)

        def test_ruta_invalida(self):
            # Probar una ruta no válida
            response = self.app.get('/ruta_invalida')
            self.assertEqual(response.status_code, 404)

    if __name__ == '__main__':
        unittest.main()
    ```

### 3.2 Ejecución de Pruebas

1. **Ejecutar las pruebas:**
    ```sh
    python3 test_app.py
    ```

## 4. Distribución y Documentación

### 4.1 Preparar para la Distribución

1. **Crear un archivo `requirements.txt`:**
    ```sh
    pip freeze > requirements.txt
    ```

2. **Crear un script de despliegue (`deploy.sh`):**
    ```sh
    #!/bin/bash
    source myenv/bin/activate
    pip install -r requirements.txt
    python app.py
    ```

### 4.2 Documentación Técnica

1. **Crear un archivo `README.md`:**
    ```markdown
    # Aplicación Flask

    ## Descripción
    Esta es una aplicación web simple construida con Flask. Incluye una ruta para mostrar un mensaje de bienvenida y un formulario para ingresar un nombre y registrar ese nombre en una base de datos MySQL.

    ## Requisitos
    - Python 3
    - Flask
    - PyMySQL

    ## Instalación
    1. Clona el repositorio:
        ```sh
        git clone <url-del-repositorio>
        cd <nombre-del-repositorio>
        ```
    2. Crea y activa un entorno virtual:
        ```sh
        python3 -m venv myenv
        source myenv/bin/activate
        ```
    3. Instala las dependencias:
        ```sh
        pip install -r requirements.txt
        ```

    ## Ejecución
    1. Ejecuta la aplicación:
        ```sh
        python app.py
        ```
    2. Visita la aplicación en tu navegador en `http://<tu-instancia

-public-ip>:8080/`.

    ## Pruebas
    1. Ejecuta los casos de prueba:
        ```sh
        python test_app.py
        ```

    ## Despliegue
    1. Usa el script de despliegue para preparar el entorno:
        ```sh
        ./deploy.sh
        ```

    ## Contribución
    1. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`).
    2. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`).
    3. Empuja la rama (`git push origin feature/nueva-caracteristica`).
    4. Abre un Pull Request.
    ```

## 5. Entrega

1. **Crea un repositorio en GitHub.**
2. **Agrega y sube los archivos al repositorio:**
    ```sh
    git init
    git add .
    git commit -m "Initial commit"
    git remote add origin <url-de-tu-repositorio>
    git push -u origin master
    ```
3. **Pega el enlace del repositorio en la entrega del examen.**

### Notas Adicionales

- Asegúrate de que tu base de datos RDS esté configurada para permitir conexiones desde la IP de tu instancia EC2.
- Añade configuraciones de seguridad adicionales según las mejores prácticas de AWS para proteger tu aplicación y base de datos.
- Incluye instrucciones claras en el README sobre cómo clonar y ejecutar tu proyecto para que otros desarrolladores puedan replicar tu entorno fácilmente.
