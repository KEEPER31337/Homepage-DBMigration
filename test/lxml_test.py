from os import remove
from pprint import PrettyPrinter
from lxml.html import clean
from lxml import etree
from lxml.etree import tostring
from markdownify import markdownify as md



html =  """
        <tr>
			<td>538</td>
			<td><img src="http://keeper.cse.pusan.ac.kr//modules/point/icons/level2/538.gif"></td>
			<td><label> point</label></td>
			<td>우수회원,</td>
		</tr>
		<tr>
			<td>539</td>
			<td><img src="http://keeper.cse.pusan.ac.kr//modules/point/icons/level2/539.gif"></td>
			<td><label> point</label></td>
			<td>우수회원,</td>
		</tr>
        """

removeStr = "http://keeper.cse.pusan.ac.kr/"
parser = etree.HTMLParser()
tree = etree.fromstring(html,parser)
for i in tree.xpath('//img') :
    i.set("src",i.attrib['src'].strip(removeStr))
    
print(md(html))