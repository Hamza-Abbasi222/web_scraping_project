from lxml import html

# Sample HTML content
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Books</title>
</head>
<body>
    <h1>Book List</h1>
    <table>
        <tr>
            <th>Title</th>
            <th>Author</th>
        </tr>
        <tr>
            <td>1984</td>
            <td>George Orwell</td>
        </tr>
        <tr>
            <td>Brave New World</td>
            <td>Aldous Huxley</td>
        </tr>
    </table>
</body>
</html>
'''

# Parse the HTML
tree = html.fromstring(html_content)

# XPath queries
title = tree.xpath('//title/text()')
h1 = tree.xpath('//h1/text()')
first_book_title = tree.xpath('//table/tr[2]/td[1]/text()')
brave_new_world_author = tree.xpath('//table/tr[3]/td[2]/text()')
all_rows = tree.xpath('//table/tr')

print("Page Title:", title)
print("Header (H1):", h1)
print("First Book Title:", first_book_title)
print("Author of Brave New World:", brave_new_world_author)

print("All Rows:")
for row in all_rows:
    print(row.xpath('.//td/text()'))
