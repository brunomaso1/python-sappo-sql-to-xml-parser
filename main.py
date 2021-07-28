from Parser import Parser
import pathlib
import os

print('Software Comonent:')
softwareComponent = input()

print('Namespace: ')
nameSpace = input()

actualPath = pathlib.Path(__file__).parent.resolve()
inputPath = actualPath.joinpath('input')

for entry in os.scandir(inputPath):
    if (entry.path.endswith(".sql") or entry.path.endswith(".txt")) and entry.is_file():
        parser = Parser(entry, actualPath, inputPath, softwareComponent, nameSpace)
        parser.parse()