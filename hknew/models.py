import json
import os
import platform
from pathlib import Path

import tomlkit
import typer
from tomlkit import parse


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


def caminho_config():
    sistema = platform.system()

    if sistema == "Linux":
        return Path.home() / ".config" / "hknew"

    if sistema == "Windows":
        appdata = os.getenv("APPDATA")

        if appdata is None:
            raise RuntimeError("APPDATA não está disponível.")

        return Path(appdata) / "hknew"

    raise RuntimeError("Sistema operacional não suportado.")

def carregar_configuracoes() -> dict:
    config = caminho_config()
    config = config / 'config.json'
    with open(config, 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
        return dados


def listar_predefinicoes():
    vereficar_integride()
    from hknew.idioma import carregar_idioma

    idioma = carregar_idioma()
    caminho = caminho_config() / 'presets'

    if not caminho.exists() or not caminho.is_dir():
        typer.echo(f'{idioma["arquivos_funcao"]["models"]["listar_predefinicoes"]["caminho_nao_encontrado"]}')
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
    from .idioma import criar_idioma_padrao

    caminho = caminho_config()
    presets = caminho / "presets"
    languages = caminho / "languages"

    caminho.mkdir(parents=True, exist_ok=True)
    presets.mkdir(exist_ok=True)
    languages.mkdir(exist_ok=True)

    arquivo_config = caminho / "config.json"
    preset_default = presets / "default.toml"

    config_basica_json = {
        "language": "pt_br"
    }

    with open(arquivo_config, "w", encoding="utf-8") as arq:
        json.dump(config_basica_json, arq, indent=4)

    with open(preset_default, "w", encoding="utf-8") as arq:
        arq.write(config_default_toml)

    criar_idioma_padrao()

def carregar_predefinicao(caminho: Path):
    conteudo = caminho.read_text(encoding='utf-8')
    return parse(conteudo)


def vereficar_toml():
    caminho = caminho_config()
    path = caminho / "presets" / "default.toml"

    if not path.exists():
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            dados = tomlkit.load(f)

        dados_padrao = tomlkit.parse(config_default_toml)

    except():
        return False

    return dados == dados_padrao


def verificar_config():
    caminho = caminho_config()
    arquivo = caminho / "config.json"

    if not arquivo.exists():
        return False

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (json.JSONDecodeError, OSError):
        return False

    if not isinstance(config, dict):
        return False

    config_padrao = {
        "language": "pt_br"
    }

    if set(config) != set(config_padrao):
        return False

    if not isinstance(config["language"], str):
        return False

    if not config["language"]:
        return False

    return True


def vereficar_integride():
    from .idioma import analisar_escolhido, analisar_padrao

    caminho = caminho_config()

    presets = caminho / "presets"
    languages = caminho / "languages"
    config = caminho / "config.json"
    toml = presets / "default.toml"
    idioma_padrao = languages / "pt_br.json"

    # 1. Bootstrap da estrutura
    if not caminho.exists():
        criar_configuracoes()
        return

    if not presets.exists():
        criar_configuracoes()
        return

    if not languages.exists():
        criar_configuracoes()
        return

    if not config.exists():
        criar_configuracoes()
        return

    if not toml.exists():
        criar_configuracoes()
        return

    if not idioma_padrao.exists():
        criar_configuracoes()
        return

    # 2. Validar config
    if not verificar_config():
        criar_configuracoes()
        return

    # 3. Descobrir idioma escolhido
    configs = carregar_configuracoes()

    idioma_escolhido_path = (
        languages / f'{configs["language"]}.json'
    )

    # 4. Idioma escolhido não existe → pt_br
    if not idioma_escolhido_path.exists():
        configs["language"] = "pt_br"

        with open(config, "w", encoding="utf-8") as f:
            json.dump(configs, f, indent=4)

        idioma_escolhido_path = idioma_padrao

    # 5. Validar arquivos
    if not vereficar_toml():
        criar_configuracoes()
        return

    if not analisar_padrao():
        criar_configuracoes()
        return

    if not analisar_escolhido():
        criar_configuracoes()
        return
