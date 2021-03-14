from math import ceil


BOOK_PAGES_PER_SHEET = 4


class BookPrint:

    def __init__(self,
                 amountBookPages: int,
                 startPage: int,
                 endPage:int,
                 amountSheetsPerNotebook: int):
        self.amountBookPages = amountBookPages
        self.startPage = startPage
        self.endPage = endPage
        self.amountSheetsPerNotebook = amountSheetsPerNotebook

    def _parseRange(self, ranges: tuple):

        assert(ranges[1] >= ranges[0])

        sheets = list(range(ranges[0], ranges[1]))

        obverse = []
        reverse = []
        
        iteration = 0
        while len(sheets) > 1:

            pivot = ceil(len(sheets) / 2)
            result = sheets[pivot - 1: pivot + 1]

            if iteration % 2 == 0:
                obverse.append(result)
            else:
                reverse.append(result)

            sheets = sheets[: pivot - 1] + sheets[pivot + 1:]
                
            iteration += 1

        if sheets:
            obverse.append(sheets) if iteration % 2 == 0 else reverse.append(sheets)

        return obverse, reverse

    def _parseBook(self):

        result = []
        iteration = 0

        existed = BOOK_PAGES_PER_SHEET * (iteration + 1)
        pagesPerNotebook = BOOK_PAGES_PER_SHEET * self.amountSheetsPerNotebook

        while existed <= self.endPage - self.startPage:

            iteration += 1

            if iteration % self.amountSheetsPerNotebook == 0:
                result.append(self._parseRange((existed - pagesPerNotebook + self.startPage,
                                                existed - pagesPerNotebook + BOOK_PAGES_PER_SHEET * self.amountSheetsPerNotebook + self.startPage)))

            existed = BOOK_PAGES_PER_SHEET * (iteration + 1)

            """if iteration % self.amountSheetsPerNotebook != 0:
            unusedPages = (self.startPage + existed - (iteration % self.amountSheetsPerNotebook + 1) * BOOK_PAGES_PER_SHEET,
                           self.endPage + 1)
            result.append(self._parseRange(unusedPages))"""

        unusedPages = (self.startPage + existed - (iteration % self.amountSheetsPerNotebook + 1) * BOOK_PAGES_PER_SHEET,
                       self.endPage + 1)
        result.append(self._parseRange(unusedPages))

        return result

    def getRowsToPrint(self, amountNotebookPerRun: int = 3):

        parsedBook = self._parseBook()
        result = {}

        run = 1
        for iteration, notebook in enumerate(parsedBook, 1):
            obverse = self._implodeSheetsToRow(notebook[0][::-1])
            reverse = self._implodeSheetsToRow(notebook[1], switchPairs=True)

            if run not in result:
                result[run] = {
                    'obverse': obverse,
                    'reverse': reverse,
                }
            else:
                result[run]['obverse'] = obverse + ',' + result[run]['obverse']
                result[run]['reverse'] += ',' + reverse

            run = run if iteration % amountNotebookPerRun != 0 else run + 1

        return result

    def _implodeSheetsToRow(self, listOfSheets, switchPairs: bool = False):
        result = ''
        for pair in listOfSheets:
            result += ','.join(map(str, pair[::-1] if switchPairs else pair)) + ','

        return result.rstrip(',')


def test():

    book = BookPrint(489, 3, 488, 4)

    result = book.getRowsToPrint()

    for iteration in result:
        print(iteration, " прогон")
        print("Лицевая сторона \t", result[iteration]['reverse'])
        print("Тыльная сторона \t", result[iteration]['obverse'])
        print()


def start():
    
    amountBookPages = int(input('Число страниц в книге...'))
    startPage = int(input('Первая страница...'))
    endPage = int(input('Последняя страница...'))
    amountSheetsPerNotebook = int(input('Число листов на одну тетрадь...'))

    book = Book(amountBookPages, startPage, endPage, amountSheetsPerNotebook)

    result = book.getRowsToPrint()

    for iteration in result:
        print(iteration, " прогон")
        print("Лицевая сторона \t", result[iteration]['reverse'])
        print("Тыльная сторона \t", result[iteration]['obverse'])
        print()


def main():

    test()


if __name__ == "__main__":
    main()
