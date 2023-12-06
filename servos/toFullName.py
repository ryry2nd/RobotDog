from servos.ardSerial import skillFullName

reversedSkillFullName = {}

for d, data in skillFullName.items():
    reversedSkillFullName[data] = d

def shortToLong(st: str):
    return skillFullName.get(st.strip())

def longToShort(st: str):
    output = ''.join(x for x in st.title() if x.isalnum())
    return reversedSkillFullName.get((output[0].lower() + output[1:]))

def isWord(st: str):
    return st in reversedSkillFullName.keys()