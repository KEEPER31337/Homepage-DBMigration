
def logDuplicatedColumnAdded(err: Exception,
                             className: str,
                             methodName: str) -> None:
    print(f"{err} : This column is already added. From {className}.{methodName}.")
