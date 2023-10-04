# Dockerfile that builds a fully functional image of your app.
#
# This image installs all Python dependencies for your application. It's based
# on CentOS 7 with Python 3 (https://github.com/inveniosoftware/docker-invenio)
# and includes Pip, Pipenv, Node.js, NPM and some few standard libraries
# Invenio usually needs.
#
# Note: It is important to keep the commands in this file in sync with your
# bootstrap script located in ./scripts/bootstrap.

FROM registry.cern.ch/inveniosoftware/almalinux:1

ARG OEDATAREP_RELEASE
ARG NVM_VERS
ARG NODE_VERS

# Clone custom repositories
RUN git clone --depth 1 --branch ${OEDATAREP_RELEASE} https://github.com/ingv-oe-dev/invenio-assets.git ../invenio-assets
RUN git clone --depth 1 --branch ${OEDATAREP_RELEASE} https://github.com/ingv-oe-dev/oedatarep-ts-loader.git ../oedatarep-ts-loader

COPY site ./site
COPY Pipfile Pipfile.lock ./
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/${NVM_VERS}/install.sh | bash
RUN pipenv install --deploy --system --pre

COPY ./docker/uwsgi/ ${INVENIO_INSTANCE_PATH}
COPY ./invenio.cfg ${INVENIO_INSTANCE_PATH}
COPY ./templates/ ${INVENIO_INSTANCE_PATH}/templates/
COPY ./app_data/ ${INVENIO_INSTANCE_PATH}/app_data/
COPY ./translations/ ${INVENIO_INSTANCE_PATH}/translations/
COPY ./ .

RUN source ~/.bash_profile && nvm install ${NODE_VERS}
RUN source ~/.bash_profile && \
    nvm use ${NODE_VERS} && \
    cp -r ./static/. ${INVENIO_INSTANCE_PATH}/static/ && \
    cp -r ./assets/. ${INVENIO_INSTANCE_PATH}/assets/ && \
    rm -rf /opt/invenio/src/site/oedatarep_invenio_rdm/assets/semantic-ui/less && \
    invenio collect --verbose  && \
    invenio webpack buildall

ENTRYPOINT [ "bash", "-c"]
