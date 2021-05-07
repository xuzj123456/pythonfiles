# coding=utf-8
import csv
from datetime import datetime, timedelta
from copy import copy

import numpy as np
import pyqtgraph as pg

class BacktesterManager(QtWidgets.QWidget):
    """"""

    setting_filename = "cta_backtester_setting.json"

    signal_log = QtCore.pyqtSignal(Event)
    signal_backtesting_finished = QtCore.pyqtSignal(Event)
    signal_optimization_finished = QtCore.pyqtSignal(Event)

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine):
        """"""
        super().__init__()

        self.main_engine = main_engine
        self.event_engine = event_engine

        self.backtester_engine = main_engine.get_engine(APP_NAME)
        self.class_names = []
        self.settings = {}

        self.target_display = ""

        self.init_ui()
        self.register_event()
        self.backtester_engine.init_engine()
        self.init_strategy_settings()
        self.load_backtesting_setting()

    def init_strategy_settings(self):
        """"""
        self.class_names = self.backtester_engine.get_strategy_class_names()

        for class_name in self.class_names:
            setting = self.backtester_engine.get_default_setting(class_name)
            self.settings[class_name] = setting

        self.class_combo.addItems(self.class_names)

    def init_ui(self):
        """"""
        self.setWindowTitle("CTA回测")

        # Setting Part
        self.class_combo = QtWidgets.QComboBox()

        self.symbol_line = QtWidgets.QLineEdit("IF88.CFFEX")

        self.interval_combo = QtWidgets.QComboBox()
        for interval in Interval:
            self.interval_combo.addItem(interval.value)

        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=3 * 365)

        self.start_date_edit = QtWidgets.QDateEdit(
            QtCore.QDate(
                start_dt.year,
                start_dt.month,
                start_dt.day
            )
        )
        self.end_date_edit = QtWidgets.QDateEdit(
            QtCore.QDate.currentDate()
        )

        self.rate_line = QtWidgets.QLineEdit("0.000025")
        self.slippage_line = QtWidgets.QLineEdit("0.2")
        self.size_line = QtWidgets.QLineEdit("300")
        self.pricetick_line = QtWidgets.QLineEdit("0.2")
        self.capital_line = QtWidgets.QLineEdit("1000000")

        self.inverse_combo = QtWidgets.QComboBox()
        self.inverse_combo.addItems(["正向", "反向"])

        backtesting_button = QtWidgets.QPushButton("开始回测")
        backtesting_button.clicked.connect(self.start_backtesting)

        optimization_button = QtWidgets.QPushButton("参数优化")
        optimization_button.clicked.connect(self.start_optimization)

        self.result_button = QtWidgets.QPushButton("优化结果")
        self.result_button.clicked.connect(self.show_optimization_result)
        self.result_button.setEnabled(False)

        downloading_button = QtWidgets.QPushButton("下载数据")
        downloading_button.clicked.connect(self.start_downloading)

        self.order_button = QtWidgets.QPushButton("委托记录")
        self.order_button.clicked.connect(self.show_backtesting_orders)
        self.order_button.setEnabled(False)

        self.trade_button = QtWidgets.QPushButton("成交记录")
        self.trade_button.clicked.connect(self.show_backtesting_trades)
        self.trade_button.setEnabled(False)

        self.daily_button = QtWidgets.QPushButton("每日盈亏")
        self.daily_button.clicked.connect(self.show_daily_results)
        self.daily_button.setEnabled(False)

        self.candle_button = QtWidgets.QPushButton("K线图表")
        self.candle_button.clicked.connect(self.show_candle_chart)
        self.candle_button.setEnabled(False)

        edit_button = QtWidgets.QPushButton("代码编辑")
        edit_button.clicked.connect(self.edit_strategy_code)

        reload_button = QtWidgets.QPushButton("策略重载")
        reload_button.clicked.connect(self.reload_strategy_class)

        for button in [
            backtesting_button,
            optimization_button,
            downloading_button,
            self.result_button,
            self.order_button,
            self.trade_button,
            self.daily_button,
            self.candle_button,
            edit_button,
            reload_button
        ]:
            button.setFixedHeight(button.sizeHint().height() * 2)

        form = QtWidgets.QFormLayout()
        form.addRow("交易策略", self.class_combo)
        form.addRow("本地代码", self.symbol_line)
        form.addRow("K线周期", self.interval_combo)
        form.addRow("开始日期", self.start_date_edit)
        form.addRow("结束日期", self.end_date_edit)
        form.addRow("手续费率", self.rate_line)
        form.addRow("交易滑点", self.slippage_line)
        form.addRow("合约乘数", self.size_line)
        form.addRow("价格跳动", self.pricetick_line)
        form.addRow("回测资金", self.capital_line)
        form.addRow("合约模式", self.inverse_combo)

        result_grid = QtWidgets.QGridLayout()
        result_grid.addWidget(self.trade_button, 0, 0)
        result_grid.addWidget(self.order_button, 0, 1)
        result_grid.addWidget(self.daily_button, 1, 0)
        result_grid.addWidget(self.candle_button, 1, 1)

        left_vbox = QtWidgets.QVBoxLayout()
        left_vbox.addLayout(form)
        left_vbox.addWidget(backtesting_button)
        left_vbox.addWidget(downloading_button)
        left_vbox.addStretch()
        left_vbox.addLayout(result_grid)
        left_vbox.addStretch()
        left_vbox.addWidget(optimization_button)
        left_vbox.addWidget(self.result_button)
        left_vbox.addStretch()
        left_vbox.addWidget(edit_button)
        left_vbox.addWidget(reload_button)

        # Result part
        self.statistics_monitor = StatisticsMonitor()

        self.log_monitor = QtWidgets.QTextEdit()
        self.log_monitor.setMaximumHeight(400)

        self.chart = BacktesterChart()
        self.chart.setMinimumWidth(1000)

        self.trade_dialog = BacktestingResultDialog(
            self.main_engine,
            self.event_engine,
            "回测成交记录",
            BacktestingTradeMonitor
        )
        self.order_dialog = BacktestingResultDialog(
            self.main_engine,
            self.event_engine,
            "回测委托记录",
            BacktestingOrderMonitor
        )
        self.daily_dialog = BacktestingResultDialog(
            self.main_engine,
            self.event_engine,
            "回测每日盈亏",
            DailyResultMonitor
        )

        # Candle Chart
        self.candle_dialog = CandleChartDialog()

        # Layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.statistics_monitor)
        vbox.addWidget(self.log_monitor)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(left_vbox)
        hbox.addLayout(vbox)
        hbox.addWidget(self.chart)
        self.setLayout(hbox)

        # Code Editor
        self.editor = CodeEditor(self.main_engine, self.event_engine)

    def load_backtesting_setting(self):
        """"""
        setting = load_json(self.setting_filename)
        if not setting:
            return

        self.class_combo.setCurrentIndex(
            self.class_combo.findText(setting["class_name"])
        )

        self.symbol_line.setText(setting["vt_symbol"])

        self.interval_combo.setCurrentIndex(
            self.interval_combo.findText(setting["interval"])
        )

        start_str = setting.get("start", "")
        if start_str:
            start_dt = QtCore.QDate.fromString(start_str, "yyyy-MM-dd")
            self.start_date_edit.setDate(start_dt)

        self.rate_line.setText(str(setting["rate"]))
        self.slippage_line.setText(str(setting["slippage"]))
        self.size_line.setText(str(setting["size"]))
        self.pricetick_line.setText(str(setting["pricetick"]))
        self.capital_line.setText(str(setting["capital"]))

        if not setting["inverse"]:
            self.inverse_combo.setCurrentIndex(0)
        else:
            self.inverse_combo.setCurrentIndex(1)

    def register_event(self):
        """"""
        self.signal_log.connect(self.process_log_event)
        self.signal_backtesting_finished.connect(
            self.process_backtesting_finished_event)
        self.signal_optimization_finished.connect(
            self.process_optimization_finished_event)

        self.event_engine.register(EVENT_BACKTESTER_LOG, self.signal_log.emit)
        self.event_engine.register(
            EVENT_BACKTESTER_BACKTESTING_FINISHED, self.signal_backtesting_finished.emit)
        self.event_engine.register(
            EVENT_BACKTESTER_OPTIMIZATION_FINISHED, self.signal_optimization_finished.emit)

    def process_log_event(self, event: Event):
        """"""
        msg = event.data
        self.write_log(msg)

    def write_log(self, msg):
        """"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        msg = f"{timestamp}\t{msg}"
        self.log_monitor.append(msg)

    def process_backtesting_finished_event(self, event: Event):
        """"""
        statistics = self.backtester_engine.get_result_statistics()
        self.statistics_monitor.set_data(statistics)

        df = self.backtester_engine.get_result_df()
        self.chart.set_data(df)

        self.trade_button.setEnabled(True)
        self.order_button.setEnabled(True)
        self.daily_button.setEnabled(True)

        # Tick data can not be displayed using candle chart
        interval = self.interval_combo.currentText()
        if interval != Interval.TICK.value:
            self.candle_button.setEnabled(True)

    def process_optimization_finished_event(self, event: Event):
        """"""
        self.write_log("请点击[优化结果]按钮查看")
        self.result_button.setEnabled(True)

    def start_backtesting(self):
        """"""
        class_name = self.class_combo.currentText()
        vt_symbol = self.symbol_line.text()
        interval = self.interval_combo.currentText()
        start = self.start_date_edit.dateTime().toPyDateTime()
        end = self.end_date_edit.dateTime().toPyDateTime()
        rate = float(self.rate_line.text())
        slippage = float(self.slippage_line.text())
        size = float(self.size_line.text())
        pricetick = float(self.pricetick_line.text())
        capital = float(self.capital_line.text())

        if self.inverse_combo.currentText() == "正向":
            inverse = False
        else:
            inverse = True

        # Check validity of vt_symbol
        if "." not in vt_symbol:
            self.write_log("本地代码缺失交易所后缀，请检查")
            return

        _, exchange_str = vt_symbol.split(".")
        if exchange_str not in Exchange.__members__:
            self.write_log("本地代码的交易所后缀不正确，请检查")
            return

        # Save backtesting parameters
        backtesting_setting = {
            "class_name": class_name,
            "vt_symbol": vt_symbol,
            "interval": interval,
            "start": start.isoformat(),
            "rate": rate,
            "slippage": slippage,
            "size": size,
            "pricetick": pricetick,
            "capital": capital,
            "inverse": inverse,
        }
        save_json(self.setting_filename, backtesting_setting)

        # Get strategy setting
        old_setting = self.settings[class_name]
        dialog = BacktestingSettingEditor(class_name, old_setting)
        i = dialog.exec()
        if i != dialog.Accepted:
            return

        new_setting = dialog.get_setting()
        self.settings[class_name] = new_setting

        result = self.backtester_engine.start_backtesting(
            class_name,
            vt_symbol,
            interval,
            start,
            end,
            rate,
            slippage,
            size,
            pricetick,
            capital,
            inverse,
            new_setting
        )

        if result:
            self.statistics_monitor.clear_data()
            self.chart.clear_data()

            self.trade_button.setEnabled(False)
            self.order_button.setEnabled(False)
            self.daily_button.setEnabled(False)
            self.candle_button.setEnabled(False)

            self.trade_dialog.clear_data()
            self.order_dialog.clear_data()
            self.daily_dialog.clear_data()
            self.candle_dialog.clear_data()

    def start_optimization(self):
        """"""
        class_name = self.class_combo.currentText()
        vt_symbol = self.symbol_line.text()
        interval = self.interval_combo.currentText()
        start = self.start_date_edit.dateTime().toPyDateTime()
        end = self.end_date_edit.dateTime().toPyDateTime()
        rate = float(self.rate_line.text())
        slippage = float(self.slippage_line.text())
        size = float(self.size_line.text())
        pricetick = float(self.pricetick_line.text())
        capital = float(self.capital_line.text())

        if self.inverse_combo.currentText() == "正向":
            inverse = False
        else:
            inverse = True

        parameters = self.settings[class_name]
        dialog = OptimizationSettingEditor(class_name, parameters)
        i = dialog.exec()
        if i != dialog.Accepted:
            return

        optimization_setting, use_ga = dialog.get_setting()
        self.target_display = dialog.target_display

        self.backtester_engine.start_optimization(
            class_name,
            vt_symbol,
            interval,
            start,
            end,
            rate,
            slippage,
            size,
            pricetick,
            capital,
            inverse,
            optimization_setting,
            use_ga
        )

        self.result_button.setEnabled(False)

    def start_downloading(self):
        """"""
        vt_symbol = self.symbol_line.text()
        interval = self.interval_combo.currentText()
        start_date = self.start_date_edit.date()
        end_date = self.end_date_edit.date()

        start = datetime(
            start_date.year(),
            start_date.month(),
            start_date.day(),
        )
        start = DB_TZ.localize(start)

        end = datetime(
            end_date.year(),
            end_date.month(),
            end_date.day(),
            23,
            59,
            59,
        )
        end = DB_TZ.localize(end)

        self.backtester_engine.start_downloading(
            vt_symbol,
            interval,
            start,
            end
        )

    def show_optimization_result(self):
        """"""
        result_values = self.backtester_engine.get_result_values()

        dialog = OptimizationResultMonitor(
            result_values,
            self.target_display
        )
        dialog.exec_()

    def show_backtesting_trades(self):
        """"""
        if not self.trade_dialog.is_updated():
            trades = self.backtester_engine.get_all_trades()
            self.trade_dialog.update_data(trades)

        self.trade_dialog.exec_()

    def show_backtesting_orders(self):
        """"""
        if not self.order_dialog.is_updated():
            orders = self.backtester_engine.get_all_orders()
            self.order_dialog.update_data(orders)

        self.order_dialog.exec_()

    def show_daily_results(self):
        """"""
        if not self.daily_dialog.is_updated():
            results = self.backtester_engine.get_all_daily_results()
            self.daily_dialog.update_data(results)

        self.daily_dialog.exec_()

    def show_candle_chart(self):
        """"""
        if not self.candle_dialog.is_updated():
            history = self.backtester_engine.get_history_data()
            self.candle_dialog.update_history(history)

            trades = self.backtester_engine.get_all_trades()
            self.candle_dialog.update_trades(trades)

        self.candle_dialog.exec_()

    def edit_strategy_code(self):
        """"""
        class_name = self.class_combo.currentText()
        file_path = self.backtester_engine.get_strategy_class_file(class_name)

        self.editor.open_editor(file_path)
        self.editor.show()

    def reload_strategy_class(self):
        """"""
        self.backtester_engine.reload_strategy_class()

        current_strategy_name = self.class_combo.currentText()

        self.class_combo.clear()
        self.init_strategy_settings()

        ix = self.class_combo.findText(current_strategy_name)
        self.class_combo.setCurrentIndex(ix)

    def show(self):
        """"""
        self.showMaximized()