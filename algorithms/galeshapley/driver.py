import galeshapley

sampleJson = open("util/sample.json", "r")
matching = galeshapley.main(sampleJson)
print(matching)

