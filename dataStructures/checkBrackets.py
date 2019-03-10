# ================================================================================
# This algorithm utilizes a stack data structure to check for balanced brackets

# Given an input file:
# Report 'success' if all brackets had been opened and closed properly
# Report 1-based index if there is a unmatched opening bracket
# Report 1-based index if there is a unmatched closing bracket

# To run program in command line:
# Create bracket.txt file of random characters (be sure to include brackets)
# In Mac Terminal         $ cat bracket.txt | python checkBrackets.py
# In Windows Command Line $ type bracket.txt | python checkBrackets.py
# ================================================================================


import sys


class Bracket:
    def __init__(self, item, position):
        self.item     = item
        self.position = position

    def match(self, c):
        if self.item == '[' and c == ']':
            return True

        if self.item == '{' and c == '}':
            return True

        if self.item == '(' and c == ')':
            return True

        return False


if __name__ == '__main__':
    # Read .txt file of characters
    text = sys.stdin.read()

    # Exit program if file cannot be read
    if not text:
        print("Cannot read file...")
        sys.exit(1)

    # Create the stack
    opening_bracket_stack = []

    # For every character in the input.txt file, confirm matching brackets
    for index, c in enumerate(text):
        # If opening bracket, add bracket object on top of stack
        if c == '(' or c == '[' or c == '{':
            bracket = Bracket(c, index)
            opening_bracket_stack.append(bracket)
            pass

        # If closing bracket, check for match and pop if match is true
        if c == ')' or c == ']' or c == '}':
            if opening_bracket_stack:
                item_to_match = opening_bracket_stack.pop(len(opening_bracket_stack) - 1)

                # Report 1-based index of mismatched brackets
                if not item_to_match.match(c):
                    print(index + 1)
                    sys.exit()
                    
            # Report 1-based index of unmatched closing bracket
            else:
                print(index + 1)
                sys.exit()
            pass

    # Report 1-based index of unmatched opening bracket
    if opening_bracket_stack:
        unmatched_item = opening_bracket_stack.pop(len(opening_bracket_stack) - 1).position
        print(unmatched_item + 1)

    else:
        print("success!")