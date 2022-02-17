from db_controller.db_controller import DBController
from html_content_cleaner.comment_html_content_cleaner import CommentHtmlContentCleaner
from html_content_cleaner.document_html_content_cleaner import DocumentHtmlContentCleaner


def cleanHtmlContent(oldDB: DBController) -> None:
    cleanDocumentHtmlContent(oldDB)
    cleanCommentHtmlContent(oldDB)


def cleanDocumentHtmlContent(oldDB: DBController) -> None:
    documentHtmlContentCleaner = DocumentHtmlContentCleaner()
    documentHtmlContentCleaner.setDBController(oldDB)
    documentHtmlContentCleaner.cleanHtmlContent()


def cleanCommentHtmlContent(oldDB: DBController) -> None:
    commentHtmlContentCleaner = CommentHtmlContentCleaner()
    commentHtmlContentCleaner.setDBController(oldDB)
    commentHtmlContentCleaner.cleanHtmlContent()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    cleanHtmlContent(oldDB)
