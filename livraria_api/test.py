import unittest
from app import create_app, db
from app.models.models import Livro


class TestLivrariaAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = create_app()


        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.client = app.test_client()
        # Cria o contexto de aplicação
        with app.app_context():
            db.create_all()
            # Adiciona um livro de exemplo
            #livro = Livro(titulo="Livro de Teste", ano_publicacao=2024, autor="Morrice")
            #db.session.add(livro)
            db.session.commit()

    #@classmethod
    #def tearDownClass(cls):
    #    #db.session.remove()
    #    #db.session.close()     
    #    db.drop_all()

    def test_get_livros(self):
        response = self.client.get('/livros/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

    def test_add_livro(self):
        novo_livro = {
            "id":1,
            "titulo": "Titulo de livro teste",
            "autor":"Seu Jorge",
            "ano_publicacao":2023,
        }
        response = self.client.post("/livros/", json=novo_livro)
        self.assertEqual(response.status_code, 201)


    def test_update_livro(self):
        update_data = {
            "titulo": "Livro Atualizado"
        }
        response = self.client.put(f'/livros/update/1', json=update_data)
        print(f'Resposta UPDATE: {response.status_code}')
        self.assertEqual(response.status_code, 200)
        


    def test_delete_livro(self):
        response = self.client.delete('/livros/delete/1')
        self.assertEqual(response.status_code, 200)
        print(f'Resposta Rota DELETAR Livros{response}')


if __name__ == '__main__':
    unittest.main()