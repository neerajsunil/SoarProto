import os
import time

def TelemetryLogger(filename, dataPair):

    os.makedirs("TeleLogs/", exist_ok=True)

    file_path = os.path.join("TeleLogs/", filename)

    file_exists = os.path.exists(file_path)

    logFile = open(file_path, "a" if file_exists else "w")

    if not file_exists:
        logFile.write("time " + " ".join(dataPair.keys()) + "\n")

    logFile.write(str(time.time()) + " ")

    for key in dataPair:
      logFile.write(str(dataPair[key]) + " ")

    logFile.write("\n")
    logFile.close()
