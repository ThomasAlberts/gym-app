class DomainError(Exception):
    """Business-rule violation. The HTTP layer decides which status code it maps to."""


class UnknownExerciseDefinition(DomainError):
    def __init__(self, ids):
        self.ids = sorted(ids)
        super().__init__(f"exercise_definition_id(s) {self.ids} do not exist")


class InvalidWorkoutSession(DomainError):
    pass


class InvalidAiResponse(DomainError):
    pass

class AiGenerationFailed(Exception):
    """The AI provider call failed (network, quota, auth, etc.)."""


class EmptyCurrentExercises(Exception):
    """Suggestions requested without any current exercises."""