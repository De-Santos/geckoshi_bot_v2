from fastapi import HTTPException, status


class ChequeIsNotModifiable(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT, "Cheque is no longer modifiable")


class ChequeModificationForbidden(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Cheque modification forbidden")


class ChequeForbidden(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Cheque forbidden")


class ChequeInactive(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_410_GONE, "Cheque inactive")


class MultipleChequeActivationForbidden(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Multiple cheque activation forbidden")


class InaccessibleChatInChequeRequirements(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Cheque has inaccessible chat in requirements")


class InvalidChequeData(HTTPException):
    def __init__(self, reason: str) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, f"Limits check failed: {reason}")
