from html_content_cleaner.html_content_cleaner import HtmlContentCleaner


class DocumentHtmlContentCleaner(HtmlContentCleaner):

    def __init__(self,
                 cleanContentCol: str = "clean_content",
                 tableClean: str = "xe_documents",
                 srlCol: str = "document_srl") -> None:
        
        super().__init__(cleanContentCol,tableClean,srlCol)
