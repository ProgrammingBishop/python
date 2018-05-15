'''

### Breadth-First:

if tree = null
    return
    
Queue q

q.enqueue(tree)

while not q.empty()
    node = q.dequeue()
    
    print(node)
    
    if node.left != null
        q.enqueue(node.left)

'''