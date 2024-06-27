from dataclasses import dataclass

@dataclass
class Squadra:
    teamCode: str
    ID: int
    name: str
    salarioSquadra: float

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        return self.ID == other.ID

    def __str__(self):
        return f"{self.name}"