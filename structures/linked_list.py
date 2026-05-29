#linked_list

class Node(object):
    def __init__(self, data, next=None, previous=None):
        self.data = data
        self.next = next
        self.previous = previous

class DoublyLinkedList(object):
    def __init__(self):
        self.head = None

    def insertAtEnd(self, data):
        newNode = Node(data)
        temp = self.head
        if temp is None:
            self.head = newNode
            return
        while temp.next != None:
            temp = temp.next
        temp.next = newNode
        newNode.previous = temp

    def get_all_logs(self):
        logs = []
        temp = self.head
        while temp is not None:
            logs.append(temp.data)
            temp = temp.next
        return logs