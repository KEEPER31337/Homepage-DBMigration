from typedef.typedef import Row
from library_migrator.library_migrator import LibraryMigrator


class EquipmentMigrator(LibraryMigrator):

    insertEquipmentFormat = ("INSERT INTO {newTableMigrate}(name,information,total)"
                             " VALUES(%(name)s,%(author)s,%(total)s);")

    def __init__(self,
                 oldTableMigrate: str = "equipment",
                 newTableMigrate: str = "equipment") -> None:

        self.insertLibraryFormat = self.insertEquipmentFormat
        super().__init__(oldTableMigrate, newTableMigrate)

    def getLibraryName(self, equipmentName: str) -> str:
        return self.getSplitedEquipmentName(equipmentName)

    def getSplitedEquipmentName(self, equipmentName: str) -> str:
        return equipmentName.split('_')[0]

    def editLibraryRow(self, row: Row) -> Row:
        return self.editEquipmentRow(row)

    def editEquipmentRow(self, row: Row) -> Row:
        return self.setNameTotalOnRow(row)

    def migrateEquipment(self) -> None:
        self.migrateLibrary()
