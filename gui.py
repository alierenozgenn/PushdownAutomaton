from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QSplitter, QFrame, QListWidget,
                            QListWidgetItem, QMessageBox, QApplication, QHeaderView)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap
import os
import sys
from styles import STYLES, get_stack_item_style
from pda import PDA

class PDASimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.pda = PDA()
        self.history = []  # İncelenen ifadelerin geçmişi
        self.current_step = -1
        self.simulation_results = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Pushdown Automaton Simulator")
        self.setWindowIcon(QIcon(os.path.join('resources', 'icon.png')))
        self.resize(1000, 800)
        
        # Ana widget ve layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Üst bölüm - Giriş ve kontrol butonları
        input_layout = QHBoxLayout()
        
        # İfade giriş alanı
        self.expression_input = QLineEdit()
        self.expression_input.setPlaceholderText("Matematiksel ifade girin... Örnek: (3+4)*5")
        self.expression_input.returnPressed.connect(self.check_expression)
        self.expression_input.setStyleSheet(STYLES['input'])
        
        # Kontrol et butonu
        self.check_button = QPushButton("Kontrol Et")
        self.check_button.clicked.connect(self.check_expression)
        self.check_button.setStyleSheet(STYLES['button'])
        self.check_button.setMinimumWidth(120)
        
        # Animasyon butonları
        self.start_animation_button = QPushButton("Adım Adım Göster")
        self.start_animation_button.clicked.connect(self.start_animation)
        self.start_animation_button.setStyleSheet(STYLES['button'])
        
        self.next_step_button = QPushButton("Sonraki Adım")
        self.next_step_button.clicked.connect(self.next_step)
        self.next_step_button.setStyleSheet(STYLES['button'])
        self.next_step_button.setEnabled(False)
        
        self.reset_button = QPushButton("Sıfırla")
        self.reset_button.clicked.connect(self.reset_simulation)
        self.reset_button.setStyleSheet(STYLES['button'])
        
        input_layout.addWidget(self.expression_input)
        input_layout.addWidget(self.check_button)
        input_layout.addWidget(self.start_animation_button)
        input_layout.addWidget(self.next_step_button)
        input_layout.addWidget(self.reset_button)
        
        # Orta bölüm - Simülasyon ve Stack görselleştirme
        middle_layout = QHBoxLayout()
        
        # Sol taraf - Simülasyon tablo ve sonuç göstergesi
        left_panel = QVBoxLayout()
        
        # Simülasyon başlığı
        simulation_header = QLabel("İfade Analizi")
        simulation_header.setStyleSheet(STYLES['header'])
        left_panel.addWidget(simulation_header)
        
        # Simülasyon tablosu
        self.simulation_table = QTableWidget(0, 5)
        self.simulation_table.setHorizontalHeaderLabels(["İndeks", "Karakter", "Durum", "Açıklama", "Geçerli"])
        self.simulation_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.simulation_table.verticalHeader().setVisible(False)
        self.simulation_table.setStyleSheet(STYLES['table'])
        self.simulation_table.setAlternatingRowColors(True)
        left_panel.addWidget(self.simulation_table)
        
        # Sonuç etiketi
        self.result_label = QLabel("İfadeyi kontrol edin")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(STYLES['result_waiting'])
        self.result_label.setMinimumHeight(60)
        left_panel.addWidget(self.result_label)
        
        # Sağ taraf - Stack görselleştirme
        right_panel = QVBoxLayout()
        
        # Stack başlığı
        stack_header = QLabel("Stack Durumu")
        stack_header.setStyleSheet(STYLES['header'])
        right_panel.addWidget(stack_header)
        
        # Stack listesi
        self.stack_list = QListWidget()
        self.stack_list.setStyleSheet(STYLES['stack_list'])
        self.stack_list.setFlow(QListWidget.TopToBottom)
        self.stack_list.setSpacing(5)
        right_panel.addWidget(self.stack_list)
        
        # Panelleri düzenle
        middle_widget = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        
        middle_widget.addWidget(left_widget)
        middle_widget.addWidget(right_widget)
        middle_widget.setSizes([600, 400])
        
        # Alt bölüm - Geçmiş
        bottom_layout = QVBoxLayout()
        
        # Geçmiş başlığı
        history_header = QLabel("Geçmiş")
        history_header.setStyleSheet(STYLES['header'])
        bottom_layout.addWidget(history_header)
        
        # Geçmiş tablosu
        self.history_table = QTableWidget(0, 3)
        self.history_table.setHorizontalHeaderLabels(["İfade", "Sonuç", "Tarih"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setStyleSheet(STYLES['table'])
        self.history_table.setAlternatingRowColors(True)
        bottom_layout.addWidget(self.history_table)
        
        # Ana layout'a tüm bölümleri ekle
        main_layout.addLayout(input_layout)
        main_layout.addWidget(middle_widget, 3)
        main_layout.addLayout(bottom_layout, 1)
        
        self.setCentralWidget(main_widget)
        
    def check_expression(self):
        """İfadeyi kontrol et ve sonucu göster"""
        expression = self.expression_input.text().strip()
        if not expression:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir matematiksel ifade girin!")
            return
        
        # İfadeyi simüle et ve sonuçları göster
        self.simulation_results, final_valid = self.pda.simulate_step_by_step(expression)
        self.update_simulation_table()  # Simülasyon tablosunu güncelle
        self.show_result(expression, final_valid)
        
        # Geçmişe ekle
        from datetime import datetime
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.history.append({
            'expression': expression,
            'valid': final_valid,
            'date': now
        })
        self.update_history_table()
    
    def update_simulation_table(self):
        """Simülasyon tablosunu güncelle"""
        if not self.simulation_results:
            return
            
        # Tabloyu temizle ve yeni satırları ekle
        self.simulation_table.setRowCount(len(self.simulation_results))
        
        # Tüm adımları tabloya ekle
        for i, step_data in enumerate(self.simulation_results):
            for col, value in enumerate([
                step_data['index'], 
                step_data['char'], 
                step_data['state'], 
                self.pda.get_state_description(step_data['state']),
                "✓" if step_data['valid'] else "✗"
            ]):
                item = QTableWidgetItem(str(value))
                if col == 4:  # Geçerli sütunu
                    if value == "✓":
                        item.setForeground(QColor('green'))
                    else:
                        item.setForeground(QColor('red'))
                item.setTextAlignment(Qt.AlignCenter)
                self.simulation_table.setItem(i, col, item)
        
        # Son stack durumunu göster
        if self.simulation_results:
            last_step = self.simulation_results[-1]
            self.update_stack_visualization(last_step['stack'])
    
    def show_result(self, expression, valid):
        """Sonucu görsel olarak göster"""
        if valid:
            self.result_label.setText(f"İfade geçerli: {expression}")
            self.result_label.setStyleSheet(STYLES['result_valid'])
        else:
            self.result_label.setText(f"İfade geçersiz: {expression}")
            self.result_label.setStyleSheet(STYLES['result_invalid'])
    
    def start_animation(self):
        """Adım adım simülasyonu başlat"""
        expression = self.expression_input.text().strip()
        if not expression:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir matematiksel ifade girin!")
            return
        
        self.simulation_results, final_valid = self.pda.simulate_step_by_step(expression)
        self.current_step = -1
        
        # Simülasyon tablosunu hazırla
        self.simulation_table.setRowCount(len(self.simulation_results))
        
        # Butonları güncelle
        self.next_step_button.setEnabled(True)
        self.start_animation_button.setEnabled(False)
        
        # İlk adımı göster
        self.next_step()
    
    def next_step(self):
        """Simülasyonun bir sonraki adımını göster"""
        if not self.simulation_results or self.current_step >= len(self.simulation_results) - 1:
            # Simülasyon tamamlandı
            if self.simulation_results:
                expression = self.expression_input.text().strip()
                final_valid = self.pda.is_accepted(expression)
                self.show_result(expression, final_valid)
            self.next_step_button.setEnabled(False)
            self.start_animation_button.setEnabled(True)
            return
        
        self.current_step += 1
        step_data = self.simulation_results[self.current_step]
        
        # Tabloyu güncelle
        for col, value in enumerate([
            step_data['index'], 
            step_data['char'], 
            step_data['state'], 
            self.pda.get_state_description(step_data['state']),
            "✓" if step_data['valid'] else "✗"
        ]):
            item = QTableWidgetItem(str(value))
            if col == 4:  # Geçerli sütunu
                if value == "✓":
                    item.setForeground(QColor('green'))
                else:
                    item.setForeground(QColor('red'))
            item.setTextAlignment(Qt.AlignCenter)
            self.simulation_table.setItem(step_data['index'], col, item)
        
        # Mevcut satırı vurgula
        self.simulation_table.selectRow(step_data['index'])
        self.simulation_table.scrollToItem(self.simulation_table.item(step_data['index'], 0))
        
        # Stack'i güncelle
        self.update_stack_visualization(step_data['stack'])
        
        # Durum red ise sonucu göster
        if step_data['state'] == 'rejected':
            expression = self.expression_input.text().strip()
            self.show_result(expression, False)
            self.next_step_button.setEnabled(False)
            self.start_animation_button.setEnabled(True)
        
        # Son adım ise sonucu göster
        elif self.current_step == len(self.simulation_results) - 1:
            expression = self.expression_input.text().strip()
            final_valid = self.pda.is_accepted(expression)
            self.show_result(expression, final_valid)
    
    def update_stack_visualization(self, stack):
        """Stack'in görsel temsilini güncelle"""
        self.stack_list.clear()
        
        if not stack:
            empty_item = QListWidgetItem("[ Boş ]")
            empty_item.setTextAlignment(Qt.AlignCenter)
            empty_item.setForeground(QColor('gray'))
            self.stack_list.addItem(empty_item)
            return
        
        # Stack'in üstünden (sondan) başlayarak ekle
        for i, item_value in enumerate(reversed(stack)):
            item = QListWidgetItem(item_value)
            item.setTextAlignment(Qt.AlignCenter)
            
            # Stack derinliğine göre stil uygula
            item_style = get_stack_item_style(i, len(stack))
            item.setBackground(QColor(item_style['bg_color']))
            item.setForeground(QColor(item_style['text_color']))
            
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            item.setFont(font)
            
            self.stack_list.addItem(item)
    
    def update_history_table(self):
        """Geçmiş tablosunu güncelle"""
        self.history_table.setRowCount(len(self.history))
        
        for row, entry in enumerate(reversed(self.history)):  # En son giriş en üstte
            # İfade
            expr_item = QTableWidgetItem(entry['expression'])
            expr_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 0, expr_item)
            
            # Sonuç
            result_text = "Geçerli" if entry['valid'] else "Geçersiz"
            result_item = QTableWidgetItem(result_text)
            result_item.setTextAlignment(Qt.AlignCenter)
            if entry['valid']:
                result_item.setForeground(QColor('green'))
            else:
                result_item.setForeground(QColor('red'))
            self.history_table.setItem(row, 1, result_item)
            
            # Tarih
            date_item = QTableWidgetItem(entry['date'])
            date_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 2, date_item)
    
    def reset_simulation(self):
        """Simülasyonu sıfırla"""
        self.simulation_table.setRowCount(0)
        self.stack_list.clear()
        self.result_label.setText("İfadeyi kontrol edin")
        self.result_label.setStyleSheet(STYLES['result_waiting'])
        self.next_step_button.setEnabled(False)
        self.start_animation_button.setEnabled(True)
        self.current_step = -1
        self.simulation_results = None