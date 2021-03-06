from util.db_controller import DBController
from module.html_content_cleaners.comment_html_content_cleaner import CommentHtmlContentCleaner
from module.html_content_cleaners.document_html_content_cleaner import DocumentHtmlContentCleaner


def cleanHtmlContent(oldDB: DBController) -> None:
    print(
        f"Cleaning and inserting document html contents on {oldDB.getDBName()}...")
    cleanDocumentHtmlContent(oldDB)

    print(
        f"Cleaning and inserting comment html contents on {oldDB.getDBName()}...")
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
