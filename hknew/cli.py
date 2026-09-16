import re
from pathlib import Path
import typer
from .criar import (
    criar_pasta,
    criar_toml,
    criar_venv,
    instalar_dependencias,
    adicionar_dependencias_toml,
    remover_dependencias_toml,
)
from .models import (
    criar_configuracoes,
    listar_predefinicoes,
)
from .toml import gerar_toml
from .uteis import opcoes, opcoes_loop


app = typer.Typer()

dados = {}


@app.command()
def main():
    """Create a new Python project."""
    typer.echo('HKNew 🚀')


@app.command()
def criar(project_name: str):
    criar_configuracoes()
    num_2 = 2

    while True:
        version = typer.prompt(
            'Versão',
            default='0.1.0',
        ).strip()

        if not version or not re.fullmatch(r'\d+(?:\.\d+)*', version):
            typer.echo('Valor inválido, virará o padrão')
            version = '0.1.0'

        dados['predefinicao'] = None
        dados['project_name'] = project_name
        dados['version'] = version

        dados['description'] = typer.prompt(
            'Descrição',
            default='Um lindo projeto python',
        )

        dados['author'] = typer.prompt(
            'Author',
            default='Um cara inteligente',
        )

        dados['license'] = typer.prompt(
            'Licença',
            default='MIT',
        )

        dados['requires-python'] = typer.prompt(
            'Versão do Python',
            default='>=3.10,<4.0',
        )

        dados['readme'] = typer.prompt(
            'Readme',
            default='README.md',
        )

        while True:
            status = {
                'nenhuma': False,
                'manual': False,
                'predefinicao': False,
            }

            escolha = opcoes_loop(['Nenhuma', 'Manual', 'Ver predefinições'])
            if escolha == 0:
                status['nenhuma'] = True

                typer.echo('Nenhuma opção selecionada, continuando...')

                break

            elif escolha == 1:
                status['manual'] = True
                dados['dependencies'] = []

                mensagem = 'Digite as dependências do projeto (pressione Enter para finalizar):'

                while True:
                    dependencia = typer.prompt(
                        mensagem,
                        default='',
                    ).strip()

                    if not dependencia:
                        break

                    dados['dependencies'].append(dependencia)

                break

            elif escolha == num_2:
                status['predefinicao'] = True

                nomes, caminhos = listar_predefinicoes()

                escolha = opcoes_loop(nomes)

                dados['predefinicao'] = caminhos[escolha]

                break

        resultado = gerar_toml(dados, status)

        typer.echo()
        typer.echo('╭── Pré-visualização do pyproject.toml ──╮')
        typer.echo()
        typer.echo(resultado, nl=False)
        typer.echo()
        typer.echo('╰────────────────────────────────────────╯')
        typer.echo()

        confirmar = typer.confirm('Criar projeto?')

        if confirmar:
            certeza = typer.confirm('Tem certeza que deseja criar o projeto?')

            if certeza:
                diretorio = criar_pasta(project_name)

                criar_toml(diretorio, resultado)

                criar_venv(diretorio)

                instalar_dependencias(diretorio)

                typer.echo('Projeto criado com sucesso! 🚀')

                break

            typer.echo('Criação cancelada.')
            continue

        repetir = typer.confirm('Repetir informações?')

        if repetir:
            continue

        typer.echo('Abortado, Tchau até o próximo projeto seu pythonico :)')

        break


"""@app.command()
def configurar():

    opcoes_config = [
        'Ver configurações',
        'Alterar caminho das predefinições',
    ]

    escolha = opcoes_loop(opcoes_config)

    if escolha == 0:
        configuracoes = carregar_configuracoes()

        typer.echo(f'Configurações atuais: {configuracoes}')
"""


@app.command()
def adicionar(dependencias: list[str]):
    return adicionar_dependencias_toml(*dependencias)


@app.command()
def remover(dependencias: list[str]):
    return remover_dependencias_toml(*dependencias)
