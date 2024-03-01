class bms_edit:
    def __init__(self, file_path: str, encoding: str = "utf-8"):
        import parse
        self.bms = parse.Bms.parse(open(file_path, "r", encoding=encoding).read())
        self.file_path = file_path
        self.encoding = encoding
    def update_header(self,key: str, value: str):
        self.bms.head[key] = value
    def update_channel(self,channel: str, value: str):
        self.bms.channel[channel] = value
    def write(self):
        file=open(self.file_path, "w", encoding=self.encoding)
        bms=""
        for head in self.bms.head.items():
            if (head[0]=="wav"or head[0]=="bmp" or head[0]=="stop"or head[0]=="bpm") is False:
                print(head[0])
                bms+=f"#{head[0].upper()} {str(head[1])}\n"
            else:
                for i in head[1].items():
                    print(i)
                    bms+=f"#{head[0].upper()}{i[0]if len(i[0])==2 else f"0{i[0]}"} {str(i[1])}\n"
        for channel in self.bms.channel.items():
            bms+=f"#{channel[0]}:{channel[1]}\n"
        file.write(bms)
if __name__ == "__main__":
    bb=bms_edit("test.bms")
    bb.update_header("title", "new_title")
    bb.write()
