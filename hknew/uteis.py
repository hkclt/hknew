import typer

from hknew.idioma import carregar_idioma
from hknew.models import vereficar_integride


def opcoes_limit3(opcoes):
    vereficar_integride()
    idioma = carregar_idioma()
    for i, opcao in enumerate(opcoes):
        typer.echo(f'({i + 1}). {opcao}')

    escolha = typer.prompt(idioma['arquivos_funcao']['uteis']['opcoes_limit3']['escolha_uma_opcao']).strip()
    try:
        escolha = int(escolha)
        escolha -= 1
    except ValueError:
        return idioma['arquivos_funcao']['uteis']['opcoes_limit3']['valor_invalido']
    else:
        if 0 <= escolha <= 2:
            return escolha
        else:
            return idioma['arquivos_funcao']['uteis']['opcoes_limit3']['valor_invalido']


def opcoes(opcoes):
    vereficar_integride()
    idioma = carregar_idioma()
    for i, opcao in enumerate(opcoes):
        typer.echo(f'({i + 1}). {opcao}')

    escolha = typer.prompt(idioma['arquivos_funcao']['uteis']['opcoes']['escolha_uma_opcao']).strip()
    try:
        escolha = int(escolha)
        escolha -= 1
    except ValueError:
        return idioma['arquivos_funcao']['uteis']['opcoes']['valor_invalido']
    else:
        if 0 <= escolha < len(opcoes):
            return escolha
        else:
            return idioma['arquivos_funcao']['uteis']['opcoes']['valor_invalido']


def opcoes_loop(opcoes):
    vereficar_integride()
    idioma = carregar_idioma()
    for i, opcao in enumerate(opcoes):
        typer.echo(f'({i + 1}). {opcao}')

    while True:
        escolha = typer.prompt(idioma['arquivos_funcao']['uteis']['opcoes_loop']['escolha_uma_opcao']).strip()
        try:
            escolha = int(escolha)
            escolha -= 1
        except ValueError:
            typer.echo(idioma['arquivos_funcao']['uteis']['opcoes_loop']['valor_invalido'])
        else:
            if 0 <= escolha < len(opcoes):
                return escolha
            else:
                typer.echo(idioma['arquivos_funcao']['uteis']['opcoes_loop']['valor_invalido'])
