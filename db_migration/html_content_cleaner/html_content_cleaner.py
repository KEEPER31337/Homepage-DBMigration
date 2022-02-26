from abc import ABCMeta, abstractmethod
from util.typedef import Table
from pymysql import OperationalError
from lxml.html import clean
from lxml.etree import ParserError
from markdownify import markdownify as md
from db_controller.db_controller import DBController


class HtmlContentCleaner(metaclass=ABCMeta):
    dbController: DBController

    cleanContentCol: str
    tableClean: str
    srlCol: str

    safeAttributeSet: set

    selectContentFormat = (
        "SELECT {srlCol}, content"
        " FROM {tableClean};")

    addCleanContentColumnFormat = (
        "ALTER TABLE {tableClean}"
        " ADD {cleanContentCol} TEXT DEFAULT NULL")

    updateCleanContentFormat = (
        "UPDATE {tableClean}"
        " SET {cleanContentCol} = %({cleanContentCol})s"
        " WHERE {srlCol} = %({srlCol})s;")

    @abstractmethod
    def __init__(self, cleanContentCol: str,
                 tableClean: str,
                 srlCol: str) -> None:

        self.cleanContentCol = cleanContentCol
        self.tableClean = tableClean
        self.srlCol = srlCol

        self.safeAttributeSet = set()
        self.addSafeAttribute("href")
        self.addSafeAttribute("src")

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def addSafeAttribute(self, attributeAdd: str) -> None:
        self.safeAttributeSet.add(attributeAdd)

    def cleanHtmlContent(self) -> None:
        self.addCleanContentColumn()

        contentTable = self.selectContent()
        cleanContentTable = self.getCleanContentTable(contentTable)
        self.updateCleanContent(cleanContentTable)

    def addCleanContentColumn(self) -> None:
        try:
            self.dbController.getCursor().execute(self.formatAddCleanContentColumnQuery())
        except OperationalError as oe:
            print(
                f"{oe} : There is a column already."
                f" From {self.addCleanContentColumn.__name__}.")

    def formatAddCleanContentColumnQuery(self) -> str:
        return self.addCleanContentColumnFormat.format(
            tableClean=self.tableClean,
            cleanContentCol=self.cleanContentCol)

    def selectContent(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.formatSelectContentQuery())
        tableContent = cursor.fetchall()
        return tableContent

    def formatSelectContentQuery(self) -> str:
        return self.selectContentFormat.format(
            srlCol=self.srlCol,
            tableClean=self.tableClean)

    def getCleanContentTable(self, contentTable: Table) -> Table:
        cleaner = self.getHtmlCleaner()

        for i, row in enumerate(contentTable):
            try:
                cleanHtml = cleaner.clean_html(row["content"])
                if(self.checkHtmlContentSize(cleanHtml)):
                    cleanHtml = self.removeRedundantTag(cleanHtml)
            except ParserError as pe:
                print(
                    f"{pe} : Content will be empty string. From {self.getCleanContentTable.__name__}")
                cleanHtml = ""
            finally:
                contentTable[i][self.cleanContentCol] = cleanHtml

        return contentTable

    def getHtmlCleaner(self) -> clean.Cleaner:
        return clean.Cleaner(
            safe_attrs_only=True,
            safe_attrs=self.safeAttributeSet)

    def checkHtmlContentSize(self, htmlContent: str) -> bool:
        return len(htmlContent) > 65535

    def removeRedundantTag(self, htmlContent: str) -> str:
        return md(htmlContent)

    def updateCleanContent(self, cleanContentTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.formatUpdateCleanContentQuery(), cleanContentTable)
        self.dbController.getDB().commit()

    def formatUpdateCleanContentQuery(self) -> str:
        return self.updateCleanContentFormat.format(
            srlCol=self.srlCol,
            tableClean=self.tableClean,
            cleanContentCol=self.cleanContentCol)
