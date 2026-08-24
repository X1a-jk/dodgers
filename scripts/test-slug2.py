name='Jonathan Hernández'
print([c for c in name])
print([hex(ord(c)) for c in name])
s=''
for c in name.lower().replace(' ','-').replace("'",'').replace('.',''):
    if ('a' <= c <= 'z') or ('0' <= c <= '9') or c == '-':
        s += c
    else:
        print('removed', repr(c))
print('slug:', repr(s))
