FROM continuumio/miniconda3:4.8.2

SHELL ["/bin/bash", "-c"]

ADD ./conda-spec.txt /conda-spec.txt

RUN conda create --name wheretolive.ch --file /conda-spec.txt
RUN echo "source activate wheretolive.ch" > ~/.bashrc
ENV PATH /opt/conda/envs/wheretolive.ch/bin:$PATH
RUN pip install --no-cache-dir retry

ADD ./wheretolive /wheretolive

ENTRYPOINT ["/opt/conda/envs/wheretolive.ch/bin/python"]