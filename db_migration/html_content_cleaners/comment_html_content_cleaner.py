from html_content_cleaners.html_content_cleaner import HtmlContentCleaner


class CommentHtmlContentCleaner(HtmlContentCleaner):

    def __init__(self,
                 cleanContentCol: str = "clean_content",
                 tableClean: str = "xe_comments",
                 srlCol: str = "comment_srl") -> None:

        super().__init__(cleanContentCol, tableClean, srlCol)
