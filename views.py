def root():
    with open('templates/root.html') as template:
        return template.read()
def favicon():
    with open('templates/favicon.html') as template:
        return template.read()