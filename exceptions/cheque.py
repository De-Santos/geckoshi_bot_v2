from fastapi import HTTPException, status


class ChequeIsNotModifiable(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT, "Cheque is no longer modifiable")


class ChequeModificationForbidden(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "Cheque modification forbidden")
