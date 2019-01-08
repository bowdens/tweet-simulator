from datetime import datetime
import threading

defaultTF = "%e-%b-%Y %T.%f"

class StaticLog():
    def log(s):
        print("{}\t{}".format(datetime.now().strftime(defaultTF), s))

class Log():
    def __init__(self, timeFormat=defaultTF):
        Log.lockLog = threading.Lock()
        self.timeFormat = timeFormat

    def getTime(self):
        return datetime.now().strftime(self.timeFormat)

    def log(self, s):
        Log.lockLog.acquire()
        print("{}\t{}".format(self.getTime(), s))
        Log.lockLog.release()

class FileLog(Log):
    def __init__(self, timeFormat=defaultTF, f="log.txt"):
        super().__init__(timeFormat=timeFormat)
        self.file=f
        self.log("OPENED NEW LOG\n")

    def log(self, s):
        Log.lockLog.acquire()
        f = open(self.file, "a")
        line = "{}\t{}\n".format(self.getTime(), s.replace("\n", "\n\t"))
        f.write(line)
        f.close()
        print(line)
        Log.lockLog.release()


