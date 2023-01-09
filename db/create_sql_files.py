RUS_WORDS_TXT = 'russian_singular_and_plural.txt'
FN = 'sql/russian_singular_and_plural.sql'
ENCODING = 'utf-8'


def count_lines(file_name, chunk_size=1 << 13):
    with open(file_name) as file:
        return sum(chunk.count('\n')
                   for chunk in iter(lambda: file.read(chunk_size), ''))


def init_russian_words():
    with open(FN, 'w', encoding=ENCODING) as f:
        f.write('INSERT INTO words(word, lang, is_active) VALUES \n')
        with open(RUS_WORDS_TXT, 'r', encoding=ENCODING) as file:
            for i in range(count_lines(RUS_WORDS_TXT)):
                word = file.readline()
                line = "('" + word.strip() + "', " + "'RU'" + ', ' + 'true' + '),\n'
                f.write(line)

