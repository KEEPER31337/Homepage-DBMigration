from util.typedef import Row
from module.library_migrators.library_migrator import LibraryMigrator


class EquipmentMigrator(LibraryMigrator):

    __insertEquipmentFormat = ("INSERT INTO {newTableMigrate}(name,information,total)"
                               " VALUES(%(name)s,%(author)s,%(total)s);")

    def __init__(self,
                 oldTableMigrate: str = "equipment",
                 newTableMigrate: str = "equipment") -> None:

        self._insertLibraryFormat = self.__insertEquipmentFormat
        super().__init__(oldTableMigrate, newTableMigrate)

    def migrateEquipment(self) -> None:
        self._migrateLibrary()

    def _getLibraryName(self, equipmentName: str) -> str:
        return self.__getSplitedEquipmentName(equipmentName)

    def __getSplitedEquipmentName(self, equipmentName: str) -> str:
        return equipmentName.split('_')[0]

    def _editLibraryRow(self, row: Row) -> Row:
        return self.__editEquipmentRow(row)

    def __editEquipmentRow(self, row: Row) -> Row:
        return self._setNameTotalOnRow(row)
