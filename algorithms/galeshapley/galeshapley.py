from matching.algorithms import galeshapley
import json

def main(wrappedInput):
    stringInput = wrappedInput.read()
    jsonInput = json.loads(stringInput)
    print(jsonInput['author'])
    menSuitors = jsonInput['sample_input']['men']
    womenSuitors = jsonInput['sample_input']['women']
    matching = galeshapley(menSuitors, womenSuitors)
    print(matching)

if __name__ == "__main__":
    main(jsonInput)