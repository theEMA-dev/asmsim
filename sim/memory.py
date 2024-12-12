class Memory:
    def __init__(self, size=512):
        # Initialize memory as a byte array
        self.memory = bytearray(size)

    def load(self, address, value):
        """Load a value into memory at the given address."""
        self.memory[address:address + 4] = value.to_bytes(4, 'big')

    def fetch(self, address):
        """Fetch a value from memory at the given address."""
        return int.from_bytes(self.memory[address:address + 4], 'big')
