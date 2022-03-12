
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

    def getSourceClassMethod(self):
        return f" From {self.className}.{self.methodName}."

    def getErrorName(self):
        return f"{self.__class__.__name__}"


class ParentSrlEqualError(UtilError):
    parentSrl: int
    rowSrl: int

    def __init__(self,
                 className: str,
                 methodName: str,
                 parentSrl: int,
                 rowSrl: int,
                 msg: str = "") -> None:

        self.parentSrl = parentSrl
        self.rowSrl = rowSrl

        super().__init__(className, methodName, msg)

    def __str__(self) -> str:
        return(
            f"{self.getErrorName} : Parent srl {self.parentSrl} and this row srl {self.rowSrl} is equal!"
            f"{self.msg}"
            f"{self.getSourceClassMethod()}.")


class ParentSrlNotFoundError(UtilError):
    parentSrl: int

    def __init__(self,
                 className: str,
                 methodName: str,
                 parentSrl: int,
                 msg: str = "") -> None:
        super().__init__(className, methodName, msg)
        self.parentSrl = parentSrl

    def __str__(self) -> str:
        return (
            f"{self.getErrorName()} : Parent srl {self.parentSrl} not found..."
            f"{self.msg}"
            f"{self.getSourceClassMethod()}.")


class DataLenOverError(UtilError):
    def __str__(self) -> str:
        return (
            f"{self.getErrorName()} : Data is too long to insert into the table..."
            f"{self.msg}"
            f"{self.getSourceClassMethod()}.")


class UtilErrorLog(UtilError):
    err: Exception

    def __init__(self,
                 err: Exception,
                 className: str,
                 methodName: str,
                 msg: str) -> None:
        self.err = err
        super().__init__(className, methodName, msg)


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
                f"{self.getSourceClassMethod()}.")


class DuplicatedColumnExistErrorLog(UtilErrorLog):
    columnName: str

    def __init__(self,
                 err: Exception,
                 className: str,
                 methodName: str,
                 columnName: str = "",
                 msg: str = "") -> None:

        self.columnName = columnName

        super().__init__(err, className, methodName, msg)

    def __str__(self) -> str:
        return (f"{self.err} : Column {self.columnName} is already exist."
                f"{self.getSourceClassMethod()}")


class LxmlCleanerParseErrorLog(UtilErrorLog):
    def __str__(self) -> str:
        return (f"{self.err} : Lxml can't parse this content."
                f"{self.msg}"
                f" From {self.getSourceClassMethod()}")
