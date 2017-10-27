import subprocess
import csv

from shutil import copyfile
from timeit import default_timer as timer

projectRoots = ["C:/prog/kotlin/kotlinTorrent/", "C:/prog/java/javaTorrent/"]
changeTargetFileRelative = ["src/main/java/torrent/Torrent.kt", "src/main/java/torrent/Torrent.java"]
changeFileLocation = [["Torrent_original.kt", "Torrent_cancel.kt"], ["Torrent_original.java", "Torrent_cancel.java"]]
iterationCount = 20

with open('results.csv', 'w', newline='') as csvfile:
    resultWriter = csv.writer(csvfile, delimiter=';')
    for rootIndex, root in enumerate(projectRoots):
        cleanTimes = []
        buildTimes = []
        subprocess.check_output("gradlew --no-daemon --no-build-cache --stop", cwd=root, shell=True)
        for x in range(iterationCount):
            start = timer()
            subprocess.check_output("gradlew --no-daemon --no-build-cache clean", cwd=root, shell=True)
            end = timer()
            cleanTimes.append(end - start)

            start = timer()
            subprocess.call("gradlew --no-daemon --no-build-cache assemble", cwd=root, shell=True)
            end = timer()
            buildTimes.append(end - start)
        resultWriter.writerow(projectRoots[rootIndex] + ["No-daemon, full build"])
        resultWriter.writerow(["clean"] + cleanTimes)
        resultWriter.writerow(["build"] + buildTimes)

    for root in projectRoots:
        cleanTimes = []
        buildTimes = []
        for x in range(iterationCount):
            start = timer()
            subprocess.call("gradlew --no-daemon --no-build-cache assemble", cwd=root, shell=True)
            end = timer()
            buildTimes.append(end - start)
        resultWriter.writerow(projectRoots[rootIndex] + ["No-daemon, no-change build"])
        resultWriter.writerow(["build"] + buildTimes)

    for rootIndex, root in enumerate(projectRoots):
        cleanTimes = []
        buildTimes = []

        #do a build before changing the file
        copyfile(changeFileLocation[rootIndex][1], root + changeTargetFileRelative[rootIndex])
        subprocess.call("gradlew --no-daemon --no-build-cache -Pkotlin.incremental=true assemble", cwd=root, shell=True)

        for x in range(iterationCount):
            copyfile(changeFileLocation[rootIndex][x % len(changeFileLocation[rootIndex])], root + changeTargetFileRelative[rootIndex])

            start = timer()
            subprocess.call("gradlew --no-daemon --no-build-cache -Pkotlin.incremental=true assemble", cwd=root, shell=True)
            end = timer()
            buildTimes.append(end - start)
        resultWriter.writerow(projectRoots[rootIndex] + ["No-daemon, incremental build"])
        resultWriter.writerow(["build"] + buildTimes)

    #with daemon
    for rootIndex, root in enumerate(projectRoots):
        subprocess.check_output("gradlew --stop", cwd=root, shell=True)
        subprocess.check_output("gradlew", cwd=root, shell=True)
        cleanTimes = []
        buildTimes = []
        for x in range(iterationCount):
            start = timer()
            subprocess.check_output("gradlew clean", cwd=root, shell=True)
            end = timer()
            cleanTimes.append(end - start)

            start = timer()
            subprocess.call("gradlew assemble", cwd=root, shell=True)
            end = timer()
            buildTimes.append(end - start)
        resultWriter.writerow(projectRoots[rootIndex] + ["full build"])
        resultWriter.writerow(["clean"] + cleanTimes)
        resultWriter.writerow(["build"] + buildTimes)

    for rootIndex, root in enumerate(projectRoots):
        subprocess.check_output("gradlew --stop", cwd=root, shell=True)
        subprocess.check_output("gradlew", cwd=root, shell=True)
        cleanTimes = []
        buildTimes = []
        for x in range(iterationCount):
            start = timer()
            subprocess.call("gradlew assemble", cwd=root, shell=True)
            end = timer()
            buildTimes.append(end - start)
        resultWriter.writerow(projectRoots[rootIndex] + ["no-change build"])
        resultWriter.writerow(["build"] + buildTimes)

    for rootIndex, root in enumerate(projectRoots):
        subprocess.check_output("gradlew --stop", cwd=root, shell=True)
        subprocess.check_output("gradlew", cwd=root, shell=True)
        cleanTimes = []
        buildTimes = []

        #do a build before changing the file
        copyfile(changeFileLocation[rootIndex][1], root + changeTargetFileRelative[rootIndex])
        subprocess.call("gradlew -Pkotlin.incremental=true assemble", cwd=root, shell=True)

        for x in range(iterationCount):
            copyfile(changeFileLocation[rootIndex][x % len(changeFileLocation[rootIndex])], root + changeTargetFileRelative[rootIndex])

            start = timer()
            subprocess.call("gradlew -Pkotlin.incremental=true assemble", cwd=root, shell=True)
            end = timer()
            buildTimes.append(end - start)
        resultWriter.writerow(projectRoots[rootIndex] + ["incremental build"])
        resultWriter.writerow(["build"] + buildTimes)