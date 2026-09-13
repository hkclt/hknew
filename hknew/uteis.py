import typer


def opcoes_limit3(opcoes):

    for i, opcao in enumerate(opcoes):
        typer.echo(f'({i + 1}). {opcao}')

    escolha = typer.prompt('escolha uma opcão').strip()
    try:
        escolha = int(escolha)
        escolha -= 1
    except ValueError:
        return 'Valor invalido, tente novamente'
    else:
        if 0 <= escolha <= 2:
            return escolha
        else:
            return 'Valor invalido, tente novamente'


def opcoes(opcoes):
    for i, opcao in enumerate(opcoes):
        typer.echo(f'({i + 1}). {opcao}')

    escolha = typer.prompt('Escolha uma opção').strip()
    try:
        escolha = int(escolha)
        escolha -= 1
    except ValueError:
        return 'Valor inválido, tente novamente'
    else:
        if 0 <= escolha < len(opcoes):
            return escolha
        else:
            return 'Valor inválido, tente novamente'


def opcoes_loop(opcoes):
    for i, opcao in enumerate(opcoes):
        typer.echo(f'({i + 1}). {opcao}')

    while True:
        escolha = typer.prompt('Escolha uma opção').strip()
        try:
            escolha = int(escolha)
            escolha -= 1
        except ValueError:
            typer.echo('Valor inválido, tente novamente')
        else:
            if 0 <= escolha < len(opcoes):
                typer.echo(f'Opção selecionada: {escolha}')
                return escolha
            else:
                typer.echo('Valor inválido, tente novamente')
