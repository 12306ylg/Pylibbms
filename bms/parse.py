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
            "subtitle": "",
            "bpm": {"mainbpm": 120.0},
            "playlevel": 0,
            "rank": 0,
            "total": 0,
            "volwav": 0,
            "lntype": 0,
            "tags": [],
            "wav": {},
            "stop": {},
            "bpm": {},
        }
        self.channel = {}
        self.info = []

    @classmethod
    def parse(cls, parse: str):
        global instance
        instance = Bms()

        for index, line in enumerate(parse.split("\n")):
            line = line.strip()
            header_matched = cls.pattern_header.match(line)
            data_matched = cls.pattern_data.match(line)
            if data_matched:
                try:
                    cls.parse_data(instance, data_matched)
                except Exception as e:
                    instance.info.append(f"(line:{index+1})Error in data parse: {e}")
            elif header_matched:
                try:
                    cls.parse_header(instance, header_matched)
                except Exception as e:
                    instance.info.append(f"(line:{index+1})Error in header parse: {e}")
        return instance

    @staticmethod
    def parse_header(instance, matched: re.Match[str]):
        field = matched.group("field")
        value = matched.group("value")
        if field == "BPM":
            try:
                instance.head["bpm"]["mainbpm"] = float(value)
            except (ValueError,TypeError):
                raise ValueError("The bpm value must be a number")
        elif field == "PLAYLEVEL":
            try:
                instance.head["playlevel"] = int(value)
            except (ValueError,TypeError):
                raise ValueError("The playlevel value must be a number")
        elif field == "RANK":
            try:
                instance.head["rank"] = int(value)
                if instance.head["rank"] < 0 or instance.head["rank"] > 4:
                    raise ValueError
            except (ValueError,TypeError):
                raise ValueError("Rank value is out of range[0-4]")
        elif field == "TOTAL":
            try:
                instance.head["total"] = int(value)
            except (ValueError,TypeError):
                raise ValueError("The total value must be a number")
        elif field == "VOLWAV":
            try:
                instance.head["volwav"] = int(value)

            except (ValueError,TypeError):
                raise ValueError("The volwav value must be a number")
            
        elif field == "LNTYPE":
            try:
                instance.head["lntype"] = int(value)
                if instance.head["lntype"] in range(1, 3) is False:
                    raise ValueError
            except (ValueError,TypeError):
                raise ValueError("The lntype value is out of range[1-2]")
        elif field == "TAGS":
            for tag in value.split("#"):
                instance.head["tags"].append(tag)
        elif field == "PY":
            instance.head["py"] = value.split(",")
        elif field.startswith("WAV"):
            instance.head["wav"][field[4:]] = value
        elif field.startswith("BMP"):
            instance.head["bmp"][field[4:]] = value
        elif field.startswith("STOP"):
            instance.head["stop"][field[4:]] = value
        elif field.startswith("BPM") and field != "BPM":
            try:
                instance.head["bpm"][field[4:]] = float(value)
            except (ValueError,TypeError):
                raise ValueError("The bpm value must be a number")

        else:
            instance.head[field.lower()] = value
        
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
            else:
                print("warn:cannot auto-get correct encoding")
                file = open(bmspath, encoding=bmscode)
            return file
