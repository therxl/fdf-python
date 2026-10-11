import struct
import zlib

width, height = 800, 500
pixels = bytearray()
for y in range(height):
    pixels.append(0)
    for x in range(width):
        r = int(40 + (x / width) * 120)
        g = int(50 + (y / height) * 150)
        b = int(100 + (x / width) * 100)
        pixels.extend((r, g, b))


def chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

raw = b''.join(b'\x00' + bytes(pixels[y * width * 3:(y + 1) * width * 3]) for y in range(height))
img = b'\x89PNG\r\n\x1a\n'
img += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
img += chunk(b'IDAT', zlib.compress(raw, 9))
img += chunk(b'IEND', b'')
with open(r'c:\Users\Администратор\Desktop\лаба1\docs\screenshot.png', 'wb') as f:
    f.write(img)
print('created screenshot.png')
