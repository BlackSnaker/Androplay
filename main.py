import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, 
    QTabWidget, QHBoxLayout, QListWidget, QFileDialog, QListWidgetItem, QSlider
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class TrackWidget(QWidget):
    def __init__(self, track_name, artist_name, duration, track_path, parent=None):
        super().__init__(parent)
        self.track_path = track_path

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #292929, 
                    stop: 1 #333333);
                border-radius: 10px;
                padding: 10px;
            }
            QWidget:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #343434, 
                    stop: 1 #4a4a4a);
                border: 1px solid #0074D9;
            }
            QLabel {
                color: white;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Иконка трека
        icon_label = QLabel(self)
        icon_label.setFixedSize(40, 40)
        icon_label.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, 
                x2: 1, y2: 1, 
                stop: 0 #555555, 
                stop: 1 #777777);
            border-radius: 20px;
        """)
        layout.addWidget(icon_label)

        info_layout = QVBoxLayout()

        # Название трека
        self.track_name_label = QLabel(track_name, self)
        self.track_name_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.track_name_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
            }
            QLabel:hover {
                color: #ffffff;
                font-size: 13px;
            }
        """)
        info_layout.addWidget(self.track_name_label)

        # Имя артиста
        self.artist_name_label = QLabel(artist_name, self)
        self.artist_name_label.setFont(QFont('Arial', 10))
        self.artist_name_label.setStyleSheet("color: #b0b0b0;")
        info_layout.addWidget(self.artist_name_label)

        layout.addLayout(info_layout)

        # Длительность трека
        self.duration_label = QLabel(duration, self)
        self.duration_label.setFont(QFont('Arial', 10))
        self.duration_label.setStyleSheet("color: #b0b0b0;")
        layout.addWidget(self.duration_label)

class MusicPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EL Music Player")
        self.setFixedSize(400, 700)

        # Инициализация медиаплеера
        self.player = QMediaPlayer()
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)

        # Применение градиента для основного виджета
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #001f3f, 
                    stop: 0.5 #0074D9, 
                    stop: 1 #001f3f);
            }
            QLabel {
                color: white;
            }
            QTabWidget::pane {
                background: #3a3a3a;
                border: none;
            }
            QTabBar::tab {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #4a4a4a, 
                    stop: 1 #5a5a5a);
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #0074D9, 
                    stop: 1 #0056A3);
                color: #ffffff;
            }
            QListWidget {
                background-color: #2a2a2a;
                border: none;
                color: white;
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #444444, 
                    stop: 1 #666666);
                border-radius: 20px;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #555555, 
                    stop: 1 #777777);
            }
            QSlider::groove:horizontal {
                background: #3a3a3a;
                border-radius: 5px;
                height: 10px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #0074D9, 
                    stop: 1 #33aaff);
                border-radius: 5px;
            }
            QSlider::add-page:horizontal {
                background: #2a2a2a;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                border: 1px solid #0074D9;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #33aaff;
                border: 1px solid #0056A3;
            }
        """)

        # Заголовок
        title = QLabel("JW Music")
        title.setFont(QFont('Arial', 16))
        title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(title)

        # Вкладки
        self.tabs = QTabWidget()
        self.tracks_tab = QWidget()
        self.albums_tab = QWidget()
        self.playlists_tab = QWidget()
        self.artists_tab = QWidget()

        self.tabs.addTab(self.tracks_tab, "Треки")
        self.tabs.addTab(self.albums_tab, "Альбомы")
        self.tabs.addTab(self.playlists_tab, "Плейлисты")
        self.tabs.addTab(self.artists_tab, "Артисты")
        self.main_layout.addWidget(self.tabs)

        # Вкладка "Треки"
        self.tracks_layout = QVBoxLayout(self.tracks_tab)
        self.tracks_list = QListWidget()
        self.tracks_list.itemDoubleClicked.connect(self.show_track_info)
        self.tracks_layout.addWidget(self.tracks_list)

        # Кнопка добавления треков
        add_track_button = QPushButton("Добавить трек")
        add_track_button.setIcon(QIcon("/home/blacksnaker/Androplay/icons/add.png"))  # Добавляем иконку
        add_track_button.clicked.connect(self.add_track)
        self.tracks_layout.addWidget(add_track_button)

        # Панель управления воспроизведением
        self.playback_panel = QWidget()
        self.playback_panel.setFixedHeight(150)
        self.playback_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #2c2c2c, 
                    stop: 1 #3a3a3a);
                border-top: 2px solid #444444;
                border-radius: 15px;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #444444, 
                    stop: 1 #666666);
                border-radius: 25px;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1, 
                    stop: 0 #555555, 
                    stop: 1 #777777);
            }
        """)

        self.playback_layout = QVBoxLayout(self.playback_panel)

        # Информация о треке
        self.track_info_layout = QHBoxLayout()
        
        self.track_icon = QLabel()
        self.track_icon.setFixedSize(50, 50)
        self.track_icon.setStyleSheet("background-color: #555555; border-radius: 25px;")  # Заглушка для иконки
        self.track_info_layout.addWidget(self.track_icon)

        self.track_details_layout = QVBoxLayout()

        self.track_name_label = QLabel("Название трека")
        self.track_name_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.track_details_layout.addWidget(self.track_name_label)

        self.track_artist_label = QLabel("Имя артиста")
        self.track_artist_label.setFont(QFont('Arial', 10))
        self.track_details_layout.addWidget(self.track_artist_label)

        self.track_info_layout.addLayout(self.track_details_layout)
        self.playback_layout.addLayout(self.track_info_layout)

        # Слайдер прогресса
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.sliderMoved.connect(self.set_position)
        self.playback_layout.addWidget(self.progress_slider)

        # Кнопки управления
        self.controls_layout = QHBoxLayout()
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("/home/blacksnaker/Androplay/icons/play.png"))
        self.play_button.setIconSize(QSize(30, 30))
        self.play_button.setFixedSize(50, 50)
        self.play_button.clicked.connect(self.toggle_playback)
        self.controls_layout.addWidget(self.play_button)

        self.playback_layout.addLayout(self.controls_layout)
        self.main_layout.addWidget(self.playback_panel)

    def add_track(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите музыкальные файлы", "", "Audio Files (*.mp3 *.wav *.flac)")

        if files:
            for file in files:
                track_name = file.split("/")[-1]
                track_widget = TrackWidget(track_name, "Unknown Artist", "3:45", file)
                list_item = QListWidgetItem()
                list_item.setSizeHint(track_widget.sizeHint())
                self.tracks_list.addItem(list_item)
                self.tracks_list.setItemWidget(list_item, track_widget)

    def show_track_info(self, item):
        track_widget = self.tracks_list.itemWidget(item)
        if track_widget:
            track_name = track_widget.track_name_label.text()
            artist_name = track_widget.artist_name_label.text()

            # Обновляем информацию в панели воспроизведения
            self.track_name_label.setText(track_name)
            self.track_artist_label.setText(artist_name)
            self.track_icon.setStyleSheet("background-color: #555555; border-radius: 25px;")  # Заглушка для иконки

            # Загружаем трек в плеер
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(track_widget.track_path)))
            self.player.play()
            self.play_button.setIcon(QIcon("/home/blacksnaker/Androplay/icons/pause.png"))  # Меняем иконку на паузу

    def toggle_playback(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setIcon(QIcon("/home/blacksnaker/Androplay/icons/play.png"))  # Меняем иконку на воспроизведение
        else:
            self.player.play()
            self.play_button.setIcon(QIcon("/home/blacksnaker/Androplay/icons/pause.png"))  # Меняем иконку на паузу

    def update_position(self, position):
        self.progress_slider.setValue(position)

    def update_duration(self, duration):
        self.progress_slider.setRange(0, duration)

    def set_position(self, position):
        self.player.setPosition(position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayerApp()
    player.show()
    sys.exit(app.exec_())
