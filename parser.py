class Parser:
    def __init__(self, input_str):
        self.tokens = list(input_str)
        self.pos = 0
        self.node_id = 0
        self.nodes = []
        self.edges = []
        self.derivation = ['S']  # Derivation history
        self.working_string = 'S'

    def parse(self):
        self.S()
        if self.pos != len(self.tokens):
            raise SyntaxError(f"Invalid String!")
        self.derivation.append(''.join(self.tokens))  # Final string

    def S(self):
        my_id = self._new_node('S')
        if self.pos < len(self.tokens) and self.tokens[self.pos] == 'a':
            self._update_derivation('S', 'aSc')
            a_id = self._new_node('a')
            self._add_edge(my_id, a_id)
            self.pos += 1

            child = self.S()
            self._add_edge(my_id, child)

            if self.pos >= len(self.tokens) or self.tokens[self.pos] != 'c':
                raise SyntaxError(f"Expected 'c' at position {self.pos}")
            c_id = self._new_node('c')
            self._add_edge(my_id, c_id)
            self.pos += 1
        else:
            self._update_derivation('S', 'B')
            child = self.B()
            self._add_edge(my_id, child)
        return my_id

    def B(self):
        my_id = self._new_node('B')
        b_count = 0
        while self.pos < len(self.tokens) and self.tokens[self.pos] == 'b':
            b_id = self._new_node('b')
            self._add_edge(my_id, b_id)
            self.pos += 1
            b_count += 1
        self._update_derivation('B', 'b' * b_count)
        return my_id

    def _update_derivation(self, from_sym, to_str):
        idx = self.working_string.find(from_sym)
        if idx != -1:
            self.working_string = self.working_string[:idx] + to_str + self.working_string[idx + 1:]
            self.derivation.append(self.working_string)

    def get_derivations(self):
        return self.derivation

    def to_dot(self):
        lines = [
            'digraph G {',
            '  rankdir=TB;',
            '  node [shape=circle, style=filled, fillcolor="#E0F7FA"];',
            '  edge [color="#00796B"];'
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
