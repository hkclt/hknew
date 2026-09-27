import json
from .models import caminho_config, carregar_configuracoes, vereficar_integride
import typer

pt_br = {
    "cli": {
        "create": {
            "versao_mensagem": "Versão",
            "versao_padrao": "0.1.0",
            "versao_erro_modelo_errado": "Valor inválido, será usado o padrão",
            "descricao_mensagem": "Descrição",
            "descricao_padrao": "Um lindo projeto Python",
            "autor_mensagem": "Autor",
            "autor_padrao": "Um cara inteligente",
            "licenca_mensagem": "Licença",
            "licenca_padrao": "MIT",
            "versao_python_mensagem": "Versão do Python",
            "versao_python_padrao": ">=3.10,<4.0",
            "readme_mensagem": "README",
            "readme_padrao": "README.md",
            "status_opcoes": {
                "nenhuma": False,
                "manual": False,
                "predefinicao": False,
            },
            "opcoes_estilo_dependencias": [
                "Nenhuma",
                "Manual",
                "Ver predefinições",
            ],
            "opcao_nenhuma_mensagem": "Nenhuma opção selecionada, continuando...",
            "opcao_manual_mensagem": "Digite as dependências do projeto (pressione Enter para finalizar):",
            "mensagem_pre_visualizacao": "Pré-visualização do pyproject.toml",
            "mensagem_confirmar_projeto": "Criar projeto?",
            "mensagem_certeza": "Tem certeza de que deseja criar o projeto?",
            "mensagem_projeto_criado": "Projeto criado com sucesso! 🚀",
            "mensagem_criacao_cancelada": "Criação cancelada.",
            "mensagem_repetir_informacoes": "Repetir informações?",
            "mensagem_criacao_abortada": "Abortado. Tchau, até o próximo projeto, seu pythonico! :)",
        }
    },
    "arquivos_funcao": {
        "criar": {
            "adicionar_dependencias_toml": {
                "mensagem_dependencia_ja_existe": "A dependência {dependencia} já existe",
                "erro_algo_deu_errado": "Algo deu errado, por favor, analise ou tente novamente",
                "mensagem_dependencias_instaladas": "Todas as novas dependências foram instaladas",
            },
            "remover_dependencias_toml": {
                "mensagem_erro": "Algo deu errado, por favor, analise ou tente novamente",
                "mensagem_dependencia_nao_registrada": "A dependência {dependencia} não está registrada no projeto",
                "mensagem_todas_dependencias_removidas": "Todas as dependências escolhidas foram desinstaladas",
            },
            "pegar_python_venv": {
                "mensagem_sistema_invalido": "Sistema inválido, suporte não desenvolvido. Abra uma issue no GitHub",
                "ambiente_virtual_nao_encontrado": "Python do ambiente virtual não encontrado: {python}",
            },
        },
        "models": {
            "caminho_config": {
                "mensagem_erro_appdata_nao_existe": "APPDATA não existe",
                "sistema_sem_suporte": "Sistema não suportado. Abra uma issue no GitHub.",
            },
            "listar_predefinicoes": {
                "caminho_nao_encontrado": "Caminho das predefinições {caminho} não encontrado ou não é um diretório.",
            },
        },
        "uteis": {
            "opcoes_limit3": {
                "escolha_uma_opcao": "Escolha uma opção",
                "valor_invalido": "Valor inválido, tente novamente",
            },
            "opcoes": {
                "escolha_uma_opcao": "Escolha uma opção",
                "valor_invalido": "Valor inválido, tente novamente",
            },
            "opcoes_loop": {
                "escolha_uma_opcao": "Escolha uma opção",
                "valor_invalido": "Valor inválido, tente novamente",
            },
        },
        "idioma": {
            "criar_idioma_padrao": 
                {
                    "padrao_existe": "pacote idioma padrão ja existe"
                    },
            "remover_idioma": 
                {
                    "pergunta_nome_arquivo": "Nome do arquivo: ",
                "impossivel_remover_idioma": "Não é possível remover o idioma atual.",
                "idioma_nao_encotrado": "Idioma não encontrado.",
                "idioma_removido": "removido"
                },
            "criar_idioma": 
                {
                    "pergunta_nome_arquivo": "Nome do arquivo: ",
                    "idioma_ja_existe": "Ja existe um idioma com esse nome.",
                    "confirmar": "confirmar?",
                    "idioma_criado": "idioma criado"
                    },
        },
    }
}


def criar_idioma_padrao():
    dados = pt_br
    caminho = caminho_config()
    caminho = caminho / "languages" / "pt_br.json"
    with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)


def analisar_padrao():
    caminho = caminho_config()
    caminho = caminho / "languages" / "pt_br.json"
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        if dados == pt_br:
            return True
        else:
            return False


def analisar(dados, pt_br):
    for chave, valor in dados.items():
        if len(dados) != len(pt_br):
            return False

        if chave not in pt_br:
            return False

        valor_padrao = pt_br[chave]

        if isinstance(valor, dict):
            if not isinstance(valor_padrao, dict):
                return False

            if not analisar(valor, valor_padrao):
                return False
    return True


def analisar_escolhido():
    caminho = caminho_config()
    caminho = caminho / "languages"
    config = carregar_configuracoes()
    idioma_escolhido = config["language"]
    idioma = caminho / f"{idioma_escolhido}.json"
    if idioma.exists():
        with open(idioma, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return analisar(dados, pt_br)
    else:
        return False


def carregar_idioma():

    caminho = caminho_config()
    configs = carregar_configuracoes()
    caminho = caminho / "languages" / f"{configs['language']}.json"
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        return dados


def listar_idiomas():
    config = caminho_config()
    pasta = config / "languages"
    lista = 1
    for arquivo in pasta.glob("*.json"):
        typer.echo(f"{lista}{arquivo.stem}")


def criar_idioma():
    vereficar_integride()
    idioma = carregar_idioma()
    nome_idioma = typer.prompt(idioma["arquivos_funcao"]["idioma"]["criar_idioma"]["pergunta_nome_arquivo"])
    caminho = caminho_config() / "languages" / f"{nome_idioma}.json"
    if caminho.exists():
        typer.echo(idioma["arquivos_funcao"]["idioma"]["criar_idioma"]["idioma_ja_existe"])
        return
    else:
        novo_idioma = {}

        def preencher(base, destino):
            for chave, valor in base.items():
                if isinstance(valor, dict):
                    destino[chave] = {}
                    preencher(valor, destino[chave])
                else:
                    destino[chave] = input(f"{chave}: ")

        preencher(pt_br, novo_idioma)

    print("\nPreview:")
    print(json.dumps(novo_idioma, indent=4, ensure_ascii=False))
    confirmar = typer.confirm(idioma["arquivos_funcao"]["idioma"]["criar_idioma"]["confirmar"])
    if confirmar:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(novo_idioma, f, ensure_ascii=False, indent=4)

        return idioma["arquivos_funcao"]["idioma"]["criar_idioma"]["idioma_criado"]


def remover_idioma():
    pasta_idiomas = caminho_config() / "languages"

    with open(caminho_config() / "config.json", encoding="utf-8") as arquivo:
        config = json.load(arquivo)

    idioma_atual = config["language"]

    nome_arquivo = typer.prompt(pt_br["arquivos_funcao"]["idioma"]["remover_idioma"]["pergunta_nome_arquivo"])

    if not nome_arquivo.endswith(".json"):
        nome_arquivo += ".json"

    arquivo = pasta_idiomas / nome_arquivo

    if arquivo.stem == idioma_atual:
        typer.echo(pt_br["arquivos_funcao"]["idioma"]["remover_idioma"]["impossivel_remover_idioma"])
        return

    if not arquivo.exists():
        typer.echo(pt_br["arquivos_funcao"]["idioma"]["remover_idioma"]["idioma_nao_encotrado"])
        return

    arquivo.unlink()

    typer.echo(f'{arquivo.stem} {pt_br["arquivos_funcao"]["idioma"]["remover_idioma"]["idioma_removido"]}')
