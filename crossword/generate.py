import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains.keys():
            set_copy=self.domains[v].copy()
            for x in set_copy:
                if len(x)!= v.length:
                    self.domains[v].remove(x)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        intersection=self.crossword.overlaps[x,y]
        if intersection is None :
            return False
        set_copy=self.domains[x].copy()
        revision= False
        for x_value in set_copy:
            found=False
            for y_value in self.domains[y]:
                if x_value[intersection[0]]==y_value[intersection[1]]:
                    found=True
            if not found:
                self.domains[x].remove(x_value)
                revision=True
        return revision






    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue=[]
        if arcs is None:
            queue = list(self.crossword.overlaps.keys())
        else :
            queue =arcs
        while(queue):
            (x,y)= queue.pop()
            if self.revise(x,y):
                if len(self.domains[x])==0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z!=y:
                        queue.append((z,x))
        return True



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(self.crossword.variables)!=len(assignment):
            return False
        return True
                

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if len(set(assignment.values()))!= len(assignment.values()) :
            return False
        for v in assignment:
            if len(assignment[v]) != v.length :
                return False
            for v2 in assignment:
                if v==v2:
                    continue
                intersection=self.crossword.overlaps[v,v2]
                if intersection and  assignment[v][intersection[0]]!=assignment[v2][intersection[1]]:
                    return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = list(self.crossword.neighbors(var))
        for v in neighbors:
            if v in assignment:
                neighbors.remove(v)
        dic ={}
        for value in self.domains[var]:
            eliminates=0
            for v in neighbors:
                for value2 in self.domains[v]:
                    intersection=self.crossword.overlaps[var,v]
                    if intersection and  value[intersection[0]]!=value2[intersection[1]]:
                        eliminates+=1
                dic[value]=eliminates
                eliminates=0
        # Create a list of the dictionary's keys
        keys_list = list(dic.keys())

        # Sort the keys list based on the dictionary values
        keys_list.sort(key=lambda x: dic[x])
        return keys_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        length=float('inf')
        variable_to_return=None
        for v in self.domains:
            if v in assignment:
                continue
            if len(self.domains[v])<length:
                length=len(self.domains[v])
                variable_to_return=v
            elif len(self.domains[v])==length:
                if len(self.crossword.neighbors(v))>len(self.crossword.neighbors(variable_to_return)):
                    variable_to_return=v
        return variable_to_return

            

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            
            assignment[var]=value
            if self.consistent(assignment) :
                inferences = self.ac3([(var,x) for x in self.crossword.neighbors(var)])
                if  not inferences:
                    return None
                result = self.backtrack(assignment)
                if result is not None :
                    return result 
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()