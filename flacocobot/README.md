# Flacocobot Experiment

This module contains the results and analysis of the flacocobot experiment.

---------------------------------------------------------------

### Projects under analysis

The following table contains the list of projects monitored by Flacocobot during the experiment to test fault localization in the field.

| Project                                                                                                 | Source |
|---------------------------------------------------------------------------------------------------------|--------|
| [apache/dubbo](https://github.com/apache/dubbo)                                                         | Bears  |
| [debezium/debezium](https://github.com/debezium/debezium)                                               | Bears  |
| [apache/pinot](https://github.com/apache/pinot)                                                         | Bears  |
| [vert-x3/vertx-jdbc-client](https://github.com/vert-x3/vertx-jdbc-client)                               | Bears  |
| [vert-x3/vertx-web](https://github.com/vert-x3/vertx-web)                                               | Bears  |
| [INRIA/spoon](https://github.com/INRIA/spoon)                                                           | Bears  |
| [apache/rocketmq](https://github.com/apache/rocketmq)                                                   | GitHub |
| [confluentinc/kafka-connect-jdbc](https://github.com/confluentinc/kafka-connect-jdbc)                   | GitHub |
| [jenkinsci/kubernetes-plugin](https://github.com/jenkinsci/kubernetes-plugin)                           | GitHub |
| [apache/shardingsphere](https://github.com/apache/shardingsphere)                                       | GitHub |

### Results

The results can be found in the folder [experiment-data](experiment-data). In particular, the folder contains three sub folders: `phase-1-logs`, `phase-2-logs`, and `projects-prs-analysis`. The first two folders contain the log files associated with the execution of Flacocobot in two different phases of the experiment. The third folder contains the results, divided per project, of fault localization performed by Flacocobot on every pull request analyzed.
