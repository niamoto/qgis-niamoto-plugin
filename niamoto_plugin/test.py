# coding: utf-8

import sys

from PyQt4.QtGui import *
from niamoto_plugin.mainplugin import TaxonTreeWidget


def main(args):
    app = QApplication(sys.argv)
    taxon_tree_widget = TaxonTreeWidget(None)
    taxon_tree_widget.show()
    app.exec_()


if __name__ == '__main__':
    print("Start")

    main(sys.argv)
