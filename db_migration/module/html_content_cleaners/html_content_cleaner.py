from abc import ABCMeta, abstractmethod
from util.err import DataLenOverError, DuplicatedColumnExistErrorLog, LxmlCleanerParseErrorLog
from util.typedef import Row, Table
from pymysql import OperationalError
from lxml.html import clean
from lxml.etree import ParserError
from markdownify import markdownify as md
from db_controllers.db_controller import DBController

CONTENT_MAX_LENGTH = 65535


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
            print(DuplicatedColumnExistErrorLog(
                err=oe,
                className=self.__class__.__name__,
                methodName=self.addCleanContentColumn.__name__,
                columnName=self.cleanContentCol))

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

        for i, row in enumerate(contentTable):
            cleanContent = self.getCleanContent(row)
            contentTable[i][self.cleanContentCol] = cleanContent

        return contentTable

    def getCleanContent(self, contentRow: Row) -> str:
        cleanContent: str
        cleaner = self.getHtmlCleaner()

        try:
            cleanContent = cleaner.clean_html(contentRow["content"])

        except ParserError as pe:
            print(LxmlCleanerParseErrorLog(
                err=pe,
                className=self.__class__.__name__,
                methodName=self.getCleanContent.__name__,
                msg="Return empty string."))
            return ""

        try:
            if(self.checkHtmlContentSize(cleanContent)):
                raise DataLenOverError(
                    className=self.__class__.__name__,
                    methodName=self.getCleanContent.__name__,
                    msg="Redundant tags will be removed.")

        except DataLenOverError as de:
            print(de)
            cleanContent = self.removeRedundantTag(cleanContent)

        try:
            if(self.checkHtmlContentSize(cleanContent)):
                raise DataLenOverError(
                    className=self.__class__.__name__,
                    methodName=self.getCleanContent.__name__,
                    msg=("Content is over the limit length even redundant tags removed..."
                         "Content will be empty string."))

        except DataLenOverError as de:
            print(de)
            cleanContent = ""

        return cleanContent

    def getHtmlCleaner(self) -> clean.Cleaner:
        return clean.Cleaner(
            safe_attrs_only=True,
            safe_attrs=self.safeAttributeSet)

    def checkHtmlContentSize(self, htmlContent: str) -> bool:
        return len(htmlContent) > CONTENT_MAX_LENGTH

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
