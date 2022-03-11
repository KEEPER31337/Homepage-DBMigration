
def logDuplicatedColumnAdded(err: Exception,
                             className: str,
                             methodName: str) -> None:
    print(f"{err} : This column is already added. From {className}.{methodName}.")


class UtilException(Exception):
    className: str
    methodName: str

    def __init__(self, className: str, methodName: str) -> None:
        self.className = className
        self.methodName = methodName

    def getSourceClassMethodName(self):
        return f"{self.className}.{self.methodName}"


class ParentSrlEqualError(UtilException):
    parentSrl: int
    rowSrl: int

    def __init__(self,
                 className: str,
                 methodName: str,
                 parentSrl: int,
                 rowSrl: int) -> None:
        super().__init__(className,methodName)
        self.parentSrl = parentSrl
        self.rowSrl = rowSrl

    def __str__(self) -> str:
        return(
            f"Parent srl {self.parentSrl} and this row srl {self.rowSrl} is equal!"
            " To avoid infinite loop, return and set parent srl 0."
            f" From {self.getSourceClassMethodName()}.")


class ParentSrlNotFoundError(UtilException):
    parentSrl: int

    def __init__(self,
                 className: str,
                 methodName: str,
                 parentSrl: int) -> None:
        super().__init__(className,methodName)
        self.parentSrl = parentSrl

    def __str__(self) -> str:
        return (f"Parent srl {self.parentSrl} not found..."
                " Return and set parent srl 0."
                f" From {self.getSourceClassMethodName()}.")
