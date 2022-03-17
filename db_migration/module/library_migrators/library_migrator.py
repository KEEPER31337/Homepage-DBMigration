from abc import ABCMeta, abstractmethod
from module.db_controll_interface import DoubleDBControllInterface
from util.typedef import Row, Table
from util.db_controller import DBController


class LibraryMigrator(DoubleDBControllInterface, metaclass=ABCMeta):

    __oldTableMigrate: str
    __newTableMigrate: str

    __selectLibraryFormat = ("SELECT number, name, author"
                             " FROM {oldTableMigrate};")

    _insertLibraryFormat: str

    def __init__(self,
                 oldTableMigrate: str,
                 newTableMigrate: str) -> None:

        self.__oldTableMigrate = oldTableMigrate
        self.__newTableMigrate = newTableMigrate

    def _migrateLibrary(self) -> None:
        libraryTable = self.__selectLibrary()
        editedLibraryTable = self.__getEditedLibraryTable(libraryTable)
        self.__insertLibrary(editedLibraryTable)

    def __selectLibrary(self) -> Table:
        cursor = self._oldDBController.getCursor()
        cursor.execute(self.__formatSelectLibraryQuery())
        libraryTable = cursor.fetchall()
        return libraryTable

    def __formatSelectLibraryQuery(self) -> str:
        return self.__selectLibraryFormat.format(oldTableMigrate=self.__oldTableMigrate)

    def __getEditedLibraryTable(self, libraryTable: Table) -> Table:
        editedLibraryTable: Table = list()

        for row in libraryTable:
            name = self._getLibraryName(row["name"])
            bookEquipmentIndex = self.__findLibrary(editedLibraryTable, name)

            if(bookEquipmentIndex == -1):
                editedLibraryTable.append(self._editLibraryRow(row))
            else:
                editedLibraryTable[bookEquipmentIndex]["total"] += 1
                editedLibraryTable[bookEquipmentIndex]["enable"] += 1

        return editedLibraryTable

    @abstractmethod
    def _getLibraryName(self, name: str) -> str: pass

    def __findLibrary(self, table: Table, name: str) -> int:

        for i in range(len(table)-1, -1, -1):
            if(table[i]["name"] == name):
                return i
        return -1

    @abstractmethod
    def _editLibraryRow(self, row: Row) -> Row: pass

    def _setNameTotalOnRow(self, row: Row) -> Row:
        row["name"] = self._getLibraryName(row["name"])
        row["total"] = 1
        row["enable"] = 1
        return row

    def __insertLibrary(self, editedLibraryTable: Table) -> None:
        cursor = self._newDBController.getCursor()

        cursor.executemany(
            self.__formatInsertLibraryQuery(),
            editedLibraryTable
        )
        self._newDBController.getDB().commit()

    def __formatInsertLibraryQuery(self) -> str:
        return self._insertLibraryFormat.format(newTableMigrate=self.__newTableMigrate)
