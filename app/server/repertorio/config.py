import os
import sys
from dataclasses import dataclass
from pathlib import Path


def user_data_dir():
    """Pasta de dados do usuário em cada sistema, fora da pasta do programa."""
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/Repertorio"
    if sys.platform == "win32":
        return Path(os.getenv("LOCALAPPDATA") or Path.home() / "AppData/Local") / "Repertorio"
    return Path(os.getenv("XDG_DATA_HOME") or Path.home() / ".local/share") / "repertorio"


def default_home(root):
    """A biblioteca fica na pasta de dados do usuário: atualizar ou apagar a pasta do programa não a afeta.
    Instalações anteriores, com a biblioteca em app/.runtime, continuam usando essa pasta."""
    legacy = root / "app/.runtime"
    return legacy if (legacy / "library.sqlite3").exists() else user_data_dir()


@dataclass(frozen=True)
class Settings:
    root: Path
    home: Path
    port: int = 8766

    def __post_init__(self):
        object.__setattr__(self,'root',Path(self.root).expanduser().resolve())
        object.__setattr__(self,'home',Path(self.home).expanduser().resolve())

    @classmethod
    def load(cls):
        root = Path(os.getenv("REPERTORIO_ROOT", Path(__file__).resolve().parents[3])).resolve()
        home = Path(os.getenv("REPERTORIO_HOME") or default_home(root)).resolve()
        return cls(root, home, int(os.getenv("REPERTORIO_PORT", "8766")))

    @property
    def url(self):
        return f"http://127.0.0.1:{self.port}"

    @property
    def db(self):
        return self.home / "library.sqlite3"
