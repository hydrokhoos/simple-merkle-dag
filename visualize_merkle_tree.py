from graphviz import Digraph


def visualize_merkle_tree(root, dot=None):
    if dot is None:
        dot = Digraph(comment='Merkle Tree')

    if root is not None:
        dot.node(root.hash, label=root.hash[:20]+'...')
        for child in root.children:
            if child is not None:
                dot.node(child.hash, label=child.hash[:20]+'...')
                dot.edge(root.hash, child.hash)
                visualize_merkle_tree(child, dot)

    return dot
