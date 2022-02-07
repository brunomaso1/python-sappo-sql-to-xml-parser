class ParserUtilsGenerators:
    tableName = ''
    softwareComponent = ''
    switcher = {}
    dtName = ''
    nameSpace = ''

    def __init__(self, tableName, softwareComponent, nameSpace):
        self.tableName = tableName
        self.softwareComponent = softwareComponent
        self.switcher = {
            "NUMBER": ' type="xsd:string" minOccurs="0" />',
            "VARCHAR2": ' type="xsd:string" minOccurs="0" />',
            "DATE": """ minOccurs="0">
                <xsd:complexType>
                <xsd:simpleContent>
                    <xsd:extension base="xsd:string">
                        <xsd:attribute name="hasQuot" type="xsd:string" />
                    </xsd:extension>
                </xsd:simpleContent>
                </xsd:complexType>
            </xsd:element>"""
        }
        self.dtName = 'DT_%s_%s_' % (self.softwareComponent, self.tableName)
        self.nameSpace = nameSpace + self.tableName

    def generateItemComplexType(self, fields, _type):
        text = ''
        text += '<xsd:complexType name="%sITEM%s">' % (
            self.dtName, _type)
        text += self.generateSequence(fields)
        text += '</xsd:complexType>'

        return text

    def generateSOAPReqComplexType(self):
        text = ''
        text += '<xsd:complexType name="%sSOAP_REQ">' % self.dtName
        text += '<xsd:sequence>'
        text += '<xsd:element name="%s" type="%sITEM" maxOccurs="unbounded" />' % (
            self.tableName, self.dtName)
        text += '</xsd:sequence>'
        text += '</xsd:complexType>'

        return text

    def generateSOAPRspComplexType(self):
        text = ''
        text += '<xsd:complexType name="%sSOAP_RSP">' % self.dtName
        text += '<xsd:sequence>'
        text += '<xsd:element name="RESPONSE" minOccurs="0" maxOccurs="unbounded">'
        text += '<xsd:complexType>'
        text += '<xsd:sequence>'

        text += '<xsd:element name="row" type="%sITEM" minOccurs="0" maxOccurs="unbounded" />' % self.dtName
        text += '<xsd:element name="result_count" type="xsd:string" minOccurs="0" />'

        text += '</xsd:sequence>'
        text += '</xsd:complexType>'
        text += '</xsd:element>'
        text += '</xsd:sequence>'
        text += '</xsd:complexType>'

        return text

    def generateJDBCRspComplexType(self):
        text = ''
        text += '<xsd:complexType name="%sJDBC_RSP">' % self.dtName
        text += '<xsd:sequence>'
        text += '<xsd:element name="STATEMENT_response" maxOccurs="unbounded">'
        text += '<xsd:complexType>'
        text += '<xsd:sequence>'
        text += '<xsd:element name="row" type="%sITEM" minOccurs="0" maxOccurs="unbounded" />' % self.dtName
        text += '<xsd:element name="update_count" type="xsd:integer" minOccurs="0" />'
        text += '<xsd:element name="delete_count" type="xsd:integer" minOccurs="0" />'
        text += '<xsd:element name="insert_count" type="xsd:integer" minOccurs="0" />'
        text += '</xsd:sequence>'
        text += '</xsd:complexType>'
        text += '</xsd:element>'
        text += '</xsd:sequence>'
        text += '</xsd:complexType>'

        return text

    def generateJDBCReqCompelxType(self, _type):
        text = ''
        text += '<xsd:complexType name="%sJDBC_REQ_%s">' % (self.dtName, _type)
        text += '<xsd:sequence>'
        text += '<xsd:element name="STATEMENT">'
        text += '<xsd:complexType>'
        text += '<xsd:sequence>'
        text += '<xsd:element name="%s">' % self.tableName
        text += '<xsd:complexType>'
        text += '<xsd:sequence>'
        text += '<xsd:element name="TABLE" type="xsd:string" />'

        if (_type == 'SELECT'):
            text += '<xsd:element name="ACCESS" type="%sITEM" />' % self.dtName
            text += '<xsd:element name="KEY" type="%sITEM" />' % self.dtName
        elif (_type == 'INSERT'):
            text += '<xsd:element name="ACCESS" type="%sITEM" maxOccurs="unbounded" />' % self.dtName
        elif (_type == 'UPDATE'):
            text += '<xsd:element name="ACCESS" type="%sITEM_WOKEY" />' % self.dtName
            text += '<xsd:element name="KEY" type="%sITEM_KEY" />' % self.dtName
        else:
            text += '<xsd:element name="KEY" type="%sITEM_KEY" />' % self.dtName

        text += '</xsd:sequence>'
        text += '<xsd:attribute name="ACTION" type="xsd:string" use="required" />'
        text += '</xsd:complexType>'
        text += '</xsd:element>'
        text += '</xsd:sequence>'
        text += '</xsd:complexType>'
        text += '</xsd:element>'
        text += '</xsd:sequence>'
        text += '</xsd:complexType>'

        return text

    def generateOutput(self, itemString):
        text = ''
        text += '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="%s" targetNamespace="%s">' % (self.nameSpace, self.nameSpace)
        text += itemString
        text += '</xsd:schema>'
        
        return text


    def generateSequence(self, fields):
        text = ''
        text += '<xsd:sequence>'

        for item in fields:
            itemName = item[0]
            itemType = item[1]

            text += '<xsd:element name="%s"' % itemName
            text += self.switcher.get(itemType)

        text += '</xsd:sequence>'

        return text
