
from db_controller.db_controller import DBController
from html_content_cleaner.comment_html_content_cleaner import CommentHtmlContentCleaner
from html_content_cleaner.document_html_content_cleaner import DocumentHtmlContentCleaner

if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setPasswd("")
    oldDB.setDB()

    documentHtmlContentCleaner = DocumentHtmlContentCleaner()
    documentHtmlContentCleaner.setDBController(oldDB)
    documentHtmlContentCleaner.cleanHtmlContent()

    commentHtmlContentCleaner = CommentHtmlContentCleaner()
    commentHtmlContentCleaner.setDBController(oldDB)
    commentHtmlContentCleaner.cleanHtmlContent()
