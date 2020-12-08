from abc import ABC, abstractmethod


class WordsStore:
    def __init__(self, words_array=[]):
        self._words = []  # index words - first words in chunks
        self._words_array = words_array  # list of list of words
        self._words_array_size = 0
        if words_array:
            self.update_on_words_array()

    @property
    def words_array(self):
        return self._words_array

    @words_array.setter
    def words_array(self, words_array) -> None:
        self._words_array = words_array
        self.update_on_words_array()

    @property
    def words(self):
        return self._words

    @property
    def words_array_size(self):
        return self._words_array_size

    def update_on_words_array(self):
        self._words_array_size = len(self._words_array)
        for w_list in self._words_array:
            self._words.append(w_list[0])


class AbstractLang2Loader(ABC):

    def __init__(self, source=None):
        self._words_store = WordsStore()
        #
        if source:
            self.load(source)

    @property
    def words_store(self):
        return self._words_store

    @words_store.setter
    def words_store(self, words_store) -> None:
        self._words_store = words_store

    @abstractmethod
    def load(self, source=None):
        """ load all in wordsArray as [[], []....]"""
        pass

    def clear_data(self):
        self._words_store = WordsStore()


class Lang2FileWordsLoader(AbstractLang2Loader):

    def load(self, source):
        """ source: is a file"""
        load_words_array = []
        with open(source) as f:
            word_list = []
            for line in f:
                if line.startswith("#"):
                    if len(word_list) > 0:
                        load_words_array.append(word_list)
                        word_list = []
                    continue
                word_list.append(line.strip('\n'))

            if len(word_list) > 0:
                load_words_array.append(word_list)

        self.words_store = WordsStore(load_words_array)


class Lang2WordsLoaderStub(AbstractLang2Loader):
    TEST_W_A = [["Hello", "Привет"],
                ["Gist", "Суть"]]

    def __init__(self, words_array=None):
        super().__init__(None)

        end_words_array = words_array if words_array else Lang2WordsLoaderStub.TEST_W_A
        self.words_store = WordsStore(end_words_array)

    def load(self, source: str):
        self.words_store = WordsStore(Lang2WordsLoaderStub.TEST_W_A)


if __name__ == '__main__':
    # wordsPlayFlag = True
    file = "first.lang2"

    w_stub = Lang2FileWordsLoader(file)

    w_arr = [['11', '12'], ['21', '22']]
    ws = WordsStore(w_arr)
    ws.words_array = w_arr

    w_stub = Lang2WordsLoaderStub(w_arr)


