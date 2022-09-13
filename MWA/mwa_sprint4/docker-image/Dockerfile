FROM thoom/pyresttest
COPY ./tests /usr/src/app
WORKDIR /usr/src/app
ENTRYPOINT [ "pyresttest" ]
CMD ["https://nmf8dx6r64.execute-api.us-east-1.amazonaws.com/", "api_test.yml"]