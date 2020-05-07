FROM continuumio/miniconda3:4.8.2

SHELL ["/bin/bash", "-c"]

ADD ./environment.yml /environment.yml

RUN conda update -n base -c defaults conda
RUN conda env create -f /environment.yml
RUN echo "source activate wheretolive.ch" > ~/.bashrc
ENV PATH /opt/conda/envs/wheretolive.ch/bin:$PATH

ADD ./wheretolive /wheretolive
ADD ./csa/ /csa

ENTRYPOINT ["/opt/conda/envs/wheretolive.ch/bin/flask"]
