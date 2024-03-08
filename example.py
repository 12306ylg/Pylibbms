from bms.parse import bms_parse
re=bms_parse(open("test.bms").read())
print(re.channel)
print(re.head)
print(re.info)