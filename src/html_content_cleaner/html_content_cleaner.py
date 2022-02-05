from lxml.html import clean
from lxml.etree import ParserError
from markdownify import markdownify as md
from db_controller.db_controller import DBController
from typedef.typedef import Table


class HtmlContentCleaner:
    dbController: DBController

    cleanContentCol: str

    safeAttributeSet: set

    selectDocumentQuery = (
        "SELECT document_srl, content"
        " FROM xe_documents;")

    addCleanContentColumnQuery = (
        "ALTER TABLE xe_documents"
        " ADD clean_content TEXT DEFAULT NULL")

    updateDocumentQuery = (
        "UPDATE xe_documents"
        " SET clean_content = %(clean_content)s"
        " WHERE document_srl = %(document_srl)s;")

    def __init__(self, cleanContentCol: str = "clean_content") -> None:
        self.cleanContentCol = cleanContentCol

        self.safeAttributeSet = set()
        self.addSafeAttribute("href")
        self.addSafeAttribute("src")

    def setDBController(self, dbController: DBController):
        self.dbController = dbController

    def addSafeAttribute(self, attributeAdd: str) -> None:
        self.safeAttributeSet.add(attributeAdd)

    def addCleanContentColumn(self) -> None:
        self.dbController.getCursor().execute(self.addCleanContentColumnQuery)

    def selectDocument(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectDocumentQuery)
        documentContent = cursor.fetchall()
        return documentContent

    def checkHtmlContentSize(self, htmlContent: str) -> bool:
        return len(htmlContent) > 65535

    def removeRedundantTag(self, htmlContent: str) -> str:
        return md(htmlContent)

    def getCleanContentTable(self) -> Table:
        documentTable = self.selectDocument()
        cleaner = clean.Cleaner(safe_attrs_only=True,
                                safe_attrs=self.safeAttributeSet)

        for i, d in enumerate(documentTable):
            
            try:
                cleanHtml = cleaner.clean_html(d["content"])
                if(self.checkHtmlContentSize(cleanHtml)) : 
                    cleanHtml = self.removeRedundantTag(cleanHtml)
            except ParserError as e:
                cleanHtml = ""
            finally:    
                documentTable[i][self.cleanContentCol] = cleanHtml

        return documentTable

    def updateDocumentTable(self) -> None:
        self.dbController.getCursor().executemany(
            self.updateDocumentQuery, self.getCleanContentTable())
        self.dbController.getDB().commit()

    def cleanHtmlContent(self) -> None:
        self.addCleanContentColumn()
        self.updateDocumentTable()
