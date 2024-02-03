from servos.ardSerial import skillFullName

reversedSkillFullName = {}

for d, data in skillFullName.items():
    reversedSkillFullName[data] = d

def shortToLong(*st: str):
    for s in st:
        s = s.strip()
        if s in skillFullName.keys():
            return skillFullName.get(s.strip())
    return None

def longToShort(*st: str):
    for s in st:
        s = s.strip()
        if s in reversedSkillFullName.keys():
            output = ''.join(x for x in s.title() if x.isalnum())
            return reversedSkillFullName.get((output[0].lower() + output[1:]))

def isWord(*st: str):
    for s in st:
        if s.strip() in reversedSkillFullName.keys():
            return True
    return False