from pathlib import Path
import subprocess
import sys
import tomlkit
import typer
from tomlkit import load
import venv


def criar_pasta(nome: str) -> Path:
    caminho = Path.cwd() / nome

    caminho.mkdir(parents=True, exist_ok=False)

    return caminho


def criar_toml(diretorio: Path, dados: str) -> Path:
    arquivo = diretorio / 'pyproject.toml'

    arquivo.write_text(
        dados,
        encoding='utf-8',
    )

    return arquivo


def criar_venv(diretorio: Path) -> Path:
    venv_dir = diretorio / '.venv'

    venv.create(
        venv_dir,
        with_pip=True,
    )

    return venv_dir


def instalar_dependencias(caminho_projeto: Path):
    python = caminho_projeto / '.venv' / 'bin' / 'python'

    subprocess.run(
        [
            python,
            '-m',
            'pip',
            'install',
            '.',
        ],
        cwd=caminho_projeto,
        check=True,
    )


def baixar_dependencia(dependencia):
    resultado = subprocess.run([sys.executable, '-m', 'pip', 'install', dependencia], check=False)
    if resultado.returncode == 0:
        return True
    else:
        return False


def adicionar_dependencias_toml(*dependencias):
    arquivo_toml = Path.cwd() / 'pyproject.toml'
    with open(arquivo_toml, 'r', encoding='utf-8') as f:
        dados = load(f)
        for dependencia in dependencias:
            if dependencia in dados['project']['dependencies']:
                typer.echo(f'A {dependencia} ja existe')
            else:
                baixado = baixar_dependencia(dependencia)
                if baixado:
                    dados['project']['dependencies'].append(dependencia)
                else:
                    return 'algo deu de errado, por favor analise ou tente novamente'
        typer.echo('Todas novas dependencias instaladas')
    with open(arquivo_toml, 'w', encoding='utf-8') as f:
        tomlkit.dump(dados, f)


def remover_dependencia(dependencia):
    resultado = subprocess.run([sys.executable, '-m', 'pip', 'uninstall', dependencia], check=False)
    if resultado.returncode == 0:
        return True
    else:
        return False


def remover_dependencias_toml(*dependencias):
    arquivo_toml = Path.cwd() / 'pyproject.toml'
    with open(arquivo_toml, 'r', encoding='utf-8') as f:
        dados = load(f)
        for dependencia in dependencias:
            if dependencia in dados['project']['dependencies']:
                remover = remover_dependencia(dependencia)
                if remover:
                    dados['project']['dependencies'].remove(dependencia)
                else:
                    return 'algo deu de errado, por favor analise ou tente novamente'
            else:
                typer.echo(f'A dependencia {dependencia} Nao esta registrada no projeto')
        typer.echo('Todas dependencias escolhidas desisntaladas')
    with open(arquivo_toml, 'w', encoding='utf-8') as f:
        tomlkit.dump(dados, f)
