from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

    def __str__(self):
        return f"[{self.line}:{self.column}] {self.type:12} '{self.value}'"