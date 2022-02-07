from Parser import Parser
import pathlib
import os

print('Software Component:')
# softwareComponent = input()
softwareComponent = 'GIC'

print('Namespace (http://imm.gub.uy/SAP-GIC/): ')
# nameSpace = input()
nameSpace = 'http://imm.gub.uy/SAP-GIC/'

actualPath = pathlib.Path(__file__).parent.resolve()
inputPath = actualPath.joinpath('input')

for entry in os.scandir(inputPath):
    if (entry.path.endswith(".sql") or entry.path.endswith(".txt")) and entry.is_file():
        parser = Parser(entry, actualPath, inputPath, softwareComponent, nameSpace)
        parser.parse()