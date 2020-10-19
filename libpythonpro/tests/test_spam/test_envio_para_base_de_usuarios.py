from unittest.mock import Mock

import pytest

from libpythonpro.spam.enviador_de_email import Enviador
from libpythonpro.spam.main import EnviadorDeSpam
from libpythonpro.spam.modelos import Usuario


@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='Guilherme', email='gmartinsfilho@gmail.com'),
            Usuario(nome='Renzo', email='foo@foo.com.br')
        ],
        [
            Usuario(nome='Guilherme', email='gmartinsfilho@gmail.com')
        ]
    ]
)

def test_qde_de_spam(sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'guilherme@gmail.com',
        'Curso',
        'Confira os módulos'
    )
    assert len(usuarios) == enviador.enviar.call_count

class EnviadorMock(Enviador):
    def __init__(self):
        super().__init__()
        self.qtd_email_enviados = 0
        self.parametros_de_envio = None

    def enviar(self, remetente, destinatario, assunto, corpo):
        self.parametros_de_envio = (remetente, destinatario, assunto, corpo)
        self.qtd_email_enviados += 1

def test_parametros_de_spam(sessao):
    usuario = Usuario(nome='Guilherme', email='gmartinsfilho@gmail.com')
    sessao.salvar(usuario)
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'foo@foo.com',
        'Curso',
        'Confira os módulos'
    )
    enviador.enviar.assert_called_once_with(
        'foo@foo.com',
        'gmartinsfilho@gmail.com',
        'Curso',
        'Confira os módulos'
    )