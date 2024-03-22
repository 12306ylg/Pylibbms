"""
WIP...
"""


class bms_edit:

    def __init__(self, file_path: str, encoding: str = "utf-8"):
        from bms import parse

        # 初始化bms_edit类，传入文件路径和编码格式
        self.bms = parse.bms_parse_low_level(
            open(file_path, "r", encoding=encoding).read()
        )
        self.file_path = file_path
        self.encoding = encoding

    def update_header(self, key: str, value: str):
        # 更新头信息
        self.bms.head[key] = value

    def update_channel(self, channel: str, value: str):
        # 更新通道信息
        self.bms.channel[channel] = value

    def delete_channel(self, channel: str):
        # 删除通道信息
        if channel in self.bms.channel:
            del self.bms.channel[channel]
        else:
            raise KeyError(f"Channel '{channel}' does not exist.")

    def write(self):
        # 将更改后的信息写入文件
        file = open(self.file_path, "w", encoding=self.encoding)
        bms = ""
        for head in self.bms.head.items():
            print(head[0])
            bms += f"#{head[0].upper()} {str(head[1])}\n"
        for channel in self.bms.channel.items():
            bms += f"#{channel[0]}:{channel[1]}\n"
        file.write(bms)
