FROM ubuntu:22.04

# Setup workdir
WORKDIR /

# Setup dependencies
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update --fix-missing
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update --fix-missing
RUN apt-get install git openjdk-11-jdk maven curl python3.10 python3.10-distutils -y
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip3 install joblib numpy

# Setup experiment
WORKDIR /
COPY runFlacocobotProjects4Classfiles.py ./
RUN mkdir projects
RUN mkdir results

CMD [ "python3.10", "runFlacocobotProjects4Classfiles.py" , "--storage", "projects" , "--output", "results" ]
