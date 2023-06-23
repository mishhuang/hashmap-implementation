# Name: Michelle Huang
# Description: a completed implementation of a HashMap using separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        updates the key/value pair in the hash map
        if the given key already exists in the hash map, its associated value is replaced with the new value
        if the given key does not exist in the hash map, a new key/value pair is added
        """
        # if load factor greater than or equal to 1, then resize table
        load_factor = self.table_load()
        if load_factor >= 1:
            self.resize_table(self.get_capacity()*2)

        # calculate hash value and find bucket index
        hash_value = self._hash_function(key)
        bucket_index = hash_value % self.get_capacity()

        # get linked list in bucket
        linked_list = self._buckets[bucket_index]

        # check if key already exists in linked list
        node = linked_list.contains(key)
        if node:
            node.value = value
        else:
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        returns the number of empty buckets in the hash table
        """
        # initialize variable
        empty_count = 0

        # access each bucket
        for index in range (self.get_capacity()):
            bucket = self._buckets[index]
            # check if bucket has linked list nodes or not
            if bucket.length() == 0:
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        returns the current hash table load factor
        """
        return self.get_size() / self.get_capacity()

    def clear(self) -> None:
        """
        clears out the contents of a hash table
        """
        for index in range(self._buckets.length()):
            self._buckets[index] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        changes the capacity of the internal hash table. all existing key/value pairs are transferred to the new hash
        map and all hash table links are rehashed
        if the new capacity is less than 1, nothing is done
        the new capacity must be a prime number, if it is not then it is changed to the next highest prime number
        """
        # check if new_capacity valid
        if new_capacity < 1:
            return

        # intialize variables
        new_ll = LinkedList()
        new_da = DynamicArray()

        # if the new capacity is not a prime number, set it to the next highest prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # initialize the new dynamic array with empty linked lists
        for index in range(new_capacity):
            new_da.append(LinkedList())

        # access hash table entries
        for pos in range(self.get_capacity()):
            entry = self._buckets[pos]
            if entry is not None:
                # acess nodes in entry
                for node in entry:
                    # inset node into the new linked list
                    new_ll.insert(node.key, node.value)

        # reset the size of the hash table
        self._size = 0
        # update the properties of the hash table
        self._buckets = new_da
        self._capacity = new_capacity

        # add each node to the hash table
        for node in new_ll:
            self.put(node.key, node.value)

    def get(self, key: str):
        """
        returns the value associated with the given key
        if the key does not exist in the hash map, returns None
        """
        hash_value = self._hash_function(key)
        bucket_index = hash_value % self.get_capacity()

        linked_list = self._buckets[bucket_index]
        node = linked_list.contains(key)

        if node:
            return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        returns true if the given key exists in the hashmap, and false otherwise
        an empty hash map does not contain any keys
        """
        hash_value = self._hash_function(key)
        bucket_index = hash_value % self.get_capacity()

        linked_list = self._buckets[bucket_index]
        node = linked_list.contains(key)

        return node is not None

    def remove(self, key: str) -> None:
        """
        removes the given key and its associated value from the hash map
        if the key does not exist in the hash map, then nothing done
        """
        hash_value = self._hash_function(key)
        bucket_index = hash_value % self.get_capacity()

        linked_list = self._buckets[bucket_index]
        remove = linked_list.remove(key)
        if remove:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map
        """
        # initialize new array
        new_da = DynamicArray()

        # access the bucket
        for index in range(self._buckets.length()):
            bucket = self._buckets[index]
            current = bucket._head
            while current:
                # add entries to new dynamic array
                new_da.append((current.key, current.value))
                current = current.next

        return new_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    returns a tuple of the mode values of the given dynamic array and the highest frequency
    if more than 1 value has the highest frequency, all values are included in the tuple's dynamic array
    the given dynamic array must contain at least one element and all values must be stored in the array as strings
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    for index in range(da.length()):
        value = da[index]
        if map.contains_key(value):
            map.put(value, map.get(value)+1)
        else:
            map.put(value, 1)

    # initialize variables
    mode = DynamicArray()
    max_frequency = 0

    # determine mode and its frequency
    for pos in range(map.get_capacity()):
        linked_list = map._buckets[pos]
        for node in linked_list:
            if node.value > max_frequency:
                max_frequency = node.value
                mode = DynamicArray([node.key])
            elif node.value == max_frequency:
                mode.append(node.key)

    return mode, max_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
