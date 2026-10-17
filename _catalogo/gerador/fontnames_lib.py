import struct, sys, os, json
def names_at(data, off):
    numTables = struct.unpack('>H', data[off+4:off+6])[0]
    tables = {}
    for i in range(numTables):
        tag, cs, toff, tlen = struct.unpack('>4sIII', data[off+12+16*i: off+28+16*i])
        tables[tag] = (toff, tlen)
    if b'name' not in tables: return {}
    toff, tlen = tables[b'name']
    fmt, count, stroff = struct.unpack('>HHH', data[toff:toff+6])
    res = {}
    for i in range(count):
        pid, eid, lid, nid, ln, o = struct.unpack('>HHHHHH', data[toff+6+12*i: toff+18+12*i])
        raw = data[toff+stroff+o: toff+stroff+o+ln]
        try:
            if pid == 3 or pid == 0: s = raw.decode('utf-16-be')
            elif pid == 1: s = raw.decode('mac_roman')
            else: continue
        except Exception: continue
        pri = 0 if (pid == 3 and lid == 0x409) else (1 if pid == 3 else 2)
        if nid not in res or pri < res[nid][0]: res[nid] = (pri, s)
    return {k: v[1] for k, v in res.items()}
