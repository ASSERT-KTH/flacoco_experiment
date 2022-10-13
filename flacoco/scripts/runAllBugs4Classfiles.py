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


def get_classfiles(args, bin_dir):
    chunks = np.array_split(np.array(list(Path(bin_dir).glob("**/*.class"))), 8)
    results = Parallel(n_jobs=8)(delayed(get_classfiles_chunk)(args, chunk) for chunk in chunks)

    versions = {}
    for result in results:
        for version in result:
            if version in versions:
                versions[version] += result[version]
            else:
                versions[version] = result[version]

    return versions


def run_bug(args, og_dir, pid, bid):
    os.chdir(og_dir)
    print("Running for %s%s..." % (pid, bid))

    # Setup env
    output = { "pid" : pid, "bid" : bid, "env" : False, "checkout" : False, "compile" : False , "classfiles" : None }
    bug_dir = os.path.join(args.storage, str(pid) + "_" + str(bid))
    if os.path.exists(bug_dir): shutil.rmtree(bug_dir, ignore_errors=True)
    os.makedirs(bug_dir)
    os.chdir(bug_dir)
    output["env"] = True

    # Checkout bug
    run = subprocess.run(["defects4j", "checkout", "-p", str(pid), "-v", str(bid) + "b", "-w", "./"], capture_output=True)
    output["checkout"] = run.returncode == 0
    if not output["checkout"]: 
        os.chdir(og_dir)
        return output
    
    # Get binary directories
    run = subprocess.run(["defects4j", "export", "-p", "dir.bin.classes"], capture_output=True)
    java_bin = run.stdout.decode("utf-8")

    # Compile
    run = subprocess.run(["defects4j", "compile"], capture_output=True)
    output["compile"] = run.returncode == 0
    output["classfiles"] = get_classfiles(args, java_bin)
        
    # Cleanup
    os.chdir(og_dir)

    return output


def producer(pids, bugs):
    for pid in pids:
        for bid in bugs[pid]:
            yield (pid, bid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gather the classfile versions of all Defects4J bugs")
    parser.add_argument("--storage", help="Path to the storage directory", required=True, metavar="<path_to_storage>")
    parser.add_argument("--output", help="Path to the output directory", required=True, metavar="<path_to_output>")
    args = parser.parse_args()

    # Get all project ids
    run = subprocess.run(["defects4j", "pids"], capture_output=True)
    run.check_returncode()
    pids = {pid.decode("utf-8") for pid in run.stdout.split()}

    # Get all bug ids for all projects
    # bugs -> mapping (pid -> set of bids)
    bugs = {}
    for pid in pids:
        run = subprocess.run(["defects4j", "bids", "-p", pid], capture_output=True)
        run.check_returncode()
        bugs[pid] = {bid.decode("utf-8") for bid in run.stdout.split()}
        print("Found %3d bugs for project %s" % (len(bugs[pid]), pid))

    # DEBUG lines
    #bugs = { "Math" : {70} }
    #pids = { "Math" }
    # Checkout all buggy and fixed versions
    og_dir = os.getcwd()
    results = Parallel(n_jobs=8)(delayed(run_bug)(args, og_dir, pid, bid) for (pid, bid) in producer(pids, bugs))
    
    for (pid, bid) in producer(pids, bugs):
        bug_dir = os.path.join(args.storage, str(pid) + "_" + str(bid))
        shutil.rmtree(bug_dir, ignore_errors=True)
    
    # Write results to csv file
    keys = ["pid", "bid", "env", "checkout", "compile", "classfiles"]
    with open(os.path.join(args.output, "results.csv"), "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for result in results:
            writer.writerow([result[k] for k in keys])
