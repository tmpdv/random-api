RUS_WORDS_TXT = 'txt/russian_singular_and_plural.txt'
RUS_WORDS_SQL = 'sql/russian_singular_and_plural.sql'
GENDERS_TXT = 'txt/genders.txt'
GENDERS_SQL = 'sql/genders.sql'
ENCODING = 'utf-8'


def count_lines(file_name, chunk_size=1 << 13):
    with open(file_name) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


def init_russian_words():
    with open(RUS_WORDS_SQL, 'w', encoding=ENCODING) as f:
        f.write('INSERT INTO words(word, lang, is_active) VALUES \n')
        with open(RUS_WORDS_TXT, 'r', encoding=ENCODING) as file:
            for i in range(count_lines(RUS_WORDS_TXT)):
                word = file.readline()
                line = "('" + word.strip() + "', " + "'RU'" + ', ' + 'true' + '),\n'
                f.write(line)


def init_genders():
    with open(GENDERS_SQL, 'w', encoding=ENCODING) as f:
        f.write('INSERT INTO genders(name, is_active) VALUES \n')
        with open(GENDERS_TXT, 'r', encoding=ENCODING) as file:
            for i in range(count_lines(GENDERS_TXT)):
                name = file.readline()
                line = "('" + name.strip() + "', " + 'true' + '),\n'
                f.write(line)

init_genders()
