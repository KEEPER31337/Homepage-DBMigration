from library_migrator.library_migrator import LibraryMigrator
from typedef.typedef import Row


class BookMigrator(LibraryMigrator):
    oldTableMigrate = "books"
    newTableMigrate = "book"

    insertTableQuery = ("INSERT INTO {newTableMigrate}(title,author,total,department)"
                        " VALUES(%(name)s,%(author)s,%(total)s,%(department)s);")

    bookDepartmentDict: dict = dict()

    def getBookEquipmentName(self, bookName: str) -> str:
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
        row = self.setNameTotal(row)
        row = self.setBookDepartment(row)
        return row

    def editBookEquipmentRow(self, row: Row) -> Row:
        return self.editBookRow(row)

    def migrateBook(self) -> None:
        self.migrateBookLibrary()
