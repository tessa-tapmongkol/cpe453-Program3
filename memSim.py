from audioop import add
from cgi import print_arguments
import sys

PAGE_SIZE = 2
TLB_SIZE = 16

class StatTracker:
    def __init__(self):
        self.num_trans_addrs = 0
        self.page_hits = 0
        self.page_accesses = 0
        self.tlb_hits = 0
        self.tlb_accesses = 0
        
    def incTLBHits(self):
        self.tlb_hits += 1
        
    def incTLBAccesses(self):
        self.tlb_accesses += 1
        
    def incPageHits(self):
        self.page_hits += 1
        
    def incPageAccesses(self):
        self.page_accesses += 1
        
    def incNumTransAddresses(self):
        self.num_trans_addrs += 1
        
    def printSummary(self):
        print(F"Number of Translated Addresses = {self.num_trans_addrs}")
        print(F"Page Faults = {self.page_accesses - self.page_hits}")
        print(F"Page Fault Rate = {(self.page_accesses - self.page_hits) / self.page_accesses}")
        print(F"TLB Hits = {self.tlb_hits}")
        print(F"TLB Misses = {self.tlb_accesses - self.tlb_hits}")
        print(F"TLB Hit Rate = {self.page_hits / self.tlb_accesses}")

class PhysicalMemory:
    def __init__(self, nf):
        self.memory = [None] * nf
        self.num_frames = nf
        self.length = 0
    
    def setFrame(self, frame_num, data):
        self.memory[frame_num] = data
    
    def getNumFrames(self):
        return self.num_frames
        
    def isFull(self):
        return None not in self.memory
            
    def getLength(self):
        return self.length
    
    def setLength(self, num):
        self.length = num
        
    def getMemory(self):
        return self.memory
             
class TLB:
    def __init__(self):
        self.tlb = {}

    def addEntry(self, page, frame):
        if len(self.tlb.keys()) == TLB_SIZE:
            self.tlb.pop(list(d.keys()).pop(0))
        self.tlb.update({page : frame})  
            
    def is_empty(self):
        return len(self.tlb.keys()) == 0
    
    def findPage(self, page):
        return page in self.tlb.keys()
    
    def getFrame(self, page):
        return self.tlb[page]
    
    def remEntry(self, page):
        self.tlb.pop(page, None)

class PageTable:
    def __init__(self):
        self.pt = {}

    def updateEntry(self, page, frame, v_bit):
        self.pt.update({tuple((page , frame)) :  v_bit})      
    
    def findEntry(self, page):
        for entry in self.pt.items():
            if entry[0][0] == page and entry[1] == 1:
                return True
        return False
    
    def getValidBit(self, page, frame):
        return self.pt.get(page, frame)     
    
    def setValidBit(self, page, frame, bit):
        self.pt.update({tuple((page, frame)): bit})    
        
    def getFrame(self, page):
        for entry in self.pt.items():
            if entry[0][0] == page and entry[1] == 1:
                return entry[0][1]
            
    def getPage(self, frame):
        for entry in self.pt.items():
            if entry[0][1] == frame and entry[1] == 1:
                return entry[0][0]
    
    def pop(self):
        return self.pt.popitem()
    
    def isFull(self):
        return len(self.pt) >= PAGE_SIZE
      
def printHeader(address, frame, mem):
    page_num = address // PAGE_SIZE
    offset = address % PAGE_SIZE
    referenced_byte = accessBackingStore(PAGE_SIZE * page_num + offset, 1)
    rbyteInteger = int.from_bytes(referenced_byte, 'little', signed=True)
    print(F"{address}, {rbyteInteger}, {frame},")
    print(mem.getMemory()[frame].hex().upper())
    
# Given a byte offset and number of bytes to read,
# opens Backing Store, moves file descriptor to offset
# and reads the number of bytes from the offset
def accessBackingStore(offset, num_of_bytes):
    file = open("BACKING_STORE.bin","rb")
    file.seek(offset, 0)
    bytes_read = file.read(num_of_bytes)
    file.close()
    return bytes_read

# Gets virtual addresses from user specified text file
def getVirtualAddresses(filename):
    vAddresses = []
    file = open(filename, "r")
    lines = file.readlines()
    for line in lines:
        vAddresses.append(int(line))
    file.close()
    return vAddresses


def LRU(vAddresses, tlb, pt, mem, stats):
    lru_tracker = list(range(0,mem.getNumFrames()))
    for vAddress in vAddresses:
        frame = processAddressLRU(vAddress, tlb, pt, mem, lru_tracker, stats)
        printHeader(vAddress, frame, mem)
    stats.printSummary()
        
def updateLRUTracker(lru_tracker, tlb, page):
    lru_frame = lru_tracker.remove(tlb.getFrame(page))
    lru_tracker.insert(0,lru_frame)

def processAddressLRU(vAddress,  tlb, pt, mem, lru_tracker, stats):
    page = vAddress // PAGE_SIZE
    stats.incTLBAccesses()
    
    if(tlb.findPage(page)):
        updateLRUTracker(lru_tracker, tlb, page)
        stats.incTLBHits()
        return  tlb.getFrame(page)
    
    stats.incPageAccesses()
    
    if(pt.findEntry(page)):
        updateLRUTracker(lru_tracker, tlb, page)
        stats.incPageHits()
        tlb.addEntry(page, pt.getFrame(page))
        return pt.getFrame(page)

    upd_frame = mem.getLength()
    
    if(mem.isFull()):
        upd_frame = lru_tracker.pop()
        lru_tracker.insert(0, upd_frame)
        remPage = pt.getPage(upd_frame)
        pt.updateEntry(remPage, upd_frame, 0) 
        tlb.remEntry(remPage)

    tlb.addEntry(page, upd_frame)
    pt.updateEntry(page, upd_frame, 1)
    mem.setFrame(upd_frame, accessBackingStore(PAGE_SIZE * page, 256))
    mem.setLength(mem.getLength() + 1)
    stats.incNumTransAddresses()
    
    return upd_frame

        
def FIFO(vAddresses, tlb, pt, mem, stats):
    fifo_tracker = list(range(0, mem.getNumFrames()))
    for vAddress in vAddresses:
        frame = processAddressFIFO(vAddress, tlb, pt, mem, stats, fifo_tracker)
        printHeader(vAddress, frame, mem)
    stats.printSummary()

def processAddressFIFO(vAddress, tlb, pt, mem, stats, fifo_tracker):
    page = vAddress // PAGE_SIZE
    stats.incTLBAccesses()
    
    if(tlb.findPage(page)):
        stats.incTLBHits()
        return  tlb.getFrame(page)
    
    stats.incPageAccesses()
    
    if(pt.findEntry(page)):
        stats.incPageHits()
        tlb.addEntry(page, pt.getFrame(page))
        return pt.getFrame(page)

    upd_frame = mem.getLength()

    if(mem.isFull()):
        upd_frame = fifo_tracker.pop(0)
        fifo_tracker.append(upd_frame)
        remPage = pt.getPage(upd_frame)
        pt.updateEntry(remPage, upd_frame, 0) 
        tlb.remEntry(remPage)

    if pt.isFull():
        pt_entry = pt.pop()
        if pt_entry[1] == 1:
            tlb.remEntry(pt_entry[0][0])

    tlb.addEntry(page, upd_frame)
    pt.updateEntry(page, upd_frame, 1)
    mem.setFrame(upd_frame, accessBackingStore(PAGE_SIZE * page, 256))
    mem.setLength(mem.getLength() + 1)
    stats.incNumTransAddresses()
    
    return upd_frame

def OPT(vAddresses, tlb, pt, mem, stats):
    return

def main(argv):
    FRAMES = 256
    PRA = "FIFO"
    stats = StatTracker()
    tlb = TLB() 
    page_table = PageTable()
    vAddresses = getVirtualAddresses(argv[0])
        
    for i in range(1, len(argv)):
        if argv[i].isnumeric():
            FRAMES = int(argv[i])
        elif argv[i] == "LRU" or argv == "OPT":
            PRA = argv[i]
            
    mem = PhysicalMemory(FRAMES)
            
    if PRA == "FIFO":
        FIFO(vAddresses, tlb, page_table, mem, stats)
    elif PRA == "OPT":
        OPT(vAddresses, tlb, page_table, mem, stats)
    else:
        LRU(vAddresses, tlb, page_table, mem, stats)

if __name__ == "__main__":
    main(sys.argv[1:])    