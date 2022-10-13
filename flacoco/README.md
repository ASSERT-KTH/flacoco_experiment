# Flacoco Experiment

This module contains the reproduction package, results, and analysis of the flacoco experiments.

---------------------------------------------------------------

## Inspection of Defects4J classfiles

We inspect the classfiles of the [Defects4J v2.0](https://github.com/rjust/defects4j) bugs.

### Reproduction

The following files contain the source code for reproducing the experiment:
- [flacoco/scripts/runAllBugs4Classfiles.py](flacoco/scripts/runAllBugs4Classfiles.py)
- [flacoco/scripts/classfiles.Dockerfile](flacoco/scripts/classfiles.Dockerfile)
 
To reproduce the experiment:
```bash
cd flacoco/scripts/
docker build . --tag flacoco/classfiles:latest --file classfiles.Dockerfile
docker run -d flacoco/classfiles:latest
docker cp $CONTAINER_ID:/results ./
```

### Results

The results can be found under [flacoco/results_classfiles/results.csv](flacoco/results_classfiles/results.csv)

### Analysis

The analysis can be found under [flacoco/classfiles.ipynb](flacoco/classfiles.ipynb)

---------------------------------------------------------------

## Fault Localization on Defects4J v2.0 with FLACOCO and GZoltar

We compile each bug of [Defects4J v2.0](https://github.com/rjust/defects4j) to different target bytecode versions (Java LTS).
Then, we run both [FLACOCO](https://github.com/SpoonLabs/flacoco) and [GZoltar](GZoltar/gzoltar) on each of the bugs.

### Reproduction

The directory [flacoco/scripts](flacoco/scripts) contains the required scripts and files for reproducing the experiment.
 
To reproduce the experiment for the default configuration of [Defects4J v2.0](https://github.com/rjust/defects4j):
```bash
cd flacoco/scripts/
TARGET=default
docker build . --tag flacoco/$TARGET:latest --file $TARGET.Dockerfile
docker run -d flacoco/$TARGET:latest
docker cp $CONTAINER_ID:/results ./
```

For other targets (`java7`, `java8`, `java11`, and `java17`), replace the `TARGET` variable.

### Results

The results can be found under [flacoco/results_faultlocalization](flacoco/results_faultlocalization).

In each directory, we make available the execution information for each triplet (bug, target, tool).

The execution information contains the executed tests, the failing tests, and the fault localization results.

In addition, we make available the set of [Defects4J v2.0](https://github.com/rjust/defects4j) compatible with each target version
(i.e. [flacoco/results_faultlocalization/java11_bugs.csv](flacoco/results_faultlocalization/java11_bugs.csv) contains the bugs that can be compiled to Java 11).

In [flacoco/results_faultlocalization/all_bugs.csv](flacoco/results_faultlocalization/all_bugs.csv), we make available the set of bugs that are compatible with all versions.

### Analysis

The analysis can be found under [flacoco/all.ipynb](flacoco/all.ipynb).
This notebook contains the results reported in RQ1, including comparisons at the fault localization level and at the execution time level.

Furthermore, an analysis for each target version can be found under the homonymous notebooks.

---------------------------------------------------------------

## Inspection of FlacocoBot classfiles

We inspect the classfiles of the projects identified during the FlacocoBot experiment.

### Reproduction

The following files contain the source code for reproducing the experiment:
- [flacoco/scripts/runAllBugs4Classfiles.py](flacoco/scripts/runFlacocobotProjects4Classfiles.py)
- [flacoco/scripts/classfiles.Dockerfile](flacoco/scripts/classfiles.Dockerfile)
 
To reproduce the experiment:
```bash
cd flacoco/scripts/
docker build . --tag flacoco/classfiles_flacocobot:latest --file classfiles_flacocobot.Dockerfile
docker run -d flacoco/classfiles_flacocobot:latest
docker cp $CONTAINER_ID:/results ./
```

### Results

The results can be found under [flacoco/results_classfiles/results.csv](flacoco/results_classfiles_flacocobot/results.csv)
