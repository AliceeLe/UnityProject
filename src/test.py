import imgkit
html_content = '''
<html>
<head>
</head>
<body>
<h1>Helo</h1>
</body>
</html>
'''

imgkit.from_string(html_content, 'output.png')