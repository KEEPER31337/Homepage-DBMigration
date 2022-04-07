from abc import ABCMeta
from module.interface import SingleDBControllable, queryFormattable
from util.err import DataLenOverError, DuplicatedColumnExistErrorLog, LxmlCleanerParseErrorLog
from util.typedef import Row, Table
from pymysql import OperationalError
from lxml.html import clean
from lxml.etree import ParserError
from markdownify import markdownify as md

CONTENT_MAX_LENGTH = 65535


class HtmlContentCleaner(SingleDBControllable, queryFormattable, metaclass=ABCMeta):

    __cleanContentCol: str
    __tableClean: str
    __srlCol: str

    __safeAttributeSet: set

    __selectContentFormat = (
        "SELECT {srlCol}, content"
        " FROM {tableClean};")

    __addCleanContentColumnFormat = (
        "ALTER TABLE {tableClean}"
        " ADD {cleanContentCol} TEXT DEFAULT NULL")

    __updateCleanContentFormat = (
        "UPDATE {tableClean}"
        " SET {cleanContentCol} = %({cleanContentCol})s"
        " WHERE {srlCol} = %({srlCol})s;")

    def __init__(self, cleanContentCol: str,
                 tableClean: str,
                 srlCol: str) -> None:

        self.__cleanContentCol = cleanContentCol
        self.__tableClean = tableClean
        self.__srlCol = srlCol

        self.__safeAttributeSet = set()
        self.addSafeAttribute("href")
        self.addSafeAttribute("src")

    def addSafeAttribute(self, attributeAdd: str) -> None:
        self.__safeAttributeSet.add(attributeAdd)

    def cleanHtmlContent(self) -> None:
        self.__addCleanContentColumn()

        contentTable = self.__selectContent()
        cleanContentTable = self.__getCleanContentTable(contentTable)
        self.__updateCleanContent(cleanContentTable)

    def __addCleanContentColumn(self) -> None:
        try:
            self._dbController.getCursor().execute(
                self._formatQuery(self.__addCleanContentColumnFormat))
        except OperationalError as oe:
            print(DuplicatedColumnExistErrorLog(
                err=oe,
                className=self.__class__.__name__,
                methodName=self.__addCleanContentColumn.__name__,
                columnName=self.__cleanContentCol))

    def _formatQuery(self, queryFormat: str) -> str:
        return queryFormat.format(
            srlCol=self.__srlCol,
            tableClean=self.__tableClean,
            cleanContentCol=self.__cleanContentCol)

    def __selectContent(self) -> Table:
        cursor = self._dbController.getCursor()
        cursor.execute(self._formatQuery(self.__selectContentFormat))
        tableContent = cursor.fetchall()
        return tableContent

    def __getCleanContentTable(self, contentTable: Table) -> Table:

        for i, row in enumerate(contentTable):
            cleanContent = self.__getCleanContent(row)
            contentTable[i][self.__cleanContentCol] = cleanContent

        return contentTable

    def __getCleanContent(self, contentRow: Row) -> str:
        cleanContent: str
        cleaner = self.__getHtmlCleaner()

        try:
            cleanContent = cleaner.clean_html(contentRow["content"])

        except ParserError as pe:
            print(LxmlCleanerParseErrorLog(
                err=pe,
                className=self.__class__.__name__,
                methodName=self.__getCleanContent.__name__,
                msg="Return empty string."))
            return ""

        try:
            if(self.__checkHtmlContentSize(cleanContent)):
                raise DataLenOverError(
                    className=self.__class__.__name__,
                    methodName=self.__getCleanContent.__name__,
                    msg="Redundant tags will be removed.")

        except DataLenOverError as de:
            print(de)
            cleanContent = self.__removeRedundantTag(cleanContent)

        try:
            if(self.__checkHtmlContentSize(cleanContent)):
                raise DataLenOverError(
                    className=self.__class__.__name__,
                    methodName=self.__getCleanContent.__name__,
                    msg=("Content is over the limit length even redundant tags removed..."
                         "Content will be empty string."))

        except DataLenOverError as de:
            print(de)
            cleanContent = ""

        return cleanContent

    def __getHtmlCleaner(self) -> clean.Cleaner:
        return clean.Cleaner(
            safe_attrs_only=True,
            safe_attrs=self.__safeAttributeSet)

    def __checkHtmlContentSize(self, htmlContent: str) -> bool:
        return len(htmlContent) > CONTENT_MAX_LENGTH

    def __removeRedundantTag(self, htmlContent: str) -> str:
        return md(htmlContent)

    def __updateCleanContent(self, cleanContentTable: Table) -> None:
        self._dbController.getCursor().executemany(
            self._formatQuery(self.__updateCleanContentFormat), cleanContentTable)
        self._dbController.getDB().commit()
