import vobject
s = open("data.txt", "r")

vcard = vobject.readOne(s)
vcard.prettyPrint()
