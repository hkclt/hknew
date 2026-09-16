import os
from pathlib import Path
import typer
from tomlkit import parse
import platform
import json


def caminho_config():
    sistema = platform.system()
    if sistema == 'Linux':
        config_dir = Path.home() / '.config' / 'hknew'
    elif sistema == 'Windows':
        appdata = os.getenv('appdata')
        if appdata is None:
            raise RuntimeError('APPDATA não existe')
        else:
            config_dir = Path(appdata)
            config_dir = config_dir / 'hknew'
    else:
        raise RuntimeError(
        'Sistema não suportado. Abra uma issue no GitHub.'
    )
    return config_dir


def carregar_configuracoes() -> dict:
    config = caminho_config()
    config = config / 'config.json'
    with open(config, 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
        return dados


def listar_predefinicoes():
    caminho = caminho_config() / 'presets'

    if not caminho.exists() or not caminho.is_dir():
        typer.echo(
            f"Caminho das predefinições '{caminho}' "
            "não encontrado ou não é um diretório."
        )
        return [], []

    tomls = list(caminho.glob('*.toml'))

    nomes = []
    caminhos = []

    for toml_file in tomls:
        nomes.append(toml_file.stem)
        caminhos.append(toml_file)

    return nomes, caminhos


def mesclar_toml(destino, origem):
    for chave, valor in origem.items():
        if chave == 'project':
            continue

        destino[chave] = valor


def criar_configuracoes():
    caminho = caminho_config()
    presets = caminho / 'presets'
    arquivo_config = caminho / 'config.json'
    preset_default = presets / 'default.toml'
    config_basica_json = {'language': 'pt-BR'}
    config_default_toml = """
[project]
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.12.0",
]

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I"]

[tool.taskipy.tasks]
test = "pytest"
lint = "ruff check ."
format = "ruff format ."
    """
    caminho.mkdir(parents=True, exist_ok=True)
    (caminho / 'presets').mkdir(exist_ok=True)
    (caminho / 'languages').mkdir(exist_ok=True)
    if not arquivo_config.exists():
        with open(arquivo_config, 'w', encoding='utf-8') as arq:
            json.dump(config_basica_json, arq, indent=4)
    if not preset_default.exists():
        with open(preset_default, 'w', encoding='utf-8') as arq:
            arq.write(config_default_toml)


def carregar_predefinicao(caminho: Path):
    conteudo = caminho.read_text(encoding='utf-8')
    return parse(conteudo)
