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
target_to_class_version = {
        "1.1" : "45",
        "1.2" : "46",
        "1.3" : "47",
        "1.4" : "48",
        "1.5" : "49",
        "1.6" : "50",
        "1.7" : "51",
        "1.8" : "52",
        "9"   : "53",
        "10"  : "54",
        "11"  : "55",
        "12"  : "56",
        "13"  : "57",
        "14"  : "58",
        "15"  : "59",
        "16"  : "60",
        "17"  : "61",
        "18"  : "62"
        }


def get_exec_time(run):
    stdout = run.stdout.decode("utf-8")
    m = re.search("Time Total\(s\): ([0-9]*\.[0-9]*)", stdout)
    if m != None and len(m.groups()) == 1:
        return float(m.groups()[0])
    else:
        return None


def check_classfiles_chunk(args, chunk):
    for path in chunk:
        if "package-info.class" in path.name:
            continue
        run = subprocess.run(["javap", "-verbose", str(path)], capture_output=True)
        stdout = run.stdout.decode("utf-8")
        m = re.search("major version: ([0-9][0-9])", stdout)
        if m != None and len(m.groups()) > 0:
            for group in m.groups():
                if group != target_to_class_version[args.target]:
                    print("File %s is of wrong version (%s should be %s)" % (path, group, target_to_class_version[args.target]))
                    return False
        else:
            print("No regex match for file %s" % path)
            return False
    return True


def check_classfiles(args, bin_dir):
    chunks = np.array_split(np.array(list(Path(bin_dir).glob("**/*.class"))), 8)
    results = Parallel(n_jobs=8)(delayed(check_classfiles_chunk)(args, chunk) for chunk in chunks)
    return False not in results


def check_failing_test_execution(args, og_dir, tool, pid, bid):
    try:
        # Read the baseline failing set
        with open(Path(og_dir, "test_baselines", "%s_%s_failing_tests" % (str(pid), str(bid)))) as f:
            failing_tests_baseline = set([x.strip() for x in f.readlines()])
        # Read the failing set from the execution trace
        with open(Path(og_dir, args.output, "%s_failing_tests_%s%s.csv" % (tool.upper(), str(pid), str(bid)))) as f:
            failing_tests = set([x.strip() for x in f.readlines()])

        # True if both pair of sets are equal
        return failing_tests == failing_tests_baseline
    except IOError as e:
        print(e)
        return False


def check_baseline_test_execution(args, og_dir, tool, pid, bid):
    try:
        # Read the baseline test execution
        with open(Path(og_dir, "test_baselines", "%s_%s_all_tests" % (str(pid), str(bid)))) as f:
            executed_tests_baseline = set([x.strip() for x in f.readlines()])
        # Read the executed trace
        with open(Path(og_dir, args.output, "%s_executed_tests_%s%s.csv" % (tool.upper(), str(pid), str(bid)))) as f:
            executed_tests = set([x.strip() for x in f.readlines()])

        # True if both pair of sets are equal
        return executed_tests == executed_tests_baseline
    except IOError as e:
        print(e)
        return False


def check_fault_localization(args, og_dir, tool, pid, bid):
    try:
        with open(Path(og_dir, args.output, "%s_suspicious_%s%s.csv" % (tool.upper(), str(pid), str(bid)))) as f:
            suspicious_lines = [x for x in [x.strip() for x in f.readlines()]]
            return len(suspicious_lines) > 0
    except IOError as e:
        print(e)
        return False


def compile(args, pid, bid):
    try:
        if pid == "Chart":
            with open("ant/build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            with open("ant/build-swt.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "Cli":
            if bid <= 21:
                run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern -Dant.build.javac.source=" + args.target + " -Dant.build.javac.target=" + args.target], capture_output=True)
                return run.returncode == 0
            elif bid > 21:
                if Path("build.xml").exists():
                    with open("build.xml", "r+") as f:
                        content = f.read()
                        content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                        content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                        f.truncate(0)
                        f.seek(0)
                        f.write(content)
                if Path("maven-build.xml").exists():
                    with open("maven-build.xml", "r+") as f:
                        content = f.read()
                        content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                        content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                        f.truncate(0)
                        f.seek(0)
                        f.write(content)
                run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
                return run.returncode == 0

        elif pid == "Closure":
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern -Dant.build.javac.source=" + args.target + " -Dant.build.javac.target=" + args.target], capture_output=True)
            return run.returncode == 0

        elif pid == "Codec":
            with open("build.xml", "r+") as f:
                content = f.read()
                if '<import file="maven-build.xml"/>' in content:
                    with open("maven-build.xml", "r+") as pom_f:
                        content_pom = pom_f.read()
                        content_pom = re.sub("source=\"1\.[1-8]\"", " encoding=\"UTF-8\" source=\"" + args.target + "\"", content_pom)
                        content_pom = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content_pom)
                        pom_f.truncate(0)
                        pom_f.seek(0)
                        pom_f.write(content_pom)
                elif 'source="${compile.source}"' in content:
                    content = re.sub('source=\"\$\{compile.source\}\"', " encoding=\"UTF-8\" source=\"" + args.target + "\"", content)
                    content = re.sub('target=\"\$\{compile.target\}\"', "target=\"" + args.target + "\"", content)
                else:
                    content = re.sub("<javac srcdir",
                        "<javac encoding=\"UTF-8\" source=\"" + args.target + "\" " +
                        "target=\"" + args.target + "\" srcdir", 
                        content
                    )
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern -Dcompile.source=" + args.target + " -Dcompile.target=" + args.target], capture_output=True)
            return run.returncode == 0

        elif pid == "Collections":
            with open("build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern -Dcompile.source=" + args.target + " -Dcompile.target=" + args.target], capture_output=True)
            return run.returncode == 0

        elif pid == "Compress":
            with open("maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "Csv":
            with open("maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "Gson":
            with open("gson/maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "JacksonCore":
            with open("maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "JacksonDatabind":
            with open("maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "JacksonXml":
            with open("maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "Jsoup":
            with open("maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "JxPath":
            with open("build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern -Dcompile.source=" + args.target + " -Dcompile.target=" + args.target], capture_output=True)
            return run.returncode == 0

        elif pid == "Lang":
            if bid <= 20 or bid >= 42:
                run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern -Dcompile.source=" + args.target + " -Dcompile.target=" + args.target], capture_output=True)
                return run.returncode == 0
            else:
                with open("maven-build.xml", "r+") as f:
                    content = f.read()
                    content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                    content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                    f.truncate(0)
                    f.seek(0)
                    f.write(content)
                run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
                return run.returncode == 0

        elif pid == "Math":
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern -Dcompile.source=" + args.target + " -Dcompile.target=" + args.target], capture_output=True)
            return run.returncode == 0

        elif pid == "Mockito":
            with open("build.gradle", "r+") as f:
                content = f.read()
                content = re.sub("sourceCompatibility = 1\.[1-8]", "sourceCompatibility = " + args.target, content)
                content = re.sub("targetCompatibility = 1\.[1-8]", "targetCompatibility = " + args.target, content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

        elif pid == "Time":
            with open("maven-build.xml", "r+") as f:
                content = f.read()
                content = re.sub("source=\"1\.[1-8]\"", "source=\"" + args.target + "\"", content)
                content = re.sub("target=\"1\.[1-8]\"", "target=\"" + args.target + "\"", content)
                f.truncate(0)
                f.seek(0)
                f.write(content)
            run = subprocess.run(["defects4j", "compile", "-o", "-Dbuild.compiler=modern"], capture_output=True)
            return run.returncode == 0

    except Exception:
        return False


def run_bug(args, og_dir, pid, bid):
    tools = ["gzoltar", "flacoco"]
    output = { "target" : args.target , "pid" : pid , "bid" : bid , "env" : False , "checkout" : False , "compile": False , "check_classfiles" : False , "gzoltar_exec_time" : None , "gzoltar_executed_tests" : False, "gzoltar_failing_tests" : False , "gzoltar_fl" : False , "flacoco_exec_time" : None , "flacoco_executed_tests" : False , "flacoco_failing_tests" : False , "flacoco_fl" : False }

    for tool in tools:
        out = run_fl_on_bug(args, og_dir, tool, pid, bid)
        output["env"] = out["env"]
        output["checkout"] = out["checkout"]
        output["compile"] = out["compile"]
        output["check_classfiles"] = out["check_classfiles"]
        output[tool + "_exec_time"] = out[tool + "_exec_time"]
        output[tool + "_executed_tests"] = out[tool + "_executed_tests"]
        output[tool + "_failing_tests"] = out[tool + "_failing_tests"]
        output[tool + "_fl"] = out[tool + "_fl"]

    return output


def run_fl_on_bug(args, og_dir, tool, pid, bid):
    os.chdir(og_dir)
    print("Running for %s%s... with %s" % (pid, bid, tool))

    # Setup env
    output = {"target" : args.target, "pid" : pid, "bid" : bid, "env" : False, "checkout" : False, "compile" : False, "check_classfiles" : False , tool + "_exec_time" : None, tool + "_executed_tests" : False , tool + "_failing_tests" : False , tool + "_fl" : False }
    bug_dir = os.path.join(args.storage, str(pid) + "_" + str(bid) + "_" + tool)
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
    if args.target != None:
        output["compile"] = compile(args, pid, bid)
        output["check_classfiles"] = output["compile"] and check_classfiles(args, java_bin)
    else:
        run = subprocess.run(["defects4j", "compile"], capture_output=True)
        output["compile"] = run.returncode == 0
        output["check_classfiles"] = output["compile"]
        
    if not output["compile"] or not output["check_classfiles"]:
        os.chdir(og_dir)
        return output

    # Get classpath + dirs
    run = subprocess.run(["defects4j", "export", "-p", "cp.test"], capture_output=True)
    classpath = run.stdout.decode("utf-8")
    run = subprocess.run(["defects4j", "export", "-p", "dir.src.classes"], capture_output=True)
    java_src = run.stdout.decode("utf-8")
    run = subprocess.run(["defects4j", "export", "-p", "dir.bin.classes"], capture_output=True)
    java_bin = run.stdout.decode("utf-8")
    run = subprocess.run(["defects4j", "export", "-p", "dir.src.tests"], capture_output=True)
    test_src = run.stdout.decode("utf-8")
    run = subprocess.run(["defects4j", "export", "-p", "dir.bin.tests"], capture_output=True)
    test_bin = run.stdout.decode("utf-8")

    # Call Astor with FL tool
    astor_mode = { "flacoco" : "flacoco" , "gzoltar" : "gzoltar1_7" }
    run = subprocess.run(["timeout",  "1h", "java", "-cp", os.path.join(og_dir, "astor.jar"),
        "fr.inria.main.FaultLocalizationMain", "-mode", "jgenprog", "-location", ".",
        "-dependencies", classpath, "-id", str(pid) + str(bid), "-srcjavafolder", java_src,
        "-srctestfolder", test_src, "-binjavafolder", java_bin, "-bintestfolder", test_bin,
        "-faultlocalization", astor_mode[tool], "-flthreshold", "0.0",
        "-filetestcases4fl", Path(og_dir, "test_baselines", "%s_%s_all_tests" % (str(pid), str(bid))),
        "-locationGzoltarJar", og_dir,
        "-parameters", "outfl:" + os.path.join(og_dir, args.output)], capture_output=True)
    #print(run.stdout.decode("utf-8"))
    #print(run.stderr.decode("utf-8"))
    output[tool + "_exec_time"] = get_exec_time(run)
    output[tool + "_executed_tests"] = check_baseline_test_execution(args, og_dir, astor_mode[tool], pid, bid)
    output[tool + "_failing_tests"] = check_failing_test_execution(args, og_dir, astor_mode[tool], pid, bid)
    output[tool + "_fl"] = run.returncode == 0 and check_fault_localization(args, og_dir, astor_mode[tool], pid, bid)
    
    # Cleanup
    os.chdir(og_dir)

    # Cleanup gzoltar files
    if tool == "gzoltar":
        outputgzoltar = Path(og_dir, args.output, "outputgzoltar")
        if outputgzoltar.exists(): shutil.rmtree(outputgzoltar, ignore_errors=True)
        outtest = Path(og_dir, args.output, "outTest.txt")
        if outtest.exists(): outtest.unlink()

    return output


def producer(pids, bugs):
    for pid in pids:
        for bid in bugs[pid]:
            yield (pid, bid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run GZoltar and Flacoco on all Defects4J bugs")
    parser.add_argument("--storage", help="Path to the storage directory", required=True, metavar="<path_to_storage>")
    parser.add_argument("--output", help="Path to the output directory", required=True, metavar="<path_to_output>")
    parser.add_argument("--target", help="Compilation target version", required=False, metavar="<java_target_version>")
    args = parser.parse_args()

    # Check target is None or is inside the target list
    if args.target != None and args.target not in target_to_class_version.keys():
        print("Invalid target specified.\nPlease select one of the following:\n" + str(list(target_to_class_version.keys())))
        sys.exit()
    
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
    
    tools = ["gzoltar", "flacoco"]
    for tool in tools:
        for (pid, bid) in producer(pids, bugs):
            bug_dir = os.path.join(args.storage, str(pid) + "_" + str(bid) + "_" + tool)
            shutil.rmtree(bug_dir, ignore_errors=True)

    # Write results to csv file
    keys = ["target", "pid", "bid", "env", "checkout", "compile", "check_classfiles", "gzoltar_exec_time" , "gzoltar_executed_tests", "gzoltar_failing_tests", "gzoltar_fl", "flacoco_exec_time", "flacoco_executed_tests", "flacoco_failing_tests",  "flacoco_fl"]
    with open(os.path.join(args.output, "results.csv"), "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for result in results:
            writer.writerow([result[k] for k in keys])
