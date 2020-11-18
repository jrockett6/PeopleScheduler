from typing import List, Set, Dict

class Team():
    def __init__(self, name: str) -> None:
        self._name = name
        self._timesteps_busy = 0

    def __repr__(self) -> str:
        return self._name

    def timestep(self):
        self._timesteps_busy -= 1
        self._timesteps_busy = max(0, self._timesteps_busy)

    def __eq__(self, o: object) -> bool:
        try:
            if (self._name == o._name):
                return True
            return False
        except:
            return False

