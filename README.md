# mysqltokenizer

Podman/Docker image for tokenize identifiers and/or literals of SQL queries (MySQL 8 dialect). This allows you to get a SQL query string with unique literals and/or unique identifiers replaced with tokens, which can be useful in cases of further analysis of the SQL query.

## Used dependencies

ANTLR Project [antlr4 4.12.0](https://github.com/antlr/antlr4/tree/4.12.0) using [BSD-3-clause license](https://github.com/antlr/antlr4/blob/4.12.0/LICENSE.txt)

Python Software Foundation [Python 3.11.3](https://www.python.org/downloads/release/python-3113/) using [PSF license](https://docs.python.org/3/license.html)

Positive Technologies [MySQL grammar](https://github.com/antlr/grammars-v4/tree/307bc033bb787c43191a097f2a0356238b13e42d/sql/mysql/Positive-Technologies) using [MIT License](https://github.com/antlr/grammars-v4/blob/307bc033bb787c43191a097f2a0356238b13e42d/sql/mysql/Positive-Technologies/MySqlLexer.g4)

## Building and using image from git repo

Clone the repository to your environment using git:

```
git clone https://github.com/vreitech/mysqltokenizer.git
cd mysqltokenizer
```

Build mysqltokenizer image using buildah:

```
buildah bud -t mysqltokenizer
```

Run mysqltokenizer contaner using podman and tokenize SQL query by 4 different ways:

```
echo 'select * from `some_table` order by desc limit 10;' > ./example.sql

# Tokenize everything (identifiers and literals)
cat ./example.sql | podman run -i --rm localhost/mysqltokenizer

# Tokenize, but left identifiers untouched
cat ./example.sql | podman run -i --rm localhost/mysqltokenizer -i

# Tokenize, but left literals untouched
cat ./example.sql | podman run -i --rm localhost/mysqltokenizer -l

# Tokenize, but left identifiers and literals untouched
# (i. e. just capitalize ther rest of tokens and remove line feeds and extra spaces)
cat ./example.sql | podman run -i --rm localhost/mysqltokenizer -il
```

## Using image from Docker Hub (or GitHub)

Run mysqltokenizer contaner using podman and tokenize SQL query by 4 different ways:

```
echo 'select * from `some_table` order by desc limit 10;' > ./example.sql

# Tokenize everything (identifiers and literals)
cat ./example.sql | podman run -i --rm docker.io/vreitech/mysqltokenizer

# Tokenize, but left identifiers untouched
cat ./example.sql | podman run -i --rm docker.io/vreitech/mysqltokenizer -i

# Tokenize, but left literals untouched
cat ./example.sql | podman run -i --rm docker.io/vreitech/mysqltokenizer -l

# Tokenize, but left identifiers and literals untouched
# (i. e. just capitalize ther rest of tokens and remove line feeds and extra spaces)
cat ./example.sql | podman run -i --rm docker.io/vreitech/mysqltokenizer -il
```

If you decided to pull the image from GitHub package storage you can replace `docker.io` onto `ghcr.io` in image URI.
