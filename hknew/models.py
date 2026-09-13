import json
import typer
from pathlib import Path
from tomlkit import parse


def carregar_configuracoes():
    try:
        with open('hknew/config.json', 'r') as arquivo:
            configuracoes = json.load(arquivo)
            return configuracoes
    except FileNotFoundError:
        typer.echo('Arquivo de configuração não encontrado. Usando configurações padrão.')
        return {'caminho_predefinicao': './predefinicoes'}
    except json.JSONDecodeError:
        typer.echo('Erro ao decodificar o arquivo de configuração. Usando configurações padrão.')
        return {'caminho_predefinicao': './predefinicoes'}


def alterar_caminho_predefinicoes(novo_caminho):
    configuracoes = carregar_configuracoes()
    configuracoes['caminho_predefinicao'] = novo_caminho
    with open('hknew/config.json', 'w') as arquivo:
        json.dump(configuracoes, arquivo, indent=4)


def caminho_predefinicoes():
    with open('hknew/config.json', 'r') as arquivo:
        configuracoes = json.load(arquivo)
        caminho = configuracoes['caminho_predefinicao']
        return caminho


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
        nome = toml_file.stem

        nomes.append(nome)
        caminhos.append(toml_file)

    return nomes, caminhos


def carregar_predefinicao(caminho):
    conteudo = caminho.read_text(encoding='utf-8')
    return parse(conteudo)


def mesclar_toml(destino, origem):
    for chave, valor in origem.items():
        if chave == 'project':
            pass
        else:
            destino[chave] = valor
