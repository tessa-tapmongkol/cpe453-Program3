import sys


# backing_store.seek(p * PAGE_SIZE + d, 0)
# ref_byte = backing_store.read(1)
# ref_byte_int = int.from_bytes(ref_byte, 'little', signed=True)
# https://www.geeksforgeeks.org/python-seek-function/ 


PAGE_SIZE = 256
TLB_SIZE = 16
TLB = []
PageTable = []
backingStore = []
Memory = []

def main(argv):
    FRAMES = 256
    PRA = "FIFO"

    backingStore = readBackingStoreFile("BACKING_STORE.bin")
    vAddresses = getVirtualAddresses(argv[0])
    
    for i in range(1, len(argv)):
        if argv[i].isnumeric():
            FRAMES = int(argv[i])
        elif argv[i] == "LRU" or argv == "OPT":
            PRA = argv[i]
            
    if PRA == "FIFO":
        FIFO(vAddresses, FRAMES)
    elif PRA == "OPT":
        OPT(vAddresses, FRAMES)
    else:
        LRU(vAddresses, FRAMES)
        
def readBackingStoreFile(filename):
    b_store = []
    file = open(filename,"rb")
    byte = file.read(256).hex()
    while byte:
        b_store.append(byte) 
        print(byte)
        byte = file.read(256).hex()
    file.close()
    return b_store


# Gets virtual addresses from user specified text file
def getVirtualAddresses(filename):
    vAddresses = []
    file = open(filename, "r")
    lines = file.readlines()
    for line in lines:
        vAddresses.append(int(line))
    file.close()
    return vAddresses

def isInTlb(virtual):
    return

def isInPageTable(virtual):
    return

def FIFO(vAddresses, frames):
    results = []
    pageHits = 0
    pageAccessed = 0
    tlbHits = 0
    tlbAccessed = 0
    frame = 0
    for virtual in vAddresses:
        # calculate page number and page offset
        pageNumber = virtual / PAGE_SIZE
        offset = virtual % PAGE_SIZE
        tlbAccessed += 1
        # Checks if virtual address is already stored in TLB
        if isInTlb(virtual):
            tlbHits += 1
            # Need to get byte at that offset
            byteValue = Memory[pageNumber]
            results.append(Reference_Sequence(virtual, byteValue, frame, Memory[pageNumber]))
            continue
        pageAccessed += 1
        if isInPageTable(virtual):
            pageHits += 1
            if len(TLB) > TLB_SIZE:
                TLB.pop(0)
            TLB.append(TLB_Entry(pageNumber, frame))
            # Need to get byte value at that offset
            byteValue = Memory[pageNumber]
            results.append(Reference_Sequence(virtual, byteValue, frame, Memory[pageNumber]))
            continue
        # FIFO page replacement alg
        else:
            if frame <= frames - 1:
                PageTable.append(PageTable_Entry(pageNumber, frame, 1))
            else:
                frame = 0
                PageTable.pop(0)
                PageTable.append(PageTable_Entry(pageNumber, frame, 1))
            Memory[pageNumber] = backingStore[pageNumber]
    exportReferenceSequence(results, pageHits, pageAccessed, tlbHits, tlbAccessed)

def exportReferenceSequence(results, pageHits, pageAccessed, tlbHits, tlbAccessed):
    for result in results:
        print(result)
    tlbMisses = tlbAccessed - tlbHits
    pageFaults = pageAccessed - pageHits

def OPT(vAddresses, frames):
    return

def LRU(vAddresses, frames):
    return

class TLB_Entry:
    def __init__(self, page, frame):
        self.page = page
        self.frame = frame

class PageTable_Entry:
    def __init__(self, page, frame, valid):
        self.page = page
        self.frame = frame
        self.valid = valid

class Reference_Sequence:
    def __init__(self, virtual, byteValue, frame, entireFrame):
        self.virtual = virtual
        self.byteValue = byteValue
        self.frame = frame
        self.entireFrame = entireFrame


# def processFile(filename):
#     try:
#         colnames = ["StLastName", "StFirstName", "Grade", "Classroom", "Bus", "GPA", "TLastName", "TFirstName"]
#         dataset = pd.read_csv(filename, names=colnames, header=None)
#         return dataset
#     except IOError:
#         print('Error: students.txt could not be found in current directory.\nExiting program :)')
#         sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
