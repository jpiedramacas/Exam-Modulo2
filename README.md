# README: Desarrollo de Aplicación Web con Flask en AWS

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
4. [Desarrollo de la Aplicación Web](#desarrollo-de-la-aplicación-web)
5. [Pruebas y Depuración](#pruebas-y-depuración)
6. [Distribución y Documentación](#distribución-y-documentación)
7. [Entrega](#entrega)

## Introducción
Este documento proporciona instrucciones paso a paso para configurar un entorno de desarrollo, desarrollar una aplicación web utilizando Flask, probar y depurar la aplicación, y preparar la aplicación para su distribución. El entorno se configura en una instancia EC2 de AWS, y se utiliza Python, Git y el IDE Cloud9.

## Requisitos Previos
Antes de comenzar, asegúrate de tener:
- Una cuenta activa de AWS.
- Conocimientos básicos de Python y Git.
- Permisos para crear instancias EC2 y recursos relacionados en AWS.

## Configuración del Entorno de Desarrollo

### 1. Crear una Instancia EC2
1. Inicia sesión en AWS Management Console.
2. Navega a **EC2 Dashboard** y selecciona **Launch Instance**.
3. Selecciona **Amazon Linux 2 AMI**.
4. Elige el tipo de instancia (t2.micro es suficiente para este ejercicio).
5. Configura los detalles de la instancia y el almacenamiento.
6. Configura el grupo de seguridad para permitir tráfico SSH (puerto 22) y HTTP (puerto 80).
7. Revisa y lanza la instancia.

### 2. Conectarse a la Instancia EC2
1. Conéctate a la instancia usando SSH:
    ```sh
    ssh -i "ruta/a/tu/clave.pem" ec2-user@<tu-instancia-public-ip>
    ```

### 3. Instalar Python y Git
1. Actualiza el paquete de la lista:
    ```sh
    sudo yum update -y
    ```
2. Instala Python y Git:
    ```sh
    sudo yum install python3 git -y
    ```

### 4. Configurar Cloud9
1. En AWS Management Console, navega a **Cloud9** y crea un nuevo entorno.
2. Asocia el entorno Cloud9 con tu instancia EC2.

### 5. Configurar Seguridad
1. Configura las reglas del grupo de seguridad de la instancia para permitir solo los puertos necesarios (ej. 22 para SSH, 80 para HTTP).

## Desarrollo de la Aplicación Web

### 1. Crear una Aplicación Flask Básica
1. Crea un entorno virtual:
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    ```
2. Instala Flask:
    ```sh
    pip install Flask
    ```
3. Crea el archivo `app.py`:
    ```python
    from flask import Flask, request, render_template

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Hola, mundo!"

    @app.route('/form', methods=['GET', 'POST'])
    def form():
        if request.method == 'POST':
            nombre = request.form['nombre']
            return f"Hola, {nombre}!"
        return '''
            <form method="post">
                Nombre: <input type="text" name="nombre"><br>
                <input type="submit" value="Enviar">
            </form>
        '''

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80)
    ```
4. Ejecuta la aplicación:
    ```sh
    python app.py
    ```

### 2. Configurar Base de Datos (RDS)
1. En AWS Management Console, navega a **RDS** y crea una nueva base de datos MySQL.
2. Conéctate a la base de datos desde tu instancia EC2 e inicializa la base de datos.

### 3. Integrar la Base de Datos en Flask
1. Instala `pymysql`:
    ```sh
    pip install pymysql
    ```
2. Modifica `app.py` para registrar datos en la base de datos:
    ```python
    import pymysql

    connection = pymysql.connect(host='tu-rds-endpoint',
                                 user='tu-usuario',
                                 password='tu-contraseña',
                                 db='tu-base-de-datos')

    @app.route('/form', methods=['GET', 'POST'])
    def form():
        if request.method == 'POST':
            nombre = request.form['nombre']
            with connection.cursor() as cursor:
                sql = "INSERT INTO usuarios (nombre) VALUES (%s)"
                cursor.execute(sql, (nombre,))
                connection.commit()
            return f"Hola, {nombre}!"
        return '''
            <form method="post">
                Nombre: <input type="text" name="nombre"><br>
                <input type="submit" value="Enviar">
            </form>
        '''
    ```

### 4. Integrar Control de Versiones
1. Inicializa un repositorio Git:
    ```sh
    git init
    ```
2. Añade los archivos al repositorio:
    ```sh
    git add .
    ```
3. Realiza un commit inicial:
    ```sh
    git commit -m "Initial commit"
    ```
4. Conecta el repositorio local con un repositorio remoto en GitHub:
    ```sh
    git remote add origin <url-del-repositorio-git>
    git push -u origin master
    ```

## Pruebas y Depuración

### 1. Desarrollar Casos de Prueba
1. Crea el archivo `test_app.py`:
    ```python
    import unittest
    from app import app

    class FlaskTestCase(unittest.TestCase):

        def test_home(self):
            tester = app.test_client(self)
            response = tester.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Hola, mundo!', response.data)

        def test_form_get(self):
            tester = app.test_client(self)
            response = tester.get('/form')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Nombre:', response.data)

    if __name__ == '__main__':
        unittest.main()
    ```

### 2. Ejecutar Pruebas
1. Ejecuta las pruebas:
    ```sh
    python test_app.py
    ```

### 3. Depurar la Aplicación
1. Usa `print` para depurar el código si es necesario.

## Distribución y Documentación

### 1. Preparar para la Distribución
1. Crea un archivo `requirements.txt`:
    ```sh
    pip freeze > requirements.txt
    ```
2. Crea un script de despliegue (`deploy.sh`):
    ```sh
    #!/bin/bash
    source myenv/bin/activate
    pip install -r requirements.txt
    python app.py
    ```

### 2. Documentación Técnica
1. Documenta la aplicación, el diseño y la estructura de archivos en un archivo `README.md`.

## Entrega

1. Crea un repositorio en GitHub.
2. Agrega y sube los archivos al repositorio:
    ```sh
    git init
    git add .
    git commit -m "Initial commit"
    git remote add origin <url-de-tu-repositorio>
    git push -u origin master
    ```
3. Pega el enlace del repositorio en la entrega del examen.

### Notas Adicionales
- Asegúrate de que tu base de datos RDS esté configurada para permitir conexiones desde la IP de tu instancia EC2.
- Añade configuraciones de seguridad adicionales según las mejores prácticas de AWS para proteger tu aplicación y base de datos.
- Incluye instrucciones claras en el README sobre cómo clonar y ejecutar tu proyecto para que otros desarrolladores puedan replicar tu entorno fácilmente.
