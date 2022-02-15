from abc import ABCMeta, abstractclassmethod
from typedef.typedef import Row, Table
from db_controller.db_controller import DBController


class LibraryMigrator(metaclass=ABCMeta):
    oldDBController: DBController
    newDBController: DBController

    oldTableMigrate: str
    newTableMigrate: str

    selectLibraryFormat = ("SELECT number, name, author"
                           " FROM {oldTableMigrate};")

    insertLibraryFormat: str

    @abstractclassmethod
    def __init__(self,
                 oldTableMigrate: str,
                 newTableMigrate: str) -> None:

        self.oldTableMigrate = oldTableMigrate
        self.newTableMigrate = newTableMigrate

    def setOldDBController(self, dbController: DBController) -> None:
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self.newDBController = dbController

    def formatSelectLibraryQuery(self) -> str:
        return self.selectLibraryFormat.format(oldTableMigrate=self.oldTableMigrate)

    def formatInsertLibraryQuery(self) -> str:
        return self.insertLibraryFormat.format(newTableMigrate=self.newTableMigrate)

    def selectLibrary(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.formatSelectLibraryQuery())
        libraryTable = cursor.fetchall()
        return libraryTable

    @abstractclassmethod
    def getLibraryName(self, name: str) -> str: pass

    @abstractclassmethod
    def editLibraryRow(self, row: Row) -> Row: pass

    def setNameTotalOnRow(self, row: Row) -> Row:
        row["name"] = self.getLibraryName(row["name"])
        row["total"] = 1
        return row

    def getEditedLibraryTable(self, libraryTable: Table) -> Table:
        editedLibraryTable: Table = list()

        for row in libraryTable:
            name = self.getLibraryName(row["name"])
            bookEquipmentIndex = self.findLibrary(editedLibraryTable, name)

            if(bookEquipmentIndex == -1):
                editedLibraryTable.append(self.editLibraryRow(row))
            else:
                editedLibraryTable[bookEquipmentIndex]["total"] += 1

        return editedLibraryTable

    def findLibrary(self, table: Table, name: str) -> int:

        for i in range(len(table)-1, -1, -1):
            if(table[i]["name"] == name):
                return i
        return -1

    def insertLibrary(self, editedLibraryTable: Table) -> None:
        cursor = self.newDBController.getCursor()

        cursor.executemany(
            self.formatInsertLibraryQuery(),
        )
        self.newDBController.getDB().commit()

    def migrateLibrary(self) -> None:
        libraryTable = self.selectLibrary()
        editedLibraryTable = self.getEditedLibraryTable(libraryTable)
        self.insertLibrary(editedLibraryTable)
