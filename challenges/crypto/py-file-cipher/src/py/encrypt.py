class Encrypt:
    def __init__(self, key):
        self.key = key

    def do(self, data):
        for i in range(len(data)):
            data[i] = ~(~data[i] ^ self.key[i % len(self.key)])
        return data
