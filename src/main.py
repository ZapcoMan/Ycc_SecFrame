import sys
import os
import sys
import json
import time

# 获取资源路径
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), relative_path)
# 尝试导入win32com.client用于解析Windows快捷方式
try:
    import win32com.client
    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False

# 尝试导入win32gui和win32con用于获取图标
try:
    import win32gui
    import win32con
    HAS_WIN32GUI = True
except ImportError:
    HAS_WIN32GUI = False
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QFrame, QInputDialog, QMenu, QAction, QMessageBox, QGridLayout, QScrollArea, QFileIconProvider
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QFileInfo, QEvent
from PyQt5.QtGui import QIcon, QFont, QLinearGradient, QPalette, QBrush, QColor, QPixmap

class DudeSuiteApp(QMainWindow):
    _ui_initialized = False  # 类级别的静态变量
    _instance_count = 0  # 实例计数器
    
    def __init__(self):
        super().__init__()
        DudeSuiteApp._instance_count += 1
        self.instance_id = DudeSuiteApp._instance_count
        print(f'创建新实例 #{self.instance_id}, 当前_ui_initialized: {DudeSuiteApp._ui_initialized}')
        self.nav_items = []  # 存储导航项
        self.nav_icons = {
            'home': '🏠',
            'request_test': '🔍',
            'vulnerability_test': '⚠️',
            'packet_capture': '📡',
            'port_scan': '🔌',
            'password_crack': '🔑',
            'remote_management': '🖥️',
            'security_tools': '🛡️',
            'system_settings': '⚙️',
            'authenticated_user': '👤'
        }
        print('在__init__中调用load_categories')
        self.load_categories()  # 加载分类数据
        print(f'实例 #{self.instance_id} 准备调用init_ui, 当前_ui_initialized: {DudeSuiteApp._ui_initialized}')
        if not DudeSuiteApp._ui_initialized:
            self.init_ui()
        self.setWindowTitle('Ycc_SecFrame 框架')
        self.setGeometry(100, 100, 1000, 600)
        
        # 设置窗口图标
        logo_path = resource_path('resources/Logo.png')
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        
        # 设置全局样式
        self.setStyleSheet('''
            QMainWindow, QWidget {
                background-color: #121212;
                color: #e0e0e0;
            }
        ''')
        
        # 创建渐变背景
        self.set_gradient_background()
        
        # 添加窗口阴影效果
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouse_move_event(self, event):
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouse_release_event(self, event):
        self.dragging = False

    def set_gradient_background(self):
        # 创建渐变背景
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(18, 18, 18))
        gradient.setColorAt(1.0, QColor(30, 30, 30))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def init_ui(self):
        print(f'实例 #{self.instance_id} 进入init_ui, 当前_ui_initialized: {DudeSuiteApp._ui_initialized}')
        if DudeSuiteApp._ui_initialized:
            print('UI已经初始化，跳过')
            return
        
        import traceback
        print(f'开始执行init_ui, 调用栈: {traceback.extract_stack()[-2]}')
        # 创建主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 创建标题栏
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar.setStyleSheet('background-color: #1e1e1e; border-radius: 8px;')

        # 标题栏标题
        title_label = QLabel('Ycc_SecFrame 框架')
        title_label.setStyleSheet('font-size: 14px; font-weight: bold; color: #4da6ff;')
        title_label.setAlignment(Qt.AlignCenter)  # 确保标题文本水平和垂直居中

        # 创建一个水平布局来放置标题，确保它居中对齐
        logo_title_layout = QHBoxLayout()
        logo_title_layout.setAlignment(Qt.AlignCenter)
        logo_title_layout.addWidget(title_label)

        # 标题栏按钮
        close_btn = QPushButton('×')
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet('''
            QPushButton {
                background-color: #ff5252; 
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff7979;
            }
        ''')
        close_btn.clicked.connect(self.close)

        minimize_btn = QPushButton('−')
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet('''
            QPushButton {
                background-color: #feca57; 
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffda79;
            }
        ''')
        minimize_btn.clicked.connect(self.showMinimized)

        # 添加到标题栏布局 - 前后添加伸缩项使Logo和标题水平居中
        title_bar_layout.addStretch(1)
        title_bar_layout.addLayout(logo_title_layout)
        title_bar_layout.addStretch(1)
        title_bar_layout.addWidget(minimize_btn)
        title_bar_layout.addWidget(close_btn)

        # 添加标题栏到主布局
        main_layout.addWidget(title_bar)

        # 窗口移动相关变量
        self.dragging = False
        self.drag_position = None

        # 为标题栏添加鼠标事件
        title_bar.mousePressEvent = self.mouse_press_event
        title_bar.mouseMoveEvent = self.mouse_move_event
        title_bar.mouseReleaseEvent = self.mouse_release_event

        # 创建内容区域布局
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        # 创建左侧导航菜单
        self.nav_menu = QListWidget()
        self.nav_menu.setFixedWidth(200)
        self.nav_menu.setStyleSheet('''
            QListWidget {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 10px 0;
                border: 1px solid #2d2d2d;
            }
            QListWidgetItem {
                height: 48px;
                padding: 8px 20px;
                border-radius: 6px;
                margin: 3px 10px;
                transition: all 0.3s ease;
                border-left: 3px solid transparent;
            }
            QListWidgetItem:hover {
                background-color: #252525;
                transform: translateX(5px);
                border-left: 3px solid #4da6ff;
            }
            QListWidgetItem:selected {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4da6ff, stop:1 #0077ff);
                color: white;
                font-weight: bold;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transform: translateX(3px);
                border-left: 3px solid #ffffff;
            }
            QListWidget::item:selected:!active {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3a86ff, stop:1 #0056b3);
            }
            QListWidget::item:selected:active {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4da6ff, stop:1 #0077ff);
            }
        ''')

        # 导航项图标字典已在__init__方法中初始化

        # 先清空导航菜单
        self.nav_menu.clear()
        print('清空导航菜单')

        # 添加加号按钮作为第一个导航项
        plus_item = QListWidgetItem('➕  添加分类')
        print('添加加号按钮')
        plus_item.setData(Qt.UserRole, 'add_category')
        plus_item.setFlags(plus_item.flags() | Qt.ItemIsEditable)
        font = QFont()
        font.setPointSize(10)
        plus_item.setFont(font)
        self.nav_menu.addItem(plus_item)
        
        # 然后添加所有保存的分类项
        if not hasattr(self, 'categories_added') or not self.categories_added:
            print(f'开始添加保存的分类项，当前时间戳: {time.time()}, 顺序: {self.nav_items}')
            print(f'分类项数量: {len(self.nav_items)}')
            
            # 获取当前导航菜单中的所有项文本
            existing_items = []
            for i in range(self.nav_menu.count()):
                item = self.nav_menu.item(i)
                existing_items.append(item.text())
            
            for i, (text, icon_name) in enumerate(self.nav_items):
                # 创建带有图标的导航项文本
                icon = self.nav_icons.get(icon_name, '')
                item_text = f'{icon}  {text}'
                
                # 检查该项是否已存在
                if item_text not in existing_items:
                    print(f'添加第 {i+1} 个分类项: {text}')
                    item = QListWidgetItem(item_text)
                    item.setData(Qt.UserRole, icon_name)
                    
                    # 设置字体和对齐方式
                    font = QFont()
                    font.setPointSize(10)
                    item.setFont(font)
                    
                    self.nav_menu.addItem(item)
                    print(f'已添加分类项: {text}')
                    existing_items.append(item_text)
                else:
                    print(f'分类项 {text} 已存在，跳过')
            
            self.categories_added = True
        else:
            print('分类项已经添加过，跳过')

        # 默认选择第一个项
        self.nav_menu.setCurrentRow(0)
        print('完成添加所有分类项')
        print('init_ui执行完毕')
        
        DudeSuiteApp._ui_initialized = True  # 设置标志为True
        print('UI初始化完成')

        # 连接导航项点击信号
        self.nav_menu.itemClicked.connect(self.on_nav_item_clicked)
        # 连接导航项移动信号
        self.nav_menu.model().rowsMoved.connect(self.on_rows_moved)

        # 设置导航菜单支持拖拽
        self.nav_menu.setDragEnabled(True)
        self.nav_menu.setAcceptDrops(True)
        self.nav_menu.setDropIndicatorShown(True)
        self.nav_menu.setDragDropMode(QListWidget.DragDrop)
        # 安装事件过滤器来处理拖放事件
        self.nav_menu.installEventFilter(self)
        
        # 启用右键菜单
        self.nav_menu.setContextMenuPolicy(Qt.CustomContextMenu)
        self.nav_menu.customContextMenuRequested.connect(self.show_context_menu)
        
        # 确保导航菜单接受拖放
        self.nav_menu.setAcceptDrops(True)
        
        # 初始化快捷方式数据
        self.shortcuts = {}  # 存储分类ID到快捷方式列表的映射
        self.load_shortcuts()  # 加载快捷方式数据

        # 创建主内容区域
        self.content_area = QWidget()
        self.content_area.setStyleSheet('background-color: #1e1e1e; border-radius: 8px;')
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        # 创建内容框架
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet('background-color: #252525; border-radius: 8px;')
        self.content_frame_layout = QVBoxLayout(self.content_frame)
        self.content_frame_layout.setContentsMargins(0, 0, 0, 0)

        # 添加内容框架到内容区域
        self.content_layout.addWidget(self.content_frame)

        # 创建首页内容
        self.create_home_page()

        # 添加导航菜单和内容区域到内容布局
        content_layout.addWidget(self.nav_menu)
        content_layout.addWidget(self.content_area, 1)

        # 添加内容布局到主布局
        main_layout.addLayout(content_layout, 1)

        self.setCentralWidget(main_widget)

    def create_software_description_page(self):
        # 清空内容框架
        while self.content_frame_layout.count() > 0:
            item = self.content_frame_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()
                self.content_frame_layout.removeWidget(widget)

        # 创建软件说明页面
        description_widget = QWidget()
        description_widget.setStyleSheet('background-color: #1a1a1a; border-radius: 10px;')
        description_layout = QVBoxLayout(description_widget)
        description_layout.setContentsMargins(50, 30, 50, 30)

        # 添加标题
        title_label = QLabel('软件说明')
        title_label.setStyleSheet('''
            font-size: 28px; 
            font-weight: bold;
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4da6ff, stop:1 #0077ff);
            margin-bottom: 30px;
            padding: 10px 0;
            border-bottom: 1px solid rgba(77, 166, 255, 0.3);
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        description_layout.addWidget(title_label)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet('background-color: transparent; border: none;')

        # 创建内容 widget
        content_widget = QWidget()
        content_widget.setStyleSheet('background-color: transparent;')
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setSpacing(15)

        # 添加软件说明内容
        # 项目简介
        section_label = QLabel('📋 项目简介')
        section_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #4da6ff; margin-top: 20px;')
        content_layout.addWidget(section_label)

        content_frame = QFrame()
        content_frame.setStyleSheet('background-color: #252525; border-radius: 8px; padding: 15px;')
        content_frame_layout = QVBoxLayout(content_frame)
        
        content_label = QLabel('Ycc_SecFrame 框架是一个可以集成多种工具的管理平台，旨在提供便捷的安全测试和工具管理功能。通过本平台，用户可以轻松添加、组织和启动各种安全工具，提高工作效率。')
        content_label.setStyleSheet('font-size: 14px; color: #ddd; line-height: 1.6;')
        content_label.setWordWrap(True)
        content_frame_layout.addWidget(content_label)
        
        content_layout.addWidget(content_frame)

        # 软件信息
        section_label = QLabel('📝 软件信息')
        section_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #4da6ff; margin-top: 20px;')
        content_layout.addWidget(section_label)
        
        info_frame = QFrame()
        info_frame.setStyleSheet('background-color: #252525; border-radius: 8px; padding: 15px;')
        info_frame_layout = QVBoxLayout(info_frame)
        info_frame_layout.setSpacing(10)
        
        software_info = [
            ('🏷️ 软件名称', 'Ycc_SecFrame 框架'),
            ('👨‍💻 开发者', '杨CC'),
            ('🔢 版本号', '1.0.0.1'),
            ('🔗 GitHub地址', 'https://github.com/Sgyling/Ycc_SecFrame'),
            ('🌐 官网地址', 'https://Yancy77.cn')
        ]
        for icon, text in software_info:
            info_layout = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet('font-size: 14px; color: #4da6ff; min-width: 80px;')
            
            if 'GitHub地址' in icon or '官网地址' in icon:
                text_label = QLabel(f'<a href="{text}">{text}</a>')
                text_label.setTextFormat(Qt.RichText)
                text_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)
                text_label.setOpenExternalLinks(True)
                text_label.setStyleSheet('font-size: 14px; color: #4da6ff; text-decoration: none;')
            else:
                text_label = QLabel(text)
                text_label.setStyleSheet('font-size: 14px; color: #ddd;')
            
            info_layout.addWidget(icon_label)
            info_layout.addWidget(text_label)
            info_frame_layout.addLayout(info_layout)
        
        content_layout.addWidget(info_frame)
        
        # 添加Logo
        logo_frame = QFrame()
        logo_frame.setStyleSheet('background-color: #252525; border-radius: 8px; padding: 20px; margin-top: 15px;')
        logo_frame_layout = QHBoxLayout(logo_frame)
        logo_frame_layout.setAlignment(Qt.AlignCenter)
        
        logo_label = QLabel()
        logo_path = resource_path('resources/Logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        
        logo_frame_layout.addWidget(logo_label)
        content_layout.addWidget(logo_frame)
        
        # 主要功能
        section_label = QLabel('🚀 主要功能')
        section_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #4da6ff; margin-top: 20px;')
        content_layout.addWidget(section_label)

        features_frame = QFrame()
        features_frame.setStyleSheet('background-color: #252525; border-radius: 8px; padding: 15px;')
        features_frame_layout = QVBoxLayout(features_frame)
        features_frame_layout.setSpacing(10)

        features = [
            ('🔍 请求测试', '对目标URL发送各种HTTP请求，测试其响应'),
            ('⚠️ 漏洞验证', '验证目标系统是否存在特定漏洞'),
            ('📡 抓包劫持', '捕获和分析网络数据包'),
            ('🔌 端口扫描', '扫描目标主机开放的端口'),
            ('🔑 密码爆破', '尝试破解密码保护的系统或服务'),
            ('🖥️ 远程管理', '远程连接和管理目标系统'),
            ('🧰 安全工具', '集成各种实用的安全工具'),
            ('🔒 核心原理', '其实这只是个框架,需要自己拖入应用')
        ]
        for icon, text in features:
            feature_layout = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet('font-size: 14px; color: #4da6ff; min-width: 80px;')
            text_label = QLabel(text)
            text_label.setStyleSheet('font-size: 14px; color: #ddd;')
            text_label.setWordWrap(True)
            feature_layout.addWidget(icon_label)
            feature_layout.addWidget(text_label)
            features_frame_layout.addLayout(feature_layout)
        
        content_layout.addWidget(features_frame)

        # 使用指南
        section_label = QLabel('📚 使用指南')
        section_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #4da6ff; margin-top: 20px;')
        content_layout.addWidget(section_label)

        guides_frame = QFrame()
        guides_frame.setStyleSheet('background-color: #252525; border-radius: 8px; padding: 15px;')
        guides_frame_layout = QVBoxLayout(guides_frame)
        guides_frame_layout.setSpacing(10)

        guides = [
            ('➕ 添加工具', '将工具快捷方式拖放到相应分类下'),
            ('📁 创建分类', '点击左侧导航栏顶部的"+"按钮添加新分类'),
            ('✏️ 重命名分类', '右键点击分类，选择"重命名分类"'),
            ('🗑️ 删除分类', '右键点击分类，选择"删除分类"'),
            ('▶️ 启动工具', '点击工具图标启动相应工具')
        ]
        for icon, text in guides:
            guide_layout = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet('font-size: 14px; color: #4da6ff; min-width: 80px;')
            text_label = QLabel(text)
            text_label.setStyleSheet('font-size: 14px; color: #ddd;')
            text_label.setWordWrap(True)
            guide_layout.addWidget(icon_label)
            guide_layout.addWidget(text_label)
            guides_frame_layout.addLayout(guide_layout)
        
        content_layout.addWidget(guides_frame)

        # 注意事项
        section_label = QLabel('⚠️ 注意事项')
        section_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #ff6b6b; margin-top: 20px;')
        content_layout.addWidget(section_label)

        notes_frame = QFrame()
        notes_frame.setStyleSheet('background-color: rgba(255, 107, 107, 0.1); border: 1px solid rgba(255, 107, 107, 0.3); border-radius: 8px; padding: 15px;')
        notes_frame_layout = QVBoxLayout(notes_frame)
        notes_frame_layout.setSpacing(10)

        notes = [
            ('🚨 法律声明', '本工具仅供安全测试和学习使用，请勿用于非法用途'),
            ('🔒 权限要求', '使用前请确保您有权测试目标系统'),
            ('📌 分类限制', '软件说明分类无法重命名、删除和移动'),
            ('🗑️ 工具管理', '右键点击工具可以删除工具')
        ]
        for icon, text in notes:
            note_layout = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet('font-size: 14px; color: #ff6b6b; min-width: 80px;')
            text_label = QLabel(text)
            text_label.setStyleSheet('font-size: 14px; color: #ddd;')
            text_label.setWordWrap(True)
            note_layout.addWidget(icon_label)
            note_layout.addWidget(text_label)
            notes_frame_layout.addLayout(note_layout)
        
        content_layout.addWidget(notes_frame)

        # 支持开发者
        section_label = QLabel('### 支持开发者')
        section_label.setStyleSheet('font-size: 18px; font-weight: bold; color: #4da6ff; margin-top: 15px;')
        content_layout.addWidget(section_label)
        
        # 创建二维码容器
        qr_container = QWidget()
        qr_layout = QHBoxLayout(qr_container)
        qr_layout.setAlignment(Qt.AlignCenter)
        qr_layout.setSpacing(40)
        
        # 微信支付
        wx_label = QLabel()
        wx_path = resource_path('resources/wx.jpg')
        if os.path.exists(wx_path):
            pixmap = QPixmap(wx_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            wx_label.setPixmap(pixmap)
        wx_text = QLabel('微信支付')
        wx_text.setStyleSheet('font-size: 14px; color: #ddd;')
        wx_text.setAlignment(Qt.AlignCenter)
        wx_vbox = QVBoxLayout()
        wx_vbox.addWidget(wx_label)
        wx_vbox.addWidget(wx_text)
        qr_layout.addLayout(wx_vbox)
        
        # 支付宝支付
        zfb_label = QLabel()
        zfb_path = resource_path('resources/zfb.jpg')
        if os.path.exists(zfb_path):
            pixmap = QPixmap(zfb_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            zfb_label.setPixmap(pixmap)
        zfb_text = QLabel('支付宝支付')
        zfb_text.setStyleSheet('font-size: 14px; color: #ddd;')
        zfb_text.setAlignment(Qt.AlignCenter)
        zfb_vbox = QVBoxLayout()
        zfb_vbox.addWidget(zfb_label)
        zfb_vbox.addWidget(zfb_text)
        qr_layout.addLayout(zfb_vbox)
        
        content_layout.addWidget(qr_container)

        scroll_area.setWidget(content_widget)
        description_layout.addWidget(scroll_area, 1)

        # 添加到内容框架
        self.content_frame_layout.addWidget(description_widget)
        description_widget.show()

        # 添加淡入动画效果
        self.animate_widget(description_widget)

    def create_home_page(self):
        # 清空内容框架
        while self.content_frame_layout.count() > 0:
            item = self.content_frame_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()
                self.content_frame_layout.removeWidget(widget)

        # 创建首页部件
        home_widget = QWidget()
        home_widget.setStyleSheet('background-color: transparent;')
        home_layout = QVBoxLayout(home_widget)
        home_layout.setAlignment(Qt.AlignCenter)
        home_layout.setContentsMargins(50, 50, 50, 50)

        # 添加标题
        # 添加标题
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(15)

        # 添加Logo
        logo_label = QLabel()
        logo_path = resource_path('resources/Logo.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        title_layout.addWidget(logo_label)

        # 添加标题文本
        title_text_label = QLabel('Ycc_SecFrame 框架')
        title_text_label.setStyleSheet('''
            font-size: 32px;
            font-weight: bold;
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4da6ff, stop:1 #0077ff);
        ''')
        title_layout.addWidget(title_text_label)

        home_layout.addWidget(title_container)
        title_container.setStyleSheet('margin-bottom: 15px;')

        # 添加版本信息
        version_label = QLabel('Version 1.0.0.1 - 杨CC')
        version_label.setStyleSheet('font-size: 14px; color: #888; margin-bottom: 40px;')
        version_label.setAlignment(Qt.AlignCenter)

        # 添加功能简介卡片
        features_frame = QFrame()
        features_frame.setStyleSheet('background-color: #1e1e1e; border-radius: 10px;')
        features_layout = QHBoxLayout(features_frame)
        features_layout.setSpacing(20)
        features_layout.setContentsMargins(20, 20, 20, 20)

        # 功能卡片数据
        features = [
            ('安全框架', '📡', '可以拖入不同的工具,进行不同的安全测试'),
            ('安全分类', '🔍', '可以对不同的工具进行分类,支持创建分类'),
            ('工具管理', '📦', '可以对不同的工具进行管理,支持创建分类'),
            ('其他分类', '🔌', '可以对不同的应用进行分类,支持创建分类')
        ]

        for title, icon, desc in features:
            # 创建功能卡片
            card = QFrame()
            card.setStyleSheet('background-color: #252525; border-radius: 8px;')
            card.setMinimumHeight(150)
            card.setMinimumWidth(180)  # 设置最小宽度确保标题能显示
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 15, 15, 15)
            card_layout.setAlignment(Qt.AlignCenter)

            # 卡片图标
            icon_label = QLabel(icon)
            icon_label.setStyleSheet('font-size: 32px; color: #4da6ff; margin-bottom: 10px;')
            icon_label.setAlignment(Qt.AlignCenter)

            # 卡片标题
            card_title_label = QLabel(title)
            card_title_label.setStyleSheet('font-size: 16px; font-weight: bold; color: white; margin-bottom: 5px;')
            card_title_label.setAlignment(Qt.AlignCenter)

            # 卡片描述
            desc_label = QLabel(desc)
            desc_label.setStyleSheet('font-size: 12px; color: #aaa;')
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)

            # 添加到卡片布局
            card_layout.addWidget(icon_label)
            card_layout.addWidget(card_title_label)
            card_layout.addWidget(desc_label)

            # 添加到功能布局
            features_layout.addWidget(card)

        # 添加警告信息
        # 创建包含链接的警告标签
        warning_text = '本软件只是一个框架，需要自己拖入工具。\n \n 总而言之，这只是个框架。\n \n <a href="https://yancy77.cn" style="color: #4da6ff; text-decoration: none;">访问官方网站: https://yancy77.cn</a>'
        warning_label = QLabel(warning_text)
        warning_label.setStyleSheet('font-size: 12px; color: #ff6b6b; margin-top: 40px;')
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setWordWrap(True)
        warning_label.setTextFormat(Qt.RichText)
        warning_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)
        warning_label.setOpenExternalLinks(True)

        # 添加到布局
        home_layout.addWidget(version_label)
        home_layout.addWidget(features_frame)
        home_layout.addWidget(warning_label)

        # 添加到内容框架
        self.content_frame_layout.addWidget(home_widget)
        home_widget.show()

        # 添加淡入动画效果
        self.animate_widget(home_widget)

    def on_nav_item_clicked(self, item):
        # 获取点击的导航项数据
        icon_name = item.data(Qt.UserRole)

        # 根据不同的导航项显示不同的内容
        if icon_name == 'home':
            self.create_home_page()
        elif icon_name == 'add_category':
            # 添加新分类的逻辑
            self.add_new_category()
        elif icon_name == 'software_description':
            # 显示软件说明页面
            self.create_software_description_page()
        else:
            # 这里只是一个示例，实际应用中应该为每个导航项创建对应的页面
            self.show_module_page(item.text())

    def add_new_category(self):
        # 创建一个输入对话框来获取新分类名称
        category_name, ok = QInputDialog.getText(self, '添加分类', '请输入新分类名称:')
        if ok and category_name:
            # 为新分类生成唯一ID
            category_id = f'category_{len(self.nav_items) + 1}'
            # 添加新分类到导航菜单
            new_item = QListWidgetItem(f'📌  {category_name}')
            new_item.setData(Qt.UserRole, category_id)
            font = QFont()
            font.setPointSize(10)
            new_item.setFont(font)
            # 添加新分类到导航菜单末尾
            self.nav_menu.addItem(new_item)
            # 更新导航项列表 - 将新分类添加到末尾
            self.nav_items.append((category_name, category_id))
            # 添加新分类图标
            self.nav_icons[category_id] = '📌'
            # 保存分类数据
            self.save_categories()

    def save_categories(self):
        # 保存分类数据到JSON文件
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_path, exist_ok=True)
        categories_file = os.path.join(data_path, 'categories.json')
        with open(categories_file, 'w', encoding='utf-8') as f:
            json.dump(self.nav_items, f, ensure_ascii=False, indent=2)
        print(f'保存分类顺序: {self.nav_items}')

    _categories_loaded = False  # 类级别的静态变量
    
    def load_categories(self):
        if DudeSuiteApp._categories_loaded:
            print('分类数据已经加载，跳过加载')
            return
        
        # 从JSON文件加载分类数据
        import traceback
        print(f'调用load_categories, 调用栈: {traceback.extract_stack()[-2]}')
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        categories_file = os.path.join(data_path, 'categories.json')
        if os.path.exists(categories_file):
            with open(categories_file, 'r', encoding='utf-8') as f:
                self.nav_items = json.load(f)
            print(f'加载分类顺序: {self.nav_items}')
        else:
            # 默认分类数据
            self.nav_items = [
                ('首页', 'home'),
                ('请求测试', 'request_test'),
                ('漏洞验证', 'vulnerability_test'),
                ('抓包劫持', 'packet_capture'),
                ('端口扫描', 'port_scan'),
                ('密码爆破', 'password_crack'),
                ('远程管理', 'remote_management'),
                ('安全工具', 'security_tools'),
                ('软件说明', 'software_description')
            ]
            # 保存默认分类
            self.save_categories()

        # 确保自定义分类图标正确加载
        for name, id in self.nav_items:
            if id.startswith('category_') and id not in self.nav_icons:
                self.nav_icons[id] = '📌'
        
        DudeSuiteApp._categories_loaded = True  # 设置类级别标志为True

    def load_shortcuts(self):
        # 从JSON文件加载快捷方式数据
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        shortcuts_file = os.path.join(data_path, 'shortcuts.json')
        if os.path.exists(shortcuts_file):
            with open(shortcuts_file, 'r', encoding='utf-8') as f:
                self.shortcuts = json.load(f)
        else:
            # 默认快捷方式数据
            self.shortcuts = {}
            # 保存默认快捷方式
            self.save_shortcuts()

    def save_shortcuts(self):
        # 保存快捷方式数据到JSON文件
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(data_path, exist_ok=True)
        shortcuts_file = os.path.join(data_path, 'shortcuts.json')
        with open(shortcuts_file, 'w', encoding='utf-8') as f:
            json.dump(self.shortcuts, f, ensure_ascii=False, indent=2)

    def animate_widget(self, widget):
        # 创建淡入动画
        animation = QPropertyAnimation(widget, b'windowOpacity')
        animation.setDuration(500)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def show_context_menu(self, position):
        # 获取右键点击的项
        item = self.nav_menu.itemAt(position)
        if item and item.data(Qt.UserRole) != 'add_category' and item.data(Qt.UserRole) not in ['home', 'software_description']:
            # 创建右键菜单
            menu = QMenu()
            rename_action = QAction('重命名分类', self)
            rename_action.triggered.connect(lambda: self.rename_category(item))
            delete_action = QAction('删除分类', self)
            delete_action.triggered.connect(lambda: self.delete_category(item))
            menu.addAction(rename_action)
            menu.addAction(delete_action)
            menu.exec_(self.nav_menu.mapToGlobal(position))

    def rename_category(self, item):
        # 获取当前分类名称和ID
        item_text = item.text()
        category_id = item.data(Qt.UserRole)
        
        # 获取分类对应的图标
        icon = self.nav_icons.get(category_id, '')
        
        # 移除图标和后面的空格，获取当前名称
        if icon and item_text.startswith(icon):
            # 移除图标和后面的所有空格
            current_name = item_text[len(icon):].lstrip()
        else:
            current_name = item_text

        # 弹出输入对话框
        new_name, ok = QInputDialog.getText(self, '重命名分类', '请输入新的分类名称:', text=current_name)
        if ok and new_name and new_name != current_name:
            # 更新导航项文本，确保图标和名称之间只有一个空格
            item.setText(f'{icon} {new_name}')

            # 更新导航项数据
            for i, (name, id) in enumerate(self.nav_items):
                if id == category_id:
                    self.nav_items[i] = (new_name, id)
                    break

            # 保存分类数据
            self.save_categories()

    def delete_category(self, item):
        # 获取分类ID
        category_id = item.data(Qt.UserRole)
        category_name = item.text().replace('📁  ', '')
        
        # 从导航项列表中删除
        self.nav_items = [(name, id) for name, id in self.nav_items if id != category_id]
        
        # 从导航菜单中删除
        row = self.nav_menu.row(item)
        self.nav_menu.takeItem(row)
        
        # 删除对应的图标
        if category_id in self.nav_icons:
            del self.nav_icons[category_id]
        
        # 删除对应的快捷方式
        if category_id in self.shortcuts:
            del self.shortcuts[category_id]
            self.save_shortcuts()
        
        # 保存分类数据
        self.save_categories()

    def dragEnterEvent(self, event):
        # 检查拖入的数据是否是文本或URL（快捷方式通常以这些形式表示）
        if event.mimeData().hasText() or event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def eventFilter(self, source, event):
        if source == self.nav_menu and event.type() == QEvent.Drop:
            # 检查是否移动了软件说明分类
            software_description_moved = False
            original_index = -1
            current_index = -1
            for i in range(self.nav_menu.count()):
                item = self.nav_menu.item(i)
                if item.data(Qt.UserRole) == 'software_description':
                    current_index = i
                    # 查找原始位置（最后一次保存的位置）
                    for j, (name, id) in enumerate(self.nav_items):
                        if id == 'software_description':
                            original_index = j
                            break
                    break

            if current_index != -1 and original_index != -1 and current_index != original_index:
                software_description_moved = True

            if not software_description_moved:
                # 拖放事件发生后，更新导航项数据
                self.update_nav_items()
                return True
            else:
                # 恢复软件说明分类的位置
                # 找到软件说明分类项
                software_description_item = None
                for i in range(self.nav_menu.count()):
                    item = self.nav_menu.item(i)
                    if item.data(Qt.UserRole) == 'software_description':
                        software_description_item = item
                        current_index = i
                        break

                if software_description_item and original_index != -1:
                    # 移除软件说明分类项
                    self.nav_menu.takeItem(current_index)
                    # 在原始位置插入软件说明分类项
                    self.nav_menu.insertItem(original_index, software_description_item)
                    # 更新导航项数据
                    self.update_nav_items()
                return False
        return super().eventFilter(source, event)

    def restore_software_description_position(self):
        # 找到软件说明分类项
        software_description_item = None
        current_index = -1
        for i in range(self.nav_menu.count()):
            item = self.nav_menu.item(i)
            if item.data(Qt.UserRole) == 'software_description':
                software_description_item = item
                current_index = i
                break

        if software_description_item and self.original_software_description_index != -1 and current_index != self.original_software_description_index:
            # 移除软件说明分类项
            self.nav_menu.takeItem(current_index)
            # 在原始位置插入软件说明分类项
            self.nav_menu.insertItem(self.original_software_description_index, software_description_item)
            # 更新导航项数据
            self.update_nav_items()

    def update_nav_items(self):
        # 从导航菜单更新self.nav_items数据
        print('开始更新导航项数据')
        new_nav_items = []
        for i in range(self.nav_menu.count()):
            item = self.nav_menu.item(i)
            if item.data(Qt.UserRole) != 'add_category':  # 跳过添加分类按钮
                # 提取文本和图标ID
                text = item.text().replace('📌  ', '').replace('📁  ', '').replace('🏠  ', '').replace('📡  ', '').replace('🔍  ', '').replace('📦  ', '').replace('🔌  ', '').replace('🔑  ', '').replace('🖥️  ', '').replace('🛠️  ', '').replace('⚙️  ', '').replace('👤  ', '').replace('⚠️  ', '').replace('🛡️  ', '')
                icon_id = item.data(Qt.UserRole)
                new_nav_items.append((text, icon_id))
        
        # 更新数据并保存
        print(f'更新后的导航项数据: {new_nav_items}')
        self.nav_items = new_nav_items
        self.save_categories()
        
    def on_rows_moved(self, parent, start, end, destination, row):
        # 当导航项移动时调用此方法
        print(f'分类项移动: 从位置 {start} 到位置 {row}')
        # 更新导航项数据
        self.update_nav_items()

    def launch_shortcut(self, shortcut):
        # 启动快捷方式
        print(f'启动快捷方式: {shortcut}')
        # 这里可以添加实际启动快捷方式的代码
        # 例如，如果是应用程序路径，可以使用os.startfile
        import os
        try:
            os.startfile(shortcut)
        except Exception as e:
            print(f'启动快捷方式失败: {e}')
            # 显示错误消息
            QMessageBox.critical(self, '启动失败', f'无法启动快捷方式: {str(e)}')

    def get_shortcut_icon(self, shortcut_path):
        """获取快捷方式的图标

        Args:
            shortcut_path: 快捷方式文件路径

        Returns:
            QIcon: 快捷方式的图标
        """
        icon = QIcon()
        try:
            # 处理可能的URL格式路径
            if shortcut_path.startswith('file://'):
                # 移除file://前缀
                shortcut_path = shortcut_path[7:]
                # 对于Windows路径，确保路径格式正确
                if shortcut_path.startswith('/'):
                    shortcut_path = shortcut_path[1:]
                shortcut_path = shortcut_path.replace('/', '\\')
                print(f'转换URL路径为本地路径: {shortcut_path}')

            if shortcut_path.lower().endswith('.lnk') and HAS_WIN32COM:
                # 使用win32com.client解析Windows快捷方式
                try:
                    shell = win32com.client.Dispatch('WScript.Shell')
                    lnk = shell.CreateShortcut(shortcut_path)
                    target_path = lnk.TargetPath
                    print(f'快捷方式目标路径: {target_path}')
                    
                    # 确保目标路径不为空
                    if not target_path:
                        print(f'快捷方式目标路径为空: {shortcut_path}')
                        target_path = shortcut_path
                except Exception as e:
                    print(f'解析快捷方式失败: {e}')
                    target_path = shortcut_path
            else:
                target_path = shortcut_path

            # 使用QFileIconProvider获取文件图标
            try:
                file_icon_provider = QFileIconProvider()
                icon = file_icon_provider.icon(QFileInfo(target_path))
                if icon.isNull():
                    print(f'QFileIconProvider无法加载图标: {target_path}')
                    # 使用默认图标
                    if os.path.exists('resources/Logo.png'):
                        icon = QIcon('resources/Logo.png')
                    else:
                        # 使用PyQt5内置图标
                        icon = QIcon.fromTheme('application-x-executable')
            except Exception as e:
                print(f'使用QFileIconProvider获取图标失败: {e}')
                # 使用默认图标
                if os.path.exists('resources/Logo.png'):
                    icon = QIcon('resources/Logo.png')
                else:
                    icon = QIcon.fromTheme('application-x-executable')

            # 检查图标是否有效
            if icon.isNull():
                print(f'QIcon无法加载图标: {shortcut_path}')
                # 使用默认图标
                if os.path.exists('resources/Logo.png'):
                    icon = QIcon('resources/Logo.png')
                else:
                    icon = QIcon.fromTheme('application-x-executable')
        except Exception as e:
            print(f'获取图标失败: {e}')
            # 使用默认图标
            icon = QIcon.fromTheme('application-x-executable')
        return icon

    def delete_shortcut(self, category_id, shortcut):
        # 删除快捷方式
        print(f'删除快捷方式: {shortcut} 从分类: {category_id}')
        if category_id in self.shortcuts and shortcut in self.shortcuts[category_id]:
            # 从列表中移除快捷方式
            self.shortcuts[category_id].remove(shortcut)
            # 保存更改
            self.save_shortcuts()
            # 刷新当前页面
            # 查找当前模块名称
            current_module_name = None
            for text, icon_name in self.nav_items:
                if icon_name == category_id:
                    # 添加图标前缀
                    if category_id in self.nav_icons:
                        current_module_name = f'{self.nav_icons[category_id]}  {text}'
                    else:
                        current_module_name = f'📁  {text}'
                    break
            # 刷新页面
            if current_module_name:
                self.show_module_page(current_module_name)

    def eventFilter(self, source, event):
        # 确保事件来自导航菜单
        if source == self.nav_menu:
            # 处理拖入事件
            if event.type() == QEvent.DragEnter:
                self.dragEnterEvent(event)
                return True
            # 处理拖移事件
            elif event.type() == QEvent.DragMove:
                self.dragMoveEvent(event)
                return True
            # 处理拖放事件
            elif event.type() == QEvent.Drop:
                self.dropEvent(event)
                return True
        # 对于其他事件，使用默认处理
        return super().eventFilter(source, event)
        
    def dragEnterEvent(self, event):
        # 检查拖入的数据类型
        if event.mimeData().hasText() or event.mimeData().hasUrls():
            # 获取当前拖放位置的项
            item = self.nav_menu.itemAt(event.pos())
            if item:
                item_data = item.data(Qt.UserRole)
                # 检查是否是排除的分类
                excluded_categories = ['home', 'software_description', 'add_category']
                
                # 只有非排除的分类才允许拖放
                if item_data not in excluded_categories:
                    event.acceptProposedAction()
                    return
        event.ignore()
        
    def dragMoveEvent(self, event):
        # 检查拖入的数据类型
        if event.mimeData().hasText() or event.mimeData().hasUrls():
            # 获取当前拖放位置的项
            item = self.nav_menu.itemAt(event.pos())
            if item:
                item_data = item.data(Qt.UserRole)
                # 检查是否是排除的分类
                excluded_categories = ['home', 'software_description', 'add_category']
                
                # 只有非排除的分类才允许拖放
                if item_data not in excluded_categories:
                    event.acceptProposedAction()
                    return
        event.ignore()
        
    def dropEvent(self, event):
        # 获取拖入的文本或URL
        shortcut_text = None
        if event.mimeData().hasText():
            shortcut_text = event.mimeData().text()
        elif event.mimeData().hasUrls():
            # 取第一个URL
            shortcut_text = event.mimeData().urls()[0].toString()
            # 如果是本地文件URL，去掉file://前缀
            if shortcut_text.startswith('file:///'):
                shortcut_text = shortcut_text[8:]
            elif shortcut_text.startswith('file://'):
                shortcut_text = shortcut_text[7:]
                # 对于Windows路径，确保路径格式正确
                if shortcut_text.startswith('/'):
                    shortcut_text = shortcut_text[1:]
                shortcut_text = shortcut_text.replace('/', '\\')
        
        # 获取当前拖放位置的项
        item = self.nav_menu.itemAt(event.pos())
        if item and shortcut_text:
            item_data = item.data(Qt.UserRole)
            # 检查是否是排除的分类（没有右键功能的分类）
            excluded_categories = ['home', 'software_description', 'add_category']
            
            # 只有非排除的分类才允许拖放
            if item_data not in excluded_categories:
                category_id = item_data
                
                # 确保分类在快捷方式字典中存在
                if category_id not in self.shortcuts:
                    self.shortcuts[category_id] = []
                
                # 添加快捷方式
                self.shortcuts[category_id].append(shortcut_text)
                
                # 保存快捷方式数据
                self.save_shortcuts()
                
                # 显示成功消息
                QMessageBox.information(self, '添加成功', f'已将快捷方式添加到分类: {item.text()}')
                print(f'已将快捷方式添加到分类: {item.text()}')
        
        super().dropEvent(event)

    def show_module_page(self, module_name):
        # 清空内容框架
        while self.content_frame_layout.count() > 0:
            item = self.content_frame_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()
                self.content_frame_layout.removeWidget(widget)

        # 创建模块页面
        module_widget = QWidget()
        module_widget.setStyleSheet('background-color: transparent;')
        module_widget.setAcceptDrops(True)  # 启用拖放
        module_layout = QVBoxLayout(module_widget)
        module_layout.setAlignment(Qt.AlignTop)
        module_layout.setContentsMargins(20, 20, 20, 20)

        # 重写拖入事件
        def dragEnterEvent(event):
            if event.mimeData().hasText():
                event.acceptProposedAction()

        # 重写拖放事件
        def dropEvent(event):
            if event.mimeData().hasText():
                shortcut_text = event.mimeData().text()
                
                # 获取当前模块ID
                current_module_id = None
                clean_module_name = module_name.replace('📌  ', '').replace('📁  ', '').replace('🏠  ', '').replace('📡  ', '').replace('🔍  ', '').replace('📦  ', '').replace('🔌  ', '').replace('🔑  ', '').replace('🖥️  ', '').replace('🛠️  ', '').replace('⚙️  ', '').replace('👤  ', '').replace('⚠️  ', '').replace('🛡️  ', '')
                
                for text, icon_name in self.nav_items:
                    if text == clean_module_name:
                        current_module_id = icon_name
                        break
                
                # 确保分类在快捷方式字典中存在
                if current_module_id:
                    if current_module_id not in self.shortcuts:
                        self.shortcuts[current_module_id] = []
                    
                    # 添加快捷方式
                    self.shortcuts[current_module_id].append(shortcut_text)
                    
                    # 保存快捷方式数据
                    self.save_shortcuts()
                    
                    # 刷新页面以显示新添加的快捷方式
                    self.show_module_page(module_name)
                    
                    # 显示成功消息
                    print(f'已将快捷方式添加到分类: {module_name}')

        # 绑定事件
        module_widget.dragEnterEvent = dragEnterEvent
        module_widget.dropEvent = dropEvent

        # 模块标题
        title_label = QLabel(module_name)
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #4da6ff; margin-bottom: 20px;')
        module_layout.addWidget(title_label)

        # 查找当前模块的ID
        current_module_id = None
        # 移除模块名称中的图标前缀
        clean_module_name = module_name.replace('📌  ', '').replace('📁  ', '').replace('🏠  ', '').replace('📡  ', '').replace('🔍  ', '').replace('📦  ', '').replace('🔌  ', '').replace('🔑  ', '').replace('🖥️  ', '').replace('🛠️  ', '').replace('⚙️  ', '').replace('👤  ', '').replace('⚠️  ', '').replace('🛡️  ', '')
        
        for text, icon_name in self.nav_items:
            if text == clean_module_name:
                current_module_id = icon_name
                break

        # 添加说明文本
        desc_label = QLabel('杨CC温馨提示~ 将快捷方式拖动到此处，以方便正常使用。')
        desc_label.setStyleSheet('font-size: 16px; color: #4da6ff; margin-bottom: 20px;')
        desc_label.setAlignment(Qt.AlignCenter)
        module_layout.addWidget(desc_label)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet('QScrollArea {background-color: transparent; border: none;}')
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 创建快捷方式容器
        shortcuts_container = QFrame()
        shortcuts_container.setStyleSheet('background-color: #252525; border-radius: 10px; padding: 20px;')
        shortcuts_layout = QGridLayout(shortcuts_container)
        shortcuts_layout.setAlignment(Qt.AlignTop)
        shortcuts_layout.setSpacing(10)

        # 设置滚动区域的widget
        scroll_area.setWidget(shortcuts_container)

        # 显示当前分类的快捷方式
        if current_module_id and current_module_id in self.shortcuts:
            shortcuts = self.shortcuts[current_module_id]
            if shortcuts:
                row = 0
                col = 0
                max_cols = 4  # 每行最多显示4个图标
                for shortcut in shortcuts:
                    # 创建快捷方式卡片
                    shortcut_card = QFrame()
                    shortcut_card.setStyleSheet('background-color: #333; border-radius: 8px; padding: 10px;')
                    shortcut_card.setMinimumWidth(100)
                    shortcut_card.setMinimumHeight(100)
                    shortcut_layout = QVBoxLayout(shortcut_card)
                    shortcut_layout.setAlignment(Qt.AlignCenter)
                    shortcut_layout.setSpacing(5)

                    # 提取快捷方式名称（去掉路径和扩展名）
                    shortcut_name = os.path.splitext(os.path.basename(shortcut))[0]

                    # 获取快捷方式图标
                    icon = self.get_shortcut_icon(shortcut)

                    # 快捷方式图标
                    icon_label = QLabel()
                    icon_pixmap = icon.pixmap(32, 32)
                    if icon_pixmap.isNull():
                        icon_label.setText('📌')
                        icon_label.setStyleSheet('font-size: 24px; color: #4da6ff;')
                    else:
                        icon_label.setPixmap(icon_pixmap)
                    icon_label.setAlignment(Qt.AlignCenter)

                    # 快捷方式名称
                    name_label = QLabel(shortcut_name)
                    name_label.setStyleSheet('font-size: 12px; color: white;')
                    name_label.setAlignment(Qt.AlignCenter)
                    name_label.setWordWrap(True)

                    # 添加到卡片布局
                    shortcut_layout.addWidget(icon_label)
                    shortcut_layout.addWidget(name_label)

                    # 添加点击事件 - 只响应左键点击
                    def mousePressEvent(event, s=shortcut):
                        if event.button() == Qt.LeftButton:
                            self.launch_shortcut(s)
                        # 对于右键点击，不执行任何操作，让contextMenuEvent处理

                    shortcut_card.mousePressEvent = mousePressEvent

                    # 添加右键菜单
                    def contextMenuEvent(event, s=shortcut, card=shortcut_card):
                        menu = QMenu()
                        delete_action = QAction('删除', self)
                        delete_action.triggered.connect(lambda: self.delete_shortcut(current_module_id, s))
                        menu.addAction(delete_action)
                        menu.exec_(event.globalPos())

                    shortcut_card.contextMenuEvent = contextMenuEvent

                    # 添加到网格布局
                    shortcuts_layout.addWidget(shortcut_card, row, col)
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
            else:
                no_shortcuts_label = QLabel('当前分类没有快捷方式')
                no_shortcuts_label.setStyleSheet('font-size: 14px; color: #888;')
                no_shortcuts_label.setAlignment(Qt.AlignCenter)
                shortcuts_layout.addWidget(no_shortcuts_label)
        else:
            no_shortcuts_label = QLabel('当前分类没有快捷方式')
            no_shortcuts_label.setStyleSheet('font-size: 14px; color: #888;')
            no_shortcuts_label.setAlignment(Qt.AlignCenter)
            shortcuts_layout.addWidget(no_shortcuts_label)

        module_layout.addWidget(scroll_area)

        # 添加返回按钮
        back_btn = QPushButton('返回首页')
        back_btn.setStyleSheet('''
            QPushButton {
                background-color: #4da6ff;
                color: white;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #0077ff;
            }
        ''')
        back_btn.clicked.connect(self.create_home_page)
        module_layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        # 添加到内容框架
        self.content_frame_layout.addWidget(module_widget)
        module_widget.show()

        # 添加淡入动画效果
        self.animate_widget(module_widget)

# 添加win32gui所需的结构体大小函数
import ctypes

def sizeof(struct):
    """获取结构体大小"""
    return ctypes.sizeof(struct)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DudeSuiteApp()
    window.show()
    sys.exit(app.exec_())