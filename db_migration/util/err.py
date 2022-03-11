
def logDuplicatedColumnAdded(err: Exception,
                             className: str,
                             methodName: str) -> None:
    print(f"{err} : This column is already added. From {className}.{methodName}.")


class UtilError(Exception):
    className: str
    methodName: str
    msg: str

    def __init__(self,
                 className: str,
                 methodName: str,
                 msg: str) -> None:
        self.className = className
        self.methodName = methodName
        self.msg = f" {msg}"

    def getSourceClassMethodName(self):
        return f"{self.className}.{self.methodName}"


class UtilErrorLog(UtilError):
    err: Exception

    def __init__(self,
                 err: Exception,
                 className: str,
                 methodName: str,
                 msg:str) -> None:
        self.err = err
        super().__init__(className, methodName,msg)


class StringNotFoundErrorLog(UtilErrorLog):
    stringFound: str
    msg: str

    def __init__(self,
                 err: Exception,
                 className: str,
                 methodName: str,
                 stringFound: str = "",
                 msg: str = "") -> None:

        self.stringFound = stringFound

        super().__init__(err, className, methodName, msg)

    def __str__(self) -> str:
        return (f"{self.err} : {self.stringFound} string is not found."
                f"{self.msg}"
                f" From {self.getSourceClassMethodName()}.")


class ParentSrlEqualError(UtilError):
    parentSrl: int
    rowSrl: int

    def __init__(self,
                 className: str,
                 methodName: str,
                 parentSrl: int,
                 rowSrl: int,
                 msg: str = "") -> None:
        super().__init__(className, methodName,msg)
        self.parentSrl = parentSrl
        self.rowSrl = rowSrl

    def __str__(self) -> str:
        return(
            f"Parent srl {self.parentSrl} and this row srl {self.rowSrl} is equal!"
            f"{self.msg}"
            f" From {self.getSourceClassMethodName()}.")


class ParentSrlNotFoundError(UtilError):
    parentSrl: int

    def __init__(self,
                 className: str,
                 methodName: str,
                 parentSrl: int,
                 msg: str = "") -> None:
        super().__init__(className, methodName,msg)
        self.parentSrl = parentSrl

    def __str__(self) -> str:
        return (
            f"Parent srl {self.parentSrl} not found..."
            f"{self.msg}"
            f" From {self.getSourceClassMethodName()}.")
