from dataclasses import dataclass, field


@dataclass
class Plugin:

    name: str
    description: str = ""
    version: str = ""
    maintainer: str = ""
    loaded: bool = False
    dependencies: list[str] = field(default_factory=list[str])

    def load_str(self) -> str:
        return f"plugins.{self.name}.{self.name}"