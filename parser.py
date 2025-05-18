# This code implements a parser for a specific grammar using a recursive descent approach.
class Parser:
    def __init__(self, input_str):
        self.tokens = list(input_str)
        self.pos = 0
        self.node_id = 0
        self.nodes = []
        self.edges = []
        self.derivation = ['S']
        self.working_string = 'S'
        
    def parse(self): # Parse the input string
        root_id = self.S()
        if self.pos != len(self.tokens):
            raise SyntaxError(f"Invalid String!")
        self.derivation.append(''.join(self.tokens))

    def S(self):
        # Create a node for non-terminal S
        my_id = self._new_node('S')

        # If current token is 'a', apply S → aSc
        if self.pos < len(self.tokens) and self.tokens[self.pos] == 'a':
            self._update_derivation('S', 'aSc')

            # Process 'a'
            a_id = self._new_node('a')
            self._add_edge(my_id, a_id)
            self.pos += 1

            # Recursively process S again
            s_id = self.S()
            self._add_edge(my_id, s_id)

            # Expect and process 'c'
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != 'c':
                raise SyntaxError(f"Expected 'c' at position {self.pos}")
            c_id = self._new_node('c')
            self._add_edge(my_id, c_id)
            self.pos += 1
        else:
            # Otherwise, apply S → B
            self._update_derivation('S', 'B')
            b_id = self.B()
            self._add_edge(my_id, b_id)

        return my_id

    def B(self):
        # Create a node for non-terminal B
        my_id = self._new_node('B')

        # If current token is 'b', apply B → bB
        if self.pos < len(self.tokens) and self.tokens[self.pos] == 'b':
            self._update_derivation('B', 'bB')

            # Process 'b'
            b_terminal = self._new_node('b')
            self._add_edge(my_id, b_terminal)
            self.pos += 1

            # Recursively process B again
            b_node = self.B()
            self._add_edge(my_id, b_node)
        else:
            # Otherwise, apply B → ε (empty)
            self._update_derivation('B', 'ε')
            epsilon = self._new_node('ε')
            self._add_edge(my_id, epsilon)

        return my_id

    def _update_derivation(self, from_sym, to_str):
        idx = self.working_string.find(from_sym)
        if idx != -1:
            self.working_string = (
                self.working_string[:idx] + to_str + self.working_string[idx + 1:]
            )
            self.derivation.append(self.working_string)

    def get_derivations(self):
        return self.derivation

    def to_dot(self):
        lines = [
            'digraph G {',
            '  rankdir=TB;',
            '  node [shape=circle, style=filled, fillcolor="#E0F7FA"];'
        ]
        for nid, label in self.nodes:
            lines.append(f'  {nid} [label="{label}"];')
        for src, dst in self.edges:
            lines.append(f'  {src} -> {dst};')
        lines.append('}')
        return "\n".join(lines)

    def _new_node(self, label):
        nid = f'node{self.node_id}'
        self.node_id += 1
        self.nodes.append((nid, label))
        return nid

    def _add_edge(self, src, dst):
        self.edges.append((src, dst))
