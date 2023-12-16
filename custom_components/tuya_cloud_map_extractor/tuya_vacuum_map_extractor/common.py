def _hexStringToNumber(bits):
    number = []
    for i in [bits[i : i + 2] for i in range(0, len(bits), 2)]:
        number.append(int(i, 16))
    return number

def _chunk(In, n):
    out = []
    for i in [In[i : i + n] for i in range(0, len(In), n)]:
        out.append(i)
    return out

def _highLowToInt(high, low):
    return low + (high << 8)

def decode_header(header: str):
    maxmin = list(
        map(lambda x: _highLowToInt(x[0], x[1]), _chunk(_hexStringToNumber(header), 2))
    )
    return {
        "id": list(
            map(
                lambda x: _highLowToInt(x[0], x[1]),
                _chunk(_hexStringToNumber(header[2:6]), 2),
            )
        ),
        "version": _hexStringToNumber(header[0:2]),
        "roomeditable": True,
        "type": _hexStringToNumber(header[6:8]),
        "width": maxmin[2],
        "height": maxmin[3],
        "originx": maxmin[4],
        "originy": maxmin[5],
        "mapResolution": maxmin[6],
        "pileX": maxmin[7],
        "pileY": maxmin[8],
        "totalcount": int(header[36:44], 16),
        "compressbeforelength": int(header[36:44], 16),
        "compressafterlenght": maxmin[11],
        "calibrationPoints": [{
            'vacuum': {'x': 0, 'y': 0}, 
            'map': {'x': 0.0, 'y': -0.0}
        }, 
        {
            'vacuum': {'x': 0, 'y': 200}, 
            'map': {'x': 0.0, 'y': -20.0}
        }, 
        {
            'vacuum': {'x': 200, 'y': 0}, 
            'map': {'x': 20.0, 'y': -0.0}
        }]
    }