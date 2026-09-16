import platform
from pathlib import Path
import subprocess
import sys
import tomlkit
import typer
from tomlkit import load
import venv


def pegar_python_venv(diretorio: Path) -> Path:
    sistema = platform.system()
    venv_dir = diretorio / '.venv'

    if sistema == 'Linux':
        python = venv_dir / 'bin' / 'python'
    elif sistema == 'Windows':
        python = venv_dir / 'Scripts' / 'python.exe'
    else:
        typer.echo(
            'Sistema invalido, suporte nao desenvolvido, '
            'abra uma issue no github'
        )
        raise typer.Exit(code=1)

    if not python.exists():
        raise FileNotFoundError(
            f'Python do ambiente virtual nao encontrado: {python}'
        )

    return python



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
    python = pegar_python_venv(caminho_projeto)

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
    python = pegar_python_venv(Path.cwd())
    resultado = subprocess.run([python, '-m', 'pip', 'install', dependencia], check=False)
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
    python = pegar_python_venv(Path.cwd())
    resultado = subprocess.run([python, '-m', 'pip', 'uninstall', dependencia], check=False)
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


def encontrar_toml():
    caminho = Path.cwd()
    while True:
        antigo_caminho = caminho
        procura = caminho / 'pyproject.toml'
        if procura.exists():
            return procura
        caminho = caminho.parent
        if caminho == antigo_caminho:
            return None

