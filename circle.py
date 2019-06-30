# circle.py, methods and classes involved in representing
# the network's identifier circle.

# Tulip's entire keyspace is arranged around the circle's
# circumference. Hence each point stores a particular key
# (or address).

# Moreover, both peers and artefacts share this space, 
# which yields a Named Data Network.

# Written by, Kale Champagnie <kjchampagnie@gmail.com>



from hashlib import sha256
from binascii import unhexlify



# Environment variables and other constant values.



# The string encoding used to store addresses.

CODEC = 'utf-8'

# The size of a SHA-256 hex digest in bytes.

SHASIZE = 64

# The size of the network's keyspace is dependent on the
# number of possible keys.

BASE = 16
KEYSIZE = 48

KEYSPACE = BASE ** KEYSIZE

# Endianess when dealing with byte data.

END = 'big'



# Miscaleneous functions for various purposes.



# Trauncate a string up to a given index. This is parhaps a
# little unnecessary.

def shorten(string, index):
    sub = string[:index]

    return sub



# Convert an address to an integer. This is required when
# calculating node distance.

def atoi(address):
    # Convert the hexadecimal address into a raw digest.

    bytes = unhexlify(address)
    value = int.from_bytes(bytes, END)

    return value



# Override the builting hash funciton with SHA-256 hashing.

def hash(artefact):
    # If the given piece of data is not bytes, encode it.

    if not isinstance(artefact, bytes):
        artefact = artefact.encode()

    sha = sha256(artefact)
    digest = sha.hexdigest()

    return digest



# Perform normalisation on a given SHA-256 digest. This 
# ensures all addresses adhere to the same format.

def normalise(digest):
    # Ensure the digest is of correct length.

    if len(digest) != SHASIZE:
        return 

    # Trauncate the digest to produce an address within
    # the keyspace.

    address = shorten(digest, KEYSIZE)

    return address



# Derive the address for a given artefact. IT will exist
# on the circle and within the keyspace.

def derive(artefact):
    try:
        digest = hash(artefact)
    
    # If the artefact was invalid, do not try and normalise
    # the digest.

    except:
        return

    if digest:
        string = normalise(digest)

        return string



# Represents an address arround the circle. An address
# inherits from the string class.

class address(str):
    def __new__(self, artefact):
        # Allow the address to be directly accessed as a
        # string.

        return derive(artefact)

    # Convert the address to raw bytes.



# Represents the data asociated with a particular point
# arround the circle. Namely, its address and artefact.

class node:
    def __init__(self, artefact):
        self.bind(artefact)

    # Asociate the node with a particular piece of data.

    def bind(self, artefact):
        # Update the node's address based on the new data.

        self.address = address(artefact)
        self.artefact = artefact

    # When a node is subject to int(), it will return the
    # integer value of its address.

    def __int__(self):
        return atoi(self.address)



# Calculate the distance between two nodes using their
# addresses.

# Distance can be calculated in a number of ways. Here, it
# is found as the numerical difference in addresses.

def delta(a, b):
    return int(a) - int(b)
