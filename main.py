# main.py
import sys
from PyQt6 import QtWidgets, QtCore, QtGui
from val_gui import Ui_MainWindow
from val import convert_currency


class CurrencyConverterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.perform_conversion)
        
        self.setup_hints()

        self.setup_validators()
    
    def setup_hints(self):
        self.ui.klineedit.setPlaceholderText("Например: USD, EUR, RUB")
        self.ui.klineedit_2.setPlaceholderText("Например: EUR, USD, RUB")
        self.ui.klineedit_3.setPlaceholderText("Введите сумму")
        self.ui.klineedit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.klineedit_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.klineedit_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    
    def setup_validators(self):
        validator = QtGui.QDoubleValidator(0, 1000000000, 2)
        validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        self.ui.klineedit_3.setValidator(validator)
        self.ui.klineedit.setMaxLength(3)
        self.ui.klineedit_2.setMaxLength(3)
    
    def perform_conversion(self):
        """Выполняет конвертацию валюты"""
        from_currency = self.ui.klineedit.text().strip()
        to_currency = self.ui.klineedit_2.text().strip()
        amount_text = self.ui.klineedit_3.text().strip()
        if not from_currency or not to_currency or not amount_text:
            self.show_message("Ошибка", "Пожалуйста, заполните все поля")
            return
        
        if len(from_currency) != 3:
            self.show_message("Ошибка", f"Код валюты должен содержать 3 символа\nВы ввели: '{from_currency}'")
            return
            
        if len(to_currency) != 3:
            self.show_message("Ошибка", f"Код валюты должен содержать 3 символа\nВы ввели: '{to_currency}'")
            return
        
        try:
            amount = float(amount_text.replace(',', '.'))
            if amount <= 0:
                self.show_message("Ошибка", "Сумма должна быть больше 0")
                return
        except ValueError:
            self.show_message("Ошибка", "Введите корректное число для суммы\nНапример: 100 или 100.50")
            return
        
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))

        result = convert_currency(from_currency, to_currency, amount)

        QtWidgets.QApplication.restoreOverrideCursor()

        self.show_message("Результат конвертации", result)
    
    def show_message(self, title, message):
        """Показывает сообщение в диалоговом окне"""
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: rgb(63, 106, 58);
                font-size: 14px;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: rgb(0, 56, 0);
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: 1px solid rgb(140, 255, 153);
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: rgb(0, 76, 0);
            }
        """)
        
        msg_box.exec()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = CurrencyConverterApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()