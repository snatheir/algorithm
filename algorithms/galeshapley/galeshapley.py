from matching.algorithms import galeshapley
import json

def main(wrappedInput):
    stringInput = wrappedInput.read()
    jsonInput = json.loads(stringInput)
    menSuitors = jsonInput['sample_input']['men']
    womenSuitors = jsonInput['sample_input']['women']
    matchingDict = galeshapley(menSuitors, womenSuitors)
    matchingJson = json.dumps(matchingDict, indent=2)
    return matchingJson

if __name__ == "__main__":
    main(jsonInput)