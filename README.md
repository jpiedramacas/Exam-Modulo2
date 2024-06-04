# Desarrollo de Aplicación Web con Flask en AWS

## Tabla de Contenidos
1. [Configuración del Entorno de Desarrollo](#1-configuración-del-entorno-de-desarrollo)
2. [Desarrollo de la Aplicación Web](#2-desarrollo-de-la-aplicación-web)
3. [Pruebas y Depuración](#3-pruebas-y-depuración)
4. [Distribución y Documentación](#4-distribución-y-documentación)
5. [Entrega](#entrega)

## 1. Configuración del Entorno de Desarrollo

### 1.1 Crear una Instancia EC2
1. Inicia sesión en AWS Management Console.
2. Navega a **EC2 Dashboard** y selecciona **Launch Instance**.
3. Selecciona **Amazon Linux 2 AMI**.
4. Elige el tipo de instancia (t2.micro es suficiente para este ejercicio).
5. Configura los detalles de la instancia y el almacenamiento.
    - En **Instance Details**, puedes usar los valores predeterminados.
    - En **Add Storage**, puedes usar el almacenamiento predeterminado.
6. Configura el grupo de seguridad para permitir tráfico SSH (puerto 22) y HTTP (puerto 80):
    - Crea un nuevo grupo de seguridad.
    - Añade una regla para SSH con el puerto 22 y origen "My IP".
    - Añade una regla para HTTP con el puerto 80 y origen "Anywhere".
7. Revisa y lanza la instancia.
8. Descarga el archivo PEM para la clave SSH y guarda en un lugar seguro.

### 1.2 Conectarse a la Instancia EC2
1. Abre una terminal y navega a la ubicación donde guardaste el archivo PEM.
2. Conéctate a la instancia usando SSH:
    ```sh
    ssh -i "ruta/a/tu/clave.pem" ec2-user@<tu-instancia-public-ip>
    ```

### 1.3 Instalar Python y Git
1. Actualiza el paquete de la lista:
    ```sh
    sudo yum update -y
    ```
2. Instala Python y Git:
    ```sh
    sudo yum install python3 git -y
    ```
3. Verifica las instalaciones:
    ```sh
    python3 --version
    git --version
    ```

### 1.4 Configurar Cloud9
1. En AWS Management Console, navega a **Cloud9** y crea un nuevo entorno.
2. Configura el entorno para que se asocie con la instancia EC2 que creaste.
    - Selecciona **Create Environment**.
    - Proporciona un nombre y una descripción.
    - Elige **Connect with EC2** y selecciona la instancia EC2 que creaste.
3. Completa la configuración y abre el entorno Cloud9.
4. Configura el entorno para usar Python 3 por defecto:
    ```sh
    sudo alternatives --set python /usr/bin/python3
    ```

### 1.5 Configurar Seguridad
1. Configura las reglas del grupo de seguridad de la instancia para permitir solo los puertos necesarios (ej. 22 para SSH, 80 para HTTP).

## 2. Desarrollo de la Aplicación Web

### 2.1 Crear una Aplicación Flask Básica
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
5. Visita la aplicación en tu navegador utilizando la IP pública de tu instancia EC2.

### 2.2 Configurar Base de Datos (RDS)
1. En AWS Management Console, navega a **RDS** y crea una nueva base de datos MySQL.
2. Configura la base de datos con los siguientes detalles:
    - Engine type: MySQL.
    - Template: Free tier.
    - DB instance identifier: mydatabase.
    - Master username: admin.
    - Master password: <tu-contraseña>.
3. En **Additional configuration**, configura el nombre de la base de datos inicial.
4. Lanza la instancia de base de datos.
5. Asegúrate de que el grupo de seguridad de la base de datos permita conexiones desde la IP de tu instancia EC2.

### 2.3 Integrar la Base de Datos en Flask
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
3. Ejecuta la aplicación y verifica que los datos se registren en la base de datos.

### 2.4 Integrar Control de Versiones
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

## 3. Pruebas y Depuración

### 3.1 Desarrollar Casos de Prueba
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

### 3.2 Ejecutar Pruebas
1. Ejecuta las pruebas:
    ```sh
    python test_app.py
    ```

### 3.3 Depurar la Aplicación
1. Usa `print` para depurar el código si es necesario.
    ```python
    print("Valor de la variable:", variable)
    ```
2. Verifica los logs para identificar y corregir errores.

## 4. Distribución y Documentación

### 4.1 Preparar para la Distribución
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

### 4.2 Documentación Técnica
1. Documenta la aplicación, el diseño y la estructura de archivos en un archivo `README.md`.
2. Incluye instrucciones claras sobre cómo clonar y ejecutar el proyecto.

### 4.3 Ejemplo de Documentación Técnica
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
2. Visita la aplicación en tu navegador en `http://<tu-instancia-public-ip>`.

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
