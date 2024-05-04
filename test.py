from datetime import datetime

line = "LOG  : General     , 1714824465202> 1,208,208,614> CheckModsNeedUpdate: Mods updated"

def splitLine(line: str) -> tuple[datetime, str]:
        """Split a log line into a timestamp and the remaining message"""
        timestampStr, trash, message = line.strip()[1:].split(">", 2)

        # Ignore the start of the message before the timestamp
        timestampStr = timestampStr[timestampStr.find(",", 2) + 1 :]
        timestampStr = timestampStr.translate({ord(' '): None}) #fix unknown space issue

        return timestampStr, message
        #timestamp = datetime.strptime(timestampStr, "%d-%m-%y %H:%M:%S.%f")
        #return timestamp, message
message = splitLine(line)
print(message)
#print(timestampStr)