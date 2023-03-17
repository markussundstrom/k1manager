from pathlib import Path
import io
from k1data import K1patch, K1library

def pr_peek(filebuffer, bytestoread):
    return (filebuffer.peek(bytestoread)[:bytestoread])

def read_bankfiles(infiles, k1library):
    for infile in infiles:
        bankfile = open(infile, "rb")
        while bankfile.peek(1) :
            if (pr_peek(bankfile, 1)) == b'\xF0':
                bankfile.seek(7, io.SEEK_CUR)
                if pr_peek(bankfile, 1) == b'\x00' or \
                   pr_peek(bankfile, 1) == b'\x20':
                    #single
                    bankfile.seek(1, io.SEEK_CUR)
                    while pr_peek(bankfile, 1) != b'\xF7':
                        datachunk = bankfile.read(88)
                        if len(datachunk) < 88:
                            break
                        patch = K1patch(datachunk, Path(infile).stem)
                        k1library.add_single(patch)
                elif pr_peek(bankfile, 1) == b'\x40':
                    #multi
                    while pr_peek(bankfile, 1) != b'\xF7':
                        datachunk = bankfile.read(76)
                        if len(datachunk) < 76:
                            break
                        patch = K1patch(datachunk, Path(infile).stem)
                        k1library.add_multi(patch)
                else:
                    print("error")
                    #pass#unexpected sysex format
            else:
                bankfile.seek(1, io.SEEK_CUR)
        #end while
        k1library.add_bankname(Path(infile).stem)
        bankfile.close()
