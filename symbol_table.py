
class SymbolTable:
    def __init__(self, size=101):
        # initialize the hash table
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash(self, value):
        # calculate the hash position
        return sum(ord(char) for char in value) % self.size

    def add(self, value):
        # find the hash position
        position = self.hash(value)

        # check if the value already exists
        for index, existing_value in enumerate(self.table[position]):
            if existing_value == value:
                return (position, index)

        # insert the new value
        self.table[position].append(value)
        return (position, len(self.table[position]) - 1)

    def search(self, value):
        # search for a value in the table
        position = self.hash(value)

        for index, existing_value in enumerate(self.table[position]):
            if existing_value == value:
                return (position, index)

        return None

    def display(self):
        # display all stored symbols
        for position, bucket in enumerate(self.table):
            for index, value in enumerate(bucket):
                print(f"{value} -> ({position}, {index})")


# test the symbol table
if __name__ == "__main__":
    st = SymbolTable()

    st.add("sum")
    st.add("average")
    st.add("grade")
    st.add("sum")
    st.add("mus")

    print("SYMBOL TABLE:")
    st.display()

    print("\nSEARCH RESULTS:")
    print("sum:", st.search("sum"))
    print("count:", st.search("count"))
