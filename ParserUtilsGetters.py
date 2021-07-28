import re

class ParserUtilsGetters:
    fields = []
    fieldsKeys = []
    fieldsWOKeys = []
    omitFields = ['FACT', 'UACT', 'FCREA', 'UCREA']

    def getFields(self, text):
        regexPatern = r'^.*"(\w+)"\s+(\w+\b(?<!\bPRIMARY)).+$'
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
        resultString = regex.search(text).group()

        regexPatern = r'"(\w+)(?<!ACLARACIONES)"'
        regex = re.compile(regexPatern)
        result = regex.findall(resultString)

        fieldsKeys = []
        for key in result:
            indexKey = [y[0] for y in self.fields].index(key)
            fieldsKeys.append(self.fields[indexKey])

        self.fieldsKeys = fieldsKeys
        return self.fieldsKeys

    def getFieldsWOKeys(self):
        fieldsWOKeys = []
        fieldsWOKeys = self.fields

        for item in self.fieldsKeys:
            key = item[0]
            indexKey = [y[0] for y in self.fields].index(key)
            del fieldsWOKeys[indexKey]

        self.fieldsWOKeys = fieldsWOKeys
        return self.fieldsWOKeys