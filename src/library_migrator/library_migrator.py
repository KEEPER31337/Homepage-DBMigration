from db_controller.db_controller import DBController
from typedef.typedef import Table


class LibraryMigrator:
    oldDBController: DBController
    newDBController: DBController

    tableMigrate: str

    selectTableQuery = ("SELECT number, name, author"
                        " FROM {tableMigrate};")

    def setOldDBController(self, dbController: DBController) -> None:
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self.newDBController = dbController

    def formatSelectTableQuery(self) -> str:
        return self.selectTableQuery.format(tableMigrate=self.tableMigrate)

    def selectTable(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.formatSelectTableQuery())
        tableContent = cursor.fetchall()
        return tableContent

    