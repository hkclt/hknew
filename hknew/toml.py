from tomlkit import document, table, dumps
from .models import carregar_predefinicao, mesclar_toml

toml = document()


def gerar_toml(dados, status):
    project = table()
    toml['project'] = project
    project['name'] = dados['project_name']
    project['version'] = dados['version']
    project['description'] = dados['description']
    project['authors'] = [{'name': dados['author']}]
    project['license'] = dados['license']
    project['requires-python'] = dados['requires-python']
    project['readme'] = dados['readme']

    if status['nenhuma']:
        pass
    if status['manual']:
        project['dependencies'] = dados['dependencies']
    if status['predefinicao']:
        predefinicao = carregar_predefinicao(dados['predefinicao'])
        mesclar_toml(toml, predefinicao)
    return dumps(toml)
