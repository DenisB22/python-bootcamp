from singly_linked_list import Node, LinkedList


def merge_lists(first_list, second_list, merged_list):
    # 1 -> 3 -> 4 || 2 -> 7 -> 9 || 1 -> 2 -> 3 -> 4 -> None
    current_first = first_list.head
    current_second = second_list.head

    while True:
        if current_first is None:
            merged_list.insert_end(current_second)
            break

        if second_list is None:
            merged_list.insert_end(current_first)
            break

        if current_first.data < current_second.data:
            current_first_next = current_first.next
            current_first.next = None
            merged_list.insert_end(current_first)
            current_first = current_first_next

        else:
            current_second_next = current_second.next
            current_second.next = None
            merged_list.insert_end(current_second)
            current_second = current_second_next


# First List
node_one = Node(1)
node_two = Node(3)
node_three = Node(4)
first_list = LinkedList()
first_list.insert_end(node_one)
first_list.insert_end(node_two)
first_list.insert_end(node_three)

# Second List
node_four = Node(2)
node_five = Node(7)
node_six = Node(9)
second_list = LinkedList()
second_list.insert_end(node_four)
second_list.insert_end(node_five)
second_list.insert_end(node_six)

print("Printing First List: ")
first_list.print_list()
print("Printing Second List: ")
second_list.print_list()

merged_list = LinkedList()

merge_lists(first_list, second_list, merged_list)
del first_list
del second_list

print("Printing Merged List")
merged_list.print_list()