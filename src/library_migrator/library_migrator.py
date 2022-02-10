from abc import abstractclassmethod
from db_controller.db_controller import DBController
from numpy import insert
from pymysql import OperationalError
from typedef.typedef import Table


class LibraryMigrator:
    oldDBController: DBController
    newDBController: DBController

    oldTableMigrate: str
    newTableMigrate: str

    addTotalColumnQuery = ("ALTER TABLE {oldTableMigrate}"
                           " ADD total INT NOT NULL DEFAULT 1;")

    selectTableQuery = ("SELECT number, name, author"
                        " FROM {oldTableMigrate};")

    insertTableQuery: str

    def setOldDBController(self, dbController: DBController) -> None:
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self.newDBController = dbController

    def formatSelectTableQuery(self) -> str:
        return self.selectTableQuery.format(oldTableMigrate=self.oldTableMigrate)

    def formatAddTotalColumnQuery(self) -> str:
        return self.addTotalColumnQuery.format(oldTableMigrate=self.oldTableMigrate)

    def formatInsertTableQuery(self) -> str:
        return self.insertTableQuery.format(newTableMigrate=self.newTableMigrate)

    def addTotalColumn(self) -> None:
        try:
            self.oldDBController.getCursor().execute(self.formatAddTotalColumnQuery())
        except OperationalError as oe:
            print(
                f"{oe} : There is a column already. From {self.addTotalColumn.__name__}.")

    def selectTable(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.formatSelectTableQuery())
        tableContent = cursor.fetchall()
        return tableContent

    @abstractclassmethod
    def getBookEquipmentName(self, bookEquipmentName: str) -> str:
        pass

    def setTotalBookEquipment(self, table: Table) -> Table:
        tableSetTotal: list = list()

        for row in table:
            name = self.getBookEquipmentName(row["name"])
            findResult = self.findBookEquipment(tableSetTotal, name)

            if(findResult == -1):
                row["name"] = name
                row["total"] = 1

                row["department"] = self.getBookDepartment(row["number"])

                tableSetTotal.append(row)

            else:
                tableSetTotal[findResult]["total"] += 1

        return tableSetTotal

    def findBookEquipment(self, table: Table, name: str) -> int:

        for i in range(len(table)-1, -1, -1):
            if(table[i]["name"] == name):
                return i
        return -1

    def getTotalSetTable(self) -> Table:
        return self.setTotalBookEquipment(self.selectTable())

    def insertTable(self) -> None:
        cursor = self.newDBController.getCursor()

        cursor.executemany(
            self.formatInsertTableQuery(),
            self.getTotalSetTable()
        )
        self.newDBController.getDB().commit()

    def migrateBookLibrary(self) -> None:
        self.addTotalColumn()
        self.insertTable()
