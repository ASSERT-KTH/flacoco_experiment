#!/usr/bin/env python3
import argparse
import subprocess
import os
import shutil
import csv
import sys
from joblib import Parallel, delayed
import re
import time
from pathlib import Path


def save_results(args, pid, bid):
    try:
        with open("all_tests", "r") as f:
            # Reformat the output given by Defects4J
            lines = [y[1][:-2] + "#" + y[0] for y in [x.split("(") for x in f.readlines()]]
            with open(os.path.join(args.output, "%s_%s_all_tests" % (str(pid), str(bid))), "w") as fp:
                for line in lines:
                    fp.write(line + "\n")

        with open("failing_tests", "r") as f:
            lines = [y.replace("::", "#") for y in [x[4:-1] for x in f.readlines() if x.startswith("---")]]
            with open(os.path.join(args.output, "%s_%s_failing_tests" % (str(pid), str(bid))), "w") as fp:
                for line in lines:
                    fp.write(line + "\n")
    
        return True
    except Exception as e:
        print(e)
        return False


def run_bug(args, og_dir, pid, bid):
    os.chdir(og_dir)
    print("Running for %s%s..." % (pid, bid))

    # Setup env
    output = {"pid" : pid, "bid" : bid, "env" : False, "success" : False}
    bug_dir = os.path.join(args.storage, str(pid) + "_" + str(bid) + "_tests_baseline")
    if os.path.exists(bug_dir): shutil.rmtree(bug_dir)
    os.makedirs(bug_dir)
    os.chdir(bug_dir)
    output["env"] = True

    # Checkout bug
    run = subprocess.run(["defects4j", "checkout", "-p", str(pid), "-v", str(bid) + "b", "-w", "./"], capture_output=True)
    output["checkout"] = run.returncode == 0
    if not output["checkout"]: return output


    # Call defectstj test and gather test information
    run = subprocess.run(["defects4j", "test"], capture_output=True)
    output["success"] = run.returncode == 0 and save_results(args, pid, bid)
    if not output["success"]: return output


    # Cleanup
    os.chdir(og_dir)
    shutil.rmtree(bug_dir)

    return output


def producer(pids, bugs):
    for pid in pids:
        for bid in bugs[pid]:
            yield (pid, bid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obtain the list of executed and failing test cases for each Defects4J bug")
    parser.add_argument("--storage", help="Path to the storage directory", required=True, metavar="<path_to_storage>")
    parser.add_argument("--output", help="Path to the output directory", required=True, metavar="<path_to_output>")
    args = parser.parse_args()

    # Make output and storage absolute paths so they can be used everywhere
    args.storage = str(Path(args.storage).absolute())
    args.output = str(Path(args.output).absolute())

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

    # Checkout all buggy and fixed versions
    og_dir = os.getcwd()
    results = Parallel(n_jobs=8)(delayed(run_bug)(args, og_dir, pid, bid) for (pid, bid) in producer(pids, bugs))

    # Write results to csv file
    keys = ["pid", "bid", "env", "checkout", "success"]
    with open(os.path.join(args.output, "results.csv"), "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for result in results:
            writer.writerow([result[k] for k in keys])
