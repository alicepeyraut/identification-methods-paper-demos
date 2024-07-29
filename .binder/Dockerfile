################################################################################
###                                                                          ###
### Created by Martin Genet                                                  ###
###                                                                          ###
### École Polytechnique, Palaiseau, France                                   ###
###                                                                          ###
################################################################################

FROM registry.gitlab.inria.fr/apeyraut/identification-methods-paper-demos:latest


# Fix ImageMagick, cf. https://stackoverflow.com/a/59193253
USER root
RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml 
ARG NB_USER=jovyan
USER ${NB_USER}



# Copy repo into the image, cf. https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html. MG20230531: OMG this copies from the "build context", cf. https://stackoverflow.com/questions/73156067/where-does-the-copy-command-in-docker-copy-from; here it seems to be the repo itself.
ARG NB_USER=jovyan
ARG NB_UID=1000
USER ${NB_USER}
ENV HOME /home/${NB_USER}
COPY --chown=${NB_UID} . ${HOME}
