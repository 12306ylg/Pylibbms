import bms.parse as parse
re=parse.Bms.parse(open("test.bms").read())
print(re.channel)
print(re.head)
print(re.info)