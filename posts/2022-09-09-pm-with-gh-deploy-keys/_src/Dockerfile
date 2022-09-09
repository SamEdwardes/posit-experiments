FROM rstudio/rstudio-package-manager:bionic-2022.07.2-11 

# Install R
USER root
RUN sudo apt-get update
RUN sudo apt-get install -y gdebi-core
ENV R_VERSION=4.1.3
RUN curl -O https://cdn.rstudio.com/r/ubuntu-1804/pkgs/r-${R_VERSION}_1_amd64.deb
RUN sudo gdebi -n r-${R_VERSION}_1_amd64.deb

USER rstudio-pm
