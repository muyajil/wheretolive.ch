FROM continuumio/miniconda3:4.8.2

SHELL ["/bin/bash", "-c"]

ADD ./conda-spec.txt /conda-spec.txt

RUN conda create --name wheretolive.ch --file /conda-spec.txt
RUN echo "source activate wheretolive.ch" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH
RUN pip install --no-cache-dir retry

ADD ./* /src/
WORKDIR /src

ENTRYPOINT ["/bin/bash", "-c"]