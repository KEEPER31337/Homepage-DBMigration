from util.typedef import Row
from library_migrator.library_migrator import LibraryMigrator


class BookMigrator(LibraryMigrator):

    bookDepartmentDict: dict

    insertBookFormat = ("INSERT INTO {newTableMigrate}(title,author,total,department)"
                        " VALUES(%(name)s,%(author)s,%(total)s,%(department)s);")

    def __init__(self,
                 oldTableMigrate: str = "books",
                 newTableMigrate: str = "book") -> None:

        self.insertLibraryFormat = self.insertBookFormat
        self.bookDepartmentDict = dict()
        super().__init__(oldTableMigrate, newTableMigrate)

    def getLibraryName(self, bookName: str) -> str:
        return self.getBookName(bookName)

    def getBookName(self, bookName: str) -> str:
        return bookName.strip()

    def addBookDepartment(self, oldDepartmentNumber: int, newDepartmentId: int) -> None:
        self.bookDepartmentDict[oldDepartmentNumber] = newDepartmentId

    def parseBookDepartment(self, bookNumber: str) -> int:
        oldNumber = int(bookNumber[0])
        return self.bookDepartmentDict[oldNumber]

    def setBookDepartment(self, row: Row) -> Row:
        row["department"] = self.parseBookDepartment(row["number"])
        return row

    def editBookRow(self, row: Row) -> Row:
        row = self.setNameTotalOnRow(row)
        row = self.setBookDepartment(row)
        return row

    def editLibraryRow(self, row: Row) -> Row:
        return self.editBookRow(row)

    def migrateBook(self) -> None:
        self.migrateLibrary()
