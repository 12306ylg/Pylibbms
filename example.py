import libbmsparse as parse
re=parse.Bms.parse("test.bms")
print(re.channel)

print(re.head)
print(re.info)