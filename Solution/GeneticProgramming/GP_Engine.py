import random
import copy


# Phép chia an toàn (tránh lỗi Division by Zero)
def protected_div(left, right):
    return left / right if right != 0 else 1.0


# Các hàm toán học cốt lõi
FUNCTIONS = {
    '+': lambda l, r: l + r,
    '-': lambda l, r: l - r,
    '*': lambda l, r: l * r,
    '/': protected_div,
    'max': lambda l, r: max(l, r),
    'min': lambda l, r: min(l, r)
}

# Các biến trạng thái lấy từ xưởng sản xuất
TERMINALS = ['PT', 'DD', 'T', 'MFT', 'RO']


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def evaluate(self, state):
        if self.value in FUNCTIONS:
            return FUNCTIONS[self.value](self.left.evaluate(state), self.right.evaluate(state))
        elif self.value in TERMINALS:
            return state[self.value]
        else:
            return self.value

    def __str__(self):
        if self.value in FUNCTIONS:
            return f"({self.left} {self.value} {self.right})"
        return str(self.value)

    def get_depth(self):
        if self.left is None and self.right is None: return 1
        return 1 + max(self.left.get_depth() if self.left else 0, self.right.get_depth() if self.right else 0)


def generate_random_tree(max_depth, current_depth=1):
    if current_depth >= max_depth:
        return Node(random.choice(TERMINALS))

    if current_depth > 1 and random.random() < 0.3:
        return Node(random.choice(TERMINALS))

    func = random.choice(list(FUNCTIONS.keys()))
    left = generate_random_tree(max_depth, current_depth + 1)
    right = generate_random_tree(max_depth, current_depth + 1)
    return Node(func, left, right)


def crossover(tree1, tree2):
    t1_copy = copy.deepcopy(tree1)
    t2_copy = copy.deepcopy(tree2)

    def get_random_node(node):
        nodes = []

        def traverse(n):
            if n.left: nodes.append(n.left); traverse(n.left)
            if n.right: nodes.append(n.right); traverse(n.right)

        traverse(node)
        return random.choice(nodes) if nodes else node

    if t1_copy.left or t1_copy.right:
        node1 = get_random_node(t1_copy)
        node2 = get_random_node(t2_copy)
        node1.value, node2.value = node2.value, node1.value
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right

    return t1_copy, t2_copy


def mutate(tree, max_depth=4):
    t_copy = copy.deepcopy(tree)

    def traverse_and_mutate(node, current_depth):
        if node.left and node.right:
            if random.random() < 0.15:
                new_branch = generate_random_tree(max_depth, current_depth)
                node.value = new_branch.value
                node.left = new_branch.left
                node.right = new_branch.right
            else:
                traverse_and_mutate(node.left, current_depth + 1)
                traverse_and_mutate(node.right, current_depth + 1)

    traverse_and_mutate(t_copy, 1)
    return t_copy