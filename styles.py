"""
Stil tanımlamaları için modül
"""

# Ana renkler
PRIMARY_COLOR = "#2c3e50"  # Koyu mavi
SECONDARY_COLOR = "#3498db"  # Mavi
ACCENT_COLOR = "#e74c3c"  # Kırmızı
SUCCESS_COLOR = "#2ecc71"  # Yeşil
WARNING_COLOR = "#f39c12"  # Turuncu
BACKGROUND_COLOR = "#ecf0f1"  # Açık gri
TEXT_COLOR = "#2c3e50"  # Koyu mavi

# Stil tanımlamaları
STYLES = {
    'button': f"""
        QPushButton {{
            background-color: {SECONDARY_COLOR};
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #2980b9;
        }}
        QPushButton:pressed {{
            background-color: #1f618d;
        }}
        QPushButton:disabled {{
            background-color: #95a5a6;
        }}
    """,
    
    'input': f"""
        QLineEdit {{
            border: 2px solid {SECONDARY_COLOR};
            border-radius: 4px;
            padding: 8px;
            background-color: white;
            selection-background-color: {SECONDARY_COLOR};
        }}
        QLineEdit:focus {{
            border: 2px solid #1abc9c;
        }}
    """,
    
    'header': f"""
        QLabel {{
            color: {PRIMARY_COLOR};
            font-size: 16px;
            font-weight: bold;
            padding: 5px;
            border-bottom: 2px solid {SECONDARY_COLOR};
        }}
    """,
    
    'table': f"""
        QTableWidget {{
            background-color: white;
            alternate-background-color: {BACKGROUND_COLOR};
            border: 1px solid #d1d1d1;
            gridline-color: #f0f0f0;
        }}
        QTableWidget::item {{
            padding: 5px;
        }}
        QTableWidget::item:selected {{
            background-color: {SECONDARY_COLOR};
            color: white;
        }}
        QHeaderView::section {{
            background-color: {PRIMARY_COLOR};
            color: white;
            padding: 5px;
            border: 1px solid #1a2530;
        }}
    """,
    
    'result_valid': f"""
        QLabel {{
            background-color: {SUCCESS_COLOR};
            color: white;
            border-radius: 4px;
            font-weight: bold;
            padding: 10px;
            font-size: 14px;
        }}
    """,
    
    'result_invalid': f"""
        QLabel {{
            background-color: {ACCENT_COLOR};
            color: white;
            border-radius: 4px;
            font-weight: bold;
            padding: 10px;
            font-size: 14px;
        }}
    """,
    
    'result_waiting': f"""
        QLabel {{
            background-color: {WARNING_COLOR};
            color: white;
            border-radius: 4px;
            font-weight: bold;
            padding: 10px;
            font-size: 14px;
        }}
    """,
    
    'stack_list': f"""
        QListWidget {{
            background-color: #f9f9f9;
            border: 1px solid #d1d1d1;
            border-radius: 4px;
        }}
        QListWidget::item {{
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            margin: 3px;
            min-height: 30px;
        }}
    """
}

def get_stack_item_style(index, total):
    """Stack item için derinliğe göre stil döndürür"""
    # Mavi tonlarından başlayıp turkuaza doğru geçiş
    colors = [
        {"bg_color": "#3498db", "text_color": "white"},  # Mavi (en üst)
        {"bg_color": "#2980b9", "text_color": "white"},
        {"bg_color": "#2471a3", "text_color": "white"},
        {"bg_color": "#1f618d", "text_color": "white"},
        {"bg_color": "#1a5276", "text_color": "white"},
        {"bg_color": "#154360", "text_color": "white"},
        {"bg_color": "#0e2f44", "text_color": "white"},  # Koyu mavi (en alt)
    ]
    
    # Index'e göre renk seç (en fazla 7 farklı renk)
    color_index = min(index, len(colors) - 1)
    return colors[color_index]