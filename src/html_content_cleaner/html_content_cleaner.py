from lxml.html import clean
from db_controller.db_controller import DBController


class HtmlContentCleaner:
    oldDBController: DBController
    newDBController: DBController

    safeAttributeSet = {'href', 'src'}  # 주요 attribute인 href, src만 남김

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

    def addSafeAttribute(self, attributeAdd: str) -> None:
        self.safeAttributeSet.add(attributeAdd)

    def addCleanContentColumn(self) -> None:
        self.oldDBController.getCursor().execute(self.addCleanContentColumnQuery)

    def selectDocument(self):
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.selectDocumentQuery)
        documentContent = cursor.fetchall()
        return documentContent

    def getCleanContentTable(self):
        documentTable = self.selectDocument()
        cleaner = clean.Cleaner(safe_attrs_only=True,
                                safe_attrs=self.safeAttributeSet)

        for i, d in enumerate(documentTable):
            cleanHtml = cleaner.clean_html(d["content"])
            documentTable[i]["clean_content"] = cleanHtml

        return documentTable

    def updateDocumentTable(self) -> None:
        self.newDBController.getCursor().executemany(
            self.updateDocumentQuery, self.getCleanContentTable())

        self.newDBController.getDB().commit()

    def cleanHtmlContent(self) -> None :
        self.addCleanContentColumn()
        self.updateDocumentTable()

