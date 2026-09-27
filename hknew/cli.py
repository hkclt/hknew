import re

import typer

from hknew.idioma import carregar_idioma, criar_idioma, listar_idiomas, remover_idioma

from .criar import (
    adicionar_dependencias_toml,
    criar_pasta,
    criar_toml,
    criar_venv,
    instalar_dependencias,
    remover_dependencias_toml,
)
from .models import listar_predefinicoes, vereficar_integride
from .toml import gerar_toml
from .uteis import opcoes_loop

app = typer.Typer()
idioma_app = typer.Typer()
app.add_typer(idioma_app, name='idioma')

dados = {}


@app.command()
def main():
    """Create a new Python project."""
    typer.echo('HKNew 🚀')


@app.command()
def criar(project_name: str):
    vereficar_integride()
    idioma = carregar_idioma()
    while True:
        version = typer.prompt(
            idioma['cli']['create']['versao_mensagem'],
            default=idioma['cli']['create']['versao_padrao'],
        ).strip()

        if not version or not re.fullmatch(r'\d+(?:\.\d+)*', version):
            typer.echo(idioma['cli']['create']['versao_erro_modelo_errado'])
            version = idioma['cli']['create']['versao_padrao']

        dados['predefinicao'] = None
        dados['project_name'] = project_name
        dados['version'] = version

        dados['description'] = typer.prompt(
            idioma['cli']['create']['descricao_mensagem'],
            default=idioma['cli']['create']['descricao_padrao'],
        )

        dados['author'] = typer.prompt(
            idioma['cli']['create']['autor_mensagem'],
            default=idioma['cli']['create']['autor_padrao'],
        )

        dados['license'] = typer.prompt(
            idioma['cli']['create']['licenca_mensagem'],
            default=idioma['cli']['create']['licenca_padrao'],
        )

        dados['requires-python'] = typer.prompt(
            idioma['cli']['create']['versao_python_mensagem'],
            default=idioma['cli']['create']['versao_python_padrao'],
        )

        dados['readme'] = typer.prompt(
            idioma['cli']['create']['readme_mensagem'],
            default=idioma['cli']['create']['readme_padrao'],
        )

        while True:
            status = idioma['cli']['create']['status_opcoes']

            escolha = opcoes_loop(idioma['cli']['create']['opcoes_estilo_dependencias'])
            if escolha == 0:
                status['nenhuma'] = True

                typer.echo(idioma['cli']['create']['opcao_nenhuma_mensagem'])

                break

            elif escolha == 1:
                status['manual'] = True
                dados['dependencies'] = []

                mensagem = idioma['cli']['create']['opcao_manual_mensagem']

                while True:
                    dependencia = typer.prompt(
                        mensagem,
                        default='',
                    ).strip()

                    if not dependencia:
                        break

                    dados['dependencies'].append(dependencia)

                break

            elif escolha == 2:
                status['predefinicao'] = True

                nomes, caminhos = listar_predefinicoes()

                escolha = opcoes_loop(nomes)

                dados['predefinicao'] = caminhos[escolha]

                break

        resultado = gerar_toml(dados, status)

        typer.echo()
        typer.echo(f'╭── {idioma["cli"]["create"]["mensagem_pre_visualizacao"]} ──╮')
        typer.echo()
        typer.echo(resultado, nl=False)
        typer.echo()
        typer.echo('╰────────────────────────────────────────╯')
        typer.echo()

        confirmar = typer.confirm(idioma['cli']['create']['mensagem_confirmar_projeto'])

        if confirmar:
            certeza = typer.confirm(idioma['cli']['create']['mensagem_certeza'])

            if certeza:
                diretorio = criar_pasta(project_name)

                criar_toml(diretorio, resultado)

                criar_venv(diretorio)

                instalar_dependencias(diretorio)

                typer.echo(idioma['cli']['create']['mensagem_projeto_criado'])

                break

            typer.echo(idioma['cli']['create']['mensagem_criacao_cancelada'])
            continue

        repetir = typer.confirm(idioma['cli']['create']['mensagem_repetir_informacoes'])

        if repetir:
            continue

        typer.echo(idioma['cli']['create']['mensagem_criacao_abortada'])

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


@idioma_app.command('listar')
def listar():
    return listar_idiomas()


@idioma_app.command('criar')
def criar_idiomas():
    return criar_idioma()


@idioma_app.command('remover')
def remover_idiomas():
    return remover_idioma()
