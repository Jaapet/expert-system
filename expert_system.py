import sys
import src.knowledgeBase as k
import src.parser as p
import src.inputHandler as i
import src.inferenceEngine as e
import re


def run_interactive_mode(kb, engine, queries):
    """
    Runs an interactive loop allowing the user to change facts and re-solve.
    """
    print("Type new facts (e.g., '=AC' or '-AC') to update state, or 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\n> ")

            if user_input.lower() in ['exit', 'quit']:
                break

            if not re.match(r'^=[A-Z]*$', user_input) and not re.match(r'^-[A-Z]*$', user_input):
                print("Error: Invalid format. Use '=' or '-' followed by facts (e.g., '=AB' or '-AB').")
                continue

            if '=' in user_input:
                kb.add_facts(user_input)
            elif '-' in user_input:
                kb.rm_facts(user_input)

            print(f"Facts updated: {user_input if len(user_input)>1 else 'None'}")

            print("-" * 30)
            for query in queries:
                result = engine.solve(query)
                if result == True:
                    result_str = "TRUE"
                elif result == False:
                    result_str = "FALSE"
                else:
                    result_str = "UNDEFINED"
                print("-" * 30)
                engine.print_reasoning()
                print(f"\n==> {query} is {result_str}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break


def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 expert_system.py <input_file>")
            return

        kb = k.KnowledgeBase()
        parser = p.Parser()
        input_handler = i.InputHandler(sys.argv[1], kb, parser)

        queries = input_handler.process_file()

        # print(kb)

        engine = e.InferenceEngine(kb)
        for query in queries:
            result = engine.solve(query)
            if result == True:
                result_str = "TRUE"
            elif result == False:
                result_str = "FALSE"
            else:
                result_str = "UNDEFINED"
            print("-" * 30)
            engine.print_reasoning()
            print(f"\n==> {query} is {result_str}\n")

        run_interactive_mode(kb, engine, queries)

    
    except Exception as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
