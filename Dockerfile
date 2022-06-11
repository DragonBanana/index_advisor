FROM postgres:14

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository main
RUN apt update -y
RUN apt install lsb-release -y

# Install PDDG packages
RUN apt install curl ca-certificates gnupg -y
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN apt update -y

# Install Postgres
RUN apt install postgresql -y
RUN apt install postgresql-contrib -y
RUN apt install postgresql-common -y

RUN apt install postgresql-14-hypopg -y

RUN apt install python3-pip -y

# Install base utilities
RUN apt install software-properties-common -y
RUN apt install build-essential -y
RUN apt install wget -y

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Install git
RUN apt install git -y
RUN apt install flex bison -y
RUN apt install unzip -y
RUN apt install net-tools -y

ADD . /index_advisor

RUN conda config --set restore_free_channel true
RUN conda env create -f index_advisor/environment.yaml python=3.6