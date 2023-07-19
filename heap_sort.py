# Heap implementation

# MaxHeapify
def max_heapify(arr, n, i):
    # n -> size
    # i -> position
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Largest value so far is compared with left child
    if left < n and arr[largest] < arr[left]:
        largest = left

    # Largest value so far is compared with right child
    if right < n and arr[largest] < arr[right]:
        largest = right

    # Change the parent
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        # Recursive call
        max_heapify(arr, n, largest)


def heapsort(arr):
    for i in range(n - 1, 0, -1):
        # Swapp
        arr[i], arr[0] = arr[0], arr[i]
        max_heapify(arr, i, 0)


# Driver Code
arr = [2, 66, 30, 5, 9, 10]
n = len(arr)

# Build a max heap
for i in range(n // 2 - 1, -1, -1):
    max_heapify(arr, n, i)

heapsort(arr)
# Display
print("Sorted Array is")
for i in range(n):
    print(arr[i])
