import galeshapley
import json
# import os

# cwd = os.getcwd()
# list = os.listdir()
# print(cwd)
# print(list)


sampleJson = open("util/sample.json", "r")
# print(type(sampleJson))
# json.loads(sampleJson)
galeshapley.main(sampleJson)
