import os
from dataclasses import dataclass
from pathlib import Path


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
        home = Path(os.getenv("REPERTORIO_HOME", root / "repertorio/.runtime")).resolve()
        return cls(root, home, int(os.getenv("REPERTORIO_PORT", "8766")))

    @property
    def url(self):
        return f"http://127.0.0.1:{self.port}"

    @property
    def db(self):
        return self.home / "library.sqlite3"
