from pathlib import Path
from sys import executable
import subprocess
import venv


def criar_pasta(nome: str) -> Path:
    caminho = Path.cwd() / nome

    caminho.mkdir(parents=True, exist_ok=False)

    return caminho


def criar_toml(diretorio: Path, dados: str) -> Path:
    arquivo = diretorio / "pyproject.toml"

    arquivo.write_text(
        dados,
        encoding="utf-8",
    )

    return arquivo


def criar_venv(diretorio: Path) -> Path:
    venv_dir = diretorio / ".venv"

    venv.create(
        venv_dir,
        with_pip=True,
    )

    return venv_dir


def instalar_dependencias(caminho_projeto: Path):
    python = caminho_projeto / ".venv" / "bin" / "python"

    subprocess.run(
        [
            python,
            "-m",
            "pip",
            "install",
            ".",
        ],
        cwd=caminho_projeto,
        check=True,
    )
