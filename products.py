import requests
import json
import sys
import time
import concurrent.futures
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon


def get_product(url) -> dict:
    """Obtains single product from given URL"""
    response = requests.get(url)
    return response.json()

def threader(sublist) -> list:
    """Process a sublist of URLs using threads"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as thread_exe:
        return list(thread_exe.map(get_product, sublist))

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """Initialize UI and connect a button with method"""
        super().__init__()
        self.ui = loadUi("ui/products.ui", self)
        self.ui.pushButton.clicked.connect(self.get_products)

        # Initializes pair of process-thread number
        self.process_thread_numbers = {2:50, 5:20, 10:10, 20:5, 50:2}
        self.n_processes = int(self.ui.comboBox.currentText())
        self.ui.label_4.setText(f"Selected: {str(self.n_processes)} processes, {str(self.process_thread_numbers[self.n_processes])} threads")
        
        # Signals any change in the combobox selection
        self.comboBox.currentIndexChanged.connect(self.update_label)

    def update_label(self):
        """Changes label as soon as combobox selected item changes"""
        self.n_processes = int(self.ui.comboBox.currentText())
        self.ui.label_4.setText(f"Selected: {str(self.n_processes)} processes, {str(self.process_thread_numbers[self.n_processes])} threads")

    def get_products(self) -> None:
        """Obtains products from given number of URLs in parallel and writes them to JSON"""

        # A list of all URLs
        urls = [f'https://dummyjson.com/products/{str(i)}' for i in range(1, 101)]

        # Initializing empty list to store URL sublists
        url_sublists = []
        first, last = 0, self.process_thread_numbers[self.n_processes]

        # Create sublists and add to url_sublists list
        while last < 101:
            sublist = urls[first:last]
            first = last
            last = first + self.process_thread_numbers[self.n_processes]
            url_sublists.append(sublist)

        # Perform paallel processing on each sublist
        self.products = [] # This will store all the obtained products
        start_time = time.perf_counter()
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as process_exe:
            results = process_exe.map(threader, url_sublists)
            for result in results:
                self.products.extend(result)
        end_time = time.perf_counter()

        with open('products.json', 'w') as f:
            json.dump(self.products, f, indent=4)

        # Empty products list for future use
        self.products.clear()

        # Set labels
        self.ui.label.setStyleSheet("color:rgb(0, 255, 127)")
        self.ui.label.setText("Success")
        self.ui.label_2.setText(f"Obtained 100 products in {round(end_time - start_time, 3)} seconds")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("TBC Academy")
    window.setWindowIcon(QIcon("resources/tbcicon.png"))
    window.show()
    sys.exit(app.exec_())
