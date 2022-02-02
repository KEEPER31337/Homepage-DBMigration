from lxml.html import clean
from db_controller.db_controller import DBController
from utils.typedef import Table


class HtmlContentCleaner:
    oldDBController: DBController
    newDBController: DBController
    cleanContentCol: str

    safeAttributeSet: set

    selectDocumentQuery = (
        "SELECT document_srl, content",
        " FROM xe_documents;")

    addCleanContentColumnQuery = (
        "ALTER TABLE xe_documents"
        "ADD clean_content TEXT DEFAULT NULL")

    updateDocumentQuery = (
        "UPDATE xe_documents"
        " SET clean_content = %(clean_content)s"
        " WHERE document_srl = %(document_srl)s;")

    def __init__(self, cleanContentCol: str = "clean_content") -> None:
        self.cleanContentCol = cleanContentCol

        self.safeAttributeSet = set()
        self.addSafeAttribute("href")
        self.addSafeAttribute("src")

    def addSafeAttribute(self, attributeAdd: str) -> None:
        self.safeAttributeSet.add(attributeAdd)

    def addCleanContentColumn(self) -> None:
        self.oldDBController.getCursor().execute(self.addCleanContentColumnQuery)

    def selectDocument(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.selectDocumentQuery)
        documentContent = cursor.fetchall()
        return documentContent

    def getCleanContentTable(self) -> Table:
        documentTable = self.selectDocument()
        cleaner = clean.Cleaner(safe_attrs_only=True,
                                safe_attrs=self.safeAttributeSet)

        for i, d in enumerate(documentTable):
            cleanHtml = cleaner.clean_html(d["content"])
            documentTable[i][self.cleanContentCol] = cleanHtml

        return documentTable

    def updateDocumentTable(self) -> None:
        self.newDBController.getCursor().executemany(
            self.updateDocumentQuery, self.getCleanContentTable())

        self.newDBController.getDB().commit()

    def cleanHtmlContent(self) -> None:
        self.addCleanContentColumn()
        self.updateDocumentTable()
