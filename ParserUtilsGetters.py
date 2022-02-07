import re
from copy import deepcopy


class ParserUtilsGetters:
    fields = []
    fieldsKeys = []
    fieldsWOKeys = []
    omitFields = ['FACT', 'UACT', 'FCREA', 'UCREA']
    tableName = ''

    def __init__(self, tableName):
        self.tableName = tableName

    def getFields(self, text):
        # regexPatern = r'^.*"(\w+)"\s+(\w+\b(?<!\bPRIMARY)).+$'
        regexPatern = r'^\W+"(\w+)"\s+(\w+).+$'
        regex = re.compile(regexPatern, re.MULTILINE)
        result = regex.findall(text)

        for item in self.omitFields:
            itemKey = [y[0] for y in result].index(item)
            del result[itemKey]

        self.fields = result
        return self.fields

    def getFieldsKeys(self, text):
        regexPatern = r'^.+CONSTRAINT.+\)$'
        regex = re.compile(regexPatern, re.MULTILINE)
        try:
            resultString = regex.search(text).group()

            regexPatern = r'"(\w+)"(?:,|\))'
            regex = re.compile(regexPatern)
            result = regex.findall(resultString)

            fieldsKeys = []
            for key in result:
                indexKey = [y[0] for y in self.fields].index(key)
                fieldsKeys.append(self.fields[indexKey])
        except:
            fieldsKeys = deepcopy(self.fields)

        self.fieldsKeys = fieldsKeys
        return self.fieldsKeys

    def getFieldsWOKeys(self):
        fieldsWOKeys = []
        fieldsWOKeys = deepcopy(self.fields)

        for item in self.fieldsKeys:
            key = item[0]
            indexKey = [y[0] for y in fieldsWOKeys].index(key)
            del fieldsWOKeys[indexKey]

        if (fieldsWOKeys == []):
            self.fieldsWOKeys = deepcopy(self.fields)
        else:
            self.fieldsWOKeys = fieldsWOKeys

        return self.fieldsWOKeys

    def log(self):
        print('Tabla:')
        print(self.tableName)
        print('Fields:')
        print(self.fields)
        print('FieldKeys:')
        print(self.fieldsKeys)
        print('FieldsWOKeys:')
        print(self.fieldsWOKeys)
        print('\n')