# node.py, methods and classes involved in representing an
# abstract keyspace.

# Tulip's keyspace can be abstractly thought of as ring
# where each point corresponds to a particular key.

# Both peers and artefacts they store exist as nodes,
# sharing a single keyspace.



from hashlib import sha256
from binascii import unhexlify
from random import randint



# Environment variables and other constant values.



# The string encoding used to store addresses.

CODEC = 'utf-8'

# The size of a SHA-256 hex digest in bytes.

SHASIZE = 64

# The size of the network's keyspace is dependent on the
# number of possible keys.

BASE = 16
KEYSIZE = 36

KEYSPACE = BASE ** KEYSIZE

# Endianess when dealing with byte data.

END = 'big'



# Miscaleneous functions for various purposes.



# Trauncate a string up to a given index. This is parhaps a
# little unnecessary.

def shorten(string, index):
    sub = string[:index]

    return sub



# Find the ordinal value of a particular address, its 
# position arround the keyspace ring.

def order(address):
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



# Derive the address for a given artefact. It will exist
# on the circle and within the keyspace.

def address(artefact):
    try:
        digest = hash(artefact)
    
    # If the artefact was invalid, do not proceed.

    except:
        return

    if digest:
        text = normalise(digest)

        return text



# Represents a peer or artefact on the network, assigned
# a key and artefact (if any).

class node:
    def __init__(self, artefact):
        self.bind(artefact)

        
        
    # Asociate the node with a particular piece of data.

    def bind(self, artefact):
        # Update the node's address based on the new data.

        self.address = address(artefact)
        self.artefact = artefact



    # Return the node's position on the keyspace ring.
   
    def __int__(self):
        return order(self.address)

    
    
    # Calculate the distance between two nodes via their
    # respective positions on the ring.

    def __sub__(self, node):
        delta = int(self) - int(node)

        return delta



    def __repr__(self):
        return self.address



# Generate a unique identifier for a peer node. Each 
# should be lenghty to avoid collision.

def uunode():
    name = bytes([
        randint(0, 255) 

        # Its name should be the same length as keyspace
        # addresses.

        for i in range(KEYSIZE)
    ])

    return node(name)



# Sort a list of nodes by distance from a target node.

def vote(target, nodes):
    votes = dict()

    for node in nodes:

        delta = abs(target - node)
        votes[delta] = node



    # The ditionary will be sorted by distance. Then, just
    # yield each node.

    for delta in sorted(votes):
        node = votes.get(delta)

        yield node
