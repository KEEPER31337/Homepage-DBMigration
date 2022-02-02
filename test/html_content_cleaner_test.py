
from src.db_controller.db_controller import DBController
from src.html_content_cleaner.html_content_cleaner import HtmlContentCleaner


if __name__ == "__main__":

    oldDB = DBController()
    oldDB.setDBName("keeper")
    oldDB.setDB()

    htmlContentCleaner = HtmlContentCleaner()

    htmlContentCleaner.setDBController(oldDB)

    htmlContentCleaner.cleanHtmlContent()
