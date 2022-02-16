from db_controller.db_controller import DBController
from html_content_cleaner.comment_html_content_cleaner import CommentHtmlContentCleaner
from html_content_cleaner.document_html_content_cleaner import DocumentHtmlContentCleaner


def testHtmlContentCleaner(oldDB: DBController) -> None:
    testDocumentHtmlContentCleaner(oldDB)
    testCommentHtmlContentCleaner(oldDB)


def testDocumentHtmlContentCleaner(oldDB: DBController) -> None:
    documentHtmlContentCleaner = DocumentHtmlContentCleaner()
    documentHtmlContentCleaner.setDBController(oldDB)
    documentHtmlContentCleaner.cleanHtmlContent()


def testCommentHtmlContentCleaner(oldDB: DBController) -> None:
    commentHtmlContentCleaner = CommentHtmlContentCleaner()
    commentHtmlContentCleaner.setDBController(oldDB)
    commentHtmlContentCleaner.cleanHtmlContent()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    testHtmlContentCleaner(oldDB)
