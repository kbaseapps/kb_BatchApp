FROM kbase/kbase:sdkbase2.latest
LABEL maintainer="KBase Developer"

COPY ./ /kb/module
WORKDIR /kb/module

# install the python coverage tool

RUN pip install coverage \
    && mkdir -p /kb/module/work \
    && chmod -R a+rw /kb/module \
    && make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
