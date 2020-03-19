import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from design import Ui_Form as Design


class MyWidget(QWidget, Design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films.db")
        self.update_result()
        self.pushButton.clicked.connect(self.search)

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from films").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def search(self):
        m = str(self.lineEdit.text())
        cur = self.con.cursor()
        if self.comboBox.currentText() == 'Название':
            result = cur.execute("""Select * from films
                                    WHERE title = ?""", (m,)).fetchall()
        elif self.comboBox.currentText() == 'Год выпуска':
            result = cur.execute("""Select * from films
                                    WHERE year = ?""", (m,)).fetchall()
        else:
            result = cur.execute("""Select * from films
                                    WHERE duration = ?""", (m,)).fetchall()
        try:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        except:
            if self.lineEdit.text() == '':
                self.update_result()
            else:
                self.tableWidget.setRowCount(1)
                self.tableWidget.setColumnCount(1)


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())