import re
import chardet

detector = chardet


class Bms(object):
    pattern_header = re.compile(
        r"#(?P<field>\S+)(?:\s(?P<value>.*))?",
    )

    pattern_data = re.compile(
        r"#(?P<bar>\d{3})" "(?P<channel>[0-9a-f]{2}):" "(?P<data>.*)$", re.IGNORECASE
    )

    def __init__(self):
        self.head = {
            "title": "New song",
            "subtitle": "",
            "artist": "None",
            "genre": "None",
            "playlevel": "1",
            "subtitle": "",
            "copyright": "",
            "bpm": {"mainbpm": 120.0},
            "tags": [],
            "wav": {},
            "stop": {},
            "bpm": {},
            "bars": {},
            "run_pyscript": "no",
            "py": [],
        }
        self.channel = {}
        self.info = []

    @classmethod
    def parse(cls, fileparse: str):
        global instance
        instance = Bms()
        fileparse = Bms.pre(fileparse).read()
        for line in fileparse.split("\n"):
            line = line.strip()
            header_matched = cls.pattern_header.match(line)
            data_matched = cls.pattern_data.match(line)
            if data_matched:
                try:
                    cls.parse_data(instance, data_matched)
                except Exception as e:
                    instance.info.append(f"Error in data parse: {e}")
            elif header_matched:
                try:
                    cls.parse_header(instance, header_matched)
                except Exception as e:
                    instance.info.append(f"Error in header parse: {e}")
        if instance.head["run_pyscript"] == "yes":
            try:
                for script in instance.head["py"]:
                    exec(script)
            except Exception as e:
                instance.info.append(f"Error in python script: {e}")
        return instance

    @staticmethod
    def parse_header(instance, matched: re.Match[str]):
        field = matched.group("field")
        value = matched.group("value")
        if field == "BPM":
            try:
                instance.header["bpm"]["mainbpm"] = float(value)
            except ValueError:
                instance.header["bpm"]["mainbpm"] = 120.0
        elif field == "PLAYLEVEL":
            try:
                instance.playlevel = int(value)
            except ValueError:
                instance.playlevel = 0
        elif field == "RANK":
            try:
                instance.rank = int(value)
            except ValueError:
                instance.rank = 0
        elif field == "TOTAL":
            try:
                instance.total = int(value)
            except ValueError:
                instance.total = 0
        elif field == "VOLWAV":
            try:
                instance.volwav = int(value)
            except ValueError:
                instance.volwav = 0
        elif field == "LNTYPE":
            try:
                instance.lntype = int(value)
            except ValueError:
                instance.lntype = 0
        elif field == "TAGS":
            for tag in value.split("#"):
                instance.header["tags"].append(tag)
        elif field == "py":
            instance.header["py"] = value.split(",")
        elif field.startswith("WAV"):
            instance.header["wav"][field[4:]] = value
        elif field.startswith("BMP"):
            instance.header["bmp"][field[4:]] = value
        elif field.startswith("STOP"):
            instance.header["stop"][field[4:]] = value
        elif field.startswith("BPM") and field != "BPM":
            instance.header["bpm"][field[4:]] = value

        else:
            instance.header[field.lower()] = value
        sortcache = [{}, {}, {}, {}]
        for key in sorted(instance.header["wav"][key]):
            sortcache[0][key] = instance.header["wav"][key]
        for key in sorted(instance.header["bmp"][key]):
            sortcache[1][key] = instance.header["bmp"][key]
        for key in sorted(instance.header["stop"][key]):
            sortcache[2][key] = instance.header["stop"][key]
        for key in sorted(instance.header["bpm"][key]):
            sortcache[3][key] = instance.header["bpm"][key]
        instance.header["wav"] = sortcache[0]
        instance.header["bmp"] = sortcache[1]
        instance.header["stop"] = sortcache[2]
        instance.header["bpm"] = sortcache[3]
        return instance

    def parse_data(instance, matched):
        channel = matched.group("channel")
        bar = matched.group("bar")
        data = matched.group("data")
        try:
            instance.channel[channel]
        except KeyError:
            instance.channel[channel] = []
        instance.channel[channel].append([bar, data])
        return instance

    def pre(bmspath):
        with open(bmspath, "rb") as parsefilepre:
            bmscode = detector.detect(parsefilepre.read())
            if bmscode["confidence"] >= 0.50:
                if bmscode["encoding"] == "Windows-1252":
                    bmscode["encoding"] = "Shift-jis"
                file = open(bmspath, encoding=bmscode["encoding"])
                print(bmscode)
                return file
            else:
                print("cannot autoget encoding")
                bmscode = input("encoding:")
                file = open(bmspath, encoding=bmscode)
                return file
