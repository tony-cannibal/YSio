
aduana_areas = {
    '/975241781343571091704/': ['Aduana', 'M1'],
    '/444542572494684692436/': ['Aduana', 'M2']
}


# areas = ['Corte M1', 'Medios M1', 'Corte M2', 'Medios M2', 'BATTERY']

tab_style = '''
    QTabWidget::pane { /* The tab widget frame */
        border: 2px solid #C2C7CB;
        border-radius: 3px;
    }

    QTabWidget::tab-bar {
        left: 5px; /* move to the right by 5px */
    }

    /* Style the tab using the tab sub-control. Note that
        it reads QTabBar _not_ QTabWidget */
    QTabBar::tab {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                    stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        border: 1px solid #C4C4C3;
        border-bottom-color: #C2C7CB; /* same as the pane color */
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        padding-left: 6px;
        min-width: 8ex;
        padding: 2px;
    }

    QTabBar::tab:selected, QTabBar::tab:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                    stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
    }

    QTabBar::tab:selected {
        border-color: #9B9B9B;
        border-bottom-color: #C2C7CB; /* same as pane color */
    }

    QTabBar::tab:!selected {
        margin-top: 2px; /* make non-selected tabs look smaller */
    }
'''


line_style = '''
    QLineEdit {
        border: 1px solid ack;
        border-radius: 3px;
        background-color: #fff;
        opacity: 100;
    }
'''