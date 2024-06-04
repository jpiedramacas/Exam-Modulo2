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

