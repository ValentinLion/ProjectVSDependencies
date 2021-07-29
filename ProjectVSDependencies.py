import os
import re
import sys
import csv
from collections import Counter

def extractDirectoryName():
    
    directory = "."
    if(len(sys.argv) >= 2):
        directory = sys.argv[1]

    return directory

def listingProjectFilesInDirectory(directory):

    projectFiles = []

    for filename in os.scandir(directory):
        if filename.is_file():
            if(filename.name.endswith('.vcxproj')):
                projectFiles.append(filename)
        else:
           projectFiles.extend(listingProjectFilesInDirectory(filename))
        
    return projectFiles
    
    
def extractDependencies(projectFiles):

    dependencies = {}

    pattern = re.compile(r"\\([^\\]*.props)\"")

    for file in projectFiles:
    
        dependenciesOfThisFile = []
    
        for line in open(file):
            for match in re.finditer(pattern, line):
                 dependenciesOfThisFile.append(match.group(1))
        
        dependencies[file.name] = dependenciesOfThisFile
    
    return dependencies

def writeDependenciesToCSV(dependencies):
    
    with open('projectVSDependencies.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
                                
        for project, projectDependencies in dependencies.items():
            
            spamwriter.writerow([project,""])

            counter = Counter(projectDependencies)
                        
            for project,count in counter.most_common():
                if count > 1:
                    text = "WARNING " + project + " " + str(count) + " times" 
                    spamwriter.writerow([text, ""])
 
            for dependencie in projectDependencies:
                spamwriter.writerow(["",dependencie])
                
            spamwriter.writerow(["",""])


directoryName = extractDirectoryName()     
projectFiles = listingProjectFilesInDirectory(directoryName)
dependencies = extractDependencies(projectFiles)
writeDependenciesToCSV(dependencies)
