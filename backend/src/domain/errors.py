class DomainError(Exception):
    """Business-rule violation. The HTTP layer decides which status code it maps to."""


class UnknownExerciseDefinition(DomainError):
    def __init__(self, ids):
        self.ids = sorted(ids)
        super().__init__(f"exercise_definition_id(s) {self.ids} do not exist")


class InvalidWorkout(DomainError):
    pass


class InvalidAiResponse(DomainError):
    pass
