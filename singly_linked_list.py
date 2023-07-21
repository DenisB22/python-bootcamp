# Create nodes

# Create linked list

# Add nodes to linked list

# Print linked list

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def is_list_empty(self):
        if self.head is None:
            return True
        else:
            return False

    def list_length(self):
        current_node = self.head
        length = 0
        while current_node is not None:
            length += 1
            current_node = current_node.next
        return length

    def insert_head(self, new_node):
        # data => Matthew, next => None
        temporary_node = self.head  # John
        self.head = new_node  # Matthew
        self.head.next = temporary_node
        del temporary_node

    def insert_end(self, new_node):
        # head => John -> None
        if self.head is None:
            self.head = new_node
        else:
            # head => John -> Ben -> None || John -> Matthew
            last_node = self.head
            while True:
                if last_node.next is None:
                    break
                last_node = last_node.next
            last_node.next = new_node

    def insert_at(self,new_node, position):
        # head => 10 -> 20 -> None || new_node => 15 -> None || position => 1
        if position < 0 or position > self.list_length():
            print("Invalid position")
            return

        if position == 0:
            self.insert_head(new_node)
            return

        current_node = self.head  # 10, 20
        current_position = 0  # 0, 1
        while True:
            if current_position == position:
                previous_node.next = new_node
                new_node.next = current_node
                break
            previous_node = current_node
            current_node = current_node.next
            current_position += 1

    def delete_head(self):
        if self.is_list_empty() is False:
            previous_head = self.head
            self.head = previous_head.next
            previous_head.next = None

            print(self.head.data)
        else:
            print("Linked list is empty. Delete failed.")



    def delete_at(self, position):
        if position < 0 or position > self.list_length():
            print('Invalid position')
            return

        if self.is_list_empty() is False:
            if position == 0:
                self.delete_head()

            current_node = self.head
            current_position = 0

            while True:
                if current_position == position:
                    previous_node.next = current_node.next
                    current_node.next = None
                    del current_node
                    # print(previous_node.data)
                    break
                previous_node = current_node
                current_node = current_node.next
                current_position += 1

                # print(f"Previous Node: {previous_node.data}")
                # print(f"Current Node: {current_node.data}")

    def delete_end(self):
        # head => John -> Ben -> Matthew
        last_node = self.head
        while last_node.next is not None:
            previous_node = last_node
            last_node = last_node.next
        previous_node.next = None

    def print_list(self):
        # head => John -> Ben -> Matthew -> None
        if self.head is None:
            print("List is empty")
            return

        current_node = self.head
        while True:
            if current_node is None:
                break
            print(current_node.data)
            current_node = current_node.next


# Node => data, next
# first_node.data => John, first_node.next => None
first_node = Node("John")
linked_list = LinkedList()
linked_list.insert_end(first_node)
second_node = Node("Ben")
linked_list.insert_end(second_node)
third_node = Node("Matthew")
# linked_list.insert_head(third_node)
linked_list.insert_end(third_node)
fourth_node = Node("Peter")
linked_list.insert_end(fourth_node)
# linked_list.delete_end()
linked_list.print_list()
print('----------------')
linked_list.delete_head()
# linked_list.delete_at(2)
print('----------------')
linked_list.print_list()
