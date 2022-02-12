from abc import abstractclassmethod
from db_controller.db_controller import DBController
from typedef.typedef import Row, Table


class LibraryMigrator:
    oldDBController: DBController
    newDBController: DBController

    oldTableMigrate: str
    newTableMigrate: str

    selectTableQuery = ("SELECT number, name, author"
                        " FROM {oldTableMigrate};")

    insertTableQuery: str

    def setOldDBController(self, dbController: DBController) -> None:
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self.newDBController = dbController

    def formatSelectTableQuery(self) -> str:
        return self.selectTableQuery.format(oldTableMigrate=self.oldTableMigrate)

    def formatInsertTableQuery(self) -> str:
        return self.insertTableQuery.format(newTableMigrate=self.newTableMigrate)

    def selectTable(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.formatSelectTableQuery())
        tableContent = cursor.fetchall()
        return tableContent

    @abstractclassmethod
    def getBookEquipmentName(self, name: str) -> str: pass

    @abstractclassmethod
    def editBookEquipmentRow(self, row: Row) -> Row: pass

    def setNameTotal(self, row: Row) -> Row:
        row["name"] = self.getBookEquipmentName(row["name"])
        row["total"] = 1
        return row

    def getTableEdited(self, table: Table) -> Table:
        tableEdited: list = list()

        for row in table:
            name = self.getBookEquipmentName(row["name"])
            bookEquipmentIndex = self.findBookEquipment(tableEdited, name)

            if(bookEquipmentIndex == -1):
                tableEdited.append(self.editBookEquipmentRow(row))
            else:
                tableEdited[bookEquipmentIndex]["total"] += 1

        return tableEdited

    def findBookEquipment(self, table: Table, name: str) -> int:

        for i in range(len(table)-1, -1, -1):
            # print(str(len(name)) + " : " + str(len(table[i]["name"])))
            if(table[i]["name"] == name):
                # print("correct")
                return i
        return -1

    def getTableInsert(self) -> Table:
        return self.getTableEdited(self.selectTable())

    def insertTable(self) -> None:
        cursor = self.newDBController.getCursor()

        cursor.executemany(
            self.formatInsertTableQuery(),
            self.getTableInsert()
        )
        self.newDBController.getDB().commit()

    def migrateBookLibrary(self) -> None:
        self.insertTable()
