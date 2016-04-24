# coding: utf-8

import sys
import os
import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from occfinder.mainplugin import TaxonTreeWidget


def main(args):
    app = QApplication(sys.argv)
    taxon_tree_widget = TaxonTreeWidget(None)
    taxon_tree_widget.show()
    app.exec_()


if __name__ == '__main__':
    print("Start")

    main(sys.argv)
