class ObjectiveRegistry:
    def __init__(self):
        self._objectives = []

    def register(self, objective):
        self._objectives.append(objective)

    def all(self):
        return tuple(self._objectives)

    def names(self):
        return tuple(objective.name for objective in self._objectives)
