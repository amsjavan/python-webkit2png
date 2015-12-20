import logging
import os
import signal
import sys
import webkit2png
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication

# Technically, this is a QtGui application, because QWebPage requires it
# to be. But because we will have no user interaction, and rendering can
# not start before 'app.exec_()' is called, we have to trigger our "main"
# by a timer event.

LOG_FILENAME = 'webkit2png.log'
logger = logging.getLogger('webkit2png')
def init_qtgui(display=None, style=None, qtargs=None):
    """Initiates the QApplication environment using the given args."""
    if QApplication.instance():
        logger.debug("QApplication has already been instantiated. \
                        Ignoring given arguments and returning existing QApplication.")
        return QApplication.instance()

    qtargs2 = [sys.argv[0]]

    if display:
        qtargs2.append('-display')
        qtargs2.append(display)
        # Also export DISPLAY var as this may be used
        # by flash plugin
        os.environ["DISPLAY"] = display

    if style:
        qtargs2.append('-style')
        qtargs2.append(style)

    qtargs2.extend(qtargs or [])

    return QApplication(qtargs2)
def __main_qt():
    # Render the page.
    # If this method times out or loading failed, a
    # RuntimeException is thrown
    try:
        # Initialize WebkitRenderer object
        renderer = webkit2png.WebkitRenderer()
        renderer.logger = logger
        out = open('table.png', 'bw')
        renderer.render_to_file(res='table.html',file_object=out)
        out.close()
        QApplication.exit(0)
    except RuntimeError as e:
        logger.error("main: %s" % e)
        print(sys.stderr, e)
        QApplication.exit(1)



# from skimage import data
# from skimage.viewer import ImageViewer
# import skimage
# skimage.io.imshow('/home/amir/Dropbox/Photos/Sample Album/Pensive Parakeet.png')
def dataframe2png(df):

    style = """
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    <style>
    table, td, th {
        border: 1px solid black;
        text-align: center;
    }
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th {
        font-family: Nazanin, Tahoma;
        background-color: #f2f2f2;
    }
    </style>
    </head>
    """

    with open('table.html', 'w') as file:
        file.write("<html>"+ style + df.to_html()+"</html>")

    # Initialize Qt-Application, but make this script
    # abortable via CTRL-C
    app = init_qtgui()
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    QTimer.singleShot(0, __main_qt)
    app.exec_()
    from PIL import Image
    img = Image.open('table.png')
    return img


def test():
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfVectorizer
    import pandas as pd
    import numpy as np
    import hazm
    import os
    import nazarkav as nk
    data_path = '/home/amir/Dropbox/ProgrammingProjects/Python/nazarkav/nazarkav/data'
    hotel_pol = pd.read_csv(os.path.join(data_path, 'hotel-polarity.tsv'), sep='\t')
    hotel_comment = hotel_pol['comment'].tolist()
    vectorizer = CountVectorizer(
    tokenizer=nk.Preprocessor(stem=False).tokenize,
    preprocessor=nk.Cleaner().clean,
    max_features=20)
    train_data_features = vectorizer.fit_transform(hotel_comment)
    dataframe2png(pd.DataFrame(train_data_features.toarray(),columns=vectorizer.get_feature_names
                ()).head(10))



test()