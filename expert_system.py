import sys
import src.knowledgeBase as k
import src.parser as p
import src.inputHandler as i
import src.inferenceEngine as e


def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 expert_system.py <input_file>")
            return

        kb = k.KnowledgeBase()
        parser = p.Parser()
        input_handler = i.InputHandler(sys.argv[1], kb, parser)

        queries = input_handler.process_file()

        print(kb)

        engine = e.InferenceEngine(kb)
        for query in queries:
            result = engine.solve(query)
            print(f"{query} is {result}")
    
    except Exception as ex:
        print(f"Error: {ex}")

if __name__ == "__main__":
    main()
