import sys
import src.knowledgeBase as k
import src.parser as p
import src.inputHandler as i

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 expert_system.py <input_file>")
        return

    kb = k.KnowledgeBase()
    parser = p.Parser()
    input_handler = i.InputHandler(sys.argv[1], kb, parser)

    queries = input_handler.process_file()

    print(kb)

    # engine = InferenceEngine(kb)
    # for query in queries:
    #     result = engine.solve(query)
    #     print(f"{query} is {result}")

if __name__ == "__main__":
    main()

#CHECK FOR BOTH SIDES TO EXIST AND OPERATORS BETWEEN SYMBOLS
