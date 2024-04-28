import hashlib

from visualize_merkle_tree import visualize_merkle_tree


NUM_CHILDREN = 2

class MerkleNode:
    def __init__(self, data: bytes):
        self.data = data
        self.hash = self._calculate_hash(data)
        self.children = [None] * NUM_CHILDREN

    def _calculate_hash(self, data: bytes):
        return hashlib.sha256(data).hexdigest()

def build_merkle_tree(segments: bytearray) -> MerkleNode:
    if len(segments) == 0:
        return None

    nodes = [MerkleNode(segment) for segment in segments]

    while len(nodes) > 1:
        new_level = []
        for i in range(0, len(nodes), NUM_CHILDREN):
            children = nodes[i:i+NUM_CHILDREN]
            combined_data = b''.join(child.data for child in children if child is not None)
            combined_hash = b''.join(child.hash.encode() for child in children if child is not None)
            parent_node = MerkleNode(combined_data)
            parent_node.children = children
            parent_node.hash = hashlib.sha256(combined_hash).hexdigest()
            new_level.append(parent_node)
        nodes = new_level

    return nodes[0]


def retrieve_data(root: MerkleNode) -> bytes:
    if root is None:
        return b''

    if all(child is None for child in root.children):
        return root.data

    child_data = b''.join(retrieve_data(child) for child in root.children if child is not None)
    return child_data


if __name__ == '__main__':
    with open('internet_god.png', 'rb') as f:
        data = f.read()
    segments = []
    segment_size = 10 * 1024
    for i in range(0, len(data), segment_size):
        segments.append(data[i:i+segment_size])

    root = build_merkle_tree(segments)
    print("Root hash:", root.hash)

    with open('output.png', 'wb') as f:
        f.write(retrieve_data(root))

    dot = visualize_merkle_tree(root)
    dot.render('merkleDAG', format='png', cleanup=True)
