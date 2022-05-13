from util.typedef import Row
from module.library_migrators.library_migrator import LibraryMigrator


class BookMigrator(LibraryMigrator):

    __bookDepartmentDict: dict

    __insertBookFormat = ("INSERT INTO {newTableMigrate}(title,author,total,department)"
                          " VALUES(%(name)s,%(author)s,%(total)s,%(department)s);")

    def __init__(self,
                 oldTableMigrate: str = "books",
                 newTableMigrate: str = "book") -> None:

        self._insertLibraryFormat = self.__insertBookFormat
        self.__bookDepartmentDict = dict()
        super().__init__(oldTableMigrate, newTableMigrate)

    def addBookDepartment(self, oldDepartmentNumber: int, newDepartmentId: int) -> None:
        self.__bookDepartmentDict[oldDepartmentNumber] = newDepartmentId

    def migrateBook(self) -> None:
        self._migrateLibrary()

    def _getLibraryName(self, bookName: str) -> str:
        return self.__getBookName(bookName)

    def __getBookName(self, bookName: str) -> str:
        return bookName.strip()

    def __setBookDepartment(self, row: Row) -> Row:
        row["department"] = self.__parseBookDepartment(row["number"])
        return row

    def __parseBookDepartment(self, bookNumber: str) -> int:
        oldNumber = int(bookNumber[0])
        return self.__bookDepartmentDict[oldNumber]

    def _editLibraryRow(self, row: Row) -> Row:
        return self.__editBookRow(row)

    def __editBookRow(self, row: Row) -> Row:
        row = self._setNameTotalOnRow(row)
        row = self.__setBookDepartment(row)
        return row
