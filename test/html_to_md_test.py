# import markdownify
# import html2text
# import html2markdown
# import htmltabletomd
import lxml.html.clean as clean

inputHtml = open("sample.html","r") # test용 html
html = inputHtml.read()

safe_attrs = frozenset({'href','src'}) # 주요 attribute인 href, src만 남김

cleaner = clean.Cleaner(safe_attrs_only=True,safe_attrs=safe_attrs) # Set cleaner
markDown = cleaner.clean_html(html) # Cleaning html code

outputMd = open("cvt.md","w") # md파일로 저장
outputMd.write(markDown)

inputHtml.close()
outputMd.close()