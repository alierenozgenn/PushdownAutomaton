#!/usr/bin/env python3
"""
Matematiksel İfade Doğrulama için Pushdown Automaton Simülatörü
PDA (Pushdown Automaton), parantezlerin dengesini ve operatörlerin doğru yerleşimini kontrol eder.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QTimer
from gui import PDASimulatorGUI
import platform

def create_resources_directory():
    """Kaynaklar dizinini oluştur ve icon.png dosyasını hazırla"""
    os.makedirs('resources', exist_ok=True)
    
    # Basit bir ikon oluştur
    from PyQt5.QtCore import QSize
    
    pixmap = QPixmap(128, 128)
    pixmap.fill(QColor('#2c3e50'))  # Koyu mavi arkaplan
    
    painter = QPainter(pixmap)
    painter.setPen(QColor('white'))
    painter.setFont(QFont('Arial', 60, QFont.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "PDA")
    painter.end()
    
    icon_path = os.path.join('resources', 'icon.png')
    pixmap.save(icon_path)
    
    return icon_path

def main():
    """Uygulamayı başlat"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern görünüm için Fusion stilini kullan
    
    # MacOS için menü barını ayarla
    if platform.system() == 'Darwin':
        app.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    
    # Kaynaklar dizinini kontrol et ve oluştur
    icon_path = create_resources_directory()
    
    # Açılış ekranı
    splash_pixmap = QPixmap(400, 200)
    splash_pixmap.fill(QColor('#ecf0f1'))  # Açık gri arkaplan
    
    painter = QPainter(splash_pixmap)
    painter.setPen(QColor('#2c3e50'))  # Koyu mavi yazı
    painter.setFont(QFont('Arial', 24, QFont.Bold))
    painter.drawText(splash_pixmap.rect(), Qt.AlignCenter, "PDA Simülatörü\nYükleniyor...")
    painter.end()
    
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    
    # Ana uygulama penceresi
    window = PDASimulatorGUI()
    
    # Kısa gecikme sonrası ana pencereyi göster
    QTimer.singleShot(1500, lambda: (splash.finish(window), window.show()))
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()