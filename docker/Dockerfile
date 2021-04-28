FROM continuumio/miniconda3:4.8.2

LABEL version="1.0.1" maintainer="Joe Brown <brwnjm@gmail.com>"

ARG MOSDEPTH_VERSION="v0.3.1"
ARG BEDTOOLS_VERSION="2.30.0"

RUN apt-get update && apt-get install -y g++ make procps
RUN conda create -n main -c bioconda -c conda-forge python==3.8.3 bedtools==${BEDTOOLS_VERSION}
RUN echo "source activate main" > ~/.bashrc
ENV PATH /opt/conda/envs/main/bin:$PATH
RUN wget -qO /usr/local/bin/mosdepth https://github.com/brentp/mosdepth/releases/download/${MOSDEPTH_VERSION}/mosdepth && chmod +x /usr/local/bin/mosdepth
