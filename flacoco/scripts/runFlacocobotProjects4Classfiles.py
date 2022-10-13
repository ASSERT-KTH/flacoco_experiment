#!/usr/bin/env python3
import argparse
import subprocess
import os
from os import path
import shutil
import csv
import sys
from joblib import Parallel, delayed
import re
import time
import numpy as np
from pathlib import Path

# from https://en.wikipedia.org/wiki/Java_class_file#General_layout byte 6/7
# and https://javarevisited.blogspot.com/2011/07/javalangunsupportedclassversionerror.html
class_version_to_target = {
        "45" : "1.1",
        "46" : "1.2",
        "47" : "1.3",
        "48" : "1.4",
        "49" : "1.5",
        "50" : "1.6",
        "51" : "1.7",
        "52" : "1.8",
        "53" :   "9",
        "54" :  "10",
        "55" :  "11",
        "56" :  "12",
        "57" :  "13",
        "58" :  "14",
        "59" :  "15",
        "60" :  "16",
        "61" :  "17",
        "62" :  "18",
        }


flacocobot_projects = {
        "apache/dubbo" : ("7de8b982fbd9e080edb91bf6ffd774ab519c0226", "grep -rl '0.0.4.1-SNAPSHOT' . | xargs sed -i 's/0.0.4.1-SNAPSHOT/0.0.4.1/g' && mvn clean install -DskipTests"),
        "debezium/debezium" : ("d19fc234eeb6af513fa831feca3690c4af67a6a9", "mvn clean compile"),
        "apache/pinot" : ("30c4635bfeee88f88aa9c9f63b93bcd4a650607f", "mvn clean compile"),
        "vert-x3/vertx-jdbc-client" : ("f0a593a853a3b867da6b116369ebd54f6a5a4c27", "mvn clean compile"),
        "vert-x3/vertx-web" : ("643df8faff1416a318d86e39cada32c16edb134e", "mvn clean compile"),
        "INRIA/spoon" : ("17e000b58363dee4ee1687e582f13ef993b387e0", "mvn clean compile"),
        "apache/rocketmq" : ("a17fa7605cfbd266e4468e6fe2d6cf6711572111", "mvn package --file pom.xml -DskipTests -Dmaven.compiler.failOnError=false"),
        "confluentinc/kafka-connect-jdbc" : ("ea445621b21cc762921d544c0fb83517ed0b35eb", "mvn clean compile"),
        "jenkinsci/kubernetes-plugin" : ("b9a92ea9845aa6b87beebf63e9812ccaec4e0a5a", "mvn clean compile"),
        "apache/shardingsphere" : ("938a4bcc553d350ca5936fed36965ee0c0a0c1ad", "mvn clean install -DskipTests"),
        }


def get_classfiles_chunk(args, chunk):
    versions = {}
    for path in chunk:
        new_versions = set()
        run = subprocess.run(["javap", "-verbose", str(path)], capture_output=True)
        stdout = run.stdout.decode("utf-8")
        m = re.search("major version: ([0-9][0-9])", stdout)
        if m != None and len(m.groups()) > 0:
            for group in m.groups():
                if group not in class_version_to_target:
                    print("ERROR: found a match (%s) which doesn't have a target version associated with" % group)
                else:
                    new_versions.add(class_version_to_target[group])
        else:
            print("No regex match for file %s" % path)
            continue

        for version in new_versions:
            if version in versions:
                versions[version] += 1
            else:
                versions[version] = 1
    
    return versions


def get_classfiles(args, bin_dirs):
    globs = set()
    for bin_dir in bin_dirs:
        globs.update(set(Path(bin_dir).glob("**/*.class")))
    chunks = np.array_split(np.array(list(globs)), 8)
    results = Parallel(n_jobs=8)(delayed(get_classfiles_chunk)(args, chunk) for chunk in chunks)

    versions = {}
    for result in results:
        for version in result:
            if version in versions:
                versions[version] += result[version]
            else:
                versions[version] = result[version]

    return versions


def run_bug(args, og_dir, project):
    os.chdir(og_dir)
    print("Running for %s..." % project)

    # Setup env
    output = { "project" : project, "commit_id" : None,  "clone" : False, "checkout" : False, "compile" : False , "classfiles" : None }
    bug_dir = os.path.join(args.storage, project.split("/")[0] + "_" + project.split("/")[1])
    if os.path.exists(bug_dir): shutil.rmtree(bug_dir, ignore_errors=True)
    os.makedirs(bug_dir)
    os.chdir(bug_dir)
    output["env"] = True

    # Clone project
    run = subprocess.run(["git", "clone", "https://github.com/" + project + ".git", "."], capture_output=True)
    output["clone"] = run.returncode == 0
    if not output["clone"]: 
        os.chdir(og_dir)
        return output

    # Checkout commit
    output["commit_id"] = flacocobot_projects[project][0]
    run = subprocess.run(["git", "checkout", flacocobot_projects[project][0]], capture_output=True)
    output["checkout"] = run.returncode == 0
    if not output["checkout"]:
        os.chdir(og_dir)
        return output
    
    # Compile
    run = subprocess.run(flacocobot_projects[project][1], shell=True, capture_output=True)
    output["compile"] = run.returncode == 0
    if not output["compile"]:
        output["compile"] = run.stdout.decode("utf-8").splitlines()[-50:]
        os.chdir(og_dir)
        return output

    # Get binary directories
    bin_dirs = re.findall("Compiling \d+ source files to (.*)", run.stdout.decode("utf-8"))
    output["classfiles"] = get_classfiles(args, bin_dirs)
        
    # Cleanup
    os.chdir(og_dir)

    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gather the classfile versions of all Defects4J bugs")
    parser.add_argument("--storage", help="Path to the storage directory", required=True, metavar="<path_to_storage>")
    parser.add_argument("--output", help="Path to the output directory", required=True, metavar="<path_to_output>")
    args = parser.parse_args()

    # Clone projects, checkout identified commit, run classfile script
    og_dir = os.getcwd()
    results = Parallel(n_jobs=8)(delayed(run_bug)(args, og_dir, project) for project in flacocobot_projects.keys())
    
    for project in flacocobot_projects.keys():
        bug_dir = os.path.join(args.storage, project.split("/")[0] + "_" + project.split("/")[1])
        shutil.rmtree(bug_dir, ignore_errors=True)
    
    # Write results to csv file
    keys = ["project", "commit_id", "clone", "checkout", "compile", "classfiles"]
    with open(os.path.join(args.output, "results.csv"), "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for result in results:
            writer.writerow([result[k] for k in keys])
