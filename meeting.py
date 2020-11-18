from typing import List

class Meeting():
    def __init__(self, name: str, required_teams: List[str], duration: int, dependencies: List[str]):
        self._name = name
        self._duration = duration
        self._required_teams = set(required_teams)
        self._dependencies = set(dependencies)

    def __repr__(self) -> str:
        return self._name