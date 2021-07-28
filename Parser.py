from FileUtils import FileUtils
from ParserUtilsGetters import ParserUtilsGetters
from ParserUtilsGenerators import ParserUtilsGenerators


class Parser:
    tableName = ''
    actualPath = ''
    filePath = ''
    inputPath = ''
    softwareComponent = ''
    nameSpace = ''
    dtName = ''

    def __init__(self, fileName, actualPath, inputPath, softwareComponent, nameSpace):
        if (fileName.name.endswith(".sql")):
            self.tableName = fileName.name.split(".sql")[0]
        else:
            self.tableName = fileName.name.split(".txt")[0]
        self.actualPath = actualPath
        self.inputPath = inputPath
        self.filePath = inputPath.joinpath(fileName.name)
        self.softwareComponent = softwareComponent
        self.nameSpace = nameSpace
        self.dtName = 'DT_%s_%s_' % (self.softwareComponent, self.tableName)

    def parse(self):
        # Obtengo la ruta de la carpeta de salida.
        outputPath = self.actualPath.joinpath(self.tableName + '_OUTPUT')

        # Creo la ruta de salida.
        if not (outputPath.exists()):
            outputPath.mkdir()

        # Cargo el archivo en un string.
        fileUtils = FileUtils()
        text = fileUtils.loadFile(self.filePath)

        # Obtengo los campos y claves.
        parserUtilsGetter = ParserUtilsGetters()
        fields = parserUtilsGetter.getFields(text)
        fieldsKeys = parserUtilsGetter.getFieldsKeys(text)
        fieldsWOKeys = parserUtilsGetter.getFieldsWOKeys()

        # Genero los items complex type.
        dataTypes = []
        parserUtilsGenerators = ParserUtilsGenerators(
            self.tableName, self.softwareComponent, self.nameSpace)

        # DT_ITEMS
        dataTypes.append(
            (self.dtName + 'ITEM', parserUtilsGenerators.generateItemComplexType(fields, '')))
        dataTypes.append((self.dtName + 'ITEM_KEY',
                         parserUtilsGenerators.generateItemComplexType(fieldsKeys, '_KEY')))
        dataTypes.append((self.dtName + 'ITEM_WOKEY',
                         parserUtilsGenerators.generateItemComplexType(fieldsWOKeys, '_WOKEY')))

        # DT_SOAP
        dataTypes.append(
            (self.dtName + 'SOAP_REQ', parserUtilsGenerators.generateSOAPReqComplexType()))
        dataTypes.append(
            (self.dtName + 'SOAP_RSP', parserUtilsGenerators.generateSOAPRspComplexType()))

        # DT_JDBC
        dataTypes.append(
            (self.dtName + 'JDBC_RSP', parserUtilsGenerators.generateJDBCRspComplexType()))

        dataTypes.append((self.dtName + 'JDBC_REQ_SELECT',
                         parserUtilsGenerators.generateJDBCReqCompelxType('SELECT')))
        dataTypes.append((self.dtName + 'JDBC_REQ_INSERT',
                         parserUtilsGenerators.generateJDBCReqCompelxType('INSERT')))
        dataTypes.append((self.dtName + 'JDBC_REQ_DELETE',
                         parserUtilsGenerators.generateJDBCReqCompelxType('DELETE')))
        dataTypes.append((self.dtName + 'JDBC_REQ_UPDATE',
                         parserUtilsGenerators.generateJDBCReqCompelxType('UPDATE')))

        for item in dataTypes:
            dtFileName = outputPath.joinpath(item[0] + '.xsd')
            dtOutput = parserUtilsGenerators.generateOutput(item[1])
            fileUtils.writeFile(filePath=dtFileName, content=dtOutput)
