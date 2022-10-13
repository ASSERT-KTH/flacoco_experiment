FROM ubuntu:22.04

# Setup workdir
WORKDIR /

# Setup dependencies
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install git subversion openjdk-11-jdk curl unzip build-essential cpanminus python3.10 python3.10-distutils -y
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip3 install joblib numpy

# Setup Defects4J
RUN git clone https://github.com/andre15silva/defects4j.git
WORKDIR defects4j
RUN git checkout compile-options-java-18
RUN cpanm --installdeps .
RUN ./init.sh
ENV PATH="${PATH}:/defects4j/framework/bin"

# Setup experiment
WORKDIR /
COPY astor.jar ./
COPY com.gzoltar.agent.rt-1.7.3-all.jar ./
COPY com.gzoltar.cli-1.7.3-jar-with-dependencies.jar ./
COPY runAllBugs.py ./
ADD test_baselines /test_baselines
RUN mkdir projects
RUN mkdir results

CMD [ "python3.10", "runAllBugs.py" , "--storage", "projects" , "--output", "results" , "--target" , "11" ]
