from bms.parse import bms_parse_low_level
from bms.edit import bms_edit
re=bms_parse_low_level(open("test.bms").read())
print(re.channel)
print(re.head)
print(re.info)
bms_edit("test.bms").write()
