import json
from pathlib import Path
from re import A
import subprocess
import sys
import tomlkit
import typer
from tomlkit import parse, load


def caminho_config() -> Path:
    config_dir = Path.home() / '.config' / 'hknew'

    config_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    return config_dir / 'config.json'


def caminho_predefinicoes_padrao() -> Path:
    return Path(__file__).resolve().parent / 'predefinicoes'


def carregar_configuracoes() -> dict:
    config = caminho_config()

    try:
        with config.open('r', encoding='utf-8') as arquivo:
            return json.load(arquivo)

    except FileNotFoundError:
        typer.echo('Arquivo de configuração não encontrado. Usando configurações padrão.')

        return {'caminho_predefinicao': str(caminho_predefinicoes_padrao())}

    except json.JSONDecodeError:
        typer.echo('Erro ao decodificar o arquivo de configuração. Usando configurações padrão.')

        return {'caminho_predefinicao': str(caminho_predefinicoes_padrao())}


def alterar_caminho_predefinicoes(novo_caminho: str) -> None:
    configuracoes = carregar_configuracoes()

    configuracoes['caminho_predefinicao'] = novo_caminho

    with caminho_config().open('w', encoding='utf-8') as arquivo:
        json.dump(
            configuracoes,
            arquivo,
            indent=4,
        )


def caminho_predefinicoes() -> str:
    configuracoes = carregar_configuracoes()

    return configuracoes['caminho_predefinicao']


def listar_predefinicoes(caminho=None):
    if caminho is None:
        caminho = caminho_predefinicoes()

    predefinicoes_path = Path(caminho)

    if not predefinicoes_path.exists() or not predefinicoes_path.is_dir():
        typer.echo(f"Caminho das predefinições '{caminho}' não encontrado ou não é um diretório.")

        return [], []

    tomls = list(predefinicoes_path.glob('*.toml'))

    nomes = []
    caminhos = []

    for toml_file in tomls:
        nomes.append(toml_file.stem)
        caminhos.append(toml_file)

    return nomes, caminhos


def carregar_predefinicao(caminho: Path):
    conteudo = caminho.read_text(encoding='utf-8')

    return parse(conteudo)


def mesclar_toml(destino, origem):
    for chave, valor in origem.items():
        if chave == 'project':
            continue

        destino[chave] = valor
