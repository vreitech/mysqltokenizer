FROM docker.io/adoptopenjdk/openjdk11:alpine AS builder

WORKDIR /opt/antlr4

ARG ANTLR_VERSION="4.12.0"
ARG MAVEN_OPTS="-Xmx1G"

RUN apk add --no-cache maven git \
    && git clone https://github.com/antlr/antlr4.git \
    && cd antlr4 \
    && git checkout $ANTLR_VERSION \
    && mvn clean --projects tool --also-make \
    && mvn -DskipTests install --projects tool --also-make \
    && mv ./tool/target/antlr4-*-complete.jar antlr4-tool.jar

FROM docker.io/adoptopenjdk/openjdk11:alpine-jre AS antlr4

WORKDIR /work
COPY --from=builder /opt/antlr4/antlr4/antlr4-tool.jar /usr/local/lib/
COPY MySqlLexer.g4.patch /work

ARG CLASSPATH=".:/usr/local/lib/antlr4-tool.jar:$CLASSPATH"

RUN apk add --no-cache wget patch \
    && cd /work \
    && wget -q https://raw.githubusercontent.com/antlr/grammars-v4/307bc033bb787c43191a097f2a0356238b13e42d/sql/mysql/Positive-Technologies/MySqlLexer.g4 \
    && wget -q https://raw.githubusercontent.com/antlr/grammars-v4/307bc033bb787c43191a097f2a0356238b13e42d/sql/mysql/Positive-Technologies/MySqlParser.g4 \
    && patch MySqlLexer.g4 MySqlLexer.g4.patch \
    && java -Xmx500M -cp /usr/local/lib/antlr4-tool.jar org.antlr.v4.Tool -Dlanguage=Python3 MySqlLexer.g4 MySqlParser.g4

FROM docker.io/python:3.11.3-alpine3.17

WORKDIR /work
COPY --from=antlr4 /work/MySqlLexer.py /work/MySqlParser.py /work/
COPY mysqltokenizer.py /work

RUN apk add --no-cache bash \
    && pip3 install antlr4-python3-runtime \
    && cd /work

ENTRYPOINT ["python3", "./mysqltokenizer.py"]

