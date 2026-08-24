import re
name='Jonathan Hernández'
slug=re.sub(r'[^a-z0-9-]','',name.lower().replace(' ','-').replace("'",'').replace('.',''))
print(repr(slug))
