from lxml.html import clean
from lxml.etree import ParserError
from pymysql import OperationalError
from markdownify import markdownify as md
from db_controller.db_controller import DBController
from typedef.typedef import Table


class HtmlContentCleaner:
    dbController: DBController

    cleanContentCol: str
    tableClean: str
    srlCol: str

    safeAttributeSet: set

    selectTableQuery = (
        "SELECT {srlCol}, content"
        " FROM {tableClean};")

    addColumnQuery = (
        "ALTER TABLE {tableClean}"
        " ADD {cleanContentCol} TEXT DEFAULT NULL")

    updateTableQuery = (
        "UPDATE {tableClean}"
        " SET {cleanContentCol} = %({cleanContentCol})s"
        " WHERE {srlCol} = %({srlCol})s;")

    def __init__(self, cleanContentCol: str = "clean_content") -> None:
        self.cleanContentCol = cleanContentCol

        self.safeAttributeSet = set()
        self.addSafeAttribute("href")
        self.addSafeAttribute("src")

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def addSafeAttribute(self, attributeAdd: str) -> None:
        self.safeAttributeSet.add(attributeAdd)

    def formatSelectTableQuery(self) -> str:
        return self.selectTableQuery.format(
            srlCol=self.srlCol,
            tableClean=self.tableClean
        )

    def formatAddColumnQuery(self) -> str:
        return self.addColumnQuery.format(
            tableClean=self.tableClean,
            cleanContentCol=self.cleanContentCol
        )

    def formatUpdateTableQuery(self) -> str:
        return self.updateTableQuery.format(
            srlCol=self.srlCol,
            tableClean=self.tableClean,
            cleanContentCol=self.cleanContentCol
        )

    def addCleanContentColumn(self) -> None:
        try:
            self.dbController.getCursor().execute(self.formatAddColumnQuery())
        except OperationalError as oe:
            print(
                f"{oe} : There is a column already. From {self.addCleanContentColumn.__name__}.")

    def selectTable(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.formatSelectTableQuery())
        tableContent = cursor.fetchall()
        return tableContent

    def updateTable(self) -> None:
        self.dbController.getCursor().executemany(
            self.formatUpdateTableQuery(), self.getCleanContentTable())
        self.dbController.getDB().commit()

    def getCleanContentTable(self) -> Table:
        originalTable = self.selectTable()
        cleaner = clean.Cleaner(safe_attrs_only=True,
                                safe_attrs=self.safeAttributeSet)

        for i, d in enumerate(originalTable):
            try:
                cleanHtml = cleaner.clean_html(d["content"])
                if(self.checkHtmlContentSize(cleanHtml)):
                    cleanHtml = self.removeRedundantTag(cleanHtml)
            except ParserError as pe:
                print(
                    f"{pe} : Content will be empty string. From {self.getCleanContentTable.__name__}")
                cleanHtml = ""
            finally:
                originalTable[i][self.cleanContentCol] = cleanHtml

        return originalTable

    def checkHtmlContentSize(self, htmlContent: str) -> bool:
        return len(htmlContent) > 65535

    def removeRedundantTag(self, htmlContent: str) -> str:
        return md(htmlContent)

    def cleanHtmlContent(self) -> None:
        self.addCleanContentColumn()
        self.updateTable()
