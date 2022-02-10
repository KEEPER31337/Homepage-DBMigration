from library_migrator.library_migrator import LibraryMigrator


class EquipmentMigrator(LibraryMigrator):
    oldTableMigrate = "equipment"
    newTableMigrate = "equipment"

    insertTableQuery = ("INSERT INTO {newTableMigrate}(name,information,total)"
                        " VALUES(%(name)s,%(author)s,%(total)s);")

    def getBookEquipmentName(self, equipmentName: str) -> str:
        return self.getSplitedEquipmentName(equipmentName)

    def getSplitedEquipmentName(self, equipmentName: str) -> str:
        return equipmentName.split('_')[0]

    def migrateEquipment(self) -> None:
        self.migrateBookLibrary()
