class FileUtils:
    def loadFile(self, path):
        with open(path) as table_file:
            return table_file.read()

    def writeFile(self, filePath, content):
        with open(filePath, 'w') as dt_file:
            dt_file.write(content)