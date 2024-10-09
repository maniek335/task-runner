import openpyxl


class Spreadsheet:
    def __init__(self, path: str):
        self.path = path

        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.workbook.save(self.path)

    def append(self, data: list[str]):
        self.sheet.append(data)
