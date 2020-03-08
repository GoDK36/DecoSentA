# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from nagisa import tagging
from PyQt5 import QtCore, QtGui, QtWidgets
from dateutil.parser import parse
import pandas, re, codecs, os, pycrfsuite, time, twint, datetime, Stemmer, jieba, gensim, multiprocessing, csv
from kiwipiepy import Kiwi
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn import metrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import mplcursors
from matplotlib import font_manager, rc
from matplotlib import style
from wordcloud import *
import plotnine
from plotnine import *
import DecoSentA_Resource_rc

class subwindow(QtWidgets.QWidget):
    def createWindow(self, WindowWidth, WindowHeight):
       parent=None
       super(subwindow,self).__init__(parent)
       self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
       self.resize(WindowWidth, WindowHeight)

class Ui_MainWindow(object):
    global Stop_words, Font
    Stop_words = 'Stopwords.txt'
    Font = 'malgun.ttf'
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 600))
        MainWindow.setWindowTitle("DecoSentA")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 601, 601))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/image/bg2.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        self.menuPreProcessing = QtWidgets.QMenu(self.menubar)
        self.menuPreProcessing.setObjectName("menuPreProcessing")
        self.menuExpand_and_Annotate = QtWidgets.QMenu(self.menubar)
        self.menuExpand_and_Annotate.setObjectName("menuExpand_and_Annotate")
        self.menuSentiment_Analysis = QtWidgets.QMenu(self.menubar)
        self.menuSentiment_Analysis.setObjectName("menuSentiment_Analysis")
        self.menuVisualize = QtWidgets.QMenu(self.menubar)
        self.menuVisualize.setObjectName("menuVisualize")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionPreProcess_By_PGT = QtWidgets.QAction(MainWindow)
        self.actionPreProcess_By_PGT.setObjectName("actionPreProcess_By_PGT")
        self.actionAuto_Spacing = QtWidgets.QAction(MainWindow)
        self.actionAuto_Spacing.setObjectName("actionAuto_Spacing")
        self.actionTwitter_Scrapping = QtWidgets.QAction(MainWindow)
        self.actionTwitter_Scrapping.setObjectName("actionTwitter_Scrapping")
        self.actionWord2Vec = QtWidgets.QAction(MainWindow)
        self.actionWord2Vec.setObjectName("actionWord2Vec")
        self.actionToSAC_Annotator = QtWidgets.QAction(MainWindow)
        self.actionToSAC_Annotator.setObjectName("actionToSAC_Annotator")
        self.actionWordCloud = QtWidgets.QAction(MainWindow)
        self.actionWordCloud.setObjectName("actionWordCloud_2")
        self.actionAbout_DICORA = QtWidgets.QAction(MainWindow)
        self.actionAbout_DICORA.setObjectName("actionAbout_DICORA")
        self.actionSSA_based_Trend = QtWidgets.QAction(MainWindow)
        self.actionSSA_based_Trend.setObjectName("actionSSA_based_Trend")
        self.actionSESACbasedSSA = QtWidgets.QAction(MainWindow)
        self.actionSESACbasedSSA.setObjectName("actionSESACbasedSSA")
        self.actionPolaLexLGGbasedSSA = QtWidgets.QAction(MainWindow)
        self.actionPolaLexLGGbasedSSA.setObjectName("actionPolaLexLGGbasedSSA")
        self.actionLGGbasedFSA = QtWidgets.QAction(MainWindow)
        self.actionLGGbasedFSA.setObjectName("actionLGGbasedFSA")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuPreProcessing.addAction(self.actionTwitter_Scrapping)
        self.menuPreProcessing.addAction(self.actionAuto_Spacing)
        self.menuPreProcessing.addAction(self.actionPreProcess_By_PGT)
        self.menuExpand_and_Annotate.addAction(self.actionWord2Vec)
        self.menuExpand_and_Annotate.addAction(self.actionToSAC_Annotator)
        self.menuSentiment_Analysis.addAction(self.actionSESACbasedSSA)
        self.menuSentiment_Analysis.addAction(self.actionPolaLexLGGbasedSSA)
        self.menuSentiment_Analysis.addAction(self.actionLGGbasedFSA)
        self.menuVisualize.addAction(self.actionWordCloud)
        self.menuVisualize.addAction(self.actionSSA_based_Trend)
        self.menuHelp.addAction(self.actionAbout_DICORA)
        self.menuHelp.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuPreProcessing.menuAction())
        self.menubar.addAction(self.menuExpand_and_Annotate.menuAction())
        self.menubar.addAction(self.menuSentiment_Analysis.menuAction())
        self.menubar.addAction(self.menuVisualize.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionTwitter_Scrapping.triggered.connect (self.Tweetscrap_module)
        self.actionAuto_Spacing.triggered.connect (self.Autospace_module)
        self.actionPreProcess_By_PGT.triggered.connect(self.PGT_module)
        self.actionWord2Vec.triggered.connect (self.Word2Vec_module)
        self.actionToSAC_Annotator.triggered.connect (self.ToSAC_Annotator_module)
        self.actionSESACbasedSSA.triggered.connect (self.SESACbasedSSA_module)
        self.actionPolaLexLGGbasedSSA.triggered.connect (self.PolaLexLGGbasedSSA_module)
        self.actionLGGbasedFSA.triggered.connect (self.LGGbasedFSA_module)
        self.actionWordCloud.triggered.connect (self.MorphemeCloud_module)
        self.actionSSA_based_Trend.triggered.connect(self.SSAbasedTrend_module)
        self.actionAbout_DICORA.triggered.connect (self.AboutDicora_Info)
        self.actionPreferences.triggered.connect (self.Preference_setting)


    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        self.menuPreProcessing.setTitle (_translate ("MainWindow", "PreProcessing"))
        self.menuExpand_and_Annotate.setTitle (_translate ("MainWindow", "Expand/Annotate"))
        self.menuSentiment_Analysis.setTitle (_translate ("MainWindow", "Sentiment Analysis"))
        self.menuVisualize.setTitle (_translate ("MainWindow", "Visualize"))
        self.menuHelp.setTitle (_translate ("MainWindow", "Help"))
        self.actionPreProcess_By_PGT.setText (_translate ("MainWindow", "PreProcess by PGT"))
        self.actionAuto_Spacing.setText (_translate ("MainWindow", "Auto-Spacing"))
        self.actionTwitter_Scrapping.setText (_translate ("MainWindow", "Twitter Scrapping"))
        self.actionWord2Vec.setText (_translate ("MainWindow", "Expanding Lexica via Word2Vec"))
        self.actionToSAC_Annotator.setText (_translate ("MainWindow", "ToSAC-Annotator"))
        self.actionSESACbasedSSA.setText (_translate ("MainWindow", "SESACbasedSSA"))
        self.actionPolaLexLGGbasedSSA.setText (_translate ("MainWindow", "PolaLexLGGbasedSSA"))
        self.actionLGGbasedFSA.setText(_translate("MainWindow","LGGbasedFSA"))
        self.actionAbout_DICORA.setText (_translate ("MainWindow", "about DICORA"))
        self.actionPreferences.setText (_translate ("MainWindow", "Preferences"))
        self.actionWordCloud.setText (_translate ("MainWindow", "WordCloud"))
        self.actionSSA_based_Trend.setText (_translate ("MainWindow", "SSAbased-Trend"))

    def Process(self):
        self.Process_window = subwindow ()
        self.Process_window.setObjectName ("Process")
        self.Process_window.createWindow(370, 10)
        self.Process_label = QtWidgets.QLabel (self.Process_window)
        self.Process_label.setGeometry (QtCore.QRect (0, 0, 371, 101))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.Process_label.setFont (font)
        self.Process_label.setAlignment (QtCore.Qt.AlignCenter)
        self.Process_label.setObjectName ("Process_label")
        _translate = QtCore.QCoreApplication.translate
        self.Process_window.setWindowTitle (_translate ("Process", "Processing..."))
        self.Process_label.setText (_translate ("Process", "Processing.."))
        self.Process_label.setText ('Complete')
        self.Process_window.show()

    def Preference_setting(self):
        self.Preferences_window = subwindow()
        self.Preferences_window.createWindow(460, 160)
        self.Preferences_window.setObjectName('Preferences')
        self.frame = QtWidgets.QFrame (self.Preferences_window)
        self.frame.setGeometry (QtCore.QRect (10, 40, 441, 111))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.Pref_apply = QtWidgets.QPushButton (self.frame)
        self.Pref_apply.setGeometry (QtCore.QRect (180, 80, 75, 23))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (False)
        font.setWeight (50)
        self.Pref_apply.setFont (font)
        self.Pref_apply.setObjectName ("Pref_apply")
        self.Stopwords_path = QtWidgets.QLineEdit (self.frame)
        self.Stopwords_path.setGeometry (QtCore.QRect (180, 20, 171, 20))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.Stopwords_path.setFont (font)
        self.Stopwords_path.setClearButtonEnabled (False)
        self.Stopwords_path.setObjectName ("Stopwords_path")
        self.Font_browse = QtWidgets.QPushButton (self.frame)
        self.Font_browse.setGeometry (QtCore.QRect (360, 50, 75, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (False)
        font.setWeight (50)
        self.Font_browse.setFont (font)
        self.Font_browse.setObjectName ("Stopwords_browse_2")
        self.label = QtWidgets.QLabel (self.frame)
        self.label.setGeometry (QtCore.QRect (0, 20, 171, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        font.setBold (False)
        font.setWeight (50)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName ("label")
        self.Stopwords_browse = QtWidgets.QPushButton (self.frame)
        self.Stopwords_browse.setGeometry (QtCore.QRect (360, 20, 75, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (False)
        font.setWeight (50)
        self.Stopwords_browse.setFont (font)
        self.Stopwords_browse.setObjectName ("Stopwords_browse")
        self.Regular_font_loc = QtWidgets.QLineEdit (self.frame)
        self.Regular_font_loc.setGeometry (QtCore.QRect (190, 50, 161, 21))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.Regular_font_loc.setFont (font)
        self.Regular_font_loc.setClearButtonEnabled (False)
        self.Regular_font_loc.setObjectName ("Regular_font_loc")
        self.label_3 = QtWidgets.QLabel (self.frame)
        self.label_3.setGeometry (QtCore.QRect (-20, 50, 201, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        font.setBold (False)
        font.setWeight (50)
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        self.label_4 = QtWidgets.QLabel (self.Preferences_window)
        self.label_4.setGeometry (QtCore.QRect (10, 10, 171, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        font.setItalic (True)
        self.label_4.setFont (font)
        self.label_4.setObjectName ("label_4")
        _translate = QtCore.QCoreApplication.translate
        self.Preferences_window.setWindowTitle (_translate ("Preferences", "Preferences"))
        self.Pref_apply.setText (_translate ("Preferences", "Apply"))
        self.Stopwords_path.setText (_translate ("Preferences", "Stopwords.txt"))
        self.Font_browse.setText (_translate ("Preferences", "Browse.."))
        self.label.setText (_translate ("Preferences", "Stopswords Setting:"))
        self.Stopwords_browse.setText (_translate ("Preferences", "Browse.."))
        self.Regular_font_loc.setText (_translate ("Preferences", "malgun.ttf"))
        self.label_3.setText (_translate ("Preferences", "Regular Font Location:"))
        self.label_4.setText (_translate ("Preferences", "Preferences Setting"))

        self.Stopwords_browse.released.connect (self.Pref_stopwords_open)
        self.Font_browse.released.connect (self.Pref_font_open)
        self.Pref_apply.released.connect(self.Pref_Appling)

        self.Preferences_window.show()

    def Pref_stopwords_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.Stopwords_path.setText((str(fname)).split("', '")[0][2:])

    def Pref_font_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.Regular_font_loc.setText((str(fname)).split("', '")[0][2:])

    def Pref_Appling(self):
        global Stop_words, Font
        Stop_words = self.Stopwords_path.text()
        Font = self.Regular_font_loc.text()
        self.Preferences_window.close()


    ###PGT Module description###
    def PGT_module(self):
        self.PGT_window = subwindow ()
        self.PGT_window.createWindow (850, 287)
        self.PGT_window.setObjectName ("PGT")
        self.horizontalLayout = QtWidgets.QHBoxLayout (self.PGT_window)
        self.horizontalLayout.setObjectName ("horizontalLayout")
        self.widget = QtWidgets.QWidget (self.PGT_window)
        self.widget.setObjectName ("widget")
        self.pgt_corpus = QtWidgets.QLineEdit (self.widget)
        self.pgt_corpus.setGeometry (QtCore.QRect (30, 80, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.pgt_corpus.setFont (font)
        self.pgt_corpus.setClearButtonEnabled (True)
        self.pgt_corpus.setObjectName ("pgt_corpus")
        self.label_1 = QtWidgets.QLabel (self.widget)
        self.label_1.setGeometry (QtCore.QRect (0, 0, 831, 31))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label_1.setFont (font)
        self.label_1.setAlignment (QtCore.Qt.AlignCenter)
        self.label_1.setObjectName ("label_1")
        self.pgt_apply_save = QtWidgets.QPushButton (self.widget)
        self.pgt_apply_save.setGeometry (QtCore.QRect (190, 220, 121, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.pgt_apply_save.setFont (font)
        self.pgt_apply_save.setObjectName ("pgt_apply_save")
        self.label_4 = QtWidgets.QLabel (self.widget)
        self.label_4.setGeometry (QtCore.QRect (340, 70, 511, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (True)
        font.setWeight (75)
        self.label_4.setFont (font)
        self.label_4.setAutoFillBackground (False)
        self.label_4.setObjectName ("label_4")
        self.pgt_file_loc = QtWidgets.QLineEdit (self.widget)
        self.pgt_file_loc.setGeometry (QtCore.QRect (30, 150, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.pgt_file_loc.setFont (font)
        self.pgt_file_loc.setClearButtonEnabled (True)
        self.pgt_file_loc.setObjectName ("pgt_file_loc")
        self.label_2 = QtWidgets.QLabel (self.widget)
        self.label_2.setGeometry (QtCore.QRect (30, 50, 251, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_2.setFont (font)
        self.label_2.setObjectName ("label_2")
        self.pgt_target_browse = QtWidgets.QPushButton (self.widget)
        self.pgt_target_browse.setGeometry (QtCore.QRect (190, 80, 121, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.pgt_target_browse.setFont (font)
        self.pgt_target_browse.setObjectName ("pgt_target_browse")
        self.pgt_setting_browse = QtWidgets.QPushButton (self.widget)
        self.pgt_setting_browse.setGeometry (QtCore.QRect (190, 150, 121, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.pgt_setting_browse.setFont (font)
        self.pgt_setting_browse.setObjectName ("pgt_setting_browse")
        self.label_3 = QtWidgets.QLabel (self.widget)
        self.label_3.setGeometry (QtCore.QRect (30, 120, 251, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_3.setFont (font)
        self.label_3.setObjectName ("label_3")
        self.frame = QtWidgets.QFrame (self.widget)
        self.frame.setGeometry (QtCore.QRect (330, 100, 491, 151))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.cArabicN = QtWidgets.QCheckBox (self.frame)
        self.cArabicN.setGeometry (QtCore.QRect (20, 120, 231, 21))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (10)
        self.cArabicN.setFont (font)
        self.cArabicN.setObjectName ("cArabicN")
        self.cPgtAp = QtWidgets.QCheckBox (self.frame)
        self.cPgtAp.setGeometry (QtCore.QRect (20, 20, 231, 21))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (10)
        self.cPgtAp.setFont (font)
        self.cPgtAp.setChecked (True)
        self.cPgtAp.setObjectName ("cPgtAp")
        self.cPunct = QtWidgets.QCheckBox (self.frame)
        self.cPunct.setGeometry (QtCore.QRect (20, 70, 231, 21))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (10)
        self.cPunct.setFont (font)
        self.cPunct.setObjectName ("cPunct")
        self.cReloc = QtWidgets.QCheckBox (self.frame)
        self.cReloc.setGeometry (QtCore.QRect (250, 120, 241, 21))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (10)
        self.cReloc.setFont (font)
        self.cReloc.setObjectName ("cReloc")
        self.cLower = QtWidgets.QCheckBox (self.frame)
        self.cLower.setGeometry (QtCore.QRect (250, 70, 241, 21))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (10)
        self.cLower.setFont (font)
        self.cLower.setObjectName ("cLower")
        self.cRepeat = QtWidgets.QCheckBox (self.frame)
        self.cRepeat.setGeometry (QtCore.QRect (250, 20, 240, 21))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (10)
        self.cRepeat.setFont (font)
        self.cRepeat.setObjectName ("cRepeat")
        self.pgt_result_loc = QtWidgets.QLineEdit (self.widget)
        self.pgt_result_loc.setGeometry (QtCore.QRect (30, 220, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.pgt_result_loc.setFont (font)
        self.pgt_result_loc.setClearButtonEnabled (True)
        self.pgt_result_loc.setObjectName ("pgt_result_loc")
        self.label_5 = QtWidgets.QLabel (self.widget)
        self.label_5.setGeometry (QtCore.QRect (30, 190, 251, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_5.setFont (font)
        self.label_5.setObjectName ("label_5")
        self.horizontalLayout.addWidget (self.widget)

        _translate = QtCore.QCoreApplication.translate
        self.PGT_window.setWindowTitle (_translate ("PGT", "Preprocess by PGT"))
        self.pgt_corpus.setText (_translate ("PGT", "No file seleted"))
        self.label_1.setText (_translate ("PGT", "Preprocess by PGT"))
        self.pgt_apply_save.setText (_translate ("PGT", "Applying / Save"))
        self.label_4.setText (_translate ("PGT", "Preprocessing Options:"))
        self.pgt_file_loc.setText (_translate ("PGT", "No file seleted"))
        self.label_2.setText (_translate ("PGT", "Target Text:"))
        self.pgt_target_browse.setText (_translate ("PGT", "Browse.."))
        self.pgt_setting_browse.setText (_translate ("PGT", "Browse.."))
        self.label_3.setText (_translate ("PGT", "PGT Setting(.csv):"))
        self.cArabicN.setText (_translate ("PGT", "Remove Arabic Numerals"))
        self.cPgtAp.setText (_translate ("PGT", "Applying PGT"))
        self.cPunct.setText (_translate ("PGT", "Remove Punctuation Marks"))
        self.cReloc.setText (_translate ("PGT", "Relocating Enclosed Tokens "))
        self.cLower.setText (_translate ("PGT", "Lowercasing"))
        self.cRepeat.setText (_translate ("PGT", "Normalize Repeated Letters"))
        self.pgt_result_loc.setText (_translate ("PGT", ".txt format"))
        self.label_5.setText (_translate ("PGT", "Result File:"))

        self.pgt_apply_save.released.connect(self.Process)
        self.pgt_apply_save.released.connect (self.PGT_Full_func)
        self.pgt_target_browse.released.connect(self.PGT_Targetfile_open)
        self.pgt_setting_browse.released.connect(self.PGT_Setting_open)
        self.PGT_window.show()

    def PGT_Targetfile_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.pgt_corpus.setText((str(fname)).split("', '")[0][2:])

    def PGT_Setting_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.pgt_file_loc.setText((str(fname)).split("', '")[0][2:])

    def PGT_Full_func(self):
        try:
            text = codecs.open (self.pgt_corpus.text(), encoding='utf-8-sig').read()
            if self.cPunct.isChecked() == True:
                text = re.sub (r'[\'\"\.\,\?\!\:\;]+', '', text)
            if self.cArabicN.isChecked() == True:
                text = re.sub (r'[\d]+', '', text)
            if self.cRepeat.isChecked() == True:
                text = re.sub (r'([ㄱ-ㅎㅏ-ㅣ]{2})[ㄱ-ㅎㅏ-ㅣ]+', '\\1', text)
            if self.cLower.isChecked() == True:
                text = text.lower ()
            if self.cReloc.isChecked() == True:
                text = re.sub (r'([가-힣]+)([\(\[\-\<])([\w\d\s]+)([\)\]\-\>])([가-힣]+)', '\\1\\5 \\2\\3\\4', text)
            if self.cPgtAp.isChecked() == True:
                pgt_original = pandas.read_csv(self.pgt_file_loc.text(), names=['0','1'] ,encoding='utf-8-sig')
                for i, j in zip(list(pgt_original['0']), list(pgt_original['1'])):
                    text = re.sub (i, j, text)
            pgt_applying_text = text
            if os.path.isdir ("Result") == False:
                os.mkdir ("Result")
            save_temp = os.path.join ('Result', self.pgt_result_loc.text ())
            saveloc = codecs.open (save_temp, 'w', encoding='utf-8')
            saveloc.write (pgt_applying_text)
            saveloc.close ()
            os.startfile (save_temp)
            self.Process_window.close()
        except UnicodeDecodeError:
            pass


    ###AutoSpacing Module description###
    def Autospace_module(self):
        self.Autospace_window = subwindow ()
        _translate = QtCore.QCoreApplication.translate
        self.Autospace_window.createWindow (500, 320)
        self.Autospace_window.setObjectName ("AutoSpacing")
        sizePolicy = QtWidgets.QSizePolicy (QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch (0)
        sizePolicy.setVerticalStretch (0)
        sizePolicy.setHeightForWidth (self.Autospace_window.sizePolicy ().hasHeightForWidth ())
        self.Autospace_window.setSizePolicy (sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout (self.Autospace_window)
        self.verticalLayout.setObjectName ("verticalLayout")
        self.widget = QtWidgets.QWidget (self.Autospace_window)
        self.widget.setAutoFillBackground (False)
        self.widget.setObjectName ("widget")
        self.label = QtWidgets.QLabel (self.widget)
        self.label.setGeometry (QtCore.QRect (0, 10, 481, 31))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setWeight (75)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignCenter)
        self.label.setObjectName ("label")
        self.frame = QtWidgets.QFrame (self.widget)
        self.frame.setGeometry (QtCore.QRect (10, 40, 461, 151))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.label_2 = QtWidgets.QLabel (self.frame)
        self.label_2.setGeometry (QtCore.QRect (20, 10, 241, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_2.setFont (font)
        self.label_2.setObjectName ("label_2")
        self.corpus_for_training = QtWidgets.QLineEdit (self.frame)
        self.corpus_for_training.setGeometry (QtCore.QRect (20, 40, 241, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.corpus_for_training.setFont (font)
        self.corpus_for_training.setClearButtonEnabled (True)
        self.corpus_for_training.setObjectName ("corpus_for_training")
        self.label_3 = QtWidgets.QLabel (self.frame)
        self.label_3.setGeometry (QtCore.QRect (20, 80, 241, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_3.setFont (font)
        self.label_3.setObjectName ("label_3")
        self.target_corpus = QtWidgets.QLineEdit (self.frame)
        self.target_corpus.setGeometry (QtCore.QRect (20, 110, 241, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.target_corpus.setFont (font)
        self.target_corpus.setClearButtonEnabled (True)
        self.target_corpus.setObjectName ("target_corpus")
        self.training_browse = QtWidgets.QPushButton (self.frame)
        self.training_browse.setGeometry (QtCore.QRect (270, 40, 81, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.training_browse.setFont (font)
        self.training_browse.setObjectName ("training_browse")
        self.target_browse = QtWidgets.QPushButton (self.frame)
        self.target_browse.setGeometry (QtCore.QRect (270, 110, 81, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.target_browse.setFont (font)
        self.target_browse.setObjectName ("target_browse")
        self.train_button = QtWidgets.QPushButton (self.frame)
        self.train_button.setGeometry (QtCore.QRect (370, 40, 81, 101))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (True)
        font.setWeight (75)
        self.train_button.setFont (font)
        self.train_button.setObjectName ("train_button")
        self.frame_2 = QtWidgets.QFrame (self.widget)
        self.frame_2.setGeometry (QtCore.QRect (10, 200, 461, 91))
        self.frame_2.setFrameShape (QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName ("frame_2")
        self.label_4 = QtWidgets.QLabel (self.frame_2)
        self.label_4.setGeometry (QtCore.QRect (20, 10, 241, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_4.setFont (font)
        self.label_4.setObjectName ("label_4")
        self.AS_result_loc = QtWidgets.QLineEdit (self.frame_2)
        self.AS_result_loc.setGeometry (QtCore.QRect (20, 40, 241, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.AS_result_loc.setFont (font)
        self.AS_result_loc.setClearButtonEnabled (True)
        self.AS_result_loc.setObjectName ("AS_result_loc")
        self.export_button = QtWidgets.QPushButton (self.frame_2)
        self.export_button.setGeometry (QtCore.QRect (270, 40, 181, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (True)
        font.setWeight (75)
        self.export_button.setFont (font)
        self.export_button.setObjectName ("export_button")
        self.verticalLayout.addWidget (self.widget)

        _translate = QtCore.QCoreApplication.translate
        self.Autospace_window.setWindowTitle (_translate ("MainWindow", "Auto-Spacing"))
        self.label.setText (_translate ("MainWindow", "Auto-Spacing Module"))
        self.label_2.setText (_translate ("MainWindow", "Training Text:"))
        self.corpus_for_training.setText (_translate ("MainWindow", "No file seleted"))
        self.label_3.setText (_translate ("MainWindow", "Target Text:"))
        self.target_corpus.setText (_translate ("MainWindow", "No file seleted"))
        self.training_browse.setText (_translate ("MainWindow", "Browse.."))
        self.target_browse.setText (_translate ("MainWindow", "Browse.."))
        self.train_button.setText (_translate ("MainWindow", "Train!"))
        self.label_4.setText (_translate ("MainWindow", "Result File:"))
        self.AS_result_loc.setText (_translate ("MainWindow", ".txt format"))
        self.export_button.setText (_translate ("MainWindow", "Extract Output"))

        self.train_button.released.connect(self.Process)
        self.train_button.released.connect (self.Autospace_Training)
        self.export_button.released.connect (self.Target_In_Output)
        self.training_browse.released.connect(self.AS_Trainfile_open)
        self.target_browse.released.connect(self.AS_Target_file_open)
        self.Autospace_window.show()

    def AS_Trainfile_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.corpus_for_training.setText((str(fname)).split("', '")[0][2:])
    def AS_Target_file_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.target_corpus.setText((str(fname)).split("', '")[0][2:])

    def raw2corpus(self, corpus):
        raw = codecs.open (corpus, encoding='utf-8')
        raw_sentences = raw.read ().split ('\n')
        training_text = ""
        sentences = []
        for raw_sentence in raw_sentences:
            if not raw_sentence:
                continue
            text = re.sub (r'( )+', ' ', raw_sentence).strip ()
            taggeds = []
            for i in range (len (text)):
                if i == 0:
                    taggeds.append ('{}/B'.format (text[i]))
                elif text[i] != ' ':
                    successor = text[i - 1]
                    if successor == ' ':
                        taggeds.append ('{}/B'.format (text[i]))
                    else:
                        taggeds.append ('{}/I'.format (text[i]))
            sentences.append (' '.join (taggeds))
        training_text += '\n'.join (sentences)
        return training_text

    def corp2raw(self, corpus):
        corpus_sentences = corpus.split('\n')
        restore = ""
        sentences = []
        for corpus_sentence in corpus_sentences:
            taggeds = corpus_sentence.split (' ')
            text = ''
            len_taggeds = len(taggeds)
            for tagged in taggeds:
                try:
                    word, tag = tagged.split ('/')
                    if word and tag:
                        if tag == 'B':
                            text += ' ' + word
                        else:
                            text += word
                except:
                    pass
            sentences.append(text.strip())
        restore += '\n'.join(sentences)
        return restore

    def corp2sent(self, corpus):
        raws = corpus.split ('\n')
        sentences = []
        for raw in raws:
            tokens = raw.split (' ')
            sentence = []
            for token in tokens:
                try:
                    word, tag = token.split ('/')
                    if word and tag:
                        sentence.append ([word, tag])
                except:
                    pass
            sentences.append (sentence)
        return sentences

    def index2feature(self, sent, i, offset):
        word, tag = sent[i + offset]
        if offset < 0:
            sign = ''
        else:
            sign = '+'
        return '{}{}:word={}'.format (sign, offset, word)

    def word2features(self, sent, i):
        L = len(sent)
        word, tag = sent[i]
        features = ['bias']
        features.append(self.index2feature(sent, i, 0))
        if i > 1:
            features.append(self.index2feature(sent, i, -2))
        if i > 0:
            features.append(self.index2feature(sent, i, -1))
        else:
            features.append('bos')
        if i < L - 2:
            features.append(self.index2feature(sent, i, 2))
        if i < L - 1:
            features.append (self.index2feature(sent, i, 1))
        else:
            features.append('eos')
        return features

    def sentence2words(self, sent):
        return [word for word, tag in sent]

    def sentence2tags(self, sent):
        return [tag for word, tag in sent]

    def sentence2features(self, sent):
        return [self.word2features(sent, i) for i in range (len (sent))]

    def flush(self, X, Y):
        result = ""
        for x, y in zip (X, Y):
            result += ' '.join (['{}/{}'.format (feature[1].split ('=')[1], tag) for feature, tag in zip (x, y)])
            result += ('\n')
        return result

    def Autospace_Training(self):
        train = self.raw2corpus (self.corpus_for_training.text ())
        train_sents = self.corp2sent(train)
        train_x = [self.sentence2features (sent) for sent in train_sents]
        train_y = [self.sentence2tags (sent) for sent in train_sents]
        trainer = pycrfsuite.Trainer()

        for x, y in zip(train_x, train_y):
            trainer.append (x, y)
        trainer.train ('autospacing.crfsuite')
        time.sleep (3)
        self.Process_window.close ()


    def Target_In_Output(self):
        tagger = pycrfsuite.Tagger()
        tagger.open('autospacing.crfsuite')
        target = self.raw2corpus(self.target_corpus.text())
        test_sents = self.corp2sent(target)
        target_x = [self.sentence2features (sent) for sent in test_sents]

        pred_y = [tagger.tag(x) for x in target_x]

        result = self.flush(target_x, pred_y)
        result_restored = self.corp2raw(result)
        if os.path.isdir ("Result") == False:
            os.mkdir("Result")
        txt_file_loc = os.path.join("Result", self.AS_result_loc.text())
        result_txt = codecs.open(txt_file_loc, 'w', encoding='utf-8')
        result_txt.write(result_restored)
        result_txt.close()
        os.startfile(txt_file_loc)


    ###Tweet Scrap Module description###
    def Tweetscrap_module(self):
        self.Tweetscrap_window = subwindow ()
        _translate = QtCore.QCoreApplication.translate
        self.Tweetscrap_window.createWindow(545, 310)
        self.Tweetscrap_window.setObjectName ("Twitter Scrapper")
        self.verticalLayout = QtWidgets.QVBoxLayout (self.Tweetscrap_window)
        self.verticalLayout.setObjectName ("verticalLayout")
        self.widget = QtWidgets.QWidget (self.Tweetscrap_window)
        self.widget.setObjectName ("widget")
        self.label_3 = QtWidgets.QLabel (self.widget)
        self.label_3.setGeometry (QtCore.QRect (10, 130, 101, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        self.TwscrapSave = QtWidgets.QPushButton (self.widget)
        self.TwscrapSave.setGeometry (QtCore.QRect (300, 250, 211, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.TwscrapSave.setFont (font)
        self.TwscrapSave.setObjectName ("pushButton_2")
        self.label_5 = QtWidgets.QLabel (self.widget)
        self.label_5.setGeometry (QtCore.QRect (10, 250, 101, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_5.setFont (font)
        self.label_5.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName ("label_5")
        self.TwKeyword = QtWidgets.QLineEdit (self.widget)
        self.TwKeyword.setGeometry (QtCore.QRect (120, 90, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.TwKeyword.setFont (font)
        self.TwKeyword.setClearButtonEnabled (True)
        self.TwKeyword.setObjectName ("TwKeyword")
        self.Twlimit = QtWidgets.QLineEdit (self.widget)
        self.Twlimit.setGeometry (QtCore.QRect (120, 210, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.Twlimit.setFont (font)
        self.Twlimit.setObjectName ("lineEdit")
        self.EndDate = QtWidgets.QDateEdit (self.widget)
        self.EndDate.setGeometry (QtCore.QRect (120, 170, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.EndDate.setFont (font)
        self.EndDate.setDate (QtCore.QDate (2019, 1, 1))
        self.EndDate.setObjectName ("EndDate")
        self.label = QtWidgets.QLabel (self.widget)
        self.label.setGeometry (QtCore.QRect (10, 50, 101, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName ("label")
        self.TwscrapStart = QtWidgets.QPushButton (self.widget)
        self.TwscrapStart.setGeometry (QtCore.QRect (300, 210, 211, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.TwscrapStart.setFont (font)
        self.TwscrapStart.setObjectName ("pushButton")
        self.Twit_Langbox = QtWidgets.QComboBox (self.widget)
        self.Twit_Langbox.setGeometry (QtCore.QRect (120, 50, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.Twit_Langbox.setFont (font)
        self.Twit_Langbox.setObjectName ("comboBox")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Twit_Langbox.addItem ("")
        self.Title_label = QtWidgets.QLabel (self.widget)
        self.Title_label.setGeometry (QtCore.QRect (0, 0, 521, 41))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.Title_label.setFont (font)
        self.Title_label.setAlignment (QtCore.Qt.AlignCenter)
        self.Title_label.setObjectName ("Title_label")
        self.label_4 = QtWidgets.QLabel (self.widget)
        self.label_4.setGeometry (QtCore.QRect (10, 170, 101, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_4.setFont (font)
        self.label_4.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName ("label_4")
        self.startDate = QtWidgets.QDateEdit (self.widget)
        self.startDate.setGeometry (QtCore.QRect (120, 130, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.startDate.setFont (font)
        self.startDate.setDate (QtCore.QDate (2019, 1, 1))
        self.startDate.setObjectName ("startDate")
        self.label_6 = QtWidgets.QLabel (self.widget)
        self.label_6.setGeometry (QtCore.QRect (10, 210, 101, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_6.setFont (font)
        self.label_6.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName ("label_6")
        self.label_2 = QtWidgets.QLabel (self.widget)
        self.label_2.setGeometry (QtCore.QRect (10, 90, 101, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.Twresult_file = QtWidgets.QLineEdit (self.widget)
        self.Twresult_file.setGeometry (QtCore.QRect (120, 250, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.Twresult_file.setFont (font)
        self.Twresult_file.setClearButtonEnabled (True)
        self.Twresult_file.setObjectName ("Twresult_file")
        self.frame = QtWidgets.QFrame (self.widget)
        self.frame.setGeometry (QtCore.QRect (300, 50, 211, 131))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.white_E = QtWidgets.QCheckBox (self.frame)
        self.white_E.setGeometry (QtCore.QRect (10, 10, 201, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.white_E.setFont (font)
        self.white_E.setObjectName ("white_E_2")
        self.URL_E = QtWidgets.QCheckBox (self.frame)
        self.URL_E.setGeometry (QtCore.QRect (10, 40, 171, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.URL_E.setFont (font)
        self.URL_E.setObjectName ("URL_E_2")
        self.TwtID_E = QtWidgets.QCheckBox (self.frame)
        self.TwtID_E.setGeometry (QtCore.QRect (10, 70, 171, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.TwtID_E.setFont (font)
        self.TwtID_E.setObjectName ("TwtID_E_2")
        self.Hash_E = QtWidgets.QCheckBox (self.frame)
        self.Hash_E.setGeometry (QtCore.QRect (10, 100, 171, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.Hash_E.setFont (font)
        self.Hash_E.setObjectName ("Hash_E_2")
        self.verticalLayout.addWidget (self.widget)

        _translate = QtCore.QCoreApplication.translate
        self.Tweetscrap_window.setWindowTitle (_translate ("Twitter Scrapper", "Twitter Scrapper"))
        self.label_3.setText (_translate ("Twitter Scrapper", "Start date:"))
        self.TwscrapSave.setText (_translate ("Twitter Scrapper", "Save"))
        self.label_5.setText (_translate ("Twitter Scrapper", "Result File:"))
        self.TwKeyword.setText (_translate ("Twitter Scrapper", "Input Keyword"))
        self.label.setText (_translate ("Twitter Scrapper", "Language:"))
        self.TwscrapStart.setText (_translate ("Twitter Scrapper", "Start"))
        self.Twit_Langbox.setItemText (0, _translate ("Twitter Scrapper", "Korean"))
        self.Twit_Langbox.setItemText (1, _translate ("Twitter Scrapper", "English"))
        self.Twit_Langbox.setItemText (2, _translate ("Twitter Scrapper", "Arabic"))
        self.Twit_Langbox.setItemText (3, _translate ("Twitter Scrapper", "Bengali"))
        self.Twit_Langbox.setItemText (4, _translate ("Twitter Scrapper", "Czech"))
        self.Twit_Langbox.setItemText (5, _translate ("Twitter Scrapper", "Danish"))
        self.Twit_Langbox.setItemText (6, _translate ("Twitter Scrapper", "German"))
        self.Twit_Langbox.setItemText (7, _translate ("Twitter Scrapper", "Greek"))
        self.Twit_Langbox.setItemText (8, _translate ("Twitter Scrapper", "Spanish"))
        self.Twit_Langbox.setItemText (9, _translate ("Twitter Scrapper", "Persian"))
        self.Twit_Langbox.setItemText (10, _translate ("Twitter Scrapper", "Finnish"))
        self.Twit_Langbox.setItemText (11, _translate ("Twitter Scrapper", "Filipino"))
        self.Twit_Langbox.setItemText (12, _translate ("Twitter Scrapper", "French"))
        self.Twit_Langbox.setItemText (13, _translate ("Twitter Scrapper", "Hebrew"))
        self.Twit_Langbox.setItemText (14, _translate ("Twitter Scrapper", "Hindi"))
        self.Twit_Langbox.setItemText (15, _translate ("Twitter Scrapper", "Hungarian"))
        self.Twit_Langbox.setItemText (16, _translate ("Twitter Scrapper", "Indonesian"))
        self.Twit_Langbox.setItemText (17, _translate ("Twitter Scrapper", "Italian"))
        self.Twit_Langbox.setItemText (18, _translate ("Twitter Scrapper", "Japanese"))
        self.Twit_Langbox.setItemText (19, _translate ("Twitter Scrapper", "Malay"))
        self.Twit_Langbox.setItemText (20, _translate ("Twitter Scrapper", "Dutch"))
        self.Twit_Langbox.setItemText (21, _translate ("Twitter Scrapper", "Norwegian"))
        self.Twit_Langbox.setItemText (22, _translate ("Twitter Scrapper", "Polish"))
        self.Twit_Langbox.setItemText (23, _translate ("Twitter Scrapper", "Portuguese"))
        self.Twit_Langbox.setItemText (24, _translate ("Twitter Scrapper", "Romanian"))
        self.Twit_Langbox.setItemText (25, _translate ("Twitter Scrapper", "Russian"))
        self.Twit_Langbox.setItemText (26, _translate ("Twitter Scrapper", "Swedish"))
        self.Twit_Langbox.setItemText (27, _translate ("Twitter Scrapper", "Thai"))
        self.Twit_Langbox.setItemText (28, _translate ("Twitter Scrapper", "Turkish"))
        self.Twit_Langbox.setItemText (29, _translate ("Twitter Scrapper", "Ukrainian"))
        self.Twit_Langbox.setItemText (30, _translate ("Twitter Scrapper", "Urdu"))
        self.Twit_Langbox.setItemText (31, _translate ("Twitter Scrapper", "Vietnamese"))
        self.Twit_Langbox.setItemText (32, _translate ("Twitter Scrapper", "Chinese(Simplified)"))
        self.Twit_Langbox.setItemText (33, _translate ("Twitter Scrapper", "Chinese(Traditional)"))
        self.Title_label.setText (_translate ("Twitter Scrapper", "Twitter Scrapper"))
        self.label_4.setText (_translate ("Twitter Scrapper", "End date:"))
        self.label_6.setText (_translate ("Twitter Scrapper", "Limit:"))
        self.label_2.setText (_translate ("Twitter Scrapper", "Keyword:"))
        self.Twresult_file.setText (_translate ("Twitter Scrapper", ".csv(korean) or .txt"))
        self.white_E.setText (_translate ("Twitter Scrapper", "White Space Elimination"))
        self.URL_E.setText (_translate ("Twitter Scrapper", "URL Elimination"))
        self.TwtID_E.setText (_translate ("Twitter Scrapper", "Twitter ID Elimination"))
        self.Hash_E.setText (_translate ("Twitter Scrapper", "Hash-Tag Elimination"))

        self.TwscrapStart.released.connect(self.Process)
        self.TwscrapStart.released.connect (self.Twitter_moudule_start)
        self.TwscrapSave.released.connect (self.Twitter_moudule_save)

        self.Tweetscrap_window.show ()

    def Twitter_moudule_start(self):
        tempScrap = open ('Temp.txt', 'w', encoding='utf-8')
        tempScrap.close ()
        language = self.Twit_Langbox.currentText()
        query = self.TwKeyword.text()
        lang_dic = {'English': 'en', 'Arabic': 'ar', 'Bengali': 'bn', 'Czech': 'cs', 'Danish': 'da', 'German': 'de',
                    'Greek': 'el', 'Spanish': 'es', 'Persian': 'fa', 'Finnish': 'fi', 'Filipino': 'fil', 'French': 'fr',
                    'Hebrew': 'he', 'Hindi': 'hi', 'Hungarian': 'hu', 'Indonesian': 'id', 'Italian': 'it',
                    'Japanese': 'ja', 'Korean': 'ko', 'Malay': 'msa', 'Dutch': 'nl', 'Norwegian': 'no', 'Polish': 'pl',
                    'Portuguese': 'pt', 'Romanian': 'ro', 'Russian': 'ru', 'Swedish': 'sv', 'Thai': 'th',
                    'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Vietnamese': 'vi',
                    'Chinese(Simplified)': 'zh-cn', 'Chinese(Traditional)': 'zh-tw'}

        c = twint.Config()
        c.Search = query
        c.lang = str(lang_dic[language])
        c.Output = 'Temp.txt'
        c.Limit = int(self.Twlimit.text())

        # 시작일 인풋을 받아서 Until로 계속 돌려줘야 함
        sinceDate = self.startDate.date().toString("yyyy-MM-dd")
        untilDate = sinceDate
        endDateinput = self.EndDate.date().toString("yyyy-MM-dd")
        endDate_fin = str(datetime.datetime.strftime(parse(endDateinput) + datetime.timedelta(days=1), "%Y-%m-%d"))

        # 초기값 설정
        while True:
            if untilDate != endDate_fin:
                c.Until = untilDate
                c.Format = "{date} |TAB| {time} |TAB| {tweet}"
                twint.run.Search (c)
                untilDate = str (datetime.datetime.strftime (parse (untilDate) + datetime.timedelta (days=1), "%Y-%m-%d"))
            else:
                print('Scrapping Done..')
                break
        time.sleep (3)
        self.Process_window.close ()

    def Twitter_moudule_save(self):
        tempScraptxt = list (open('Temp.txt', 'r', encoding='utf-8'))
        print ('Open Temp file..')

        Tweet_date = []
        Tweet_time = []
        Tweets = []

        print ('Data Frame Function Initiating..')
        for i in tempScraptxt:
            Tweet_date.append (i.split (" |TAB| ")[0])
            Tweet_time.append (i.split (" |TAB| ")[1])
            Tweets.append (i.split (" |TAB| ")[2])

        print ('Save function Initiating..')

        if os.path.isdir ("TweetScrap_Output") == False:
            os.mkdir ("TweetScrap_Output")
        print ('Directory Check..')
        result_tweets = []
        for content in Tweets:
            if self.white_E.isChecked() == True:
                content = re.sub (r"\s+", ' ', content)
                content = re.sub (r'\n+', '\n', content)
            if self.URL_E.isChecked() == True:
                content = re.sub (r"(http|ftp|https)://(?:[-\w.]|(?:%[\da-zA-Z/]{2}))+", "", content)
                content = re.sub (r"(pic.)(?:[-\w.]|(?:%[\da-zA-Z]{2}))+", "", content)
            if self.TwtID_E.isChecked() == True:
                content = re.sub (r'@[\\S0-9]+', "", content)
            if self.Hash_E.isChecked() == True:
                content = re.sub (r'#[\\S0-9]+', "", content)
            result_tweets.append (content)
        print ('Preprocessing Done..')

        if self.Twit_Langbox.currentText() == "Korean":
            scrap_result = pandas.DataFrame (
                {'Tweet Date': Tweet_date, 'Tweet Time': Tweet_time, 'Tweet Text': result_tweets},
                columns=["Tweet Date", "Tweet Time", "Tweet Text"])
            if os.path.isdir ("Result") == False:
                os.mkdir ("Result")
            twitter_csv_loc = os.path.join ("Result", self.Twresult_file.text())
            scrap_result.to_csv (twitter_csv_loc, sep=",", encoding="utf-8-sig")
        else:
            scrap_result = pandas.DataFrame (
                {'Tweet Date': Tweet_date, 'Tweet Time': Tweet_time, 'Tweet Text': result_tweets},
                columns=["Tweet Date", "Tweet Time", "Tweet Text"])
            if os.path.isdir ("Result") == False:
                os.mkdir ("Result")
            twitter_csv_loc = os.path.join ("Result", self.Twresult_file.text())
            scrap_result.to_csv (twitter_csv_loc, sep=",", encoding="utf-8-sig")
        print ('Save Done..')
        os.startfile (twitter_csv_loc)


    ### ToSAC-Annotator Module description###
    def ToSAC_Annotator_module(self):
        self.ToSAC_window = subwindow ()
        self.ToSAC_window.createWindow (570, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout (self.ToSAC_window)
        self.horizontalLayout.setObjectName ("horizontalLayout")
        self.widget = QtWidgets.QWidget (self.ToSAC_window)
        self.widget.setObjectName ("widget")
        self.label = QtWidgets.QLabel (self.widget)
        self.label.setGeometry (QtCore.QRect (0, 0, 551, 41))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignCenter)
        self.label.setObjectName ("label")
        self.frame = QtWidgets.QFrame (self.widget)
        self.frame.setGeometry (QtCore.QRect (10, 40, 531, 151))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.label_1 = QtWidgets.QLabel (self.frame)
        self.label_1.setGeometry (QtCore.QRect (-20, 10, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_1.setFont (font)
        self.label_1.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_1.setObjectName ("label_1")
        self.ToSAC_Langbox = QtWidgets.QComboBox (self.frame)
        self.ToSAC_Langbox.setGeometry (QtCore.QRect (140, 10, 141, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.ToSAC_Langbox.setFont (font)
        self.ToSAC_Langbox.setObjectName ("ToSAC_Langbox")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Langbox.addItem ("")
        self.ToSAC_Target = QtWidgets.QLineEdit (self.frame)
        self.ToSAC_Target.setGeometry (QtCore.QRect (140, 60, 231, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.ToSAC_Target.setFont (font)
        self.ToSAC_Target.setClearButtonEnabled (True)
        self.ToSAC_Target.setObjectName ("ToSAC_Target")
        self.ToSAC_Target_browse = QtWidgets.QPushButton (self.frame)
        self.ToSAC_Target_browse.setGeometry (QtCore.QRect (380, 60, 121, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.ToSAC_Target_browse.setFont (font)
        self.ToSAC_Target_browse.setObjectName ("ToSAC_Target_browse")
        self.label_3 = QtWidgets.QLabel (self.frame)
        self.label_3.setGeometry (QtCore.QRect (-20, 110, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        self.ToSAC_Tags_browse = QtWidgets.QPushButton (self.frame)
        self.ToSAC_Tags_browse.setGeometry (QtCore.QRect (380, 110, 121, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.ToSAC_Tags_browse.setFont (font)
        self.ToSAC_Tags_browse.setObjectName ("ToSAC_Tags_browse")
        self.Stemming_Check = QtWidgets.QCheckBox (self.frame)
        self.Stemming_Check.setGeometry (QtCore.QRect (290, 10, 341, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        self.Stemming_Check.setFont (font)
        self.Stemming_Check.setChecked (True)
        self.Stemming_Check.setObjectName ("checkBox")
        self.ToSAC_Tags = QtWidgets.QLineEdit (self.frame)
        self.ToSAC_Tags.setGeometry (QtCore.QRect (140, 110, 231, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.ToSAC_Tags.setFont (font)
        self.ToSAC_Tags.setClearButtonEnabled (True)
        self.ToSAC_Tags.setObjectName ("ToSAC_Tags")
        self.label_2 = QtWidgets.QLabel (self.frame)
        self.label_2.setGeometry (QtCore.QRect (-20, 60, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.frame_2 = QtWidgets.QFrame (self.widget)
        self.frame_2.setGeometry (QtCore.QRect (10, 200, 531, 71))
        self.frame_2.setFrameShape (QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName ("frame_2")
        self.ToSAC_SaveFile = QtWidgets.QLineEdit (self.frame_2)
        self.ToSAC_SaveFile.setGeometry (QtCore.QRect (140, 20, 231, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.ToSAC_SaveFile.setFont (font)
        self.ToSAC_SaveFile.setClearButtonEnabled (True)
        self.ToSAC_SaveFile.setObjectName ("ToSAC_SaveFile")
        self.label_4 = QtWidgets.QLabel (self.frame_2)
        self.label_4.setGeometry (QtCore.QRect (-20, 20, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        self.label_4.setFont (font)
        self.label_4.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName ("label_4")
        self.export_button = QtWidgets.QPushButton (self.frame_2)
        self.export_button.setGeometry (QtCore.QRect (380, 20, 121, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (False)
        font.setWeight (50)
        self.export_button.setFont (font)
        self.export_button.setObjectName ("export_button")
        self.horizontalLayout.addWidget (self.widget)
        _translate = QtCore.QCoreApplication.translate
        self.ToSAC_window.setWindowTitle (_translate ("Form", "ToSAC Annotator"))
        self.label.setText (_translate ("Form", "ToSAC-Annotator"))
        self.label_1.setText (_translate ("Form", "Language:"))
        self.ToSAC_Langbox.setItemText (0, _translate ("Form", "Korean"))
        self.ToSAC_Langbox.setItemText (1, _translate ("Form", "Japanese"))
        self.ToSAC_Langbox.setItemText (2, _translate ("Form", "Chinese"))
        self.ToSAC_Langbox.setItemText (3, _translate ("Form", "English"))
        self.ToSAC_Langbox.setItemText (4, _translate ("Form", "Danish"))
        self.ToSAC_Langbox.setItemText (5, _translate ("Form", "Dutch"))
        self.ToSAC_Langbox.setItemText (6, _translate ("Form", "Finnish"))
        self.ToSAC_Langbox.setItemText (7, _translate ("Form", "French"))
        self.ToSAC_Langbox.setItemText (8, _translate ("Form", "German"))
        self.ToSAC_Langbox.setItemText (9, _translate ("Form", "Hungarian"))
        self.ToSAC_Langbox.setItemText (10, _translate ("Form", "Italian"))
        self.ToSAC_Langbox.setItemText (11, _translate ("Form", "Norwegian"))
        self.ToSAC_Langbox.setItemText (12, _translate ("Form", "Portuguese"))
        self.ToSAC_Langbox.setItemText (13, _translate ("Form", "Romanian"))
        self.ToSAC_Langbox.setItemText (14, _translate ("Form", "Russian"))
        self.ToSAC_Langbox.setItemText (15, _translate ("Form", "Spanish"))
        self.ToSAC_Langbox.setItemText (16, _translate ("Form", "Swedish"))
        self.ToSAC_Langbox.setItemText (17, _translate ("Form", "Turkish"))
        self.ToSAC_Target.setText (_translate ("Form", "No file seleted"))
        self.ToSAC_Target_browse.setText (_translate ("Form", "Browse.."))
        self.label_3.setText (_translate ("Form", "Tag Data:"))
        self.ToSAC_Tags_browse.setText (_translate ("Form", "Browse.."))
        self.Stemming_Check.setText (_translate ("Form", "Applied Stemmer/Tokenizer"))
        self.ToSAC_Tags.setText (_translate ("Form", "No file seleted"))
        self.label_2.setText (_translate ("Form", "Target Text:"))
        self.ToSAC_SaveFile.setText (_translate ("Form", ".txt format"))
        self.label_4.setText (_translate ("Form", "Result File:"))
        self.export_button.setText (_translate ("Form", "Apply / Save"))

        self.export_button.released.connect (self.ToSAC_Annotation_Start)
        self.ToSAC_Target_browse.released.connect (self.ToSAC_Target_open)
        self.ToSAC_Tags_browse.released.connect (self.ToSAC_Tags_open)
        self.ToSAC_window.show()

    def ToSAC_Target_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.ToSAC_Target.setText((str(fname)).split("', '")[0][2:])

    def ToSAC_Tags_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.ToSAC_Tags.setText((str(fname)).split("', '")[0][2:])

    def ToSAC_Annotation_Save(self, text, tags):
            annotation_csv_loc = tags
            annotation_data = [i.strip().split ('\t') for i in open(annotation_csv_loc, 'r', encoding='utf-8').read().split ('\n')]
            if annotation_data[-1] == ['']:
                annotation_data.remove (annotation_data[-1])
            for x, y in annotation_data:
                reg_temp = "\\b(" + x + ")\\b"
                text = re.sub (reg_temp, x + '/' + y, text)
            annotated_text_list = text.replace ('.', '.\n').replace('\n\n','\n').split('\n')
            if os.path.isdir ("Result") == False:
                os.mkdir ("Result")
            result_loc = os.path.join("Result", self.ToSAC_SaveFile.text())
            result = open (result_loc, 'w', encoding='utf-8')
            for i in annotated_text_list:
                result.write (str (i).strip () + '\n')
            result.close()
            return os.startfile(result_loc)

    def ToSAC_Annotation_Start(self):
        if self.ToSAC_Langbox.currentText().lower() == "korean":
            if self.Stemming_Check.isChecked() == True:
                tagger = Kiwi ()
                tagger.prepare ()
                target_corpus = open(self.ToSAC_Target.text(), 'r', encoding='utf-8').read().split('\n')
                # 키위 형태소 태거 활용하여 리스트 내의 어절들을 어휘/태그 형태로 치환, tagged_text에 스트링 형태로 저장
                tagged_text = ''
                for i in target_corpus:
                    temp_tagging = [x[0] for x in tagger.analyze (i, top_n=1)]
                    inner_temp = ["{}/{}".format (word, tag) for word, tag, score1, score2 in temp_tagging[0]]
                    for j in inner_temp:
                        tagged_text += j + ' '
                # 전체 문장에 대한 Lemmatizing
                temp = tagged_text
                temp = re.sub (r"([가-힣]+)/[A-Z]+( 게)(/EC)", '\\1게', temp)  # 부사형 붙여주기
                temp = re.sub (r"([ᆫᆯᆷ가-힣]+)/[EJIXU][A-Z]+", '', temp)  # 어미, 조사, 감탄사 생략
                temp = re.sub (r"([가-힣]+)/[MN][A-Z]+", '\\1', temp)  # 관형사 및 일반 부사, 명사 태그 생략
                temp = re.sub (r"([가-힣]+)/V[A-Z]+", '\\1다', temp)  # 동사 및 형용사 태그 생략 및 레마화
                temp = re.sub (r"/S[A-Z]+", '', temp)  # 구두점 태그 생략
                temp = re.sub (r"(\s)+", ' ', temp)  # 띄어쓰기 중복 제거
                temp = re.sub (r'\s([\\.\'\"])', '\\1', temp)
                lemma_text = temp
            else:
                lemma_text = open(self.ToSAC_Target.text(), 'r', encoding='utf-8').read()

            self.ToSAC_Annotation_Save(lemma_text, self.ToSAC_Tags.text())

        elif self.ToSAC_Langbox.currentText().lower() == "japanese":
            if self.Stemming_Check.isChecked() == True:
                japan_target_corpus = open(self.ToSAC_Target.text(), 'r', encoding='utf-8').read().split('\n')
                japan_text = ""
                for i in japan_target_corpus:
                    japan_temp = ""
                    japan_tokens = tagging (i)
                    for i in japan_tokens.words:
                        japan_temp += i + " "
                    japan_text += japan_temp.strip() + "\n"
            else:
                japan_text = open(self.ToSAC_Target.text (), 'r', encoding='utf-8').read()

            self.ToSAC_Annotation_Save (japan_text, self.ToSAC_Tags.text())

        elif self.ToSAC_Langbox.currentText().lower() == "chinese":
            if self.Stemming_Check.isChecked () == True:
                chinese_text = ""
                china_target_corpus = open (self.ToSAC_Target.text (), 'r', encoding='utf-8').read ().split('\n')
                for i in china_target_corpus:
                    chinese_tokens = jieba.cut(i, cut_all=True)
                    chinese_text += " ".join(chinese_tokens).strip() + '\n'
            else:
                chinese_text = open (self.ToSAC_Target.text (), 'r', encoding='utf-8').read()

            self.ToSAC_Annotation_Save (chinese_text, self.ToSAC_Tags.text ())

        else:
            if self.Stemming_Check.isChecked () == True:
                multilangStemmer = Stemmer.Stemmer(self.ToSAC_Langbox.currentText().lower())
                multilang_target_corpus = open(self.ToSAC_Target.text(), 'r', encoding='utf-8').read().split('\n')
                multilang_text = ""
                for i in multilang_target_corpus:
                    multilang_temp = ""
                    for j in i.split(' '):
                        stemming_word = multilangStemmer.stemWord(j)
                        multilang_temp += stemming_word + ' '
                    multilang_text += multilang_temp.strip() + '\n'
            else:
                multilang_text = open(self.ToSAC_Target.text(), 'r', encoding='utf-8').read()

            self.ToSAC_Annotation_Save(multilang_text, self.ToSAC_Tags.text())

    ### Word2Vec Module description###
    def Word2Vec_module(self):
        self.Word2vec_window = subwindow ()
        self.Word2vec_window.createWindow (590, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout (self.Word2vec_window)
        self.horizontalLayout.setObjectName ("horizontalLayout")
        self.widget = QtWidgets.QWidget (self.Word2vec_window)
        self.widget.setObjectName ("widget")
        self.label_3 = QtWidgets.QLabel (self.widget)
        self.label_3.setGeometry (QtCore.QRect (0, 0, 571, 41))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignCenter)
        self.label_3.setObjectName ("label_3")
        self.Wv_Expanding_button = QtWidgets.QPushButton (self.widget)
        self.Wv_Expanding_button.setGeometry (QtCore.QRect (440, 51, 111, 221))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        font.setBold (True)
        font.setWeight (75)
        self.Wv_Expanding_button.setFont (font)
        self.Wv_Expanding_button.setObjectName ("Wv_Training_button")
        self.frame = QtWidgets.QFrame (self.widget)
        self.frame.setGeometry (QtCore.QRect (0, 50, 431, 221))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.Wv_Training_button = QtWidgets.QPushButton (self.frame)
        self.Wv_Training_button.setGeometry (QtCore.QRect (330, 70, 91, 141))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        self.Wv_Training_button.setFont (font)
        self.Wv_Training_button.setObjectName ("Wv_Expanding_button")
        self.Wv_Training_Text = QtWidgets.QLineEdit (self.frame)
        self.Wv_Training_Text.setGeometry (QtCore.QRect (10, 30, 301, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.Wv_Training_Text.setFont (font)
        self.Wv_Training_Text.setClearButtonEnabled (True)
        self.Wv_Training_Text.setObjectName ("Wv_Training_Text")
        self.label_2 = QtWidgets.QLabel (self.frame)
        self.label_2.setGeometry (QtCore.QRect (10, 70, 261, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_2.setFont (font)
        self.label_2.setObjectName ("label_2")
        self.Wv_Target_Word = QtWidgets.QLineEdit (self.frame)
        self.Wv_Target_Word.setGeometry (QtCore.QRect (10, 101, 301, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (9)
        self.Wv_Target_Word.setFont (font)
        self.Wv_Target_Word.setClearButtonEnabled (True)
        self.Wv_Target_Word.setObjectName ("Wv_Target_Word")
        self.Wv_topn_index = QtWidgets.QLineEdit (self.frame)
        self.Wv_topn_index.setGeometry (QtCore.QRect (260, 180, 51, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        font.setPointSize (10)
        self.Wv_topn_index.setFont (font)
        self.Wv_topn_index.setAlignment (QtCore.Qt.AlignCenter)
        self.Wv_topn_index.setObjectName ("Wv_topn_index")
        self.Wv_Training_browse = QtWidgets.QPushButton (self.frame)
        self.Wv_Training_browse.setGeometry (QtCore.QRect (330, 30, 91, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        self.Wv_Training_browse.setFont (font)
        self.Wv_Training_browse.setObjectName ("Wv_Training_browse")
        self.label = QtWidgets.QLabel (self.frame)
        self.label.setGeometry (QtCore.QRect (10, 0, 311, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label.setFont (font)
        self.label.setObjectName ("label")
        self.label_4 = QtWidgets.QLabel (self.frame)
        self.label_4.setGeometry (QtCore.QRect (10, 140, 381, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_4.setFont (font)
        self.label_4.setObjectName ("label_4")
        self.Wv_topn_slide = QtWidgets.QSlider (self.frame)
        self.Wv_topn_slide.setGeometry (QtCore.QRect (10, 182, 241, 31))
        self.Wv_topn_slide.setOrientation (QtCore.Qt.Horizontal)
        self.Wv_topn_slide.setObjectName ("Wv_topn_slide")
        self.horizontalLayout.addWidget (self.widget)
        _translate = QtCore.QCoreApplication.translate
        self.Word2vec_window.setWindowTitle (_translate ("Form", "Expanding Lexica via Word2Vec"))
        self.label_3.setText (_translate ("Form", "Expanding Lexica via Word2Vec"))
        self.Wv_Expanding_button.setText (_translate ("Form", "Expanding"))
        self.Wv_Training_button.setText (_translate ("Form", "Training"))
        self.Wv_Training_Text.setText (_translate ("Form", "No file selected"))
        self.label_2.setText (_translate ("Form", "Target Word:"))
        self.Wv_Target_Word.setText (_translate ("Form", "Input Keyword"))
        self.Wv_topn_index.setText (_translate ("Form", "0"))
        self.Wv_Training_browse.setText (_translate ("Form", "Browse.."))
        self.label.setText (_translate ("Form", "Training Text:"))
        self.label_4.setText (_translate ("Form", "The Number of Words Expansion:"))

        self.Wv_topn_slide.valueChanged.connect (self.showHorizontalSliderValue)
        self.Wv_topn_index.textChanged.connect (self.InputHorizontalSliderValue)
        self.Wv_Training_browse.released.connect (self.Wv_Traintext_open)
        self.Wv_Expanding_button.released.connect (self.Word2Vec_Save)
        self.Wv_Training_button.released.connect (self.Word2Vec_Start)

        self.Word2vec_window.show ()

    def showHorizontalSliderValue(self):
        self.Wv_topn_index.setText(str(self.Wv_topn_slide.value()))
    def InputHorizontalSliderValue(self):
        self.Wv_topn_slide.setValue(int(self.Wv_topn_index.text()))
    def Wv_Traintext_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.Wv_Training_Text.setText((str(fname)).split("', '")[0][2:])
    def Word2Vec_Start(self):
        global Wvmodel
        corpus_raw = codecs.open (self.Wv_Training_Text.text(), 'r', encoding='utf-8')
        search_query = self.Wv_Target_Word.text()
        search_regex = "\\b(" + search_query + ")"
        corpus = re.sub (search_regex + r'[가-힣]*', search_query, corpus_raw.read ())
        corpus = re.sub (r'[\"\']*' + search_query + r'[?!\"\'.,\s]*', search_query + ' ', corpus)
        qnorm_corpus = corpus.split('\n')
        tagged_temp = []

        for i in qnorm_corpus:
            if i != '':
                tagged_temp.append (i.split (' '))

        config = {
            'min_count': 5,  # frequency min count
            'size': 200,  # vertor space count
            'sg': 1,  # Skip-gram
            'iter': 20,  # training epochs
            'workers': multiprocessing.cpu_count(),
        }
        Wvmodel = gensim.models.Word2Vec (**config)
        Wvmodel.build_vocab (tagged_temp)
        Wvmodel.train (tagged_temp, epochs=Wvmodel.epochs, total_examples=Wvmodel.corpus_count)

    def Word2Vec_Save(self):
        Words = []
        Vectors = []
        for i in Wvmodel.wv.most_similar(self.Wv_Target_Word.text(), topn=int(self.Wv_topn_index.text())):
            Words.append(list(i)[0])
            Vectors.append(str(list(i)[1]))
        result = pandas.DataFrame({'Words': Words, 'Vectors': Vectors}, columns=["Words", 'Vectors'])
        if os.path.isdir("Result") == False:
            os.mkdir("Result")
        file_loc = os.path.join ("Result", "Word2Vec_Result.txt")
        result.to_csv (file_loc, sep="\t", encoding="utf-8")
        return os.startfile(file_loc)

    ### SESACbasedSSA Module description###
    def SESACbasedSSA_module(self):
        self.SESACSSA_window = subwindow ()
        self.SESACSSA_window.createWindow (825, 310)
        self.horizontalLayout = QtWidgets.QHBoxLayout (self.SESACSSA_window)
        self.horizontalLayout.setObjectName ("horizontalLayout")
        self.widget = QtWidgets.QWidget (self.SESACSSA_window)
        self.widget.setObjectName ("widget")
        self.label_3 = QtWidgets.QLabel (self.widget)
        self.label_3.setGeometry (QtCore.QRect (0, 0, 801, 40))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignCenter)
        self.label_3.setObjectName ("label_3")
        self.frame = QtWidgets.QFrame (self.widget)
        self.frame.setGeometry (QtCore.QRect (0, 40, 801, 171))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.SSSA_Training_Text = QtWidgets.QLineEdit (self.frame)
        self.SSSA_Training_Text.setGeometry (QtCore.QRect (160, 50, 181, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSSA_Training_Text.setFont (font)
        self.SSSA_Training_Text.setClearButtonEnabled (True)
        self.SSSA_Training_Text.setObjectName ("SSSA_Training_Text")
        self.SSSA_Tr_Browse = QtWidgets.QPushButton (self.frame)
        self.SSSA_Tr_Browse.setGeometry (QtCore.QRect (360, 50, 81, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        self.SSSA_Tr_Browse.setFont (font)
        self.SSSA_Tr_Browse.setObjectName ("SSSA_Tr_Browse")
        self.label_4 = QtWidgets.QLabel (self.frame)
        self.label_4.setGeometry (QtCore.QRect (20, 90, 131, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_4.setFont (font)
        self.label_4.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName ("label_4")
        self.SSSA_Valid_text = QtWidgets.QTextBrowser (self.frame)
        self.SSSA_Valid_text.setGeometry (QtCore.QRect (450, 41, 331, 111))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSSA_Valid_text.setFont (font)
        self.SSSA_Valid_text.setObjectName ("SSSA_Valid_text")
        self.SSSA_Tr_Model = QtWidgets.QComboBox (self.frame)
        self.SSSA_Tr_Model.setGeometry (QtCore.QRect (160, 10, 181, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSSA_Tr_Model.setFont (font)
        self.SSSA_Tr_Model.setObjectName ("SSSA_Tr_Model")
        self.SSSA_Tr_Model.addItem ("")
        self.SSSA_Tr_Model.addItem ("")
        self.SSSA_Tr_Model.addItem ("")
        self.SSSA_Tr_Model.addItem ("")
        self.SSSA_Tr_Model.addItem ("")
        self.label_2 = QtWidgets.QLabel (self.frame)
        self.label_2.setGeometry (QtCore.QRect (10, 50, 141, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.SSSA_Ta_Browse = QtWidgets.QPushButton (self.frame)
        self.SSSA_Ta_Browse.setGeometry (QtCore.QRect (360, 90, 81, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        self.SSSA_Ta_Browse.setFont (font)
        self.SSSA_Ta_Browse.setObjectName ("SSSA_Ta_Browse")
        self.label = QtWidgets.QLabel (self.frame)
        self.label.setGeometry (QtCore.QRect (0, 10, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label.setObjectName ("label")
        self.SSSA_Valid_Type = QtWidgets.QComboBox (self.frame)
        self.SSSA_Valid_Type.setGeometry (QtCore.QRect (590, 10, 191, 22))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSSA_Valid_Type.setFont (font)
        self.SSSA_Valid_Type.setObjectName ("SSSA_Valid_Type")
        self.SSSA_Valid_Type.addItem ("")
        self.SSSA_Valid_Type.addItem ("")
        self.label_5 = QtWidgets.QLabel (self.frame)
        self.label_5.setGeometry (QtCore.QRect (440, 10, 141, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (True)
        font.setWeight (75)
        self.label_5.setFont (font)
        self.label_5.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName ("label_5")
        self.SSSA_Target_Text = QtWidgets.QLineEdit (self.frame)
        self.SSSA_Target_Text.setGeometry (QtCore.QRect (160, 90, 181, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSSA_Target_Text.setFont (font)
        self.SSSA_Target_Text.setClearButtonEnabled (True)
        self.SSSA_Target_Text.setObjectName ("SSSA_Target_Text")
        self.SSSA_Tr_butt = QtWidgets.QPushButton (self.frame)
        self.SSSA_Tr_butt.setGeometry (QtCore.QRect (200, 130, 241, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        self.SSSA_Tr_butt.setFont (font)
        self.SSSA_Tr_butt.setObjectName ("SSSA_Tr_butt")
        self.label_7 = QtWidgets.QLabel (self.frame)
        self.label_7.setGeometry (QtCore.QRect (20, 130, 131, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_7.setFont (font)
        self.label_7.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName ("label_7")
        self.SSSA_Vector_Weight = QtWidgets.QLineEdit (self.frame)
        self.SSSA_Vector_Weight.setGeometry (QtCore.QRect (160, 130, 31, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSSA_Vector_Weight.setFont (font)
        self.SSSA_Vector_Weight.setClearButtonEnabled (False)
        self.SSSA_Vector_Weight.setObjectName ("SSSA_Vector_Weight")
        self.frame_2 = QtWidgets.QFrame (self.widget)
        self.frame_2.setGeometry (QtCore.QRect (0, 220, 461, 51))
        self.frame_2.setFrameShape (QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName ("frame_2")
        self.SSSA_Export_butt = QtWidgets.QPushButton (self.frame_2)
        self.SSSA_Export_butt.setGeometry (QtCore.QRect (360, 10, 71, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (10)
        self.SSSA_Export_butt.setFont (font)
        self.SSSA_Export_butt.setObjectName ("SSSA_Export_butt")
        self.label_6 = QtWidgets.QLabel (self.frame_2)
        self.label_6.setGeometry (QtCore.QRect (0, 10, 151, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (12)
        font.setBold (False)
        font.setWeight (50)
        self.label_6.setFont (font)
        self.label_6.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName ("label_6")
        self.SSSA_result_loc = QtWidgets.QLineEdit (self.frame_2)
        self.SSSA_result_loc.setGeometry (QtCore.QRect (160, 9, 181, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSSA_result_loc.setFont (font)
        self.SSSA_result_loc.setClearButtonEnabled (True)
        self.SSSA_result_loc.setObjectName ("SSSA_result_loc")
        self.horizontalLayout.addWidget (self.widget)
        _translate = QtCore.QCoreApplication.translate
        self.SESACSSA_window.setWindowTitle (_translate ("Form", "SESACbasedSSA"))
        self.label_3.setText (_translate ("Form", "SESAC based SSA"))
        self.SSSA_Training_Text.setText (_translate ("Form", "No file selected"))
        self.SSSA_Tr_Browse.setText (_translate ("Form", "Browse.."))
        self.label_4.setText (_translate ("Form", "Target Text:"))
        self.SSSA_Tr_Model.setItemText (0, _translate ("Form", "Multinomial Naive Bayes"))
        self.SSSA_Tr_Model.setItemText (1, _translate ("Form", "Bernoulli Naive Bayes"))
        self.SSSA_Tr_Model.setItemText (2, _translate ("Form", "Logistic Regression"))
        self.SSSA_Tr_Model.setItemText (3, _translate ("Form", "SGD Classifier"))
        self.SSSA_Tr_Model.setItemText (4, _translate ("Form", "Linear SVC"))
        self.label_2.setText (_translate ("Form", "Training Text:"))
        self.SSSA_Ta_Browse.setText (_translate ("Form", "Browse.."))
        self.label.setText (_translate ("Form", "Training Model:"))
        self.SSSA_Valid_Type.setItemText (0, _translate ("Form", "Default"))
        self.SSSA_Valid_Type.setItemText (1, _translate ("Form", "5-Fold Cross"))
        self.label_5.setText (_translate ("Form", "Validation Type:"))
        self.SSSA_Target_Text.setText (_translate ("Form", "No file selected"))
        self.SSSA_Tr_butt.setText (_translate ("Form", "Training / Predicition"))
        self.label_7.setText (_translate ("Form", "Vector Weight:"))
        self.SSSA_Vector_Weight.setText (_translate ("Form", "2"))
        self.SSSA_Export_butt.setText (_translate ("Form", "Save"))
        self.label_6.setText (_translate ("Form", "Result File:"))
        self.SSSA_result_loc.setText (_translate ("Form", ".csv format"))

        self.SSSA_Tr_Browse.released.connect (self.SSSA_Train_open)
        self.SSSA_Ta_Browse.released.connect (self.SSSA_Target_open)
        self.SSSA_Tr_butt.released.connect(self.Process)
        self.SSSA_Tr_butt.released.connect(self.SESACbasedSSA_Training)
        self.SSSA_Export_butt.released.connect(self.SESACbasedSSA_export)
        self.SESACSSA_window.show ()

    def SSSA_Train_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.SSSA_Training_Text.setText((str(fname)).split("', '")[0][2:])

    def SSSA_Target_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.SSSA_Target_Text.setText((str(fname)).split("', '")[0][2:])

    def SESACbasedSSA_Training (self):
        global pred_data, prediction
        try:
            def NullrowExec_train(location):
                temp_raw = pandas.read_table (location, encoding='utf-8')
                temp_raw['text'] = temp_raw['text'].str.replace (r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
                temp_raw = temp_raw.dropna (how='any')
                new_df = pandas.DataFrame ({'text': temp_raw['text'], 'label': temp_raw['label']},
                                           columns=('text', 'label'),
                                           index=None)
                new_loc = location.replace ('.txt', '_SSA.txt')
                new_df.to_csv (new_loc, sep='\t', encoding='utf-8', index=None)
                loc = codecs.open (new_loc, 'r', encoding='utf-8')
                return loc
            def NullrowExec_test(location):
                temp_raw = pandas.read_table (location, encoding='utf-8')
                temp_raw['text'] = temp_raw['text'].str.replace (r"[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
                temp_raw = temp_raw.dropna (how='any')
                new_df = pandas.DataFrame ({'text': temp_raw['text']})
                new_loc = location.replace ('.txt', '_SSA_Test.txt')
                new_df.to_csv (new_loc, sep='\t', encoding='utf-8', index=None)
                loc = codecs.open (new_loc, 'r', encoding='utf-8')
                return loc
            ##학습 데이터 인풋, 예측 대상 데이터 인풋
            train_loc = self.SSSA_Training_Text.text()
            pred_loc = self.SSSA_Target_Text.text()
            train_df = NullrowExec_train(train_loc)
            pred_df = NullrowExec_test(pred_loc)

            ##한국어 스테밍 모듈(list to list)
            tagger = Kiwi ()
            tagger.prepare ()

            # 불용어 리스트

            stop_set = codecs.open(Stop_words, encoding='utf-8').read ().split ('\r\n')

            def Steming(sentences):
                Stem_sentences = []
                for sentence in sentences:
                    temp = ""
                    temp_tagging = [x[0] for x in tagger.analyze (sentence, top_n=1)]
                    inner_temp = ["{}/{}".format (word, tag) for word, tag, score1, score2 in temp_tagging[0]]
                    for j in inner_temp:
                        temp += j + ' '

                    temp = re.sub (r"([가-힣]+)/[A-Z]+( 게)(/EC)", '\\1게', temp.strip ())  # 부사형 붙여주기
                    temp = re.sub (r"([ᆫᆯᆷᆸㄱ-ㅎㅏ-ㅣ가-힣]*)/[EJIXU][A-Z]+", '', temp)  # 어미, 조사, 감탄사 생략
                    temp = re.sub (r"([가-힣ㄱ-ㅎㅏ-ㅣ]*)/[MN][A-Z]+", '\\1', temp)  # 관형사 및 일반 부사, 명사 태그 생략
                    temp = re.sub (r"([가-힣]+)/V[A-Z]+", '\\1다', temp)  # 동사 및 형용사 태그 생략 및 레마화
                    temp = re.sub (r"/[S|U][A-Z]+", '', temp)  # 구두점 태그 생략
                    temp = re.sub (r"[ㄱ-ㅎㅏ-ㅣ]+", '', temp)
                    temp = re.sub (r"\\b(\\/[A-Za-z])\\b", '', temp)
                    temp = re.sub (r'\s([\\.\'\"])', '\\1', temp)
                    for i in stop_set:
                        temp = re.sub ("\\b(" + i + ")\\b", "", temp)
                    temp = re.sub (r"( )+", ' ', temp)  # 띄어쓰기 중복 제거
                    Stem_sentences.append (temp.strip ())

                return Stem_sentences

            org_feat = []
            org_label = []
            org_data = []
            pred_data = []
            train_reader = csv.reader (train_df, delimiter='\t')
            pred_reader = csv.reader (pred_df, delimiter='\t')

            for row in train_reader:
                if row[0] == 'text':
                    pass
                elif len (row[0].split ()) < 2 or len (row[0].split ()) > 8:
                    pass
                else:
                    org_feat.append ([row[0], row[1]])

            for row in pred_reader:
                if row[0] == 'text' or "":
                    pass
                else:
                    pred_data.append (row[0])

            # random.shuffle(org_feat)
            for i in org_feat:
                org_data.append (i[0])
                org_label.append (i[1])

            org_data = Steming (org_data)
            pred_data = Steming (pred_data)

            # 벡터가중치:vecW
            vecW = int(self.SSSA_Vector_Weight.text())
            model_dic = {'Multinomial Naive Bayes': 'MNB', 'Bernoulli Naive Bayes': 'BNB', 'Logistic Regression': 'LR',
                         'SGD Classifier': 'SGD', 'Linear SVC': 'LSVM'}
            if self.SSSA_Valid_Type.currentText () == 'Default':
                clf_name = model_dic[self.SSSA_Tr_Model.currentText()]
                if clf_name == 'MNB':
                    clf = Pipeline ([('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', MultinomialNB ())])
                elif clf_name == 'BNB':
                    clf = Pipeline ([('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', BernoulliNB ())])
                elif clf_name == 'LR':
                    clf = Pipeline ([('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', LogisticRegression())])
                elif clf_name == 'SGD':
                    clf = Pipeline ([('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', SGDClassifier ())])
                elif clf_name == 'LSVM':
                    clf = Pipeline ([('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', LinearSVC ())])

                split_size = int (len (org_data) * 0.8)
                train_data = org_data[:split_size]
                train_label = org_label[:split_size]
                test_data = org_data[split_size:]
                test_label = org_label[split_size:]
                clf.fit (train_data, train_label)
                test_pred = clf.predict (test_data)
                prediction = clf.predict (pred_data)
                self.SSSA_Valid_text.setText('--------------------------------------\nSINGLE FOLD RESULT\n--------------------------------------\nClassification Report:\n'+ str(metrics.classification_report (test_label, test_pred))+'\n')

            ##n-fold validation
            else:
                clf_name = model_dic[self.SSSA_Tr_Model.currentText()]
                fold_n = 5  # 5-fold cross-validation
                subset_size = len (org_data) / fold_n
                fold_accuracy = []
                fold_precision = []
                fold_recall = []
                fold_fmeasure = []
                for i in range (fold_n):
                    testing_round = org_data[i * int (subset_size):][:int (subset_size)]
                    testing_round_label = org_label[i * int (subset_size):][:int (subset_size)]
                    training_round = org_data[:i * int (subset_size)] + org_data[(i + 1) * int (subset_size):]
                    training_round_label = org_label[:i * int (subset_size)] + org_label[(i + 1) * int (subset_size):]

                    if clf_name == 'MNB':
                        clf = Pipeline (
                            [('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', MultinomialNB ())])
                    elif clf_name == 'BNB':
                        clf = Pipeline ([('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', BernoulliNB ())])
                    elif clf_name == 'LR':
                        clf = Pipeline (
                            [('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', LogisticRegression ())])
                    elif clf_name == 'SGD':
                        clf = Pipeline (
                            [('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', SGDClassifier ())])
                    elif clf_name == 'LSVM':
                        clf = Pipeline ([('vect', TfidfVectorizer (min_df=vecW, lowercase=False)), ('clf', LinearSVC ())])

                    clf.fit (training_round, training_round_label)
                    test_pred = clf.predict (testing_round)

                    accuracy = metrics.accuracy_score (testing_round_label, test_pred)
                    precision = metrics.precision_score (testing_round_label, test_pred, average='weighted')
                    recall = metrics.recall_score (testing_round_label, test_pred, average='weighted')
                    fmeasure = metrics.f1_score (testing_round_label, test_pred, average='weighted')

                    fold_accuracy.append (accuracy)
                    fold_precision.append (precision)
                    fold_recall.append (recall)
                    fold_fmeasure.append (fmeasure)

                self.SSSA_Valid_text.setText('--------------------------------------\n' + str (fold_n) + '-FOLD CROSS VALIDATION RESULT\n--------------------------------------\nAccuracy: '+ str(sum (fold_accuracy) / fold_n) +'\nPrecision: ' + str(sum (fold_precision) / fold_n) + '\nRecall: '+ str(sum (fold_recall) / fold_n) + '\nF-measure: '+ str(sum (fold_fmeasure) / fold_n))
            self.Process_window.close()
        except Exception:
            pass

    def SESACbasedSSA_export(self):
        result = pandas.DataFrame({'text': pred_data, 'pred': prediction})
        if os.path.isdir ("Result") == False:
            os.mkdir ("Result")
        file_loc = os.path.join ("Result", self.SSSA_result_loc.text())
        result.to_csv (file_loc, sep="\t", encoding="utf-8", index=None)
        os.startfile (file_loc)

    ### PolaLex Module description###
    def PolaLexLGGbasedSSA_module(self):
        self.PolaLex_window = subwindow ()
        self.PolaLex_window.createWindow(500,200)
        self.label = QtWidgets.QLabel (self.PolaLex_window)
        self.label.setGeometry (QtCore.QRect (0, 0, 501, 40))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignCenter)
        self.label.setObjectName ("label")
        self.Polalex_Target_Text = QtWidgets.QLineEdit (self.PolaLex_window)
        self.Polalex_Target_Text.setGeometry (QtCore.QRect (180, 50, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.Polalex_Target_Text.setFont (font)
        self.Polalex_Target_Text.setAlignment (QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Polalex_Target_Text.setClearButtonEnabled (True)
        self.Polalex_Target_Text.setObjectName ("Polalex_Target_Text")
        self.Polalex_browse = QtWidgets.QPushButton (self.PolaLex_window)
        self.Polalex_browse.setGeometry (QtCore.QRect (370, 50, 75, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.Polalex_browse.setFont (font)
        self.Polalex_browse.setObjectName ("Polalex_browse")
        self.Polalex_Type = QtWidgets.QComboBox (self.PolaLex_window)
        self.Polalex_Type.setGeometry (QtCore.QRect (180, 100, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.Polalex_Type.setFont (font)
        self.Polalex_Type.setObjectName ("Polalex_Type")
        self.Polalex_Type.addItem ("")
        self.Polalex_Type.addItem ("")
        self.Polalex_Type.addItem ("")
        self.Polalex_Startbutt = QtWidgets.QPushButton (self.PolaLex_window)
        self.Polalex_Startbutt.setGeometry (QtCore.QRect (180, 150, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.Polalex_Startbutt.setFont (font)
        self.Polalex_Startbutt.setObjectName ("Polalex_Startbutt")
        self.label_2 = QtWidgets.QLabel (self.PolaLex_window)
        self.label_2.setGeometry (QtCore.QRect (-40, 50, 211, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.label_3 = QtWidgets.QLabel (self.PolaLex_window)
        self.label_3.setGeometry (QtCore.QRect (-40, 100, 211, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        _translate = QtCore.QCoreApplication.translate
        self.PolaLex_window.setWindowTitle (_translate ("Form", "PolaLexLGGbasedSSA"))
        self.label.setText (_translate ("Form", "PolaLexLGGbasedSSA"))
        self.Polalex_Target_Text.setText (_translate ("Form", "No file selected"))
        self.Polalex_browse.setText (_translate ("Form", "Browse.."))
        self.Polalex_Type.setItemText (0, _translate ("Form", "Sum-Up 5"))
        self.Polalex_Type.setItemText (1, _translate ("Form", "Last-Head 3"))
        self.Polalex_Type.setItemText (2, _translate ("Form", "DecoSenti-Classifier"))
        self.Polalex_Startbutt.setText (_translate ("Form", "Start PolaLexLGG SSA"))
        self.label_2.setText (_translate ("Form", "Input UNITEX Corpus:"))
        self.label_3.setText (_translate ("Form", "Classifiation Type:"))

        self.Polalex_browse.released.connect(self.PolaLex_Target_open)
        self.Polalex_Startbutt.released.connect(self.PolaLexLGGbasedSSA_Start)

        self.PolaLex_window.show()

    def PolaLex_Target_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.Polalex_Target_Text.setText((str(fname)).split("', '")[0][2:])

    def PolaLexLGGbasedSSA_Start(self):
        try:
            polar_corpus = codecs.open (self.Polalex_Target_Text.text(), encoding='utf-8').read ()
            corpus_temp = re.sub (r"\<[가-힣A-Za-z_]*(QXSP|QXPO|QXSN|QXNG|PSD)\>", "", polar_corpus)
            corpus_temp = re.sub (r"\<\/(QXSP|QXPO|QXSN|QXNG|PSD)\>", "/\\1", corpus_temp)
            corpus_temp = re.sub (r"\<(PSD)\>", "/\\1", corpus_temp)

            font_name = font_manager.FontProperties (fname=Font).get_name ()
            rc ('font', family=font_name)
            style.use ('ggplot')

            def Sum_up_5_fomular(QXSP, QXPO, QXSN, QXNG):
                return ((2 * QXSP) + QXPO) - (QXNG + (QXSN * 2))

            def PolaLex_pieArg(labels, ratio, score_list):
                for i in ["Strongly-Positive", 'Positive', "Strongly-Negative", 'Negative', 'Undeterminable']:
                    if i in score_list:
                        labels.append (i)
                        ratio.append ((score_list.count (i) / len (score_list)) * 100)
                    else:
                        pass

            preprocessed_corpus = corpus_temp.split ('\r\n')

            if self.Polalex_Type.currentText() == 'Sum-Up 5':
                sentence_list = []
                score_list = []
                for i in preprocessed_corpus:
                    sentence_list.append (i.strip ())
                    temp_pol = re.findall (r'/(QXSP|QXPO|QXSN|QXNG)', i)
                    qxsp_count = temp_pol.count ('QXSP')
                    qxpo_count = temp_pol.count ('QXPO')
                    qxsn_count = temp_pol.count ('QXSN')
                    qxng_count = temp_pol.count ('QXNG')
                    score = Sum_up_5_fomular (qxsp_count, qxpo_count, qxsn_count, qxng_count)
                    if score >= 2:
                        score_list.append ("Strongly-Positive")
                    elif score > 0 and score < 2:
                        score_list.append ("Positive")
                    elif score == 0:
                        score_list.append ('Undeterminable')
                    elif score < -2:
                        score_list.append ("Strongly-Negative")
                    else:
                        score_list.append ('Negative')

                result = pandas.DataFrame ({'Sentence': preprocessed_corpus, 'Polarity': score_list},
                                       columns=['Sentence', 'Polarity'])
                result.index += 1
                if os.path.isdir ("Result") == False:
                    os.mkdir ("Result")
                file_loc = os.path.join ("Result", "SumUp_5.txt")
                result.to_csv (file_loc, sep="\t", encoding="utf-8")
                os.startfile (file_loc)

                labels = []
                ratio = []
                PolaLex_pieArg (labels, ratio, score_list)
                plt.pie (ratio, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                plt.show ()

            elif self.Polalex_Type.currentText() == 'Last-Head 3':
                sentence_list = []
                score_list = []
                for i in preprocessed_corpus:
                    sentence_list.append (i.strip ())
                    temp_pol = re.findall (r'/(QXSP|QXPO|QXSN|QXNG)', i)
                    if temp_pol == []:
                        score_list.append ('Undeterminable')
                    else:
                        if temp_pol[-1] in ["QXPO", "QXSP"]:
                            score_list.append ("Positive")
                        else:
                            score_list.append ("Negative")
                result = pandas.DataFrame ({'Sentence': preprocessed_corpus, 'Polarity': score_list},
                                       columns=['Sentence', 'Polarity'])
                result.index += 1
                if os.path.isdir ("Result") == False:
                    os.mkdir ("Result")
                file_loc = os.path.join("Result", "Last_head_3.txt")
                result.to_csv (file_loc, sep="\t", encoding="utf-8")
                os.startfile (file_loc)
                labels = []
                ratio = []
                PolaLex_pieArg (labels, ratio, score_list)
                plt.pie (ratio, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                plt.show ()


            elif self.Polalex_Type.currentText() == 'DecoSenti-Classifier':
                calcSentenceList = []
                score_list = []
                jaso_emotion = re.compile (r"[ㄱ-ㅎㅏ-ㅣ\-]+/(QXSP|QXPO|QXSN|QXNG)")
                for i in preprocessed_corpus:
                    if i.count ('/PSD') >= 1:
                        rep_int = i.count ('/PSD') - 1
                        i = i.replace ('/PSD', '', rep_int)
                        i = i[i.index ('/PSD'):]
                    try:
                        if type (jaso_emotion.search (i).group ()) == str:
                            emo_find = re.findall (r'/(QXSP|QXPO|QXSN|QXNG)',
                                                   i[:i.index (jaso_emotion.search (i).group ())])
                            if emo_find == []:
                                pass
                            else:
                                i = re.sub (jaso_emotion.search (i).group (), '/' + emo_find[-1], i)
                                print (i)
                    except AttributeError:
                        pass
                    calcSentenceList.append (i.strip ())
                    temp_pol = re.findall (r'/(QXSP|QXPO|QXSN|QXNG)', i)
                    qxsp_count = temp_pol.count ('QXSP')
                    qxpo_count = temp_pol.count ('QXPO')
                    qxsn_count = temp_pol.count ('QXSN')
                    qxng_count = temp_pol.count ('QXNG')
                    score = Sum_up_5_fomular (qxsp_count, qxpo_count, qxsn_count, qxng_count)
                    if score >= 2:
                        score_list.append ("Strongly-Positive")
                    elif score > 0 and score < 2:
                        score_list.append ("Positive")
                    elif score == 0:
                        score_list.append ('Undeterminable')
                    elif score < -2:
                        score_list.append ("Strongly-Negative")
                    else:
                        score_list.append ('Negative')
                result = pandas.DataFrame (
                    {'Sentence': preprocessed_corpus, "Calculation Sents": calcSentenceList, 'Polarity': score_list},
                    columns=['Sentence', "Calculation Sents", 'Polarity'])
                result.index += 1
                if os.path.isdir ("Result") == False:
                    os.mkdir ("Result")
                file_loc = os.path.join ("Result", "DecoSenti_Classifier.txt")
                result.to_csv (file_loc, sep="\t", encoding="utf-8")
                os.startfile (file_loc)

                labels = []
                ratio = []
                PolaLex_pieArg (labels, ratio, score_list)
                plt.pie (ratio, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                plt.show ()
        except Exception:
            pass

    ### DecoLGGbasedFSA Module description###
    def LGGbasedFSA_module(self):
        self.LGGFSA_window = subwindow ()
        self.LGGFSA_window.createWindow (500, 300)
        self.label = QtWidgets.QLabel (self.LGGFSA_window)
        self.label.setGeometry (QtCore.QRect (0, 0, 501, 40))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignCenter)
        self.label.setObjectName ("label")
        self.LGGFSA_Target_Text = QtWidgets.QLineEdit (self.LGGFSA_window)
        self.LGGFSA_Target_Text.setGeometry (QtCore.QRect (180, 50, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.LGGFSA_Target_Text.setFont (font)
        self.LGGFSA_Target_Text.setClearButtonEnabled (True)
        self.LGGFSA_Target_Text.setObjectName ("LGGFSA_Target_Text")
        self.LGGFSA_browse = QtWidgets.QPushButton (self.LGGFSA_window)
        self.LGGFSA_browse.setGeometry (QtCore.QRect (370, 50, 75, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.LGGFSA_browse.setFont (font)
        self.LGGFSA_browse.setObjectName ("LGGFSA_browse")
        self.LGGFSA_Startbutt = QtWidgets.QPushButton (self.LGGFSA_window)
        self.LGGFSA_Startbutt.setGeometry (QtCore.QRect (170, 250, 191, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.LGGFSA_Startbutt.setFont (font)
        self.LGGFSA_Startbutt.setObjectName ("LGGFSA_Startbutt")
        self.label_2 = QtWidgets.QLabel (self.LGGFSA_window)
        self.label_2.setGeometry (QtCore.QRect (-90, 50, 261, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.LGGFSA_nFeatures = QtWidgets.QLineEdit (self.LGGFSA_window)
        self.LGGFSA_nFeatures.setGeometry (QtCore.QRect (180, 200, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.LGGFSA_nFeatures.setFont (font)
        self.LGGFSA_nFeatures.setClearButtonEnabled (True)
        self.LGGFSA_nFeatures.setObjectName ("LGGFSA_nFeatures")
        self.label_5 = QtWidgets.QLabel (self.LGGFSA_window)
        self.label_5.setGeometry (QtCore.QRect (-80, 200, 241, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_5.setFont (font)
        self.label_5.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName ("label_5")
        self.frame = QtWidgets.QFrame (self.LGGFSA_window)
        self.frame.setGeometry (QtCore.QRect (40, 90, 411, 101))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.LGGFSA_Spec_input = QtWidgets.QLineEdit (self.frame)
        self.LGGFSA_Spec_input.setGeometry (QtCore.QRect (140, 60, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.LGGFSA_Spec_input.setFont (font)
        self.LGGFSA_Spec_input.setClearButtonEnabled (True)
        self.LGGFSA_Spec_input.setObjectName ("LGGFSA_Spec_input")
        self.LGGFSA_Type = QtWidgets.QComboBox (self.frame)
        self.LGGFSA_Type.setGeometry (QtCore.QRect (140, 10, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.LGGFSA_Type.setFont (font)
        self.LGGFSA_Type.setObjectName ("LGGFSA_Type")
        self.LGGFSA_Type.addItem ("")
        self.LGGFSA_Type.addItem ("")
        self.label_4 = QtWidgets.QLabel (self.frame)
        self.label_4.setGeometry (QtCore.QRect (-70, 60, 191, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_4.setFont (font)
        self.label_4.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName ("label_4")
        self.label_3 = QtWidgets.QLabel (self.frame)
        self.label_3.setGeometry (QtCore.QRect (-100, 10, 221, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        _translate = QtCore.QCoreApplication.translate
        self.LGGFSA_window.setWindowTitle (_translate ("Form", "LGGbasedFSA"))
        self.label.setText (_translate ("Form", "LGG based FSA"))
        self.LGGFSA_Target_Text.setText (_translate ("Form", "No file selected"))
        self.LGGFSA_browse.setText (_translate ("Form", "Browse.."))
        self.LGGFSA_Startbutt.setText (_translate ("Form", "Start LGGbasedFSA"))
        self.label_2.setText (_translate ("Form", "Input UNITEX Corpus:"))
        self.LGGFSA_nFeatures.setText (_translate ("Form", "Input integer"))
        self.label_5.setText (_translate ("Form", "Number of Features:"))
        self.LGGFSA_Spec_input.setText (_translate ("Form", "Input text/integer"))
        self.LGGFSA_Type.setItemText (0, _translate ("Form", "Topic Word"))
        self.LGGFSA_Type.setItemText (1, _translate ("Form", "Number Array"))
        self.label_4.setText (_translate ("Form", "Specific Input:"))
        self.label_3.setText (_translate ("Form", "FSA Type:"))

        self.LGGFSA_browse.released.connect(self.LGGFSA_Target_open)
        self.LGGFSA_Startbutt.released.connect(self.LGGbasedFSA_Start)
        self.LGGFSA_window.show()

    def LGGFSA_Target_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()
        self.LGGFSA_Target_Text.setText((str(fname)).split("', '")[0][2:])
    def LGGbasedFSA_Start(self):
        try:

            tag_pattern1 = re.compile ('(XX[A-Z]+)')

            tag_pattern2 = re.compile ('(QXPO|QXSP|QXJO|QXLO|QXWI|QXNG|QXSN|QXSA|QXDG|QXAN|QXFE|QXEU|XQFT|XX[A-Z]+)')
            target_corpus = codecs.open(self.LGGFSA_Target_Text.text(), 'r', encoding='utf-8').read()
            target_corpus = re.sub (r"\<([가-힣A-Za-z_]*)_(QX[A-Z]+|XQFT|XX[A-Z]+)\>", " \\1/\\2 ", target_corpus)
            target_corpus = re.sub (r"\<\/(QX[A-Z]+|XQFT|XX[A-Z]+)\>", "", target_corpus)
            target_corpus = re.sub (r'[\'\"!?\^\-\\;ㄱ-ㅎ가-힣ㅏ-ㅣ]+/([\'\"!?\^\-\\;ㄱ-ㅎ가-힣ㅏ-ㅣ]+)', '\\1', target_corpus)
            target_corpus = target_corpus.replace ('|', ' ').replace ('+', ' ').replace ('( )+', ' ').replace ('<E>','').replace (
                '{S}', '').replace ('.', '').replace (',', '')

            data_temp = []
            for i in target_corpus.split ('\r\n'):
                target_temp = ""
                if re.search (tag_pattern1, i) != None:
                    for j in i.split ():
                        if re.search (tag_pattern2, j) != None:
                            target_temp += (j + ' ')
                        else:
                            pass
                else:
                    pass
                data_temp.append (target_temp.strip ())

            data_temp = [x for x in data_temp if x]

            FSAPoldic = ["QXSP", "QXPO", "QXNG", "QXSN", "QXJO", "QXEP", "QXLO", "QXWI", "QXSA", "QXDG", "QXAN", "QXFE",
                         "QXEU"]
            FSAPolpos = ['QXPO', 'QXSP', 'QXJO', 'QXEP', 'QXLO', 'QXWI']

            entity_pattern = re.compile (r'([가-힣ㄱ-ㅎ]+)[\/A-Z]*\/(XX[A-Z]+)')
            feature_pattern = re.compile (r'([가-힣ㄱ-ㅎ]+)[\/A-Z]*\/(XQFT)')
            result = []

            for i in data_temp:
                temp = {}
                entity = re.sub (entity_pattern, '\\1', entity_pattern.search (i).group ())
                temp["Entity"] = entity
                if feature_pattern.search (i) == None:
                    feature = 'GEN'
                else:
                    feature = re.sub (feature_pattern, '\\1', feature_pattern.search (i).group ())
                temp['Feature'] = feature
                temp['Total'] = 0
                for pol in FSAPoldic:
                    if pol in i:
                        if pol in FSAPolpos:
                            temp[pol] = i.count (pol)
                            temp['Total'] += i.count (pol)
                            result.append (temp)
                        else:
                            temp[pol] = -1 * i.count (pol)
                            temp['Total'] += i.count (pol)
                            result.append (temp)
                    else:
                        pass

            temp_df = pandas.DataFrame (result)
            temp_df = temp_df.fillna (0)
            temp_df = temp_df.groupby (['Entity', 'Feature'], as_index=False).sum ()
            result_df = temp_df.sort_values (by=['Total'], ascending=False)

            # 단일 어휘 추출(topicWord), 토탈 카운트의 상위 Entity 추출(numArray)
            if self.LGGFSA_Type.currentText() == 'Topic Word':
                try:
                    keyword = self.LGGFSA_Spec_input.text()
                    forPrint_df = result_df[result_df['Entity'].isin([keyword])]
                    # iloc 첫번째는 인덱스는 feture array
                    if self.LGGFSA_nFeatures.text() == "":
                        forPrint_df2 = forPrint_df.iloc[:, 1:]
                    else:
                        forPrint_df2 = forPrint_df.iloc[:int (self.LGGFSA_nFeatures.text ()), 1:]
                    forPrint_df2.set_index (forPrint_df2['Feature'], inplace=True)
                    mpl.rcParams['axes.unicode_minus'] = False
                    font_path = Font
                    font_name = fm.FontProperties (fname=font_path, size=18).get_name ()
                    mpl.rc ('font', family=font_name)
                    del forPrint_df2['Total']
                    # print (list(forPrint_df2.iloc[1].index[:])[1:])
                    forPrint_df2.plot.bar (stacked=True, edgecolor='white')
                    plt.title (keyword)
                    plt.xlabel ('Feature')
                    plt.ylabel ("Polarity")
                    mplcursors.cursor (hover=True).connect ('add')
                except TypeError:
                    print ('데이터가 없습니다.')


            else:
                try:
                    entity_temp = list (result_df.iloc[:, 0])
                    entity_list = []
                    entity_counter = 0
                    # entity couter는 상위 entity 개수
                    for i in entity_temp:
                        if i not in entity_list:
                            entity_list.append (i)
                            entity_counter += 1
                        if entity_counter == int(self.LGGFSA_Spec_input.text()):
                            break

                    for i in entity_list:
                        forPrint_df_sep = result_df[result_df['Entity'].isin ([i])]
                        # iloc 첫번째는 인덱스는 feture array
                        if self.LGGFSA_nFeatures.text() == "":
                            forPrint_df_sep = forPrint_df_sep.iloc[:, 1:]
                        else:
                            forPrint_df_sep = forPrint_df_sep.iloc[:int(self.LGGFSA_nFeatures.text()), 1:]
                        forPrint_df_sep.set_index (forPrint_df_sep['Feature'], inplace=True)
                        mpl.rcParams['axes.unicode_minus'] = False
                        font_path = Font
                        font_name = fm.FontProperties (fname=font_path, size=18).get_name ()
                        mpl.rc ('font', family=font_name)
                        del forPrint_df_sep['Total']
                        forPrint_df_sep.plot.bar (stacked=True, edgecolor="black")
                        plt.title (i)
                        plt.xlabel ('Feature')
                        plt.ylabel ("Polarity")
                        mplcursors.cursor (hover=True).connect ('add')
                except TypeError:
                    print ('데이터가 없습니다.')
        except Exception:
            pass

        plt.show ()

    ### MorphemeCloud Module description###
    def MorphemeCloud_module(self):
        self.MorphC_window = subwindow ()
        _translate = QtCore.QCoreApplication.translate
        self.MorphC_window.createWindow (570, 200)
        self.label = QtWidgets.QLabel (self.MorphC_window)
        self.label.setGeometry (QtCore.QRect (0, 0, 571, 40))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignCenter)
        self.label.setObjectName ("label")
        self.MorphC_Text = QtWidgets.QLineEdit (self.MorphC_window)
        self.MorphC_Text.setGeometry (QtCore.QRect (180, 50, 251, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.MorphC_Text.setFont (font)
        self.MorphC_Text.setClearButtonEnabled(True)
        self.MorphC_Text.setObjectName ("MorphC_Text")
        self.MorphC_browse = QtWidgets.QPushButton (self.MorphC_window)
        self.MorphC_browse.setGeometry (QtCore.QRect (450, 50, 81, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.MorphC_browse.setFont (font)
        self.MorphC_browse.setObjectName ("MorphC_browse")
        self.label_2 = QtWidgets.QLabel (self.MorphC_window)
        self.label_2.setGeometry (QtCore.QRect (0, 50, 171, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.frame = QtWidgets.QFrame (self.MorphC_window)
        self.frame.setGeometry (QtCore.QRect (20, 89, 511, 71))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.MorphC_x = QtWidgets.QLineEdit (self.frame)
        self.MorphC_x.setGeometry (QtCore.QRect (70, 10, 41, 20))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.MorphC_x.setFont (font)
        self.MorphC_x.setAlignment (QtCore.Qt.AlignCenter)
        self.MorphC_x.setObjectName ("MorphC_x")
        self.MorphC_y = QtWidgets.QLineEdit (self.frame)
        self.MorphC_y.setGeometry (QtCore.QRect (70, 40, 41, 20))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.MorphC_y.setFont (font)
        self.MorphC_y.setAlignment (QtCore.Qt.AlignCenter)
        self.MorphC_y.setObjectName ("MorphC_y")
        self.MorphC_bgc = QtWidgets.QComboBox (self.frame)
        self.MorphC_bgc.setGeometry (QtCore.QRect (220, 10, 81, 22))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.MorphC_bgc.setFont (font)
        self.MorphC_bgc.setSizeAdjustPolicy (QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.MorphC_bgc.setObjectName ("MorphC_bgc")
        self.MorphC_bgc.addItem ("")
        self.MorphC_bgc.addItem ("")
        self.MorphC_mask = QtWidgets.QComboBox (self.frame)
        self.MorphC_mask.setGeometry (QtCore.QRect (220, 40, 81, 22))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.MorphC_mask.setFont (font)
        self.MorphC_mask.setObjectName ("MorphC_mask")
        self.MorphC_mfs = QtWidgets.QLineEdit (self.frame)
        self.MorphC_mfs.setGeometry (QtCore.QRect (470, 10, 31, 20))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.MorphC_mfs.setFont (font)
        self.MorphC_mfs.setObjectName ("MorphC_mfs")
        self.MorphC_stem = QtWidgets.QCheckBox (self.frame)
        self.MorphC_stem.setGeometry (QtCore.QRect (310, 40, 191, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.MorphC_stem.setFont (font)
        self.MorphC_stem.setLayoutDirection (QtCore.Qt.RightToLeft)
        self.MorphC_stem.setObjectName ("MorphC_stem")
        self.label_3 = QtWidgets.QLabel (self.frame)
        self.label_3.setGeometry (QtCore.QRect (-10, 10, 71, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        self.label_4 = QtWidgets.QLabel (self.frame)
        self.label_4.setGeometry (QtCore.QRect (0, 40, 61, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_4.setFont (font)
        self.label_4.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName ("label_4")
        self.label_5 = QtWidgets.QLabel (self.frame)
        self.label_5.setGeometry (QtCore.QRect (120, 10, 91, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_5.setFont (font)
        self.label_5.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName ("label_5")
        self.label_6 = QtWidgets.QLabel (self.frame)
        self.label_6.setGeometry (QtCore.QRect (130, 40, 81, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_6.setFont (font)
        self.label_6.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName ("label_6")
        self.label_7 = QtWidgets.QLabel (self.frame)
        self.label_7.setGeometry (QtCore.QRect (320, 10, 141, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_7.setFont (font)
        self.label_7.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName ("label_7")
        self.MorphC_startButton = QtWidgets.QPushButton (self.MorphC_window)
        self.MorphC_startButton.setGeometry (QtCore.QRect (230, 170, 81, 23))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.MorphC_startButton.setFont (font)
        self.MorphC_startButton.setObjectName ("MorphC_startB")
        _translate = QtCore.QCoreApplication.translate
        self.MorphC_window.setWindowTitle (_translate ("Form", "Morpheme Cloud"))
        self.label.setText (_translate ("Form", "Morpheme Cloud"))
        self.MorphC_Text.setText (_translate ("Form", "No file seleted"))
        self.MorphC_browse.setText (_translate ("Form", "Browse.."))
        self.label_2.setText (_translate ("Form", "Text file input(.txt): "))
        self.MorphC_x.setText (_translate ("Form", "800"))
        self.MorphC_y.setText (_translate ("Form", "800"))
        self.MorphC_bgc.setItemText (0, _translate ("Form", "white"))
        self.MorphC_bgc.setItemText (1, _translate ("Form", "black"))
        self.MorphC_mfs.setText (_translate ("Form", "10"))
        self.MorphC_stem.setText (_translate ("Form", "Apply Korean Stemmer:"))
        self.label_3.setText (_translate ("Form", "x-axis:"))
        self.label_4.setText (_translate ("Form", "y-axis:"))
        self.label_5.setText (_translate ("Form", "background:"))
        self.label_6.setText (_translate ("Form", "mask:"))
        self.label_7.setText (_translate ("Form", "Minimum font size:"))
        self.MorphC_startButton.setText (_translate ("Form", "Start"))


        self.MorphC_browse.released.connect (self.MorphC_Target_open)
        self.MorphC_startButton.released.connect (self.MorphC_Start)
        self.MorphC_window.show ()

    def MorphC_Target_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName ()
        self.MorphC_Text.setText ((str (fname)).split ("', '")[0][2:])

    def MorphC_Start(self):
        try:
            target_corpus = codecs.open (self.MorphC_Text.text(), 'r', encoding='utf-8')
            tagged_temp = []

            if self.MorphC_stem.isChecked() == True:
                tagger = Kiwi ()
                tagger.prepare ()
                for i in target_corpus:
                    i = i.strip ()
                    temp_tagging = [x[0] for x in tagger.analyze (i, top_n=1)]
                    inner_temp = ["{}/{}".format (word, tag) for word, tag, score1, score2 in temp_tagging[0]]
                    tagged_temp.append (tuple (inner_temp))

                tagged_list = []

                for i in tagged_temp:
                    for j in i:
                        if '/V' in j:
                            j = j.replace ('/VV', '다/VV')
                            tagged_list.append (j)
                        elif '/A' in j:
                            j.replace ('/VA', '다/VA')
                            tagged_list.append (j)
                        else:
                            tagged_list.append (j)

                wordfreqDict = {}
                for morph_tag in tagged_list:
                    morph = morph_tag.split ('/')[0]
                    tag = morph_tag.split ('/')[1]
                    if tag.startswith ('N' or 'VV' or 'VA' or 'D'):
                        if morph in wordfreqDict:
                            wordfreqDict[morph] += 1
                        else:
                            wordfreqDict[morph] = 1
            else:
                wordfreqDict = {}
                tagged_list = target_corpus.read ().split ()
                for word in tagged_list:
                    if word in wordfreqDict:
                        wordfreqDict[word] += 1
                    else:
                        wordfreqDict[word] = 1

            font_path = Font
            wordcloud = WordCloud (font_path=font_path,
                                   width=int(self.MorphC_x.text()),
                                   height=int(self.MorphC_y.text()),
                                   background_color=self.MorphC_bgc.currentText(),
                                   prefer_horizontal=0.9999,
                                   min_font_size=int(self.MorphC_mfs.text()))
            wordcloud = wordcloud.generate_from_frequencies (wordfreqDict)

            # 이미지 사이즈
            fig = plt.figure (figsize=(12, 12))

            plt.imshow (wordcloud, interpolation='bilinear')
            plt.axis ('off')
            plt.show ()
        except Exception:
            pass

    ### SSAbasedTrend description ###
    def SSAbasedTrend_module(self):
        self.SSAbasedTrend_window = subwindow ()
        self.SSAbasedTrend_window.createWindow (501, 206)
        self.label = QtWidgets.QLabel (self.SSAbasedTrend_window)
        self.label.setGeometry (QtCore.QRect (0, 0, 501, 40))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignCenter)
        self.label.setObjectName ("label")
        self.SSATrend_Input = QtWidgets.QLineEdit (self.SSAbasedTrend_window)
        self.SSATrend_Input.setGeometry (QtCore.QRect (210, 60, 161, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSATrend_Input.setFont (font)
        self.SSATrend_Input.setObjectName ("SSATrend_Input")
        self.SSATrend_Browse = QtWidgets.QPushButton (self.SSAbasedTrend_window)
        self.SSATrend_Browse.setGeometry (QtCore.QRect (400, 60, 75, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.SSATrend_Browse.setFont (font)
        self.SSATrend_Browse.setObjectName ("SSATrend_Browse")
        self.SSATrend_Int = QtWidgets.QComboBox (self.SSAbasedTrend_window)
        self.SSATrend_Int.setGeometry (QtCore.QRect (210, 110, 31, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSATrend_Int.setFont (font)
        self.SSATrend_Int.setObjectName ("SSATrend_Int")
        self.SSATrend_Int.addItem ("")
        self.SSATrend_Int.addItem ("")
        self.SSATrend_Int.addItem ("")
        self.SSATrend_Int.addItem ("")
        self.SSATrend_Int.addItem ("")
        self.SSATrend_Int.addItem ("")
        self.SSATrend_Int.addItem ("")
        self.SSATrend_GroupD = QtWidgets.QComboBox (self.SSAbasedTrend_window)
        self.SSATrend_GroupD.setGeometry (QtCore.QRect (260, 110, 111, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSATrend_GroupD.setFont (font)
        self.SSATrend_GroupD.setObjectName ("SSATrend_GroupD")
        self.SSATrend_GroupD.addItem ("")
        self.SSATrend_GroupD.addItem ("")
        self.SSATrend_GroupD.addItem ("")
        self.SSATrend_GroupD.addItem ("")
        self.SSATrend_Output = QtWidgets.QLineEdit (self.SSAbasedTrend_window)
        self.SSATrend_Output.setGeometry (QtCore.QRect (212, 160, 161, 31))
        font = QtGui.QFont ()
        font.setFamily ("Arial")
        self.SSATrend_Output.setFont (font)
        self.SSATrend_Output.setObjectName ("SSATrend_Output")
        self.SSATrend_Start = QtWidgets.QPushButton (self.SSAbasedTrend_window)
        self.SSATrend_Start.setGeometry (QtCore.QRect (400, 160, 75, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.SSATrend_Start.setFont (font)
        self.SSATrend_Start.setObjectName ("SSATrend_Start")
        self.label_2 = QtWidgets.QLabel (self.SSAbasedTrend_window)
        self.label_2.setGeometry (QtCore.QRect (10, 60, 191, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.label_3 = QtWidgets.QLabel (self.SSAbasedTrend_window)
        self.label_3.setGeometry (QtCore.QRect (-20, 110, 221, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        self.label_4 = QtWidgets.QLabel (self.SSAbasedTrend_window)
        self.label_4.setGeometry (QtCore.QRect (-20, 160, 221, 31))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_4.setFont (font)
        self.label_4.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName ("label_4")
        _translate = QtCore.QCoreApplication.translate
        self.SSAbasedTrend_window.setWindowTitle (_translate ("Form", "Form"))
        self.label.setText (_translate ("Form", "SSAbasedTrend"))
        self.SSATrend_Input.setText (_translate ("Form", "No file selected"))
        self.SSATrend_Browse.setText (_translate ("Form", "Browse.."))
        self.SSATrend_Int.setItemText (0, _translate ("Form", "1"))
        self.SSATrend_Int.setItemText (1, _translate ("Form", "2"))
        self.SSATrend_Int.setItemText (2, _translate ("Form", "3"))
        self.SSATrend_Int.setItemText (3, _translate ("Form", "4"))
        self.SSATrend_Int.setItemText (4, _translate ("Form", "5"))
        self.SSATrend_Int.setItemText (5, _translate ("Form", "6"))
        self.SSATrend_Int.setItemText (6, _translate ("Form", "7"))
        self.SSATrend_GroupD.setItemText (0, _translate ("Form", "Day"))
        self.SSATrend_GroupD.setItemText (1, _translate ("Form", "Week"))
        self.SSATrend_GroupD.setItemText (2, _translate ("Form", "Month"))
        self.SSATrend_GroupD.setItemText (3, _translate ("Form", "Year"))
        self.SSATrend_Output.setText (_translate ("Form", ".csv format"))
        self.SSATrend_Start.setText (_translate ("Form", "Start"))
        self.label_2.setText (_translate ("Form", "Input Polarity Data(.csv):"))
        self.label_3.setText (_translate ("Form", "Grouping Sentiment by Date:"))
        self.label_4.setText (_translate ("Form", "Save File Input:"))

        self.SSATrend_Browse.released.connect(self.SSATrend_open)
        self.SSATrend_Start.released.connect(self.SSATrend_process)

        self.SSAbasedTrend_window.show()

    def SSATrend_open(self):
        fname = QtWidgets.QFileDialog.getOpenFileName ()
        self.SSATrend_Input.setText ((str (fname)).split ("', '")[0][2:])

    def SSATrend_process(self):
        try:
            data = list (csv.reader (open (self.SSATrend_Input.text(), 'r', encoding='cp949')))[1:]
            pol_data = pandas.read_csv (self.SSATrend_Input.text(), names=['date', 'pol'])[1:]

            # data의 논항들 리스트화
            pv = list (set (pol_data.pol.tolist ()))

            ##데이터 프레임 정렬

            startDate = data[0][0]
            endDate = data[-1][0]
            tempDt = pandas.to_datetime (startDate, dayfirst=True)
            tempDt = datetime.datetime.date (tempDt)
            endDt = pandas.to_datetime (endDate, dayfirst=True)
            dtList = []
            while True:
                tempStr = str (tempDt)
                dtList.append (tempStr)
                tempDt += datetime.timedelta (days=1)  ##이 숫자를 변형해서 주기 설정 가능 , 단, weeks(주)단위가 최대
                if tempDt >= endDt:
                    tempStr = str (tempDt)
                    dtList.append (tempStr)
                    break

            res = []

            for x in data:
                temp = {}
                for y in dtList:
                    if y in x:
                        temp['date'] = y
                    else:
                        continue
                for z in pv:
                    if z in pv:
                        temp[z] = x.count (z)
                    else:
                        continue
                res.append (temp)
            pol_df = pandas.DataFrame (res)
            pol_df = pol_df.groupby (['date'], as_index=False).sum ()
            pol_df['date'] = pandas.to_datetime (pol_df['date'])
            pol_df = pol_df.set_index ('date', inplace=False)

            ##날짜 범위 설정해주기
            n = self.SSATrend_Int.currentText() + self.SSATrend_GroupD.currentText()[0]
            n_pol_df = pol_df.resample (n).sum ()
            n_pol_df = n_pol_df.reset_index ('date')
            print (n_pol_df)

            # 그래프 그리기

            pol_graph = (
                    ggplot (n_pol_df, aes (x='date'))
                    + stat_smooth (aes (y='POSITIVE', group=1), se=False, color='#33cccc')  # 평균 선 그리기
                    + stat_smooth (aes (y='NEGATIVE', group=2), color='crimson', se=False)  # 평균 선 그리기
                    + geom_line (aes (y='POSITIVE'), color='#33cccc', alpha=0.3)
                    + geom_line (aes (y='NEGATIVE'), color='crimson', alpha=0.3)
                    + geom_point (aes (y='POSITIVE'), color='#33cccc', size=2, alpha=0.3)  # alpha는 투명도 0부터1까지
                    + geom_point (aes (y='NEGATIVE'), color='crimson', size=2, alpha=0.3)
                    + ylab ("Sentiment")
                    + xlab ("Date")
                    + theme (axis_line=element_line (color='black'))
                    + theme_bw ()
                    + theme (panel_background=element_rect (),
                             plot_background=element_rect (),
                             strip_background=element_rect (),
                             panel_grid_major_x=element_line (size=0.1, color='grey', linetype='-'),
                             panel_grid_minor_x=element_rect (),
                             panel_spacing=float (1),
                             axis_line=element_line (size=0.6, color='black'),
                             legend_key=element_rect (fill='white'),
                             axis_ticks=element_line (color='black'),
                             figure_size=(16, 8),
                             )
                    + theme (axis_line=element_line (color='black'))
            )

            print (pol_graph)

            ##csv파일로 출력
            if os.path.isdir ("Result") == False:
                os.mkdir ("Result")
            file_loc = os.path.join ("Result", self.SSATrend_Output.text())
            n_pol_df.to_csv (file_loc)
            os.startfile (file_loc)
        except Exception:
            pass

    ### AboutDicora description###
    def AboutDicora_Info(self):
        self.AboutDicora_window = subwindow ()
        self.AboutDicora_window.createWindow (540, 210)
        self.label = QtWidgets.QLabel (self.AboutDicora_window)
        self.label.setGeometry (QtCore.QRect (0, 10, 210, 30))
        font = QtGui.QFont ()
        font.setFamily ("HY산B")
        font.setPointSize (16)
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label.setFont (font)
        self.label.setAlignment (QtCore.Qt.AlignCenter)
        self.label.setObjectName ("label")
        self.label_2 = QtWidgets.QLabel (self.AboutDicora_window)
        self.label_2.setGeometry (QtCore.QRect (10, 165, 521, 20))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (8)
        self.label_2.setFont (font)
        self.label_2.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName ("label_2")
        self.label_3 = QtWidgets.QLabel (self.AboutDicora_window)
        self.label_3.setGeometry (QtCore.QRect (0, 180, 531, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setPointSize (8)
        self.label_3.setFont (font)
        self.label_3.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName ("label_3")
        self.frame = QtWidgets.QFrame (self.AboutDicora_window)
        self.frame.setGeometry (QtCore.QRect (10, 40, 521, 111))
        self.frame.setFrameShape (QtWidgets.QFrame.Box)
        self.frame.setFrameShadow (QtWidgets.QFrame.Raised)
        self.frame.setObjectName ("frame")
        self.label_8 = QtWidgets.QLabel (self.frame)
        self.label_8.setGeometry (QtCore.QRect (192, 80, 331, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_8.setFont (font)
        self.label_8.setObjectName ("label_8")
        self.label_9 = QtWidgets.QLabel (self.frame)
        self.label_9.setGeometry (QtCore.QRect (-10, 80, 201, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label_9.setFont (font)
        self.label_9.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName ("label_9")
        self.label_6 = QtWidgets.QLabel (self.frame)
        self.label_6.setGeometry (QtCore.QRect (220, 30, 261, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        self.label_6.setFont (font)
        self.label_6.setAlignment (QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName ("label_6")
        self.label_4 = QtWidgets.QLabel (self.frame)
        self.label_4.setGeometry (QtCore.QRect (34, 30, 181, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setBold (True)
        font.setItalic (False)
        font.setWeight (75)
        self.label_4.setFont (font)
        self.label_4.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName ("label_4")
        self.label_5 = QtWidgets.QLabel (self.frame)
        self.label_5.setGeometry (QtCore.QRect (-10, 10, 181, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setItalic (True)
        self.label_5.setFont (font)
        self.label_5.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName ("label_5")
        self.label_7 = QtWidgets.QLabel (self.frame)
        self.label_7.setGeometry (QtCore.QRect (-10, 60, 181, 21))
        font = QtGui.QFont ()
        font.setFamily ("휴먼옛체")
        font.setItalic (True)
        self.label_7.setFont (font)
        self.label_7.setAlignment (QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName ("label_7")
        _translate = QtCore.QCoreApplication.translate
        self.AboutDicora_window.setWindowTitle (_translate ("Form", "About Dicora"))
        self.label.setText (_translate ("Form", "About Dicora"))
        self.label_2.setText (_translate ("Form", "COPYRIGHT @ 2019 DICORA HANKUK UNIVERSITY OF FOREIGN STUDIES"))
        self.label_3.setText (_translate ("Form", "81 OYDAE-RO CHEOIN-GU YONGIN-SI GYEONGGI-DO 17035 KOREA"))
        self.label_8.setText (_translate ("Form", ", Professor, Ph.D., Director of DICORA, HUFS"))
        self.label_9.setText (_translate ("Form", "Jeesun Nam"))
        self.label_6.setText (_translate ("Form", ", Senior Researcher of DICORA, HUFS"))
        self.label_4.setText (_translate ("Form", "ChangHoe Hwang"))
        self.label_5.setText (_translate ("Form", "Program Developed by "))
        self.label_7.setText (_translate ("Form", "Directed by "))

        self.AboutDicora_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DecoPyTex_Main = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(DecoPyTex_Main)
    DecoPyTex_Main.show()
    sys.exit(app.exec_())