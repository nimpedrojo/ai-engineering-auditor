class AIEAError(Exception):
    """Base exception for AI Engineering Auditor."""


class ProjectNotInitialized(AIEAError):
    """Raised when the current project has not been initialized."""