FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
RUN mkdir -p ${WORKDIR}/modules
WORKDIR ${WORKDIR}
COPY src/modules ${WORKDIR}/modules

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install --upgrade python-dotenv \
    && pip install apache-beam[gcp] \
    && pip install pytest \
    && pip install unittest \
    && pip install google-cloud-secret-manager==2.0.0

COPY src/__init__.py ${WORKDIR}/__init__.py
COPY src/setup.py ${WORKDIR}/setup.py
COPY src/__main__.py ${WORKDIR}/__main__.py
COPY src/spec/metadata.json ${WORKDIR}/metadata.json

ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/__main__.py"

ARG PROJECT_ID
ARG IMAGE 
ARG BUCKET 
ARG REGION 

RUN echo "PROJECT_ID=${PROJECT_ID}" >> .env
RUN echo "IMAGE=${IMAGE}" >> .env
RUN echo "BUCKET=${BUCKET}" >> .env
RUN echo "REGION=${REGION}" >> .env



# RUN echo "++++++++++++++++++++++++++++"
# RUN echo "=======Running Echos========"
# RUN echo "++++++++++++++++++++++++++++"

# RUN echo '----- Working directory path'
# RUN echo ${WORKDIR}
# RUN echo '----- Python File'
# RUN echo ${FLEX_TEMPLATE_PYTHON_PY_FILE}
# RUN echo '----- Python Requirements File'
# RUN echo ${FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE}
# RUN echo '----- Python Setup File'
# RUN echo ${FLEX_TEMPLATE_PYTHON_SETUP_FILE}
# RUN echo '----- PROJECT_ID'
# RUN echo ${PROJECT_ID}
# RUN echo '----- ENVIRONMENT'
# RUN echo ${ENVIRONMENT}

# RUN echo '----- Listing Working Directory'
# RUN ls -la ${WORKDIR}

# RUN echo '---- Listing Modules--'
# RUN ls -la ${WORKDIR}/modules
