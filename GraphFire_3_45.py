#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys


# In[2]:


class SplashScreen:
    """Экран загрузки приложения"""
    
    def __init__(self, root):
        """Инициализация splash-экрана с корневым окном"""
        self.splash = tk.Toplevel(root)  # Всплывающее окно поверх главного
        self.splash.title("Graph Fire")  # Заголовок окна
        self.splash.geometry("600x400")  # Фиксированный размер окна
        self.splash.overrideredirect(True)  # Отключение системной рамки окна
        self.canvas = tk.Canvas(self.splash, bg='#FFFFFF', highlightthickness=0)  # Холст для рисования
        self.canvas.pack(fill="both", expand=True, padx=1, pady=1)  # Растяжение холста на все окно
        self._center_window()  # Центрирование окна на экране
        self._draw_all()  # Отрисовка всех элементов интерфейса
        self.splash.update()
        self.root = root  # Сохранение корневого окна для последующего отображения
        
    def _center_window(self):
        """Центрирование окна относительно экрана"""
        self.splash.update_idletasks()  # Обновление геометрии окна перед расчетом
        x = (self.splash.winfo_screenwidth() - 600) // 2  # Центр по горизонтали
        y = (self.splash.winfo_screenheight() - 400) // 2  # Центр по вертикали
        self.splash.geometry(f'+{x}+{y}')  # Установка позиции окна
    
    def _draw_all(self):
        """Отрисовка всего интерфейса splash-экрана"""
        w, h = 600, 400  # Ширина и высота окна
        top_h = int(h * 0.55)  # Высота верхней части с заголовком
        self.canvas.create_text(40, top_h//2 - 20, text="Graph Fire", font=("Segoe UI", 36, "bold"), fill='#3b6ea5', anchor="w")  # Заголовок
        self.canvas.create_text(40, top_h//2 + 50, text="Version 1.0", font=("Segoe UI", 12), fill='#1E2939', anchor="w")  # Версия приложения
        self._draw_logo(int(w * 0.65) - 20, top_h//2)  # Логотип приложения
        self.canvas.create_line(40, top_h - 10, w - 40, top_h - 10, fill='#d5d5d5', width=1)  # Разделительная линия
        self.canvas.create_text(w//2, h//2 + 130, text="Loading...", font=("Segoe UI", 11), fill='#6c757d')  # Текст загрузки
        self._create_progress_indicator()  # Индикатор прогресса в виде графа
    
    def _draw_logo(self, x, y):
        """Отрисовка логотипа из файла"""
        try:
            if os.path.exists("logo_graph_fire.png"):  # Проверка существования файла логотипа
                self.logo_img = tk.PhotoImage(file="logo_graph_fire.png")  # Загрузка изображения
                self.canvas.create_image(x + 80, y, image=self.logo_img, anchor="center")  # Отрисовка логотипа
                return
        except:
            pass  # Игнорирование ошибок при отсутствии логотипа
    
    def _create_progress_indicator(self):
        """Создание индикатора прогресса в виде последовательных вершин графа"""
        w, h = 600, 400  # Ширина и высота окна
        self.vertex_count = 10  # Количество вершин в индикаторе
        self.vertices = []  # Список идентификаторов вершин
        self.vertex_texts = []  # Список идентификаторов текста вершин
        self.edges = []  # Список идентификаторов ребер
        radius = 16  # Радиус вершины
        start_x, end_x = 100, w - 100  # Начальная и конечная координаты X
        y_pos = h//2 + 70  # Позиция Y для всех вершин
        spacing = (end_x - start_x - 2 * radius * self.vertex_count) / (self.vertex_count - 1)  # Расстояние между вершинами
        
        for i in range(self.vertex_count):  # Цикл по всем вершинам
            x = start_x + i * (2 * radius + spacing) + radius  # X-координата текущей вершины
            if i < self.vertex_count - 1:  # Не последняя вершина
                next_x = start_x + (i + 1) * (2 * radius + spacing) + radius  # X-координата следующей вершины
                edge = self.canvas.create_line(x + radius, y_pos, next_x - radius, y_pos, fill='#6c757d', width=1.5)  # Ребро между вершинами
                self.edges.append(edge)  # Сохранение идентификатора ребра
            # Круги с вершинами и номерами
            vertex = self.canvas.create_oval(x - radius, y_pos - radius, x + radius, y_pos + radius, fill='#dde1e3', outline='#6c757d', width=1)
            text = self.canvas.create_text(x, y_pos, text=str(i + 1), font=("Segoe UI", 11, "bold"), fill='#95a5a6')  # Номер вершины
            self.vertices.append(vertex)  # Сохранение идентификатора вершины
            self.vertex_texts.append(text)  # Сохранение идентификатора текста
        self.current_step = 0  # Текущий шаг прогресса (0 - ничего не загружено)
    
    def update_progress(self, step):
        """Обновление прогресса загрузки с изменением цвета вершин и ребер"""
        step = max(0, min(step, self.vertex_count))  # Ограничение шага диапазоном 0..vertex_count
        for i in range(step):  # Закрашивание пройденных вершин
            self.canvas.itemconfig(self.vertices[i], fill='#3b6ea5', outline='#3b6ea5')  # Активный цвет вершины
            self.canvas.itemconfig(self.vertex_texts[i], fill='#FFFFFF')  # Белый текст на активной вершине
            if i < len(self.edges):  # Существует ребро после этой вершины
                self.canvas.itemconfig(self.edges[i], fill='#3b6ea5', width=2)  # Активный цвет ребра
        
        for i in range(step, self.vertex_count):  # Сброс цвета у непройденных вершин
            self.canvas.itemconfig(self.vertices[i], fill='#dde1e3', outline='#6c757d')  # Неактивный цвет вершины
            self.canvas.itemconfig(self.vertex_texts[i], fill='#95a5a6')  # Серый текст на неактивной вершине
            if i < len(self.edges) and i >= step:  # Ребро после непройденной вершины
                self.canvas.itemconfig(self.edges[i], fill='#6c757d', width=2)  # Неактивный цвет ребра
        
        self.current_step = step  # Сохранение текущего шага
        self.splash.update()  # Принудительное обновление окна
    
    def close(self):
        """Закрытие splash-экрана и показ главного окна"""
        self.splash.destroy()  # Уничтожение окна splash


# In[3]:


import random
import math
import numpy as np
import networkx as nx
from scipy.stats import truncnorm, t as stats_t, laplace, nct, lognorm, gaussian_kde, norm
from scipy import stats
from datetime import datetime
from typing import Callable, List, Dict, Tuple, Optional, Protocol
import copy
import csv

import pandas as pd
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages


# In[4]:


TRANSLATIONS = { # Словарь переводов для интерфейса
    'RU': {
        '':'',
        # Названия вкладок
        'tab_generation': 'Генерация графа',
        'tab_custom': 'Пользовательский граф',
        'tab_simulation': 'Запуск симуляции',
        'tab_multiple': 'Множественная симуляция',
        'tab_help': 'Как пользоваться',
        'tab_settings': 'Настройки',
        
        # Кнопки
        'start_fire': 'Запуск 🔥',
        'reset': 'Сброс',
        'new_graph': 'Новый граф',
        'next_graph': 'Следующий граф',
        'insert_into_custom': 'Вставить граф в "Пользовательский граф"',
        'insert_into_simulation': 'Вставить граф в "Запуск симуляции"',
        'insert_into_multiple': 'Вставить граф в "Множественная симуляция"',        
        'reset_to_default': 'Сбросить к графу по умолчанию',
        'export_pdf': 'Экспортировать в PDF',
        'export_csv': 'Экспортировать в CSV',
        'batch_stop': 'Остановить',
        'view_results': 'Смотреть итоги',
        'export_all': 'Экспорт всех',
        'view_all_results': 'Смотреть итоги всех',
        'apply': 'Применить',
        'load_csv': 'Загрузить данные из CSV',
        'save_csv': 'Сохранить данные в CSV',
        'select_csv_file': 'Выбрать CSV-файл',
        'select_another_file': 'Выбрать другой файл',
        'cancel': 'Отмена',

        # Диалоги подтверждения действий
        'confirm_title': 'Подтверждение',
        'confirm_replace_custom': 'Текущий граф на вкладке "Пользовательский граф" будет заменен. Продолжить?',
        'confirm_replace_simulation': 'Текущий граф на вкладке "Запуск симуляции" будет заменен. Продолжить?',
        'confirm_replace_multiple': 'Текущий граф на вкладке "Множественная симуляция" будет заменен. Продолжить?',
        'confirm_reset_default': 'Сбросить все изменения к графу по умолчанию?',
        'export_title': 'Выберите формат для экспорта',
        
        # Заголовки разделов (вкладка генерации графа)
        'vertex_count': 'Количество вершин',
        'edge_distribution': 'Распределение ребер',
        'vertex_distribution': 'Распределение вершин',
        'resistance_type': 'Тип устойчивости',
        'influence_type': 'Тип влияния',
        'damping_type': 'Тип затухания',

        # Типы распределений
        'None': 'Нет',
        'Uniform': 'Равномерное',
        'Normal': 'Нормальное',
        'Student': 'Стьюдента',
        'Laplace': 'Лапласа',
        'Bimodal': 'Бимодальное',
        'Skewed_t': 'Скошенное t',
        'Lognormal': 'Логнормальное',
        'Stepwise': 'Ступенчатое',
        'custom': 'Пользовательское',

        # Значения для типов устойчивости, влияния и затухания
        'param_direct': 'Прямо пропорционально размеру',
        'param_inverse': 'Обратно пропорционально размеру',
        'damping_exponential': 'Экспоненциальное',
        'damping_hyperbolic': 'Гиперболическое',
        'damping_discrete': 'Дискретное',
        
        # Обозначения параметров распределений
        'left': 'L',
        'right': 'R',
        'mean': 'μ',
        'mu': 'μ',
        'std': 'σ',
        'sigma': 'σ',
        'df': 'df',
        'scale': 'scale',
        'loc': 'loc',
        'shape': 'α',
        'weight': 'Вес первого режима',
        'gamma': 'γ',
        'mu1': 'μ₁',
        'sigma1': 'σ₁',
        'mu2': 'μ₂',
        'sigma2': 'σ₂',
        'coeff': 'коэф.',

        # Ступенчатое распределение
        'stages_count': 'Количество ступеней',
        'elements_count_stage': 'Количество элементов в ступени',
        'presets': 'Шаблоны',
        'stage': 'Ступень',
        'left_bound': 'Левая граница',
        'right_bound': 'Правая граница',
        'market': 'Рыночный',
        'oligopoly': 'Олигополия',
        'uniform_preset': 'Равномерный ',
        'pyramid': 'Пирамида',
        'exponential': 'Экспоненциальный',
        'social': 'Социальный',
        'economic': 'Экономический',
        'information': 'Информационный',
        'hierarchical': 'Иерархический',
        'ecosystem': 'Экосистемный',
        'infrastructure': 'Критический',
        'epidemic': 'Эпидемиологический',

        # Текст для гистограмм
        'num_bins': 'Бинов',

        # Загрузка CSV файла
        'format_requirements': 'Требования к формату файла',
        'size_sync': 'Синхронизация размеров',
        'format_csv': 'Файл в формате .csv с разделителем-запятой',
        'format_encoding': 'Кодировка UTF-8',
        'v_format_structure': 'Один столбец чисел (веса вершин) без заголовка',
        'v_format_range': 'Допустимый диапазон значений от 0.01 до 1.0',
        'e_format_structure': 'Квадратная матрица без заголовков (Используется только верхний треугольник)',
        'e_format_range': 'Допустимый диапазон значений от -1.0 до 1.0',
        'v_sync_limit': 'Если в файле более 1000 вершин, будут использованы первые 1000',
        'v_sync_more': 'Если вершин в файле больше текущего количества, будут добавлены новые ребра с дефолтным весом',
        'v_sync_less': 'Если вершин в файле меньше текущего количества, матрица ребер будет обрезана до нужного размера',
        'e_sync_limit': 'Если в файле более 1000 вершин, будут использованы первые 1000',
        'e_sync_more': 'Если ребер в файле больше текущего количества, будут добавлены новые вершины с дефолтным весом',
        'e_sync_less': 'Если ребер в файле меньше текущего количества, матрица вершин будет обрезана до нужного размера',
        'error_title': 'Ошибка при чтении файла',

        # Заголовки разделов (вкладка запуска симуляции)
        'graph_parameters': 'Параметры графа',
        'edge_stats': 'Статистика ребер',
        'vertex_stats': 'Статистика вершин',
        'simulation_results': 'Итоги симуляции возгорания',
        'start_vertex_title': 'Выбор стартовой вершины',
        'start_vertex_stats': 'Статистика стартовой вершины',
        'additional_properties': 'Дополнительные свойства',
        'generation_params': 'Параметры генерации',
        'graph_seed': 'Seed графа',

        # Статистики параметров графа
        'source_tab': 'Вкладка-источник графа',
        'insert_time': 'Время вставки',
        'vertex_count_stat': 'Количество вершин',
        'edge_count_stat': 'Количество ребер',
        'resistance_stat': 'Устойчивость',
        'influence_stat': 'Влияние',
        'damping_stat': 'Затухание',

        # Статистики ребер и вершин
        'min_stat': 'Мин',
        'max_stat': 'Макс',
        'mean_stat': 'Среднее',
        'std_stat': 'Стд.откл.',
        'median': 'Медиана',
        'skewness': 'Асимметрия',
        'kurtosis': 'Эксцесс',
        'q05': 'Квантиль 5%',
        'q95': 'Квантиль 95%',
        'positive_sum': 'Сумма положительных',
        'negative_sum': 'Сумма отрицательных',
        'positive_mean': 'Среднее положительных',
        'negative_mean': 'Среднее отрицательных',
        'vertex_number': 'Вершина №',
        'vertex_weight': 'Вес вершины',
        'avg_edge_weight': 'Среднее связей',
        'positive_count': 'Положительных связей',
        'negative_count': 'Отрицательных связей',
        'positive_percent': 'Процент положительных',
        'negative_percent': 'Процент отрицательных',
        'resistance_factor': 'Коэф. устойчивости',
        'influence_factor': 'Коэф. влияния',
        
        # Статистики итогов симуляции пожара
        'total_burned': 'Сгорело вершин',
        'total_iterations': 'Всего итераций',
        'spread_rate_1': 'Новые возгорания на шаге 1',
        'spread_rate_2': 'Новые возгорания на шаге 2',
        'spread_rate_3': 'Новые возгорания на шаге 3',
        'spread_rate_4': 'Новые возгорания на шаге 4',
        'spread_rate_5': 'Новые возгорания на шаге 5',
        'peak_new_burns': 'Макс. новых возгораний',
        'time_to_peak': 'Шагов до пика',
        'time_from_peak': 'Шагов от пика до конца',
        
        # Вкладка множественной симуляции
        'batch_generation_params': 'Параметры множественной генерации',
        'batch_graphs_count': 'Количество графов заданного распределения',
        'batch_start_vertices_count': 'Количество стартовых вершин в каждом графе',
        'batch_start_vertices': 'Номера стартовых вершин',
        'batch_simulations_per_vertex': 'Количество симуляций на каждую вершину',
        'total_generations': 'Всего генераций',
        'batch_results': 'Результаты генерации',
        'graph_label': 'G {}',        
        'all_graphs': 'Все графы',    

        'batch_summary_title': 'Итоги множественной симуляции',
        'burned_vertices_title': 'Количество сгоревших вершин',
        'features_importance_title': 'Значимость признаков для количества сгоревших вершин',
        'burned_duration_title': 'Длительность возгорания',
        'features_importance_duration_title': 'Значимость признаков (total_iterations)',
        'time_to_peak_title': 'Время до пика',
        'peak_new_burns_title': 'Пиковое количество возгораний',
        'time_from_peak_title': 'Время от пика до конца',
        'features_importance_time_to_peak_title': 'Значимость признаков (time_to_peak)',
        'features_importance_peak_title': 'Значимость признаков (peak_new_burns)',
        'features_importance_time_from_peak_title': 'Значимость признаков (time_from_peak_to_end)',
        'spread_rate_title_1': 'Скорость распространения (шаг 1)',
        'features_importance_spread_1_title': 'Значимость признаков (spread_rate_1)',
        'vulnerability_rating_title': 'Рейтинг уязвимости вершин',
        'vuln_rank': 'Ранг',
        'vuln_total_percent': '% сгорания',
        'vuln_step1_percent': '% на шаге 1',
        'vuln_step2_percent': '% на шаге 2',
        'vuln_step3_percent': '% на шаге 3',
        'vuln_step4_percent': '% на шаге 4',
        'vuln_step5_percent': '% на шаге 5',
        'vertex_number': 'Вершина №',

        'help_section_overview': 'Основное',
        'spearman_correlation': 'Корреляция Спирмена',
        'mutual_information': 'Взаимная информация',
        'permutation_importance': 'Важность перестановкой',
        
        # Настройки интерфейса
        'settings_interface': 'Параметры интерфейса',
        'language': 'Язык',
        'RU': 'Русский',
        'EN': 'Английский',
        'settings_theme': 'Тема',
        'theme_light': 'Светлая',
        'theme_dark': 'Темная',
        'font_size': 'Размер шрифта',

        # Настройки округления
        'rounding_settings': 'Округление вещественных чисел',
        'rounding_input': 'Знаков после точки в полях ввода',
        'rounding_stats': 'Знаков после точки в статистиках',
        
        # Настройки воспроизводимости
        'settings_reproducibility': 'Воспроизводимость',
        'settings_seed_global': 'Глобальный seed (отправная точка)',
        'settings_seed_graph': 'Локальный seed графа (для симуляции)',
        'seed_random': 'Случайный',
        'seed_fixed': 'Фиксированный',
        
        # Настройки макс. количества вершин в графе
        'max_vertex_count': 'Максимальное допустимое количество вершин в графе',

        # Настройки поджога
        'ignition_settings': 'Параметры поджога',
        'ignition_method': 'Метод поджога',
        'Sequential': 'Последовательный',
        'Simultaneous': 'Одновременный',
        'threshold_method': 'Тип порога',
        'threshold_value': 'Значение порога',
        'Maximum': 'Максимум',
        'Mean': 'Среднее',
        'Median': 'Медиана',
        
        # Настройки визуализации графа
        'visualization_settings': 'Визуализация графа',
        'hide_graph_display': 'Не отображать граф',
        'vertex_layout_type': 'Тип расположения вершин',
        'layout_spring': 'Пружинная компоновка',
        'layout_circular': 'Круговая компоновка',
        'layout_random': 'Случайная компоновка',
        'layout_grid': 'Сеточная компоновка',
        'show_non_burning_edges': 'Рисовать негорящие ребра в графе',
        'settings_show_negative': 'Показывать отрицательные ребра',
        'use_simple_edge_colors': 'Упрощенная цветовая схема (только 2 цвета)',
        'threshold_redraw': 'Перерисовывать пользовательский граф после добавления вершин',
        
        # Настройки графа по умолчанию (кастомный дефолтный граф)
        'default_graph_params': 'Параметры графа по умолчанию',
        'default_vertex_count_label': 'Количество вершин в графе по умолчанию',
        'default_vertex_weight_label': 'Дефолтный вес вершин в графе по умолчанию',
        'default_edge_weight_label': 'Дефолтная толщина ребер в графе по умолчанию',

        # Настройки множественной генерации
        'batch_generation_params_title': 'Параметры множественной генерации',
        'max_batch_graphs_label': 'Максимальное количество графов',
        'max_batch_simulations_label': 'Максимальное количество симуляций на одну вершину',
        'progress_update_mode': 'Изменение прогресс-бара после обработки',
        'progress_per_vertex': 'одной вершины',
        'progress_per_graph': 'одного графа',       
    },
    
    'EN': {
        '':'',
        # Названия вкладок
        'tab_generation': 'Graph Generation',
        'tab_custom': 'Custom Graph',
        'tab_simulation': 'Run Simulation',
        'tab_multiple': 'Multiple Simulation',
        'tab_help': 'How to Use',
        'tab_settings': 'Settings',
        
        # Кнопки
        'start_fire': 'Start 🔥',
        'reset': 'Reset',
        'new_graph': 'New graph',
        'next_graph': 'Next graph',
        'insert_into_custom': 'Insert graph into "Custom Graph"',
        'insert_into_simulation': 'Insert graph into "Run Simulation"',
        'insert_into_multiple': 'Insert graph into "Multiple Simulation"',        
        'reset_to_default': 'Reset to default graph',
        'export_pdf': 'Export to PDF',
        'export_csv': 'Export to CSV',
        'batch_stop': 'Stop',
        'view_results': 'View results',
        'export_all': 'Export all',
        'view_all_results': 'View all results',
        'apply': 'Apply',
        'load_csv': 'Load data from CSV',
        'save_csv': 'Save data to CSV',
        'select_csv_file': 'Select CSV File',
        'select_another_file': 'Select Another File',
        'cancel': 'Cancel',

        # Диалоги подтверждения действий
        'confirm_title': 'Confirmation',
        'confirm_replace_custom': 'The current graph in the "Custom Graph" tab will be replaced. Continue?',
        'confirm_replace_simulation': 'The current graph in the "Run Simulation" tab will be replaced. Continue?',
        'confirm_replace_multiple': 'The current graph in the "Multiple Simulation" tab will be replaced. Continue?',
        'confirm_reset_default': 'Reset all changes to the default graph?',
        'export_title': 'Select export format',
        
        # Заголовки разделов (вкладка генерации графа)
        'vertex_count': 'Vertex count',
        'edge_distribution': 'Edge distribution',
        'vertex_distribution': 'Vertex distribution',
        'resistance_type': 'Resistance Type',
        'influence_type': 'Influence Type',
        'damping_type': 'Damping Type',

        # Типы распределений
        'None': 'None',
        'Uniform': 'Uniform',
        'Normal': 'Normal',
        'Student': 'Student',
        'Laplace': 'Laplace',
        'Bimodal': 'Bimodal',
        'Skewed_t': 'Skewed t',
        'Lognormal': 'Lognormal',
        'Stepwise': 'Stepwise',
        'custom': 'Custom',

        # Значения для типов устойчивости, влияния и затухания
        'param_direct': 'Direct proportional to size',
        'param_inverse': 'Inversely proportional to size',
        'damping_exponential': 'Exponential',
        'damping_hyperbolic': 'Hyperbolic',
        'damping_discrete': 'Discrete',
        
        # Обозначения параметров распределений
        'left': 'L',
        'right': 'R',
        'mean': 'μ',
        'mu': 'μ',
        'std': 'σ',
        'sigma': 'σ',
        'df': 'df',
        'scale': 'scale',
        'loc': 'loc',
        'shape': 'α',
        'weight': 'Weight of first mode',
        'gamma': 'γ',
        'mu1': 'μ₁',
        'sigma1': 'σ₁',
        'mu2': 'μ₂',
        'sigma2': 'σ₂',
        'coeff': 'coeff.',

        # Ступенчатое распределение
        'stages_count': 'Number of stages',
        'elements_count_stage': 'Number of elements in stage',
        'presets': 'Presets',
        'stage': 'Stage',
        'left_bound': 'Left bound',
        'right_bound': 'Right bound',
        'market': 'Market',
        'oligopoly': 'Oligopoly',
        'uniform_preset': 'Uniform ',
        'pyramid': 'Pyramid',
        'exponential': 'Exponential',
        'social': 'Social',
        'economic': 'Economic',
        'information': 'Information',
        'hierarchical': 'Hierarchical',
        'ecosystem': 'Ecosystem',
        'infrastructure': 'Critical',
        'epidemic': 'Epidemiological',

        # Текст для гистограмм
        'num_bins': 'Bins',

        # Загрузка CSV файла
        'format_requirements': 'File Format Requirements',
        'size_sync': 'Size Synchronization',
        'format_csv': 'CSV file with comma separator',
        'format_encoding': 'UTF-8 encoding',
        'v_format_structure': 'Single column of numbers (vertex weights) without header',
        'v_format_range': 'Allowed value range from 0.01 to 1.0',
        'e_format_structure': 'Square matrix without headers (Only upper triangle is used)',
        'e_format_range': 'Allowed value range from -1.0 to 1.0',
        'v_sync_limit': 'If file contains more than 1000 vertices, only first 1000 will be used',
        'v_sync_more': 'If file has more vertices than current graph, new edges will be added with default weight',
        'v_sync_less': 'If file has fewer vertices than current graph, edge matrix will be truncated',
        'e_sync_limit': 'If file contains more than 1000 vertices, only first 1000 will be used',
        'e_sync_more': 'If file has more edges than current graph, new vertices will be added with default weight',
        'e_sync_less': 'If file has fewer edges than current graph, vertex matrix will be truncated',
        'error_title': 'Error reading file',

        # Заголовки разделов (вкладка запуска симуляции)
        'graph_parameters': 'Graph parameters',
        'edge_stats': 'Edge statistics',
        'vertex_stats': 'Vertex statistics',
        'simulation_results': 'Fire simulation results',
        'start_vertex_title': 'Starting vertex selection',
        'start_vertex_stats': 'Starting vertex statistics',
        'additional_properties': 'Additional Properties',
        'generation_params': 'Generation parameters',

        # Статистики параметров графа
        'source_tab': 'Graph source tab',
        'insert_time': 'Insertion time',
        'vertex_count_stat': 'Vertex count',
        'edge_count_stat': 'Edge count',
        'resistance_stat': 'Resistance',
        'influence_stat': 'Influence',
        'damping_stat': 'Damping',
        'graph_seed': 'Graph seed',

        # Статистики ребер и вершин
        'min_stat': 'Min',
        'max_stat': 'Max',
        'mean_stat': 'Mean',
        'std_stat': 'Std',
        'median': 'Median',
        'skewness': 'Skewness',
        'kurtosis': 'Kurtosis',
        'q05': '5% Quantile',
        'q95': '95% Quantile',
        'positive_sum': 'Positive sum',
        'negative_sum': 'Negative sum',
        'positive_mean': 'Positive mean',
        'negative_mean': 'Negative mean',
        'vertex_number': 'Vertex #',
        'vertex_weight': 'Vertex weight',
        'avg_edge_weight': 'Average edge weight',
        'positive_count': 'Positive connections',
        'negative_count': 'Negative connections',
        'positive_percent': 'Positive %',
        'negative_percent': 'Negative %',
        'resistance_factor': 'Resistance coeff.',
        'influence_factor': 'Influence coeff.',
        
        # Статистики итогов симуляции пожара
        'total_burned': 'Total burned vertices',
        'total_iterations': 'Total iterations',
        'spread_rate_1': 'New fires at step 1',
        'spread_rate_2': 'New fires at step 2',
        'spread_rate_3': 'New fires at step 3',
        'spread_rate_4': 'New fires at step 4',
        'spread_rate_5': 'New fires at step 5',
        'peak_new_burns': 'Peak new fires',
        'time_to_peak': 'Steps to peak',
        'time_from_peak': 'Steps from peak to end',
        
        # Вкладка множественной симуляции
        'batch_generation_params': 'Batch generation parameters',
        'batch_graphs_count': 'Number of graphs of a given distribution',
        'batch_start_vertices_count': 'Number of starting vertices per graph',
        'batch_start_vertices': 'Starting vertex numbers',
        'batch_simulations_per_vertex': 'Number of simulations per vertex',
        'total_generations': 'Total generations',
        'batch_results': 'Generation results',
        'graph_label': 'G {}',        
        'all_graphs': 'All graphs',      

        'batch_summary_title': 'Batch simulation results',
        'burned_vertices_title': 'Burned vertices count',
        'features_importance_title': 'Feature importance for burned vertices count',
        'burned_duration_title': 'Burning duration',
        'features_importance_duration_title': 'Feature importance (total_iterations)',
        'time_to_peak_title': 'Time to peak',
        'peak_new_burns_title': 'Peak new burns',
        'time_from_peak_title': 'Time from peak to end',
        'features_importance_time_to_peak_title': 'Feature importance (time_to_peak)',
        'features_importance_peak_title': 'Feature importance (peak_new_burns)',
        'features_importance_time_from_peak_title': 'Feature importance (time_from_peak_to_end)',
        'spread_rate_title_1': 'Spread Rate (Step 1)',
        'features_importance_spread_1_title': 'Feature Importance (spread_rate_1)',
        'vulnerability_rating_title': 'Vertex Vulnerability Rating',
        'vuln_rank': 'Rank',
        'vuln_total_percent': '% Burned',
        'vuln_step1_percent': '% at Step 1',
        'vuln_step2_percent': '% at Step 2',
        'vuln_step3_percent': '% at Step 3',
        'vuln_step4_percent': '% at Step 4',
        'vuln_step5_percent': '% at Step 5',
        'vertex_number': 'Vertex #',

        'help_section_overview': 'Overview',
        'spearman_correlation': 'Spearman Correlation',
        'mutual_information': 'Mutual Information',
        'permutation_importance': 'Permutation Importance',
        
        # Настройки интерфейса
        'settings_interface': 'Interface parameters',
        'language': 'Language',
        'RU': 'Russian',
        'EN': 'English',
        'settings_theme': 'Theme',
        'theme_light': 'Light',
        'theme_dark': 'Dark',
        'font_size': 'Font size',

        # Настройки округления
        'rounding_settings': 'Floating point rounding',
        'rounding_input': 'Decimal places in input fields',
        'rounding_stats': 'Decimal places in statistics',
        
        # Настройки воспроизводимости
        'settings_reproducibility': 'Reproducibility',
        'settings_seed_global': 'Global seed (starting point)',
        'settings_seed_graph': 'Graph local seed (for simulation)',
        'seed_random': 'Random',
        'seed_fixed': 'Fixed',
        
        # Настройки макс. количества вершин в графе
        'max_vertex_count': 'Maximum allowed number of vertices in the graph',

        # Настройки поджога
        'ignition_settings': 'Ignition Settings',
        'ignition_method': 'Ignition Method',
        'Sequential': 'Sequential',
        'Simultaneous': 'Simultaneous',
        'threshold_method': 'Threshold Type',
        'threshold_value': 'Threshold Value',
        'Maximum': 'Maximum',
        'Mean': 'Mean',
        'Median': 'Median',
        
        # Настройки визуализации графа
        'visualization_settings': 'Graph visualization',
        'hide_graph_display': 'Hide graph display',
        'vertex_layout_type': 'Vertex layout type',
        'layout_spring': 'Spring layout',
        'layout_circular': 'Circular layout',
        'layout_random': 'Random layout',
        'layout_grid': 'Grid layout',
        'show_non_burning_edges': 'Show non-burning edges in graph',
        'settings_show_negative': 'Show negative edges',
        'use_simple_edge_colors': 'Simplified color scheme (only 2 colors)',
        'threshold_redraw': 'Redraw custom graph after adding vertices',
        
        # Настройки графа по умолчанию (кастомный дефолтный граф)
        'default_graph_params': 'Default Graph Parameters',
        'default_vertex_count_label': 'Default number of vertices in graph',
        'default_vertex_weight_label': 'Default vertex weight',
        'default_edge_weight_label': 'Default edge weight',

        # Настройки множественной генерации
        'batch_generation_params_title': 'Batch Generation Parameters',
        'max_batch_graphs_label': 'Maximum number of graphs',
        'max_batch_simulations_label': 'Maximum number of simulations per vertex',
        'progress_update_mode': 'Progress bar update mode',
        'progress_per_vertex': 'per vertex',
        'progress_per_graph': 'per graph',       
    },
}


# In[5]:


THEME_COLORS = { # Словарь цветов для интерфейса
    'theme_light': {
        # Цвета фона
        'bg_color': "#ffffff",                # Основной фон приложения
        'frame_bg': "#ffffff",                # Фон рамок и панелей
        'plot_bg': "#ffffff",                 # Фон графиков
        
        # Цвета текста
        'text_color': "#000000",              # Основной текст
        'text_secondary': "#666666",          # Вторичный текст
        'btn_text': "#ffffff",                # Текст на кнопках
        'accent_color': "#4a6fa5",            # Акцентный цвет

        # Цвета вкладок в шапке
        'tab1_inactive': '#DBE2F8',           # Генерация графа
        'tab1_active': '#A3B1E3',
        'tab2_inactive': '#E6E0F7',           # Пользовательский граф
        'tab2_active': '#B8ABE3',
        'tab3_inactive': '#E9D4C3',           # Запуск симуляции
        'tab3_active': '#C69E82', 
        'tab4_inactive': '#EAD6B4',           # Множественная генерация
        'tab4_active': '#C9A66B',
        'tab5_inactive': '#D6DFCB',           # Как пользоваться
        'tab5_active': '#A2B38C',
        'tab6_inactive': '#DED8C4',           # Настройки
        'tab6_active': '#B3A885',
        
        # Цвета элементов интерфейса и виджетов
        'border_color': "#cccccc",            # Рамка фреймов
        'input_bg': "#f0f0f0",                # Фон полей ввода
        # Слайдеры
        'slider_trough': "#f0f0f0",           # Дорожка слайдера
        'slider_thumb': "#e0e0e0",            # Ползунок слайдера
        'slider_thumb_active': "#e0e0e0",     # Ползунок при активации
        'slider_frame': "#f0f0f0",            # Рамка слайдера
        # Полоса прокрутки
        'scrollbar_trough': "#f0f0f0",        # Дорожка прокрутки
        'scrollbar_slider': "#e0e0e0",        # Ползунок прокрутки
        'scrollbar_slider_active': "#e0e0e0", # Ползунок при активации
        'scrollbar_frame': "#f0f0f0",         # Рамка прокрутки
        'scrollbar_arrow': "#666666",         # Стрелки прокрутки        

        # Цвета кнопок
        'btn_color': "#e0e0e0",               # Маленькие кнопки (пресеты ступеней)
        'btn_hover': "#d0d0d0",               # ... при наведении
        'add_button': '#5D9730',              # Кнопка добавить
        'add_button_hover': '#508A23',        # ... при наведении
        'delete_button': '#F5564A',           # Кнопка удалить
        'delete_button_hover': '#D74444',     # ... при наведении
        # Цвета основных кнопок симуляции
        'fire_start': "#D2691E",              # Кнопка "Запуск 🔥"
        'fire_hover': "#B85A1A",              # ...при наведении
        'reset_color': "#6B8E23",             # Кнопка "Сброс"
        'reset_hover': "#5A771E",             # ...при наведении
        'new_graph_color': "#9370DB",         # Кнопка "Новый граф" и "Следующий граф"
        'new_graph_hover': "#7D5FC5",         # ...при наведении
        'insert_custom': '#7260A4',           # Кнопка "Вставить в Пользоватльский граф"
        'insert_custom_hover': '#5B4C82',     # ... при наведении
        'insert_sim': '#8B5F3F',              # Кнопка "Вставить в Сапуск симуляции"
        'insert_sim_hover': '#704C32',        # ... при наведении
        'insert_multi': '#876E38',            # Кнопка "Вставить в Множественную симуляцию"
        'insert_multi_hover': '#6C582D',      # ... при наведении
        'export_button': '#B4679D',           # Кнопка экспорта дданных
        'export_button_hover': '#904C7D',     # ... при наведении
        'batch_view_button': '#CAA306',       # Кнопка "Смотреть итоги"
        'batch_view_button_hover': '#A28205', # ... при наведении
        'apply_button': '#4a6fa5',            # Кнопка "Применить настройки"
        'apply_button_hover': '#3a5a84',      # ... при наведении

        # Цвета для плотности распределений и гистограмм
        'edge_density_color': "#2196f3",      # Ребра
        'vertex_density_color': "#c2185b",    # Вершины
        'palette_edge_stepwise': ['#80ccff', '#66b8ff', '#4da3f2', '#338fe6', '#1a7ad9', '#0066cc'],   # Ступени ребер
        'palette_vertex_stepwise': ['#ffe4ec', '#ffb7d5', '#ff8abf', '#ff5da8', '#ff3092', '#ff037b'], # Ступени вершин
        
        # Цвета элементов графа
        'graph_vertex': "#bbdefb",            # Фон негорящих вершин
        'graph_vertex_border': "#000000",     # Границы вершин
        # Цветовая шкала (градиент по точкам цвета)
        'custom_edge_cmap': ['#935CB7', '#ffffff', '#48883A'],  # Негорящие ребра
        'custom_fire_cmap': ['#B43628', '#E46F16', '#EEC10E'],  # Горящие ребра/вершины   
    },
    
    'theme_dark': {
        # Цвета фона
        'bg_color': "#1a1a1a",                # Основной фон приложения
        'frame_bg': "#1a1a1a",                # Фон рамок и панелей
        'plot_bg': "#1a1a1a",                 # Фон графиков
        
        # Цвета текста
        'text_color': "#ffffff",              # Основной текст
        'text_secondary': "#aaaaaa",          # Вторичный текст
        'btn_text': "#ffffff",                # Текст на кнопках
        'accent_color': "#5d8cc8",            # Акцентный цвет

        # Цвета вкладок в шапке
        'tab1_inactive': '#272946',           # Генерация графа
        'tab1_active': '#3B3E75',
        'tab2_inactive': '#322A49',           # Пользовательский граф
        'tab2_active': '#51427B',
        'tab3_inactive': '#3F2919',           # Запуск симуляции
        'tab3_active': '#6A4021',
        'tab4_inactive': '#402E0E',           # Множественная генерация
        'tab4_active': '#6C470C',
        'tab5_inactive': '#252D1A',           # Как пользоваться
        'tab5_active': '#374723',
        'tab6_inactive': '#353229',           # Настройки
        'tab6_active': '#57513E',
        
        # Цвета элементов интерфейса и виджетов
        'border_color': "#666666",            # Рамка фреймов
        'input_bg': "#444444",                # Фон полей ввода
        # Слайдеры
        'slider_trough': "#444444",           # Дорожка слайдера
        'slider_thumb': "#2d2d2d",            # Ползунок слайдера
        'slider_thumb_active': "#2d2d2d",     # Ползунок при активации
        'slider_frame': "#444444",            # Рамка слайдера
        # Полоса прокрутки
        'scrollbar_trough': "#444444",        # Дорожка прокрутки
        'scrollbar_slider': "#2d2d2d",        # Ползунок прокрутки
        'scrollbar_slider_active': "#2d2d2d", # Ползунок при активации
        'scrollbar_frame': "#444444",         # Рамка прокрутки
        'scrollbar_arrow': "#aaaaaa",         # Стрелки прокрутки        

        # Цвета кнопок
        'btn_color': "#2d2d2d",               # Маленькие кнопки (пресеты ступеней)
        'btn_hover': "#262626",               # ... при наведении
        'add_button': '#136717',              # Кнопка добавить
        'add_button_hover': '#257929',        # ... при наведении
        'delete_button': '#8C1818',           # Кнопка удалить
        'delete_button_hover': '#A62A2A',     # ... при наведении
        # Цвета основных кнопок симуляции
        'fire_start': "#E55C2E",              # Кнопка "Запуск 🔥"
        'fire_hover': "#FF7043",              # ...при наведении
        'reset_color': "#3E8C41",             # Кнопка "Сброс"
        'reset_hover': "#4CAF50",             # ...при наведении
        'new_graph_color': "#6A45A5",         # Кнопка "Новый граф" и "Следующий граф"
        'new_graph_hover': "#7E57C2",         # ...при наведении
        'insert_custom': '#403663',           # Кнопка "Вставить в Пользоватльский граф"
        'insert_custom_hover': '#52437C',     # ... при наведении
        'insert_sim': '#5C391F',              # Кнопка "Вставить в Сапуск симуляции"
        'insert_sim_hover': '#724728',        # ... при наведении
        'insert_multi': '#543F10',            # Кнопка "Вставить в Множественную симуляцию"
        'insert_multi_hover': '#6A4E14',      # ... при наведении
        'export_button': '#B4679D',           # Кнопка экспорта дданных
        'export_button_hover': '#D68FC0',     # ... при наведении
        'batch_view_button': '#F0B429',       # Кнопка "Смотреть итоги"
        'batch_view_button_hover': '#FFD966', # ... при наведении
        'apply_button': '#253E62',            # Кнопка "Применить настройки"
        'apply_button_hover': '#30496D',      # ... при наведении

        # Цвета для плотности распределений и гистограмм
        'edge_density_color': "#5d8cc8",      # Ребра
        'vertex_density_color': "#e91e63",    # Вершины
        'palette_edge_stepwise': ['#4d94ff', '#4282e7', '#3871d0', '#2d60b9', '#224fa3', '#183e8c'],   # Ступени ребер
        'palette_vertex_stepwise': ['#ff478c', '#e74282', '#d03d78', '#b9386e', '#a13364', '#8a2e5a'], # Ступени вершин
        
        # Цвета элементов графа
        'graph_vertex': "#37474f",            # Фон негорящих вершин
        'graph_vertex_border': "#ffffff",     # Границы вершин
        # Цветовая шкала (градиент по точкам цвета)
        'custom_edge_cmap': ['#633681', '#1A1A1A', '#276718'],  # Негорящие ребра
        'custom_fire_cmap': ['#BA1B10', '#CF5B18', '#CDA508'],  # Горящие ребра/вершины   
    },
}


# In[6]:


# Пресеты для вершин
VERTEX_TIER_PRESETS = {
    "market": {  # Рыночное распределение
        2: {"bounds": [(0.0, 0.2), (0.2, 1.0)], "counts": [80, 20]},
        3: {"bounds": [(0.0, 0.1), (0.1, 0.35), (0.35, 1.0)], "counts": [70, 20, 10]},
        4: {"bounds": [(0.0, 0.05), (0.05, 0.2), (0.2, 0.5), (0.5, 1.0)], "counts": [60, 25, 10, 5]},
        5: {"bounds": [(0.0, 0.05), (0.05, 0.15), (0.15, 0.35), (0.35, 0.65), (0.65, 1.0)], "counts": [50, 25, 15, 7, 3]},
        6: {"bounds": [(0.0, 0.05), (0.05, 0.13), (0.13, 0.25), (0.25, 0.45), (0.45, 0.75), (0.75, 1.0)], "counts": [40, 25, 15, 10, 7, 3]}
    },
    "oligopoly": {  # Олигополия
        2: {"bounds": [(0.0, 0.05), (0.05, 1.0)], "counts": [95, 5]},
        3: {"bounds": [(0.0, 0.05), (0.05, 0.25), (0.25, 1.0)], "counts": [85, 12, 3]},
        4: {"bounds": [(0.0, 0.05), (0.05, 0.15), (0.15, 0.35), (0.35, 1.0)], "counts": [75, 15, 7, 3]},
        5: {"bounds": [(0.0, 0.05), (0.05, 0.1), (0.1, 0.25), (0.25, 0.5), (0.5, 1.0)], "counts": [65, 20, 10, 4, 1]},
        6: {"bounds": [(0.0, 0.05), (0.05, 0.1), (0.1, 0.25), (0.25, 0.4), (0.4, 0.65), (0.65, 1.0)], "counts": [55, 25, 12, 5, 2, 1]}
    },
    "uniform_preset": {  # Равномерное
        2: {"bounds": [(0.0, 0.5), (0.5, 1.0)], "counts": [50, 50]},
        3: {"bounds": [(0.0, 0.33), (0.33, 0.66), (0.66, 1.0)], "counts": [33, 34, 33]},
        4: {"bounds": [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)], "counts": [25, 25, 25, 25]},
        5: {"bounds": [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)], "counts": [20, 20, 20, 20, 20]},
        6: {"bounds": [(0.0, 0.167), (0.167, 0.333), (0.333, 0.5), (0.5, 0.667), (0.667, 0.833), (0.833, 1.0)], "counts": [17, 17, 16, 17, 16, 17]}
    },
    "pyramid": {  # Пирамидальное
        2: {"bounds": [(0.0, 0.15), (0.15, 1.0)], "counts": [80, 20]},
        3: {"bounds": [(0.0, 0.08), (0.08, 0.35), (0.35, 1.0)], "counts": [70, 20, 10]},
        4: {"bounds": [(0.0, 0.05), (0.05, 0.25), (0.25, 0.55), (0.55, 1.0)], "counts": [60, 25, 10, 5]},
        5: {"bounds": [(0.0, 0.05), (0.05, 0.2), (0.2, 0.38), (0.38, 0.65), (0.65, 1.0)], "counts": [50, 25, 15, 7, 3]},
        6: {"bounds": [(0.0, 0.05), (0.05, 0.15), (0.15, 0.28), (0.28, 0.48), (0.48, 0.73), (0.73, 1.0)], "counts": [40, 25, 15, 10, 7, 3]}
    },
    "exponential": {  # Экспоненциальное
        2: {"bounds": [(0.0, 0.1), (0.1, 1.0)], "counts": [90, 10]},
        3: {"bounds": [(0.0, 0.05), (0.05, 0.25), (0.25, 1.0)], "counts": [80, 15, 5]},
        4: {"bounds": [(0.0, 0.05), (0.05, 0.15), (0.15, 0.4), (0.4, 1.0)], "counts": [70, 20, 8, 2]},
        5: {"bounds": [(0.0, 0.05), (0.05, 0.1), (0.1, 0.25), (0.25, 0.5), (0.5, 1.0)], "counts": [60, 25, 10, 4, 1]},
        6: {"bounds": [(0.0, 0.05), (0.05, 0.1), (0.1, 0.2), (0.2, 0.35), (0.35, 0.6), (0.6, 1.0)], "counts": [50, 25, 15, 6, 3, 1]}
    }
}

# Пресеты для ребер
EDGE_TIER_PRESETS = {
    "social": {  # Социальные связи
        2: {"bounds": [(-1.0, -0.5), (-0.5, 1.0)], "counts": [70, 30]},
        3: {"bounds": [(-1.0, -0.6), (-0.6, -0.1), (-0.1, 1.0)], "counts": [70, 25, 5]},
        4: {"bounds": [(-1.0, -0.7), (-0.7, -0.3), (-0.3, 0.2), (0.2, 1.0)], "counts": [60, 25, 10, 5]},
        5: {"bounds": [(-1.0, -0.8), (-0.8, -0.5), (-0.5, -0.1), (-0.1, 0.3), (0.3, 1.0)], "counts": [50, 25, 15, 7, 3]},
        6: {"bounds": [(-1.0, -0.85), (-0.85, -0.6), (-0.6, -0.3), (-0.3, 0.1), (0.1, 0.5), (0.5, 1.0)], "counts": [40, 25, 20, 10, 4, 1]}
    },
    "economic": {  # Экономические потоки
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [60, 40]},
        3: {"bounds": [(-1.0, -0.4), (-0.4, 0.2), (0.2, 1.0)], "counts": [50, 35, 15]},
        4: {"bounds": [(-1.0, -0.6), (-0.6, -0.1), (-0.1, 0.4), (0.4, 1.0)], "counts": [40, 35, 20, 5]},
        5: {"bounds": [(-1.0, -0.7), (-0.7, -0.3), (-0.3, 0.1), (0.1, 0.5), (0.5, 1.0)], "counts": [35, 30, 20, 12, 3]},
        6: {"bounds": [(-1.0, -0.8), (-0.8, -0.5), (-0.5, -0.1), (-0.1, 0.3), (0.3, 0.7), (0.7, 1.0)], "counts": [30, 25, 20, 15, 8, 2]}
    },
    "information": {  # Информационные каналы
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [40, 60]},
        3: {"bounds": [(-1.0, -0.3), (-0.3, 0.3), (0.3, 1.0)], "counts": [30, 50, 20]},
        4: {"bounds": [(-1.0, -0.5), (-0.5, 0.0), (0.0, 0.5), (0.5, 1.0)], "counts": [25, 40, 25, 10]},
        5: {"bounds": [(-1.0, -0.65), (-0.65, -0.2), (-0.2, 0.2), (0.2, 0.6), (0.6, 1.0)], "counts": [20, 35, 25, 15, 5]},
        6: {"bounds": [(-1.0, -0.75), (-0.75, -0.4), (-0.4, 0.0), (0.0, 0.4), (0.4, 0.75), (0.75, 1.0)], "counts": [15, 30, 25, 20, 8, 2]}
    },
    "hierarchical": {  # Иерархическая структура
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [80, 20]},
        3: {"bounds": [(-1.0, -0.3), (-0.3, 0.3), (0.3, 1.0)], "counts": [70, 25, 5]},
        4: {"bounds": [(-1.0, -0.5), (-0.5, 0.0), (0.0, 0.5), (0.5, 1.0)], "counts": [60, 25, 10, 5]},
        5: {"bounds": [(-1.0, -0.65), (-0.65, -0.2), (-0.2, 0.2), (0.2, 0.65), (0.65, 1.0)], "counts": [50, 25, 15, 8, 2]},
        6: {"bounds": [(-1.0, -0.75), (-0.75, -0.4), (-0.4, 0.0), (0.0, 0.4), (0.4, 0.75), (0.75, 1.0)], "counts": [40, 25, 20, 10, 4, 1]}
    },
    "ecosystem": {  # Экосистемные связи
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [40, 60]},
        3: {"bounds": [(-1.0, -0.25), (-0.25, 0.25), (0.25, 1.0)], "counts": [25, 50, 25]},
        4: {"bounds": [(-1.0, -0.4), (-0.4, 0.0), (0.0, 0.4), (0.4, 1.0)], "counts": [25, 35, 30, 10]},
        5: {"bounds": [(-1.0, -0.5), (-0.5, -0.1), (-0.1, 0.3), (0.3, 0.7), (0.7, 1.0)], "counts": [20, 30, 30, 15, 5]},
        6: {"bounds": [(-1.0, -0.6), (-0.6, -0.25), (-0.25, 0.1), (0.1, 0.45), (0.45, 0.75), (0.75, 1.0)], "counts": [15, 25, 30, 20, 8, 2]}
    },
    "infrastructure": {  # Критическая инфраструктура
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [40, 60]},
        3: {"bounds": [(-1.0, -0.4), (-0.4, 0.4), (0.4, 1.0)], "counts": [20, 60, 20]},
        4: {"bounds": [(-1.0, -0.5), (-0.5, 0.0), (0.0, 0.5), (0.5, 1.0)], "counts": [15, 50, 25, 10]},
        5: {"bounds": [(-1.0, -0.6), (-0.6, -0.2), (-0.2, 0.2), (0.2, 0.6), (0.6, 1.0)], "counts": [10, 40, 30, 15, 5]},
        6: {"bounds": [(-1.0, -0.7), (-0.7, -0.3), (-0.3, 0.1), (0.1, 0.5), (0.5, 0.8), (0.8, 1.0)], "counts": [8, 35, 30, 20, 5, 2]}
    },
    "epidemic": {  # Эпидемиологическая
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [85, 15]},
        3: {"bounds": [(-1.0, -0.3), (-0.3, 0.3), (0.3, 1.0)], "counts": [70, 20, 10]},
        4: {"bounds": [(-1.0, -0.5), (-0.5, 0.0), (0.0, 0.5), (0.5, 1.0)], "counts": [60, 25, 10, 5]},
        5: {"bounds": [(-1.0, -0.6), (-0.6, -0.2), (-0.2, 0.2), (0.2, 0.6), (0.6, 1.0)], "counts": [50, 30, 12, 6, 2]},
        6: {"bounds": [(-1.0, -0.7), (-0.7, -0.35), (-0.35, 0.0), (0.0, 0.35), (0.35, 0.7), (0.7, 1.0)], "counts": [40, 25, 20, 10, 4, 1]}
    },
    "uniform_preset": {  # Равномерное
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [50, 50]},
        3: {"bounds": [(-1.0, -0.33), (-0.33, 0.33), (0.33, 1.0)], "counts": [33, 34, 33]},
        4: {"bounds": [(-1.0, -0.5), (-0.5, 0.0), (0.0, 0.5), (0.5, 1.0)], "counts": [25, 25, 25, 25]},
        5: {"bounds": [(-1.0, -0.6), (-0.6, -0.2), (-0.2, 0.2), (0.2, 0.6), (0.6, 1.0)], "counts": [20, 20, 20, 20, 20]},
        6: {"bounds": [(-1.0, -0.66), (-0.66, -0.33), (-0.33, 0.0), (0.0, 0.33), (0.33, 0.66), (0.66, 1.0)], "counts": [17, 17, 16, 17, 16, 17]}
    }
}


# In[7]:


PARAM_CONFIG = { # Словарь допустимых значений параметров
    'global': {
        'gap': 0.05,                                    # Минимальный зазор между левой и правой границей в распределениях
        'tolerance': 1e-10,                             # Точность сравнения для чисел с плавающей точкой
        'max_stages': 6,                                # Максимальное количество ступеней в ступенчатом распределении

        'resistance_coeff': {'range': (0.0, 1.0), 'is_int': False},          # Коэффициент устойчивости
        'influence_coeff': {'range': (0.0, 1.0), 'is_int': False},           # Коэффициент влияния
        'damping_coeff': {'range': (0.0, 1.0), 'is_int': False},             # Коэффициент затухания
        
        'vertex_count': {'range': (2, 200), 'is_int': True},                 # Количество вершин в графе
        'start_vertex': {'range': (1, 200), 'is_int': True},                 # Номер стартовой вершины (1-индексация)
        'bins_count': {'range': (5, 20), 'is_int': True},                    # Количество интервалов (бинов) в гистограмме
        
        'batch_graphs_count': {'range': (1, 100), 'is_int': True},           # Количество графов в пакетной генерации
        'batch_start_vertices_count': {'range': (1, 200), 'is_int': True},   # Количество стартовых вершин в пакетной симуляции
        'batch_simulations_per_vertex': {'range': (1, 100), 'is_int': True}, # Количество симуляций на одну вершину
        
        'font_size': {'range': (8, 15), 'is_int': True},                     # Размер шрифта интерфейса в пунктах
        'seed_value': {'range': (1, 99999), 'is_int': True},                 # Значение seed для генерации случайных чисел
        'max_vertices': {'range': (100, 1000), 'is_int': True},              # Максимально допустимое количество вершин в графе
        'threshold_value': {'range': (0.0, 1.0), 'is_int': False},           # Пороговое значение для метода поджога
        'threshold_add_vertex': {'range': (1, 10), 'is_int': True},          # Порог добавления вершин для перестроения графа
        'default_vertex_count': {'range': (1, 200), 'is_int': True},         # Количество вершин в графе по умолчанию
        'default_vertex_weight': {'range': (0.01, 1.0), 'is_int': False},    # Вес вершины по умолчанию
        'default_edge_weight': {'range': (-1.0, 1.0), 'is_int': False},      # Вес ребра по умолчанию
        'max_batch_graphs': {'range': (10, 1000), 'is_int': True},           # Максимальное количество графов в пакетной генерации
        'max_batch_simulations': {'range': (10, 1000), 'is_int': True},      # Максимальное количество симуляций на одну вершину
        'rounding_input': {'range': (2, 10), 'is_int': True},                # Количество знаков после запятой в полях ввода
        'rounding_stats': {'range': (2, 10), 'is_int': True},                # Количество знаков после запятой в статистиках
    },
    
    'edge': {
        'Uniform': {
            'left': {'range': (-1.0, 0.95), 'sync_with': 'right', 'is_int': False},
            'right': {'range': (-0.95, 1.0), 'sync_with': 'left', 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.uniform(n, p['left'], p['right'], rng),
            'plot_update': lambda plot, vars: plot.update_uniform(vars['left'].get(), vars['right'].get()),
            'ui_type': 'dual',
            'param_order': ['left', 'right']
        },
        'Normal': {
            'mean': {'range': (-1.0, 1.0), 'is_int': False},
            'std': {'range': (0.01, 1.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.normal(n, p['mean'], p['std'], -1, 1, rng),
            'plot_update': lambda plot, vars: plot.update_normal(vars['mean'].get(), vars['std'].get()),
            'ui_type': 'standard',
            'param_order': ['mean', 'std']
        },
        'Student': {
            'df': {'range': (1.0, 30.0), 'is_int': False},
            'scale': {'range': (0.01, 1.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.student(n, p['df'], p['scale'], -1, 1, rng),
            'plot_update': lambda plot, vars: plot.update_student(vars['df'].get(), vars['scale'].get()),
            'ui_type': 'standard',
            'param_order': ['df', 'scale']
        },
        'Laplace': {
            'loc': {'range': (-1.0, 1.0), 'is_int': False},
            'scale': {'range': (0.01, 1.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.laplace(n, p['loc'], p['scale'], -1, 1, rng),
            'plot_update': lambda plot, vars: plot.update_laplace(vars['loc'].get(), vars['scale'].get()),
            'ui_type': 'standard',
            'param_order': ['loc', 'scale']
        },
        'Bimodal': {
            'mu1': {'range': (-1.0, 1.0), 'is_int': False},
            'sigma1': {'range': (0.01, 1.0), 'is_int': False},
            'mu2': {'range': (-1.0, 1.0), 'is_int': False},
            'sigma2': {'range': (0.01, 1.0), 'is_int': False},
            'weight': {'range': (0.0, 1.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.bimodal(n, p['mu1'], p['sigma1'], p['mu2'], p['sigma2'], p['weight'], -1, 1, rng),
            'plot_update': lambda plot, vars: plot.update_bimodal(vars['mu1'].get(), vars['sigma1'].get(),
                                                                  vars['mu2'].get(), vars['sigma2'].get(), vars['weight'].get()),
            'ui_type': 'standard',
            'param_order': ['mu1', 'sigma1', 'mu2', 'sigma2', 'weight']
        },
        'Skewed_t': {
            'df': {'range': (1.0, 30.0), 'is_int': False},
            'shape': {'range': (-2.0, 2.0), 'is_int': False},
            'scale': {'range': (0.01, 1.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.skewed_t(n, p['df'], p['shape'], p['scale'], -1, 1, rng),
            'plot_update': lambda plot, vars: plot.update_skewed_t(vars['df'].get(), vars['shape'].get(), vars['scale'].get()),
            'ui_type': 'standard',
            'param_order': ['df', 'shape', 'scale']
        },
        'Stepwise': {
            'stage': {
                'left': {'range': (-1.0, 0.95), 'sync_with': 'right', 'is_int': False},
                'right': {'range': (-0.95, 1.0), 'sync_with': 'left', 'is_int': False},
                'weight': {'range': (1, 100), 'is_int': True}
            },
            'generator': lambda n, p, rng: DistributionGenerator.stepwise(n, p['stages'], -1, 1, rng),
            'plot_update': lambda plot, vars: plot.update_stepwise(vars['stages']),
            'ui_type': 'stepwise',
            'param_order': ['stages']
        }
    },
    
    'vertex': {
        'None': {
            'generator': lambda n, p, rng: None,
            'plot_update': lambda plot, vars: None,
            'ui_type': 'none',
            'param_order': []
        },
        'Uniform': {
            'left': {'range': (0.0, 0.95), 'sync_with': 'right', 'is_int': False},
            'right': {'range': (0.05, 1.0), 'sync_with': 'left', 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.uniform(n, p['left'], p['right'], rng),
            'plot_update': lambda plot, vars: plot.update_uniform(vars['left'].get(), vars['right'].get()),
            'ui_type': 'dual',
            'param_order': ['left', 'right']
        },
        'Normal': {
            'mean': {'range': (0.0, 1.0), 'is_int': False},
            'std': {'range': (0.01, 1.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.normal(n, p['mean'], p['std'], 0, 1, rng),
            'plot_update': lambda plot, vars: plot.update_normal(vars['mean'].get(), vars['std'].get()),
            'ui_type': 'standard',
            'param_order': ['mean', 'std']
        },
        'Lognormal': {
            'gamma': {'range': (0.0, 0.5), 'is_int': False},
            'mu': {'range': (-3.0, 1.0), 'is_int': False},
            'sigma': {'range': (0.01, 2.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.lognormal(n, p['gamma'], p['mu'], p['sigma'], 0, 1, rng),
            'plot_update': lambda plot, vars: plot.update_lognormal(vars['gamma'].get(), vars['mu'].get(), vars['sigma'].get()),
            'ui_type': 'standard',
            'param_order': ['gamma', 'mu', 'sigma']
        },
        'Bimodal': {
            'mu1': {'range': (0.0, 1.0), 'is_int': False},
            'sigma1': {'range': (0.01, 1.0), 'is_int': False},
            'mu2': {'range': (0.0, 1.0), 'is_int': False},
            'sigma2': {'range': (0.01, 1.0), 'is_int': False},
            'weight': {'range': (0.0, 1.0), 'is_int': False},
            'generator': lambda n, p, rng: DistributionGenerator.bimodal(n, p['mu1'], p['sigma1'], p['mu2'], p['sigma2'], p['weight'], 0, 1, rng),
            'plot_update': lambda plot, vars: plot.update_bimodal(vars['mu1'].get(), vars['sigma1'].get(),
                                                                  vars['mu2'].get(), vars['sigma2'].get(), vars['weight'].get()),
            'ui_type': 'standard',
            'param_order': ['mu1', 'sigma1', 'mu2', 'sigma2', 'weight']
        },
        'Stepwise': {
            'stage': {
                'left': {'range': (0.0, 0.95), 'sync_with': 'right', 'is_int': False},
                'right': {'range': (0.05, 1.0), 'sync_with': 'left', 'is_int': False},
                'weight': {'range': (1, 100), 'is_int': True}
            },
            'generator': lambda n, p, rng: DistributionGenerator.stepwise(n, p['stages'], 0, 1, rng),
            'plot_update': lambda plot, vars: plot.update_stepwise(vars['stages']),
            'ui_type': 'stepwise',
            'param_order': ['stages']
        }
    },
    
    'vertex_card': {'weight': {'range': (0.01, 1.0), 'is_int': False}},
    'edge_card': {'weight': {'range': (-1.0, 1.0), 'is_int': False}},
}


# In[8]:


FONT_CONFIG = {
    'default_family': 'Segoe UI', # Семейство шрифтов
    'default_size': 10,           # Базовый размер шрифта
    
    'styles': {
        'tab':         {'offset': 1, 'bold': True,  'color_key': 'text_color'},      # Заголовки вкладкок
        
        'header':      {'offset': 0, 'bold': True,  'color_key': 'accent_color'},    # Заголовок секций
        'normal':      {'offset': 0, 'bold': False, 'color_key': 'text_color'},      # Обычный текст
        'small':       {'offset': -1, 'bold': False, 'color_key': 'text_color'},     # Маленький текст (в статистиках)
        'small_bold':  {'offset': -1, 'bold': True,  'color_key': 'text_color'},     # Маленький жирный текст (в статистиках)
        'secondary':   {'offset': -1, 'bold': False, 'color_key': 'text_secondary'}, # Второстепенный текст
        'card_header': {'offset': -1, 'bold': True, 'color_key': 'accent_color'},    # Заголовки карточек ступенчатых распределений
        
        'button_large':   {'offset': 0, 'bold': True, 'color_key': 'btn_text'},      # Большие кнопки (основные действия)
        'button_small':   {'offset': -1, 'bold': True, 'color_key': 'text_color'},   # Маленькие кнопки (названия пресетов ступеней)
        'button_icon':    {'offset': 0, 'bold': True, 'color_key': 'btn_text'},      # Кнопки с иконкой (удалить, добавить)
        
        'entry':          {'offset': 0, 'bold': False, 'color_key': 'text_color'},   # Поле ввода
        'combobox':       {'offset': 0, 'bold': False, 'color_key': 'text_color'},   # Комбобокс
        'table_header':   {'offset': 1, 'bold': True,  'color_key': 'text_color'},   # Заголовки таблиц
        'table_cell':     {'offset': 0, 'bold': False, 'color_key': 'text_color'},   # Ячейки таблиц 
    },
}


# In[9]:


SIZE_CONFIG = { # Словарь размеров элементов интерфейса
    'container': { # Размеры фреймов с содержимым
        'tab_bar': {'height': 30},               # Высота шапки с заголовками вкладок
        'side_panel': {'width': 200},            # Ширина боковой панели
        'graph_panel': {'height': 500},          # Высота фрейма с графом
        
        'vertex_table': {'height': 90},          # Таблица вершин (на вкладке Пользовательского графа)
        'edge_table': {'height': 450},           # Таблица ребер (на вкладке Пользовательского графа)
        'start_vertices_table': {'height': 70},  # Таблица вершин (на вкладке Множественной генерации)
        'result_table': {'max_height': 500},     # Таблица итогов (на вкладке Множественной генерации)
        
        'button_group': {'height': 100},                      # Высота фрейма с большими кнопками
        'preset_row': {'height': 25},                         # Высота фрейма с кнопками пресетов для ступеней
        'stepwise_card': {'width': 220, 'min_height': 180},   # Карточки ступеней
    },
    
    'virtual_table': {'cell_width': 60, 'cell_height': 25,},  # Размеря ячеек в таблицах ребер и вершин
    
    'control': { # Размеры виджетов
        'entry': {'default': 6, 'tiny': 3, },                 # Поле ввода
        'combobox': {'default': 20, 'wide': 32, },            # Выпадающий список
        'scale': {'normal': 200, 'long': 500, 'short': 90, 'normal_no_entry': 256, }, # Слайдер
    },
}


# In[10]:


BUTTON_CONFIG = { # Словарь конфигурации кнопок
    'fire': { # Кнопка Запуск
        'bg_key': 'fire_start',
        'hover_key': 'fire_hover',
        'text_color_key': 'btn_text',
        'size': 'medium',
        'font_style': 'button_large',
    },
    'reset': { # Кнопка Сброс
        'bg_key': 'reset_color',
        'hover_key': 'reset_hover',
        'text_color_key': 'btn_text',
        'size': 'medium',
        'font_style': 'button_large',
    },
    'new_graph': { # Кнопка Новый граф / Следующий граф
        'bg_key': 'new_graph_color',
        'hover_key': 'new_graph_hover',
        'text_color_key': 'btn_text',
        'size': 'medium',
        'font_style': 'button_large',
    },
    'insert_custom': { # Кнопка Вставить в Пользовательский граф / Сбросить пользовательский граф к дефолту
        'bg_key': 'insert_custom',
        'hover_key': 'insert_custom_hover',
        'text_color_key': 'btn_text',
        'size': 'large',
        'font_style': 'button_large',
    },
    'insert_sim': { # Кнопка Вставить в Запуск симуляции
        'bg_key': 'insert_sim',
        'hover_key': 'insert_sim_hover',
        'text_color_key': 'btn_text',
        'size': 'large',
        'font_style': 'button_large',
    },
    'insert_multi': { # Кнопка Вставить в Пользовательский граф
        'bg_key': 'insert_multi',
        'hover_key': 'insert_multi_hover',
        'text_color_key': 'btn_text',
        'size': 'large',
        'font_style': 'button_large',
    },
    'export': { # Кнопка Экспортировать данные в PDF / CSV
        'bg_key': 'export_button',
        'hover_key': 'export_button_hover',
        'text_color_key': 'btn_text',
        'size': 'large',
        'font_style': 'button_large',
    },
    'insert_sim_compact': { # Компактные версии для таблицы результатов
        'bg_key': 'insert_sim',
        'hover_key': 'insert_sim_hover',
        'text_color_key': 'btn_text',
        'size': 'compact',
        'font_style': 'button_large',
    },
    'export_compact': { # Компактные версии для таблицы результатов
        'bg_key': 'export_button',
        'hover_key': 'export_button_hover',
        'text_color_key': 'btn_text',
        'size': 'compact',
        'font_style': 'button_large',
    },
    'batch_view_compact': { # Компактные версии для таблицы результатов
        'bg_key': 'batch_view_button',
        'hover_key': 'batch_view_button_hover',
        'text_color_key': 'btn_text',
        'size': 'compact',
        'font_style': 'button_large',
    },
    'apply': { # Кнопка Применить настройки
        'bg_key': 'apply_button',
        'hover_key': 'apply_button_hover',
        'text_color_key': 'btn_text',
        'size': 'large',
        'font_style': 'button_large',
    },
    'preset': { # Кнопки пресетов ступенчатых распределений
        'bg_key': 'btn_color',
        'hover_key': 'btn_hover',
        'text_color_key': 'text_color',
        'size': 'small',
        'font_style': 'button_small',
    },
    'icon_add': { # Кнопка Добавить
        'bg_key': 'add_button',
        'hover_key': 'add_button_hover',
        'text_color_key': 'btn_text',
        'size': 'icon',
        'font_style': 'button_icon',
        'icon': '➕',
    },
    'icon_delete': { # Кнопка Удалить
        'bg_key': 'delete_button',
        'hover_key': 'delete_button_hover',
        'text_color_key': 'btn_text',
        'size': 'icon',
        'font_style': 'button_icon',
        'icon': '✕',
    },
}

# Размеры кнопок
BUTTON_SIZES = {
    'large': {'min_width': 40, 'min_height': 2},
    'medium': {'min_width': 10, 'min_height': 2},
    'compact': {'min_width': 25, 'min_height': 1},
    'small': {'min_width': 20, 'min_height': 1},
    'icon': {'width': 3, 'height': 1},
}


# In[11]:


class Translator:
    """Класс перевода текстов интерфейса с поддержкой обратного поиска ключа"""
    
    def __init__(self, language='RU'):
        """Инициализация переводчика для указанного языка"""
        self.language = language  # Текущий язык перевода
        self._reverse = {}  # Обратный словарь {перевод: оригинальный_ключ}
        self._build_reverse_dict()  # Построение обратного словаря при инициализации
    
    def _build_reverse_dict(self):
        """Строит обратный словарь {перевод: ключ} для текущего языка"""
        self._reverse.clear()  # Очистка старого обратного словаря
        for key, value in TRANSLATIONS[self.language].items():  # Перебор всех переводов текущего языка
            if value:  # Пропуск пустых строк (без перевода)
                self._reverse[value] = key  # Добавление пары перевод -> ключ
    
    def t(self, key):
        """Возвращает перевод для указанного ключа"""
        return TRANSLATIONS[self.language].get(key, key)  # Поиск перевода или возврат ключа при отсутствии
    
    def to_key(self, translated_value):
        """Возвращает оригинальный ключ по его переводу"""
        return self._reverse.get(translated_value, translated_value)  # Поиск ключа или возврат перевода при отсутствии
    
    def set_language(self, language):
        """Меняет текущий язык и перестраивает обратный словарь"""
        self.language = language  # Установка нового языка
        self._build_reverse_dict()  # Перестроение обратного словаря для нового языка


# In[12]:


class ThemeManager:
    """Класс цветов интерфейса в зависимости от установленной темы"""
    
    def __init__(self, theme='theme_light'):
        """Инициализация менеджера тем с указанной темой"""
        self.theme = theme  # Текущая тема оформления ('theme_light' или 'theme_dark')
    
    def get_color(self, color_name):
        """Возвращает цвет по имени для текущей темы"""
        return THEME_COLORS[self.theme][color_name]  # Получение цвета из словаря тем по имени
    
    def get_palette(self, palette_name):
        """Возвращает палитру по имени для текущей темы"""
        key = f'palette_{palette_name}'  # Формирование ключа палитры (например, 'palette_edge_stepwise')
        return THEME_COLORS[self.theme][key]  # Получение палитры из словаря тем
    
    def set_theme(self, theme):
        """Меняет текущую тему оформления"""
        self.theme = theme  # Установка новой темы


# In[13]:


class GraphData:
    """Класс с инфо о графе"""
    
    def __init__(self, app=None):
        """Инициализация пустого графа с параметрами по умолчанию"""
        self.graph = nx.Graph()  # Пустой граф NetworkX
        self._app = app  # Ссылка на главное приложение
        self.pos_cache = None  # Кэш позиций вершин графа {node: (x, y)}
        self.generation_params = None  # Параметры генерации графа (если был сгенерирован)
        self.resistance_type = 'None'  # Тип устойчивости
        self.resistance_coeff = 0.5  # Коэффициент устойчивости
        self.influence_type = 'None'  # Тип влияния
        self.influence_coeff = 0.5  # Коэффициент влияния
        self.damping_type = 'None'  # Тип затухания
        self.damping_coeff = 0.5  # Коэффициент затухания
        self.source_tab = "tab_custom"  # Название вкладки-источника графа
        self.source_graph_index = None  # Индекс графа при множественной генерации
        self.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Время вставки графа в текущую вкладку
        self._graph_seed = None  # Базовый seed графа (отправная точка для всех симуляций)
        self._graph_seed_mode = 'seed_fixed'  # Режим seed ('seed_fixed' или 'seed_random')
        self._graph_rng = None  # Генератор графа (состояние продвигается с каждой симуляцией)
        self._sim_counter = 0  # Счетчик выполненных симуляций на этом графе

    @property
    def graph_seed(self):
        """Возвращает текущий seed графа"""
        return self._graph_seed
    
    @graph_seed.setter
    def graph_seed(self, value):
        """Устанавливает seed графа"""
        self._graph_seed = value
    
    @property
    def graph_seed_mode(self):
        """Возвращает режим seed графа"""
        return self._graph_seed_mode
    
    @graph_seed_mode.setter
    def graph_seed_mode(self, value):
        """Устанавливает режим seed графа"""
        self._graph_seed_mode = value

    def init_graph_rng(self, global_rng=None):
        """Инициализация генератора графа на основе graph_seed"""
        if self._graph_seed is None:
            if global_rng is not None:  # Генерация seed от глобального генератора
                self._graph_seed = global_rng.randint(1, 999999)
            else:  # Резервный вариант со стандартным random
                self._graph_seed = random.randint(1, 999999)
        self._graph_rng = random.Random(self._graph_seed)  # Создание генератора с заданным seed
        self._sim_counter = 0  # Сброс счетчика симуляций
        return self._graph_rng

    def get_sim_rng(self):
        """Возвращает копию rng для следующей симуляции с продвижением счетчика"""
        if self._graph_rng is None:
            self.init_graph_rng()
        current_state = self._graph_rng.getstate()  # Сохранение текущего состояния генератора
        self._graph_rng.random()  # Продвижение оригинального генератора на один шаг
        self._sim_counter += 1  # Увеличение счетчика симуляций
        result_rng = random.Random()  # Создание нового генератора
        result_rng.setstate(current_state)  # Восстановление сохраненного состояния
        return result_rng
    
    def get_sim_counter(self):
        """Возвращает количество симуляций, выполненных на этом графе"""
        return self._sim_counter
    
    def set_graph_seed(self, seed_value, mode='seed_fixed'):
        """Устанавливает seed графа и переинициализирует генератор"""
        self._graph_seed = seed_value  # Сохранение значения seed
        self._graph_seed_mode = mode  # Сохранение режима seed
        self._graph_rng = random.Random(seed_value)  # Создание нового генератора с seed
        self._sim_counter = 0  # Сброс счетчика симуляций
    
    def get_graph_seed(self):
        """Возвращает текущий seed графа"""
        return self._graph_seed
    
    def get_graph_seed_mode(self):
        """Возвращает режим seed графа"""
        return self._graph_seed_mode
    
    def copy(self):
        """Создание полной копии графа с сохранением состояния симуляций"""
        new_data = GraphData(app=self._app)  # Создание нового экземпляра
        new_data.graph = self.graph.copy()  # Копирование графа
        new_data.generation_params = copy.deepcopy(self.generation_params) if self.generation_params is not None else None  # Глубокое копирование
        new_data.pos_cache = copy.deepcopy(self.pos_cache) if self.pos_cache else None  # Глубокое копирование кэша позиций
        new_data.resistance_type = self.resistance_type  # Копирование типа устойчивости
        new_data.resistance_coeff = self.resistance_coeff  # Копирование коэффициента устойчивости
        new_data.influence_type = self.influence_type  # Копирование типа влияния
        new_data.influence_coeff = self.influence_coeff  # Копирование коэффициента влияния
        new_data.damping_type = self.damping_type  # Копирование типа затухания
        new_data.damping_coeff = self.damping_coeff  # Копирование коэффициента затухания
        new_data.source_tab = self.source_tab  # Копирование вкладки-источника
        new_data.source_graph_index = self.source_graph_index  # Копирование индекса графа
        new_data.insert_time = self.insert_time  # Копирование времени вставки
        new_data._graph_seed = self._graph_seed  # Копирование seed графа
        new_data._graph_seed_mode = self._graph_seed_mode  # Копирование режима seed
        new_data._sim_counter = self._sim_counter  # Копирование счетчика симуляций
        if self._graph_rng is not None:  # Копирование состояния генератора
            new_data._graph_rng = random.Random()  # Создание нового генератора
            new_data._graph_rng.setstate(self._graph_rng.getstate())  # Восстановление сохраненного состояния
        else:
            new_data._graph_rng = None
        return new_data
    
    def set_default(self, app=None):
        """Установка графа по умолчанию с параметрами из настроек"""
        n = app.settings['default_vertex_count'].get()  # Количество вершин из настроек
        vertex_weight = app.settings['default_vertex_weight'].get()  # Вес вершин из настроек
        edge_weight = app.settings['default_edge_weight'].get()  # Вес ребер из настроек
        self.graph = nx.Graph()  # Создание пустого графа
        for i in range(n):  # Добавление вершин
            self.graph.add_node(f'V{i}', weight=vertex_weight)
        for i in range(n):  # Добавление ребер между всеми парами вершин
            for j in range(i+1, n):
                self.graph.add_edge(f'V{i}', f'V{j}', weight=edge_weight)
        self.generation_params = None  # Сброс параметров генерации
        self.resistance_type = 'None'  # Сброс типа устойчивости
        self.resistance_coeff = 0.5  # Сброс коэффициента устойчивости
        self.influence_type = 'None'  # Сброс типа влияния
        self.influence_coeff = 0.5  # Сброс коэффициента влияния
        self.damping_type = 'None'  # Сброс типа затухания
        self.damping_coeff = 0.5  # Сброс коэффициента затухания
        self.source_tab = 'tab_custom'  # Установка вкладки-источника
        self.source_graph_index = None  # Сброс индекса графа
        self.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Время создания графа
        self._graph_seed = None  # Сброс seed графа
        self._graph_seed_mode = 'seed_fixed'  # Установка режима seed по умолчанию
        self._graph_rng = None  # Сброс генератора
        self._sim_counter = 0  # Сброс счетчика симуляций
    
    def get_vertex(self, index):
        """Возвращает вес вершины по индексу"""
        node = f'V{index}'  # Имя вершины по индексу
        return self.graph.nodes[node]['weight']  # Чтение веса из атрибутов вершины
    
    def get_all_vertices(self):
        """Возвращает список весов всех вершин"""
        return [self.graph.nodes[f'V{i}']['weight'] for i in range(self.graph.number_of_nodes())]  # Сбор весов всех вершин
    
    def get_edge_weight(self, i, j):
        """Возвращает вес ребра между вершинами i и j"""
        node_i, node_j = f'V{i}', f'V{j}'  # Имена вершин по индексам
        return self.graph[node_i][node_j]['weight']  # Чтение веса из атрибутов ребра
    
    def add_vertex(self, weight=None):
        """Добавление вершины в конец с возвратом индекса"""
        n = self.graph.number_of_nodes()  # Текущее количество вершин
        node = f'V{n}'  # Имя новой вершины
        if weight is None and hasattr(self, '_app') and self._app:  # Вес не указан
            weight = self._app.settings['default_vertex_weight'].get()  # Использование веса из настроек
        self.graph.add_node(node, weight=weight)  # Добавление вершины в граф
        return n  # Возврат индекса новой вершины
    
    def remove_vertex(self, index):
        """Удаление вершины по индексу с перенумерацией оставшихся"""
        node = f'V{index}'  # Имя удаляемой вершины
        self.graph.remove_node(node)  # Удаление вершины из графа
        remaining_nodes = list(self.graph.nodes())  # Список оставшихся вершин
        remaining_nodes.sort(key=lambda x: int(x[1:]))  # Сортировка по числовому индексу
        mapping = {old: f'V{i}' for i, old in enumerate(remaining_nodes)}  # Маппинг старых имен на новые
        self.graph = nx.relabel_nodes(self.graph, mapping)  # Переименование вершин
    
    def update_vertex(self, index, new_weight):
        """Изменение веса вершины по индексу"""
        node = f'V{index}'  # Имя целевой вершины
        self.graph.nodes[node]['weight'] = new_weight  # Обновление веса
    
    def update_edge(self, i, j, new_weight=None):
        """Изменение веса ребра между вершинами i и j"""
        node_i, node_j = f'V{i}', f'V{j}'  # Имена вершин
        if new_weight is None and hasattr(self, '_app') and self._app:  # Вес не указан
            new_weight = self._app.settings['default_edge_weight'].get()  # Использование веса из настроек
        if self.graph.has_edge(node_i, node_j):  # Ребро уже существует
            self.graph[node_i][node_j]['weight'] = new_weight  # Обновление существующего ребра
        else:  # Ребра нет
            self.graph.add_edge(node_i, node_j, weight=new_weight)  # Создание нового ребра

    def set_graph_from_params(self, params, generator, global_rng):
        """Заполнение графа из параметров генерации с использованием глобального rng"""
        self.graph = generator.generate(params, global_rng)  # Генерация графа
        self.generation_params = copy.deepcopy(params)  # Сохранение параметров генерации

    def set_resistance(self, resistance_type, resistance_coeff):
        """Установка параметров устойчивости"""
        self.resistance_type = resistance_type  # Тип устойчивости
        self.resistance_coeff = resistance_coeff  # Коэффициент устойчивости
    
    def set_influence(self, influence_type, influence_coeff):
        """Установка параметров влияния"""
        self.influence_type = influence_type  # Тип влияния
        self.influence_coeff = influence_coeff  # Коэффициент влияния
    
    def set_damping(self, damping_type, damping_coeff):
        """Установка параметров затухания"""
        self.damping_type = damping_type  # Тип затухания
        self.damping_coeff = damping_coeff  # Коэффициент затухания
      
    def get_edge_distribution_type(self):
        """Возвращает тип распределения ребер"""
        if self.generation_params is None:  # Параметры генерации отсутствуют
            return 'custom'  # Пользовательский граф
        edge_dist = self.generation_params.get('edge_dist', {})  # Параметры распределения ребер
        return edge_dist.get('type', 'custom')  # Тип распределения или 'custom'
    
    def get_vertex_distribution_type(self):
        """Возвращает тип распределения вершин"""
        if self.generation_params is None:  # Параметры генерации отсутствуют
            return 'custom'  # Пользовательский граф
        vertex_dist = self.generation_params.get('vertex_dist')  # Параметры распределения вершин
        if vertex_dist is None:  # Распределение вершин не задано
            return 'None'  # Отсутствие распределения
        return vertex_dist.get('type', 'None')  # Тип распределения или 'None'


# In[14]:


class TierManager:
    """Управление ступенчатыми распределениями"""
    
    def __init__(self):
        """Инициализация менеджера ступеней с пустыми списками"""
        self.vertex_stages = []  # Список словарей для вершин
        self.edge_stages = []    # Список словарей для ребер
    
    def set_vertex_stages(self, stages):
        """Установка списка ступеней для вершин с копированием"""
        self.vertex_stages = stages.copy()  # Сохранение копии переданного списка
    
    def set_edge_stages(self, stages):
        """Установка списка ступеней для ребер с копированием"""
        self.edge_stages = stages.copy()  # Сохранение копии переданного списка
    
    def get_vertex_config(self):
        """Возврат копии списка ступеней для вершин"""
        return self.vertex_stages.copy()  # Защита от внешних изменений через копию
    
    def get_edge_config(self):
        """Возврат копии списка ступеней для ребер"""
        return self.edge_stages.copy()  # Защита от внешних изменений через копию
    
    def add_stage(self, tier_type, left, right, count):
        """Добавление новой ступени в соответствующий список"""
        stage = {'left': left, 'right': right, 'count': count}  # Словарь параметров ступени
        if tier_type == 'vertex':  # Ступень для вершин
            self.vertex_stages.append(stage)  # Добавление в список вершин
        else:  # Ступень для ребер
            self.edge_stages.append(stage)  # Добавление в список ребер
    
    def remove_stage(self, tier_type, index):
        """Удаление ступени по индексу из соответствующего списка"""
        if tier_type == 'vertex':  # Удаление из списка вершин
            if 0 <= index < len(self.vertex_stages):  # Проверка корректности индекса
                del self.vertex_stages[index]  # Удаление элемента
        else:  # Удаление из списка ребер
            if 0 <= index < len(self.edge_stages):  # Проверка корректности индекса
                del self.edge_stages[index]  # Удаление элемента
    
    def update_stage(self, tier_type, index, left=None, right=None, count=None):
        """Обновление параметров ступени по индексу"""
        stages = self.vertex_stages if tier_type == 'vertex' else self.edge_stages  # Выбор списка
        if 0 <= index < len(stages):  # Проверка корректности индекса
            if left is not None:  # Передана левая граница
                stages[index]['left'] = left  # Обновление левой границы
            if right is not None:  # Передана правая граница
                stages[index]['right'] = right  # Обновление правой границы
            if count is not None:  # Передано количество элементов
                stages[index]['count'] = count  # Обновление количества


# In[15]:


class DistributionGenerator:
    """Генерация выборок по распределениям с использованием переданного RNG"""
    
    @staticmethod
    def uniform(n, min_val, max_val, rng):
        """Генерация выборки из равномерного распределения"""
        return np.array([rng.uniform(min_val, max_val) for _ in range(n)])  # Массив случайных чисел в интервале [min_val, max_val]
    
    @staticmethod
    def normal(n, mean, std, min_val, max_val, rng):
        """Генерация выборки из усеченного нормального распределения"""
        from scipy.stats import norm as scipy_norm  # Импорт нормального распределения из scipy
        a, b = (min_val - mean) / std, (max_val - mean) / std  # Границы усечения в стандартизованных единицах
        p_low = scipy_norm.cdf(a)  # Вероятность в левой границе
        p_high = scipy_norm.cdf(b)  # Вероятность в правой границе
        u = np.array([rng.uniform(p_low, p_high) for _ in range(n)])  # Равномерные вероятности в диапазоне усечения
        return scipy_norm.ppf(u, loc=mean, scale=std)  # Обратная функция распределения (квантили)
    
    @staticmethod
    def student(n, df, scale, min_val, max_val, rng):
        """Генерация выборки из усеченного распределения Стьюдента"""
        from scipy.stats import t as scipy_t  # Импорт распределения Стьюдента из scipy
        p_low = scipy_t.cdf(min_val, df, scale=scale)  # Вероятность в левой границе
        p_high = scipy_t.cdf(max_val, df, scale=scale)  # Вероятность в правой границе
        u = np.array([rng.uniform(p_low, p_high) for _ in range(n)])  # Равномерные вероятности в диапазоне усечения
        return scipy_t.ppf(u, df, scale=scale)  # Обратная функция распределения (квантили)
    
    @staticmethod
    def laplace(n, loc, scale, min_val, max_val, rng):
        """Генерация выборки из усеченного распределения Лапласа"""
        from scipy.stats import laplace as scipy_laplace  # Импорт распределения Лапласа из scipy
        p_low = scipy_laplace.cdf(min_val, loc=loc, scale=scale)  # Вероятность в левой границе
        p_high = scipy_laplace.cdf(max_val, loc=loc, scale=scale)  # Вероятность в правой границе
        u = np.array([rng.uniform(p_low, p_high) for _ in range(n)])  # Равномерные вероятности в диапазоне усечения
        return scipy_laplace.ppf(u, loc=loc, scale=scale)  # Обратная функция распределения (квантили)
    
    @staticmethod
    def bimodal(n, mu1, sigma1, mu2, sigma2, weight, min_val, max_val, rng):
        """Генерация выборки из бимодального распределения (смесь двух нормальных)"""
        n1 = rng.binomial(n, weight)  # Количество элементов из первой компоненты
        n2 = n - n1  # Количество элементов из второй компоненты
        samples1 = DistributionGenerator.normal(n1, mu1, sigma1, min_val, max_val, rng)  # Выборка из первой компоненты
        samples2 = DistributionGenerator.normal(n2, mu2, sigma2, min_val, max_val, rng)  # Выборка из второй компоненты
        samples = np.concatenate([samples1, samples2])  # Объединение выборок
        
        indices = list(range(len(samples)))  # Список индексов для перемешивания
        rng.shuffle(indices)  # Перемешивание индексов
        samples = samples[indices]  # Переупорядочивание выборки
        return samples

    @staticmethod
    def skewed_t(n, df, shape, scale, min_val, max_val, rng):
        """Генерация выборки из усеченного нецентрального t-распределения"""
        from scipy.stats import nct as scipy_nct  # Импорт нецентрального t-распределения из scipy
        p_low = scipy_nct.cdf(min_val, df, shape, scale=scale)  # Вероятность в левой границе
        p_high = scipy_nct.cdf(max_val, df, shape, scale=scale)  # Вероятность в правой границе
        u = np.array([rng.uniform(p_low, p_high) for _ in range(n)])  # Равномерные вероятности в диапазоне усечения
        return scipy_nct.ppf(u, df, shape, scale=scale)  # Обратная функция распределения (квантили)

    @staticmethod
    def lognormal(n, gamma, mu, sigma, min_val, max_val, rng):
        """Генерация выборки из усеченного логнормального распределения со сдвигом"""
        from scipy.stats import lognorm as scipy_lognorm  # Импорт логнормального распределения из scipy
        s = sigma  # Параметр формы
        scale = np.exp(mu)  # Масштаб (медиана распределения)
        tolerance = PARAM_CONFIG['global']['tolerance']  # Получение значения точности из конфига
        adj_min = max(min_val - gamma, tolerance)  # Левая граница после сдвига (защита от нуля)
        adj_max = max_val - gamma  # Правая граница после сдвига
        p_low = scipy_lognorm.cdf(adj_min, s, scale=scale)  # Вероятность в левой границе
        p_high = scipy_lognorm.cdf(adj_max, s, scale=scale)  # Вероятность в правой границе
        u = np.array([rng.uniform(p_low, p_high) for _ in range(n)])  # Равномерные вероятности в диапазоне усечения
        return scipy_lognorm.ppf(u, s, scale=scale) + gamma  # Обратная функция плюс сдвиг
    
    @staticmethod
    def stepwise(n, stages, min_val, max_val, rng):
        """Генерация выборки из ступенчатого распределения"""
        total_weight = sum(s['weight'] for s in stages)  # Суммарный вес всех ступеней
        weights = [s['weight'] / total_weight for s in stages]  # Нормированные вероятности ступеней
        
        counts = rng.choices(range(len(weights)), weights=weights, k=n)  # Случайный выбор ступеней для каждого элемента
        from collections import Counter  # Импорт счетчика для подсчета частот
        counts_counter = Counter(counts)  # Подсчет количества попаданий в каждую ступень
        counts_list = [counts_counter.get(i, 0) for i in range(len(weights))]  # Список количеств по ступеням
        
        samples = np.array([])  # Пустой массив для выборки
        for stage, count in zip(stages, counts_list):  # Цикл по ступеням и их количествам
            stage_samples = np.array([rng.uniform(stage['left'], stage['right']) for _ in range(count)])  # Равномерные значения в границах ступени
            samples = np.concatenate([samples, stage_samples])  # Добавление в общую выборку
        indices = list(range(len(samples)))  # Список индексов для перемешивания
        rng.shuffle(indices)  # Перемешивание индексов
        samples = samples[indices]  # Переупорядочивание выборки
        return samples


# In[16]:


class ValueValidator:
    """Валидация, корректировка и синхронизация значений параметров"""
    
    def __init__(self, config):
        """Инициализация валидатора с конфигурацией параметров"""
        self.config = config  # Словарь конфигурации параметров
        self.gap = config['global']['gap']  # Минимальный зазор между левой и правой границами
        self.tolerance = config['global']['tolerance']  # Точность сравнения для чисел с плавающей точкой

    def get_param_config(self, domain, dist_type, param_name):
        """Получение конфигурации для конкретного параметра"""
        if dist_type == 'global':  # Глобальный параметр (не связанный с распределением)
            return self.config[domain].get(param_name)  # Поиск в глобальной секции
        if dist_type == 'Stepwise':  # Параметр ступенчатого распределения
            return self.config[domain][dist_type]['stage'][param_name]  # Поиск в секции stage
        if domain in ['vertex_card', 'edge_card']:  # Параметр карточки вершины или ребра
            return self.config[domain].get(param_name)  # Поиск в секции карточки
        return self.config[domain][dist_type][param_name]  # Поиск в секции распределения

    def validate_pair(self, left, right, left_config, right_config, rounding=2):
        """Корректировка пары связанных значений с сохранением зазора между ними"""
        left_min, left_max = left_config['range']  # Диапазон левого значения
        right_min, right_max = right_config['range']  # Диапазон правого значения
        
        left = max(left_min, min(left_max, left))  # Ограничение левого значения диапазоном
        right = max(right_min, min(right_max, right))  # Ограничение правого значения диапазоном
        
        if left >= right - self.gap:  # Нарушение минимального зазора
            new_left = max(left_min, right - self.gap)  # Попытка уменьшить левое значение
            if new_left >= left_min:  # Левое значение можно уменьшить
                left = new_left
            else:  # Левое значение достигло минимума
                new_right = min(right_max, left + self.gap)  # Увеличение правого значения
                right = new_right
        
        if left >= right - self.gap:  # Повторная проверка зазора
            right = min(right_max, left + self.gap)  # Увеличение правого значения
            if left >= right - self.gap:  # Зазор все еще нарушен
                left = max(left_min, right - self.gap)  # Уменьшение левого значения
        
        return round(left, rounding), round(right, rounding)  # Возврат округленных значений
    
    def validate_stage(self, stage, domain='edge', rounding=2):
        """Валидация одной ступени ступенчатого распределения"""
        left_config = self.get_param_config(domain, 'Stepwise', 'left')  # Конфигурация левой границы
        right_config = self.get_param_config(domain, 'Stepwise', 'right')  # Конфигурация правой границы
        left, right = self.validate_pair(stage['left'], stage['right'], left_config, right_config, rounding)  # Корректировка пары
        return {'left': left, 'right': right, 'weight': stage['weight']}  # Возврат валидированной ступени
    
    def validate_stages(self, stages, domain='edge', rounding=2):
        """Валидация списка ступеней ступенчатого распределения"""
        if not stages:  # Пустой список
            return []  # Возврат пустого списка
        return [self.validate_stage(s, domain, rounding) for s in stages]  # Валидация каждой ступени

    def validate_and_correct(self, value, param_config, rounding, current_value=None):
        """Валидация и корректировка значения с приведением к типу и диапазону"""
        try:
            if param_config['is_int']:  # Целочисленный параметр
                val = int(float(value))  # Преобразование в целое число
            else:  # Вещественный параметр
                val = float(value)  # Преобразование в число с плавающей точкой
            
            min_val, max_val = param_config['range']  # Допустимый диапазон
            val = max(min_val, min(max_val, val))  # Ограничение значения диапазоном
            
            if not param_config['is_int']:  # Вещественное число
                val = round(val, rounding)  # Округление до нужного количества знаков
            return val
            
        except (ValueError, TypeError):  # Ошибка преобразования (буквы, пустая строка)
            return current_value if current_value is not None else 0.0  # Возврат предыдущего значения или 0.0
    
    def correct_entry(self, entry, variable, param_config, rounding):
        """Корректировка значения в поле ввода и синхронизация с переменной"""
        raw = entry.get()  # Сырой текст из поля ввода
        current_value = variable.get()  # Текущее значение из переменной (на случай ошибки)
        corrected = self.validate_and_correct(raw, param_config, rounding, current_value)  # Валидация и корректировка
        variable.set(corrected)  # Обновление переменной
        
        entry.delete(0, 'end')  # Очистка поля ввода
        if param_config['is_int']:  # Целочисленный параметр
            entry.insert(0, str(int(corrected)))  # Вставка целого числа без десятичной части
        else:  # Вещественный параметр
            entry.insert(0, f"{corrected:.{rounding}f}")  # Вставка с фиксированным количеством знаков


# In[17]:


class GraphGenerator:
    """Генератор графов по параметрам распределений"""
    
    def __init__(self, dist_generator, config):
        """Инициализация генератора с генератором распределений и конфигурацией"""
        self.dist = dist_generator  # Генератор распределений для создания выборок
        self.config = config  # Конфигурация параметров распределений
    
    def _get_generator(self, domain, dist_type):
        """Получение функции-генератора для указанного домена и типа распределения"""
        if dist_type == 'None':  # Распределение отсутствует
            return None  # Возврат None вместо генератора
        return self.config[domain][dist_type]['generator']  # Извлечение генератора из конфигурации
    
    def generate(self, params, global_rng):
        """Генерация графа по параметрам с использованием глобального rng"""
        n = params['n_nodes']  # Количество вершин в графе
        G = nx.Graph()  # Создание пустого графа
        
        if n < 2:  # Недостаточно вершин для построения графа
            return G  # Возврат пустого графа
        
        vertex_params = params.get('vertex_dist')  # Параметры распределения вершин
        if vertex_params and vertex_params.get('type') != 'None':  # Распределение вершин задано
            gen = self._get_generator('vertex', vertex_params['type'])  # Получение генератора вершин
            v_weights = gen(n, vertex_params, global_rng)  # Генерация весов вершин
            for i, w in enumerate(v_weights):  # Цикл по индексам и весам
                G.add_node(f'V{i}', weight=w)  # Добавление вершины с весом
        else:  # Распределение вершин не задано
            for i in range(n):  # Цикл по количеству вершин
                G.add_node(f'V{i}', weight=1.0)  # Добавление вершины с весом 1.0
        
        edge_params = params['edge_dist']  # Параметры распределения ребер
        gen = self._get_generator('edge', edge_params['type'])  # Получение генератора ребер
        n_edges = n * (n - 1) // 2  # Количество ребер в полном графе (верхний треугольник)
        edge_weights = gen(n_edges, edge_params, global_rng)  # Генерация весов ребер
        i_indices, j_indices = np.triu_indices(n, k=1)  # Индексы для верхнего треугольника матрицы
        edges = [(f'V{i}', f'V{j}', {'weight': w}) for i, j, w in zip(i_indices, j_indices, edge_weights)]  # Список ребер с весами
        G.add_edges_from(edges)  # Добавление всех ребер в граф
        return G


# In[18]:


class StatisticsCalculator:
    """Вычисление статистик"""

    # Маппинг data-ключей в ui-ключи для отображения
    STAT_LABEL_MAP = {
        # Статистика ребер
        'edge_min': 'min_stat',
        'edge_max': 'max_stat',
        'edge_mean': 'mean_stat',
        'edge_std': 'std_stat',
        'edge_median': 'median',
        'edge_skewness': 'skewness',
        'edge_kurtosis': 'kurtosis',
        'edge_q05': 'q05',
        'edge_q95': 'q95',
        'edge_count_positive': 'positive_count',
        'edge_pct_positive': 'positive_percent',
        'edge_sum_positive': 'positive_sum',
        'edge_mean_positive': 'positive_mean',
        'edge_count_negative': 'negative_count',
        'edge_pct_negative': 'negative_percent',
        'edge_sum_negative': 'negative_sum',
        'edge_mean_negative': 'negative_mean',
        
        # Статистика вершин
        'vertex_min': 'min_stat',
        'vertex_max': 'max_stat',
        'vertex_mean': 'mean_stat',
        'vertex_std': 'std_stat',
        'vertex_median': 'median',
        'vertex_skewness': 'skewness',
        'vertex_kurtosis': 'kurtosis',
        'vertex_q05': 'q05',
        'vertex_q95': 'q95',
        
        # Статистика стартовой вершины
        'start_vertex_weight': 'vertex_weight',
        'start_vertex_avg_edge_weight': 'avg_edge_weight',
        'start_vertex_count_positive': 'positive_count',
        'start_vertex_pct_positive': 'positive_percent',
        'start_vertex_sum_positive': 'positive_sum',
        'start_vertex_mean_positive': 'positive_mean',
        'start_vertex_count_negative': 'negative_count',
        'start_vertex_pct_negative': 'negative_percent',
        'start_vertex_sum_negative': 'negative_sum',
        'start_vertex_mean_negative': 'negative_mean',
        'start_vertex_resistance_factor': 'resistance_factor',
        'start_vertex_influence_factor': 'influence_factor',
        
        # Результаты симуляции пожара
        'fire_total_burned': 'total_burned',
        'fire_total_iterations': 'total_iterations',
        'fire_spread_rate_1': 'spread_rate_1',
        'fire_spread_rate_2': 'spread_rate_2',
        'fire_spread_rate_3': 'spread_rate_3',
        'fire_spread_rate_4': 'spread_rate_4',
        'fire_spread_rate_5': 'spread_rate_5',
        'fire_peak_new_burns': 'peak_new_burns',
        'fire_time_to_peak': 'time_to_peak',
        'fire_time_from_peak': 'time_from_peak',

        'graph_seed': 'graph_seed',
    }

    @classmethod
    def data_key_to_ui_key(cls, data_key):
        """Преобразование data-ключа в ui-ключ для отображения"""
        return cls.STAT_LABEL_MAP.get(data_key, data_key)  # Поиск в маппинге или возврат исходного ключа

    @staticmethod
    def calculate_all(data):
        """Вычисление всех статистик с возвратом готовых словарей"""
        graph = data.graph  # Извлечение графа из данных
        
        if not graph or graph.number_of_nodes() == 0:  # Пустой граф
            return {}, {}, []  # Возврат пустых словарей и списка
        
        edge_weights = [d['weight'] for _, _, d in graph.edges(data=True)]  # Сбор весов всех ребер
        edge_stats = StatisticsCalculator._edge_stats_for_display(edge_weights)  # Статистика ребер
        
        vertex_weights = [graph.nodes[n].get('weight', 1.0) for n in graph.nodes()]  # Сбор весов всех вершин
        vertex_stats = StatisticsCalculator._vertex_stats_for_display(vertex_weights)  # Статистика вершин
        
        vertices_stats = []  # Список статистик по каждой вершине
        for i in range(graph.number_of_nodes()):  # Цикл по индексам вершин
            node = f'V{i}'  # Имя вершины
            neighbors = list(graph.neighbors(node))  # Список соседей
            neighbor_weights = [graph[node][nbr]['weight'] for nbr in neighbors]  # Веса ребер к соседям
            
            pos_weights = [w for w in neighbor_weights if w > 0]  # Положительные веса
            neg_weights = [w for w in neighbor_weights if w < 0]  # Отрицательные веса
            
            vertices_stats.append({
                'vertex_weight': graph.nodes[node].get('weight', 1.0),  # Вес вершины
                'degree': len(neighbors),  # Степень вершины
                'positive_count': len(pos_weights),  # Количество положительных связей
                'positive_sum': sum(pos_weights),  # Сумма положительных весов
                'positive_mean': np.mean(pos_weights) if pos_weights else 0,  # Среднее положительных весов
                'negative_count': len(neg_weights),  # Количество отрицательных связей
                'negative_sum': sum(neg_weights),  # Сумма отрицательных весов
                'negative_mean': np.mean(neg_weights) if neg_weights else 0,  # Среднее отрицательных весов
                'avg_edge_weight': np.mean(neighbor_weights) if neighbor_weights else 0,  # Средний вес ребер
            })
        
        return edge_stats, vertex_stats, vertices_stats  # Возврат всех статистик

    @staticmethod
    def _edge_stats_for_display(weights):
        """Возврат статистики ребер с data-ключами"""
        if not weights:  # Пустой список весов
            return {}  # Пустой словарь
        
        w = np.array(weights)  # Преобразование в массив numpy
        pos = w[w > 0]  # Массив положительных весов
        neg = w[w < 0]  # Массив отрицательных весов
        total = len(w)  # Общее количество ребер
        
        if len(w) > 1 and np.std(w) > PARAM_CONFIG['global']['tolerance']:  # Достаточно данных для расчета
            skewness = float(stats.skew(w))  # Коэффициент асимметрии
            kurtosis = float(stats.kurtosis(w))  # Коэффициент эксцесса
        else:  # Недостаточно данных или нулевая дисперсия
            skewness = 0.0  # Обнуление асимметрии
            kurtosis = 0.0  # Обнуление эксцесса
        
        positive_count = len(pos)  # Количество положительных весов
        negative_count = len(neg)  # Количество отрицательных весов
        
        return {
            'edge_min': float(w.min()),  # Минимальный вес
            'edge_max': float(w.max()),  # Максимальный вес
            'edge_mean': float(w.mean()),  # Среднее арифметическое
            'edge_std': float(w.std()),  # Стандартное отклонение
            'edge_median': float(np.median(w)),  # Медиана
            'edge_skewness': skewness,  # Асимметрия
            'edge_kurtosis': kurtosis,  # Эксцесс
            'edge_q05': float(np.percentile(w, 5)),  # 5-процентный квантиль
            'edge_q95': float(np.percentile(w, 95)),  # 95-процентный квантиль
            'edge_count_positive': positive_count,  # Количество положительных
            'edge_pct_positive': (positive_count / total * 100) if total > 0 else 0,  # Процент положительных
            'edge_sum_positive': float(pos.sum()) if positive_count > 0 else 0,  # Сумма положительных
            'edge_mean_positive': float(pos.mean()) if positive_count > 0 else 0,  # Среднее положительных
            'edge_count_negative': negative_count,  # Количество отрицательных
            'edge_pct_negative': (negative_count / total * 100) if total > 0 else 0,  # Процент отрицательных
            'edge_sum_negative': float(neg.sum()) if negative_count > 0 else 0,  # Сумма отрицательных
            'edge_mean_negative': float(neg.mean()) if negative_count > 0 else 0,  # Среднее отрицательных
        }

    @staticmethod
    def _vertex_stats_for_display(weights):
        """Возврат статистики вершин с data-ключами"""
        if not weights:  # Пустой список весов
            return {}  # Пустой словарь
        
        w = np.array(weights)  # Преобразование в массив numpy
        
        if len(w) > 1 and np.std(w) > PARAM_CONFIG['global']['tolerance']:  # Достаточно данных для расчета
            skewness = float(stats.skew(w))  # Коэффициент асимметрии
            kurtosis = float(stats.kurtosis(w))  # Коэффициент эксцесса
        else:  # Недостаточно данных или нулевая дисперсия
            skewness = 0.0  # Обнуление асимметрии
            kurtosis = 0.0  # Обнуление эксцесса
        
        return {
            'vertex_min': float(w.min()),  # Минимальный вес
            'vertex_max': float(w.max()),  # Максимальный вес
            'vertex_mean': float(w.mean()),  # Среднее арифметическое
            'vertex_std': float(w.std()),  # Стандартное отклонение
            'vertex_median': float(np.median(w)),  # Медиана
            'vertex_skewness': skewness,  # Асимметрия
            'vertex_kurtosis': kurtosis,  # Эксцесс
            'vertex_q05': float(np.percentile(w, 5)),  # 5-процентный квантиль
            'vertex_q95': float(np.percentile(w, 95)),  # 95-процентный квантиль
        }

    @staticmethod
    def start_vertex_stats(data, vertex_index):
        """Возврат статистики для конкретной вершины с data-ключами"""
        if not data.graph or vertex_index >= data.graph.number_of_nodes():  # Некорректный индекс
            return {}  # Пустой словарь
        
        node = f'V{vertex_index}'  # Имя вершины
        neighbors = list(data.graph.neighbors(node))  # Список соседей
        neighbor_weights = [data.graph[node][nbr]['weight'] for nbr in neighbors]  # Веса ребер к соседям
        
        pos_weights = [w for w in neighbor_weights if w > 0]  # Положительные веса
        neg_weights = [w for w in neighbor_weights if w < 0]  # Отрицательные веса
        degree = len(neighbors)  # Степень вершины
        
        raw_weight = data.graph.nodes[node].get('weight', 1.0)  # Исходный вес вершины
        
        all_weights = {n: data.graph.nodes[n].get('weight', 1.0) for n in data.graph.nodes()}  # Веса всех вершин
        norm_weights = ProbabilityCalculator.normalize_weights(all_weights)  # Нормализация весов в диапазон 0-2
        norm_weight = norm_weights.get(node, 1.0)  # Нормализованный вес вершины
        
        if data.influence_type == 'None':  # Влияние не учитывается
            influence_factor = 1.0  # Множитель по умолчанию
        else:  # Влияние учитывается
            is_inverse = (data.influence_type == 'param_inverse')  # Обратная зависимость
            influence_factor = ProbabilityCalculator.factor(norm_weight, data.influence_coeff, is_inverse)  # Вычисление множителя влияния
        
        if data.resistance_type == 'None':  # Устойчивость не учитывается
            resistance_factor = 1.0  # Множитель по умолчанию
        else:  # Устойчивость учитывается
            is_inverse = (data.resistance_type == 'param_inverse')  # Обратная зависимость
            resistance_factor = ProbabilityCalculator.factor(norm_weight, data.resistance_coeff, is_inverse)  # Вычисление множителя устойчивости
        
        return {
            'start_vertex_weight': raw_weight,  # Исходный вес вершины
            'start_vertex_avg_edge_weight': np.mean(neighbor_weights) if neighbor_weights else 0,  # Средний вес ребер
            'start_vertex_count_positive': len(pos_weights),  # Количество положительных связей
            'start_vertex_pct_positive': (len(pos_weights) / degree * 100) if degree > 0 else 0,  # Процент положительных
            'start_vertex_sum_positive': sum(pos_weights),  # Сумма положительных весов
            'start_vertex_mean_positive': np.mean(pos_weights) if pos_weights else 0,  # Среднее положительных
            'start_vertex_count_negative': len(neg_weights),  # Количество отрицательных связей
            'start_vertex_pct_negative': (len(neg_weights) / degree * 100) if degree > 0 else 0,  # Процент отрицательных
            'start_vertex_sum_negative': sum(neg_weights),  # Сумма отрицательных весов
            'start_vertex_mean_negative': np.mean(neg_weights) if neg_weights else 0,  # Среднее отрицательных
            'start_vertex_resistance_factor': resistance_factor,  # Множитель устойчивости
            'start_vertex_influence_factor': influence_factor,  # Множитель влияния
        }

    @staticmethod
    def graph_seed_stats(data):
        """Возврат статистики seed графа"""
        if data and hasattr(data, 'graph_seed') and data.graph_seed is not None:  # Seed существует
            return {'graph_seed': data.graph_seed}  # Словарь с seed
        return {'graph_seed': '—'}  # Пустое значение


# In[19]:


class ProbabilityCalculator:
    """Расчет вероятностей для симуляции"""

    @staticmethod
    def normalize_weights(weights_dict):
        """Нормализация весов в диапазон 0-2"""
        if not weights_dict:  # Пустой словарь
            return {}  # Возврат пустого словаря
        values = list(weights_dict.values())  # Все значения весов
        min_val = min(values)  # Минимальный вес
        max_val = max(values)  # Максимальный вес
        if max_val - min_val < PARAM_CONFIG['global']['tolerance']:  # Все веса почти одинаковы
            return {k: 1.0 for k in weights_dict}  # Возврат нейтрального значения 1.0 для всех вершин
        return {k: 2.0 * (v - min_val) / (max_val - min_val) for k, v in weights_dict.items()}  # Нормализация в диапазон [0, 2]
    
    @staticmethod
    def factor(norm_weight, coeff, is_inverse):
        """Расчет фактора влияния или устойчивости"""
        adj = 2.0 - norm_weight if is_inverse else norm_weight  # Инверсия веса при обратной зависимости
        return math.exp(coeff * (adj - 1.0))  # Экспоненциальный множитель

    @staticmethod
    def combined_probability(probs):
        """Вычисление комбинированной вероятности от всех источников"""
        if not probs:  # Пустой список вероятностей
            return 0.0  # Нулевая вероятность
        product = 1.0  # Начальное произведение
        for p in probs:  # Цикл по всем вероятностям
            product *= (1.0 - p)  # Накопление произведения дополнений
        return 1.0 - product  # Вероятность срабатывания хотя бы одного источника

    @staticmethod
    def check_threshold(probs, method, value):
        """Проверка порогового условия для списка вероятностей"""
        if not probs:  # Пустой список вероятностей
            return False  # Порог не пройден
        if method == 'None':  # Без порога
            return True  # Всегда успешно
        elif method == 'Maximum':  # Максимальный порог
            return max(probs) >= value  # Максимум не ниже значения
        elif method == 'Mean':  # Средний порог
            return sum(probs) / len(probs) >= value  # Среднее не ниже значения
        elif method == 'Median':  # Медианный порог
            return np.median(probs) >= value  # Медиана не ниже значения
        return False  # Неизвестный метод

    @staticmethod
    def ignition_probability(edge_weight, source_norm, target_norm, iteration, resistance_type, resistance_coeff,
                             influence_type, influence_coeff, damping_type, damping_coeff):
        """Расчет вероятности возгорания вершины от соседа"""
        
        if edge_weight <= 0:  # Отрицательное или нулевое ребро
            return 0.0  # Передача огня невозможна
        
        prob = min(edge_weight, 1.0)  # Базовая вероятность (ограничена 1.0)
        
        if influence_type != 'None':  # Учет влияния источника
            is_inverse = (influence_type == 'param_inverse')  # Флаг обратной зависимости
            inf_factor = ProbabilityCalculator.factor(source_norm, influence_coeff, is_inverse)  # Множитель влияния
            prob *= inf_factor  # Применение множителя источника
        
        if resistance_type != 'None':  # Учет устойчивости цели
            is_inverse = (resistance_type == 'param_inverse')  # Флаг обратной зависимости
            res_factor = ProbabilityCalculator.factor(target_norm, resistance_coeff, is_inverse)  # Множитель устойчивости
            prob /= res_factor  # Деление на множитель цели
        
        if damping_type != 'None':  # Учет затухания со временем
            if damping_type == 'damping_exponential':  # Экспоненциальное затухание
                prob *= math.exp(-damping_coeff * iteration)  # Умножение на экспоненту
            elif damping_type == 'damping_hyperbolic':  # Гиперболическое затухание
                prob *= 1.0 / (1.0 + damping_coeff * iteration)  # Деление на линейную функцию
            elif damping_type == 'damping_discrete':  # Дискретное затухание
                prob *= math.pow(1.0 / (1.0 + damping_coeff), iteration)  # Возведение в степень
        
        return max(0.0, min(1.0, prob))  # Ограничение вероятности диапазоном [0, 1]


# In[20]:


class SimulationEngine:
    """Движок симуляции распространения пожара"""
    
    def __init__(self, prob_calculator):
        """Инициализация движка с калькулятором вероятностей"""
        self.prob = prob_calculator  # Калькулятор вероятностей возгорания

    def run(self, data, start_vertex, ignition_method='Sequential', threshold_method='None', threshold_value=0.0):
        """Запуск симуляции с использованием rng от графа"""
        rng = data.get_sim_rng()  # Получение уникального rng для этой симуляции
        graph = data.graph  # Граф из данных
        raw_weights = {node: graph.nodes[node].get('weight', 1.0) for node in graph.nodes()}  # Исходные веса вершин
        norm_weights = self.prob.normalize_weights(raw_weights)  # Нормализованные веса вершин
        burned_nodes = {start_vertex: 0}  # Словарь сгоревших вершин и шага возгорания
        burned_edges = {}  # Словарь сгоревших ребер и шага возгорания
        history = [1]  # История новых возгораний (начальное значение 1 для стартовой вершины)
        max_iter = 100  # Максимальное количество итераций
        resistance_type = data.resistance_type  # Тип устойчивости
        resistance_coeff = data.resistance_coeff  # Коэффициент устойчивости
        influence_type = data.influence_type  # Тип влияния
        influence_coeff = data.influence_coeff  # Коэффициент влияния
        damping_type = data.damping_type  # Тип затухания
        damping_coeff = data.damping_coeff  # Коэффициент затухания
        
        for iteration in range(1, max_iter + 1):  # Цикл по итерациям
            new_fires = 0  # Счетчик новых возгораний на этой итерации
            current_burned = list(burned_nodes.keys())  # Список текущих горящих вершин
            if ignition_method == 'Sequential':  # Последовательный метод поджога
                rng.shuffle(current_burned)  # Перемешивание порядка обработки источников
            candidates = {}  # Словарь кандидатов на возгорание {вершина: {вероятности, источники}}
            for source in current_burned:  # Цикл по всем горящим вершинам
                source_norm = norm_weights.get(source, 1.0)  # Нормализованный вес источника
                for target in graph.neighbors(source):  # Цикл по соседям источника
                    if target in burned_nodes:  # Вершина уже горит
                        continue
                    
                    edge = tuple(sorted((source, target)))  # Уникальный ключ ребра
                    if edge in burned_edges:  # Ребро уже использовалось
                        continue
                    
                    weight = graph[source][target]['weight']  # Вес ребра
                    if weight <= 0:  # Отрицательное ребро не передает огонь
                        continue
                    
                    target_norm = norm_weights.get(target, 1.0)  # Нормализованный вес цели
                    prob = self.prob.ignition_probability(weight, source_norm, target_norm, iteration, resistance_type, resistance_coeff,
                                                          influence_type, influence_coeff, damping_type, damping_coeff)
                    if target not in candidates:  # Первый источник для этой цели
                        candidates[target] = {'probs': [], 'sources': []}  # Инициализация записи
                    candidates[target]['probs'].append(prob)  # Добавление вероятности
                    candidates[target]['sources'].append(source)  # Добавление источника
            
            for target, info in candidates.items():  # Цикл по кандидатам
                probs = info['probs']  # Список вероятностей от разных источников
                sources = info['sources']  # Список соответствующих источников
                
                if not self.prob.check_threshold(probs, threshold_method, threshold_value):  # Проверка порога
                    continue  # Порог не пройден, пропуск вершины
                
                if ignition_method == 'Sequential':  # Последовательный поджог
                    for prob, source in zip(probs, sources):  # Цикл по источникам в порядке очереди
                        if rng.random() < prob:  # Успешное возгорание
                            burned_nodes[target] = iteration  # Запись шага возгорания вершины
                            burned_edges[tuple(sorted((source, target)))] = iteration  # Запись шага возгорания ребра
                            new_fires += 1  # Увеличение счетчика
                            break  # Выход из цикла (первый успешный источник)
                
                elif ignition_method == 'Simultaneous':  # Одновременный поджог
                    combined_prob = self.prob.combined_probability(probs)  # Комбинированная вероятность
                    if rng.random() < combined_prob:  # Успешное возгорание
                        max_idx = probs.index(max(probs))  # Индекс максимальной вероятности
                        best_source = sources[max_idx]  # Лучший источник
                        burned_nodes[target] = iteration  # Запись шага возгорания вершины
                        burned_edges[tuple(sorted((best_source, target)))] = iteration  # Запись шага возгорания ребра
                        new_fires += 1  # Увеличение счетчика
            
            history.append(new_fires)  # Добавление в историю
            
            if new_fires == 0:  # Нет новых возгораний
                break
        
        return {
            'burned_nodes': burned_nodes,  # Словарь сгоревших вершин
            'burned_edges': burned_edges,  # Словарь сгоревших ребер
            'history': history,  # История новых возгораний
            'max_iteration': max(burned_nodes.values()) if burned_nodes else 0,  # Максимальный шаг
            'graph_seed': data.get_graph_seed(),  # Seed графа для отображения
            'sim_counter': data.get_sim_counter()  # Счетчик симуляций на этом графе
        }


# In[21]:


class WidgetFactory:
    """Фабрика кастомных виджетов"""
    
    def __init__(self, theme_manager, translator, app=None, base_font_size=10, font_family="Segoe UI"):
        self.theme = theme_manager
        self.tr = translator
        self.app = app
        self.font_config = FONT_CONFIG
        self.font_family = font_family
        self.base_font_size = base_font_size
    
    def get_font(self, style_name):
        """Возвращает шрифт для указанного стиля в формате для tkinter"""
        style = self.font_config['styles'][style_name]
        size = self.base_font_size + style.get('offset', 0) # Размер шрифта
        size = max(6, size)                                 # Размер шрифта не менее 6
        weight = 'bold' if style['bold'] else 'normal'      # Начертание (жирное / обычное)
        return (self.font_family, size, weight)
    
    def update_font_size(self, new_size):
        """Обновляет базовый размер шрифта"""
        self.base_font_size = new_size
        self.font_config['default_size'] = new_size
    
    def create_frame(self, parent, **kwargs):
        """Фрейм с цветом фона из темы"""
        return tk.Frame(parent, bg=self.theme.get_color('bg_color'), **kwargs)
    
    def create_labelframe(self, parent, title_key, **kwargs):
        """Фрейм с заголовком и отступом снизу"""
        container = self.create_frame(parent)  # Внешний контейнер (для заголовка и рамки)
        title = self.create_label(container, title_key, 'header')  # Заголовок рамки
        title.pack(anchor='w', padx=0, pady=0)
        frame = tk.Frame(container, bg=self.theme.get_color('bg_color'), highlightbackground=self.theme.get_color('border_color'),
                         highlightthickness=1, highlightcolor=self.theme.get_color('border_color'), bd=0, **kwargs)  # Рамка с границей
        frame.pack(fill='both', expand=True)
        content = self.create_frame(frame)  # Внутренняя область внутри рамки для контента
        content.pack(fill='both', expand=True, padx=10, pady=10)  # Отступы по 10px для контента внутри рамки
        container.frame = frame      # Ссылка на рамку
        container.content = content  # Ссылка на область контента
        container.title = title      # Ссылка на заголовок
        return container
    
    def create_paned(self, parent, orient='horizontal', **kwargs):
        """Создает разделяемую панель"""
        return tk.PanedWindow(parent, orient=orient, bg=self.theme.get_color('bg_color'), sashwidth=5, sashrelief='raised', **kwargs)
    
    def create_label(self, parent, text_key, style='normal', **kwargs):
        """Лейбл с переводом текста"""
        font = self.get_font(style)                                 # Шрифт для указанного стиля
        color_key = self.font_config['styles'][style]['color_key']  # Ключ цвета текста из конфига стиля
        return tk.Label(parent, 
                        text=self.tr.t(text_key),                   # Переведенный текст по ключу
                        bg=self.theme.get_color('bg_color'),        # Фон
                        fg=self.theme.get_color(color_key),         # Цвет текста
                        font=font,                                  # Шрифт
                        anchor='w', **kwargs)
    
    def create_button(self, parent, text_key, command, style, **kwargs):
        """Кнопки"""
        config = BUTTON_CONFIG[style]                               # Конфигурация стиля кнопки
        bg = self.theme.get_color(config['bg_key'])                 # Фон кнопки
        hover = self.theme.get_color(config['hover_key'])           # Цвет при наведении
        text_color = self.theme.get_color(config['text_color_key']) # Цвет текста
        size_config = BUTTON_SIZES[config['size']]                  # Размер кнопки
        font = self.get_font(config['font_style'])                  # Шрифт текста на кнопке

        # Создание кнопки
        btn = tk.Button(parent, 
                       text=self.tr.t(text_key),         # Переведенный текст на кнопке
                       command=command,                  # Функция при нажатии на кнопку
                       bg=bg,                            # Цвет фона
                       fg=text_color,                    # Цвет текста
                       activebackground=hover,           # Цвет фона при наведении
                       activeforeground=text_color,      # Цвет текста при наведении
                       font=font,                        # Шрифт текста
                       width=size_config['min_width'],   # Ширина кнопки
                       height=size_config['min_height'], # Высота кнопки
                       bd=0,                             # Без границы
                       cursor='hand2',                   # Курсор-рука при наведении
                       **kwargs)
        
        # Эффекты наведения
        btn.bind('<Enter>', lambda e: btn.config(bg=hover))  # При наведении - цвет hover
        btn.bind('<Leave>', lambda e: btn.config(bg=bg))     # При уходе мыши - обычный цвет
        return btn
    
    def create_icon_button(self, parent, command, button_type='add', **kwargs):
        """Создает кнопку-иконку (+ или ✕)"""
        style = 'icon_add' if button_type == 'add' else 'icon_delete' # Стиль в зависимости от типа кнопки
        config = BUTTON_CONFIG[style]                                 # Конфигурация для иконки
        
        bg = self.theme.get_color(config['bg_key'])                  # Фон кнопки
        hover = self.theme.get_color(config['hover_key'])            # Цвет фона кнопки при наведении
        text_color = self.theme.get_color(config['text_color_key'])  # Цвет иконки
        size_config = BUTTON_SIZES[config['size']]                   # Размеры для иконки (width, height)
        font = self.get_font(config['font_style'])                   # Шрифт для иконки

        # Создание кнопки
        btn = tk.Button(parent, 
                       text=config['icon'],          # Символ иконки (+ или ✕)
                       command=command,              # Функция при нажатии на кнопку
                       bg=bg,                        # Цвет фона
                       fg=text_color,                # Цвет иконки
                       activebackground=hover,       # Цвет фона при наведении
                       activeforeground=text_color,  # Цвет иконки при наведении
                       font=font,                    # Шрифт иконки
                       width=size_config['width'],   # Ширина кнопки
                       height=size_config['height'], # Высота кнопки
                       bd=0,                         # Без границы
                       cursor='hand2',               # Курсор-рука при наведении
                       **kwargs)
        
        # Эффекты наведения
        btn.bind('<Enter>', lambda e: btn.config(bg=hover))  # При наведении - цвет hover
        btn.bind('<Leave>', lambda e: btn.config(bg=bg))     # При уходе мыши - обычный цвет
        return btn

    def create_entry(self, parent, variable, param_name, domain, dist_type, size='default', **kwargs):
        """Создает поле ввода с валидацией"""
        # Создание поля ввода
        entry = tk.Entry(parent,
                         width=self.app.size_config['control']['entry'][size],      # Ширина поля ввода из конфига
                         font=self.get_font('entry'),                               # Шрифт для полей ввода
                         justify='center',                                          # Выравнивание по центру
                         bd=0,                                                      # Без границ
                         relief='flat',                                             # Плоский (не вдавленный)
                         bg=self.theme.get_color('input_bg'),                       # Фон поля ввода
                         fg=self.theme.get_color('text_color'),                     # Цвет текста
                         insertbackground=self.theme.get_color('text_color'),       # Цвет курсора
                         highlightbackground=self.theme.get_color('border_color'),  # Цвет рамки
                         highlightthickness=1,                                      # Толщина рамки
                         **kwargs)
        
        # Сохранение начального значения на случай отмены ввода
        initial_value = variable.get()  # Запоминаем значение до редактирования
        # Вставка значения в поле с учетом округления
        rounding = self.app.settings['rounding_input'].get()
        if isinstance(variable, tk.IntVar):
            entry.insert(0, str(initial_value))  # Целые числа без округления
        else:
            entry.insert(0, f"{initial_value:.{rounding}f}")  # Вещественные с округлением
    
        # trace для синхронизации с внешними изменениями
        def sync_from_variable(*args):
            if entry.winfo_exists():    # Проверка, что поле ввода еще существует
                entry.delete(0, 'end')  # Очистка поля
                if isinstance(variable, tk.IntVar):  # Если целочисленная переменная
                    entry.insert(0, str(variable.get()))  # Вставка строки без округления
                else:  # Если вещественная переменная
                    entry.insert(0, f"{variable.get():.{rounding}f}")  # Вставка с округлением
        variable.trace_add('write', sync_from_variable)  # Отслеживание изменения переменной извне
        
        def save():
            rounding = self.app.settings['rounding_input'].get()  # Точность округления из настроек
            param_config = self.app.validator.get_param_config(domain, dist_type, param_name)  # Конфиг параметра из валидатора
            self.app.validator.correct_entry(entry, variable, param_config, rounding)  # Валидация и сохранение в переменную
        def cancel():
            # Перезапускает валидатор с текущим значением переменной = отмена ввода, возврат предыдущего корректного значения
            rounding = self.app.settings['rounding_input'].get()
            param_config = self.app.validator.get_param_config(domain, dist_type, param_name)
            self.app.validator.correct_entry(entry, variable, param_config, rounding)
            entry.master.focus_set()     # Убирает фокус с поля ввода
            
        # Эффекты наведения
        entry.bind('<FocusOut>', lambda e: save())  # Потеря фокуса - сохранение
        entry.bind('<Return>', lambda e: (save(), entry.master.focus_set()))  # Нажатие Enter - сохранение и убирание фокуса
        entry.bind('<Escape>', lambda e: cancel())  # Нажатие Escape - отмена
        return entry

    def create_table_entry(self, parent, variable, param_name, domain, dist_type, size='default'):
        """Создает поле ввода для таблиц без автоматических привязок"""
        rounding = self.app.settings['rounding_input'].get()
        param_config = self.app.validator.get_param_config(domain, dist_type, param_name)
        
        entry = tk.Entry(
            parent,
            width=self.app.size_config['control']['entry'][size],
            font=self.get_font('entry'),
            justify='center',
            bd=0,
            relief='flat',
            bg=self.theme.get_color('input_bg'),
            fg=self.theme.get_color('text_color'),
            insertbackground=self.theme.get_color('text_color'),
            highlightbackground=self.theme.get_color('border_color'),
            highlightthickness=1
        )
        
        # Вставляем значение с округлением
        if isinstance(variable, tk.IntVar):
            entry.insert(0, str(variable.get()))
        else:
            entry.insert(0, f"{variable.get():.{rounding}f}")
        
        return entry, param_config
    
    def create_scale(self, parent, variable, from_, to_, resolution=1, size='normal', orient='horizontal', **kwargs):
        """Слайдер"""
        length = self.app.size_config['control']['scale'][size]          # Длина слайдера из конфига
        # Создание слайдера
        scale = tk.Scale(parent,
                         from_=from_,                                       # Минимальное значение
                         to=to_,                                            # Максимальное значение
                         resolution=resolution,                             # Шаг изменения
                         orient=orient,                                     # Ориентация (горизонтальная / вертикальная)
                         length=length,                                     # Длина слайдера
                         variable=variable,                                 # Привязанная переменная tkinter
                         showvalue=0,                                       # Не показывать текущее значение рядом
                         bg=self.theme.get_color('bg_color'),               # Фон слайдера (по краям) и ползунка без нажатия
                         troughcolor=self.theme.get_color('slider_trough'), # Цвет дорожки слайдера
                         activebackground=self.theme.get_color('slider_thumb_active'), # Цвет ползунка под нажатием и наведением
                         highlightthickness=0,                              # Без подсветки рамки
                         bd=1,                                              # Толщина границы
                         relief='sunken',                                   # Вдавленный стиль
                         sliderrelief='raised',                             # Рельеф ползунка (приподнятый)
                         **kwargs)
        return scale
    
    def create_checkbutton(self, parent, text_key, variable, **kwargs):
        """Чекбокс"""
        font = self.get_font('normal')                                            # Шрифт для текста чекбокса
        return tk.Checkbutton(parent,
                             text=self.tr.t(text_key),                            # Переведенный текст рядом с чекбоксом
                             variable=variable,                                   # Привязанная переменная (BooleanVar)
                             onvalue=True,                                        # Значение переменной при установке флажка
                             offvalue=False,                                      # Значение переменной при снятии флажка
                             bg=self.theme.get_color('bg_color'),                 # Фон чекбокса из темы
                             fg=self.theme.get_color('text_color'),               # Цвет текста из темы
                             selectcolor=self.theme.get_color('bg_color'),        # Цвет фона при выделении (совпадает с фоном)
                             activebackground=self.theme.get_color('bg_color'),   # Цвет фона при наведении мыши
                             activeforeground=self.theme.get_color('text_color'), # Цвет текста при наведении мыши
                             font=font,                                           # Шрифт текста
                             anchor='w',                                          # Выравнивание текста по левому краю (west)
                             **kwargs)
    
    def create_combobox(self, parent, values, variable, size='default', **kwargs):
        """Выпадающий список (кастомный)"""
        width = self.app.size_config['control']['combobox'][size]          # Ширина поля из конфига
        font = self.get_font('combobox')                                   # Шрифт для текста
        frame = tk.Frame(parent, bg=self.theme.get_color('bg_color'))      # Внешний контейнер
        
        # Рамка вокруг поля ввода (того, что сейчас установлено в комбобоксе)
        entry_frame = tk.Frame(frame, bg=self.theme.get_color('input_bg'), highlightbackground=self.theme.get_color('border_color'),
                               highlightcolor=self.theme.get_color('border_color'), highlightthickness=1)
        entry_frame.pack(side='left', fill='both', expand=True)
        
        # Поле ввода (только для чтения, отображает выбранное значение)
        entry = tk.Entry(entry_frame, bg=self.theme.get_color('input_bg'), fg=self.theme.get_color('text_color'), font=font, bd=0,
                         relief='flat', state='readonly', cursor='arrow', justify='left', readonlybackground=self.theme.get_color('input_bg'),
                         insertwidth=0, highlightthickness=0, width=width)
        entry.pack(side='left', fill='both', expand=True, padx=(5, 0))     # Отступ текста выбранной опции от границы комбобокса слева 5px
        
        # Стрелка-треугольник справа (просто текстовый символ)
        arrow = tk.Label(entry_frame, text='▼', bg=self.theme.get_color('input_bg'), fg=self.theme.get_color('text_secondary'),
                         font=("Arial", 8), cursor='arrow', padx=5)
        arrow.pack(side='right')
        
        # Обновление отображаемого значения при изменении переменной
        def update_entry(*args):
            try:
                current = variable.get()                                   # Текущее значение из переменной
                # Переводим ключ в отображаемое значение
                display = self.tr.t(current) if current else ""
                entry.config(state='normal')                               # Временно разблокируем
                entry.delete(0, tk.END)                                    # Очищаем поле
                entry.insert(0, display)                                   # Вставляем переведенное значение
                entry.config(state='readonly')                             # Снова блокируем
            except (tk.TclError, AttributeError):                          # Игнорируем ошибки при уничтожении
                pass
        
        variable.trace_add('write', update_entry)                          # Отслеживаем изменения переменной
        update_entry()                                                     # Устанавливаем начальное значение
        
        # Сохраняем виджеты и данные как атрибуты фрейма
        frame.entry = entry
        frame.entry_frame = entry_frame
        frame.arrow = arrow
        frame.values = values
        frame.var = variable
        frame.font = font
        frame.dropdown_data = {'visible': False, 'window': None, 'listbox': None, 'handler': None}
        
        # Открытие выпадающего списка при клике
        def open_dropdown(e):
            self._toggle_combobox(frame, values, variable)
        
        entry.bind('<Button-1>', open_dropdown)                            # Клик по полю
        arrow.bind('<Button-1>', open_dropdown)                            # Клик по стрелке
        entry_frame.bind('<Button-1>', open_dropdown)                      # Клик по рамке
        return frame
    
    def _toggle_combobox(self, frame, values, variable):
        """Переключает видимость выпадающего списка"""
        data = frame.dropdown_data
        if data['visible']:                                                # Если открыт - закрываем
            self._close_combobox(frame)
        else:                                                              # Если закрыт - открываем
            self._open_combobox(frame, values, variable)
    
    def _open_combobox(self, frame, values, variable):
        """Открывает выпадающий список"""
        data = frame.dropdown_data
        frame.update_idletasks()                                           # Обновляем геометрию перед расчетами
        
        # Подготовка шрифта для измерения размеров
        font = self.get_font('combobox')
        import tkinter.font as tkfont
        tk_font = tkfont.Font(family=font[0], size=font[1], weight=font[2])
        
        # Расчет высоты окна
        item_height = tk_font.metrics('linespace') + 2                     # Высота одного пункта + отступы
        visible_items = len(values)                                        # Показываем все переданные значения
        height = visible_items * item_height                               # Общая высота списка
                                    
        width = frame.winfo_width()                                        # Ширина поля ввода
        
        # Позиция окна (под полем ввода)
        x = frame.winfo_rootx()                                            # X-координата левого края
        y = frame.winfo_rooty() + frame.winfo_height()                     # Y-координата под полем
        
        # Создание всплывающего окна
        window = tk.Toplevel(frame)
        window.wm_overrideredirect(True)                                   # Без рамок ОС
        window.configure(bg=self.theme.get_color('border_color'))          # Фон как у границы
        window.geometry(f"{width}x{height}+{x}+{y}")                       # Размер и позиция
        window.attributes('-topmost', True)                                # Поверх всех окон
        
        # Контейнер с отступом для рамки
        container = tk.Frame(window, bg=self.theme.get_color('border_color'), padx=1, pady=1)
        container.pack(fill='both', expand=True)
        
        # Список значений
        listbox = tk.Listbox(container, 
                             bg=self.theme.get_color('input_bg'),          # Фон как у поля ввода
                             fg=self.theme.get_color('text_color'),        # Цвет текста из темы
                             selectbackground=self.theme.get_color('accent_color'), # Цвет фона выбранной опции
                             selectforeground='white',                     # Белый цвет текста выбранной опции
                             borderwidth=0,                                # Без границы
                             highlightthickness=0,                         # Без подсветки
                             font=font,                                    # Тот же шрифт
                             activestyle='none',                           # Без подсветки при наведении
                             exportselection=False)                        # Не снимать выделение при потере фокуса
        
        # Заполнение списка значениями
        for value in values:
            listbox.insert('end', f"  {value}")                            # Добавляем отступ слева 2 пробела
        
        listbox.pack(side='left', fill='both', expand=True)                # Растягиваем на весь контейнер
        
        # Выделение текущего значения
        current_key = variable.get()
        current_display = self.tr.t(current_key) if current_key else ""
        if current_display in values:
            listbox.selection_set(values.index(current_display))
        
        # Выбор значения при клике
        def on_select(e):
            if listbox.curselection():                                     # Если что-то выделено
                idx = listbox.curselection()[0]                            # Берем первый (единственный) выделенный индекс
                selected_display = values[idx]                             # Отображаемое значение
                original_key = self.tr.to_key(selected_display)            # Получаем оригинальный ключ
                variable.set(original_key)                                 # Устанавливаем оригинальный ключ
                self._close_combobox(frame)                                # Закрываем выпадающий список
        
        listbox.bind('<<ListboxSelect>>', on_select)                       # Клик по элементу
        
        # Закрытие по Escape
        def on_escape(e):
            self._close_combobox(frame)                                    # Закрываем без изменения значения
            return "break"                                                 # Останавливаем дальнейшую обработку
        
        window.bind('<Escape>', on_escape)                                 # Обработчик для окна
        listbox.bind('<Escape>', on_escape)                                # Обработчик для списка
        
        # Глобальный обработчик клика (закрывает при клике вне области)
        def setup_click_handler():
            def on_click(e):
                if not data['visible'] or not data['window']:# Если окно уже закрыто - выходим
                    return
                # Координаты и размеры окна
                w = data['window']
                wx, wy = w.winfo_rootx(), w.winfo_rooty()
                ww, wh = w.winfo_width(), w.winfo_height()
                # Координаты и размеры комбобокса
                fx, fy = frame.winfo_rootx(), frame.winfo_rooty()
                fw, fh = frame.winfo_width(), frame.winfo_height()
                # Координаты клика
                cx, cy = e.x_root, e.y_root
                # Был ли клик внутри окна или внутри комбобокса
                in_window = wx <= cx <= wx + ww and wy <= cy <= wy + wh
                in_frame = fx <= cx <= fx + fw and fy <= cy <= fy + fh
                # Если клик вне окна и вне комбобокса - закрываем
                if not in_window and not in_frame:
                    self._close_combobox(frame)
            # Удаляем старый обработчик, если был
            if data['handler']:
                try:
                    frame.winfo_toplevel().unbind('<Button-1>', data['handler'])
                except:
                    pass
            # Устанавливаем новый обработчик
            handler = frame.winfo_toplevel().bind('<Button-1>', on_click, add='+')
            data['handler'] = handler
        setup_click_handler()
        # Сохраняем состояние и виджеты
        data.update({'visible': True, 'window': window, 'listbox': listbox})
        listbox.focus_set()
    
    def _close_combobox(self, frame):
        """Закрывает выпадающий список"""
        data = frame.dropdown_data
        # Отвязываем глобальный обработчик клика
        if data['handler']:
            try:
                frame.winfo_toplevel().unbind('<Button-1>', data['handler'])
            except:
                pass
        # Уничтожаем всплывающее окно
        if data['window'] and data['window'].winfo_exists():
            data['window'].destroy()
        # Сбрасываем состояние
        data.update({'visible': False, 'window': None, 'listbox': None, 'handler': None})

    def create_scrollbar(self, parent, orient="vertical", command=None, **kwargs):
        """Скроллбар (кастомный)"""
        style = ttk.Style()                                                     # Стиль для кастомизации внешнего вида
        
        if orient == "vertical":                                                # Для вертикальной ориентации
            style_name = "Custom.Vertical.TScrollbar"                           # Имя стиля для вертикального скроллбара
        else:                                                                   # Для горизонтальной ориентации
            style_name = "Custom.Horizontal.TScrollbar"                         # Имя стиля для горизонтального скроллбара
        
        # Цвета из текущей темы
        trough_color = self.theme.get_color('scrollbar_trough')                 # Цвет дорожки скроллбара
        slider_color = self.theme.get_color('scrollbar_slider')                 # Цвет ползунка в обычном состоянии
        slider_active = self.theme.get_color('scrollbar_slider_active')         # Цвет ползунка при нажатии / наведении
        arrow_color = self.theme.get_color('scrollbar_arrow')                   # Цвет стрелок на концах скроллбара
        border_color = self.theme.get_color('border_color')                     # Цвет границы
        
        style.configure(style_name,
            background=slider_color,                                            # Фон ползунка
            troughcolor=trough_color,                                           # Цвет дорожки
            arrowcolor=arrow_color,                                             # Цвет стрелок
            bordercolor=border_color,                                           # Цвет границы
            lightcolor=slider_color,                                            # Цвет светлой части (для 3D-эффекта)
            darkcolor=slider_color,                                             # Цвет темной части (для 3D-эффекта)
            relief='flat',                                                      # Плоский стиль (без 3D-выступов)
            borderwidth=0,                                                      # Без границы
            gripcount=0                                                         # Без насечек на ползунке
        )
        
        style.map(style_name,
            background=[                                                        # Цвет фона в разных состояниях
                ('pressed', slider_active),                                     # При нажатии - активный цвет
                ('active', slider_active),                                      # При наведении - активный цвет
                ('!active', slider_color)                                       # В обычном состоянии - обычный цвет
            ]
        )
        return ttk.Scrollbar(parent, orient=orient, command=command, style=style_name, **kwargs)

    def create_stat_row(self, parent, label_key, value=None):
        """Создает строку статистики"""
        row = self.create_frame(parent)                                         # Фрейм-контейнер для всей строки
        row.pack(fill='x', pady=0)
        label = self.create_label(row, label_key, 'small')                      # Левый текст (название статистики)
        label.pack(side='left')
        value_label = self.create_label(row, '', 'small_bold')                  # Правый текст (значение статистики)
        value_label.pack(side='right')
        if value is not None:                                                   # Если значение передано (None только для пустых строк)
            if isinstance(value, float):                                        # Для вещественных чисел
                rounding = self.app.settings['rounding_stats'].get()            # Количество знаков после запятой из настроек
                value_label.config(text=f"{value:.{rounding}f}")
            else:
                value_label.config(text=str(value))                             # Преобразуем в строку и отображаем
        return row, value_label
    
    def create_stat_column(self, parent, title_key, data_keys):
        """Создает колонку со статистикой из списка data-ключей"""
        title = self.create_labelframe(parent, title_key)
        title.pack(fill='both', expand=True)
        content = title.content
        labels = {}
        
        for data_key in data_keys:
            if data_key == '' or data_key is None:
                separator = self.create_frame(content)
                separator.pack(fill='x', pady=5)
                labels[data_key] = None
            else:
                # Получаем UI-ключ для отображения
                ui_key = StatisticsCalculator.data_key_to_ui_key(data_key)
                row, label = self.create_stat_row(content, ui_key)
                labels[data_key] = label
        
        return labels


# In[22]:


class AlignedSection:
    """Класс сгруппированных и выровненных виджетов"""
    
    def __init__(self, parent, factory, app, title_key=None):
        """Инициализация секции с опциональным заголовком"""
        self.factory = factory  # Фабрика виджетов
        self.app = app  # Ссылка на главное приложение
        self.rows = []  # Список добавленных строк
        self.current_row = 0  # Текущая строка сетки
        
        if title_key:  # Создание с заголовком
            container = factory.create_labelframe(parent, title_key)  # Фрейм с заголовком
            self.frame = container  # Весь контейнер
            self.content = container.content  # Контент внутри рамки
        else:  # Создание без заголовка
            self.frame = factory.create_frame(parent)  # Обычный фрейм
            self.content = self.frame  # Контент - сам фрейм
        
        self.content.columnconfigure(0, weight=0)  # Колонка лейбла (фиксированная)
        self.content.columnconfigure(1, weight=1)  # Колонка виджета (растяжимая)
    
    def _create_entry_scale_pair(self, variable, show_entry, parent, param_config, scale_size='normal', entry_size='default',
                                 expand_scale=False, param_name=None, dist_type=None, domain=None):
        """Создание пары [поле ввода] + [слайдер] для одной переменной"""
        frame = self.factory.create_frame(parent)  # Контейнер для пары
        entry = None  # Инициализация поля ввода
        
        if show_entry:  # Поле ввода требуется
            entry = self.factory.create_entry(frame, variable, param_name, domain, dist_type, size=entry_size)  # Создание поля
            entry.pack(side='left', padx=(0, 10))  # Размещение с отступом справа
        
        min_val, max_val = param_config['range']  # Диапазон значений
        resolution = 1 if param_config.get('is_int', False) else 10 ** (-self.app.settings['rounding_input'].get())  # Шаг изменения
        
        scale = self.factory.create_scale(frame, variable, from_=min_val, to_=max_val, resolution=resolution, size=scale_size)  # Создание слайдера
        if expand_scale:  # Растяжение слайдера
            scale.pack(side='left', fill='x', expand=True)  # Растяжение по горизонтали
        else:  # Без растяжения
            scale.pack(side='left')  # Компактное размещение
        
        return frame, entry, scale  # Возврат контейнера, поля и слайдера
    
    def add_row(self, variable, param_name, dist_type, domain, label_key=None, show_label=True, show_entry=True,
                scale_size='normal', expand_scale=False):
        """Добавление строки [лейбл] + [поле ввода] + [слайдер]"""
        param_config = self.app.validator.get_param_config(domain, dist_type, param_name)  # Конфигурация параметра
        
        pair_frame, entry, scale = self._create_entry_scale_pair(variable=variable, show_entry=show_entry, parent=self.content,
                                        param_config=param_config, scale_size=scale_size, expand_scale=expand_scale,
                                        param_name=param_name, dist_type=dist_type, domain=domain)  # Создание пары
        
        label = None  # Инициализация лейбла
        if show_label and label_key:  # Отображение лейбла
            label = self.factory.create_label(self.content, label_key, 'normal')  # Создание лейбла
            label.grid(row=self.current_row, column=0, sticky='w', padx=(0, 10))  # Размещение в первой колонке
            pair_frame.grid(row=self.current_row, column=1, sticky='ew', pady=3)  # Размещение во второй колонке
        else:  # Без лейбла
            pair_frame.grid(row=self.current_row, column=0, columnspan=2, sticky='ew', pady=3)  # На всю ширину
        
        self.rows.append({'type': 'row', 'label': label, 'entry': entry, 'scale': scale, 'variable': variable, 'frame': pair_frame})  # Сохранение
        self.current_row += 1  # Увеличение счетчика строк
        
        return pair_frame, entry, scale  # Возврат созданных виджетов
    
    def add_dual_row(self, top_label, bottom_label, top_var, bottom_var, top_param, bottom_param, dist_type, domain='edge'):
        """Добавление двойной строки с синхронизацией двух слайдеров"""
        
        top_config = self.app.validator.get_param_config(domain, dist_type, top_param)  # Конфигурация верхнего параметра
        bottom_config = self.app.validator.get_param_config(domain, dist_type, bottom_param)  # Конфигурация нижнего параметра
        
        top_label_widget = self.factory.create_label(self.content, top_label, 'normal')  # Лейбл верхнего слайдера
        top_label_widget.grid(row=self.current_row, column=0, sticky='w', padx=(0, 10))  # Размещение лейбла
        
        top_pair, top_entry, top_scale = self._create_entry_scale_pair(top_var, True, self.content, top_config, 
            param_name=top_param, dist_type=dist_type, domain=domain)  # Создание верхней пары
        top_pair.grid(row=self.current_row, column=1, sticky='ew', pady=(0, 5))  # Размещение
        self.current_row += 1  # Увеличение счетчика
        
        bottom_label_widget = self.factory.create_label(self.content, bottom_label, 'normal')  # Лейбл нижнего слайдера
        bottom_label_widget.grid(row=self.current_row, column=0, sticky='w', padx=(0, 10))  # Размещение лейбла
        
        bottom_pair, bottom_entry, bottom_scale = self._create_entry_scale_pair(bottom_var, True, self.content, bottom_config,
            param_name=bottom_param, dist_type=dist_type, domain=domain)  # Создание нижней пары
        bottom_pair.grid(row=self.current_row, column=1, sticky='ew', pady=3)  # Размещение
        self.current_row += 1  # Увеличение счетчика
        
        gap = self.app.validator.gap  # Минимальный зазор
        tolerance = self.app.validator.tolerance  # Точность сравнения
        rounding = self.app.settings['rounding_input'].get()  # Точность округления
        
        left_min, left_max = top_config['range']  # Диапазон левого слайдера
        right_min, right_max = bottom_config['range']  # Диапазон правого слайдера
        
        self._syncing = False  # Флаг для предотвращения рекурсии
        
        def sync(source='both'):
            """Синхронизация значений двух слайдеров"""
            if self._syncing:  # Предотвращение рекурсии
                return
            
            self._syncing = True  # Установка флага
            try:
                top = top_var.get()  # Текущее значение левого слайдера
                bottom = bottom_var.get()  # Текущее значение правого слайдера
                changed = False  # Флаг изменения
                
                if source in ('top', 'both') and top >= bottom - gap:  # Нарушение зазора
                    new_bottom = min(top + gap, right_max)  # Увеличение правого значения
                    new_bottom = round(new_bottom, rounding)  # Округление
                    if abs(new_bottom - bottom) > tolerance:  # Значение изменилось
                        bottom_var.set(new_bottom)  # Обновление правого слайдера
                        changed = True  # Отметка изменения
                        if new_bottom == right_max and top >= new_bottom - gap:  # Достигнут максимум
                            new_top = max(new_bottom - gap, left_min)  # Уменьшение левого
                            new_top = round(new_top, rounding)  # Округление
                            if abs(new_top - top) > tolerance:  # Значение изменилось
                                top_var.set(new_top)  # Обновление левого слайдера
                
                if source in ('bottom', 'both') and bottom <= top + gap:  # Нарушение зазора
                    new_top = max(bottom - gap, left_min)  # Уменьшение левого значения
                    new_top = round(new_top, rounding)  # Округление
                    if abs(new_top - top) > tolerance:  # Значение изменилось
                        top_var.set(new_top)  # Обновление левого слайдера
                        changed = True  # Отметка изменения
                        if new_top == left_min and bottom <= new_top + gap:  # Достигнут минимум
                            new_bottom = min(new_top + gap, right_max)  # Увеличение правого
                            new_bottom = round(new_bottom, rounding)  # Округление
                            if abs(new_bottom - bottom) > tolerance:  # Значение изменилось
                                bottom_var.set(new_bottom)  # Обновление правого слайдера
                
                if changed and hasattr(self, '_on_dual_change'):  # Вызов колбэка при изменении
                    self._on_dual_change(top_var.get(), bottom_var.get())
                    
            finally:
                self._syncing = False  # Сброс флага
        
        top_scale.config(command=lambda v: sync('top'))  # Синхронизация при движении левого слайдера
        bottom_scale.config(command=lambda v: sync('bottom'))  # Синхронизация при движении правого слайдера
        top_var.trace_add('write', lambda *a: sync('top'))  # Синхронизация при программном изменении левого
        bottom_var.trace_add('write', lambda *a: sync('bottom'))  # Синхронизация при программном изменении правого
        return top_pair, bottom_pair  # Возврат контейнеров
    
    def add_combo_row(self, combo_label, combo_keys, combo_var, size='default'):
        """Добавление строки [лейбл] + [комбобокс]"""
        label = self.factory.create_label(self.content, combo_label, 'normal')  # Создание лейбла
        label.grid(row=self.current_row, column=0, sticky='w', padx=(0, 10))  # Размещение в первой колонке
        
        translated_values = [self.factory.tr.t(key) for key in combo_keys]  # Перевод ключей
        combo = self.factory.create_combobox(self.content, translated_values, combo_var, size=size)  # Создание комбобокса
        combo.grid(row=self.current_row, column=1, sticky='w', pady=3)  # Размещение во второй колонке
        
        self.rows.append({'type': 'combo', 'label': label, 'combo': combo, 'variable': combo_var})  # Сохранение строки
        self.current_row += 1  # Увеличение счетчика
        return combo  # Возврат комбобокса
    
    
    def add_combo_with_field(self, combo_label, combo_keys, combo_var, field_label, field_var,
                             field_param, field_dist, field_domain='edge', 
                             hide_when_value='None', scale_size='normal', combo_size='wide'):
        """Добавление строки с комбобоксом и полем ввода справа"""
        self.content.columnconfigure(0, weight=0, minsize=120)  # Колонка лейбла
        self.content.columnconfigure(1, weight=0, minsize=180)  # Колонка комбобокса
        self.content.columnconfigure(2, weight=0)  # Колонка поля (фиксированная)
        
        label = self.factory.create_label(self.content, combo_label, 'normal')  # Создание лейбла
        label.grid(row=self.current_row, column=0, sticky='w', padx=(0, 10), pady=3)  # Размещение
        
        translated_keys = [self.factory.tr.t(key) for key in combo_keys]  # Перевод ключей
        combo = self.factory.create_combobox(self.content, translated_keys, combo_var, size=combo_size)  # Создание комбобокса
        combo.grid(row=self.current_row, column=1, sticky='w', padx=(0, 10), pady=3)  # Размещение
        
        field_container = self.factory.create_frame(self.content)  # Контейнер для поля
        field_container.grid(row=self.current_row, column=2, sticky='w', pady=3)  # Размещение
        
        if field_label:  # Создание лейбла для поля
            field_label_widget = self.factory.create_label(field_container, field_label, 'normal')  # Лейбл
            field_label_widget.pack(side='left', padx=(0, 5))  # Размещение слева с отступом
        
        field_config = self.app.validator.get_param_config(field_domain, field_dist, field_param)  # Конфигурация
        field_pair, field_entry, field_scale = self._create_entry_scale_pair(
            field_var, True, field_container, field_config, scale_size=scale_size,
            param_name=field_param, dist_type=field_dist, domain=field_domain,
            expand_scale=False)  # Создание пары
        field_pair.pack(side='left')  # Размещение без растяжения
        
        def toggle_field(*args):
            """Переключение видимости поля в зависимости от выбора комбобокса"""
            current_display = combo_var.get()  # Текущее отображаемое значение
            original_value = self.factory.tr.to_key(current_display)  # Оригинальный ключ
            if original_value == hide_when_value:  # Скрытие при определенном значении
                field_container.grid_remove()  # Скрытие контейнера
            else:  # Показ во всех остальных случаях
                field_container.grid()  # Показ контейнера
        
        combo_var.trace_add('write', toggle_field)  # Отслеживание изменения комбобокса
        toggle_field()  # Начальная установка видимости
        
        self.rows.append({
            'type': 'combo_with_field',
            'combo': combo,
            'field_container': field_container,
            'field_var': field_var,
        })  # Сохранение строки
        self.current_row += 1  # Увеличение счетчика
        
        return combo, field_pair  # Возврат комбобокса и контейнера поля
    
    def add_combo_with_subrow(self, combo_label, combo_keys, combo_var, 
                              sub_label, sub_var, 
                              sub_param=None, sub_dist=None, sub_domain='edge', 
                              hide_when_value='None'):
        """Добавление строки с комбобоксом и подстрокой ниже"""
        if self.current_row == 0:  # Настройка колонок для первой строки
            self.content.columnconfigure(0, weight=0, minsize=120)  # Колонка лейбла
            self.content.columnconfigure(1, weight=1)  # Колонка комбобокса (растяжимая)
        
        label = self.factory.create_label(self.content, combo_label, 'normal')  # Создание лейбла
        label.grid(row=self.current_row, column=0, sticky='w', padx=(0, 10), pady=3)  # Размещение
        
        translated_keys = [self.factory.tr.t(key) for key in combo_keys]  # Перевод ключей
        combo = self.factory.create_combobox(self.content, translated_keys, combo_var, size='wide')  # Создание комбобокса
        combo.grid(row=self.current_row, column=1, sticky='ew', pady=3)  # Размещение с растяжением
        self.current_row += 1  # Увеличение счетчика
        
        sub_row_frame = self.factory.create_frame(self.content)  # Фрейм для подстроки
        sub_row_frame.grid(row=self.current_row, column=0, columnspan=2, sticky='ew', pady=3)  # Размещение на две колонки
        sub_row_frame.columnconfigure(0, weight=0, minsize=120)  # Колонка для лейбла подстроки
        sub_row_frame.columnconfigure(1, weight=1)  # Колонка для поля
        
        sub_label_widget = self.factory.create_label(sub_row_frame, sub_label, 'normal')  # Лейбл подстроки
        sub_label_widget.grid(row=0, column=0, sticky='w', padx=(0, 10))  # Размещение
        
        field_container = self.factory.create_frame(sub_row_frame)  # Контейнер для поля
        field_container.grid(row=0, column=1, sticky='ew')  # Размещение
        
        sub_config = self.app.validator.get_param_config(sub_domain, sub_dist, sub_param)  # Конфигурация
        sub_pair, sub_entry, sub_scale = self._create_entry_scale_pair(
            variable=sub_var,
            show_entry=True,
            parent=field_container,
            param_config=sub_config,
            param_name=sub_param,
            dist_type=sub_dist,
            domain=sub_domain,
            expand_scale=True)  # Создание пары с растяжением
        sub_pair.pack(side='left', fill='x', expand=True)  # Размещение с заполнением
        
        def toggle_subrow(*args):
            """Переключение видимости подстроки в зависимости от выбора комбобокса"""
            current_display = combo_var.get()  # Текущее отображаемое значение
            original_value = self.factory.tr.to_key(current_display)  # Оригинальный ключ
            if original_value == hide_when_value:  # Скрытие при определенном значении
                sub_row_frame.grid_remove()  # Скрытие фрейма
            else:  # Показ во всех остальных случаях
                sub_row_frame.grid()  # Показ фрейма
        
        combo_var.trace_add('write', toggle_subrow)  # Отслеживание изменения комбобокса
        toggle_subrow()  # Начальная установка видимости
        
        self.rows.append({
            'type': 'combo_with_subrow',
            'combo': combo,
            'sub_row': sub_row_frame,
            'sub_var': sub_var,
        })  # Сохранение строки
        
        self.current_row += 1  # Увеличение счетчика
        return sub_pair  # Возврат контейнера подстроки
    
    def pack(self, **kwargs):
        """Упаковка фрейма секции в родительский виджет"""
        self.frame.pack(**kwargs)  # Передача параметров упаковки
    
    def grid(self, **kwargs):
        """Размещение фрейма секции в сетке"""
        self.frame.grid(**kwargs)  # Передача параметров сетки


# In[23]:


class ParameterSectionFactory:
    """Фабрика для создания секций параметров (устойчивость, влияние, затухание)"""
    
    def __init__(self, app):
        """Инициализация фабрики с ссылкой на главное приложение"""
        self.app = app  # Ссылка на главное приложение
        self._keys_map = {  # Словарь ключей для каждого типа параметра
            'resistance': ['None', 'param_direct', 'param_inverse'],  # Варианты устойчивости
            'influence': ['None', 'param_direct', 'param_inverse'],  # Варианты влияния
            'damping': ['None', 'damping_exponential', 'damping_hyperbolic', 'damping_discrete']  # Варианты затухания
        }
    
    def get_display_value(self, param_type, original_value):
        """Возврат отображаемого значения для параметра через переводчик"""
        return self.app.translator.t(original_value)  # Перевод оригинального ключа
    
    def get_original_value(self, param_type, display_value):
        """Возврат оригинального значения из отображаемого через обратный перевод"""
        return self.app.translator.to_key(display_value)  # Получение ключа по переводу
    
    def create_section(self, param_type, container, ui_vars, layout='subrow'):
        """Создание секции параметра (устойчивость, влияние или затухание)"""
        keys = self._keys_map[param_type]  # Список ключей для данного типа параметра
        display_var = ui_vars[f'{param_type}_display']  # Переменная для отображения в комбобоксе
        coeff_var = ui_vars[f'{param_type}_coeff']  # Переменная для коэффициента
        
        section = AlignedSection(container, self.app.widget_factory, self.app, None)  # Секция без заголовка
        
        if layout == 'field':  # Горизонтальный макет (поле справа от комбобокса)
            section.add_combo_with_field(
                combo_label=f'{param_type}_type',  # Лейбл комбобокса
                combo_keys=keys,  # Ключи для выпадающего списка
                combo_var=display_var,  # Переменная отображения
                field_label='coeff',  # Лейбл поля коэффициента
                field_var=coeff_var,  # Переменная коэффициента
                field_param=f'{param_type}_coeff',  # Имя параметра в конфигурации
                field_dist='global',  # Тип распределения (глобальный параметр)
                field_domain='global'  # Домен параметра
            )
        else:  # Вертикальный макет (подстрока ниже комбобокса)
            section.add_combo_with_subrow(
                combo_label=f'{param_type}_type',  # Лейбл комбобокса
                combo_keys=keys,  # Ключи для выпадающего списка
                combo_var=display_var,  # Переменная отображения
                sub_label='coeff',  # Лейбл подстроки
                sub_var=coeff_var,  # Переменная коэффициента
                sub_param=f'{param_type}_coeff',  # Имя параметра в конфигурации
                sub_dist='global',  # Тип распределения (глобальный параметр)
                sub_domain='global'  # Домен параметра
            )
        
        combo = section.rows[-1]['combo']  # Извлечение виджета комбобокса
        
        def on_combo_change(*args):
            """Обработчик изменения выбора в комбобоксе"""
            display = display_var.get()  # Текущее отображаемое значение
            original = self.app.translator.to_key(display)  # Получение оригинального ключа
            ui_vars[f'{param_type}_type'].set(original)  # Сохранение оригинального значения
        
        display_var.trace_add('write', on_combo_change)  # Отслеживание изменений переменной отображения
        
        return section, display_var, coeff_var, combo  # Возврат секции и переменных


# In[24]:


class ScrollableFrame:
    """Фрейм с вертикальной прокруткой, который правильно растягивается по ширине"""
    
    # Класс для всех скроллов на всех вкладках и в дочерних окнах
    _all_scrolls = []  # список всех созданных скроллов
    
    def __init__(self, parent, factory):
        self.factory = factory
        
        # внешний контейнер
        self.container = factory.create_frame(parent)
        
        # canvas для прокрутки
        self.canvas = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), highlightthickness=0)
        # scrollbar
        self.scrollbar = self.factory.create_scrollbar(self.container, orient='vertical', command=self.canvas.yview)
        # внутренний фрейм с содержимым
        self.inner = factory.create_frame(self.canvas)
        # настройка прокрутки
        self.inner.bind('<Configure>', self._on_inner_configure)
        # окно внутри canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor='nw', tags='inner_frame')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # привязка изменения размера canvas
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        # упаковка
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
        # Регистрируем скролл в общем списке
        # Проверяем ДО добавления - это первый экземпляр?
        is_first_scroll = (len(ScrollableFrame._all_scrolls) == 0)
        ScrollableFrame._all_scrolls.append(self)
        
        # Привязываем глобальный обработчик колеса мыши к корневому окну один раз
        if is_first_scroll:
            root = parent.winfo_toplevel()
            root.bind_all('<MouseWheel>', ScrollableFrame._global_mousewheel_handler)
    
    @classmethod
    def _global_mousewheel_handler(cls, event):
        """Глобальный обработчик колесика мыши с учетом перекрытия окон"""
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if widget is None:
            return "break"
        
        # Проверяем ScrollableFrame
        for scroll in cls._all_scrolls:
            if scroll._is_ancestor_of(widget):
                scroll.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
                return "break"
        
        # Проверяем SplitScrollFrame
        for scroll in SplitScrollFrame._all_scrolls:
            if scroll._is_ancestor_of(widget):
                scroll.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
                return "break"
        
        return "break"
    
    def _is_ancestor_of(self, widget):
        """Проверяет, является ли canvas этого скролла предком виджета widget"""
        parent = widget
        while parent is not None:
            if parent is self.canvas:
                return True
            parent = parent.master  # Поднимаемся вверх по дереву виджетов
        return False
    
    def _on_inner_configure(self, event):
        """Обновляет область прокрутки при изменении внутреннего фрейма"""
        bbox = self.canvas.bbox('all')
        if bbox:
            self.canvas.configure(scrollregion=bbox)
    
    def _on_canvas_configure(self, event):
        """Обновляет ширину внутреннего фрейма при изменении размера canvas"""
        if self.inner.winfo_reqwidth() != event.width:
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            self.inner.config(width=event.width)
            self.inner.update_idletasks()
    
    def pack(self, **kwargs):
        """Упаковывает контейнер"""
        self.container.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Размещает контейнер в сетке"""
        self.container.grid(**kwargs)
    
    def pack_forget(self):
        """Скрывает контейнер"""
        self.container.pack_forget()
    
    def grid_forget(self):
        """Скрывает контейнер из сетки"""
        self.container.grid_forget()
    
    def destroy(self):
        """Уничтожает все виджеты и удаляет себя из списка"""
        # Удаляем себя из общего списка скроллов
        if self in ScrollableFrame._all_scrolls:
            ScrollableFrame._all_scrolls.remove(self)
        # Уничтожаем контейнер со всем содержимым
        self.container.destroy()


# In[25]:


class SplitScrollFrame:
    """Две панели: левая фиксированная, правая с прокруткой"""
    
    _all_scrolls = []  # Список всех созданных скроллов
    
    def __init__(self, parent, factory, app):
        self.factory = factory
        self.app = app
        left_width = app.size_config['container']['side_panel']['width']
        # Основной контейнер
        self.container = factory.create_frame(parent)
        # Левая панель (фиксированная ширина)
        self.left_panel = factory.create_frame(self.container, width=left_width)
        self.left_panel.pack(side='left', fill='y', padx=(0, 10))
        self.left_panel.pack_propagate(False)
        # Правая панель с прокруткой
        self.right_container = factory.create_frame(self.container)
        self.right_container.pack(side='left', fill='both', expand=True)
        # Canvas для прокрутки правой панели
        self.canvas = tk.Canvas(self.right_container, bg=factory.theme.get_color('bg_color'), highlightthickness=0)
        # Scrollbar для правой панели
        self.scrollbar = self.factory.create_scrollbar(self.right_container, orient='vertical', command=self.canvas.yview)
        # Внутренний фрейм для контента справа
        self.right_content = factory.create_frame(self.canvas)
        # Окно внутри canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.right_content, anchor='nw')
        # Настройка прокрутки
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Упаковка правой панели
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        # Привязка событий
        self.right_content.bind('<Configure>', self._on_right_content_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        # Регистрируем скролл в общем списке
        is_first = (len(ScrollableFrame._all_scrolls) + len(SplitScrollFrame._all_scrolls)) == 0
        SplitScrollFrame._all_scrolls.append(self)
        # Привязываем глобальный обработчик колеса мыши один раз
        if is_first:
            root = parent.winfo_toplevel()
            root.bind_all('<MouseWheel>', ScrollableFrame._global_mousewheel_handler)
    
    def _on_right_content_configure(self, event):
        """Обновляет scrollregion при изменении содержимого"""
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _on_canvas_configure(self, event):
        """Обновляет ширину внутреннего фрейма при изменении размера canvas"""
        if self.right_content.winfo_reqwidth() != event.width:
            self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _is_ancestor_of(self, widget):
        """Проверяет, принадлежит ли виджет этому скроллу"""
        parent_widget = widget
        while parent_widget is not None:
            if parent_widget is self.canvas or parent_widget is self.right_container:
                return True
            parent_widget = parent_widget.master
        return False
    
    def yview_moveto(self, fraction):
        """Прокручивает правую панель к указанной позиции (0.0 - верх, 1.0 - низ)"""
        self.canvas.yview_moveto(fraction)
    
    def get_left(self):
        """Возвращает левую панель для добавления элементов"""
        return self.left_panel
    
    def get_right(self):
        """Возвращает правую прокручиваемую панель"""
        return self.right_content
    
    def pack(self, **kwargs):
        self.container.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.container.grid(**kwargs)
    
    def destroy(self):
        """Уничтожает все виджеты и удаляет себя из списка"""
        if self in SplitScrollFrame._all_scrolls:
            SplitScrollFrame._all_scrolls.remove(self)
        self.container.destroy()


# In[26]:


class GraphDisplay:
    """Отображение графа"""
    
    DPI = 100  # Разрешение для качества прорисовки графа
        
    def __init__(self, parent, factory, app):
        self.factory = factory  # Фабрика виджетов
        self.app = app          # Главное приложение
        self.parent = parent    # Родительский виджет
        self.frame = factory.create_frame(parent)  # Рамка для графа
        
        # Настройка размеров
        screen_width = app.root.winfo_screenwidth()                              # Ширина экрана
        right_panel_width = app.size_config['container']['side_panel']['width']  # Ширина правой панели
        graph_width_px = screen_width - right_panel_width                        # Ширина графа в пикселях
        graph_height_px = app.size_config['container']['graph_panel']['height']  # Высота графа в пикселях
        
        # Создание figure
        self.figure = Figure(figsize=(graph_width_px / self.DPI, graph_height_px / self.DPI),
                             facecolor=factory.theme.get_color('bg_color'), dpi=self.DPI)
        self.ax = self.figure.add_axes([0, 0, 1, 1])  # Оси во всю область [left, bottom, width, height]
        self.ax.set_axis_off()      # Отключение осей
        self.ax.margins(0)          # Нулевые отступы
        self.ax.set_aspect('auto')  # Автоматическое соотношение сторон
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)  # Холст tkinter
        self.canvas.get_tk_widget().pack(expand=False, fill='none')      # Упаковка холста
        
        # Кэши
        self.pos_cache = None              # Кэш позиций вершин
        self.last_graph_id = None          # Идентификатор последнего графа
        self._cached_edge_segments = None  # Кэш сегментов ребер
        self._cached_edge_weights = None   # Кэш весов ребер
        self._cached_graph_hash = None     # Хеш графа для кэша
        
        # Цвета из темы
        self.vertex_color = factory.theme.get_color('graph_vertex')          # Цвет вершин
        self.vertex_border = factory.theme.get_color('graph_vertex_border')  # Цвет границ вершин
        self.text_color = factory.theme.get_color('text_color')              # Цвет текста
        
        # Цветовые шкалы
        from matplotlib.colors import LinearSegmentedColormap
        self.edge_cmap_custom = LinearSegmentedColormap.from_list('custom_edge', factory.theme.get_color('custom_edge_cmap'), N=256)  # Ребра
        self.fire_cmap_custom = LinearSegmentedColormap.from_list('custom_fire', factory.theme.get_color('custom_fire_cmap'), N=256)  # Огонь
        
        # Упрощенные цвета
        self.simple_negative_color = self.edge_cmap_custom(0.0)  # Цвет отрицательного веса
        self.simple_positive_color = self.edge_cmap_custom(1.0)  # Цвет положительного веса
        
        self.data = None               # Данные графа
        self.burned_nodes = {}         # Словарь горящих вершин
        self.burned_edges = {}         # Словарь горящих ребер
        self.show_fire = False         # Флаг отображения пожара
        self.added_vertices_count = 0  # Счетчик добавленных вершин (для перерисовки при добавлении вершин)

    def _get_graph_hash(self, graph):
        """Возвращает хеш графа для проверки изменений"""
        return (graph.number_of_nodes(), graph.number_of_edges(), id(graph))  # Количество вершин, количество ребер, id объекта
    
    def set_graph_data(self, data):
        """Устанавливает данные графа и сбрасывает кэш"""
        self.data = data                     # Сохранение данных графа
        self.pos_cache = data.pos_cache      # Восстановление кэша позиций
        self.last_graph_id = id(data.graph)  # Сохранение идентификатора графа
        self._cached_edge_segments = None    # Сброс кэша сегментов ребер
        self._cached_edge_weights = None     # Сброс кэша весов ребер
        self.added_vertices_count = 0        # Сброс счетчика добавленных вершин
    
    def set_fire_data(self, burned_nodes, burned_edges):
        """Устанавливает данные о пожаре"""
        self.burned_nodes = burned_nodes     # Сохранение горящих вершин
        self.burned_edges = burned_edges     # Сохранение горящих ребер
        self.show_fire = bool(burned_nodes)  # Флаг отображения пожара (True если есть горящие вершины)
        self.draw()                          # Перерисовка графа
    
    def clear_fire(self):
        """Очищает данные о пожаре"""
        self.burned_nodes = {}  # Очистка словаря горящих вершин
        self.burned_edges = {}  # Очистка словаря горящих ребер
        self.show_fire = False  # Выключение флага пожара
        self.draw()             # Перерисовка графа

    def invalidate(self):
        """Сбрасывает кэш для принудительной перерисовки"""
        self._cached_edge_segments = None  # Сброс кэша сегментов ребер
        
    def rebuild_layout(self):
        """Полное перестроение графа с пересчетом layout"""
        if self.pos_cache is not None:                          # Проверка существования кэша позиций
            self.pos_cache = self._get_layout(self.data.graph)  # Пересчет компоновки графа
            self.last_graph_id = id(self.data.graph)            # Обновление идентификатора графа
            self._cached_edge_segments = None                   # Сброс кэша сегментов ребер
            self.added_vertices_count = 0                       # Сброс счетчика добавленных вершин
            self.draw()                                         # Перерисовка графа
    
    def add_vertex_at_random_position(self, node):
        """Добавляет вершину в случайное место"""
        if self.pos_cache is None or id(self.data.graph) != self.last_graph_id:  # Проверка необходимости пересчета кэша
            self.pos_cache = self._get_layout(self.data.graph)    # Пересчет компоновки графа
            self.last_graph_id = id(self.data.graph)              # Обновление идентификатора графа
        new_pos = (random.uniform(-1, 1), random.uniform(-1, 1))  # Генерация случайных координат X и Y
        self.pos_cache[node] = new_pos                            # Сохранение позиции новой вершины в кэше
        if self.data:
            self.data.pos_cache = self.pos_cache
        self.last_graph_id = id(self.data.graph)                  # Обновление идентификатора графа
        self._cached_edge_segments = None                         # Сброс кэша сегментов ребер (появятся новые ребра)
        self.draw()                                               # Перерисовка графа
        return new_pos                                            # Возврат координат добавленной вершины
    
    def remove_vertex(self, node):
        """Удаляет вершину из кэша позиций с перенумерацией"""
        if self.pos_cache is None:  # Проверка существования кэша позиций
            self.draw()             # Перерисовка графа (без кэша)
            return
        del self.pos_cache[node]  # Удаление вершины из кэша позиций
        # Перенумерация оставшихся вершин
        # Сортировка оставшихся вершин по числовому индексу (после V)
        remaining_nodes = sorted(self.pos_cache.keys(), key=lambda x: int(x[1:]))  
        # Создание нового словаря с перенумерованными ключами
        self.pos_cache = {f'V{i}': self.pos_cache[old_node] for i, old_node in enumerate(remaining_nodes)}  
        if self.data:
            self.data.pos_cache = self.pos_cache
        self.last_graph_id = id(self.data.graph)  # Обновление идентификатора графа
        self._cached_edge_segments = None         # Сброс кэша сегментов ребер
        self.draw()                               # Перерисовка графа
    
    def draw(self):
        """Рисует граф с использованием кэшированных позиций"""     
        # Проверка настройки "Не отображать граф"
        if self.app.settings.get('hide_graph_display', tk.BooleanVar(value=False)).get():
            self.ax.clear()
            self.ax.set_axis_off()
            self.ax.set_facecolor(self.factory.theme.get_color('bg_color'))
            self.canvas.draw()
            return
            
        # Обновление позиций при необходимости
        if self.pos_cache is None or id(self.data.graph) != self.last_graph_id:
            self.pos_cache = self._get_layout(self.data.graph)
            self.last_graph_id = id(self.data.graph)
            self._cached_edge_segments = None
            if self.data:
                self.data.pos_cache = self.pos_cache
        
        # Дополнительная проверка: если есть горящие ребра, но не все вершины в кэше
        if self.show_fire and self.burned_edges:
            burned_vertices = set()
            for u, v in self.burned_edges.keys():
                burned_vertices.add(u)
                burned_vertices.add(v)
            
            # Проверяем, все ли вершины есть в pos_cache
            missing_vertices = burned_vertices - set(self.pos_cache.keys())
            if missing_vertices:
                # Перестраиваем кэш полностью
                self.pos_cache = self._get_layout(self.data.graph)
                self.last_graph_id = id(self.data.graph)
                self._cached_edge_segments = None
                if self.data:
                    self.data.pos_cache = self.pos_cache
        
        self.ax.clear()
        self.ax.set_axis_off()
        self.ax.set_facecolor(self.factory.theme.get_color('bg_color'))
        pos = self.pos_cache
        graph = self.data.graph
        
        # Отрисовка ребер
        show_edges = self.app.settings.get('show_edges', tk.BooleanVar(value=True)).get()
        if show_edges:
            show_negative = self.app.settings.get('show_negative_edges', tk.BooleanVar(value=True)).get()
            self._draw_non_burning_edges(graph, pos, show_negative)
        if self.show_fire and self.burned_edges:
            self._draw_burning_edges(graph, pos)
        
        # Отрисовка вершин
        self._draw_all_vertices(graph, pos)
        self.canvas.draw()
    
    def _get_layout(self, graph):
        """Возвращает словарь позиций вершин по типу {'V0': (x0, y0), ...}, где вершина V0 с координатами (x0, y0)"""
        layout_type = self.app.settings['layout_type'].get()  # Получение типа компоновки из настроек
        
        if layout_type == 'layout_spring':      # Если "пружинная модель"
            return nx.spring_layout(graph, seed=42, iterations=100) # Из коробки nx.spring_layout
        elif layout_type == 'layout_circular':  # Если "круговая"
            return nx.circular_layout(graph)  # Равномерное расположение вершин по окружности
        elif layout_type == 'layout_random':    # Если "случайная"
            return nx.random_layout(graph, seed=42)  # Случайное расположение вершин внутри холста
        elif layout_type == 'layout_grid':      # Если "сеточная" (как на клетчатой бумаге)
            n = graph.number_of_nodes()       # Количество вершин
            cols = int(np.ceil(np.sqrt(n)))   # Количество столбцов
            rows = int(np.ceil(n / cols))     # Количество строк
            pos = {}                          # Словарь позиций вершин
            for i, node in enumerate(graph.nodes()):
                row, col = divmod(i, cols)                          # Вычисление номера строки и столбца
                x = -1 + (2 * col / (cols - 1)) if cols > 1 else 0  # Координата X
                y = 1 - (2 * row / (rows - 1)) if rows > 1 else 0   # Координата Y
                pos[node] = (x, y)                                  # Сохранение позиции вершины
            return pos
    
    def _draw_non_burning_edges(self, graph, pos, show_negative_edges):
        """Рисует все негорящие ребра""" 
        current_hash = (self._get_graph_hash(graph), show_negative_edges, id(self.burned_edges))  # Хеш для проверки изменений графа
        
        if self._cached_edge_segments is None or self._cached_graph_hash != current_hash:  # Проверка необходимости обновления кэша
            self._build_edge_cache(graph, pos, show_negative_edges)                        # Построение кэша сегментов и весов ребер
            self._cached_graph_hash = current_hash                                         # Сохранение хеша для будущих сравнений
        
        if not self._cached_edge_segments:  # Проверка наличия ребер для отрисовки
            return
        
        # Адаптивные параметры
        n_nodes = graph.number_of_nodes()  # Количество вершин графа
        if n_nodes > 100:                  # Большой граф
            alpha, linewidth = 0.25, 0.2   # Низкая непрозрачность и тонкие линии
        elif n_nodes > 50:                 # Средний граф
            alpha, linewidth = 0.4, 0.3    # Умеренная непрозрачность и средние линии
        elif n_nodes > 20:                 # Небольшой граф
            alpha, linewidth = 0.6, 0.4    # Средняя непрозрачность и средние линии
        else:                              # Маленький граф
            alpha, linewidth = 0.8, 0.5    # Высокая непрозрачность и толстые линии
        
        # Цвета ребер
        use_simple = self.app.settings.get('use_simple_edge_colors', tk.BooleanVar(value=False)).get()  # Проверка настройки упрощенной цветовой схемы
        if use_simple:  # Упрощенная схема (только 2 цвета: все положительные - зеленые, все отрицательные - фиолетовые)
            colors = [self.simple_positive_color if w > 0 else self.simple_negative_color for w in self._cached_edge_weights]
        else:  # Полная градиентная схема. Нормализация веса от -1..1 к 0..1 и получение цвета из шкалы
            colors = [self.edge_cmap_custom((w + 1) / 2) for w in self._cached_edge_weights]

        # Создание коллекции линий с цветами и толщиной
        lc = LineCollection(self._cached_edge_segments, colors=colors, linewidths=linewidth, alpha=alpha, zorder=1)
        self.ax.add_collection(lc)  # Добавление коллекции на оси
    
    def _draw_burning_edges(self, graph, pos):
        """Рисует горящие ребра"""       
        segments = []  # Список сегментов (координат) горящих ребер
        colors = []    # Список цветов для каждого ребра
        unique_iters = sorted(set(self.burned_edges.values()))  # Уникальные итерации загорания (отсортированные)
        # Нормализация итераций загорания в диапазон от 0 до 1 для выбора цвета из градиентной шкалы
        iter_to_norm = {it: i / (len(unique_iters) - 1) if len(unique_iters) > 1 else 0.5 for i, it in enumerate(unique_iters)}
        for (u, v), iteration in self.burned_edges.items():  # Перебор всех горящих ребер
            segments.append([pos[u], pos[v]])  # Добавление координат ребра в список
            colors.append(self.fire_cmap_custom(iter_to_norm[iteration]))  # Получение цвета из шкалы пожара по нормализованной итерации
        lc = LineCollection(segments, colors=colors, alpha=0.9, zorder=2)  # Создание коллекции горящих ребер
        self.ax.add_collection(lc)  # Добавление коллекции на оси
    
    def _draw_all_vertices(self, graph, pos):
        """Рисует все вершины (обычные и горящие)"""
        if not self.show_fire or not self.burned_nodes: # Если пожара нет, все вершины обычные
            self._draw_vertex_group(graph, pos, list(graph.nodes()), self.vertex_color, is_burning=False)
            return
        burned_set = self.burned_nodes  # Прямая ссылка на словарь вершин
        burning_nodes = []              # Список горящих вершин
        normal_nodes = []               # Список обычных вершин
        for node in graph.nodes():
            if node in burned_set:           # Проверка принадлежности к горящим
                burning_nodes.append(node)   # Добавление в список горящих
            else:
                normal_nodes.append(node)    # Добавление в список обычных
        if normal_nodes: # Отрисовка обычных вершин (если есть)
            self._draw_vertex_group(graph, pos, normal_nodes, self.vertex_color, is_burning=False)
        if burning_nodes: # Отрисовка горящих вершин (если есть)
            self._draw_vertex_group(graph, pos, burning_nodes, None, is_burning=True)
    
    def _draw_vertex_group(self, graph, pos, nodes, base_color, is_burning=False):
        """Рисует группу вершин"""      
        sizes = [200 + graph.nodes[node].get('weight', 0.5) * 600 for node in nodes] # Размеры вершин
        # Цвета вершин
        if is_burning:
            unique_iters = sorted(set(self.burned_nodes[n] for n in nodes))
            iter_to_norm = {it: i / (len(unique_iters) - 1) if len(unique_iters) > 1 else 0.5 for i, it in enumerate(unique_iters)}
            colors = [self.fire_cmap_custom(iter_to_norm[self.burned_nodes[node]]) for node in nodes]
        else:
            colors = [base_color] * len(nodes)
        # Отрисовка кружков
        nx.draw_networkx_nodes(graph, pos, nodelist=nodes, node_color=colors, node_size=sizes, edgecolors=self.vertex_border,
                               linewidths=0.5, alpha=0.7, ax=self.ax)
        # Подписи
        for node in nodes:
            x, y = pos[node]
            font_size = 8 + int(graph.nodes[node].get('weight', 0.5) * 4)
            node_num = str(int(node[1:]) + 1)
            self.ax.text(x, y, node_num, fontsize=font_size, fontweight='normal', ha='center', va='center', color=self.text_color)

    def _build_edge_cache(self, graph, pos, show_negative_edges):
        """Строит кэш данных для негорящих ребер"""
        segments = []   # Координаты ребер [[(x1,y1),(x2,y2)], ...]
        weights = []    # Веса ребер [0.5, -0.3, 0.8, ...]
        for u, v, d in graph.edges(data=True): # Пример: ('V0', 'V1', {'weight': 0.7})
            edge_key = tuple(sorted((u, v))) # Уникальный ключ ребра (не зависит от направления)
            if edge_key in self.burned_edges:  # Если ребро в словаре горящих ребер - пропускаем (горящие рисуются отдельно)
                continue
            if not show_negative_edges and d['weight'] <= 0: # Пропускаем отрицательное ребро, если его не надо отображать
                continue   
            segments.append([pos[u], pos[v]]) # Если ребро прошло все фильтры - добавляем его в кэш
            weights.append(d['weight'])       # Сохраняем вес ребра для последующего определения цвета
        # Сохраняем результаты в кэш объекта
        self._cached_edge_segments = segments
        self._cached_edge_weights = weights
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


# In[27]:


class DistributionPlot:
    """График плотности распределений на вкладке генерации"""
    
    def __init__(self, parent, factory, x_range=(-1, 1), color_key='edge_density_color'):
        self.factory = factory                      # Фабрика виджетов
        self.app = factory.app                      # Главное приложение
        self.x_range = x_range                      # Диапазон оси X
        self.tolerance = PARAM_CONFIG['global']['tolerance']  # Точность сравнения
        self.frame = factory.create_frame(parent)   # Родительский фрейм
        self.figure = Figure(figsize=(2.5, 1.5), dpi=80, facecolor=factory.theme.get_color('plot_bg'))
        self.ax = self.figure.add_subplot(111)      # Оси для графика
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)  # Холст tkinter
        self.canvas.get_tk_widget().pack()          # Упаковка холста
        self.color = factory.theme.get_color(color_key)  # Цвет линии из темы
        self.clear()                                # Настройка осей и очистка
    
    def clear(self):
        """Очистка графика и сброс настроек осей"""
        self.ax.clear()                             # Удаление всех элементов
        self._configure_axes()                      # Настройка внешнего вида осей
        self.canvas.draw()                          # Перерисовка холста
    
    def _configure_axes(self):
        """Настройка внешнего вида осей"""
        self.figure.set_facecolor(self.factory.theme.get_color('plot_bg'))  # Фон фигуры
        self.ax.set_facecolor(self.factory.theme.get_color('plot_bg'))      # Фон осей
        self.ax.set_xlim(self.x_range[0], self.x_range[1])                  # Границы оси X
        self.ax.set_ylim(0, 5)                                              # Границы оси Y
        self.ax.set_yticks([])                                              # Скрытие меток оси Y
        self.ax.tick_params(colors=self.factory.theme.get_color('text_color'), labelsize=7)  # Стиль меток
        for spine in self.ax.spines.values():
            spine.set_color(self.factory.theme.get_color('border_color'))  # Цвет границ
    
    def _prepare_plot(self):
        """Подготовка осей к новому графику"""
        self.ax.clear()                                  # Удаление старого графика
        self._configure_axes()                           # Применение настроек
    
    def _normalize_to_range(self, x, y):
        """Нормировка массива Y на диапазон оси X"""
        mask = (x >= self.x_range[0]) & (x <= self.x_range[1])  # Маска в пределах диапазона
        area = np.trapezoid(y[mask], x[mask])                   # Площадь под кривой
        return y / area if area > self.tolerance else y         # Нормировка или исходный массив
    
    def update_uniform(self, min_val, max_val):
        """График плотности равномерного распределения на вкладке Генерации графа"""
        self._prepare_plot()                                    # Подготовка осей
        x = np.linspace(self.x_range[0], self.x_range[1], 400)  # Сетка точек X
        y = np.zeros_like(x)                                    # Массив Y с нулями
        mask = (x >= min_val) & (x <= max_val)                  # Маска внутри границ
        y[mask] = 1 / (max_val - min_val)                       # Постоянная высота
        self.ax.fill_between(x, y, where=mask, alpha=0.3, color=self.color)  # Заливка
        self.ax.plot(x, y, color=self.color, linewidth=1.5)     # Линия
        self.canvas.draw()                                      # Перерисовка
    
    def update_normal(self, mu, sigma):
        """График плотности нормального распределения на вкладке Генерации графа"""
        self._prepare_plot()                                     # Подготовка осей
        x = np.linspace(self.x_range[0], self.x_range[1], 400)   # Сетка точек X
        a = (self.x_range[0] - mu) / sigma                       # Левая граница усечения
        b = (self.x_range[1] - mu) / sigma                       # Правая граница усечения
        y = truncnorm.pdf(x, a, b, loc=mu, scale=sigma)          # Плотность вероятности
        self.ax.fill_between(x, y, alpha=0.3, color=self.color)  # Заливка
        self.ax.plot(x, y, color=self.color, linewidth=1.5)      # Линия
        self.canvas.draw()                                       # Перерисовка
    
    def update_student(self, df, scale):
        """График плотности распределения Стьюдента на вкладке Генерации графа"""
        self._prepare_plot()                                     # Подготовка осей
        x = np.linspace(self.x_range[0], self.x_range[1], 400)   # Сетка точек X
        y = stats_t.pdf(x, df, scale=scale)                      # Плотность вероятности
        y = self._normalize_to_range(x, y)                       # Нормировка на диапазон
        self.ax.fill_between(x, y, alpha=0.3, color=self.color)  # Заливка
        self.ax.plot(x, y, color=self.color, linewidth=1.5)      # Линия
        self.canvas.draw()                                       # Перерисовка
    
    def update_laplace(self, loc, scale):
        """График плотности распределения Лапласа на вкладке Генерации графа"""
        self._prepare_plot()                                     # Подготовка осей
        x = np.linspace(self.x_range[0], self.x_range[1], 400)   # Сетка точек X
        y = laplace.pdf(x, loc=loc, scale=scale)                 # Плотность вероятности
        y = self._normalize_to_range(x, y)                       # Нормировка на диапазон
        self.ax.fill_between(x, y, alpha=0.3, color=self.color)  # Заливка
        self.ax.plot(x, y, color=self.color, linewidth=1.5)      # Линия
        self.canvas.draw()                                       # Перерисовка
    
    def update_bimodal(self, mu1, sigma1, mu2, sigma2, weight):
        """График плотности бимодального распределения на вкладке Генерации графа"""
        self._prepare_plot()                                                 # Подготовка осей
        x = np.linspace(self.x_range[0], self.x_range[1], 400)               # Сетка точек X
        a1 = (self.x_range[0] - mu1) / sigma1                                # Левая граница усечения 1
        b1 = (self.x_range[1] - mu1) / sigma1                                # Правая граница усечения 1
        a2 = (self.x_range[0] - mu2) / sigma2                                # Левая граница усечения 2
        b2 = (self.x_range[1] - mu2) / sigma2                                # Правая граница усечения 2
        y1 = truncnorm.pdf(x, a1, b1, loc=mu1, scale=sigma1) * weight        # Первая компонента
        y2 = truncnorm.pdf(x, a2, b2, loc=mu2, scale=sigma2) * (1 - weight)  # Вторая компонента
        y = y1 + y2                                                          # Сумма компонент
        self.ax.fill_between(x, y, alpha=0.3, color=self.color)              # Заливка
        self.ax.plot(x, y, color=self.color, linewidth=1.5)                  # Линия
        self.canvas.draw()                                                   # Перерисовка
    
    def update_skewed_t(self, df, shape, scale):
        """График плотности скошенного t-распределения на вкладке Генерации графа"""
        self._prepare_plot()                                          # Подготовка осей
        x = np.linspace(self.x_range[0], self.x_range[1], 400)        # Сетка точек X
        samples = nct.rvs(df, shape, scale=scale, size=5000)          # Генерация выборки
        samples = np.clip(samples, self.x_range[0], self.x_range[1])  # Усечение выборки
        kde = gaussian_kde(samples)                                   # Построение KDE
        y = kde(x)                                                    # Оценка плотности
        self.ax.fill_between(x, y, alpha=0.3, color=self.color)       # Заливка
        self.ax.plot(x, y, color=self.color, linewidth=1.5)           # Линия
        self.canvas.draw()                                            # Перерисовка
    
    def update_lognormal(self, gamma, mu, sigma):
        """График плотности логнормального распределения на вкладке Генерации графа"""
        self._prepare_plot()                                              # Подготовка осей
        x = np.linspace(self.x_range[0], self.x_range[1], 400)            # Сетка точек X
        x_shift = np.maximum(x - gamma, self.tolerance)                   # Сдвиг с защитой от нуля
        log_term = np.log(x_shift)                                        # Логарифм сдвинутой переменной
        z = (log_term - mu) / sigma                                       # Стандартизация
        y = np.exp(-0.5 * z**2) / (x_shift * sigma * np.sqrt(2 * np.pi))  # Формула PDF
        y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)             # Замена бесконечностей
        mask = (x >= gamma) & (x <= self.x_range[1])                      # Маска допустимых значений
        area = np.trapezoid(y[mask], x[mask])                             # Площадь под кривой
        if area > self.tolerance:                                         # Проверка ненулевой площади
            y = y / area                                                  # Нормировка
        self.ax.fill_between(x, y, where=mask, alpha=0.3, color=self.color)  # Заливка
        self.ax.plot(x, y, color=self.color, linewidth=1.5)               # Линия
        self.canvas.draw()                                                # Перерисовка
    
    def update_stepwise(self, stages):
        """Отрисовка ступенчатого распределения"""
        if not stages:                                   # Проверка наличия ступеней
            return
        total_weight = sum(s['weight'] for s in stages)  # Суммарный вес ступеней
        self._prepare_plot()                             # Подготовка осей
        palette_key = 'edge_stepwise' if self.x_range == (-1, 1) else 'vertex_stepwise'  # Ключ палитры
        palette = self.factory.theme.get_palette(palette_key)  # Палитра цветов (исправлено)
        max_height = 0                                   # Максимальная высота столбца
        for i, stage in enumerate(stages):               # Обход всех ступеней
            left = max(self.x_range[0], stage['left'])   # Левая граница в пределах диапазона
            right = min(self.x_range[1], stage['right']) # Правая граница в пределах диапазона
            if right <= left + self.tolerance:           # Пропуск некорректных ступеней
                continue
            height = (stage['weight'] / total_weight) * 8  # Высота столбца
            max_height = max(max_height, height)         # Обновление максимума
            color_idx = min(i, len(palette) - 1)         # Индекс цвета с защитой от выхода
            color = palette[color_idx]                   # Цвет из палитры
            self.ax.bar(left, height, width=right-left, align='edge',  # Столбец
                       color=color, alpha=0.7, edgecolor=self.color, linewidth=1)
            self.ax.axvline(left, color=self.color, linestyle='--', alpha=0.5, linewidth=0.8)  # Левая граница
            self.ax.axvline(right, color=self.color, linestyle='--', alpha=0.5, linewidth=0.8)  # Правая граница
        if max_height > 0:                               # Если есть валидные столбцы
            self.ax.set_ylim(0, max_height * 1.3)        # Отступ сверху 30%
        self.canvas.draw()                               # Перерисовка
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


# In[28]:


class HistogramWidget:
    """Виджет гистограммы фактического распределения ребер и вершин"""
    
    def __init__(self, parent, factory, app, title_key, data_type='edge'):
        self.factory = factory                                      # Фабрика виджетов
        self.app = app                                              # Главное приложение
        self.data_type = data_type                                  # Тип данных ('edge' или 'vertex')
        self.title_key = title_key                                  # Ключ перевода заголовка
        self.bins_var = tk.IntVar(value=10)                         # Количество бинов гистограммы
        self._current_data = None                                   # Текущие данные для отображения
        
        self.frame = factory.create_frame(parent)                   # Родительский фрейм
        
        # Заголовок
        self.title_label = factory.create_label(self.frame, title_key, 'small_bold')
        self.title_label.pack(anchor='w', pady=0, padx=22)
        
        # Фигура matplotlib
        self.figure = Figure(figsize=(3.0, 1.0), dpi=70, facecolor=factory.theme.get_color('plot_bg'))
        self.figure.subplots_adjust(bottom=0.2)                     # Отступ снизу для меток
        self.ax = self.figure.add_subplot(111)                      # Оси графика
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(anchor='w', expand=False, fill='none')
        
        if data_type == 'edge': # Настройка цветов и диапазона в зависимости от типа данных
            self.color = factory.theme.get_color('edge_density_color') 
            self.x_range = (-1, 1)      
        else:
            self.color = factory.theme.get_color('vertex_density_color')
            self.x_range = (0, 1)
        self._setup_axes()
        
        controls_frame = factory.create_frame(self.frame) # Фрейм с элементами управления
        controls_frame.pack(pady=(3, 0))
        
        bins_label = factory.create_label(controls_frame, 'num_bins', 'normal') # Метка "Бинов"
        bins_label.pack(side='left', padx=(2, 5))
       
        self.bins_entry = factory.create_entry(controls_frame, variable=self.bins_var, size='tiny',   # Поле ввода количества бинов
                                               param_name='bins_count', dist_type='global', domain='global')
        self.bins_entry.pack(side='left', padx=(0, 5))
        
        # Слайдер количества бинов
        param_config = app.validator.get_param_config('global', 'global', 'bins_count')
        from_val, to_val = param_config['range']
        self.bins_slider = factory.create_scale(controls_frame, variable=self.bins_var, from_=from_val, to_=to_val, size='short')
        self.bins_slider.pack(side='left')
        # Отслеживание изменения количества бинов для перерисовки гистограммы
        self.bins_var.trace_add('write', lambda *args: self._update_histogram())
    
    def _setup_axes(self):
        """Настройка внешнего вида осей"""
        self.figure.set_facecolor(self.factory.theme.get_color('plot_bg'))  # Фон фигуры из темы
        self.ax.set_facecolor(self.factory.theme.get_color('plot_bg'))      # Фон осей из темы
        self.ax.set_xlim(self.x_range[0], self.x_range[1])                  # Границы оси X
        self.ax.set_yticks([])                                              # Скрытие меток оси Y
        self.ax.tick_params(colors=self.factory.theme.get_color('text_color'), labelsize=8)  # Цвет и размер меток
        for spine in self.ax.spines.values():                               # Обход всех границ осей
            spine.set_color(self.factory.theme.get_color('border_color'))   # Цвет границ из темы

    def _update_histogram(self):
        """Перерисовывает гистограмму с текущими данными и количеством бинов"""
        self.ax.clear()                                                 # Очистка осей
        self._setup_axes()                                              # Настройка внешнего вида
        self.ax.hist(self._current_data, bins=self.bins_var.get(), color=self.color, alpha=0.6, density=True,
                     edgecolor=self.factory.theme.get_color('border_color'), range=self.x_range)  # Отрисовка гистограммы
        self.canvas.draw()                                              # Перерисовка холста

    def update(self, data):
        """Обновляет гистограмму с новыми данными"""
        self._current_data = data          # Сохранение новых данных
        self._update_histogram()           # Перерисовка гистограммы
    
    def clear(self):
        """Очищает гистограмму"""
        self._current_data = None          # Сброс данных
        self.ax.clear()                    # Очистка осей
        self._setup_axes()                 # Восстановление внешнего вида
        self.canvas.draw()                 # Перерисовка холста
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


# In[29]:


class StepwiseWidget:
    """Виджеты карточек для ступенчатых распределений"""

    def __init__(self, parent, app, tier_type, tier_manager, plot, on_change_callback=None):
        self.app = app                                        # Главное приложение
        self.tier_type = tier_type                            # Тип ступеней ('edge' или 'vertex')
        self.tier_manager = tier_manager                      # Менеджер ступенчатых распределений
        self.plot = plot                                      # Виджет графика плотности
        self.on_change_callback = on_change_callback          # Функция обратного вызова при изменении данных
        self.validator = app.validator                        # Валидатор значений (для синхронизации границ)
        self.max_stages = app.config['global']['max_stages']  # Максимальное количество ступеней

        # Основной контейнер
        self.frame = app.widget_factory.create_frame(parent)  # Родительский фрейм для всего виджета
        self.frame.grid_rowconfigure(1, weight=1)             # Растяжение строки с карточками (индекс 1)
        self.frame.grid_columnconfigure(0, weight=1)          # Пустое место справа от карточек
    
        self._create_preset_row(app)                          # Строка с пресетами

        # Контейнер для карточек (3 колонки)
        self.cards_container = app.widget_factory.create_frame(self.frame)  # Фрейм для сетки карточек
        self.cards_container.grid(row=1, column=0, sticky='nsew')           # Размещение с растяжением во все стороны
        for i in range(3):                                                  # Создание 3 колонок
            self.cards_container.columnconfigure(i, weight=1, uniform='card_col')  # Равномерная ширина колонок

        # Хранилище данных карточек
        self.cards = []  # Список словарей с данными каждой карточки: {'frame': frame, 'vars_': {...}, 'delete_btn': btn}
        # Создание все возможных карточек
        for i in range(self.max_stages):
            self.cards.append(self._create_stage_card(i))
        # Карточка добавления
        self.add_card = self._create_add_card()
        self._update_ui()  # Обновление отображения (показ/скрытие карточек)

    def _create_preset_row(self, app):
        """Создает строку с кнопками пресетов"""
        if self.tier_type == 'edge': # Выбор списка пресетов в зависимости от типа распределения
            presets = ['uniform_preset', 'social', 'economic', 'information', 'hierarchical', 'ecosystem', 'infrastructure', 'epidemic']
        else:
            presets = ['uniform_preset', 'market', 'oligopoly', 'pyramid', 'exponential']

        # Создание фрейма для строки с кнопками пресетов
        row = app.widget_factory.create_frame(self.frame, height=app.size_config['container']['preset_row']['height'])
        row.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        row.grid_propagate(False)
        
        app.widget_factory.create_label(row, 'presets', 'normal').pack(side='left', padx=(0, 10)) # Создание заголовка "Шаблоны"
        for preset in presets: # Создание кнопок для каждого пресета
            btn = app.widget_factory.create_button(row, preset, lambda p=preset: self.apply_preset(p), 'preset')
            btn.pack(side='left', padx=2)

    def _create_stage_card(self, index):
        """Создает карточку ступени"""
        card = self.app.widget_factory.create_frame(self.cards_container, highlightthickness=1, 
                      highlightbackground=self.app.theme_manager.get_color('border_color')) # Контейнер для карточек
        card.config(width=self.app.size_config['container']['stepwise_card']['width'],
                    height=self.app.size_config['container']['stepwise_card']['min_height']) # Длина и ширина контейнера
        card.grid_propagate(False)
        
        header = self.app.widget_factory.create_frame(card) # Фрейм для заголовка карточки
        header.pack(fill='x', padx=5, pady=(5, 0))
        title = self.app.widget_factory.create_label(header, 'stage', 'card_header') # Текст "Ступень N"
        title.pack(side='left')
        delete_btn = self.app.widget_factory.create_icon_button(header, lambda: self.delete_stage(index), 'delete') # Кнопка удаления
        delete_btn.pack(side='right', padx=(0, 14))
        section = AlignedSection(card, self.app.widget_factory, self.app, None) # Контент карточки (слайдеры и поля ввода)
        section.frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Переменные для хранения значений ступени
        vars_ = {
            'left': tk.DoubleVar(value=0.0),    # Левая граница
            'right': tk.DoubleVar(value=1.0),   # Правая граница
            'weight': tk.IntVar(value=20)       # Количество элементов в ступени
        }
        
        # Привязка обработчики
        for var in vars_.values():
            var.trace_add('write', lambda *args: self._on_data_changed())
        
        # Элементы управления
        section.add_dual_row(top_label='left_bound', bottom_label='right_bound', top_var=vars_['left'], bottom_var=vars_['right'],
                        top_param='left', bottom_param='right', dist_type='Stepwise', domain=self.tier_type) # Два слайдера границ
        section.add_row(label_key='elements_count_stage', variable=vars_['weight'], param_name='weight', dist_type='Stepwise', 
                        domain=self.tier_type, show_label=True, show_entry=False, scale_size='normal_no_entry') # Слайдер веса ступени
        card.grid(row=index // 3, column=index % 3, sticky='nsew', padx=5, pady=5) # Размещение карточки в сетке (3 колонки)
        return {'frame': card, 'vars_': vars_, 'delete_btn': delete_btn, 'title': title}

    def _create_add_card(self):
        """Создает карточку добавления"""
        card = self.app.widget_factory.create_frame(self.cards_container, highlightthickness=1,
                    highlightbackground=self.app.theme_manager.get_color('border_color'))
        card.config(width=self.app.size_config['container']['stepwise_card']['width'],
                   height=self.app.size_config['container']['stepwise_card']['min_height'])
        card.grid_propagate(False)
        btn = self.app.widget_factory.create_icon_button(card, self.add_stage, 'add')
        btn.pack(fill='both', expand=True)
        card.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        return card

    def _get_stages(self):
        """Возвращает текущие ступени из менеджера"""
        return self.tier_manager.get_edge_config() if self.tier_type == 'edge' else self.tier_manager.get_vertex_config()

    def _set_stages(self, stages):
        """Сохраняет ступени в менеджер"""
        if self.tier_type == 'edge':
            self.tier_manager.set_edge_stages(stages)
        else:
            self.tier_manager.set_vertex_stages(stages)

    def _on_data_changed(self):
        """Обработчик изменения данных"""
        stages = []
        # Сбор текущих значений из видимых карточек
        for i in range(len(self._get_stages())):
            vars_ = self.cards[i]['vars_']
            stages.append({'left': vars_['left'].get(), 'right': vars_['right'].get(), 'weight': vars_['weight'].get()})
        # Валидация и сохранение
        stages = self.validator.validate_stages(stages, self.tier_type)
        self._set_stages(stages)
        # Обновление графика
        self.plot.update_stepwise(stages)

    def _update_ui(self):
        """Обновляет отображение карточек"""
        stages = self._get_stages()                         # Текущий список ступеней из менеджера
        n = len(stages)                                     # Количество активных ступеней
        
        for i, card_data in enumerate(self.cards):          # Перебор всех созданных карточек (0..max_stages-1)
            if i < n:                                       # Если карточка должна быть видимой (индекс меньше количества ступеней)
                card_data['frame'].grid()                   # Показать карточку
                card_data['vars_']['left'].set(stages[i]['left'])     # Левая граница из данных ступени
                card_data['vars_']['right'].set(stages[i]['right'])   # Правая граница из данных ступени
                card_data['vars_']['weight'].set(stages[i]['weight']) # Вес из данных ступени
                card_data['title'].config(text=f"{self.app.translator.t('stage')} {i+1}")  # Заголовок "Ступень N"
                
                if n > 2: # Кнопка удаления видна только если ступеней больше 2
                    card_data['delete_btn'].pack(side='right', padx=(0, 14))  # Показать кнопку удаления
                else:                                       # Если ступеней 2 или меньше
                    card_data['delete_btn'].pack_forget()   # Скрыть кнопку удаления
            else:                                           # Если карточка не должна быть видимой
                card_data['frame'].grid_remove()            # Скрыть карточку
        
        # Карточка добавления
        if n < self.max_stages:                             # Если активных ступеней меньше максимально допустимого (6)
            self.add_card.grid(row=n // 3, column=n % 3, sticky='nsew', padx=5, pady=5)
        else:                                               # Если достигнут максимум ступеней
            self.add_card.grid_remove()                     # Скрыть кнопку добавления

    def add_stage(self):
        """Добавляет новую ступень"""
        stages = self._get_stages()
        if self.tier_type == 'edge': # Выбор словаря пресетов в зависимости от типа
            presets_dict = EDGE_TIER_PRESETS
        else:
            presets_dict = VERTEX_TIER_PRESETS
        
        preset_data = presets_dict['uniform_preset'][len(stages) + 1] # Добавляется новая ступень из равномерного пресета
        left, right = preset_data['bounds'][-1]                       # Левая и правая границы последней ступени
        weight = preset_data['counts'][-1]                            # Вес последней ступени
        
        new_stage = {'left': left, 'right': right, 'weight': weight}    # Создание словаря новой ступени
        stages.append(new_stage)                                        # Добавление ступени в список
        self._set_stages(stages)                                        # Сохранение обновленного списка в менеджере
        self._update_ui()                                               # Обновление интерфейса

    def delete_stage(self, index):
        """Удаляет ступень"""
        stages = self._get_stages()          # Получение списка ступеней из менеджера
        del stages[index]                    # Удаление ступени по индексу
        self._set_stages(stages)             # Сохранение обновленного списка в менеджере
        self._update_ui()                    # Обновление интерфейса

    def apply_preset(self, preset_name):
        """Применяет выбранный пресет для заданного количества ступеней"""
        if self.tier_type == 'edge': # Выбор словаря пресетов в зависимости от типа
            presets_dict = EDGE_TIER_PRESETS 
        else: 
            presets_dict = VERTEX_TIER_PRESETS
        
        # Получение данных пресета для текущего количества ступеней
        preset_data = presets_dict.get(preset_name, {}).get(len(self._get_stages()))
         # Создание списка ступеней из пресета
        new_stages = [{'left': l, 'right': r, 'weight': w} for (l, r), w in zip(preset_data['bounds'], preset_data['counts'])]
        self._set_stages(new_stages)
        self._update_ui()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)


# In[30]:


class VirtualVertexTable:
    """Виртуальная таблица для редактирования весов вершин"""
    
    def __init__(self, parent, factory, app):
        """Инициализация виртуальной таблицы вершин"""
        self.factory = factory  # Фабрика виджетов
        self.app = app  # Ссылка на главное приложение
        self.data = None  # Данные графа
        self.change_callbacks = []  # Список колбэков при изменении данных
        cfg = app.size_config['virtual_table']  # Конфигурация размеров
        self.cell_w, self.cell_h = cfg['cell_width'], cfg['cell_height']  # Ширина и высота ячейки
        self.container = factory.create_frame(parent)  # Контейнер таблицы
        self.container.grid_rowconfigure(1, weight=1)  # Растяжение строки с ячейками
        self.container.grid_columnconfigure(1, weight=1)  # Растяжение колонки с таблицей
        self.headers = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), highlightthickness=0, height=self.cell_h)  # Холст заголовков
        self.headers.grid(row=0, column=1, sticky='ew')  # Размещение заголовков
        self.cell_canvas = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), highlightthickness=0)  # Холст для ячеек
        self.cell_canvas.grid(row=1, column=1, sticky='nsew')  # Размещение с растяжением
        self.scrollbar = factory.create_scrollbar(self.container, orient='horizontal', command=self._on_scroll)  # Горизонтальный скроллбар
        self.scrollbar.grid(row=2, column=1, sticky='ew')  # Размещение скроллбара
        self.cell_canvas.configure(xscrollcommand=self.scrollbar.set)  # Привязка к холсту
        add_frame = factory.create_frame(self.container, width=self.cell_w, height=2*self.cell_h)  # Фрейм для кнопки добавления
        add_frame.grid(row=1, column=2, sticky='ns', padx=(5,0), pady=(0,5))  # Размещение справа
        add_frame.grid_propagate(False)  # Запрет изменения размера
        factory.create_icon_button(add_frame, self._add_vertex, 'add').pack(fill='both', expand=True)  # Кнопка добавления
        self.cell_canvas.bind('<Button-1>', self._on_click)  # Клик по ячейке
        self.cell_canvas.bind('<Configure>', lambda e: self.redraw())  # Перерисовка при изменении размера
        self.active_edit = None  # Активный редактор (None если закрыт)
    
    def _on_scroll(self, *args):
        """Обработка горизонтальной прокрутки"""
        self.cell_canvas.xview(*args)  # Прокрутка области ячеек
        self.headers.xview(*args)  # Синхронная прокрутка заголовков
        self.redraw()  # Перерисовка видимой области
    
    def redraw(self):
        """Полная перерисовка таблицы с учетом видимой области"""
        self.headers.delete('all')  # Очистка заголовков
        self.cell_canvas.delete('all')  # Очистка ячеек
        n = self.data.graph.number_of_nodes()  # Количество вершин
        if n == 0:  # Пустой граф
            self.cell_canvas.configure(scrollregion=(0,0,0,0))  # Сброс области прокрутки
            return
        total_w = n * self.cell_w  # Общая ширина таблицы
        self.cell_canvas.configure(scrollregion=(0, 0, total_w, self.cell_h * 2))  # Область прокрутки ячеек
        self.headers.configure(scrollregion=(0, 0, total_w, self.cell_h))  # Область прокрутки заголовков
        x1, x2 = self.cell_canvas.xview()  # Видимая область по горизонтали
        start = max(0, int(x1 * total_w / self.cell_w))  # Первая видимая колонка
        end = min(n, int(x2 * total_w / self.cell_w) + 2)  # Последняя видимая колонка
        rounding = self.app.settings['rounding_input'].get()  # Точность округления из настроек
        for col in range(start, end):  # Перебор видимых колонок
            x = col * self.cell_w  # X-координата ячейки
            weight = self.data.get_vertex(col)  # Вес вершины

            self.headers.create_text(x + self.cell_w//2, self.cell_h//2, text=f'V{col+1}', font=self.factory.get_font('table_header'), 
                                     fill=self.factory.theme.get_color('text_color'))  # Заголовок V#
            self.cell_canvas.create_rectangle(x, 0, x+self.cell_w, self.cell_h, fill=self.factory.theme.get_color('bg_color'), 
                                              outline=self.factory.theme.get_color('border_color'))  # Фон ячейки
            self.cell_canvas.create_text(x + self.cell_w//2, self.cell_h//2, text=f"{weight:.{rounding}f}", font=self.factory.get_font('table_cell'), 
                                         fill=self.factory.theme.get_color('text_color'), tags=(f'value_{col}',))  # Значение веса
            btn = self.factory.create_icon_button(self.cell_canvas, lambda c=col: self._delete_vertex(c), 'delete')  # Кнопка удаления
            self.cell_canvas.create_window(x + 2, self.cell_h + 2, window=btn, anchor='nw', 
                                           width=self.cell_w-4, height=self.cell_h-4)  # Размещение кнопки в ячейке
    
    def _delete_vertex(self, col):
        """Удаление вершины по индексу"""
        self._cancel_edit()  # Закрытие редактора
        self.data.remove_vertex(col)  # Удаление вершины из данных
        self.redraw()  # Перерисовка таблицы
        for cb in self.change_callbacks:  # Уведомление подписчиков
            cb('delete', col, None)
    
    def _add_vertex(self):
        """Добавление новой вершины в конец таблицы"""
        weight = self.app.settings['default_vertex_weight'].get()  # Вес новой вершины из настроек
        new_index = self.data.add_vertex(weight=weight)  # Добавление вершины в данные
        n = self.data.graph.number_of_nodes()  # Новое количество вершин
        default_edge = self.app.settings['default_edge_weight'].get()  # Вес ребра по умолчанию
        for i in range(n - 1):  # Перебор всех существующих вершин
            self.data.update_edge(i, n - 1, default_edge)  # Добавление ребер к новой вершине
        self.redraw()  # Перерисовка таблицы
        self.cell_canvas.xview_moveto(1.0)  # Прокрутка в конец таблицы
        self.headers.xview_moveto(1.0)  # Синхронная прокрутка заголовков
        for cb in self.change_callbacks:  # Уведомление подписчиков
            cb('add', new_index, weight)
    
    def _on_click(self, event):
        """Обработчик клика по ячейке"""
        if self.active_edit:  # Если есть активный редактор
            self._cancel_edit()  # Закрытие без сохранения
            return
        x = self.cell_canvas.canvasx(event.x)  # X-координата в canvas
        col = int(x // self.cell_w)  # Номер колонки
        if 0 <= col < self.data.graph.number_of_nodes() and event.y <= self.cell_h:  # Проверка границ
            self._start_edit(col)  # Начало редактирования ячейки
    
    def _start_edit(self, col):
        """Начало редактирования ячейки"""
        current = self.data.get_vertex(col)  # Текущее значение веса
        entry, param_config = self.factory.create_table_entry(parent=self.cell_canvas, variable=tk.DoubleVar(value=current), param_name='weight', 
                                                              domain='vertex_card', dist_type='vertex_card', size='default')  # Поле ввода
        win_id = self.cell_canvas.create_window(col * self.cell_w, 0, window=entry, anchor='nw', width=self.cell_w, height=self.cell_h)  # Редактор
        self.active_edit = (col, entry, win_id, current, param_config)  # Сохранение контекста
        entry.focus_set()  # Фокус на поле ввода
        
        def commit():
            """Сохранение отредактированного значения"""
            if self.active_edit:
                col, entry, win_id, old, param_config = self.active_edit  # Распаковка контекста
                try:
                    new = float(entry.get())  # Преобразование в число
                except (ValueError, TypeError):
                    new = old  # При ошибке оставляем старое
                rounding = self.app.settings['rounding_input'].get()  # Точность округления
                new = self.app.validator.validate_and_correct(new, param_config, rounding, old)  # Валидация
                if abs(new - old) > self.app.validator.tolerance:  # Значение изменилось
                    self.data.update_vertex(col, new)  # Обновление данных
                    items = self.cell_canvas.find_withtag(f'value_{col}')  # Поиск текста ячейки
                    if items:
                        self.cell_canvas.itemconfig(items[0], text=f"{new:.{rounding}f}")  # Обновление отображения
                    for cb in self.change_callbacks:  # Уведомление подписчиков
                        cb('change', col, new)
                self._cancel_edit()  # Закрытие редактора
        entry.bind('<Return>', lambda e: commit())  # Enter - сохранение
        entry.bind('<Escape>', lambda e: self._cancel_edit())  # Escape - отмена
        entry.bind('<FocusOut>', lambda e: self.cell_canvas.after(50, commit))  # Потеря фокуса - сохранение
    
    def _cancel_edit(self):
        """Отмена редактирования и закрытие редактора"""
        try:
            self.active_edit[1].destroy()  # Уничтожение поля ввода
            self.cell_canvas.delete(self.active_edit[2])  # Удаление окна с canvas
        except:
            pass
        self.active_edit = None  # Сброс контекста
    
    def set_graph_data(self, data):
        """Установка данных графа для отображения"""
        self._cancel_edit()  # Закрытие редактора
        self.data = data  # Сохранение данных
        self.cell_canvas.xview_moveto(0)  # Сброс прокрутки в начало
        self.headers.xview_moveto(0)  # Синхронный сброс заголовков
        self.redraw()  # Перерисовка таблицы
    
    def on_change(self, callback):
        """Добавление обработчика изменений данных"""
        self.change_callbacks.append(callback)  # Добавление колбэка в список
    
    def pack(self, **kwargs):
        """Упаковка контейнера в родительский виджет"""
        self.container.pack(**kwargs)  # Передача параметров упаковки
    
    def grid(self, **kwargs):
        """Размещение контейнера в сетке"""
        self.container.grid(**kwargs)  # Передача параметров сетки


# In[31]:


class VirtualEdgeTable:
    """Виртуальная таблица для редактирования весов ребер"""
    
    def __init__(self, parent, factory, app):
        """Инициализация виртуальной таблицы ребер"""
        self.factory = factory  # Фабрика виджетов
        self.app = app  # Ссылка на главное приложение
        self.data = None  # Данные графа
        self.change_callbacks = []  # Список колбэков при изменении данных
        cfg = app.size_config['virtual_table']  # Конфигурация размеров
        self.cell_w, self.cell_h = cfg['cell_width'], cfg['cell_height']  # Ширина и высота ячейки
        self.container = factory.create_frame(parent)  # Контейнер таблицы
        self.container.grid_rowconfigure(1, weight=1)  # Растяжение строки с ячейками
        self.container.grid_columnconfigure(1, weight=1)  # Растяжение колонки с таблицей
        self.corner = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), 
                                highlightthickness=0, width=self.cell_w, height=self.cell_h)  # Угловой элемент
        self.corner.grid(row=0, column=0, sticky='nsew')  # Размещение угла
        self.top_header = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), 
                                    highlightthickness=0, height=self.cell_h)  # Холст для верхних заголовков
        self.top_header.grid(row=0, column=1, sticky='ew')  # Размещение
        self.left_header = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), 
                                     highlightthickness=0, width=self.cell_w)  # Холст для левых заголовков
        self.left_header.grid(row=1, column=0, sticky='ns')  # Размещение
        self.cell_canvas = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), highlightthickness=0)  # Холст для ячеек
        self.cell_canvas.grid(row=1, column=1, sticky='nsew')  # Размещение с растяжением
        self.h_scrollbar = factory.create_scrollbar(self.container, orient='horizontal', command=self._on_h_scroll)  # Горизонтальный скроллбар
        self.v_scrollbar = factory.create_scrollbar(self.container, orient='vertical', command=self._on_v_scroll)  # Вертикальный скроллбар
        self.h_scrollbar.grid(row=2, column=1, sticky='ew')  # Размещение горизонтального
        self.v_scrollbar.grid(row=1, column=2, sticky='ns')  # Размещение вертикального
        self.cell_canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)  # Привязка скроллбаров
        self.cell_canvas.bind('<Button-1>', self._on_click)  # Клик по ячейке
        self.cell_canvas.bind('<Configure>', lambda e: self.redraw())  # Перерисовка при изменении размера
        self.active_edit = None  # Активный редактор
        self._pending_commit = False  # Флаг блокировки повторных сохранений
    
    def _on_h_scroll(self, *args):
        """Обработка горизонтальной прокрутки"""
        self.cell_canvas.xview(*args)  # Прокрутка области ячеек по горизонтали
        self.top_header.xview(*args)  # Синхронная прокрутка верхних заголовков
        self.redraw()  # Перерисовка видимой области
    
    def _on_v_scroll(self, *args):
        """Обработка вертикальной прокрутки"""
        self.cell_canvas.yview(*args)  # Прокрутка области ячеек по вертикали
        self.left_header.yview(*args)  # Синхронная прокрутка левых заголовков
        self.redraw()  # Перерисовка видимой области
    
    def redraw(self):
        """Полная перерисовка таблицы с учетом видимой области"""
        self.top_header.delete('all')  # Очистка верхних заголовков
        self.left_header.delete('all')  # Очистка левых заголовков
        self.cell_canvas.delete('all')  # Очистка ячеек
        n = self.data.graph.number_of_nodes()  # Количество вершин
        if n == 0:  # Пустой граф
            self.cell_canvas.configure(scrollregion=(0,0,0,0))  # Сброс области прокрутки
            return
        total_w, total_h = n * self.cell_w, n * self.cell_h  # Общая ширина и высота таблицы
        self.cell_canvas.configure(scrollregion=(0, 0, total_w, total_h))  # Область прокрутки ячеек
        self.top_header.configure(scrollregion=(0, 0, total_w, self.cell_h))  # Область прокрутки верхних заголовков
        self.left_header.configure(scrollregion=(0, 0, self.cell_w, total_h))  # Область прокрутки левых заголовков
        
        x1, x2 = self.cell_canvas.xview()  # Видимая область по горизонтали
        y1, y2 = self.cell_canvas.yview()  # Видимая область по вертикали
        start_col = max(0, int(x1 * total_w / self.cell_w))  # Первая видимая колонка
        end_col = min(n, int(x2 * total_w / self.cell_w) + 2)  # Последняя видимая колонка
        start_row = max(0, int(y1 * total_h / self.cell_h))  # Первая видимая строка
        end_row = min(n, int(y2 * total_h / self.cell_h) + 2)  # Последняя видимая строка
        rounding = self.app.settings['rounding_input'].get()  # Точность округления из настроек
        
        for col in range(start_col, end_col):  # Отрисовка верхних заголовков
            self.top_header.create_text(col * self.cell_w + self.cell_w//2, self.cell_h//2, text=f'V{col+1}', 
                                        font=self.factory.get_font('table_header'), fill=self.factory.theme.get_color('text_color'))
        for row in range(start_row, end_row):  # Отрисовка левых заголовков
            self.left_header.create_text(self.cell_w//2, row * self.cell_h + self.cell_h//2, text=f'V{row+1}', 
                                         font=self.factory.get_font('table_header'), fill=self.factory.theme.get_color('text_color'))
        
        for row in range(start_row, end_row):  # Перебор видимых строк
            for col in range(start_col, end_col):  # Перебор видимых колонок
                x, y = col * self.cell_w, row * self.cell_h  # Координаты ячейки
                if row == col:  # Диагональные ячейки
                    self.cell_canvas.create_rectangle(x, y, x+self.cell_w, y+self.cell_h, fill=self.factory.theme.get_color('input_bg'),
                                                      outline=self.factory.theme.get_color('border_color'))
                    self.cell_canvas.create_text(x + self.cell_w//2, y + self.cell_h//2, text='—', font=self.factory.get_font('table_cell'),
                                                 fill=self.factory.theme.get_color('text_color'))
                    
                elif row > col:  # Нижний треугольник (только отображение)
                    value = self.data.get_edge_weight(col, row)  # Вес ребра (симметричный доступ)
                    self.cell_canvas.create_rectangle(x, y, x+self.cell_w, y+self.cell_h, fill=self.factory.theme.get_color('input_bg'),
                                                      outline=self.factory.theme.get_color('border_color'), tags=(f'lower_cell_{row}_{col}',))
                    self.cell_canvas.create_text(x + self.cell_w//2, y + self.cell_h//2, text=f"{value:.{rounding}f}", 
                                                 font=self.factory.get_font('table_cell'), fill=self.factory.theme.get_color('text_color'),
                                                 tags=(f'lower_value_{row}_{col}',))
                    
                else:  # Верхний треугольник (редактируемый)
                    value = self.data.get_edge_weight(row, col)  # Вес ребра
                    self.cell_canvas.create_rectangle(x, y, x+self.cell_w, y+self.cell_h, fill=self.factory.theme.get_color('bg_color'),
                                                      outline=self.factory.theme.get_color('border_color'), tags=(f'cell_{row}_{col}',))
                    self.cell_canvas.create_text(x + self.cell_w//2, y + self.cell_h//2, text=f"{value:.{rounding}f}",
                                                 font=self.factory.get_font('table_cell'), fill=self.factory.theme.get_color('text_color'),
                                                 tags=(f'value_{row}_{col}',))
    
    def _get_cell_at(self, x, y):
        """Определение координат ячейки по клику (только верхний треугольник)"""
        cx, cy = self.cell_canvas.canvasx(x), self.cell_canvas.canvasy(y)  # Преобразование координат
        col, row = int(cx // self.cell_w), int(cy // self.cell_h)  # Номер колонки и строки
        n = self.data.graph.number_of_nodes()  # Количество вершин
        return (row, col) if 0 <= row < n and 0 <= col < n and row < col else None  # Только верхний треугольник
    
    def _on_click(self, event):
        """Обработчик клика по ячейке"""
        if self.active_edit:  # Если есть активный редактор
            self._cancel_edit()  # Закрытие без сохранения
            return
        cell = self._get_cell_at(event.x, event.y)  # Определение ячейки
        if cell:  # Клик по редактируемой ячейке
            self._start_edit(*cell)  # Начало редактирования
    
    def _start_edit(self, row, col):
        """Начало редактирования ячейки"""
        current = self.data.get_edge_weight(row, col)  # Текущее значение веса ребра
        entry, param_config = self.factory.create_table_entry(parent=self.cell_canvas, variable=tk.DoubleVar(value=current), param_name='weight', 
                                                              domain='edge_card', dist_type='edge_card', size='default')  # Поле ввода
        
        win_id = self.cell_canvas.create_window(col * self.cell_w, row * self.cell_h, window=entry, anchor='nw',
                                                width=self.cell_w, height=self.cell_h)  # Размещение редактора
        self.active_edit = (row, col, entry, win_id, current, param_config)  # Сохранение контекста
        entry.focus_set()  # Фокус на поле ввода
        
        def commit():
            """Сохранение отредактированного значения"""
            if self.active_edit and not self._pending_commit:
                self._pending_commit = True  # Блокировка повторных вызовов
                try:
                    row, col, entry, win_id, old, param_config = self.active_edit  # Распаковка контекста
                    try:
                        new = float(entry.get())  # Преобразование в число
                    except (ValueError, TypeError):
                        new = old  # При ошибке оставляем старое
                    rounding = self.app.settings['rounding_input'].get()  # Точность округления
                    new = self.app.validator.validate_and_correct(new, param_config, rounding, old)  # Валидация
                    if abs(new - old) > self.app.validator.tolerance:  # Значение изменилось
                        self.data.update_edge(row, col, new)  # Обновление данных
                        formatted = f"{new:.{rounding}f}"  # Форматирование для отображения
                        items = self.cell_canvas.find_withtag(f'value_{row}_{col}')  # Поиск текста верхней ячейки
                        if items:
                            self.cell_canvas.itemconfig(items[0], text=formatted)  # Обновление отображения
                        lower_items = self.cell_canvas.find_withtag(f'lower_value_{col}_{row}')  # Поиск текста нижней ячейки
                        if lower_items:
                            self.cell_canvas.itemconfig(lower_items[0], text=formatted)  # Обновление отображения
                        for cb in self.change_callbacks:  # Уведомление подписчиков
                            cb(row, col, new)
                finally:
                    self._cancel_edit()  # Закрытие редактора
                    self._pending_commit = False  # Сброс блокировки
        
        entry.bind('<Return>', lambda e: commit())  # Enter - сохранение
        entry.bind('<Escape>', lambda e: self._cancel_edit())  # Escape - отмена
        entry.bind('<FocusOut>', lambda e: self.cell_canvas.after(50, commit))  # Потеря фокуса - сохранение
    
    def _cancel_edit(self):
        """Отмена редактирования и закрытие редактора"""
        try:
            self.active_edit[2].destroy()  # Уничтожение поля ввода
            self.cell_canvas.delete(self.active_edit[3])  # Удаление окна с canvas
        except:
            pass
        self.active_edit = None  # Сброс контекста
    
    def set_graph_data(self, data):
        """Установка данных графа для отображения"""
        self._cancel_edit()  # Закрытие редактора
        self.data = data  # Сохранение данных
        self.cell_canvas.xview_moveto(0)  # Сброс горизонтальной прокрутки
        self.cell_canvas.yview_moveto(0)  # Сброс вертикальной прокрутки
        self.top_header.xview_moveto(0)  # Синхронный сброс верхних заголовков
        self.left_header.yview_moveto(0)  # Синхронный сброс левых заголовков
        self.redraw()  # Перерисовка таблицы
    
    def on_change(self, callback):
        """Добавление обработчика изменений данных"""
        self.change_callbacks.append(callback)  # Добавление колбэка в список
    
    def pack(self, **kwargs):
        """Упаковка контейнера в родительский виджет"""
        self.container.pack(**kwargs)  # Передача параметров упаковки
    
    def grid(self, **kwargs):
        """Размещение контейнера в сетке"""
        self.container.grid(**kwargs)  # Передача параметров сетки


# In[32]:


class StartVerticesTable:
    """Таблица для ввода номеров стартовых вершин"""
    
    def __init__(self, parent, factory, app):
        """Инициализация таблицы стартовых вершин"""
        self.factory = factory  # Фабрика виджетов
        self.app = app  # Ссылка на главное приложение
        cfg = app.size_config['virtual_table']  # Конфигурация размеров
        self.cell_w, self.cell_h = cfg['cell_width'], cfg['cell_height']  # Ширина и высота ячейки
        self.count = 0  # Количество ячеек в таблице
        self.max_vertex = 20  # Максимальный номер вершины (по умолчанию)
        self.active_edit = None  # Активный редактор
        self._editable = True  # Флаг редактируемости
        self.cell_vars = []  # Список переменных для ячеек
        self._pending_commit = False  # Флаг блокировки повторных сохранений
        self.container = factory.create_frame(parent)  # Контейнер таблицы
        self.container.grid_rowconfigure(1, weight=1)  # Растяжение строки с ячейками
        self.container.grid_columnconfigure(0, weight=1)  # Растяжение колонки
        self.headers = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), highlightthickness=0, height=self.cell_h)  # Холст заголовков
        self.headers.grid(row=0, column=0, sticky='ew')  # Размещение заголовков
        self.cell_canvas = tk.Canvas(self.container, bg=factory.theme.get_color('bg_color'), highlightthickness=0)  # Холст для ячеек
        self.cell_canvas.grid(row=1, column=0, sticky='nsew')  # Размещение с растяжением
        self.scrollbar = factory.create_scrollbar(self.container, orient='horizontal', command=self._on_scroll)  # Горизонтальный скроллбар
        self.scrollbar.grid(row=2, column=0, sticky='ew')  # Размещение скроллбара
        self.cell_canvas.configure(xscrollcommand=self.scrollbar.set)  # Привязка к холсту
        self.cell_canvas.bind('<Button-1>', self._on_click)  # Клик по ячейке
        self.cell_canvas.bind('<Configure>', lambda e: self.redraw())  # Перерисовка при изменении размера
    
    def _on_scroll(self, *args):
        """Обработка горизонтальной прокрутки"""
        self.cell_canvas.xview(*args)  # Прокрутка области ячеек
        self.headers.xview(*args)  # Синхронная прокрутка заголовков
        self.redraw()  # Перерисовка видимой области
    
    def redraw(self):
        """Полная перерисовка таблицы с учетом видимой области"""
        self.headers.delete('all')  # Очистка заголовков
        self.cell_canvas.delete('all')  # Очистка ячеек
        total_w = self.count * self.cell_w  # Общая ширина таблицы
        self.cell_canvas.configure(scrollregion=(0, 0, total_w, self.cell_h))  # Область прокрутки ячеек
        self.headers.configure(scrollregion=(0, 0, total_w, self.cell_h))  # Область прокрутки заголовков
        x1, x2 = self.cell_canvas.xview()  # Видимая область по горизонтали
        start = max(0, int(x1 * total_w / self.cell_w))  # Первая видимая колонка
        end = min(self.count, int(x2 * total_w / self.cell_w) + 2)  # Последняя видимая колонка
        for col in range(start, end):  # Отрисовка заголовков
            self.headers.create_text(col * self.cell_w + self.cell_w//2, self.cell_h//2, text='V #', font=self.factory.get_font('table_header'), 
                                     fill=self.factory.theme.get_color('text_color'))
        
        for col in range(start, end):  # Отрисовка ячеек
            x = col * self.cell_w  # X-координата ячейки
            value = self._get_value(col)  # Значение из переменной
            self.cell_canvas.create_rectangle(x, 0, x+self.cell_w, self.cell_h, fill=self.factory.theme.get_color('bg_color'), 
                                              outline=self.factory.theme.get_color('border_color'), tags=(f'cell_{col}',))
            self.cell_canvas.create_text(x + self.cell_w//2, self.cell_h//2, text=str(value), font=self.factory.get_font('table_cell'), 
                                         fill=self.factory.theme.get_color('text_color'), tags=(f'value_{col}',))
    
    def _get_value(self, col):
        """Получение значения из переменной по индексу колонки"""
        try:
            return int(self.cell_vars[col].get())  # Преобразование в целое число
        except ValueError:
            return 1  # Значение по умолчанию при ошибке
    
    def _validate_value(self, value):
        """Валидация номера вершины (диапазон 1..max_vertex)"""
        try:
            val = int(value)  # Преобразование в целое число
        except (ValueError, TypeError):
            return 1  # При ошибке возвращаем минимальное значение
        if val < 1:  # Нижняя граница
            return 1
        if val > self.max_vertex:  # Верхняя граница
            return self.max_vertex
        return val  # Корректное значение
    
    def _set_value(self, col, value):
        """Установка значения в переменную и обновление отображения"""
        value = self._validate_value(value)  # Валидация значения
        self.cell_vars[col].set(str(value))  # Сохранение в переменную
        items = self.cell_canvas.find_withtag(f'value_{col}')  # Поиск текста ячейки
        if items:
            self.cell_canvas.itemconfig(items[0], text=str(value))  # Обновление отображения
    
    def _cancel_edit(self):
        """Отмена редактирования и закрытие редактора"""
        if self.active_edit:
            try:
                self.active_edit[1].destroy()  # Уничтожение поля ввода
                self.cell_canvas.delete(self.active_edit[2])  # Удаление окна с canvas
            except:
                pass
            self.active_edit = None  # Сброс контекста
    
    def _on_click(self, event):
        """Обработчик клика по ячейке"""
        if not self._editable or self.count == 0:  # Таблица не редактируема или пуста
            return
        if self.app and hasattr(self.app, 'is_batch_running') and self.app.is_batch_running():  # Запущена множественная симуляция
            return
        if self.active_edit:  # Если есть активный редактор
            self._cancel_edit()  # Закрытие без сохранения
            return
        x = self.cell_canvas.canvasx(event.x)  # X-координата в canvas
        col = int(x // self.cell_w)  # Номер колонки
        self._start_edit(col)  # Начало редактирования
    
    def _start_edit(self, col):
        """Начало редактирования ячейки"""
        current = self._get_value(col)  # Текущее значение
        entry = tk.Entry(self.cell_canvas, bg=self.factory.theme.get_color('input_bg'), fg=self.factory.theme.get_color('text_color'), 
                         font=self.factory.get_font('table_cell'), justify='center', bd=1, relief='solid')  # Поле ввода
        entry.insert(0, str(current))  # Вставка текущего значения
        entry.select_range(0, tk.END)  # Выделение всего текста
        win_id = self.cell_canvas.create_window(col * self.cell_w, 0, window=entry, anchor='nw', width=self.cell_w, height=self.cell_h)  # Редактор
        self.active_edit = (col, entry, win_id, current)  # Сохранение контекста
        entry.focus_set()  # Фокус на поле ввода
        
        def commit():
            """Сохранение отредактированного значения"""
            if self.active_edit and not self._pending_commit:
                self._pending_commit = True  # Блокировка повторных вызовов
                try:
                    col, entry, win_id, old = self.active_edit  # Распаковка контекста
                    if not self._editable:  # Таблица больше не редактируема
                        self._cancel_edit()
                        return
                    val = self._validate_value(entry.get())  # Валидация введенного значения
                    if val is None:  # Ошибка валидации
                        val = old
                    if val != old:  # Значение изменилось
                        self._set_value(col, val)  # Сохранение нового значения
                finally:
                    self._cancel_edit()  # Закрытие редактора
                    self._pending_commit = False  # Сброс блокировки
        entry.bind('<Return>', lambda e: commit())  # Enter - сохранение
        entry.bind('<Escape>', lambda e: self._cancel_edit())  # Escape - отмена
        entry.bind('<FocusOut>', lambda e: self.cell_canvas.after(50, commit))  # Потеря фокуса - сохранение
    
    def set_count(self, count, max_vertex):
        """Установка количества ячеек и максимального значения для валидации"""
        self.count = count  # Количество ячеек
        self.max_vertex = max_vertex  # Максимальный номер вершины
        self.cell_vars = []  # Сброс списка переменных
        for i in range(count):  # Создание переменных для каждой ячейки
            initial = i + 1  # Начальное значение (1,2,3...)
            if initial > self.max_vertex:  # Если превышает максимум
                initial = self.max_vertex  # Ограничение максимумом
            self.cell_vars.append(tk.StringVar(value=str(initial)))  # Переменная с начальным значением
        self.cell_canvas.xview_moveto(0)  # Сброс прокрутки в начало
        self.headers.xview_moveto(0)  # Синхронный сброс заголовков
        self.redraw()  # Перерисовка таблицы
    
    def get_values(self):
        """Возврат списка значений из всех ячеек"""
        values = []  # Список значений
        for var in self.cell_vars:  # Перебор всех переменных
            try:
                values.append(int(var.get()))  # Преобразование в целое число
            except ValueError:
                values.append(1)  # При ошибке возвращаем 1
        return values
    
    def set_editable(self, editable):
        """Блокировка или разблокировка редактирования ячеек"""
        self._editable = editable  # Установка флага
        if not editable and self.active_edit:  # Если блокировка и есть активный редактор
            self._cancel_edit()  # Закрытие редактора
    
    def set_enabled(self, enabled):
        """Блокировка или разблокировка ячеек (сохранено для совместимости)"""
        self.set_editable(enabled)  # Вызов основного метода
    
    def pack(self, **kwargs):
        """Упаковка контейнера в родительский виджет"""
        self.container.pack(**kwargs)  # Передача параметров упаковки
    
    def grid(self, **kwargs):
        """Размещение контейнера в сетке"""
        self.container.grid(**kwargs)  # Передача параметров сетки


# In[33]:


class CSVDataManager:
    """Менеджер для загрузки и сохранения данных в CSV"""
    
    MAX_VERTICES = 1000  # Максимальное число вершин в файле для загрузки
    
    def __init__(self, parent, app, data_type, mode='load'):
        """Инициализация менеджера с указанием типа данных и режима работы"""
        self.parent = parent  # Родительское окно
        self.app = app  # Экземпляр главного приложения
        self.data_type = data_type  # Тип данных ('vertices' или 'edges')
        self.mode = mode  # Режим работы ('load' или 'save')
        
        if mode == 'load':  # Режим загрузки данных
            self.dialog = tk.Toplevel(parent)  # Создание диалогового окна
            self.dialog.title(self.app.translator.t('load_csv'))  # Заголовок окна
            self.dialog.geometry("800x450")  # Размер окна
            self.dialog.transient(parent)  # Связь с родительским окном
            self.dialog.grab_set()  # Блокировка родительского окна
            self._center_window(self.dialog, 800, 450)  # Центрирование окна
            self._create_instructions_ui()  # Создание интерфейса инструкций
            self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())  # Закрытие по Escape
        else:  # Режим сохранения данных
            self._save_data()  # Немедленное сохранение без окна
    
    @staticmethod
    def save_vertices(app):
        """Сохранение весов вершин в CSV файл"""
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  # Временная метка для имени файла
        default_filename = f"vertex_data_{timestamp}.csv"  # Имя файла по умолчанию
        filepath = filedialog.asksaveasfilename(  # Диалог выбора пути сохранения
            title=app.translator.t('save_csv'),  # Заголовок диалога
            defaultextension=".csv",  # Расширение по умолчанию
            initialfile=default_filename,  # Имя файла по умолчанию
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]  # Типы файлов
        )
        if not filepath:  # Отмена сохранения
            return
        custom_tab = app.tab_manager.tab_instances[1]  # Вкладка пользовательского графа
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:  # Открытие файла для записи
            writer = csv.writer(f)  # Создание csv-писателя
            for i in range(custom_tab.data.graph.number_of_nodes()):  # Цикл по всем вершинам
                weight = custom_tab.data.get_vertex(i)  # Получение веса вершины
                writer.writerow([weight])  # Запись строки с весом
    
    @staticmethod
    def save_edges(app):
        """Сохранение матрицы ребер в CSV файл"""
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  # Временная метка для имени файла
        default_filename = f"edge_data_{timestamp}.csv"  # Имя файла по умолчанию
        filepath = filedialog.asksaveasfilename(  # Диалог выбора пути сохранения
            title=app.translator.t('save_csv'),  # Заголовок диалога
            defaultextension=".csv",  # Расширение по умолчанию
            initialfile=default_filename,  # Имя файла по умолчанию
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]  # Типы файлов
        )
        
        if not filepath:  # Отмена сохранения
            return
        custom_tab = app.tab_manager.tab_instances[1]  # Вкладка пользовательского графа
        n = custom_tab.data.graph.number_of_nodes()  # Количество вершин
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:  # Открытие файла для записи
            writer = csv.writer(f)  # Создание csv-писателя
            for i in range(n):  # Цикл по строкам матрицы
                row = []  # Строка матрицы
                for j in range(n):  # Цикл по столбцам матрицы
                    if i == j:  # Диагональный элемент
                        row.append(0.0)  # Нулевой вес (петля)
                    else:  # Недиагональный элемент
                        weight = custom_tab.data.get_edge_weight(min(i, j), max(i, j))  # Получение веса ребра
                        row.append(weight)  # Добавление в строку
                writer.writerow(row)  # Запись строки матрицы
    
    def _save_data(self):
        """Вызов соответствующего метода сохранения в зависимости от типа данных"""
        if self.data_type == 'vertices':  # Сохранение вершин
            self.save_vertices(self.app)  # Вызов статического метода
        else:  # Сохранение ребер
            self.save_edges(self.app)  # Вызов статического метода
    
    def _center_window(self, window, width, height):
        """Центрирование окна относительно родительского окна"""
        window.update_idletasks()  # Обновление геометрии окна
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - width) // 2  # X-координата центра
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - height) // 2  # Y-координата центра
        window.geometry(f'{width}x{height}+{x}+{y}')  # Установка позиции окна
    
    def _create_instructions_ui(self):
        """Создание интерфейса с инструкциями для загрузки данных"""
        main_frame = self.app.widget_factory.create_frame(self.dialog)  # Основной контейнер
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)  # Размещение с отступами
        req_frame = self.app.widget_factory.create_labelframe(main_frame, 'format_requirements')  # Фрейм требований к формату
        req_frame.pack(fill='x', pady=(0, 20))  # Размещение
        req_texts = [  # Список ключей текстов требований
            'format_csv',  # Формат CSV
            'format_encoding',  # Кодировка UTF-8
            'v_format_structure' if self.data_type == 'vertices' else 'e_format_structure',  # Структура данных
            'v_format_range' if self.data_type == 'vertices' else 'e_format_range'  # Диапазон значений
        ]
        for text_key in req_texts:  # Цикл по ключам
            label = self.app.widget_factory.create_label(req_frame.content, text_key, 'normal')  # Создание метки
            label.pack(anchor='w', pady=2)  # Размещение с выравниванием по левому краю
        sync_frame = self.app.widget_factory.create_labelframe(main_frame, 'size_sync')  # Фрейм синхронизации размеров
        sync_frame.pack(fill='x', pady=(0, 20))  # Размещение
        sync_texts = [  # Список ключей текстов синхронизации
            'v_sync_limit' if self.data_type == 'vertices' else 'e_sync_limit',  # Ограничение размера
            'v_sync_more' if self.data_type == 'vertices' else 'e_sync_more',  # Добавление вершин
            'v_sync_less' if self.data_type == 'vertices' else 'e_sync_less'  # Удаление вершин
        ]
        for text_key in sync_texts:  # Цикл по ключам
            label = self.app.widget_factory.create_label(sync_frame.content, text_key, 'normal')  # Создание метки
            label.pack(anchor='w', pady=2)  # Размещение с выравниванием по левому краю
        btn_frame = self.app.widget_factory.create_frame(main_frame)  # Фрейм для кнопок
        btn_frame.pack(pady=(10, 0))  # Размещение с отступом сверху
        select_btn = self.app.widget_factory.create_button(btn_frame, 'select_csv_file', self._on_select_file, 'preset')# Кнопка выбора файла
        select_btn.pack(side='left', padx=(0, 10))  # Размещение слева с отступом
        cancel_btn = self.app.widget_factory.create_button(btn_frame, 'cancel', self.dialog.destroy, 'preset') # Кнопка отмены
        cancel_btn.pack(side='left')  # Размещение слева
    
    def _on_select_file(self):
        """Обработчик выбора файла в диалоговом окне"""
        filepath = filedialog.askopenfilename(  # Диалог выбора файла
            title=self.app.translator.t('load_csv'),  # Заголовок диалога
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]  # Типы файлов
        )
        if not filepath:  # Отмена выбора
            return
        try:
            if self.data_type == 'vertices':  # Загрузка вершин
                data = self._parse_vertices_csv(filepath)  # Парсинг CSV
                self._apply_vertices_data(data)  # Применение данных к графу
            else:  # Загрузка ребер
                data = self._parse_edges_csv(filepath)  # Парсинг CSV
                self._apply_edges_data(data)  # Применение данных к графу
            self.dialog.destroy()  # Закрытие диалогового окна
        except Exception as e:  # Ошибка при загрузке
            self._show_error_dialog(str(e))  # Показ окна с ошибкой
    
    def _parse_vertices_csv(self, filepath):
        """Парсинг CSV файла с весами вершин и возврат списка float"""
        values = []  # Список значений весов
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:  # Открытие файла с BOM-обработкой
                reader = csv.reader(f)  # Создание csv-читателя
                for line_num, row in enumerate(reader, 1):  # Цикл по строкам с нумерацией
                    if not row or all(cell.strip() == '' for cell in row):  # Пустая строка
                        continue
                    non_empty = [cell for cell in row if cell.strip() != '']  # Непустые ячейки
                    if len(non_empty) > 1:  # Более одного столбца
                        raise ValueError(f"Строка {line_num}: ожидался один столбец, найдено {len(non_empty)}")
                    if not non_empty:  # Нет данных в строке
                        continue
                    cell = non_empty[0]  # Первая ячейка
                    try:
                        val = float(cell)  # Преобразование в число
                        if val < 0.01 or val > 1.0:  # Проверка диапазона
                            raise ValueError(f"значение {val} вне допустимого диапазона [0.01, 1.0]")
                        values.append(val)  # Добавление в список
                    except ValueError as e:
                        if "вне допустимого диапазона" in str(e):  # Ошибка диапазона
                            raise ValueError(f"Строка {line_num}: {e}")
                        else:  # Ошибка преобразования
                            raise ValueError(f"Строка {line_num}: could not convert string to float: '{cell}'")
        except FileNotFoundError:  # Файл не найден
            raise Exception(f"Файл не найден: {filepath}")
        except PermissionError:  # Нет прав на чтение
            raise Exception(f"Нет прав на чтение файла: {filepath}")
        except UnicodeDecodeError:  # Ошибка кодировки
            raise Exception("Ошибка кодировки. Файл должен быть в кодировке UTF-8")
        if not values:  # Файл не содержит данных
            raise Exception("Файл не содержит данных")
        if len(values) > self.MAX_VERTICES:  # Превышение лимита вершин
            values = values[:self.MAX_VERTICES]  # Обрезание до лимита
        return values
    
    def _parse_edges_csv(self, filepath):
        """Парсинг CSV файла с матрицей ребер и возврат списка списков float"""
        matrix = []  # Матрица весов ребер
        expected_cols = None  # Ожидаемое количество столбцов
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:  # Открытие файла с BOM-обработкой
                reader = csv.reader(f)  # Создание csv-читателя
                for line_num, row in enumerate(reader, 1):  # Цикл по строкам с нумерацией
                    if not row or all(cell.strip() == '' for cell in row):  # Пустая строка
                        continue
                    while row and row[-1].strip() == '':  # Удаление пустых ячеек в конце
                        row = row[:-1]
                    if not row:  # Строка без данных
                        continue
                    if expected_cols is None:  # Первая непустая строка
                        expected_cols = len(row)  # Установка ожидаемого количества столбцов
                    elif len(row) != expected_cols:  # Несоответствие количества столбцов
                        raise ValueError(f"Матрица не квадратная: строка {line_num} содержит {len(row)} значений, ожидалось {expected_cols}")
                    row_values = []  # Значения строки
                    for col_num, cell in enumerate(row, 1):  # Цикл по ячейкам строки
                        cell = cell.strip()  # Удаление пробелов
                        if cell == '':  # Пустая ячейка
                            raise ValueError(f"Строка {line_num}, столбец {col_num}: пустое значение")
                        try:
                            val = float(cell)  # Преобразование в число
                            if val < -1.0 or val > 1.0:  # Проверка диапазона
                                raise ValueError(f"значение {val} вне допустимого диапазона [-1.0, 1.0]")
                            row_values.append(val)  # Добавление в строку
                        except ValueError as e:
                            if "вне допустимого диапазона" in str(e):  # Ошибка диапазона
                                raise ValueError(f"Строка {line_num}, столбец {col_num}: {e}")
                            else:  # Ошибка преобразования
                                raise ValueError(f"Строка {line_num}, столбец {col_num}: could not convert string to float: '{cell}'")
                    matrix.append(row_values)  # Добавление строки в матрицу
        except FileNotFoundError:  # Файл не найден
            raise Exception(f"Файл не найден: {filepath}")
        except PermissionError:  # Нет прав на чтение
            raise Exception(f"Нет прав на чтение файла: {filepath}")
        except UnicodeDecodeError:  # Ошибка кодировки
            raise Exception("Ошибка кодировки. Файл должен быть в кодировке UTF-8")
        if not matrix:  # Файл не содержит данных
            raise Exception("Файл не содержит данных")
        if expected_cols is not None and len(matrix) != expected_cols:  # Не квадратная матрица
            raise Exception(f"Матрица не квадратная: {len(matrix)} строк, {expected_cols} столбцов")
        n = min(len(matrix), self.MAX_VERTICES)  # Лимит размера матрицы
        matrix = [row[:n] for row in matrix[:n]]  # Обрезание до лимита
        return matrix
    
    def _apply_vertices_data(self, values):
        """Применение загруженных весов вершин к текущему графу"""
        custom_tab = self.app.tab_manager.tab_instances[1]  # Вкладка пользовательского графа
        current_n = custom_tab.data.graph.number_of_nodes()  # Текущее количество вершин
        loaded_n = len(values)  # Количество загруженных вершин
        default_edge_weight = self.app.settings['default_edge_weight'].get()  # Вес ребра по умолчанию
        if loaded_n < current_n:  # Загружено меньше вершин
            for i in range(current_n - 1, loaded_n - 1, -1):  # Удаление лишних вершин с конца
                custom_tab.data.remove_vertex(i)
            current_n = loaded_n  # Обновление текущего количества
        for i in range(min(current_n, loaded_n)):  # Обновление весов существующих вершин
            custom_tab.data.update_vertex(i, values[i])
        if loaded_n > current_n:  # Загружено больше вершин
            for i in range(current_n, loaded_n):  # Добавление новых вершин
                custom_tab.data.add_vertex(weight=values[i])
            for i in range(current_n, loaded_n):  # Добавление ребер для новых вершин
                for j in range(i):  # Связь со всеми существующими вершинами
                    custom_tab.data.update_edge(j, i, default_edge_weight)
        if custom_tab.graph_display:  # Сброс кэша позиций графа
            custom_tab.graph_display.pos_cache = None
        custom_tab.refresh_display()  # Обновление отображения
    
    def _apply_edges_data(self, matrix):
        """Применение загруженной матрицы ребер к текущему графу"""
        custom_tab = self.app.tab_manager.tab_instances[1]  # Вкладка пользовательского графа
        current_n = custom_tab.data.graph.number_of_nodes()  # Текущее количество вершин
        loaded_n = len(matrix)  # Размер загруженной матрицы
        default_vertex_weight = self.app.settings['default_vertex_weight'].get()  # Вес вершины по умолчанию
        default_edge_weight = self.app.settings['default_edge_weight'].get()  # Вес ребра по умолчанию
        if loaded_n < current_n:  # Загружена матрица меньшего размера
            for i in range(current_n - 1, loaded_n - 1, -1):  # Удаление лишних вершин
                custom_tab.data.remove_vertex(i)
            current_n = loaded_n  # Обновление текущего количества
        if loaded_n > current_n:  # Загружена матрица большего размера
            for i in range(current_n, loaded_n):  # Добавление новых вершин
                custom_tab.data.add_vertex(weight=default_vertex_weight)
        final_n = max(current_n, loaded_n)  # Итоговое количество вершин
        for i in range(final_n):  # Цикл по строкам матрицы
            for j in range(i + 1, final_n):  # Цикл по столбцам (верхний треугольник)
                if i < loaded_n and j < loaded_n:  # Индекс в пределах загруженной матрицы
                    weight = matrix[i][j]  # Использование загруженного веса
                else:  # Индекс за пределами загруженной матрицы
                    weight = default_edge_weight  # Использование веса по умолчанию
                custom_tab.data.update_edge(i, j, weight)  # Обновление веса ребра
        if custom_tab.graph_display:  # Сброс кэша позиций графа
            custom_tab.graph_display.pos_cache = None
        custom_tab.refresh_display()  # Обновление отображения
    
    def _show_error_dialog(self, error_message):
        """Показ диалогового окна с сообщением об ошибке"""
        error_dialog = tk.Toplevel(self.dialog)  # Создание окна ошибки
        error_dialog.title(self.app.translator.t('error_title'))  # Заголовок окна
        error_dialog.geometry("450x200")  # Размер окна
        error_dialog.transient(self.dialog)  # Связь с родительским окном
        error_dialog.grab_set()  # Блокировка родительского окна
        self._center_window(error_dialog, 450, 200)  # Центрирование окна
        main_frame = self.app.widget_factory.create_frame(error_dialog)  # Основной контейнер
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)  # Размещение с отступами
        error_label = tk.Label(main_frame,text=error_message, bg=self.app.theme_manager.get_color('bg_color'), fg='red',
                               font=self.app.widget_factory.get_font('normal'), justify='left', wraplength=400) # Метка сообщения об ошибке
        error_label.pack(pady=(0, 20))  # Размещение с отступом снизу
        btn_frame = self.app.widget_factory.create_frame(main_frame)  # Фрейм для кнопок
        btn_frame.pack()  # Размещение
        select_btn = self.app.widget_factory.create_button( btn_frame, 'select_another_file', 
                                                           lambda: [error_dialog.destroy(), self._on_select_file()],
                                                           'preset') # Кнопка выбора другого файла
        select_btn.pack(side='left', padx=(0, 10))  # Размещение слева с отступом
        cancel_btn = self.app.widget_factory.create_button(btn_frame, 'cancel', error_dialog.destroy, 'preset') # Кнопка отмены
        cancel_btn.pack(side='left')  # Размещение слева
        error_dialog.bind('<Escape>', lambda e: error_dialog.destroy())  # Закрытие по Escape


# In[34]:


class PDFExporter:
    """Экспорт отчета одиночной симуляции в PDF"""
    
    def __init__(self, app, sim_tab):
        """Инициализация экспортера с ссылками на приложение и вкладку симуляции"""
        self.app = app  # Экземпляр главного приложения
        self.sim_tab = sim_tab  # Экземпляр вкладки симуляции
        self.data = sim_tab.data  # Данные графа из вкладки симуляции
    
    def export(self):
        """Основной метод экспорта с диалогом сохранения и созданием pdf"""
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  # Временная метка для имени файла
        default_filename = f"simulation_report_{timestamp}.pdf"  # Имя файла по умолчанию
        filepath = filedialog.asksaveasfilename(  # Диалог выбора пути сохранения
            defaultextension=".pdf",  # Расширение по умолчанию
            initialfile=default_filename,  # Имя файла по умолчанию
            filetypes=[("PDF files", "*.pdf")]  # Типы файлов
        )
        if not filepath:  # Отмена сохранения
            return
        
        with PdfPages(filepath) as pdf:  # Создание pdf документа
            fig = plt.figure(figsize=(11, 15), facecolor='white')  # Фигура с белым фоном
            ax_graph = fig.add_axes([0.05, 0.58, 0.9, 0.37])  # Оси для графа
            self._render_graph(ax_graph)  # Отрисовка графа
            self._render_histogram(fig.add_axes([0.05, 0.45, 0.30, 0.10]), self.sim_tab.edge_hist)  # Гистограмма ребер
            self._render_histogram(fig.add_axes([0.38, 0.45, 0.30, 0.10]), self.sim_tab.vertex_hist)  # Гистограмма вершин
            self._render_start_vertex(fig.add_axes([0.71, 0.45, 0.24, 0.10]))  # Номер стартовой вершины
            y = 0.41  # Начальная позиция по вертикали
            sections = [  # Секции статистики в порядке отображения
                ('graph_parameters', self.sim_tab.graph_params_labels),  # Параметры графа
                ('generation_params', self._collect_generation_params()),  # Параметры генерации
                ('edge_stats', self.sim_tab.edge_stats_labels),  # Статистика ребер
                ('vertex_stats', self.sim_tab.vertex_stats_labels),  # Статистика вершин
                ('start_vertex_stats', self.sim_tab.start_vertex_labels),  # Статистика стартовой вершины
                ('simulation_results', self.sim_tab.simulation_results_labels),  # Результаты симуляции
            ]
            
            for title_key, labels_dict in sections:  # Цикл по секциям
                if not labels_dict:  # Пустая секция
                    continue
                y -= 0.016  # Смещение вниз
                ax = fig.add_axes([0.05, y, 0.9, 0.014])  # Оси для заголовка секции
                ax.set_axis_off()  # Отключение осей
                ax.text(0, 0.5, self.app.translator.t(title_key), fontsize=11, fontweight='bold', va='center')  # Заголовок
                for key, label in labels_dict.items():  # Цикл по строкам секции
                    if label is None or key == '' or key is None:  # Пропуск разделителей
                        continue
                    y -= 0.012  # Смещение вниз для строки
                    ax = fig.add_axes([0.07, y, 0.88, 0.011])  # Оси для строки статистики
                    ax.set_axis_off()  # Отключение осей
                    ui_key = StatisticsCalculator.data_key_to_ui_key(key)  # Преобразование в ui-ключ
                    ax.text(0, 0.5, self.app.translator.t(ui_key), fontsize=9, va='center')  # Название параметра
                    ax.text(0.98, 0.5, label.cget('text'), fontsize=9, fontweight='bold', ha='right', va='center')  # Значение
            pdf.savefig(fig, bbox_inches='tight', pad_inches=0.1)  # Сохранение страницы в pdf
            plt.close(fig)  # Закрытие фигуры
    
    def _render_graph(self, ax):
        """Копирование изображения графа на целевые оси"""
        ax.set_axis_off()  # Отключение осей
        canvas = FigureCanvasTkAgg(self.sim_tab.graph_display.figure, master=None)  # Холст из виджета графа
        canvas.draw()  # Рендеринг фигуры в canvas
        img = canvas.renderer.buffer_rgba()  # Получение изображения в виде массива rgba
        ax.imshow(img)  # Отображение изображения на осях
        ax.set_xlim(0, img.shape[1])  # Установка границ по горизонтали
        ax.set_ylim(img.shape[0], 0)  # Установка границ по вертикали
    
    def _render_histogram(self, ax, hist_widget):
        """Копирование изображения гистограммы на целевые оси"""
        ax.set_axis_off()  # Отключение осей
        if hist_widget:  # Гистограмма существует
            canvas = FigureCanvasTkAgg(hist_widget.figure, master=None)  # Холст из виджета гистограммы
            canvas.draw()  # Рендеринг фигуры в canvas
            img = canvas.renderer.buffer_rgba()  # Получение изображения в виде массива rgba
            ax.imshow(img)  # Отображение изображения на осях
            ax.set_xlim(0, img.shape[1])  # Установка границ по горизонтали
            ax.set_ylim(img.shape[0], 0)  # Установка границ по вертикали
    
    def _render_start_vertex(self, ax):
        """Отображение номера стартовой вершины"""
        ax.set_axis_off()  # Отключение осей
        text = f"{self.app.translator.t('vertex_number')}{self.sim_tab.ui_vars['start_vertex'].get()}"  # Текст с номером
        ax.text(0.5, 0.5, text, fontsize=12, fontweight='bold', ha='center', va='center', transform=ax.transAxes)  # Текст по центру
    
    def _collect_generation_params(self):
        """Сбор параметров генерации из фрейма generation_params_frame"""
        params = {}  # Словарь параметров
        if not self.sim_tab.generation_params_frame:  # Фрейм параметров отсутствует
            return params
        for child in self.sim_tab.generation_params_frame.winfo_children():  # Обход всех виджетов
            if isinstance(child, tk.Frame):  # Внешний контейнер
                for row in child.winfo_children():  # Строки внутри контейнера
                    if isinstance(row, tk.Frame):  # Строка-контейнер
                        labels = [w for w in row.winfo_children() if isinstance(w, tk.Label)]  # Метки в строке
                        if len(labels) >= 2:  # Название и значение
                            key = labels[0].cget('text')  # Текст названия параметра
                            value = labels[1].cget('text')  # Текст значения
                            if key:  # Непустой ключ
                                params[key] = value  # Добавление в словарь
        return params


# In[35]:


class CSVExporter:
    """Экспорт результатов множественной симуляции в CSV"""
    
    EXPORT_FIELDS = [  # Полный список полей для экспорта
        'graph_index',  # Индекс графа
        'graph_seed',  # Seed графа
        'graph_seed_mode',  # Режим seed графа
        'start_vertex_index',  # Индекс стартовой вершины
        'simulation_num',  # Номер симуляции
        'param_vertex_count',  # Количество вершин
        'param_edge_count',  # Количество ребер
        'param_edge_dist',  # Распределение ребер
        'param_vertex_dist',  # Распределение вершин
        'param_resistance_type',  # Тип устойчивости
        'param_resistance_coeff',  # Коэффициент устойчивости
        'param_influence_type',  # Тип влияния
        'param_influence_coeff',  # Коэффициент влияния
        'param_damping_type',  # Тип затухания
        'param_damping_coeff',  # Коэффициент затухания
        
        'edge_min',  # Минимум весов ребер
        'edge_max',  # Максимум весов ребер
        'edge_mean',  # Среднее весов ребер
        'edge_std',  # Стандартное отклонение ребер
        'edge_median',  # Медиана весов ребер
        'edge_skewness',  # Асимметрия ребер
        'edge_kurtosis',  # Эксцесс ребер
        'edge_q05',  # 5-процентный квантиль ребер
        'edge_q95',  # 95-процентный квантиль ребер
        'edge_count_positive',  # Количество положительных ребер
        'edge_pct_positive',  # Процент положительных ребер
        'edge_sum_positive',  # Сумма положительных ребер
        'edge_mean_positive',  # Среднее положительных ребер
        'edge_count_negative',  # Количество отрицательных ребер
        'edge_pct_negative',  # Процент отрицательных ребер
        'edge_sum_negative',  # Сумма отрицательных ребер
        'edge_mean_negative',  # Среднее отрицательных ребер
        
        'vertex_min',  # Минимум весов вершин
        'vertex_max',  # Максимум весов вершин
        'vertex_mean',  # Среднее весов вершин
        'vertex_std',  # Стандартное отклонение вершин
        'vertex_median',  # Медиана весов вершин
        'vertex_skewness',  # Асимметрия вершин
        'vertex_kurtosis',  # Эксцесс вершин
        'vertex_q05',  # 5-процентный квантиль вершин
        'vertex_q95',  # 95-процентный квантиль вершин
        
        'start_vertex_weight',  # Вес стартовой вершины
        'start_vertex_avg_edge_weight',  # Средний вес связей стартовой вершины
        'start_vertex_count_positive',  # Количество положительных связей стартовой вершины
        'start_vertex_pct_positive',  # Процент положительных связей стартовой вершины
        'start_vertex_sum_positive',  # Сумма положительных связей стартовой вершины
        'start_vertex_mean_positive',  # Среднее положительных связей стартовой вершины
        'start_vertex_count_negative',  # Количество отрицательных связей стартовой вершины
        'start_vertex_pct_negative',  # Процент отрицательных связей стартовой вершины
        'start_vertex_sum_negative',  # Сумма отрицательных связей стартовой вершины
        'start_vertex_mean_negative',  # Среднее отрицательных связей стартовой вершины
        'start_vertex_resistance_coeff',  # Коэффициент устойчивости для стартовой вершины
        'start_vertex_influence_coeff',  # Коэффициент влияния для стартовой вершины
        
        'fire_total_burned',  # Количество сгоревших вершин
        'fire_total_iterations',  # Количество итераций симуляции
        'fire_spread_rate_1',  # Скорость распространения на шаге 1
        'fire_spread_rate_2',  # Скорость распространения на шаге 2
        'fire_spread_rate_3',  # Скорость распространения на шаге 3
        'fire_spread_rate_4',  # Скорость распространения на шаге 4
        'fire_spread_rate_5',  # Скорость распространения на шаге 5
        'fire_peak_new_burns',  # Пиковое количество новых возгораний
        'fire_time_to_peak',  # Время достижения пика
        'fire_time_from_peak',  # Время от пика до затухания
        
        'derived_s_avg_pos',  # Среднее положительных связей стартовой вершины (производный)
        'derived_s_avg_neg',  # Среднее отрицательных связей стартовой вершины (производный)
        'derived_g_avg_pos',  # Среднее положительных ребер графа (производный)
        'derived_g_avg_neg',  # Среднее отрицательных ребер графа (производный)
        'derived_quality_diff',  # Разница качеств (производный)
        'derived_balance_diff',  # Разница балансов (производный)
        'derived_net_potential',  # Чистый потенциал (производный)
        
        'ignition_method',  # Метод поджога
        'threshold_method',  # Тип порога
        'threshold_value',  # Значение порога
        'fire_history',  # Полная история возгораний (строка)
    ]
    
    def __init__(self, app, multi_tab):
        """Инициализация экспортера с ссылками на приложение и вкладку множественной симуляции"""
        self.app = app  # Экземпляр главного приложения
        self.multi_tab = multi_tab  # Экземпляр вкладки множественной симуляции
    
    def export_single_graph(self, graph_index):
        """Экспорт одного графа по индексу в csv файл"""
        row = self._find_row(graph_index)  # Поиск строки с данными графа
        if row is None:  # Граф не найден
            return
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  # Временная метка для имени файла
        filepath = filedialog.asksaveasfilename(  # Диалог выбора пути сохранения
            defaultextension=".csv",  # Расширение по умолчанию
            initialfile=f"graph_{graph_index}_simulations_{timestamp}.csv",  # Имя файла по умолчанию
            filetypes=[("CSV files", "*.csv")]  # Типы файлов
        )
        if not filepath:  # Отмена сохранения
            return
        rows_data = self._extract_all_rows_data([row])  # Извлечение данных из строки
        self._write_csv(filepath, rows_data)  # Запись в csv файл
    
    def export_all_graphs(self):
        """Экспорт всех графов в один csv файл"""
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  # Временная метка для имени файла
        filepath = filedialog.asksaveasfilename(  # Диалог выбора пути сохранения
            defaultextension=".csv",  # Расширение по умолчанию
            initialfile=f"all_graphs_simulations_{timestamp}.csv",  # Имя файла по умолчанию
            filetypes=[("CSV files", "*.csv")]  # Типы файлов
        )
        if not filepath:  # Отмена сохранения
            return
        all_rows = [row for row in self.multi_tab.result_rows if row and row.winfo_exists()]  # Сбор всех существующих строк
        rows_data = self._extract_all_rows_data(all_rows)  # Извлечение данных из всех строк
        self._write_csv(filepath, rows_data)  # Запись в csv файл
    
    def _find_row(self, graph_index):
        """Поиск строки по индексу графа"""
        for row in self.multi_tab.result_rows:  # Перебор всех строк
            if row and row.winfo_exists() and row.graph_index == graph_index:  # Строка существует и индекс совпадает
                return row  # Возврат найденной строки
        return None  # Строка не найдена
    
    def _extract_all_rows_data(self, rows):
        """Извлечение данных из списка строк для экспорта"""
        all_data = []  # Список всех данных
        for row in rows:  # Перебор строк
            graph_data = row.graph_data  # Данные графа
            graph_index = row.graph_index  # Индекс графа
            edge_stats, vertex_stats, _ = self.app.statistics.calculate_all(graph_data)  # Статистики графа
            dist_type = graph_data.get_edge_distribution_type()  # Тип распределения ребер
            vertex_dist_type = graph_data.get_vertex_distribution_type()  # Тип распределения вершин
            params = {  # Параметры графа
                'param_vertex_count': graph_data.graph.number_of_nodes(),  # Количество вершин
                'param_edge_count': graph_data.graph.number_of_edges(),  # Количество ребер
                'param_edge_dist': dist_type.lower(),  # Тип распределения ребер (нижний регистр)
                'param_vertex_dist': vertex_dist_type.lower(),  # Тип распределения вершин (нижний регистр)
                'param_resistance_type': graph_data.resistance_type,  # Тип устойчивости
                'param_resistance_coeff': graph_data.resistance_coeff,  # Коэффициент устойчивости
                'param_influence_type': graph_data.influence_type,  # Тип влияния
                'param_influence_coeff': graph_data.influence_coeff,  # Коэффициент влияния
                'param_damping_type': graph_data.damping_type,  # Тип затухания
                'param_damping_coeff': graph_data.damping_coeff,  # Коэффициент затухания
            }
            
            for sim in row.simulations:  # Перебор всех симуляций этого графа
                sim_data = params.copy()  # Копирование общих параметров
                sim_data['graph_index'] = graph_index  # Индекс графа
                sim_data['graph_seed'] = graph_data.graph_seed if graph_data.graph_seed is not None else ''  # Seed графа
                sim_data['graph_seed_mode'] = graph_data.graph_seed_mode if graph_data.graph_seed_mode is not None else ''  # Режим seed
                sim_data['simulation_num'] = sim['simulation_num']  # Номер симуляции
                sim_data['start_vertex_index'] = sim['start_vertex']  # Индекс стартовой вершины
                result = sim['result']  # Результат симуляции
                sim_data.update(self._extract_result_metrics(result))  # Добавление метрик результата
                sim_data['ignition_method'] = self.app.settings.get('ignition_method', 'Sequential')  # Метод поджога
                sim_data['threshold_method'] = self.app.settings.get('threshold_method', 'None')  # Тип порога
                sim_data['threshold_value'] = self.app.settings.get('threshold_value', 0.5)  # Значение порога
                sim_data.update(edge_stats)  # Добавление статистики ребер
                sim_data.update(vertex_stats)  # Добавление статистики вершин
                vertex_idx = sim['start_vertex'] - 1  # Индекс стартовой вершины (0-базовый)
                start_stats = self.app.statistics.start_vertex_stats(graph_data, vertex_idx)  # Статистика стартовой вершины
                sim_data.update(start_stats)  # Добавление статистики стартовой вершины
                sim_data.update(self._compute_derived_features(sim_data))  # Добавление производных признаков
                all_data.append(sim_data)  # Добавление в общий список
        return all_data
    
    def _extract_result_metrics(self, result):
        """Извлечение метрик из результата симуляции с data-ключами"""
        history = result['history']  # История возгораний
        total_burned = len(result['burned_nodes'])  # Общее количество сгоревших вершин
        total_iters = len(history) - 1  # Количество итераций (без стартовой)
        metrics = {
            'fire_total_burned': total_burned,  # Сгоревшие вершины
            'fire_total_iterations': total_iters,  # Количество итераций
        }
        
        for i in range(1, 6):  # Первые 5 шагов распространения
            metrics[f'fire_spread_rate_{i}'] = history[i] if i < len(history) else 0  # Скорость на шаге i
        if total_iters > 0 and len(history) > 1:  # Есть данные о распространении
            peak_new_burns = max(history[1:])  # Пиковое количество новых возгораний
            peak_time = history[1:].index(peak_new_burns) + 1  # Время достижения пика
            time_from_peak = total_iters - peak_time  # Время от пика до конца
        else:  # Нет распространения
            peak_new_burns = 0  # Нулевой пик
            peak_time = 0  # Нулевое время
            time_from_peak = 0  # Нулевое время
        metrics['fire_peak_new_burns'] = peak_new_burns  # Пик новых возгораний
        metrics['fire_time_to_peak'] = peak_time  # Время до пика
        metrics['fire_time_from_peak'] = time_from_peak  # Время от пика
        metrics['fire_history'] = ','.join(str(v) for v in history)  # История в виде строки
        return metrics
    
    def _compute_derived_features(self, sim_data):
        """Вычисление производных признаков с data-ключами"""
        spc = sim_data.get('start_vertex_count_positive', 0)  # Количество положительных связей стартовой вершины
        snc = sim_data.get('start_vertex_count_negative', 0)  # Количество отрицательных связей стартовой вершины
        sps = sim_data.get('start_vertex_sum_positive', 0)  # Сумма положительных связей стартовой вершины
        sns = sim_data.get('start_vertex_sum_negative', 0)  # Сумма отрицательных связей стартовой вершины
        gpc = sim_data.get('edge_count_positive', 0)  # Количество положительных ребер графа
        gnc = sim_data.get('edge_count_negative', 0)  # Количество отрицательных ребер графа
        gps = sim_data.get('edge_sum_positive', 0)  # Сумма положительных ребер графа
        gns = sim_data.get('edge_sum_negative', 0)  # Сумма отрицательных ребер графа
        s_avg_pos = sps / spc if spc > 0 else 0  # Среднее положительных связей стартовой вершины
        s_avg_neg = sns / snc if snc > 0 else 0  # Среднее отрицательных связей стартовой вершины
        g_avg_pos = gps / gpc if gpc > 0 else 0  # Среднее положительных ребер графа
        g_avg_neg = gns / gnc if gnc > 0 else 0  # Среднее отрицательных ребер графа
        return {
            'derived_s_avg_pos': s_avg_pos,  # Среднее положительных связей стартовой вершины
            'derived_s_avg_neg': s_avg_neg,  # Среднее отрицательных связей стартовой вершины
            'derived_g_avg_pos': g_avg_pos,  # Среднее положительных ребер графа
            'derived_g_avg_neg': g_avg_neg,  # Среднее отрицательных ребер графа
            'derived_quality_diff': s_avg_pos - g_avg_neg,  # Разница качеств
            'derived_balance_diff': spc - gnc,  # Разница балансов
            'derived_net_potential': s_avg_pos * spc - g_avg_neg * gnc  # Чистый потенциал
        }
    
    def _write_csv(self, filepath, rows_data):
        """Запись данных в csv файл"""
        if not rows_data:  # Нет данных для записи
            return
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:  # Открытие файла для записи
            writer = csv.DictWriter(f, fieldnames=self.EXPORT_FIELDS, extrasaction='ignore')  # Создание csv-писателя
            writer.writeheader()  # Запись заголовка
            writer.writerows(rows_data)  # Запись всех строк данных


# In[36]:


class BatchSummaryWindow:
    """Окно просмотра итогов множественной симуляции"""
    
    COLOR_MIN_HEX = '#228B22'  # Зеленый цвет для минимальных значений
    COLOR_MAX_HEX = '#8B0000'  # Красный цвет для максимальных значений
    COLOR_MID_HEX = '#DAA520'  # Золотистый цвет для средних значений
    
    def __init__(self, parent, app, batch_params, total_generations, all_results=None, graph_index=None):
        """Инициализация окна итогов с параметрами и результатами симуляций"""
        self.parent = parent  # Родительское окно
        self.app = app  # Экземпляр главного приложения
        self.batch_params = batch_params  # Параметры пакетной генерации
        self.total_generations = total_generations  # Общее количество генераций
        self.graph_index = graph_index  # Индекс графа (если выбран конкретный)
        if graph_index is not None and all_results:  # Фильтрация по индексу графа
            self.results = [r for r in all_results if r.get('graph_index') == graph_index]
        else:  # Все результаты
            self.results = all_results or []
        self._collect_data()  # Сбор метрик и признаков
        self.window = tk.Toplevel(parent)  # Создание окна
        self.window.title(self.app.translator.t('batch_summary_title'))  # Заголовок окна
        self.window.transient(parent)  # Связь с родительским окном
        self.window.grab_set()  # Блокировка родительского окна
        self.window.state('zoomed')  # Полноэкранный режим
        self.window.configure(bg=self.app.theme_manager.get_color('bg_color'))  # Фон из темы
        self.window.bind('<Escape>', lambda e: self.window.destroy())  # Закрытие по Escape
        self._build_ui()  # Построение интерфейса
    
    def _collect_data(self):
        """Сбор всех метрик и создание dataframe из результатов"""
        self.burned_data = []  # Список сгоревших вершин
        self.iterations_data = []  # Список длительностей
        self.time_to_peak_data = []  # Список времен до пика
        self.peak_new_burns_data = []  # Список пиковых возгораний
        self.time_from_peak_data = []  # Список времен от пика
        self.spread_rates = {1: [], 2: [], 3: [], 4: [], 5: []}  # Скорости распространения по шагам
        self.n_vertices = 0  # Количество вершин в графе
        self.vulnerability_data = []  # Данные уязвимости вершин
        all_rows = []  # Все строки данных
        for result_row in self.results:  # Перебор результатов
            graph_data = result_row.get('graph_data')  # Данные графа
            if not graph_data or not graph_data.graph:  # Некорректные данные
                continue
            if self.n_vertices == 0:  # Первый граф
                self.n_vertices = graph_data.graph.number_of_nodes()  # Сохранение количества вершин
            edge_stats, vertex_stats, _ = self.app.statistics.calculate_all(graph_data)  # Статистики графа
            graph_vuln = self._init_vertex_vulnerability(result_row, graph_data)  # Инициализация уязвимости
            for sim in result_row.get('simulations', []):  # Перебор симуляций
                self._update_vertex_vulnerability(graph_vuln, sim, graph_data)  # Обновление уязвимости
                sim_data = self._process_single_simulation(sim, graph_data, edge_stats, vertex_stats,
                                                           result_row.get('graph_index', 0))# Обработка одной симуляции
                all_rows.append(sim_data)  # Добавление в список
            if graph_vuln:  # Данные уязвимости существуют
                self.vulnerability_data.append(graph_vuln)  # Добавление в список
        self.features_df = pd.DataFrame(all_rows) if all_rows else None  # Создание dataframe
    
    def _init_vertex_vulnerability(self, result_row, graph_data):
        """Инициализация словаря уязвимости с нулевыми счетчиками"""
        graph_vuln = {  # Словарь уязвимости для графа
            'graph_index': result_row.get('graph_index', 0),  # Индекс графа
            'graph_data': graph_data,  # Данные графа
            'vertex_data': {}  # Данные по вершинам
        }
        for i in range(graph_data.graph.number_of_nodes()):  # Перебор вершин
            node = f'V{i}'  # Имя вершины
            neighbors = list(graph_data.graph.neighbors(node))  # Соседи
            neighbor_weights = [graph_data.graph[node][nbr]['weight'] for nbr in neighbors]  # Веса ребер
            pos_neighbors = [w for w in neighbor_weights if w > 0]  # Положительные связи
            neg_neighbors = [w for w in neighbor_weights if w < 0]  # Отрицательные связи
            graph_vuln['vertex_data'][i] = {  # Данные вершины
                'burned_count': 0,  # Счетчик сгораний
                'not_start_count': 0,  # Счетчик не-стартовых симуляций
                'step_counts': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},  # Счетчики по шагам
                'vertex_weight': graph_data.graph.nodes[node].get('weight', 0),  # Вес вершины
                'degree': len(neighbors),  # Степень вершины
                'avg_edge_weight': np.mean(neighbor_weights) if neighbor_weights else 0,  # Средний вес ребер
                'positive_count': len(pos_neighbors),  # Количество положительных связей
                'positive_sum': sum(pos_neighbors) if pos_neighbors else 0,  # Сумма положительных весов
                'positive_mean': np.mean(pos_neighbors) if pos_neighbors else 0,  # Среднее положительных
                'negative_count': len(neg_neighbors),  # Количество отрицательных связей
                'negative_sum': sum(neg_neighbors) if neg_neighbors else 0,  # Сумма отрицательных весов
                'negative_mean': np.mean(neg_neighbors) if neg_neighbors else 0,  # Среднее отрицательных
                'positive_percent': (len(pos_neighbors) / len(neighbors) * 100) if neighbors else 0,  # Процент положительных
                'negative_percent': (len(neg_neighbors) / len(neighbors) * 100) if neighbors else 0,  # Процент отрицательных
            }
        return graph_vuln
    
    def _update_vertex_vulnerability(self, graph_vuln, sim, graph_data):
        """Обновление счетчиков уязвимости на основе одной симуляции"""
        start_vertex_idx = sim['start_vertex'] - 1  # Индекс стартовой вершины
        burned_nodes = sim['result']['burned_nodes']  # Сгоревшие вершины
        for vertex_idx in range(graph_data.graph.number_of_nodes()):  # Перебор вершин
            if vertex_idx == start_vertex_idx:  # Пропуск стартовой вершины
                continue
            node = f'V{vertex_idx}'  # Имя вершины
            graph_vuln['vertex_data'][vertex_idx]['not_start_count'] += 1  # Увеличение счетчика не-стартовых
            if node in burned_nodes:  # Вершина сгорела
                graph_vuln['vertex_data'][vertex_idx]['burned_count'] += 1  # Увеличение счетчика сгораний
                step_burned = burned_nodes[node]  # Шаг возгорания
                if step_burned in graph_vuln['vertex_data'][vertex_idx]['step_counts']:  # Шаг в пределах 1-5
                    graph_vuln['vertex_data'][vertex_idx]['step_counts'][step_burned] += 1  # Увеличение счетчика шага
    
    def _process_single_simulation(self, sim, graph_data, edge_stats, vertex_stats, graph_index):
        """Обработка одной симуляции и возврат строки данных"""
        history = sim['result']['history']  # История возгораний
        total_burned = len(sim['result']['burned_nodes'])  # Общее количество сгоревших
        total_iterations = len(history) - 1  # Количество итераций
        start_vertex = sim['start_vertex']  # Стартовая вершина
        if total_iterations > 0 and len(history) > 1:  # Есть распространение
            peak_new_burns = max(history[1:])  # Пиковое количество новых возгораний
            peak_time = history[1:].index(peak_new_burns) + 1  # Время достижения пика
            time_from_peak = total_iterations - peak_time  # Время от пика до конца
        else:  # Нет распространения
            peak_new_burns = 0  # Нулевой пик
            peak_time = 0  # Нулевое время
            time_from_peak = 0  # Нулевое время
        self.burned_data.append(total_burned)  # Добавление в список
        self.iterations_data.append(total_iterations)  # Добавление в список
        self.time_to_peak_data.append(peak_time)  # Добавление в список
        self.peak_new_burns_data.append(peak_new_burns)  # Добавление в список
        self.time_from_peak_data.append(time_from_peak)  # Добавление в список
        for step in range(1, 6):  # Первые 5 шагов
            rate = history[step] if step < len(history) else 0  # Скорость на шаге
            self.spread_rates[step].append(rate)  # Добавление в список
        start_stats = self.app.statistics.start_vertex_stats(graph_data, start_vertex - 1)  # Статистика стартовой вершины
        derived = self._compute_derived_features(start_stats, edge_stats)  # Производные признаки
        return {  # Строка данных
            'graph_index': graph_index,  # Индекс графа
            **{k: v for k, v in edge_stats.items()},  # Статистика ребер
            **{k: v for k, v in vertex_stats.items()},  # Статистика вершин
            **{k: v for k, v in start_stats.items()},  # Статистика стартовой вершины
            'fire_total_burned': total_burned,  # Сгоревшие вершины
            'fire_total_iterations': total_iterations,  # Длительность
            'fire_time_to_peak': peak_time,  # Время до пика
            'fire_peak_new_burns': peak_new_burns,  # Пик новых возгораний
            'fire_time_from_peak': time_from_peak,  # Время от пика
            'fire_spread_rate_1': history[1] if len(history) > 1 else 0,  # Скорость на шаге 1
            'fire_spread_rate_2': history[2] if len(history) > 2 else 0,  # Скорость на шаге 2
            'fire_spread_rate_3': history[3] if len(history) > 3 else 0,  # Скорость на шаге 3
            'fire_spread_rate_4': history[4] if len(history) > 4 else 0,  # Скорость на шаге 4
            'fire_spread_rate_5': history[5] if len(history) > 5 else 0,  # Скорость на шаге 5
            **derived,  # Производные признаки
        }
    
    def _compute_derived_features(self, start_stats, edge_stats):
        """Вычисление производных признаков для анализа"""
        sps = start_stats.get('start_vertex_sum_positive', 0)  # Сумма положительных связей стартовой вершины
        spc = max(start_stats.get('start_vertex_count_positive', 0), 1)  # Количество положительных связей (минимум 1)
        sns = start_stats.get('start_vertex_sum_negative', 0)  # Сумма отрицательных связей стартовой вершины
        snc = max(start_stats.get('start_vertex_count_negative', 0), 1)  # Количество отрицательных связей (минимум 1)
        gps = edge_stats.get('edge_sum_positive', 0)  # Сумма положительных ребер графа
        gpc = max(edge_stats.get('edge_count_positive', 0), 1)  # Количество положительных ребер (минимум 1)
        gns = edge_stats.get('edge_sum_negative', 0)  # Сумма отрицательных ребер графа
        gnc = max(edge_stats.get('edge_count_negative', 0), 1)  # Количество отрицательных ребер (минимум 1)
        s_avg_pos = sps / spc  # Среднее положительных связей стартовой вершины
        s_avg_neg = sns / snc  # Среднее отрицательных связей стартовой вершины
        g_avg_pos = gps / gpc  # Среднее положительных ребер графа
        g_avg_neg = gns / gnc  # Среднее отрицательных ребер графа
        return {
            'derived_s_avg_pos': s_avg_pos,  # Среднее положительных связей стартовой вершины
            'derived_s_avg_neg': s_avg_neg,  # Среднее отрицательных связей стартовой вершины
            'derived_g_avg_pos': g_avg_pos,  # Среднее положительных ребер графа
            'derived_g_avg_neg': g_avg_neg,  # Среднее отрицательных ребер графа
            'derived_quality_diff': s_avg_pos - g_avg_neg,  # Разница качеств
            'derived_balance_diff': spc - gnc,  # Разница балансов
            'derived_net_potential': s_avg_pos * spc - g_avg_neg * gnc,  # Чистый потенциал
        }
    
    def _build_ui(self):
        """Построение интерфейса окна итогов"""
        scroll = ScrollableFrame(self.window, self.app.widget_factory)  # Прокручиваемый фрейм
        scroll.pack(fill='both', expand=True)  # Размещение с растяжением
        content = scroll.inner  # Внутренний контент
        main_container = self.app.widget_factory.create_frame(content)  # Основной контейнер
        main_container.pack(fill='both', expand=True, padx=30, pady=30)  # Размещение с отступами
        main_container.columnconfigure(0, weight=1)  # Растяжение колонки
        current_row = 0  # Текущая строка
        self._build_params_section(main_container, current_row)  # Секция параметров
        current_row += 1  # Увеличение счетчика
        metric_groups = [  # Группы метрик для отображения
            {
                'data': self.burned_data,  # Данные сгоревших вершин
                'max_val': self.n_vertices,  # Максимальное значение
                'title_key': 'burned_vertices_title',  # Ключ заголовка
                'target_col': 'fire_total_burned',  # Целевая колонка
                'importance_title_key': 'features_importance_title'  # Ключ значимости
            },
            {
                'data': self.iterations_data,  # Данные длительностей
                'max_val': max(self.iterations_data) if self.iterations_data else 1,  # Максимальное значение
                'title_key': 'burned_duration_title',  # Ключ заголовка
                'target_col': 'fire_total_iterations',  # Целевая колонка
                'importance_title_key': 'features_importance_duration_title'  # Ключ значимости
            },
            {
                'data': self.time_to_peak_data,  # Данные времени до пика
                'max_val': max(self.time_to_peak_data) if self.time_to_peak_data else 1,  # Максимальное значение
                'title_key': 'time_to_peak_title',  # Ключ заголовка
                'target_col': 'fire_time_to_peak',  # Целевая колонка
                'importance_title_key': 'features_importance_time_to_peak_title'  # Ключ значимости
            },
            {
                'data': self.peak_new_burns_data,  # Данные пиковых возгораний
                'max_val': max(self.peak_new_burns_data) if self.peak_new_burns_data else 1,  # Максимальное значение
                'title_key': 'peak_new_burns_title',  # Ключ заголовка
                'target_col': 'fire_peak_new_burns',  # Целевая колонка
                'importance_title_key': 'features_importance_peak_title'  # Ключ значимости
            },
            {
                'data': self.time_from_peak_data,  # Данные времени от пика
                'max_val': max(self.time_from_peak_data) if self.time_from_peak_data else 1,  # Максимальное значение
                'title_key': 'time_from_peak_title',  # Ключ заголовка
                'target_col': 'fire_time_from_peak',  # Целевая колонка
                'importance_title_key': 'features_importance_time_from_peak_title'  # Ключ значимости
            },
            {
                'data': self.spread_rates[1],  # Данные скорости на шаге 1
                'max_val': max(self.spread_rates[1]) if self.spread_rates[1] else 1,  # Максимальное значение
                'title_key': 'spread_rate_title_1',  # Ключ заголовка
                'target_col': 'fire_spread_rate_1',  # Целевая колонка
                'importance_title_key': 'features_importance_spread_1_title'  # Ключ значимости
            },
        ]
        
        for group in metric_groups:  # Перебор групп метрик
            if group['data']:  # Есть данные для отображения
                current_row = self._build_metric_group(main_container, current_row, group)  # Построение группы
        if self.vulnerability_data:  # Есть данные уязвимости
            self._build_vulnerability_section(main_container, current_row)  # Построение секции уязвимости
    
    def _build_metric_group(self, parent, start_row, group):
        """Построение компактной группы для одной метрики"""
        current_row = start_row  # Текущая строка
        self._build_distribution_section(parent, current_row, group['data'], group['max_val'], group['title_key'])  # Секция распределения
        current_row += 1  # Увеличение счетчика
        df = self.features_df  # Dataframe признаков
        if df is not None and len(df) > 0 and group['target_col'] in df.columns:  # Проверка существования
            if df[group['target_col']].std() > 0:  # Ненулевая дисперсия
                self._build_importance_section(parent, current_row, group['target_col'], group['importance_title_key'])  # Секция значимости
                current_row += 1  # Увеличение счетчика
        spacer = self.app.widget_factory.create_frame(parent, height=30)  # Разделитель
        spacer.grid(row=current_row, column=0, sticky='ew')  # Размещение
        spacer.grid_propagate(False)  # Запрет изменения размера
        current_row += 1  # Увеличение счетчика
        return current_row  # Возврат новой строки
    
    def _build_params_section(self, parent, row):
        """Построение секции с параметрами генерации"""
        params_frame = self.app.widget_factory.create_labelframe(parent, 'batch_generation_params')  # Фрейм параметров
        params_frame.grid(row=row, column=0, sticky='ew', pady=(0, 30))  # Размещение
        content = params_frame.content  # Внутренний контент
        content.columnconfigure(0, weight=0, minsize=200)  # Колонка названий
        content.columnconfigure(1, weight=1)  # Колонка значений
        params_list = [  # Список параметров для отображения
            ('batch_graphs_count', self.batch_params.get('graphs_count', 'N/A')),  # Количество графов
            ('batch_start_vertices_count', self.batch_params.get('start_vertices_count', 'N/A')),  # Количество стартовых вершин
            ('batch_simulations_per_vertex', self.batch_params.get('simulations_per_vertex', 'N/A')),  # Количество симуляций на вершину
        ]
        for i, (label_key, value) in enumerate(params_list):  # Перебор параметров
            self.app.widget_factory.create_label(content,label_key,'normal').grid(row=i, column=0, sticky='w', pady=(10, 5))# Лейбл параметра
            val_label = self.app.widget_factory.create_label(content, '', 'normal')  # Лейбл значения
            val_label.config(text=str(value))  # Установка текста
            val_label.grid(row=i, column=1, sticky='w', pady=(10, 5), padx=(10, 0))  # Размещение
        
        row_idx = len(params_list)  # Следующая строка
        self.app.widget_factory.create_label(content, 'total_generations', 'normal').grid(row=row_idx,
                                                                column=0, sticky='w', pady=(20, 10)) # Лейбл общего количества
        val_label = self.app.widget_factory.create_label(content, '', 'small_bold')  # Лейбл значения
        val_label.config(text=str(self.total_generations))  # Установка текста
        val_label.grid(row=row_idx, column=1, sticky='w', pady=(20, 10), padx=(10, 0))  # Размещение
    
    def _build_distribution_section(self, parent, row, data, max_val, title_key):
        """Построение секции с распределением метрики"""
        frame = self.app.widget_factory.create_labelframe(parent, title_key)  # Фрейм с заголовком
        frame.grid(row=row, column=0, sticky='ew', pady=(0, 10))  # Размещение
        content = frame.content  # Внутренний контент
        self._create_full_distribution_chart(content, data, max_val)  # Полный барчарт
        groups_container = self.app.widget_factory.create_frame(content)  # Контейнер для группировок
        groups_container.pack(fill='x', pady=(20, 0))  # Размещение
        for i in range(6):  # Шесть колонок для графиков
            groups_container.columnconfigure(i, weight=1, uniform='dist_col')  # Равномерное распределение
        n = max(max_val, 1)  # Нормализация
        mid = n // 2  # Середина
        p10 = max(2, int(n * 0.1))  # 10-й процентиль
        p90 = min(n - 1, int(n * 0.9))  # 90-й процентиль
        groupings = [  # Варианты группировки
            {
                'labels': ['1', f'2-{n-1}', str(n)],  # Метки для трех групп
                'ranges': [(1, 1), (2, n-1), (n, n)]  # Диапазоны
            },
            {
                'labels': ['1', f'2-{mid}', f'{mid+1}-{n-1}', str(n)],  # Метки для четырех групп
                'ranges': [(1, 1), (2, mid), (mid+1, n-1), (n, n)]  # Диапазоны
            },
            {
                'labels': ['1', f'2-{p10}', f'{p10+1}-{p90-1}', f'{p90}-{n-1}', str(n)],  # Метки для пяти групп
                'ranges': [(1, 1), (2, p10), (p10+1, p90-1), (p90, n-1), (n, n)]  # Диапазоны
            }
        ]
        for col, grouping in enumerate(groupings):  # Перебор группировок
            group_data = self._group_data(data, grouping['ranges'])  # Группировка данных
            self._create_grouped_bar_chart(groups_container, group_data, grouping['labels'], row=0, column=col)  # Барчарт
        for col, grouping in enumerate(groupings):  # Перебор группировок для виолин-графиков
            self._create_grouped_violin_chart(groups_container, data, grouping['ranges'], grouping['labels'],
                                              n, row=0, column=col + 3)# Виолин-график
    
    def _group_data(self, data, ranges):
        """Группировка данных по диапазонам"""
        result = {}  # Словарь результатов
        for low, high in ranges:  # Перебор диапазонов
            label = str(low) if low == high else f'{low}-{high}'  # Метка диапазона
            result[label] = sum(1 for x in data if low <= x <= high)  # Подсчет количества
        return result
    
    def _get_distribution_colors(self, values, max_val):
        """Получение списка цветов для распределения"""
        return [
            self.COLOR_MAX_HEX if v == max_val  # Красный для максимума
            else self.COLOR_MIN_HEX if v == 1  # Зеленый для минимума
            else self.COLOR_MID_HEX  # Золотистый для остальных
            for v in values]
    
    def _get_grouped_colors(self, n_items):
        """Получение списка цветов для сгруппированных элементов"""
        if n_items <= 1:  # Один элемент
            return [self.COLOR_MAX_HEX]  # Только красный
        return [self.COLOR_MIN_HEX] + [self.COLOR_MID_HEX] * (n_items - 2) + [self.COLOR_MAX_HEX]  # Зеленый, золотистые, красный
    
    def _create_full_distribution_chart(self, parent, data, max_val):
        """Создание полного барчарта распределения"""
        fig = Figure(figsize=(14, 3), dpi=100, facecolor=self.app.theme_manager.get_color('plot_bg'))  # Фигура
        ax = fig.add_subplot(111)  # Оси
        ax.set_facecolor(self.app.theme_manager.get_color('plot_bg'))  # Фон осей
        counts = {}  # Счетчики значений
        for x in data:  # Перебор данных
            counts[x] = counts.get(x, 0) + 1  # Увеличение счетчика
        all_values = list(range(1, max_val + 1))  # Все возможные значения
        heights = [counts.get(v, 0) for v in all_values]  # Высоты столбцов
        colors = self._get_distribution_colors(all_values, max_val)  # Цвета столбцов
        ax.bar(all_values, heights, color=colors, alpha=0.5, edgecolor='gray', linewidth=0.5)  # Столбцы
        max_h = max(heights) if heights else 1  # Максимальная высота
        for v, h in zip(all_values, heights):  # Перебор столбцов
            if h > max_h * 0.03:  # Достаточно высокий столбец
                ax.text(v, h, str(h), ha='center', va='bottom', fontsize=7,  # Подпись значения
                       color=self.app.theme_manager.get_color('text_color'))
        ax.set_xlabel('Value', fontsize=9, color=self.app.theme_manager.get_color('text_color'))  # Подпись оси x
        ax.set_ylabel('Count', fontsize=9, color=self.app.theme_manager.get_color('text_color'))  # Подпись оси y
        ax.tick_params(colors=self.app.theme_manager.get_color('text_color'), labelsize=8)  # Параметры меток
        for spine in ['top', 'right']:  # Скрытие верхней и правой границ
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color(self.app.theme_manager.get_color('border_color'))  # Цвет нижней границы
        ax.spines['left'].set_color(self.app.theme_manager.get_color('border_color'))  # Цвет левой границы
        fig.tight_layout()  # Компактная компоновка
        canvas = FigureCanvasTkAgg(fig, master=parent)  # Холст
        canvas.get_tk_widget().pack(fill='x', pady=(0, 20))  # Размещение
        canvas.draw()  # Отрисовка
    
    def _create_grouped_bar_chart(self, parent, group_data, labels, row, column):
        """Создание маленького барчарта для группировки"""
        container = self.app.widget_factory.create_frame(parent)  # Контейнер
        container.grid(row=row, column=column, sticky='nsew', padx=5)  # Размещение
        fig = Figure(figsize=(2.5, 2), dpi=80, facecolor=self.app.theme_manager.get_color('plot_bg'))  # Фигура
        ax = fig.add_subplot(111)  # Оси
        ax.set_facecolor(self.app.theme_manager.get_color('plot_bg'))  # Фон осей
        values = [group_data.get(label, 0) for label in labels]  # Значения групп
        colors = self._get_grouped_colors(len(labels))  # Цвета столбцов
        bars = ax.bar(range(len(labels)), values, color=colors, alpha=0.5, edgecolor='gray', linewidth=0.5)  # Столбцы
        ax.set_xticks(range(len(labels)))  # Позиции меток
        ax.set_xticklabels(labels, fontsize=7, color=self.app.theme_manager.get_color('text_color'),  # Метки
                          rotation=45 if len(labels) > 4 else 0)  # Поворот при большом количестве
        for bar, val in zip(bars, values):  # Перебор столбцов
            if val > 0:  # Ненулевое значение
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(val), ha='center', va='bottom', fontsize=7,
                        color=self.app.theme_manager.get_color('text_color'))# Подпись
        ax.set_yticks([])  # Скрытие меток оси y
        for spine in ['left', 'top', 'right']:  # Скрытие левой, верхней и правой границ
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color(self.app.theme_manager.get_color('border_color'))  # Цвет нижней границы
        ax.tick_params(colors=self.app.theme_manager.get_color('text_color'), labelsize=7)  # Параметры меток
        fig.tight_layout()  # Компактная компоновка
        canvas = FigureCanvasTkAgg(fig, master=container)  # Холст
        canvas.get_tk_widget().pack(fill='both', expand=True)  # Размещение с растяжением
        canvas.draw()  # Отрисовка
    
    def _create_grouped_violin_chart(self, parent, data, ranges, labels, max_val, row, column):
        """Создание маленького виолин-графика для группировки"""
        container = self.app.widget_factory.create_frame(parent)  # Контейнер
        container.grid(row=row, column=column, sticky='nsew', padx=5)  # Размещение
        fig = Figure(figsize=(2.5, 2), dpi=80, facecolor=self.app.theme_manager.get_color('plot_bg'))  # Фигура
        ax = fig.add_subplot(111)  # Оси
        ax.set_facecolor(self.app.theme_manager.get_color('plot_bg'))  # Фон осей
        violin_data = []  # Данные для виолин
        for low, high in ranges:  # Перебор диапазонов
            group_values = [x for x in data if low <= x <= high]  # Значения в диапазоне
            if not group_values:  # Пустая группа
                group_values = [low]  # Заглушка
            violin_data.append(group_values)  # Добавление в список
        violin_colors = self._get_grouped_colors(len(ranges))  # Цвета виолин
        parts = ax.violinplot(violin_data, positions=range(len(ranges)), showmeans=True, showmedians=True, widths=0.7)  # Виолин-график
        for i, body in enumerate(parts['bodies']):  # Перебор тел виолин
            body.set_facecolor(violin_colors[i])  # Цвет заливки
            body.set_alpha(0.5)  # Прозрачность
        for partname in ('cbars', 'cmins', 'cmaxes', 'cmeans', 'cmedians'):  # Элементы виолин
            if partname in parts:  # Существующий элемент
                parts[partname].set_color(self.app.theme_manager.get_color('text_color'))  # Цвет
                parts[partname].set_linewidth(0.5)  # Толщина линии
        ax.set_xticks(range(len(labels)))  # Позиции меток
        ax.set_xticklabels(labels,fontsize=7,color=self.app.theme_manager.get_color('text_color'),rotation=45 if len(labels) > 4 else 0)# Метки
        if max_val > 0:  # Положительный максимум
            ax.set_ylim(-1, max_val + 1)  # Границы оси y
        ax.tick_params(colors=self.app.theme_manager.get_color('text_color'), labelsize=6)  # Параметры меток
        for spine in ['top', 'right']:  # Скрытие верхней и правой границ
            ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color(self.app.theme_manager.get_color('border_color'))  # Цвет нижней границы
        ax.spines['left'].set_color(self.app.theme_manager.get_color('border_color'))  # Цвет левой границы
        fig.tight_layout()  # Компактная компоновка
        canvas = FigureCanvasTkAgg(fig, master=container)  # Холст
        canvas.get_tk_widget().pack(fill='both', expand=True)  # Размещение с растяжением
        canvas.draw()  # Отрисовка
    
    def _get_feature_list(self):
        """Возврат списка всех признаков для анализа значимости"""
        return [
            'edge_min', 'edge_max', 'edge_mean', 'edge_median',  # Базовые статистики ребер
            'edge_std', 'edge_skewness', 'edge_kurtosis',  # Статистики разброса ребер
            'edge_q05', 'edge_q95',  # Квантили ребер
            'edge_count_positive', 'edge_sum_positive',  # Положительные ребра
            'edge_count_negative', 'edge_sum_negative',  # Отрицательные ребра
            
            'vertex_min', 'vertex_max', 'vertex_mean', 'vertex_median',  # Базовые статистики вершин
            'vertex_std', 'vertex_skewness', 'vertex_kurtosis',  # Статистики разброса вершин
            'vertex_q05', 'vertex_q95',  # Квантили вершин
            
            'start_vertex_weight',  # Вес стартовой вершины
            'start_vertex_avg_edge_weight',  # Средний вес связей стартовой вершины
            'start_vertex_count_positive', 'start_vertex_sum_positive',  # Положительные связи стартовой вершины
            'start_vertex_count_negative', 'start_vertex_sum_negative',  # Отрицательные связи стартовой вершины
            
            'derived_s_avg_pos', 'derived_s_avg_neg',  # Производные стартовой вершины
            'derived_g_avg_pos', 'derived_g_avg_neg',  # Производные графа
            'derived_quality_diff', 'derived_balance_diff', 'derived_net_potential',  # Составные признаки
        ]
    
    def _calc_spearman_importance(self, df, target_col):
        """Вычисление топ-5 признаков по корреляции Спирмена"""
        features = [f for f in self._get_feature_list() if f in df.columns and df[f].std() > 0]  # Фильтрация признаков
        if not features or df[target_col].std() == 0:  # Недостаточно данных
            return []
        correlations = {}  # Словарь корреляций
        for feat in features:  # Перебор признаков
            if len(set(df[feat])) > 1:  # Непостоянный признак
                try:
                    corr, _ = stats.spearmanr(df[feat], df[target_col])  # Корреляция Спирмена
                    correlations[feat] = abs(corr)  # Абсолютное значение
                except:  # Игнорирование ошибок
                    pass
        return sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:5]  # Топ-5
    
    def _calc_mutual_info_importance(self, df, target_col):
        """Вычисление топ-5 признаков по взаимной информации"""
        features = [f for f in self._get_feature_list() if f in df.columns and df[f].std() > 0]  # Фильтрация признаков
        if len(features) < 2:  # Недостаточно признаков
            return [(features[0], 0)] if features else []  # Один признак
        mi = mutual_info_regression(df[features], df[target_col], random_state=42)  # Взаимная информация
        scores = list(zip(features, mi))  # Признаки и их оценки
        return sorted(scores, key=lambda x: x[1], reverse=True)[:5]  # Топ-5
    
    def _calc_permutation_importance(self, df, target_col):
        """Вычисление топ-5 признаков по важности перестановкой"""
        features = [f for f in self._get_feature_list() if f in df.columns and df[f].std() > 0]  # Фильтрация признаков
        if len(features) < 2:  # Недостаточно признаков
            return [(features[0], 0)] if features else []  # Один признак
        X, y = df[features], df[target_col]  # Признаки и целевая переменная
        rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)  # Случайный лес
        rf.fit(X, y)  # Обучение модели
        perm_importance = permutation_importance(rf, X, y, n_repeats=10, random_state=42, n_jobs=-1)  # Важность перестановкой
        scores = list(zip(features, perm_importance.importances_mean))  # Признаки и оценки
        return sorted(scores, key=lambda x: x[1], reverse=True)[:5]  # Топ-5
    
    def _build_importance_section(self, parent, row, target_col, title_key):
        """Построение секции значимости признаков"""
        df = self.features_df  # Dataframe признаков
        if df is None or target_col not in df.columns:  # Нет данных
            return
        spearman_top5 = self._calc_spearman_importance(df, target_col)  # Корреляция Спирмена
        mutual_info_top5 = self._calc_mutual_info_importance(df, target_col)  # Взаимная информация
        permutation_top5 = self._calc_permutation_importance(df, target_col)  # Важность перестановкой
        
        all_unique_features = list(set([f for f, _ in spearman_top5] + 
                        [f for f, _ in mutual_info_top5] + [f for f, _ in permutation_top5]))# Уникальные признаки из всех методов
        
        importance_frame = self.app.widget_factory.create_labelframe(parent, title_key)  # Фрейм значимости
        importance_frame.grid(row=row, column=0, sticky='ew', pady=(0, 10))  # Размещение
        content = importance_frame.content  # Внутренний контент
        tables_container = self.app.widget_factory.create_frame(content)  # Контейнер для таблиц
        tables_container.pack(side='left', fill='y', padx=(0, 10))  # Размещение слева
        methods = [  # Методы анализа
            ('spearman_correlation', spearman_top5),  # Корреляция Спирмена
            ('mutual_information', mutual_info_top5),  # Взаимная информация
            ('permutation_importance', permutation_top5),  # Важность перестановкой
        ]
        
        for col, (method_name, top5) in enumerate(methods):  # Перебор методов
            table_frame = self.app.widget_factory.create_frame(tables_container)  # Фрейм таблицы
            table_frame.grid(row=0, column=col, sticky='n', padx=5)  # Размещение
            self._create_importance_table(table_frame, method_name, top5)  # Таблица значимости
        valid_features = [f for f in all_unique_features if f in df.columns and df[f].std() > 0]  # Признаки с дисперсией
        if len(valid_features) > 1:  # Достаточно признаков
            heatmap_container = self.app.widget_factory.create_frame(content)  # Контейнер тепловой карты
            heatmap_container.pack(side='left', fill='both', expand=True)  # Размещение
            self._create_correlation_heatmap(heatmap_container, valid_features)  # Тепловая карта корреляций
    
    def _create_importance_table(self, parent, title_key, top5):
        """Создание таблицы с топ-5 признаков"""
        header = self.app.widget_factory.create_label(parent, '', 'card_header')  # Заголовок таблицы
        header.config(text=self.app.translator.t(title_key))  # Текст заголовка
        header.pack(anchor='w', pady=(0, 10))  # Размещение
        for rank, (feat_name, value) in enumerate(top5, 1):  # Перебор признаков
            row_frame = self.app.widget_factory.create_frame(parent)  # Строка таблицы
            row_frame.pack(fill='x', pady=2)  # Размещение
            rank_label = self.app.widget_factory.create_label(row_frame, '', 'small_bold')  # Ранг
            rank_label.config(text=f"{rank}.")  # Текст ранга
            rank_label.pack(side='left', padx=(0, 5))  # Размещение
            feat_label = self.app.widget_factory.create_label(row_frame, '', 'small')  # Название признака
            feat_label.config(text=feat_name)  # Текст признака
            feat_label.pack(side='left')  # Размещение
            val_label = self.app.widget_factory.create_label(row_frame, '', 'small_bold')  # Значение
            val_label.config(text=f"{value:.4f}")  # Форматированное значение
            val_label.pack(side='right')  # Размещение
    
    def _create_correlation_heatmap(self, parent, features):
        """Создание тепловой карты корреляций с числовыми подписями"""
        fig = Figure(figsize=(5, 5), dpi=80, facecolor=self.app.theme_manager.get_color('plot_bg'))  # Фигура
        ax = fig.add_subplot(111)  # Оси
        ax.set_facecolor(self.app.theme_manager.get_color('plot_bg'))  # Фон осей
        corr_matrix = self.features_df[features].corr()  # Матрица корреляций
        im = ax.imshow(corr_matrix.values, cmap='RdYlBu_r', vmin=-1, vmax=1, aspect='auto')  # Изображение корреляций
        for i in range(len(features)):  # Перебор строк
            for j in range(len(features)):  # Перебор столбцов
                value = corr_matrix.values[i, j]  # Значение корреляции
                text_color = 'white' if abs(value) > 0.5 else 'black'  # Цвет текста
                ax.text(j, i, f'{value:.2f}', ha='center', va='center', fontsize=7, color=text_color)  # Подпись
        ax.set_xticks(range(len(features)))  # Позиции меток x
        ax.set_yticks(range(len(features)))  # Позиции меток y
        ax.set_xticklabels(features, rotation=45, ha='right', fontsize=6,color=self.app.theme_manager.get_color('text_color'))# Метки x
        ax.set_yticklabels(features, fontsize=6, color=self.app.theme_manager.get_color('text_color'))  # Метки y
        cbar = fig.colorbar(im, ax=ax, shrink=0.8)  # Цветовая шкала
        cbar.ax.tick_params(labelsize=5, colors=self.app.theme_manager.get_color('text_color'))  # Параметры шкалы
        fig.tight_layout()  # Компактная компоновка
        canvas = FigureCanvasTkAgg(fig, master=parent)  # Холст
        canvas.get_tk_widget().pack(fill='both', expand=True)  # Размещение с растяжением
        canvas.draw()  # Отрисовка
    
    def _build_vulnerability_section(self, parent, row):
        """Построение секции рейтинга уязвимости вершин"""
        vuln_frame = self.app.widget_factory.create_labelframe(parent, 'vulnerability_rating_title')  # Фрейм уязвимости
        vuln_frame.grid(row=row, column=0, sticky='ew', pady=(0, 30))  # Размещение
        content = vuln_frame.content  # Внутренний контент
        for graph_vuln in self.vulnerability_data:  # Перебор данных по графам
            graph_index = graph_vuln['graph_index']  # Индекс графа
            graph_data = graph_vuln['graph_data']  # Данные графа
            vertex_data = graph_vuln['vertex_data']  # Данные вершин
            if len(self.vulnerability_data) > 1:  # Несколько графов
                graph_label = self.app.widget_factory.create_label(content, '', 'header')  # Заголовок графа
                graph_label.config(text=f"Graph G{graph_index}")  # Текст заголовка
                graph_label.pack(anchor='w', pady=(0, 10))  # Размещение
            self._create_vulnerability_table(content, graph_data, vertex_data)  # Таблица уязвимости
    
    def _create_vulnerability_table(self, parent, graph_data, vertex_data):
        """Создание виртуальной таблицы уязвимости для одного графа"""
        cfg = self.app.size_config['virtual_table']  # Конфигурация таблицы
        cell_w = cfg['cell_width'] * 2  # Удвоенная ширина ячейки
        cell_h = cfg['cell_height']  # Высота ячейки
        n_vertices = graph_data.graph.number_of_nodes()  # Количество вершин
        rows = []  # Строки таблицы
        for vertex_idx in range(n_vertices):  # Перебор вершин
            vd = vertex_data[vertex_idx]  # Данные вершины
            not_start = vd['not_start_count']  # Количество не-стартовых симуляций
            burned = vd['burned_count']  # Количество сгораний
            total_pct = (burned / not_start * 100) if not_start > 0 else 0  # Процент сгораний
            step_pcts = {}  # Проценты по шагам
            for step in range(1, 6):  # Шаги 1-5
                step_pcts[step] = (vd['step_counts'][step] / burned * 100) if burned > 0 else 0  # Процент на шаге
            rows.append({  # Строка данных
                'vertex_idx': vertex_idx,  # Индекс вершины
                'total_pct': total_pct,  # Общий процент сгораний
                'step_pcts': step_pcts,  # Проценты по шагам
                'vertex_weight': vd['vertex_weight'],  # Вес вершины
                'avg_edge_weight': vd['avg_edge_weight'],  # Средний вес ребер
                'positive_count': vd['positive_count'],  # Количество положительных связей
                'positive_sum': vd['positive_sum'],  # Сумма положительных весов
                'positive_mean': vd['positive_mean'],  # Среднее положительных
                'negative_count': vd['negative_count'],  # Количество отрицательных связей
                'negative_sum': vd['negative_sum'],  # Сумма отрицательных весов
                'negative_mean': vd['negative_mean'],  # Среднее отрицательных
                'positive_percent': vd['positive_percent'],  # Процент положительных
                'negative_percent': vd['negative_percent'],  # Процент отрицательных
                'resistance_coeff': graph_data.resistance_coeff,  # Коэффициент устойчивости
                'influence_coeff': graph_data.influence_coeff,  # Коэффициент влияния
            })
        
        def sort_key(row):  # Ключ сортировки
            return (
                row['total_pct'],  # Общий процент сгораний
                row['step_pcts'][1],  # Процент на шаге 1
                row['step_pcts'][2],  # Процент на шаге 2
                row['step_pcts'][3],  # Процент на шаге 3
                row['step_pcts'][4],  # Процент на шаге 4
                row['step_pcts'][5],  # Процент на шаге 5
                row['vertex_weight']  # Вес вершины
            )
        
        rows.sort(key=sort_key, reverse=True)  # Сортировка по убыванию
        
        headers = [  # Заголовки таблицы
            self.app.translator.t('vuln_rank'),  # Ранг
            self.app.translator.t('vertex_number'),  # Номер вершины
            self.app.translator.t('vuln_total_percent'),  # Общий процент сгорания
            self.app.translator.t('vuln_step1_percent'),  # Процент на шаге 1
            self.app.translator.t('vuln_step2_percent'),  # Процент на шаге 2
            self.app.translator.t('vuln_step3_percent'),  # Процент на шаге 3
            self.app.translator.t('vuln_step4_percent'),  # Процент на шаге 4
            self.app.translator.t('vuln_step5_percent'),  # Процент на шаге 5
            self.app.translator.t('vertex_weight'),  # Вес вершины
            self.app.translator.t('avg_edge_weight'),  # Средний вес ребер
            self.app.translator.t('positive_count'),  # Количество положительных связей
            self.app.translator.t('positive_sum'),  # Сумма положительных весов
            self.app.translator.t('positive_mean'),  # Среднее положительных
            self.app.translator.t('negative_count'),  # Количество отрицательных связей
            self.app.translator.t('negative_sum'),  # Сумма отрицательных весов
            self.app.translator.t('negative_mean'),  # Среднее отрицательных
            self.app.translator.t('positive_percent'),  # Процент положительных
            self.app.translator.t('negative_percent'),  # Процент отрицательных
            self.app.translator.t('resistance_coeff'),  # Коэффициент устойчивости
            self.app.translator.t('influence_coeff'),  # Коэффициент влияния
        ]
        
        n_cols = len(headers)  # Количество колонок
        total_w = n_cols * cell_w  # Общая ширина
        total_h = (n_vertices + 1) * cell_h  # Общая высота
        visible_h = min(total_h, 21 * cell_h)  # Видимая высота
        table_container = self.app.widget_factory.create_frame(parent)  # Контейнер таблицы
        table_container.pack(fill='x', pady=(0, 20))  # Размещение
        table_container.grid_rowconfigure(0, weight=1)  # Растяжение строки
        table_container.grid_rowconfigure(1, weight=0)  # Фиксация строки
        table_container.grid_columnconfigure(0, weight=1)  # Растяжение колонки
        table_container.grid_columnconfigure(1, weight=0)  # Фиксация колонки
        main_canvas = tk.Canvas(table_container, bg=self.app.theme_manager.get_color('bg_color'),
                                highlightthickness=0, height=visible_h)# Холст для таблицы
        main_canvas.grid(row=0, column=0, sticky='nsew')  # Размещение
        v_scrollbar = self.app.widget_factory.create_scrollbar(table_container, orient='vertical',
                                                               command=main_canvas.yview)# Вертикальный скроллбар
        v_scrollbar.grid(row=0, column=1, sticky='ns')  # Размещение
        main_canvas.configure(yscrollcommand=v_scrollbar.set)  # Привязка
        h_scrollbar = self.app.widget_factory.create_scrollbar(table_container, orient='horizontal',
                                                               command=main_canvas.xview)# Горизонтальный скроллбар
        h_scrollbar.grid(row=1, column=0, sticky='ew')  # Размещение
        main_canvas.configure(xscrollcommand=h_scrollbar.set)  # Привязка
        main_canvas.configure(scrollregion=(0, 0, total_w, total_h))  # Область прокрутки
        header_font = self.app.widget_factory.get_font('table_cell')  # Шрифт заголовков
        header_bg = self.app.theme_manager.get_color('input_bg')  # Фон заголовков
        main_canvas.create_rectangle(0, 0, total_w, cell_h, fill=header_bg, outline='')  # Фон заголовков
        for col, header_text in enumerate(headers):  # Перебор заголовков
            x = col * cell_w + cell_w // 2  # X-координата
            main_canvas.create_text(x, cell_h // 2, text=header_text, font=header_font,
                                    fill=self.app.theme_manager.get_color('text_color'))# Текст заголовка
        cell_font = self.app.widget_factory.get_font('table_cell')  # Шрифт ячеек
        rounding = self.app.settings['rounding_stats'].get()  # Точность округления
        text_color_default = self.app.theme_manager.get_color('text_color')  # Цвет текста по умолчанию
        
        for row_idx, row_data in enumerate(rows):  # Перебор строк данных
            y = (row_idx + 1) * cell_h  # Y-координата
            bg_color = self.app.theme_manager.get_color('bg_color') if row_idx % 2 == 0 else self.app.theme_manager.get_color('input_bg')
            values = [  # Значения ячеек
                str(row_idx + 1),  # Ранг
                str(row_data['vertex_idx'] + 1),  # Номер вершины
                f"{row_data['total_pct']:.{rounding}f}%",  # Общий процент
                f"{row_data['step_pcts'][1]:.{rounding}f}%",  # Процент на шаге 1
                f"{row_data['step_pcts'][2]:.{rounding}f}%",  # Процент на шаге 2
                f"{row_data['step_pcts'][3]:.{rounding}f}%",  # Процент на шаге 3
                f"{row_data['step_pcts'][4]:.{rounding}f}%",  # Процент на шаге 4
                f"{row_data['step_pcts'][5]:.{rounding}f}%",  # Процент на шаге 5
                f"{row_data['vertex_weight']:.{rounding}f}",  # Вес вершины
                f"{row_data['avg_edge_weight']:.{rounding}f}",  # Средний вес ребер
                str(row_data['positive_count']),  # Количество положительных
                f"{row_data['positive_sum']:.{rounding}f}",  # Сумма положительных
                f"{row_data['positive_mean']:.{rounding}f}",  # Среднее положительных
                str(row_data['negative_count']),  # Количество отрицательных
                f"{row_data['negative_sum']:.{rounding}f}",  # Сумма отрицательных
                f"{row_data['negative_mean']:.{rounding}f}",  # Среднее отрицательных
                f"{row_data['positive_percent']:.{rounding}f}%",  # Процент положительных
                f"{row_data['negative_percent']:.{rounding}f}%",  # Процент отрицательных
                f"{row_data['resistance_coeff']:.{rounding}f}",  # Коэффициент устойчивости
                f"{row_data['influence_coeff']:.{rounding}f}",  # Коэффициент влияния
            ]
            
            main_canvas.create_rectangle(0, y, total_w, y + cell_h, fill=bg_color, outline='')  # Фон строки
            for col, value in enumerate(values):  # Перебор значений
                x = col * cell_w + cell_w // 2  # X-координата
                if col == 0:  # Колонка ранга
                    pct = row_data['total_pct']  # Процент сгораний
                    if pct >= 80:  # Высокая уязвимость
                        text_color = self.COLOR_MAX_HEX  # Красный
                    elif pct > 20:  # Средняя уязвимость
                        text_color = self.COLOR_MID_HEX  # Золотистый
                    else:  # Низкая уязвимость
                        text_color = self.COLOR_MIN_HEX  # Зеленый
                else:  # Остальные колонки
                    text_color = text_color_default  # Обычный цвет
                main_canvas.create_text(x, y + cell_h // 2, text=value, font=cell_font, fill=text_color)# Текст ячейки


# In[37]:


class Tab:
    """Абстрактный базовый класс для всех вкладок приложения"""
    
    def __init__(self, parent, app):
        """Инициализация базовой вкладки с родительским виджетом и приложением"""
        self.parent = parent  # Родительский виджет
        self.app = app  # Экземпляр главного приложения
        self.tab_key = 'tab_unknown'  # Ключ вкладки (должен быть переопределен в наследнике)
        self.frame = app.widget_factory.create_frame(parent)  # Основной фрейм вкладки
        self.frame.pack(fill='both', expand=True)  # Размещение с растяжением
        self._saved_state = None  # Сохраненное состояние вкладки
    
    def build(self):
        """Создание интерфейса вкладки (должен быть переопределен в наследнике)"""
        raise NotImplementedError("Метод build() должен быть реализован в наследнике")  # Обязательная реализация
    
    def on_activate(self):
        """Вызов при активации вкладки (переключении на нее)"""
        pass  # Переопределяется при необходимости
    
    def on_deactivate(self):
        """Вызов при деактивации вкладки (переключении на другую)"""
        pass  # Переопределяется при необходимости
    
    def refresh(self):
        """Полное перестроение вкладки при смене языка или темы"""
        self.save_state()  # Сохранение состояния перед перестроением
        self.save_ui_to_data()  # Сохранение ui данных в модель
        for widget in self.frame.winfo_children():  # Удаление всех дочерних виджетов
            widget.destroy()
        self.build()  # Перестроение интерфейса
        self.load_data_to_ui()  # Загрузка данных из модели в ui
        self.restore_state()  # Восстановление сохраненного состояния
    
    def save_state(self):
        """Сохранение состояния вкладки перед refresh (переопределяется при необходимости)"""
        self._saved_state = None  # Сброс сохраненного состояния по умолчанию
    
    def restore_state(self):
        """Восстановление состояния вкладки после refresh (переопределяется при необходимости)"""
        pass  # Переопределяется при необходимости
    
    def save_ui_to_data(self):
        """Сохранение данных из ui в self.data (переопределяется при необходимости)"""
        pass  # Переопределяется при необходимости
    
    def load_data_to_ui(self):
        """Загрузка данных из self.data в ui (переопределяется при необходимости)"""
        pass  # Переопределяется при необходимости


# In[38]:


class GraphTab(Tab):
    """Базовый класс для вкладок, работающих с данными графа"""
    
    def __init__(self, parent, app):
        """Инициализация вкладки графа с ссылками на виджеты отображения"""
        super().__init__(parent, app)  # Вызов конструктора родительского класса
        self.data = None  # Объект GraphData с данными графа
        self.graph_display = None  # Ссылка на виджет отображения графа
        self.edge_hist = None  # Ссылка на гистограмму ребер
        self.vertex_hist = None  # Ссылка на гистограмму вершин
        self._saved_state = None  # Сохраненное состояние для восстановления
    
    def _get_source_data(self):
        """Получение данных для вставки в другую вкладку (должен быть переопределен в наследнике)"""
        raise NotImplementedError("Метод _get_source_data() должен быть реализован в наследнике")  # Обязательная реализация
    
    def _confirm_insert(self, confirm_key):
        """Показ диалога подтверждения вставки графа"""
        return tk.messagebox.askyesno(  # Диалог с кнопками да/нет
            self.app.translator.t('confirm_title'),  # Заголовок диалога
            self.app.translator.t(confirm_key)  # Текст вопроса
        )
    
    def _do_insert(self, tab_index, data, setter_method):
        """Выполнение вставки данных и переключение на указанную вкладку"""
        setter_method(data)  # Установка данных через метод приложения
        self.app.tab_manager.activate_tab(tab_index)  # Активация целевой вкладки
    
    def insert_to_tab(self, tab_index, confirm_key, setter_method):
        """Универсальный метод вставки графа в другую вкладку с подтверждением"""
        if self.app.is_copying:  # Предотвращение рекурсивного копирования
            return
        
        if not self._confirm_insert(confirm_key):  # Отмена пользователем
            return
        
        self.save_ui_to_data()  # Сохранение текущих ui данных в модель
        source_data = self._get_source_data()  # Получение данных для вставки
        self._do_insert(tab_index, source_data, setter_method)  # Выполнение вставки
    
    def refresh_display(self):
        """Полное обновление отображения вкладки (переопределяется в наследнике)"""
        pass  # Переопределяется при необходимости
    
    def refresh_graph(self):
        """Обновление только отображения графа"""
        if self.graph_display:  # Виджет графа существует
            self.graph_display.draw()  # Перерисовка графа
    
    def refresh_histograms(self):
        """Обновление гистограмм ребер и вершин"""
        if self.edge_hist and self.data and self.data.graph.number_of_nodes() > 0:  # Гистограмма ребер существует
            edge_weights = [d['weight'] for _, _, d in self.data.graph.edges(data=True)]  # Сбор весов ребер
            if edge_weights:  # Есть данные
                self.edge_hist.update(edge_weights)  # Обновление гистограммы
            else:  # Нет данных
                self.edge_hist.clear()  # Очистка гистограммы
        
        if self.vertex_hist and self.data and self.data.graph.number_of_nodes() > 0:  # Гистограмма вершин существует
            vertex_weights = self.data.get_all_vertices()  # Сбор весов вершин
            if vertex_weights:  # Есть данные
                self.vertex_hist.update(vertex_weights)  # Обновление гистограммы
            else:  # Нет данных
                self.vertex_hist.clear()  # Очистка гистограммы
    
    def on_data_changed(self, change_type, **kwargs):
        """Обработчик изменений данных графа (переопределяется в наследнике)"""
        pass  # Переопределяется при необходимости

    def save_state(self):
        """Сохранение состояния вкладки перед refresh"""
        self._saved_state = {  # Сохранение только данных графа
            'data': self.data.copy() if self.data else None,  # Копия данных графа
            'graph_display': None,  # Виджет не сохраняется (пересоздастся)
            'edge_hist': None,  # Гистограмма не сохраняется (пересоздастся)
            'vertex_hist': None,  # Гистограмма не сохраняется (пересоздастся)
        }
    
    def restore_state(self):
        """Восстановление состояния вкладки после refresh"""
        if self._saved_state and self._saved_state.get('data'):  # Сохраненные данные существуют
            self.data = self._saved_state['data']  # Восстановление данных графа
            self.load_data_to_ui()  # Загрузка данных в ui
            self.refresh_display()  # Обновление отображения


# In[39]:


class TabManager:
    """Менеджер вкладок приложения"""
    
    def __init__(self, parent, app):
        """Инициализация менеджера вкладок с панелью и областью контента"""
        self.parent = parent  # Родительский виджет
        self.app = app  # Экземпляр главного приложения
        self.tabs = []  # Список кнопок вкладок
        self.frames = []  # Список фреймов контента вкладок
        self.tab_instances = []  # Список экземпляров классов вкладок
        self.active_index = 0  # Индекс активной вкладки
        self.active_tab = None  # Активный экземпляр вкладки
        self.tab_classes = []  # Список классов вкладок
        self.tab_keys = []  # Список ключей перевода для вкладок
        self.switching_blocked = False  # Флаг блокировки переключения вкладок
        self.main = app.widget_factory.create_frame(parent)  # Основной контейнер
        self.main.pack(fill='both', expand=True)  # Размещение с растяжением
        self.tab_bar = app.widget_factory.create_frame(self.main, height=app.size_config['container']['tab_bar']['height'])  # Панель вкладок
        self.tab_bar.pack(fill='x', side='top', padx=5, pady=0)  # Размещение сверху
        self.tab_bar.pack_propagate(False)  # Запрет изменения размера
        self.content = app.widget_factory.create_frame(self.main)  # Область контента
        self.content.pack(fill='both', expand=True, side='top', padx=10, pady=0)  # Размещение
        self.content.pack_propagate(False)  # Запрет изменения размера
    
    def add_tab(self, tab_class, tab_key):
        """Добавление вкладки для регистрации без создания экземпляра"""
        idx = len(self.tabs)  # Индекс новой вкладки
        btn_frame = self.app.widget_factory.create_frame(self.tab_bar)  # Фрейм кнопки вкладки
        btn_frame.pack(side='left', padx=(0, 1), pady=0, fill='both', expand=True)  # Размещение
        inner = self.app.widget_factory.create_frame(btn_frame)  # Внутренний фрейм для отступов
        inner.pack(fill='both', expand=True, padx=1, pady=1)  # Размещение
        btn = tk.Label(inner, text=self.app.translator.t(tab_key), bg=self.app.theme_manager.get_color('tab1_inactive'),
                       fg=self.app.theme_manager.get_color('text_color'), font=self.app.widget_factory.get_font('tab')) # Метка-кнопка вкладки
        btn.pack(fill='both', expand=True, padx=20, pady=0)  # Размещение
        btn_frame.inner = inner  # Сохранение внутреннего фрейма
        btn_frame.btn = btn  # Сохранение метки-кнопки
        btn_frame.tab_key = tab_key  # Сохранение ключа вкладки
        btn_frame.index = idx  # Сохранение индекса
        def on_click(e, i=idx):  # Обработчик клика
            if not self.switching_blocked:  # Переключение не заблокировано
                self.activate_tab(i)  # Активация вкладки
        btn.bind('<Button-1>', on_click)  # Привязка клика к метке
        inner.bind('<Button-1>', on_click)  # Привязка клика к внутреннему фрейму
        btn_frame.bind('<Button-1>', on_click)  # Привязка клика к внешнему фрейму
        tab_frame = self.app.widget_factory.create_frame(self.content)  # Фрейм для контента вкладки
        self.tabs.append(btn_frame)  # Добавление кнопки в список
        self.frames.append(tab_frame)  # Добавление фрейма в список
        self.tab_classes.append(tab_class)  # Добавление класса в список
        self.tab_keys.append(tab_key)  # Добавление ключа в список
        self.tab_instances.append(None)  # Заглушка для экземпляра
    
    def create_all_tabs(self):
        """Создание всех вкладок сразу после регистрации"""
        for i, tab_class in enumerate(self.tab_classes):  # Перебор зарегистрированных классов
            if self.tab_instances[i] is None:  # Экземпляр еще не создан
                instance = tab_class(self.frames[i], self.app)  # Создание экземпляра вкладки
                instance.build()  # Построение интерфейса вкладки
                self.tab_instances[i] = instance  # Сохранение экземпляра
                self.frames[i].pack_forget()  # Скрытие фрейма (пока не активен)
    
    def activate_tab(self, index):
        """Активация вкладки с указанным индексом"""
        if self.switching_blocked:  # Переключение заблокировано
            return
        if self.active_index < len(self.tab_instances) and self.tab_instances[self.active_index] is not None:  # Существующая активная вкладка
            self.tab_instances[self.active_index].on_deactivate()  # Вызов деактивации
            self.frames[self.active_index].pack_forget()  # Скрытие фрейма
        self.frames[index].pack(fill='both', expand=True)  # Показ нового фрейма
        self.content.update_idletasks()  # Обновление геометрии
        self.frames[index].update_idletasks()  # Обновление геометрии фрейма
        self.active_tab = self.tab_instances[index]  # Сохранение активной вкладки
        if self.active_tab is not None:  # Вкладка существует
            self.active_tab.on_activate()  # Вызов активации
        content_width = self.content.winfo_width()  # Ширина области контента
        content_height = self.content.winfo_height()  # Высота области контента
        if content_width > 1 and content_height > 1:  # Корректные размеры
            self.frames[index].config(width=content_width, height=content_height)  # Установка размеров фрейма
        self._update_tab_colors(index)  # Обновление цветов вкладок
        self.active_index = index  # Сохранение активного индекса
    
    def _update_tab_colors(self, active_index):
        """Обновление цветов кнопок вкладок в зависимости от активности"""
        for i, tab in enumerate(self.tabs):  # Перебор всех вкладок
            if i == active_index:  # Активная вкладка
                tab_num = i + 1  # Номер вкладки (1-индексация)
                color_key = f'tab{tab_num}_active'  # Ключ активного цвета
                color = self.app.theme_manager.get_color(color_key)  # Получение цвета
                text_color = self.app.theme_manager.get_color('text_color')  # Цвет текста
            else:  # Неактивная вкладка
                tab_num = i + 1  # Номер вкладки (1-индексация)
                color_key = f'tab{tab_num}_inactive'  # Ключ неактивного цвета
                color = self.app.theme_manager.get_color(color_key)  # Получение цвета
                text_color = self.app.theme_manager.get_color('text_color')  # Цвет текста
            tab.configure(bg=color)  # Обновление фона внешнего фрейма
            tab.inner.configure(bg=color)  # Обновление фона внутреннего фрейма
            tab.btn.configure(bg=color, fg=text_color)  # Обновление фона и текста метки
    
    def refresh_all(self):
        """Полное пересоздание всех вкладок при смене языка или темы"""
        ScrollableFrame._all_scrolls.clear()  # Очистка списка скроллов
        self.main.configure(bg=self.app.theme_manager.get_color('bg_color'))  # Обновление фона основного контейнера
        self.tab_bar.configure(bg=self.app.theme_manager.get_color('bg_color'))  # Обновление фона панели вкладок
        self.content.configure(bg=self.app.theme_manager.get_color('bg_color'))  # Обновление фона области контента
        active_index = self.active_index  # Сохранение индекса активной вкладки
        for tab in self.tabs:  # Обновление фона всех кнопок вкладок
            tab.configure(bg=self.app.theme_manager.get_color('bg_color'))
        saved_states = []  # Список сохраненных состояний
        for instance in self.tab_instances:  # Перебор экземпляров вкладок
            if instance is not None:  # Экземпляр существует
                instance.save_state()  # Сохранение состояния
                saved_states.append(instance._saved_state)  # Добавление в список
            else:  # Экземпляр отсутствует
                saved_states.append(None)  # Заглушка
        for i, frame in enumerate(self.frames):  # Перебор фреймов вкладок
            for widget in frame.winfo_children():  # Перебор дочерних виджетов
                try:
                    widget.destroy()  # Уничтожение виджета
                except:
                    pass  # Игнорирование ошибок
        self.tab_instances = []  # Сброс списка экземпляров
        for i, tab_class in enumerate(self.tab_classes):  # Перебор классов вкладок
            instance = tab_class(self.frames[i], self.app)  # Создание экземпляра вкладки
            instance.build()  # Построение интерфейса
            if saved_states[i] is not None:  # Сохраненное состояние существует
                instance._saved_state = saved_states[i]  # Восстановление сохраненного состояния
                instance.restore_state()  # Восстановление состояния
            self.tab_instances.append(instance)  # Добавление в список
            self.frames[i].pack_forget()  # Скрытие фрейма
        for i, tab in enumerate(self.tabs):  # Перебор кнопок вкладок
            new_text = self.app.translator.t(self.tab_keys[i])  # Новый переведенный текст
            tab.btn.configure(text=new_text)  # Обновление текста кнопки
        self.activate_tab(active_index)  # Активация предыдущей вкладки

    def block_switching(self):
        """Блокировка переключения вкладок (без изменения цветов)"""
        self.switching_blocked = True  # Установка флага блокировки
    
    def unblock_switching(self):
        """Разблокировка переключения вкладок"""
        self.switching_blocked = False  # Сброс флага блокировки


# In[40]:


class GenerationTab(GraphTab):
    """Вкладка генерации графа"""
    
    tab_key = 'tab_generation'  # Ключ для перевода названия вкладки
    
    def __init__(self, parent, app):
        """Инициализация вкладки генерации с ui переменными и виджетами"""
        super().__init__(parent, app)  # Вызов конструктора родительского класса
        self.data = app.generation_data  # Данные графа для этой вкладки
        self.param_factory = ParameterSectionFactory(app)  # Фабрика секций параметров
        self.ui_vars = {  # Ui переменные для параметров графа
            'vertex_count': tk.IntVar(value=50),  # Количество вершин
            'edge_distribution': tk.StringVar(value='Uniform'),  # Тип распределения ребер
            'vertex_distribution': tk.StringVar(value='None'),  # Тип распределения вершин
            
            'edge_uniform_left': tk.DoubleVar(value=-0.6),  # Левая граница равномерного распределения ребер
            'edge_uniform_right': tk.DoubleVar(value=0.6),  # Правая граница равномерного распределения ребер
            'edge_normal_mean': tk.DoubleVar(value=0.3),  # Среднее нормального распределения ребер
            'edge_normal_std': tk.DoubleVar(value=0.5),  # Стандартное отклонение нормального распределения ребер
            'edge_student_df': tk.DoubleVar(value=10.0),  # Степени свободы распределения Стьюдента ребер
            'edge_student_scale': tk.DoubleVar(value=0.5),  # Масштаб распределения Стьюдента ребер
            'edge_laplace_loc': tk.DoubleVar(value=0.0),  # Параметр сдвига распределения Лапласа ребер
            'edge_laplace_scale': tk.DoubleVar(value=0.5),  # Параметр масштаба распределения Лапласа ребер
            'edge_bimodal_mu1': tk.DoubleVar(value=-0.5),  # Среднее первой компоненты бимодального распределения ребер
            'edge_bimodal_sigma1': tk.DoubleVar(value=0.2),  # Стандартное отклонение первой компоненты бимодального распределения ребер
            'edge_bimodal_mu2': tk.DoubleVar(value=0.5),  # Среднее второй компоненты бимодального распределения ребер
            'edge_bimodal_sigma2': tk.DoubleVar(value=0.2),  # Стандартное отклонение второй компоненты бимодального распределения ребер
            'edge_bimodal_weight': tk.DoubleVar(value=0.5),  # Вес первой компоненты бимодального распределения ребер
            'edge_skewed_t_df': tk.DoubleVar(value=10.0),  # Степени свободы скошенного t-распределения ребер
            'edge_skewed_t_shape': tk.DoubleVar(value=0.0),  # Параметр формы скошенного t-распределения ребер
            'edge_skewed_t_scale': tk.DoubleVar(value=0.5),  # Масштаб скошенного t-распределения ребер
            
            'vertex_uniform_left': tk.DoubleVar(value=0.2),  # Левая граница равномерного распределения вершин
            'vertex_uniform_right': tk.DoubleVar(value=0.6),  # Правая граница равномерного распределения вершин
            'vertex_normal_mean': tk.DoubleVar(value=0.5),  # Среднее нормального распределения вершин
            'vertex_normal_std': tk.DoubleVar(value=0.2),  # Стандартное отклонение нормального распределения вершин
            'vertex_lognormal_gamma': tk.DoubleVar(value=0.0),  # Параметр сдвига логнормального распределения вершин
            'vertex_lognormal_mu': tk.DoubleVar(value=-1.0),  # Среднее логарифма логнормального распределения вершин
            'vertex_lognormal_sigma': tk.DoubleVar(value=0.5),  # Стандартное отклонение логарифма логнормального распределения вершин
            'vertex_bimodal_mu1': tk.DoubleVar(value=0.2),  # Среднее первой компоненты бимодального распределения вершин
            'vertex_bimodal_sigma1': tk.DoubleVar(value=0.1),  # Стандартное отклонение первой компоненты бимодального распределения вершин
            'vertex_bimodal_mu2': tk.DoubleVar(value=0.8),  # Среднее второй компоненты бимодального распределения вершин
            'vertex_bimodal_sigma2': tk.DoubleVar(value=0.1),  # Стандартное отклонение второй компоненты бимодального распределения вершин
            'vertex_bimodal_weight': tk.DoubleVar(value=0.5),  # Вес первой компоненты бимодального распределения вершин
            
            'resistance_type': tk.StringVar(value='None'),  # Тип устойчивости
            'resistance_coeff': tk.DoubleVar(value=0.5),  # Коэффициент устойчивости
            'influence_type': tk.StringVar(value='None'),  # Тип влияния
            'influence_coeff': tk.DoubleVar(value=0.5),  # Коэффициент влияния
            'damping_type': tk.StringVar(value='None'),  # Тип затухания
            'damping_coeff': tk.DoubleVar(value=0.5),  # Коэффициент затухания
            'resistance_display': tk.StringVar(value=self.app.translator.t('None')),  # Отображение типа устойчивости
            'influence_display': tk.StringVar(value=self.app.translator.t('None')),  # Отображение типа влияния
            'damping_display': tk.StringVar(value=self.app.translator.t('None')),  # Отображение типа затухания
        }
        
        self.edge_plot = None  # Виджет графика плотности ребер
        self.vertex_plot = None  # Виджет графика плотности вершин
        self.edge_params_container = None  # Контейнер параметров ребер
        self.vertex_params_container = None  # Контейнер параметров вершин
        self.edge_combo = None  # Комбобокс типа распределения ребер
        self.vertex_combo = None  # Комбобокс типа распределения вершин
        self.resistance_section = None  # Секция устойчивости
        self.influence_section = None  # Секция влияния
        self.damping_section = None  # Секция затухания
        self.vertex_props_container = None  # Контейнер дополнительных свойств вершин
        self.vertex_plot_frame = None  # Фрейм для графика плотности вершин
        self.vertex_slider = None  # Слайдер количества вершин
    
    def load_data_to_ui(self):
        """Загрузка данных из self.data в ui переменные"""
        self.ui_vars['resistance_type'].set(self.data.resistance_type)  # Восстановление типа устойчивости
        self.ui_vars['resistance_coeff'].set(self.data.resistance_coeff)  # Восстановление коэффициента устойчивости
        self.ui_vars['influence_type'].set(self.data.influence_type)  # Восстановление типа влияния
        self.ui_vars['influence_coeff'].set(self.data.influence_coeff)  # Восстановление коэффициента влияния
        self.ui_vars['damping_type'].set(self.data.damping_type)  # Восстановление типа затухания
        self.ui_vars['damping_coeff'].set(self.data.damping_coeff)  # Восстановление коэффициента затухания
        self.ui_vars['resistance_display'].set(self.app.translator.t(self.data.resistance_type))  # Восстановление отображения устойчивости
        self.ui_vars['influence_display'].set(self.app.translator.t(self.data.influence_type))  # Восстановление отображения влияния
        self.ui_vars['damping_display'].set(self.app.translator.t(self.data.damping_type))  # Восстановление отображения затухания
    
    def save_ui_to_data(self):
        """Сохранение ui переменных в self.data"""
        self.data.resistance_type = self.ui_vars['resistance_type'].get()  # Сохранение типа устойчивости
        self.data.resistance_coeff = self.ui_vars['resistance_coeff'].get()  # Сохранение коэффициента устойчивости
        self.data.influence_type = self.ui_vars['influence_type'].get()  # Сохранение типа влияния
        self.data.influence_coeff = self.ui_vars['influence_coeff'].get()  # Сохранение коэффициента влияния
        self.data.damping_type = self.ui_vars['damping_type'].get()  # Сохранение типа затухания
        self.data.damping_coeff = self.ui_vars['damping_coeff'].get()  # Сохранение коэффициента затухания
    
    def build(self):
        """Создание интерфейса вкладки генерации графа"""
        scroll = ScrollableFrame(self.frame, self.app.widget_factory)  # Прокручиваемый фрейм
        scroll.pack(fill='both', expand=True)  # Размещение с растяжением
        content = scroll.inner  # Внутренний контент
        content.columnconfigure(0, weight=1)  # Растяжение колонки
        main_container = self.app.widget_factory.create_frame(content)  # Главный контейнер
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)  # Размещение с отступами
        main_container.columnconfigure(0, weight=1)  # Растяжение колонки
        current_row = 0  # Текущая строка сетки
        
        vertex_count_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'vertex_count')  # Секция количества вершин
        pair_frame, entry, scale = vertex_count_section.add_row(  # Добавление строки с полем и слайдером
            label_key='vertex_count',  # Ключ лейбла
            variable=self.ui_vars['vertex_count'],  # Переменная количества вершин
            param_name='vertex_count',  # Имя параметра
            dist_type='global',  # Тип распределения (глобальный параметр)
            domain='global',  # Домен параметра
            show_label=False,  # Скрытие лейбла
            scale_size='long'  # Длинный слайдер
        )
        self.vertex_slider = scale  # Сохранение ссылки на слайдер
        vertex_count_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение секции
        current_row += 1  # Увеличение счетчика строк
        
        edge_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'edge_distribution')  # Секция распределения ребер
        edge_top = self.app.widget_factory.create_frame(edge_section.content)  # Верхняя часть секции
        edge_top.pack(fill='x')  # Упаковка верхней части
        
        edge_keys = ['Uniform', 'Normal', 'Student', 'Laplace', 'Bimodal', 'Skewed_t', 'Stepwise']  # Ключи типов распределений ребер
        translated_edge_keys = [self.app.translator.t(key) for key in edge_keys]  # Перевод ключей
        
        edge_display_var = tk.StringVar()  # Переменная для отображения в комбобоксе
        current_edge_value = self.ui_vars['edge_distribution'].get()  # Текущее значение типа распределения
        edge_display_var.set(self.app.translator.t(current_edge_value))  # Установка отображаемого значения
        
        self.edge_combo = self.app.widget_factory.create_combobox(edge_top,
                                                translated_edge_keys, edge_display_var, size='default')  # Комбобокс выбора типа
        self.edge_combo.pack(side='left', padx=(0, 20))  # Размещение с отступом справа
        
        def on_edge_combo_change(*args):  # Обработчик изменения комбобокса
            display_value = edge_display_var.get()  # Получение отображаемого значения
            original_value = self.app.translator.to_key(display_value)  # Получение оригинального ключа
            self.ui_vars['edge_distribution'].set(original_value)  # Установка типа распределения
            self.on_edge_dist_change()  # Обновление параметров распределения
        
        edge_display_var.trace_add('write', on_edge_combo_change)  # Отслеживание изменений переменной
        
        self.edge_plot = DistributionPlot(edge_top, self.app.widget_factory,
                                          x_range=(-1, 1), color_key='edge_density_color')  # График плотности ребер
        self.edge_plot.pack(side='left')  # Размещение графика
        
        self.edge_params_container = self.app.widget_factory.create_frame(edge_section.content)  # Контейнер параметров ребер
        self.edge_params_container.pack(fill='x', pady=(30, 0))  # Размещение с отступом сверху
        edge_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение секции
        current_row += 1  # Увеличение счетчика строк
        
        vertex_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'vertex_distribution')  # Секция распределения вершин
        vertex_top = self.app.widget_factory.create_frame(vertex_section.content)  # Верхняя часть секции
        vertex_top.pack(fill='x')  # Упаковка верхней части
        
        vertex_keys = ['None', 'Uniform', 'Normal', 'Lognormal', 'Bimodal', 'Stepwise']  # Ключи типов распределений вершин
        translated_vertex_keys = [self.app.translator.t(key) for key in vertex_keys]  # Перевод ключей
        
        vertex_display_var = tk.StringVar()  # Переменная для отображения в комбобоксе
        current_vertex_value = self.ui_vars['vertex_distribution'].get()  # Текущее значение типа распределения
        vertex_display_var.set(self.app.translator.t(current_vertex_value))  # Установка отображаемого значения
        
        self.vertex_combo = self.app.widget_factory.create_combobox(vertex_top, translated_vertex_keys,
                                                                    vertex_display_var, size='default')  # Комбобокс выбора типа
        self.vertex_combo.pack(side='left', padx=(0, 20))  # Размещение с отступом справа
        
        def on_vertex_combo_change(*args):  # Обработчик изменения комбобокса
            display_value = vertex_display_var.get()  # Получение отображаемого значения
            original_value = self.app.translator.to_key(display_value)  # Получение оригинального ключа
            self.ui_vars['vertex_distribution'].set(original_value)  # Установка типа распределения
            self.on_vertex_dist_change()  # Обновление параметров распределения
        
        vertex_display_var.trace_add('write', on_vertex_combo_change)  # Отслеживание изменений переменной
        
        self.vertex_plot_frame = self.app.widget_factory.create_frame(vertex_top)  # Фрейм для графика плотности вершин
        self.vertex_plot = DistributionPlot(self.vertex_plot_frame, self.app.widget_factory,
                                            x_range=(0, 1), color_key='vertex_density_color')  # График плотности вершин
        self.vertex_plot.pack(side='left')  # Размещение графика
        
        self.vertex_params_container = self.app.widget_factory.create_frame(vertex_section.content)  # Контейнер параметров вершин
        self.vertex_params_container.pack(fill='x', pady=(30, 0))  # Размещение с отступом сверху
        
        self.vertex_props_container = self.app.widget_factory.create_frame(vertex_section.content)  # Контейнер дополнительных свойств
        self.vertex_props_container.pack(fill='x', pady=(0, 0))  # Размещение
        
        self.resistance_section, _, _, _ = self.param_factory.create_section('resistance',
                                                self.vertex_props_container, self.ui_vars, 'field')  # Секция устойчивости
        self.resistance_section.frame.pack(fill='x')  # Размещение секции
        
        self.influence_section, _, _, _ = self.param_factory.create_section('influence',
                                                self.vertex_props_container, self.ui_vars, 'field')  # Секция влияния
        self.influence_section.frame.pack(fill='x', pady=5)  # Размещение секции с отступом
        
        vertex_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение секции
        current_row += 1  # Увеличение счетчика строк
        
        props_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'additional_properties')  # Секция дополнительных свойств
        
        self.damping_section, _, _, _ = self.param_factory.create_section('damping',
                                                props_section.content, self.ui_vars, 'field')  # Секция затухания
        self.damping_section.frame.pack(fill='x')  # Размещение секции
        
        props_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение секции
        current_row += 1  # Увеличение счетчика строк
        
        btn_group = self.app.size_config['container']['button_group']  # Конфигурация группы кнопок
        buttons_container = self.app.widget_factory.create_frame(main_container, height=btn_group['height'])  # Контейнер для кнопок
        buttons_container.grid(row=current_row, column=0, sticky='ew', padx=150, pady=(0, 100))  # Размещение с отступами
        buttons_container.grid_propagate(False)  # Запрет изменения размера
        buttons_container.columnconfigure(0, weight=1)  # Растяжение колонки
        
        buttons_frame = self.app.widget_factory.create_frame(buttons_container)  # Фрейм для кнопок
        buttons_frame.pack(fill='x', expand=True)  # Размещение с растяжением
        buttons_frame.columnconfigure(0, weight=1)  # Растяжение первой колонки
        buttons_frame.columnconfigure(1, weight=1)  # Растяжение второй колонки
        buttons_frame.columnconfigure(2, weight=1)  # Растяжение третьей колонки
        
        btn1 = self.app.widget_factory.create_button(buttons_frame, 'insert_into_custom',
                                                     self.insert_into_custom, 'insert_custom')  # Кнопка вставки в пользовательский граф
        btn1.grid(row=0, column=0, padx=30, pady=10, sticky='ew')  # Размещение кнопки
        btn2 = self.app.widget_factory.create_button(buttons_frame, 'insert_into_simulation',
                                                     self.insert_into_simulation, 'insert_sim')  # Кнопка вставки в симуляцию
        btn2.grid(row=0, column=1, padx=30, pady=10, sticky='ew')  # Размещение кнопки
        btn3 = self.app.widget_factory.create_button(buttons_frame, 'insert_into_multiple',
                                                     self.insert_into_multiple, 'insert_multi')  # Кнопка вставки в множественную симуляцию
        btn3.grid(row=0, column=2, padx=30, pady=10, sticky='ew')  # Размещение кнопки
        
        def on_edge_state_change(*args):  # Обработчик изменения состояния типа ребер
            new_value = self.ui_vars['edge_distribution'].get()  # Получение нового значения
            edge_display_var.trace_remove('write', edge_display_var.trace_info()[0][1])  # Удаление старого trace
            edge_display_var.set(self.app.translator.t(new_value))  # Установка отображаемого значения
            edge_display_var.trace_add('write', on_edge_combo_change)  # Добавление нового trace
        
        def on_vertex_state_change(*args):  # Обработчик изменения состояния типа вершин
            new_value = self.ui_vars['vertex_distribution'].get()  # Получение нового значения
            vertex_display_var.trace_remove('write', vertex_display_var.trace_info()[0][1])  # Удаление старого trace
            vertex_display_var.set(self.app.translator.t(new_value))  # Установка отображаемого значения
            vertex_display_var.trace_add('write', on_vertex_combo_change)  # Добавление нового trace
        
        self.ui_vars['edge_distribution'].trace_add('write', on_edge_state_change)  # Отслеживание изменений типа ребер
        self.ui_vars['vertex_distribution'].trace_add('write', on_vertex_state_change)  # Отслеживание изменений типа вершин
        self.on_edge_dist_change()  # Инициализация параметров ребер
        self.on_vertex_dist_change()  # Инициализация параметров вершин
    
    def on_edge_dist_change(self, *args):
        """Обработчик изменения типа распределения ребер"""
        dist_type = self.ui_vars['edge_distribution'].get()  # Текущий тип распределения
        domain = 'edge'  # Домен для конфигурации
        for widget in self.edge_params_container.winfo_children():  # Очистка контейнера параметров
            widget.destroy()  # Уничтожение виджета
        if dist_type == 'Stepwise':  # Ступенчатое распределение
            if not self.app.tier_manager.get_edge_config():  # Конфигурация ступеней не установлена
                preset_data = EDGE_TIER_PRESETS.get('uniform_preset', {}).get(6)  # Пресет из 6 ступеней
                if preset_data:  # Пресет найден
                    bounds = preset_data['bounds']  # Границы ступеней
                    counts = preset_data['counts']  # Количество элементов в ступенях
                    stages = [{'left': left, 'right': right, 'weight': count} for (left, right), count in zip(bounds, counts)]  # Список ступеней
                    self.app.tier_manager.set_edge_stages(stages)  # Установка ступеней в менеджер
            StepwiseWidget(self.edge_params_container, self.app,
                           domain, self.app.tier_manager, self.edge_plot, lambda: None).frame.pack(fill='x')  # Виджет ступеней
            return
        
        cfg = PARAM_CONFIG[domain][dist_type]  # Конфигурация распределения
        sec = AlignedSection(self.edge_params_container, self.app.widget_factory, self.app)  # Секция параметров
        vars_ = [self.ui_vars[f'{domain}_{dist_type}_{p}'.lower()] for p in cfg['param_order']]  # Переменные параметров
        if cfg['ui_type'] == 'dual':  # Двойной тип ui (левый и правый слайдер)
            sec.add_dual_row('left', 'right', vars_[0], vars_[1], 'left', 'right', dist_type, domain)  # Двойная строка
        else:  # Обычный тип ui
            for p, v in zip(cfg['param_order'], vars_):  # Перебор параметров
                sec.add_row(label_key=p, variable=v, param_name=p, dist_type=dist_type, domain=domain)  # Обычная строка
        sec.frame.pack(fill='x')  # Размещение секции
        plot_vars = {p: v for p, v in zip(cfg['param_order'], vars_)}  # Словарь для графика
        update = lambda *a: cfg['plot_update'](self.edge_plot, plot_vars)  # Функция обновления графика
        for v in vars_:  # Перебор переменных
            v.trace_add('write', update)  # Отслеживание изменений
        update()  # Первоначальное обновление графика
    
    def on_vertex_dist_change(self, *args):
        """Обработчик изменения типа распределения вершин"""
        dist_type = self.ui_vars['vertex_distribution'].get()  # Текущий тип распределения
        domain = 'vertex'  # Домен для конфигурации
        for widget in self.vertex_params_container.winfo_children():  # Очистка контейнера параметров
            widget.destroy()  # Уничтожение виджета
        if dist_type == 'None':  # Распределение отсутствует
            self.vertex_plot_frame.pack_forget()  # Скрытие фрейма графика
            self.vertex_props_container.pack_forget()  # Скрытие контейнера свойств
            self.ui_vars['resistance_type'].set('None')  # Сброс типа устойчивости
            self.ui_vars['influence_type'].set('None')  # Сброс типа влияния
            self.ui_vars['resistance_display'].set(self.app.translator.t('None'))  # Сброс отображения устойчивости
            self.ui_vars['influence_display'].set(self.app.translator.t('None'))  # Сброс отображения влияния
            return
        
        self.vertex_plot_frame.pack(side='left')  # Показ фрейма графика
        self.vertex_props_container.pack(fill='x', pady=(30, 0))  # Показ контейнера свойств
        if dist_type == 'Stepwise':  # Ступенчатое распределение
            if not self.app.tier_manager.get_vertex_config():  # Конфигурация ступеней не установлена
                preset_data = VERTEX_TIER_PRESETS.get('uniform_preset', {}).get(6)  # Пресет из 6 ступеней
                if preset_data:  # Пресет найден
                    bounds = preset_data['bounds']  # Границы ступеней
                    counts = preset_data['counts']  # Количество элементов в ступенях
                    stages = [{'left': left, 'right': right, 'weight': count} for (left, right), count in zip(bounds, counts)]  # Список ступеней
                    self.app.tier_manager.set_vertex_stages(stages)  # Установка ступеней в менеджер

            StepwiseWidget(self.vertex_params_container, self.app, domain, self.app.tier_manager,
                           self.vertex_plot, lambda: None).frame.pack(fill='x')  # Виджет ступеней
            return
        cfg = PARAM_CONFIG[domain][dist_type]  # Конфигурация распределения
        sec = AlignedSection(self.vertex_params_container, self.app.widget_factory, self.app)  # Секция параметров
        vars_ = [self.ui_vars[f'{domain}_{dist_type}_{p}'.lower()] for p in cfg['param_order']]  # Переменные параметров
        
        if cfg['ui_type'] == 'dual':  # Двойной тип ui (левый и правый слайдер)
            sec.add_dual_row('left', 'right', vars_[0], vars_[1], 'left', 'right', dist_type, domain)  # Двойная строка
        else:  # Обычный тип ui
            for p, v in zip(cfg['param_order'], vars_):  # Перебор параметров
                sec.add_row(label_key=p, variable=v, param_name=p, dist_type=dist_type, domain=domain)  # Обычная строка
        sec.frame.pack(fill='x')  # Размещение секции
        plot_vars = {p: v for p, v in zip(cfg['param_order'], vars_)}  # Словарь для графика
        update = lambda *a: cfg['plot_update'](self.vertex_plot, plot_vars)  # Функция обновления графика
        for v in vars_:  # Перебор переменных
            v.trace_add('write', update)  # Отслеживание изменений
        update()  # Первоначальное обновление графика
    
    def _collect_params(self):
        """Сбор всех параметров генерации в словарь"""
        params = {
            'n_nodes': self.ui_vars['vertex_count'].get(),  # Количество вершин
            'edge_dist': self._collect_distribution_params('edge', self.ui_vars['edge_distribution'].get())  # Параметры ребер
        }
        vertex_type = self.ui_vars['vertex_distribution'].get()  # Тип распределения вершин
        if vertex_type != 'None':  # Распределение вершин задано
            params['vertex_dist'] = self._collect_distribution_params('vertex', vertex_type)  # Параметры вершин
        return params
    
    def _get_source_data(self):
        """Создание нового graphdata на основе текущих параметров ui"""
        params = self._collect_params()  # Сбор параметров
        new_data = self.app.generate_graph_from_params(params)  # Генерация графа
        new_data.resistance_type = self.data.resistance_type  # Копирование типа устойчивости
        new_data.resistance_coeff = self.data.resistance_coeff  # Копирование коэффициента устойчивости
        new_data.influence_type = self.data.influence_type  # Копирование типа влияния
        new_data.influence_coeff = self.data.influence_coeff  # Копирование коэффициента влияния
        new_data.damping_type = self.data.damping_type  # Копирование типа затухания
        new_data.damping_coeff = self.data.damping_coeff  # Копирование коэффициента затухания
        new_data.source_tab = self.app.translator.t('tab_generation')  # Установка вкладки-источника
        new_data.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Установка времени вставки
        return new_data
        
    def _collect_distribution_params(self, domain, dist_type):
        """Сбор параметров для конкретного распределения"""
        config = PARAM_CONFIG[domain][dist_type]  # Конфигурация распределения
        params = {'type': dist_type}  # Базовый словарь с типом
        if dist_type == 'Stepwise':  # Ступенчатое распределение
            if domain == 'edge':  # Ребра
                stages = self.app.tier_manager.get_edge_config()  # Получение ступеней ребер
            else:  # Вершины
                stages = self.app.tier_manager.get_vertex_config()  # Получение ступеней вершин
            params['stages'] = stages  # Добавление ступеней
            return params
        for param_name in config.get('param_order', []):  # Перебор имен параметров
            var_name = f'{domain}_{dist_type}_{param_name}'.lower()  # Имя переменной
            params[param_name] = self.ui_vars[var_name].get()  # Получение значения из ui переменной
        return params
    
    def refresh_histograms(self):
        """В generationtab нет гистограмм (переопределение пустым методом)"""
        pass
    
    def insert_into_custom(self):
        """Вставка сгенерированного графа в customtab"""
        self.insert_to_tab(1, 'confirm_replace_custom', self.app.set_custom_data)  # Вызов универсального метода
    
    def insert_into_simulation(self):
        """Вставка сгенерированного графа в simulationtab"""
        self.insert_to_tab(2, 'confirm_replace_simulation', self.app.set_simulation_data)  # Вызов универсального метода
        sim_tab = self.app.tab_manager.tab_instances[2]  # Получение вкладки симуляции
        sim_tab.data.source_tab = self.app.translator.t('tab_generation')  # Установка источника
        sim_tab.data.source_graph_index = None  # Сброс индекса графа
        sim_tab.data.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Установка времени вставки
        sim_tab._update_source_info()  # Обновление информации об источнике
        sim_tab.clear_batch_context()  # Очистка контекста множественной симуляции
        sim_tab.reset_simulation()  # Сброс симуляции
    
    def insert_into_multiple(self):
        """Вставка сгенерированного графа в multiplesimtab"""
        self.insert_to_tab(3, 'confirm_replace_multiple', self.app.set_multiple_data)  # Вызов универсального метода

    def save_state(self):
        """Сохранение состояния перед refresh"""
        super().save_state()  # Вызов родительского метода
        ui_vars_state = {key: var.get() for key, var in self.ui_vars.items()}  # Сохранение всех ui переменных
        self._saved_state['ui_vars'] = ui_vars_state  # Добавление в сохраненное состояние
        self._saved_state['edge_stages'] = self.app.tier_manager.get_edge_config()  # Сохранение ступеней ребер
        self._saved_state['vertex_stages'] = self.app.tier_manager.get_vertex_config()  # Сохранение ступеней вершин
    
    def restore_state(self):
        """Восстановление состояния после refresh"""
        super().restore_state()  # Вызов родительского метода
        ui_vars_state = self._saved_state.get('ui_vars', {})  # Получение сохраненных ui переменных
        for key, value in ui_vars_state.items():  # Восстановление ui переменных
            self.ui_vars[key].set(value)  # Установка значения
        edge_stages = self._saved_state.get('edge_stages')  # Получение сохраненных ступеней ребер
        if edge_stages:  # Ступени существуют
            self.app.tier_manager.set_edge_stages(edge_stages)  # Восстановление ступеней ребер
        vertex_stages = self._saved_state.get('vertex_stages')  # Получение сохраненных ступеней вершин
        if vertex_stages:  # Ступени существуют
            self.app.tier_manager.set_vertex_stages(vertex_stages)  # Восстановление ступеней вершин
        self.on_edge_dist_change()  # Обновление ui распределения ребер
        self.on_vertex_dist_change()  # Обновление ui распределения вершин

    def refresh_float_sliders(self):
        """Пересоздание слайдеров для вещественных параметров"""
        self.on_edge_dist_change()  # Пересоздание слайдеров ребер
        self.on_vertex_dist_change()  # Пересоздание слайдеров вершин


# In[41]:


class CustomTab(GraphTab):
    """Вкладка пользовательского графа"""
    
    tab_key = 'tab_custom'  # Ключ для перевода названия вкладки
    
    def __init__(self, parent, app):
        """Инициализация вкладки пользовательского графа с таблицами и параметрами"""
        super().__init__(parent, app)  # Вызов конструктора родительского класса
        self.data = app.custom_data  # Данные пользовательского графа
        self.default = app.default_graph  # Граф по умолчанию для сброса
        self.param_factory = ParameterSectionFactory(app)  # Фабрика секций параметров
        self._initialized = False  # Флаг завершения инициализации
        self.ui_vars = {  # Ui переменные для параметров
            'resistance_type': tk.StringVar(value='None'),  # Тип устойчивости
            'resistance_coeff': tk.DoubleVar(value=0.5),  # Коэффициент устойчивости
            'resistance_display': tk.StringVar(value=app.translator.t('None')),  # Отображение устойчивости
            'influence_type': tk.StringVar(value='None'),  # Тип влияния
            'influence_coeff': tk.DoubleVar(value=0.5),  # Коэффициент влияния
            'influence_display': tk.StringVar(value=app.translator.t('None')),  # Отображение влияния
            'damping_type': tk.StringVar(value='None'),  # Тип затухания
            'damping_coeff': tk.DoubleVar(value=0.5),  # Коэффициент затухания
            'damping_display': tk.StringVar(value=app.translator.t('None')),  # Отображение затухания
        }
        self.graph_display = None  # Виджет отображения графа
        self.vertex_table = None  # Таблица вершин
        self.edge_table = None  # Таблица ребер
        self.edge_hist = None  # Гистограмма ребер
        self.vertex_hist = None  # Гистограмма вершин
        self.right_panel = None  # Правая панель с параметрами
        self.resistance_section = None  # Секция устойчивости
        self.influence_section = None  # Секция влияния
        self.damping_section = None  # Секция затухания
    
    def load_data_to_ui(self):
        """Загрузка данных из self.data в ui переменные"""
        for param_type in ['resistance', 'influence', 'damping']:  # Перебор типов параметров
            type_value = getattr(self.data, f'{param_type}_type')  # Тип параметра
            coeff_value = getattr(self.data, f'{param_type}_coeff')  # Коэффициент
            self.ui_vars[f'{param_type}_type'].set(type_value)  # Установка типа
            self.ui_vars[f'{param_type}_display'].set(self.app.translator.t(type_value))  # Установка отображения
            self.ui_vars[f'{param_type}_coeff'].set(coeff_value)  # Установка коэффициента
        if self.vertex_table:  # Таблица вершин существует
            self.vertex_table.set_graph_data(self.data)  # Установка данных в таблицу
        if self.edge_table:  # Таблица ребер существует
            self.edge_table.set_graph_data(self.data)  # Установка данных в таблицу
        if self.graph_display:  # Виджет графа существует
            self.graph_display.set_graph_data(self.data)  # Установка данных в виджет
            self.graph_display.draw()  # Отрисовка графа
        self.refresh_histograms()  # Обновление гистограмм
    
    def save_ui_to_data(self):
        """Сохранение ui переменных в self.data"""
        for param_type in ['resistance', 'influence', 'damping']:  # Перебор типов параметров
            original_type = self.ui_vars[f'{param_type}_type'].get()  # Тип параметра
            coeff_value = self.ui_vars[f'{param_type}_coeff'].get()  # Коэффициент
            setattr(self.data, f'{param_type}_type', original_type)  # Сохранение типа
            setattr(self.data, f'{param_type}_coeff', coeff_value)  # Сохранение коэффициента
    
    def build(self):
        """Создание интерфейса вкладки пользовательского графа"""
        self._initialized = False  # Сброс флага инициализации
        scroll = ScrollableFrame(self.frame, self.app.widget_factory)  # Прокручиваемый фрейм
        scroll.pack(fill='both', expand=True)  # Размещение с растяжением
        content = scroll.inner  # Внутренний контент
        content.columnconfigure(0, weight=1)  # Растяжение колонки
        main_container = self.app.widget_factory.create_frame(content)  # Главный контейнер
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)  # Размещение с отступами
        main_container.columnconfigure(0, weight=1)  # Растяжение колонки
        main_container.rowconfigure(0, weight=1)  # Растяжение строки
        current_row = 0  # Текущая строка сетки
        graph_panel_height = self.app.size_config['container']['graph_panel']['height']  # Высота панели графа
        graph_and_right_panel = self.app.widget_factory.create_frame(main_container,height=graph_panel_height)# Контейнер графа и правой панели
        graph_and_right_panel.grid(row=current_row, column=0, sticky='nsew', pady=(0, 30))  # Размещение
        graph_and_right_panel.grid_propagate(False)  # Запрет изменения размера
        graph_and_right_panel.columnconfigure(0, weight=1)  # Растяжение колонки графа
        graph_and_right_panel.columnconfigure(1, weight=0)  # Фиксация колонки панели
        graph_and_right_panel.rowconfigure(0, weight=1)  # Растяжение строки
        current_row += 1  # Увеличение счетчика строк
        graph_frame = self.app.widget_factory.create_frame(graph_and_right_panel)  # Фрейм для графа
        graph_frame.grid(row=0, column=0, sticky='nsew')  # Размещение
        self.graph_display = GraphDisplay(graph_frame, self.app.widget_factory, self.app)  # Виджет графа
        self.graph_display.pack(fill='both', expand=True)  # Размещение с растяжением
        side_panel_width = self.app.size_config['container']['side_panel']['width']  # Ширина правой панели
        self.right_panel = self.app.widget_factory.create_frame(graph_and_right_panel, width=side_panel_width)# Правая панель
        self.right_panel.grid(row=0, column=1, padx=(0, 0), sticky='n')  # Размещение
        self.right_panel.columnconfigure(0, weight=1)  # Растяжение колонки
        right_row = 0  # Текущая строка правой панели
        
        param_types = ['resistance', 'influence', 'damping']  # Типы параметров
        paddings = [(0, 10), (0, 10), (0, 0)]  # Отступы для каждой секции
        for param_type, pady in zip(param_types, paddings):  # Перебор типов параметров
            section, display_var, coeff_var, _ = self.param_factory.create_section(param_type,self.right_panel,self.ui_vars,'subrow')# Создание
            section.frame.grid(row=right_row, column=0, sticky='new', pady=pady, padx=(22, 0))  # Размещение
            setattr(self, f'{param_type}_section', section)  # Сохранение секции
            right_row += 1  # Увеличение счетчика строк
        hist_container = self.app.widget_factory.create_frame(self.right_panel)  # Контейнер гистограмм
        hist_container.grid(row=right_row, column=0, sticky='new', pady=(0, 0))  # Размещение
        self.edge_hist = HistogramWidget(hist_container, self.app.widget_factory, self.app, 'edge_distribution', 'edge')# Гистограмма ребер
        self.edge_hist.frame.grid(row=0, column=0, padx=0, pady=(30, 0))  # Размещение
        self.vertex_hist = HistogramWidget(hist_container, self.app.widget_factory, self.app, 'vertex_distribution', 'vertex')# Гистограмма вершин
        self.vertex_hist.frame.grid(row=0, column=1, padx=(0, 0), pady=(30, 0))  # Размещение
        
        vertex_table_height = self.app.size_config['container']['vertex_table']['height']  # Высота таблицы вершин
        self._build_table_section(main_container, current_row, 'vertex_distribution','vertex', vertex_table_height)  # Секция вершин
        current_row += 1  # Увеличение счетчика строк
        edge_table_height = self.app.size_config['container']['edge_table']['height']  # Высота таблицы ребер
        self._build_table_section(main_container, current_row, 'edge_distribution','edge', edge_table_height)  # Секция ребер
        current_row += 1  # Увеличение счетчика строк
        self._build_buttons(main_container, current_row)  # Секция кнопок
        current_row += 1  # Увеличение счетчика строк
        self.load_data_to_ui()  # Загрузка данных в ui
        self._initialized = True  # Установка флага инициализации
    
    def _build_table_section(self, parent, row, title_key, table_type, height):
        """Создание секции с таблицей вершин или ребер"""
        section = AlignedSection(parent, self.app.widget_factory, self.app, title_key)  # Секция с заголовком
        container = self.app.widget_factory.create_frame(section.content, height=height)  # Контейнер таблицы
        container.pack(fill='x', pady=0)  # Размещение
        container.pack_propagate(False)  # Запрет изменения размера
        
        if table_type == 'vertex':  # Таблица вершин
            self.vertex_table = VirtualVertexTable(container, self.app.widget_factory, self.app)  # Виртуальная таблица
            self.vertex_table.set_graph_data(self.data)  # Установка данных
            self.vertex_table.on_change(self.on_vertex_change_from_ui)  # Подписка на изменения
            self.vertex_table.pack(fill='both', expand=True)  # Размещение
            btn_frame = self.app.widget_factory.create_frame(section.content)  # Фрейм кнопок
            btn_frame.pack(fill='x', pady=(10, 0))  # Размещение
            self.app.widget_factory.create_button(btn_frame, 'load_csv', lambda: CSVDataManager(self.app.root, self.app, 'vertices', 'load'),
                                                  'preset', padx=10).pack(side='left', padx=(0, 10)) # Кнопка загрузки csv
            self.app.widget_factory.create_button(btn_frame, 'save_csv', lambda: CSVDataManager(self.app.root, self.app, 'vertices', 'save'),
                                                  'preset', padx=10).pack(side='left')# Кнопка сохранения csv
        else:  # Таблица ребер
            self.edge_table = VirtualEdgeTable(container, self.app.widget_factory, self.app)  # Виртуальная таблица
            self.edge_table.set_graph_data(self.data)  # Установка данных
            self.edge_table.on_change(self.on_edge_change_from_ui)  # Подписка на изменения
            self.edge_table.pack(fill='both', expand=True)  # Размещение
            btn_frame = self.app.widget_factory.create_frame(section.content)  # Фрейм кнопок
            btn_frame.pack(fill='x', pady=(10, 0))  # Размещение
            self.app.widget_factory.create_button(btn_frame, 'load_csv', lambda: CSVDataManager(self.app.root, self.app, 'edges', 'load'),
                                                  'preset', padx=10).pack(side='left', padx=(0, 10)) # Кнопка загрузки csv
            self.app.widget_factory.create_button(btn_frame, 'save_csv', lambda: CSVDataManager(self.app.root, self.app, 'edges', 'save'),
                                                  'preset', padx=10).pack(side='left')# Кнопка сохранения csv
        section.frame.grid(row=row, column=0, sticky='ew', pady=(0, 50))  # Размещение секции
    
    def _build_buttons(self, parent, row):
        """Создание панели с кнопками управления"""
        btn_group = self.app.size_config['container']['button_group']  # Конфигурация группы кнопок
        buttons_container = self.app.widget_factory.create_frame(parent, height=btn_group['height'])# Контейнер кнопок
        buttons_container.grid(row=row, column=0, sticky='ew', padx=150, pady=(0, 100))  # Размещение
        buttons_container.grid_propagate(False)  # Запрет изменения размера
        buttons_container.columnconfigure(0, weight=1)  # Растяжение колонки
        buttons_frame = self.app.widget_factory.create_frame(buttons_container)  # Фрейм кнопок
        buttons_frame.pack(fill='x', expand=True)  # Размещение с растяжением
        for i in range(3):  # Три колонки для кнопок
            buttons_frame.columnconfigure(i, weight=1)  # Равномерное растяжение
        
        buttons_config = [  # Конфигурация кнопок
            ('reset_to_default', self.reset_to_default, 'insert_custom'),  # Сброс к дефолту
            ('insert_into_simulation', self.insert_into_simulation, 'insert_sim'),  # Вставка в симуляцию
            ('insert_into_multiple', self.insert_into_multiple, 'insert_multi')  # Вставка в множественную
        ]
        for col, (text_key, command, style_key) in enumerate(buttons_config):  # Перебор кнопок
            btn = self.app.widget_factory.create_button(buttons_frame, text_key, command, style_key)# Создание кнопки
            btn.grid(row=0, column=col, padx=30, pady=10, sticky='ew')  # Размещение
    
    def on_data_changed(self, change_type, **kwargs):
        """Обработчик изменений данных графа (вызывается при редактировании)"""
        if change_type == 'vertex_changed':  # Изменение веса вершины
            if self.graph_display:  # Виджет графа существует
                self.graph_display.draw()  # Перерисовка графа
            self.refresh_histograms()  # Обновление гистограмм
            
        elif change_type == 'vertex_added':  # Добавление вершины
            node = kwargs.get('node')  # Имя новой вершины
            if self.graph_display and node:  # Виджет графа существует
                self.graph_display.add_vertex_at_random_position(node)  # Добавление вершины в случайное место
                self.graph_display.added_vertices_count += 1  # Увеличение счетчика добавлений
                self._check_and_rebuild_layout()  # Проверка порога перестроения
            self._update_tables_and_histograms()  # Обновление таблиц и гистограмм
            self._update_simulation_slider()  # Обновление слайдера симуляции
            
        elif change_type == 'vertex_removed':  # Удаление вершины
            node = kwargs.get('node')  # Имя удаляемой вершины
            if self.graph_display and node:  # Виджет графа существует
                self.graph_display.remove_vertex(node)  # Удаление вершины из отображения
            self._update_tables_and_histograms()  # Обновление таблиц и гистограмм
            self._update_simulation_slider()  # Обновление слайдера симуляции
            
        elif change_type == 'edge_changed':  # Изменение веса ребра
            if self.graph_display:  # Виджет графа существует
                self.graph_display._cached_edge_segments = None  # Сброс кэша ребер
                self.graph_display.draw()  # Перерисовка графа
            self.refresh_histograms()  # Обновление гистограмм
    
    def _update_tables_and_histograms(self):
        """Обновление таблиц и гистограмм после изменения данных"""
        if self.vertex_table:  # Таблица вершин существует
            self.vertex_table.redraw()  # Перерисовка таблицы
        if self.edge_table:  # Таблица ребер существует
            self.edge_table.redraw()  # Перерисовка таблицы
        self.refresh_histograms()  # Обновление гистограмм
    
    def _check_and_rebuild_layout(self):
        """Проверка счетчика добавленных вершин и перестроение графа при достижении порога"""
        threshold = self.app.settings.get('threshold_add_vertex', tk.IntVar(value=5)).get()  # Пороговое значение
        if self.graph_display and self.graph_display.added_vertices_count >= threshold:  # Порог достигнут
            self.graph_display.rebuild_layout()  # Перестроение компоновки графа
    
    def _update_simulation_slider(self):
        """Обновление слайдера стартовой вершины на вкладке симуляции"""
        if len(self.app.tab_manager.tab_instances) > 2:  # Вкладка симуляции существует
            sim_tab = self.app.tab_manager.tab_instances[2]  # Получение вкладки симуляции
            if sim_tab and hasattr(sim_tab, '_update_start_vertex_slider'):  # Метод существует
                sim_tab._update_start_vertex_slider()  # Обновление слайдера
    
    def on_vertex_change_from_ui(self, action, index, value):
        """Обработчик изменений от virtualvertextable"""
        node = f'V{index}'  # Имя вершины
        if action == 'change':  # Изменение веса
            self.on_data_changed('vertex_changed', node=node, index=index, value=value)
        elif action == 'add':  # Добавление вершины
            self.on_data_changed('vertex_added', node=node, index=index, value=value)
        elif action == 'delete':  # Удаление вершины
            self.on_data_changed('vertex_removed', node=node, index=index)
    
    def on_edge_change_from_ui(self, i, j, value):
        """Обработчик изменений от virtualedgetable"""
        u, v = f'V{i}', f'V{j}'  # Имена вершин
        self.on_data_changed('edge_changed', u=u, v=v, i=i, j=j, value=value)  # Вызов обработчика
        if self.graph_display:  # Виджет графа существует
            self.graph_display.invalidate()  # Сброс кэша
            self.refresh_graph()  # Обновление графа
    
    def _get_source_data(self):
        """Возврат копии текущего графа для вставки в другую вкладку"""
        self.save_ui_to_data()  # Сохранение ui данных в модель
        return self.data.copy()  # Копия данных графа
    
    def insert_into_simulation(self):
        """Вставка текущего графа в simulationtab"""
        self.save_ui_to_data()  # Сохранение ui данных в модель
        self.insert_to_tab(2, 'confirm_replace_simulation', self.app.set_simulation_data)  # Вызов универсального метода
        sim_tab = self.app.tab_manager.tab_instances[2]  # Получение вкладки симуляции
        if sim_tab and sim_tab.data:  # Вкладка и данные существуют
            sim_tab.data.source_tab = self.app.translator.t('tab_custom')  # Установка источника
            sim_tab.data.source_graph_index = None  # Сброс индекса графа
            sim_tab.data.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Установка времени вставки
            sim_tab._update_source_info()  # Обновление информации об источнике
            sim_tab.clear_batch_context()  # Очистка контекста множественной симуляции
            sim_tab.reset_simulation()  # Сброс симуляции
        self._update_simulation_tab(sim_tab)  # Обновление элементов симуляции
    
    def _update_simulation_tab(self, sim_tab):
        """Обновление всех элементов вкладки симуляции после вставки графа"""
        if not sim_tab:  # Вкладка не существует
            return
        sim_tab._update_start_vertex_slider()  # Обновление слайдера стартовой вершины
        sim_tab.reset_simulation()  # Сброс симуляции
        sim_tab._update_graph_params_column()  # Обновление параметров графа
        sim_tab._update_generation_params_column()  # Обновление параметров генерации
        sim_tab._update_edge_stats_column()  # Обновление статистики ребер
        sim_tab._update_vertex_stats_column()  # Обновление статистики вершин
        sim_tab._update_start_vertex_stats_column()  # Обновление статистики стартовой вершины
        sim_tab._update_histograms()  # Обновление гистограмм
    
    def insert_into_multiple(self):
        """Вставка текущего графа в multiplesimtab"""
        self.save_ui_to_data()  # Сохранение ui данных в модель
        self.insert_to_tab(3, 'confirm_replace_multiple', self.app.set_multiple_data)  # Вызов универсального метода
    
    def reset_to_default(self):
        """Сброс к графу по умолчанию"""
        if self.app.is_copying:  # Предотвращение рекурсивного копирования
            return
        
        if not tk.messagebox.askyesno(self.app.translator.t('confirm_title'),
                                      self.app.translator.t('confirm_reset_default')):# Подтверждение пользователя
            return
            
        self.data = self.app.default_graph.copy()  # Копия графа по умолчанию
        self.data.generation_params = None  # Сброс параметров генерации
        self.load_data_to_ui()  # Загрузка данных в ui
        self.refresh_display()  # Обновление отображения
    
    def refresh_display(self):
        """Полное обновление отображения вкладки"""
        if self.vertex_table:  # Таблица вершин существует
            self.vertex_table.redraw()  # Перерисовка таблицы
        if self.edge_table:  # Таблица ребер существует
            self.edge_table.redraw()  # Перерисовка таблицы
        self.refresh_graph()  # Обновление графа
        self.refresh_histograms()  # Обновление гистограмм
        self._update_simulation_slider()  # Обновление слайдера симуляции
    
    def receive_data(self, new_data):
        """Получение графа с другой вкладки"""
        if self.data is new_data:  # Те же данные
            return
        self.data = new_data  # Сохранение новых данных
        self.data.generation_params = None  # Сброс параметров генерации
        if self.vertex_table:  # Таблица вершин существует
            self.vertex_table.set_graph_data(self.data)  # Установка данных
        if self.edge_table:  # Таблица ребер существует
            self.edge_table.set_graph_data(self.data)  # Установка данных
        if self.graph_display:  # Виджет графа существует
            self.graph_display.pos_cache = None  # Сброс кэша позиций
            self.graph_display.added_vertices_count = 0  # Сброс счетчика добавлений
            self.graph_display.set_graph_data(self.data)  # Установка данных в виджет
        self.load_data_to_ui()  # Загрузка данных в ui
        self.refresh_display()  # Обновление отображения
    
    def refresh(self):
        """Полное перестроение вкладки при смене языка или темы"""
        self.save_state()  # Сохранение состояния
        self.save_ui_to_data()  # Сохранение ui данных в модель
        for widget in self.frame.winfo_children():  # Удаление всех дочерних виджетов
            widget.destroy()
        self.build()  # Перестроение интерфейса
        self.load_data_to_ui()  # Загрузка данных в ui
        self.restore_state()  # Восстановление состояния
        if self.vertex_table:  # Таблица вершин существует
            self.vertex_table.redraw()  # Перерисовка таблицы
        if self.edge_table:  # Таблица ребер существует
            self.edge_table.redraw()  # Перерисовка таблицы
    
    def save_state(self):
        """Сохранение состояния перед refresh"""
        super().save_state()  # Вызов родительского метода
        ui_vars_state = {key: var.get() for key, var in self.ui_vars.items()}  # Сохранение ui переменных
        self._saved_state['ui_vars'] = ui_vars_state  # Добавление в сохраненное состояние
    
    def restore_state(self):
        """Восстановление состояния после refresh"""
        super().restore_state()  # Вызов родительского метода
        ui_vars_state = self._saved_state.get('ui_vars', {})  # Получение сохраненных ui переменных
        for key, value in ui_vars_state.items():  # Восстановление ui переменных
            if key in self.ui_vars:  # Переменная существует
                self.ui_vars[key].set(value)  # Установка значения


# In[42]:


class SimulationTab(GraphTab):
    """Вкладка запуска симуляции"""
    
    tab_key = 'tab_simulation'  # Ключ для перевода названия вкладки
    
    def __init__(self, parent, app):
        """Инициализация вкладки симуляции с ui переменными и виджетами"""
        super().__init__(parent, app)  # Вызов конструктора родительского класса
        self.data = app.simulation_data  # Данные графа для симуляции
        self.ui_vars = {'start_vertex': tk.IntVar(value=1)}  # Номер стартовой вершины
        self._last_simulation_result = None  # Последний результат симуляции
        self._start_vertex_trace_id = None  # Идентификатор trace для стартовой вершины
        self.batch_context = None  # Контекст множественной симуляции
        self.graph_display = None  # Виджет отображения графа
        self.start_vertex_slider = None  # Слайдер выбора стартовой вершины
        self.start_vertex_entry = None  # Поле ввода стартовой вершины
        self.new_graph_button = None  # Кнопка нового графа
        self.graph_params_labels = {}  # Метки параметров графа
        self.edge_stats_labels = {}  # Метки статистики ребер
        self.vertex_stats_labels = {}  # Метки статистики вершин
        self.start_vertex_labels = {}  # Метки статистики стартовой вершины
        self.simulation_results_labels = {}  # Метки результатов симуляции
        self.generation_params_frame = None  # Фрейм параметров генерации
        self.edge_hist = None  # Гистограмма ребер
        self.vertex_hist = None  # Гистограмма вершин
    
    def build(self):
        """Создание интерфейса вкладки симуляции"""
        scroll = ScrollableFrame(self.frame, self.app.widget_factory)  # Прокручиваемый фрейм
        scroll.pack(fill='both', expand=True)  # Размещение с растяжением
        content = scroll.inner  # Внутренний контент
        content.columnconfigure(0, weight=1)  # Растяжение колонки
        main_container = self.app.widget_factory.create_frame(content)  # Главный контейнер
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)  # Размещение с отступами
        main_container.columnconfigure(0, weight=1)  # Растяжение колонки
        current_row = 0  # Текущая строка сетки
        graph_panel_height = self.app.size_config['container']['graph_panel']['height']  # Высота панели графа
        graph_and_right_panel = self.app.widget_factory.create_frame(main_container, height=graph_panel_height)# Контейнер графа и правой панели
        graph_and_right_panel.grid(row=current_row, column=0, sticky='nsew', pady=0)  # Размещение
        graph_and_right_panel.grid_propagate(False)  # Запрет изменения размера
        graph_and_right_panel.columnconfigure(0, weight=1)  # Растяжение колонки графа
        graph_and_right_panel.columnconfigure(1, weight=0)  # Фиксация колонки панели
        graph_and_right_panel.rowconfigure(0, weight=1)  # Растяжение строки
        current_row += 1  # Увеличение счетчика строк
        graph_frame = self.app.widget_factory.create_frame(graph_and_right_panel)  # Фрейм для графа
        graph_frame.grid(row=0, column=0, sticky='nsew', padx=0)  # Размещение
        self.graph_display = GraphDisplay(graph_frame, self.app.widget_factory, self.app)  # Виджет графа
        self.graph_display.pack(fill='both', expand=True)  # Размещение с растяжением
        side_panel_width = self.app.size_config['container']['side_panel']['width']  # Ширина правой панели
        right_panel = self.app.widget_factory.create_frame(graph_and_right_panel, width=side_panel_width) # Правая панель
        right_panel.grid(row=0, column=1, padx=(0, 0), sticky='n')  # Размещение
        right_panel.columnconfigure(0, weight=1)  # Растяжение колонки
        self._create_graph_params_column(right_panel)  # Колонка параметров графа
        self._create_histograms(right_panel)  # Гистограммы
        self._create_start_vertex_section(right_panel)  # Секция выбора стартовой вершины
        self._create_buttons_area(main_container, current_row)  # Кнопки управления
        current_row += 1  # Увеличение счетчика строк
        self._create_stats_columns(main_container, current_row)  # Колонки со статистикой
        self._refresh_ui_from_data()  # Загрузка данных в ui
    
    def on_activate(self):
        """Вызов при активации вкладки (синхронизация данных)"""
        if self.data is not self.app.simulation_data:  # Данные устарели
            self.receive_data(self.app.simulation_data)  # Получение актуальных данных
        else:  # Данные актуальны
            self._refresh_ui_from_data()  # Обновление интерфейса
    
    def on_deactivate(self):
        """Вызов при деактивации вкладки (ничего не делает)"""
        pass
    
    def save_state(self):
        """Сохранение состояния перед refresh"""
        super().save_state()  # Вызов родительского метода
        self._saved_state.update({  # Добавление специфичных данных
            'start_vertex': self.ui_vars['start_vertex'].get(),  # Стартовая вершина
            'last_simulation_result': self._last_simulation_result,  # Последний результат
            'batch_context': self.batch_context,  # Контекст множественной симуляции
        })
    
    def restore_state(self):
        """Восстановление состояния после refresh"""
        super().restore_state()  # Вызов родительского метода
        if self._saved_state:  # Сохраненное состояние существует
            self.ui_vars['start_vertex'].set(self._saved_state.get('start_vertex', 1))  # Восстановление стартовой вершины
            self._last_simulation_result = self._saved_state.get('last_simulation_result')  # Восстановление результата
            self.batch_context = self._saved_state.get('batch_context')  # Восстановление контекста
            if self._last_simulation_result:  # Результат существует
                self._update_simulation_results_column(self._last_simulation_result)  # Обновление колонки результатов
                if self.graph_display:  # Виджет графа существует
                    self.graph_display.set_fire_data(  # Установка данных пожара
                        self._last_simulation_result['burned_nodes'],
                        self._last_simulation_result['burned_edges'])
            self._update_new_graph_button_text()  # Обновление текста кнопки
    
    def refresh(self):
        """Полное перестроение вкладки при смене языка или темы"""
        self.save_state()  # Сохранение состояния
        if self._start_vertex_trace_id:  # Trace существует
            self.ui_vars['start_vertex'].trace_remove('write', self._start_vertex_trace_id)  # Удаление trace
            self._start_vertex_trace_id = None  # Сброс идентификатора
        for widget in self.frame.winfo_children():  # Удаление всех дочерних виджетов
            widget.destroy()
        self.build()  # Перестроение интерфейса
        self.restore_state()  # Восстановление состояния
    
    def set_batch_context(self, multiple_tab, graph_index, row_index=None):
        """Установка контекста множественной симуляции для навигации"""
        self.batch_context = {  # Сохранение контекста
            'multiple_tab_id': id(multiple_tab),  # Идентификатор вкладки множественной симуляции
            'graph_index': graph_index,  # Индекс текущего графа
            'row_index': row_index  # Индекс строки в таблице
        }
        self._update_new_graph_button_text()  # Обновление текста кнопки
    
    def clear_batch_context(self):
        """Очистка контекста множественной симуляции"""
        self.batch_context = None  # Сброс контекста
        self._update_new_graph_button_text()  # Обновление текста кнопки
    
    def _update_new_graph_button_text(self):
        """Обновление текста кнопки 'новый граф' в зависимости от контекста"""
        if not hasattr(self, 'new_graph_button') or not self.new_graph_button or not self.new_graph_button.winfo_exists():
            return  # Кнопка не существует
        if self.batch_context is not None:  # Режим множественной симуляции
            self.new_graph_button.config(text=self.app.translator.t('next_graph'))  # Текст "следующий граф"
        else:  # Обычный режим
            self.new_graph_button.config(text=self.app.translator.t('new_graph'))  # Текст "новый граф"
    
    def _load_next_graph_from_batch(self):
        """Загрузка следующего графа из множественной симуляции"""
        if self.batch_context is None:  # Нет контекста
            return
        multiple_tab = None  # Поиск вкладки множественной симуляции
        for i, instance in enumerate(self.app.tab_manager.tab_instances):  # Перебор вкладок
            if instance is not None and id(instance) == self.batch_context['multiple_tab_id']:  # Совпадение идентификатора
                multiple_tab = instance  # Найденная вкладка
                break
        if multiple_tab is None or not hasattr(multiple_tab, 'result_rows'):  # Вкладка не найдена
            self.clear_batch_context()  # Очистка контекста
            self.reset_simulation()  # Сброс симуляции
            return
        current_index = self.batch_context['graph_index']  # Текущий индекс графа
        total_graphs = len(multiple_tab.result_rows)  # Общее количество графов
        if total_graphs == 0:  # Нет графов
            self.clear_batch_context()  # Очистка контекста
            self.reset_simulation()  # Сброс симуляции
            return
        if total_graphs == 1:  # Только один граф
            self.reset_simulation()  # Сброс симуляции
            return
        current_position = -1  # Поиск позиции текущего графа
        for i, row in enumerate(multiple_tab.result_rows):  # Перебор строк
            if hasattr(row, 'graph_index') and row.graph_index == current_index:  # Совпадение индекса
                current_position = i  # Сохранение позиции
                break
        if current_position == -1:  # Текущий граф не найден
            self.clear_batch_context()  # Очистка контекста
            self.reset_simulation()  # Сброс симуляции
            return
        
        next_position = (current_position + 1) % total_graphs  # Следующая позиция (циклически)
        next_row = multiple_tab.result_rows[next_position]  # Следующая строка
        next_graph_index = next_row.graph_index  # Индекс следующего графа
        new_data = next_row.graph_data.copy()  # Копирование данных графа
        new_data.source_tab = 'tab_multiple'  # Источник - множественная симуляция
        new_data.source_graph_index = next_graph_index  # Индекс графа
        new_data.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Время вставки
        new_data.resistance_type = self.data.resistance_type  # Копирование типа устойчивости
        new_data.resistance_coeff = self.data.resistance_coeff  # Копирование коэффициента устойчивости
        new_data.influence_type = self.data.influence_type  # Копирование типа влияния
        new_data.influence_coeff = self.data.influence_coeff  # Копирование коэффициента влияния
        new_data.damping_type = self.data.damping_type  # Копирование типа затухания
        new_data.damping_coeff = self.data.damping_coeff  # Копирование коэффициента затухания
        self.data = new_data  # Обновление данных
        self.app.simulation_data = new_data  # Обновление данных в приложении
        self.batch_context['graph_index'] = next_graph_index  # Обновление индекса
        self.batch_context['row_index'] = next_position  # Обновление позиции
        self.reset_simulation()  # Сброс симуляции
        self._refresh_ui_from_data()  # Обновление интерфейса
        self._update_source_info()  # Обновление информации об источнике
    
    def _regenerate_graph(self):
        """Генерация нового графа по тем же параметрам с новым seed-ом"""
        if self.data.generation_params is None:  # Нет параметров генерации
            return
        new_data = self.app.generate_graph_from_params(self.data.generation_params)  # Генерация графа
        new_data.resistance_type = self.data.resistance_type  # Копирование типа устойчивости
        new_data.resistance_coeff = self.data.resistance_coeff  # Копирование коэффициента устойчивости
        new_data.influence_type = self.data.influence_type  # Копирование типа влияния
        new_data.influence_coeff = self.data.influence_coeff  # Копирование коэффициента влияния
        new_data.damping_type = self.data.damping_type  # Копирование типа затухания
        new_data.damping_coeff = self.data.damping_coeff  # Копирование коэффициента затухания
        new_data.source_tab = self.data.source_tab  # Копирование источника
        new_data.source_graph_index = None  # Сброс индекса графа
        new_data.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Время вставки
        self.data = new_data  # Обновление данных
        self.app.simulation_data = new_data  # Обновление данных в приложении
        self.clear_batch_context()  # Очистка контекста
        self.reset_simulation()  # Сброс симуляции
        self._refresh_ui_from_data()  # Обновление интерфейса
    
    def generate_new_graph(self):
        """Обработчик кнопки 'новый граф' или 'следующий граф'"""
        if self.batch_context is not None:  # Режим множественной симуляции
            self._load_next_graph_from_batch()  # Загрузка следующего графа
        elif self.data.generation_params is not None:  # Есть параметры генерации
            self._regenerate_graph()  # Генерация нового графа
        else:  # Пользовательский граф
            self.reset_simulation()  # Сброс симуляции
    
    def _get_source_display_name(self):
        """Возврат отображаемого имени источника графа"""
        if not hasattr(self.data, 'source_tab'):  # Нет информации об источнике
            return self.app.translator.t('tab_custom')  # По умолчанию пользовательский
        source = self.data.source_tab  # Исходная вкладка
        if not source.startswith('tab_'):  # Уже отображаемое имя
            return source
        if source == 'tab_multiple':  # Множественная симуляция
            if hasattr(self.data, 'source_graph_index') and self.data.source_graph_index is not None:  # Индекс существует
                return f"{self.app.translator.t('tab_multiple')} (G {self.data.source_graph_index})"  # С индексом
            return self.app.translator.t('tab_multiple')  # Без индекса
        return self.app.translator.t(source)  # Перевод ключа вкладки
    
    def _create_graph_params_column(self, parent):
        """Создание колонки параметров графа"""
        params = ['source_tab', 'insert_time', 'vertex_count_stat', 'edge_count_stat', 'edge_distribution', 'vertex_distribution',
                  'resistance_stat', 'influence_stat', 'damping_stat', 'graph_seed']  # Список ключей
        self.graph_params_labels = self.app.widget_factory.create_stat_column(parent, 'graph_parameters', params)  # Создание колонки
    
    def _update_source_info(self):
        """Обновление отображения источника графа и времени вставки"""
        if self.graph_params_labels:  # Метки существуют
            source_label = self.graph_params_labels.get('source_tab')  # Метка источника
            time_label = self.graph_params_labels.get('insert_time')  # Метка времени
            if source_label:  # Метка источника существует
                source_label.config(text=self._get_source_display_name())  # Обновление текста
            if time_label:  # Метка времени существует
                time_label.config(text=self.data.insert_time if hasattr(self.data, 'insert_time') else datetime.now().strftime("%d.%m.%Y %H:%M:%S"))  # Обновление времени
    
    def _update_graph_params_column(self):
        """Обновление значений в колонке параметров графа"""
        edge_type = self.data.get_edge_distribution_type()  # Тип распределения ребер
        vertex_type = self.data.get_vertex_distribution_type()  # Тип распределения вершин
        
        seed_value = self.data.graph_seed if hasattr(self.data, 'graph_seed') and self.data.graph_seed is not None else '—'  # Значение seed
        if seed_value != '—' and isinstance(seed_value, int):  # Корректное число
            seed_display = str(seed_value)  # Преобразование в строку
        else:  # Некорректное значение
            seed_display = '—'  # Пустое значение
        
        values = {  # Словарь значений
            'source_tab': self._get_source_display_name(),  # Источник
            'insert_time': self.data.insert_time if hasattr(self.data,
                                                'insert_time') else datetime.now().strftime("%d.%m.%Y %H:%M:%S"),  # Время вставки
            'vertex_count_stat': self.data.graph.number_of_nodes(),  # Количество вершин
            'edge_count_stat': self.data.graph.number_of_edges(),  # Количество ребер
            'edge_distribution': self.app.translator.t(edge_type),  # Распределение ребер
            'vertex_distribution': self.app.translator.t(vertex_type),  # Распределение вершин
            'resistance_stat': self.app.translator.t(self.data.resistance_type),  # Тип устойчивости
            'influence_stat': self.app.translator.t(self.data.influence_type),  # Тип влияния
            'damping_stat': self.app.translator.t(self.data.damping_type),  # Тип затухания
            'graph_seed': seed_display,  # Seed графа
        }
        for key, label in self.graph_params_labels.items():  # Перебор меток
            if label is not None:  # Метка существует
                value = values.get(key)  # Получение значения
                if value is not None:  # Значение существует
                    label.config(text=str(value))  # Обновление текста
    
    def _create_histograms(self, parent):
        """Создание гистограмм ребер и вершин"""
        hist_container = self.app.widget_factory.create_frame(parent)  # Контейнер гистограмм
        hist_container.pack(fill='x', pady=(30, 0))  # Размещение с отступом сверху
        self.edge_hist = HistogramWidget(hist_container, self.app.widget_factory, self.app, 'edge_distribution', 'edge') # Гистограмма ребер
        self.edge_hist.frame.pack(side='left', padx=0)  # Размещение
        self.vertex_hist = HistogramWidget(hist_container,self.app.widget_factory,self.app,'vertex_distribution','vertex') # Гистограмма вершин
        self.vertex_hist.frame.pack(side='left', padx=0)  # Размещение
    
    def _create_start_vertex_section(self, parent):
        """Создание секции выбора стартовой вершины"""
        start_container = self.app.widget_factory.create_labelframe(parent, 'start_vertex_title')  # Фрейм с заголовком
        start_container.pack(fill='x', pady=(30, 0))  # Размещение с отступом сверху
        start_content = start_container.content  # Внутренний контент
        start_vertex_section = AlignedSection(start_content, self.app.widget_factory, self.app, None)  # Секция без заголовка
        start_vertex_section.add_row(  # Добавление строки со слайдером и полем ввода
            variable=self.ui_vars['start_vertex'],  # Переменная стартовой вершины
            param_name='start_vertex',  # Имя параметра
            dist_type='global',  # Тип распределения
            domain='global',  # Домен параметра
            label_key=None,  # Без лейбла
            show_label=False,  # Скрытие лейбла
            show_entry=True,  # Показ поля ввода
            scale_size='normal',  # Нормальный размер слайдера
            expand_scale=True  # Растяжение слайдера
        )
        start_vertex_section.frame.pack(fill='x', pady=0)  # Размещение секции
        self.start_vertex_slider = start_vertex_section.rows[-1]['scale']  # Слайдер
        self.start_vertex_entry = start_vertex_section.rows[-1]['entry']  # Поле ввода
        self._start_vertex_trace_id = self.ui_vars['start_vertex'].trace_add('write',
                                                    lambda *args: self._update_start_vertex_stats_column())  # Отслеживание изменений
    
    def _create_buttons_area(self, parent, row):
        """Создание области с кнопками управления"""
        buttons_row = self.app.widget_factory.create_frame(parent)  # Строка кнопок
        buttons_row.grid(row=row, column=0, sticky='ew', pady=50)  # Размещение
        buttons_row.columnconfigure(0, weight=1)  # Растяжение левой колонки
        buttons_row.columnconfigure(1, weight=1)  # Растяжение правой колонки
        left_buttons_frame = self.app.widget_factory.create_frame(buttons_row)  # Левая группа кнопок
        left_buttons_frame.grid(row=0, column=0, sticky='ew')  # Размещение
        left_buttons_frame.columnconfigure(0, weight=1)  # Растяжение первой кнопки
        left_buttons_frame.columnconfigure(1, weight=1)  # Растяжение второй кнопки
        left_buttons_frame.columnconfigure(2, weight=1)  # Растяжение третьей кнопки
        self.new_graph_button = self.app.widget_factory.create_button(left_buttons_frame, 'new_graph',
                                                                    self.generate_new_graph, 'new_graph')  # Кнопка нового графа
        self.new_graph_button.grid(row=0, column=0, padx=5, pady=0, sticky='ew')  # Размещение
        self.app.widget_factory.create_button(left_buttons_frame, 'start_fire', self.start_simulation, 'fire').grid(row=0,
                                                                                column=1, padx=5, pady=0, sticky='ew')  # Кнопка запуска
        self.app.widget_factory.create_button(left_buttons_frame, 'reset', self.reset_simulation, 'reset').grid(row=0,
                                                                                column=2, padx=5, pady=0, sticky='ew')  # Кнопка сброса
        right_buttons_frame = self.app.widget_factory.create_frame(buttons_row)  # Правая группа кнопок
        right_buttons_frame.grid(row=0, column=1, sticky='ew')  # Размещение
        right_buttons_frame.columnconfigure(0, weight=1)  # Растяжение первой кнопки
        right_buttons_frame.columnconfigure(1, weight=1)  # Растяжение второй кнопки
        self.app.widget_factory.create_button(right_buttons_frame, 'insert_into_multiple', self.insert_into_multiple,
                                              'insert_multi').grid(row=0, column=0, padx=5, pady=0, sticky='ew')  # Вставка в множественную
        self.app.widget_factory.create_button(right_buttons_frame, 'export_pdf', self.export_data,
                                              'export').grid(row=0, column=1, padx=5, pady=0, sticky='ew')  # Экспорт в pdf
        self._update_new_graph_button_text()  # Обновление текста кнопки
    
    def _create_stats_columns(self, parent, row):
        """Создание колонок со статистикой (с использованием data-ключей)"""
        columns_container = self.app.widget_factory.create_frame(parent)  # Контейнер колонок
        columns_container.grid(row=row, column=0, sticky='nsew')  # Размещение
        columns_container.columnconfigure(0, weight=4, uniform='stats_columns')  # Первая колонка (параметры генерации)
        for i in range(1, 5):  # Остальные колонки
            columns_container.columnconfigure(i, weight=3, uniform='stats_columns')  # Равномерное распределение
        col1 = self.app.widget_factory.create_frame(columns_container)  # Колонка параметров генерации
        col1.grid(row=0, column=0, sticky='nsew', padx=3)  # Размещение
        self.generation_params_frame = col1  # Сохранение фрейма
        self._update_generation_params_column()  # Обновление содержимого
        col2 = self.app.widget_factory.create_frame(columns_container)  # Колонка статистики ребер
        col2.grid(row=0, column=1, sticky='nsew', padx=3)  # Размещение
        edge_data_keys = [  # Список data-ключей для статистики ребер
            'edge_min', 'edge_max', 'edge_mean', 'edge_std', 'edge_median','edge_skewness', 'edge_kurtosis', 'edge_q05', 'edge_q95',
            '', 'edge_count_positive', 'edge_pct_positive', 'edge_sum_positive', 'edge_mean_positive',
            '', 'edge_count_negative', 'edge_pct_negative', 'edge_sum_negative', 'edge_mean_negative']
        self.edge_stats_labels = self.app.widget_factory.create_stat_column(col2, 'edge_stats', edge_data_keys)  # Создание колонки
        
        col3 = self.app.widget_factory.create_frame(columns_container)  # Колонка статистики вершин
        col3.grid(row=0, column=2, sticky='nsew', padx=3)  # Размещение
        vertex_data_keys = [  # Список data-ключей для статистики вершин
            'vertex_min', 'vertex_max', 'vertex_mean', 'vertex_std', 'vertex_median',
            'vertex_skewness', 'vertex_kurtosis', 'vertex_q05', 'vertex_q95']
        self.vertex_stats_labels = self.app.widget_factory.create_stat_column(col3, 'vertex_stats', vertex_data_keys)  # Создание колонки
        
        col4 = self.app.widget_factory.create_frame(columns_container)  # Колонка статистики стартовой вершины
        col4.grid(row=0, column=3, sticky='nsew', padx=3)  # Размещение
        start_vertex_data_keys = [  # Список data-ключей для статистики стартовой вершины
            'start_vertex_weight', 'start_vertex_avg_edge_weight',
            '', 'start_vertex_count_positive', 'start_vertex_pct_positive', 'start_vertex_sum_positive', 'start_vertex_mean_positive',
            '', 'start_vertex_count_negative', 'start_vertex_pct_negative', 'start_vertex_sum_negative', 'start_vertex_mean_negative',
            '', 'start_vertex_resistance_factor', 'start_vertex_influence_factor',]
        self.start_vertex_labels = self.app.widget_factory.create_stat_column(col4, 'start_vertex_stats',
                                                                              start_vertex_data_keys)  # Создание колонки
        
        col5 = self.app.widget_factory.create_frame(columns_container)  # Колонка результатов симуляции
        col5.grid(row=0, column=4, sticky='nsew', padx=3)  # Размещение
        fire_data_keys = [  # Список data-ключей для результатов симуляции
            'fire_total_burned', 'fire_total_iterations',
            '', 'fire_spread_rate_1', 'fire_spread_rate_2', 'fire_spread_rate_3', 'fire_spread_rate_4', 'fire_spread_rate_5',
            '', 'fire_peak_new_burns', 'fire_time_to_peak', 'fire_time_from_peak']
        self.simulation_results_labels = self.app.widget_factory.create_stat_column(col5, 'simulation_results',
                                                                                fire_data_keys)  # Создание колонки
    
    def _update_generation_params_column(self):
        """Полное пересоздание колонки параметров генерации"""
        if not self.generation_params_frame or not self.data:  # Фрейм или данные отсутствуют
            return
        for widget in self.generation_params_frame.winfo_children():  # Удаление старых виджетов
            widget.destroy()
        title = self.app.widget_factory.create_labelframe(self.generation_params_frame, 'generation_params')  # Фрейм с заголовком
        title.pack(fill='both', expand=True)  # Размещение
        content = title.content  # Внутренний контент
        if self.data.generation_params is not None:  # Есть параметры генерации
            params = self.data.generation_params  # Параметры
            edge_dist = params.get('edge_dist', {})  # Параметры ребер
            edge_type = edge_dist.get('type', 'None')  # Тип распределения ребер
            self._add_stat_row(content, 'edge_distribution', self.app.translator.t(edge_type), use_rounding_stats=False)  # Строка типа
            if edge_type not in ('None', 'custom'):  # Не пустой тип
                self._add_distribution_params(content, edge_dist, 'edge', edge_type)  # Параметры распределения
            self.app.widget_factory.create_frame(content).pack(fill='x', pady=5)  # Разделитель
            vertex_dist = params.get('vertex_dist')  # Параметры вершин
            if vertex_dist is not None:  # Распределение вершин задано
                vertex_type = vertex_dist.get('type', 'None')  # Тип распределения вершин
                self._add_stat_row(content, 'vertex_distribution', self.app.translator.t(vertex_type), use_rounding_stats=False)  # Строка типа
                if vertex_type not in ('None', 'custom'):  # Не пустой тип
                    self._add_distribution_params(content, vertex_dist, 'vertex', vertex_type)  # Параметры распределения
            else:  # Распределение вершин не задано
                self._add_stat_row(content, 'vertex_distribution', self.app.translator.t('None'), use_rounding_stats=False)  # Строка "нет"
            self.app.widget_factory.create_frame(content).pack(fill='x', pady=5)  # Разделитель
        else:  # Нет параметров генерации (пользовательский граф)
            self._add_stat_row(content, 'edge_distribution', self.app.translator.t('custom'),
                               use_rounding_stats=False)  # Строка "пользовательский"
            self.app.widget_factory.create_frame(content).pack(fill='x', pady=5)  # Разделитель
            self._add_stat_row(content, 'vertex_distribution', self.app.translator.t('custom'),
                               use_rounding_stats=False)  # Строка "пользовательский"
            self.app.widget_factory.create_frame(content).pack(fill='x', pady=5)  # Разделитель
        self._add_stat_row(content, 'resistance_stat', self.app.translator.t(self.data.resistance_type),
                           use_rounding_stats=False) # Тип устойчивости
        if self.data.resistance_type != 'None':  # Устойчивость активна
            self._add_stat_row(content, 'coeff', self.data.resistance_coeff,
                               use_rounding_stats=False) # Коэффициент устойчивости
        self.app.widget_factory.create_frame(content).pack(fill='x', pady=5)  # Разделитель
        self._add_stat_row(content, 'influence_stat', self.app.translator.t(self.data.influence_type), use_rounding_stats=False) # Тип влияния
        if self.data.influence_type != 'None':  # Влияние активно
            self._add_stat_row(content, 'coeff', self.data.influence_coeff, use_rounding_stats=False) # Коэффициент влияния
        self.app.widget_factory.create_frame(content).pack(fill='x', pady=5)  # Разделитель
        self._add_stat_row(content, 'damping_stat', self.app.translator.t(self.data.damping_type), use_rounding_stats=False)  # Тип затухания
        if self.data.damping_type != 'None':  # Затухание активно
            self._add_stat_row(content, 'coeff', self.data.damping_coeff, use_rounding_stats=False)  # Коэффициент затухания
    
    def _add_stat_row(self, parent, label_key, value, use_rounding_stats=True):
        """Добавление строки статистики в родительский виджет"""
        if isinstance(value, float):  # Вещественное число
            if use_rounding_stats:  # Использовать округление статистик
                rounding = self.app.settings['rounding_stats'].get()  # Точность из настроек
            else:  # Использовать округление ввода
                rounding = self.app.settings['rounding_input'].get()  # Точность из настроек
            value = f"{value:.{rounding}f}"  # Форматирование с округлением
        elif value is None:  # Пустое значение
            value = ""  # Пустая строка
        _, label = self.app.widget_factory.create_stat_row(parent, label_key)  # Создание строки
        label.config(text=str(value))  # Установка текста значения
    
    def _add_distribution_params(self, parent, dist_data, domain, dist_type):
        """Добавление параметров распределения в родительский виджет"""
        try:
            config = PARAM_CONFIG[domain][dist_type]  # Конфигурация распределения
            for param_name in config.get('param_order', []):  # Перебор параметров
                if param_name == 'stages':  # Параметр ступеней
                    stages = dist_data.get('stages', [])  # Список ступеней
                    if stages:  # Ступени существуют
                        self._add_stat_row(parent, 'stages_count', len(stages), use_rounding_stats=False)  # Количество ступеней
                else:  # Обычный параметр
                    value = dist_data.get(param_name)  # Значение параметра
                    if value is not None:  # Значение существует
                        self._add_stat_row(parent, param_name, value, use_rounding_stats=False)  # Строка параметра
        except KeyError:  # Конфигурация не найдена
            pass  # Игнорирование ошибки
    
    def _update_edge_stats_column(self):
        """Обновление значений в колонке статистики ребер"""
        edge_stats, _, _ = self.app.statistics.calculate_all(self.data)  # Вычисление статистик
        for data_key, label in self.edge_stats_labels.items():  # Перебор меток
            if label is not None:  # Метка существует
                value = edge_stats.get(data_key)  # Получение значения
                if value is not None:  # Значение существует
                    label.config(text=self._format_stat_value(value, data_key))  # Обновление текста
    
    def _update_vertex_stats_column(self):
        """Обновление значений в колонке статистики вершин"""
        _, vertex_stats, _ = self.app.statistics.calculate_all(self.data)  # Вычисление статистик
        for data_key, label in self.vertex_stats_labels.items():  # Перебор меток
            if label is not None:  # Метка существует
                value = vertex_stats.get(data_key)  # Получение значения
                if value is not None:  # Значение существует
                    label.config(text=self._format_stat_value(value, data_key))  # Обновление текста
    
    def _update_start_vertex_stats_column(self):
        """Обновление значений в колонке статистики стартовой вершины"""
        vertex_index = self.ui_vars['start_vertex'].get() - 1  # Индекс вершины (0-базовый)
        stats = self.app.statistics.start_vertex_stats(self.data, vertex_index)  # Статистика вершины
        for data_key, label in self.start_vertex_labels.items():  # Перебор меток
            if label is not None:  # Метка существует
                value = stats.get(data_key)  # Получение значения
                if value is not None:  # Значение существует
                    label.config(text=self._format_stat_value(value, data_key))  # Обновление текста
    
    def _update_simulation_results_column(self, result):
        """Обновление колонки результатов симуляции (с использованием data-ключей)"""
        if result is None:  # Результат отсутствует
            for data_key, label in self.simulation_results_labels.items():  # Перебор меток
                if label is not None:  # Метка существует
                    label.config(text='0')  # Сброс значения
            return
        history = result['history']  # История возгораний
        total_burned = len(result['burned_nodes'])  # Количество сгоревших вершин
        total_iters = len(history) - 1  # Количество итераций
        values = {  # Словарь значений
            'fire_total_burned': total_burned,  # Сгоревшие вершины
            'fire_total_iterations': total_iters,  # Количество итераций
        }
        
        for i in range(1, 6):  # Первые 5 шагов
            values[f'fire_spread_rate_{i}'] = history[i] if i < len(history) else 0  # Скорость на шаге i
        if total_iters > 0:  # Было распространение
            peak = max(history[1:])  # Пиковое количество новых возгораний
            peak_time = history[1:].index(peak) + 1  # Время достижения пика
            values['fire_peak_new_burns'] = peak  # Пик
            values['fire_time_to_peak'] = peak_time  # Время до пика
            values['fire_time_from_peak'] = total_iters - peak_time  # Время от пика
        for data_key, label in self.simulation_results_labels.items():  # Перебор меток
            if label is not None:  # Метка существует
                value = values.get(data_key)  # Получение значения
                if value is not None:  # Значение существует
                    label.config(text=str(value))  # Обновление текста
    
    def _update_histograms(self):
        """Обновление гистограмм ребер и вершин"""
        edge_weights = [d['weight'] for _, _, d in self.data.graph.edges(data=True)]  # Сбор весов ребер
        if edge_weights:  # Есть данные
            self.edge_hist.update(edge_weights)  # Обновление гистограммы
        else:  # Нет данных
            self.edge_hist.clear()  # Очистка гистограммы
        vertex_weights = self.data.get_all_vertices()  # Сбор весов вершин
        if vertex_weights:  # Есть данные
            self.vertex_hist.update(vertex_weights)  # Обновление гистограммы
        else:  # Нет данных
            self.vertex_hist.clear()  # Очистка гистограммы
    
    def _update_start_vertex_slider(self):
        """Обновление диапазона слайдера стартовой вершины"""
        n = self.data.graph.number_of_nodes()  # Количество вершин
        if self.start_vertex_slider:  # Слайдер существует
            self.start_vertex_slider.configure(to=n)  # Обновление максимума
        current = self.ui_vars['start_vertex'].get()  # Текущее значение
        if current > n:  # Значение превышает максимум
            self.ui_vars['start_vertex'].set(n)  # Установка максимума
        elif current < 1:  # Значение меньше минимума
            self.ui_vars['start_vertex'].set(1)  # Установка минимума
    
    def _format_stat_value(self, value, key):
        """Форматирование значения статистики для отображения"""
        rounding = self.app.settings['rounding_stats'].get()  # Точность округления
        if 'pct' in key:  # Процентное значение
            return f"{value:.{rounding}f}%"  # Формат с процентом
        if isinstance(value, float):  # Вещественное число
            return f"{value:.{rounding}f}"  # Формат с округлением
        return str(value)  # Строковое представление
    
    def _refresh_ui_from_data(self):
        """Обновление всего интерфейса из self.data"""
        if not self.data or self.data.graph.number_of_nodes() == 0:  # Нет данных
            self.reset_simulation()  # Сброс симуляции
            if self.graph_display:  # Виджет графа существует
                self.graph_display.clear()  # Очистка графа
            return
        
        if self.graph_display:  # Виджет графа существует
            self.graph_display.set_graph_data(self.data)  # Установка данных графа
            self.graph_display.draw()  # Отрисовка графа
        self._update_graph_params_column()  # Обновление параметров графа
        self._update_generation_params_column()  # Обновление параметров генерации
        self._update_edge_stats_column()  # Обновление статистики ребер
        self._update_vertex_stats_column()  # Обновление статистики вершин
        self._update_start_vertex_stats_column()  # Обновление статистики стартовой вершины
        self._update_histograms()  # Обновление гистограмм
        self._update_start_vertex_slider()  # Обновление слайдера
        self._update_new_graph_button_text()  # Обновление текста кнопки
    
    def _get_source_data(self):
        """Возврат копии текущего графа для вставки в другую вкладку"""
        return self.data.copy()  # Копия данных графа
    
    def on_data_changed(self, change_type, **kwargs):
        """Обработчик изменений данных графа"""
        if change_type in ('vertex_changed', 'vertex_added', 'vertex_removed', 'edge_changed'):  # Изменение структуры
            if self.batch_context is not None:  # Режим множественной симуляции
                self.clear_batch_context()  # Очистка контекста
    
    def refresh_histograms(self):
        """Обновление гистограмм (переопределение метода graphtab)"""
        self._update_histograms()  # Вызов внутреннего метода
    
    def start_simulation(self):
        """Запуск симуляции с правильным продвижением seed-а графа"""
        if not self.data or self.data.graph.number_of_nodes() == 0 or self.app.is_fire_running:  # Некорректное состояние
            return
        self.app.is_fire_running = True  # Установка флага выполнения
        try:
            start_vertex = f'V{self.ui_vars["start_vertex"].get() - 1}'  # Имя стартовой вершины
            ignition_method = self.app.settings.get('ignition_method', 'Sequential')  # Метод поджога
            threshold_method = self.app.settings.get('threshold_method', 'None')  # Тип порога
            threshold_value = self.app.settings.get('threshold_value', 0.5)  # Значение порога
            result = self.app.simulation.run(self.data, start_vertex, ignition_method=ignition_method, threshold_method=threshold_method,
                                             threshold_value=threshold_value) # Запуск симуляции
            self._last_simulation_result = result  # Сохранение результата
            if self.graph_display:  # Виджет графа существует
                self.graph_display.set_fire_data(result['burned_nodes'], result['burned_edges'])  # Установка данных пожара
                self.graph_display.draw()  # Отрисовка графа
            self._update_simulation_results_column(result)  # Обновление колонки результатов
        finally:
            self.app.is_fire_running = False  # Сброс флага выполнения
    
    def reset_simulation(self):
        """Сброс симуляции (очистка результатов)"""
        self._last_simulation_result = None  # Сброс результата
        if self.graph_display:  # Виджет графа существует
            self.graph_display.clear_fire()  # Очистка пожара
        self._update_simulation_results_column(None)  # Сброс колонки результатов
    
    def insert_into_multiple(self):
        """Вставка текущего графа в multiplesimtab"""
        self.insert_to_tab(3, 'confirm_replace_multiple', self.app.set_multiple_data)  # Вызов универсального метода
    
    def export_data(self):
        """Экспорт текущего состояния в pdf файл"""
        PDFExporter(self.app, self).export()  # Вызов экспортера
    
    def receive_data(self, new_data):
        """Получение нового графа из другой вкладки"""
        self.data = new_data  # Сохранение новых данных
        self.clear_batch_context()  # Очистка контекста
        self._last_simulation_result = None  # Сброс результата
        if self.graph_display:  # Виджет графа существует
            self.graph_display.clear_fire()  # Очистка пожара
            self.graph_display.set_graph_data(self.data)  # Установка данных графа
            self.graph_display.draw()  # Отрисовка графа
        self._refresh_ui_from_data()  # Обновление интерфейса
        self._update_simulation_results_column(None)  # Сброс колонки результатов

    def refresh_all_stats(self):
        """Обновление всех статистик (вызывается при изменении rounding_stats)"""
        self._update_graph_params_column()  # Обновление параметров графа
        self._update_generation_params_column()  # Обновление параметров генерации
        self._update_edge_stats_column()  # Обновление статистики ребер
        self._update_vertex_stats_column()  # Обновление статистики вершин
        self._update_start_vertex_stats_column()  # Обновление статистики стартовой вершины
        if self._last_simulation_result:  # Результат существует
            self._update_simulation_results_column(self._last_simulation_result)  # Обновление колонки результатов


# In[43]:


class MultipleSimTab(GraphTab):
    """Вкладка множественной симуляции"""
    
    tab_key = 'tab_multiple'  # Ключ для перевода названия вкладки
    
    def __init__(self, parent, app):
        """Инициализация вкладки множественной симуляции"""
        super().__init__(parent, app)  # Вызов конструктора родительского класса
        self.data = app.multiple_data  # Данные графа для множественной симуляции
        self._saved_result_rows = None  # Сохраненные строки результатов
        self.ui_vars = {  # Ui переменные параметров
            'batch_graphs_count': tk.IntVar(value=1),  # Количество графов
            'batch_start_vertices_count': tk.IntVar(value=5),  # Количество стартовых вершин
            'batch_simulations_per_vertex': tk.IntVar(value=1),  # Количество симуляций на вершину
        }
        self.is_running = False  # Флаг выполнения симуляции
        self.current_batch_index = 0  # Индекс текущего графа в пакете
        self.batch_params_list = []  # Список параметров для каждого графа
        self.results = []  # Список результатов
        self.graphs_count_frame = None  # Фрейм выбора количества графов (для сгенерированных)
        self.graphs_count_custom_frame = None  # Фрейм отображения (для пользовательского)
        self.graphs_count_slider = None  # Слайдер количества графов
        self.graphs_count_entry = None  # Поле ввода количества графов
        self.start_count_slider = None  # Слайдер количества стартовых вершин
        self.start_count_entry = None  # Поле ввода количества стартовых вершин
        self.simulations_slider = None  # Слайдер количества симуляций
        self.simulations_entry = None  # Поле ввода количества симуляций
        self.total_info_label = None  # Метка общего количества генераций
        self.start_button = None  # Кнопка запуска
        self.stop_button = None  # Кнопка остановки
        self.progress = None  # Прогресс-бар
        self.results_container = None  # Контейнер результатов
        self.result_rows = []  # Список строк результатов
        self.all_graphs_row = None  # Строка "все графы"
        self.start_vertices_table = None  # Таблица стартовых вершин
        self.param_widgets = []  # Список виджетов параметров для блокировки
        self.current_graph_vertices = 0  # Текущее количество вершин в графе
    
    def _is_custom_graph(self):
        """Проверка, является ли текущий граф пользовательским (не сгенерированным)"""
        return self.data.generation_params is None  # Отсутствие параметров генерации
    
    def _update_graphs_count_ui(self):
        """Обновление интерфейса для блока количества графов в зависимости от типа"""
        is_custom = self._is_custom_graph()  # Проверка типа графа
        if is_custom:  # Пользовательский граф
            if self.graphs_count_frame and self.graphs_count_frame.winfo_exists():  # Фрейм существует
                self.graphs_count_frame.grid_remove()  # Скрытие фрейма
            if self.graphs_count_custom_frame and self.graphs_count_custom_frame.winfo_exists():  # Фрейм существует
                self.graphs_count_custom_frame.grid()  # Показ фрейма
        else:  # Сгенерированный граф
            if self.graphs_count_custom_frame and self.graphs_count_custom_frame.winfo_exists():  # Фрейм существует
                self.graphs_count_custom_frame.grid_remove()  # Скрытие фрейма
            if self.graphs_count_frame and self.graphs_count_frame.winfo_exists():  # Фрейм существует
                self.graphs_count_frame.grid()  # Показ фрейма
    
    def _update_total_generations(self):
        """Обновление текста с общим количеством генераций"""
        if self._is_custom_graph():  # Пользовательский граф
            graphs_count = 1  # Только один граф
        else:  # Сгенерированный граф
            graphs_count = self.ui_vars['batch_graphs_count'].get()  # Количество из ui
        start_count = self.ui_vars['batch_start_vertices_count'].get()  # Количество стартовых вершин
        sim_count = self.ui_vars['batch_simulations_per_vertex'].get()  # Количество симуляций
        total = graphs_count * start_count * sim_count  # Общее количество
        
        if self.total_info_label and self.total_info_label.winfo_exists():  # Метка существует
            self.total_info_label.config(text=f"{self.app.translator.t('total_generations')}: {graphs_count} × {start_count} × {sim_count} = {total}")  # Обновление текста
    
    def _collect_batch_params(self):
        """Сбор параметров для всех генераций в пакете"""
        is_custom = self._is_custom_graph()  # Проверка типа графа
        if is_custom:  # Пользовательский граф
            graphs_count = 1  # Только один граф
        else:  # Сгенерированный граф
            graphs_count = self.ui_vars['batch_graphs_count'].get()  # Количество из ui
        start_vertices = self.start_vertices_table.get_values() if self.start_vertices_table else []  # Стартовые вершины
        simulations_per_vertex = self.ui_vars['batch_simulations_per_vertex'].get()  # Количество симуляций
        params_list = []  # Список параметров
        for graph_idx in range(graphs_count):  # Цикл по графам
            if is_custom:  # Пользовательский граф
                graph_data = self.data  # Данные текущего графа
                need_generate = False  # Генерация не требуется
                generate_params = None  # Параметры генерации отсутствуют
            else:  # Сгенерированный граф
                if self.data.generation_params is None:  # Нет параметров генерации
                    graph_data = self.data  # Использование текущих данных
                    need_generate = False  # Генерация не требуется
                    generate_params = None  # Параметры генерации отсутствуют
                else:  # Параметры существуют
                    generate_params = copy.deepcopy(self.data.generation_params)  # Глубокое копирование параметров
                    graph_data = None  # Данные будут сгенерированы
                    need_generate = True  # Генерация требуется
            params_list.append({  # Добавление параметров
                'graph_index': graph_idx + 1,  # Индекс графа (1-базовый)
                'graph_data': graph_data,  # Данные графа
                'need_generate': need_generate,  # Флаг необходимости генерации
                'start_vertices': start_vertices.copy(),  # Копия списка стартовых вершин
                'simulations_per_vertex': simulations_per_vertex,  # Количество симуляций
                'generate_params': generate_params  # Параметры для генерации
            })
        return params_list
    
    def _generate_graph(self, params):
        """Генерация графа по параметрам с правильной инициализацией seed-а"""
        if not params['need_generate']:  # Генерация не требуется
            new_data = params['graph_data'].copy()  # Копирование существующего графа
            return new_data
        new_data = self.app.generate_graph_from_params(params['generate_params'])  # Генерация графа
        new_data.resistance_type = self.data.resistance_type  # Копирование типа устойчивости
        new_data.resistance_coeff = self.data.resistance_coeff  # Копирование коэффициента устойчивости
        new_data.influence_type = self.data.influence_type  # Копирование типа влияния
        new_data.influence_coeff = self.data.influence_coeff  # Копирование коэффициента влияния
        new_data.damping_type = self.data.damping_type  # Копирование типа затухания
        new_data.damping_coeff = self.data.damping_coeff  # Копирование коэффициента затухания
        return new_data
    
    def _run_simulations_for_graph(self, graph_data, params):
        """Запуск всех симуляций для одного графа с продвижением seed-а"""
        results = []  # Список результатов
        start_vertices = params['start_vertices']  # Стартовые вершины
        sims_per_vertex = params['simulations_per_vertex']  # Количество симуляций на вершину
        progress_mode = self.app.settings['batch_progress_update_mode'].get()  # Режим обновления прогресса
        for start_vertex in start_vertices:  # Цикл по стартовым вершинам
            node = f'V{start_vertex - 1}'  # Имя вершины
            if node not in graph_data.graph.nodes:  # Вершина не существует
                continue
            for sim_num in range(1, sims_per_vertex + 1):  # Цикл по симуляциям
                if not self.is_running:  # Симуляция остановлена
                    return results
                sim_result = self.app.simulation.run(graph_data, node)  # Запуск симуляции
                results.append({  # Добавление результата
                    'start_vertex': start_vertex,  # Стартовая вершина
                    'simulation_num': sim_num,  # Номер симуляции
                    'result': sim_result  # Результат
                })
                if progress_mode == 'progress_per_vertex':  # Обновление после каждой вершины
                    self._update_progress(1)
            if progress_mode == 'progress_per_graph' and len(results) > 0:  # Обновление после графа
                self._update_progress(sims_per_vertex)  # Увеличение прогресса на количество симуляций
        return results
    
    def _add_result_row(self, graph_index, graph_data, simulations):
        """Добавление строки в таблицу результатов с равномерным делением на 5 колонок"""
        row = self.app.widget_factory.create_frame(self.results_container)  # Фрейм строки
        row.pack(fill='x', pady=2)  # Размещение
        weights = [1, 1, 3, 3, 3]  # Пропорции колонок: граф, seed, вставить, экспорт, итоги
        for i, weight in enumerate(weights):  # Настройка колонок
            row.columnconfigure(i, weight=weight, uniform='result_col')
        label = self.app.widget_factory.create_label(row, 'graph_label', 'normal')  # Метка с номером графа
        label.config(text=self.app.translator.t('graph_label').format(graph_index))  # Текст "g {index}"
        label.grid(row=0, column=0, padx=5, pady=(5,0), sticky='ew')  # Размещение
        seed_value = graph_data.graph_seed if graph_data.graph_seed is not None else '—'  # Значение seed
        seed_text = f"seed {seed_value}" if seed_value != '—' else 'seed —'  # Текст seed
        seed_label = self.app.widget_factory.create_label(row, '', 'normal')  # Метка seed
        seed_label.config(text=seed_text)  # Установка текста
        seed_label.grid(row=0, column=1, padx=5, pady=(5,0), sticky='ew')  # Размещение
        graph_data.graph_index = graph_index  # Сохранение индекса графа в данных
        
        insert_btn = self.app.widget_factory.create_button(row, 'insert_into_simulation',
                            lambda g=graph_data: self._insert_graph_to_simulation(g), 'insert_sim_compact') # Кнопка вставки в симуляцию
        insert_btn.grid(row=0, column=2, padx=5, pady=(5,0), sticky='ew')  # Размещение
        export_btn = self.app.widget_factory.create_button(row, 'export_csv',
                            lambda: self._export_graph_data(graph_index, graph_data, simulations),'export_compact') # Кнопка экспорта
        export_btn.grid(row=0, column=3, padx=5, pady=(5,0), sticky='ew')  # Размещение
        view_btn = self.app.widget_factory.create_button(row, 'view_results',
                            lambda: self._view_graph_results(graph_index, graph_data, simulations),'batch_view_compact')# Кнопка просмотра итогов
        view_btn.grid(row=0, column=4, padx=5, pady=(5,0), sticky='ew')  # Размещение
        row.graph_index = graph_index  # Сохранение индекса
        row.graph_data = graph_data  # Сохранение данных графа
        row.simulations = simulations  # Сохранение симуляций
        row.insert_btn = insert_btn  # Сохранение кнопки вставки
        row.export_btn = export_btn  # Сохранение кнопки экспорта
        row.view_btn = view_btn  # Сохранение кнопки просмотра
        self.result_rows.append(row)  # Добавление строки в список
        if self.is_running:  # Генерация запущена
            insert_btn.grid_remove()  # Скрытие кнопки вставки
            export_btn.grid_remove()  # Скрытие кнопки экспорта
            view_btn.grid_remove()  # Скрытие кнопки просмотра
    
    def _update_buttons_visibility(self):
        """Обновление видимости всех кнопок в строках результатов"""
        for row in self.result_rows:  # Перебор строк
            if row and row.winfo_exists():  # Строка существует
                if hasattr(row, 'insert_btn') and row.insert_btn.winfo_exists():  # Кнопка вставки
                    if self.is_running:  # Симуляция запущена
                        row.insert_btn.grid_remove()  # Скрытие кнопки
                    else:  # Симуляция остановлена
                        row.insert_btn.grid()  # Показ кнопки
                if hasattr(row, 'export_btn') and row.export_btn.winfo_exists():  # Кнопка экспорта
                    if self.is_running:  # Симуляция запущена
                        row.export_btn.grid_remove()  # Скрытие кнопки
                    else:  # Симуляция остановлена
                        row.export_btn.grid()  # Показ кнопки
                if hasattr(row, 'view_btn') and row.view_btn.winfo_exists():  # Кнопка просмотра
                    if self.is_running:  # Симуляция запущена
                        row.view_btn.grid_remove()  # Скрытие кнопки
                    else:  # Симуляция остановлена
                        row.view_btn.grid()  # Показ кнопки
    
    def _hide_all_graphs_row(self):
        """Скрытие строки 'все графы'"""
        if self.all_graphs_row and self.all_graphs_row.winfo_exists():  # Строка существует
            self.all_graphs_row.pack_forget()  # Скрытие
    
    def _show_all_graphs_row(self):
        """Показ строки 'все графы' в конце таблицы"""
        if self.all_graphs_row and self.all_graphs_row.winfo_exists():  # Строка существует
            self.all_graphs_row.pack_forget()  # Скрытие для повторного добавления
            self.all_graphs_row.pack(fill='x', pady=2)  # Показ в конце
    
    def _update_all_graphs_row_state(self):
        """Обновление состояния кнопок в строке 'все графы'"""
        if not self.all_graphs_row or not self.all_graphs_row.winfo_exists():  # Строка не существует
            return
        has_results = len(self.result_rows) > 0  # Есть результаты
        if hasattr(self.all_graphs_row, 'export_btn') and self.all_graphs_row.export_btn.winfo_exists():  # Кнопка экспорта
            if has_results:  # Есть результаты
                self.all_graphs_row.export_btn.config(state='normal')  # Активация
            else:  # Нет результатов
                self.all_graphs_row.export_btn.config(state='disabled')  # Деактивация
        if hasattr(self.all_graphs_row, 'view_btn') and self.all_graphs_row.view_btn.winfo_exists():  # Кнопка просмотра
            if has_results:  # Есть результаты
                self.all_graphs_row.view_btn.config(state='normal')  # Активация
            else:  # Нет результатов
                self.all_graphs_row.view_btn.config(state='disabled')  # Деактивация
    
    def _create_all_graphs_row(self):
        """Создание строки 'все графы' с равномерным делением на 5 колонок"""
        row = self.app.widget_factory.create_frame(self.results_container)  # Фрейм строки
        weights = [1, 1, 3, 3, 3]  # Пропорции колонок
        for i, weight in enumerate(weights):  # Настройка колонок
            row.columnconfigure(i, weight=weight, uniform='result_col')
        label = self.app.widget_factory.create_label(row, 'all_graphs', 'normal')  # Метка "все графы"
        label.grid(row=0, column=0, padx=5, pady=(5,0), sticky='ew')  # Размещение
        empty_frame = self.app.widget_factory.create_frame(row)  # Пустой фрейм для колонки 1
        empty_frame.grid(row=0, column=1, padx=5, pady=(5,0), sticky='ew')  # Размещение
        empty_frame2 = self.app.widget_factory.create_frame(row)  # Пустой фрейм для колонки 2
        empty_frame2.grid(row=0, column=2, padx=5, pady=(5,0), sticky='ew')  # Размещение
        
        export_btn = self.app.widget_factory.create_button(row, 'export_all',self._export_all_data,'export_compact')# Кнопка экспорта всех
        export_btn.grid(row=0, column=3, padx=5, pady=(5,0), sticky='ew')  # Размещение
        view_btn = self.app.widget_factory.create_button(row, 'view_all_results',self._view_all_results,'batch_view_compact')# Кнопка просмотра всех итогов
        view_btn.grid(row=0, column=4, padx=5, pady=(5,0), sticky='ew')  # Размещение
        row.export_btn = export_btn  # Сохранение кнопки экспорта
        row.view_btn = view_btn  # Сохранение кнопки просмотра
        self.all_graphs_row = row  # Сохранение строки
        self.all_graphs_row.pack_forget()  # Изначально скрыта
    
    def _insert_graph_to_simulation(self, graph_data):
        """Вставка графа в единичную симуляцию"""
        if self.is_running:  # Симуляция запущена
            return
        copied_graph = graph_data.copy()  # Копирование графа
        if hasattr(graph_data, 'graph_index') and graph_data.graph_index:  # Индекс существует
            copied_graph.source_graph_index = graph_data.graph_index  # Сохранение индекса
        self.app.set_simulation_data(copied_graph)  # Установка данных в симуляцию
        sim_tab = self.app.tab_manager.tab_instances[2]  # Вкладка симуляции
        if sim_tab and sim_tab.data:  # Вкладка существует
            sim_tab.data.source_tab = 'tab_multiple'  # Источник - множественная симуляция
            if hasattr(graph_data, 'graph_index') and graph_data.graph_index:  # Индекс существует
                sim_tab.data.source_graph_index = graph_data.graph_index  # Сохранение индекса
            sim_tab.data.insert_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # Время вставки
            sim_tab._update_source_info()  # Обновление информации об источнике
            row_index = None  # Поиск индекса строки
            for i, row in enumerate(self.result_rows):  # Перебор строк
                if hasattr(row, 'graph_index') and row.graph_index == graph_data.graph_index:  # Совпадение индекса
                    row_index = i  # Сохранение индекса
                    break
            sim_tab.set_batch_context(self, graph_data.graph_index, row_index)  # Установка контекста
        self.app.tab_manager.activate_tab(2)  # Активация вкладки симуляции
    
    def _export_graph_data(self, graph_index, graph_data, simulations):
        """Экспорт одного графа в csv"""
        CSVExporter(self.app, self).export_single_graph(graph_index)  # Вызов экспортера
    
    def _view_graph_results(self, graph_index, graph_data, simulations):
        """Просмотр итогов одного графа"""
        self.show_results(graph_index=graph_index)  # Показ окна итогов
    
    def _export_all_data(self):
        """Экспорт всех графов в csv"""
        CSVExporter(self.app, self).export_all_graphs()  # Вызов экспортера
    
    def _view_all_results(self):
        """Просмотр итогов всех графов"""
        self.show_results(graph_index=None)  # Показ окна итогов
    
    def _update_progress(self, increment):
        """Обновление прогресс-бара"""
        if self.progress and self.progress.winfo_exists():  # Прогресс-бар существует
            self.progress['value'] += increment  # Увеличение значения
            self.app.root.update_idletasks()  # Обновление интерфейса
    
    def _update_ui_for_state(self):
        """Обновление интерфейса на основе состояния is_running"""
        if self.is_running:  # Состояние running
            if self.start_button and self.start_button.winfo_exists():  # Кнопка запуска
                self.start_button.grid_remove()  # Скрытие кнопки запуска
            if self.stop_button and self.stop_button.winfo_exists():  # Кнопка остановки
                self.stop_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))  # Показ кнопки остановки
            self._set_ui_enabled(False)  # Блокировка параметров
            self._hide_all_graphs_row()  # Скрытие строки "все графы"
            self._update_buttons_visibility()  # Скрытие кнопок в строках
        else:  # Состояние idle
            if self.stop_button and self.stop_button.winfo_exists():  # Кнопка остановки
                self.stop_button.grid_remove()  # Скрытие кнопки остановки
            if self.start_button and self.start_button.winfo_exists():  # Кнопка запуска
                self.start_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))  # Показ кнопки запуска
            self._set_ui_enabled(True)  # Разблокировка параметров
            self._update_buttons_visibility()  # Показ кнопок в строках
            if len(self.result_rows) > 0:  # Есть результаты
                self._show_all_graphs_row()  # Показ строки "все графы"
                self._update_all_graphs_row_state()  # Обновление состояния кнопок
        self.app.root.update_idletasks()  # Обновление интерфейса
        self.app.root.update()  # Принудительное обновление
    
    def _set_ui_enabled(self, enabled):
        """Блокировка или разблокировка элементов управления на вкладке"""
        state = 'normal' if enabled else 'disabled'  # Состояние виджетов
        self.app.set_batch_running(not enabled)  # Уведомление приложения
        for widget in self.param_widgets:  # Перебор виджетов параметров
            if widget and widget.winfo_exists():  # Виджет существует
                try:
                    widget.config(state=state)  # Установка состояния
                except:  # Игнорирование ошибок
                    pass
        if self.start_vertices_table:  # Таблица стартовых вершин существует
            self.start_vertices_table.set_editable(enabled)  # Установка редактируемости
    
    def start_batch(self):
        """Запуск пакетной симуляции"""
        if self.is_running:  # Уже запущена
            return
        for row in self.result_rows:  # Очистка предыдущих результатов
            if row and row.winfo_exists():  # Строка существует
                row.destroy()
        self.result_rows = []  # Сброс списка строк
        self._hide_all_graphs_row()  # Скрытие строки "все графы"
        self.is_running = True  # Установка флага выполнения
        self._update_ui_for_state()  # Обновление интерфейса
        self.batch_params_list = self._collect_batch_params()  # Сбор параметров
        total_simulations = 0  # Расчет общего количества симуляций
        for params in self.batch_params_list:  # Перебор параметров
            total_simulations += len(params['start_vertices']) * params['simulations_per_vertex']  # Суммирование
        if self.progress and self.progress.winfo_exists():  # Прогресс-бар существует
            self.progress['maximum'] = total_simulations if total_simulations > 0 else 1  # Максимум
            self.progress['value'] = 0  # Сброс значения
        if total_simulations == 0:  # Нет симуляций
            self._on_batch_complete()  # Завершение
            return
        self.current_batch_index = 0  # Сброс индекса
        self._process_next_graph()  # Запуск обработки
    
    def stop_batch(self):
        """Остановка пакетной симуляции"""
        if not self.is_running:  # Не запущена
            return
        self.is_running = False  # Сброс флага
        self._update_ui_for_state()  # Обновление интерфейса
    
    def _process_next_graph(self):
        """Обработка следующего графа в очереди"""
        if not self.is_running:  # Симуляция остановлена
            return
        if self.current_batch_index >= len(self.batch_params_list):  # Все графы обработаны
            self._on_batch_complete()  # Завершение
            return
        params = self.batch_params_list[self.current_batch_index]  # Текущие параметры
        try:
            graph_data = self._generate_graph(params)  # Генерация графа
            if not self.is_running:  # Проверка остановки
                return
            simulations = self._run_simulations_for_graph(graph_data, params)  # Запуск симуляций
            if not self.is_running:  # Проверка остановки
                return
            self._add_result_row(params['graph_index'], graph_data, simulations)  # Добавление строки
        except Exception as e:  # Ошибка обработки
            print(f"Ошибка при обработке графа {params['graph_index']}: {e}")
        self.current_batch_index += 1  # Увеличение индекса
        self.app.root.after(10, self._process_next_graph)  # Задержка перед следующим
    
    def _on_batch_complete(self):
        """Вызов при завершении всех симуляций"""
        if not self.is_running:  # Была остановка
            return
        self.is_running = False  # Сброс флага
        self._update_ui_for_state()  # Обновление интерфейса
    
    def receive_data(self, new_data):
        """Получение нового графа из другой вкладки"""
        if self.is_running:  # Симуляция запущена
            return
        self.data = new_data  # Сохранение данных
        self.current_graph_vertices = self.data.graph.number_of_nodes()  # Обновление количества вершин
        for row in self.result_rows:  # Очистка результатов
            if row and row.winfo_exists():  # Строка существует
                row.destroy()
        self.result_rows = []  # Сброс списка строк
        self._hide_all_graphs_row()  # Скрытие строки "все графы"
        max_vertices = max(1, self.current_graph_vertices)  # Максимальное количество вершин
        if hasattr(self, 'start_count_slider') and self.start_count_slider.winfo_exists():  # Слайдер существует
            self.start_count_slider.config(to=max_vertices)  # Обновление максимума
        if self.start_vertices_table:  # Таблица существует
            count = self.ui_vars['batch_start_vertices_count'].get()  # Количество ячеек
            self.start_vertices_table.set_count(count, self.current_graph_vertices)  # Установка
        self._update_graphs_count_ui()  # Обновление интерфейса количества графов
        if self.progress and self.progress.winfo_exists():  # Прогресс-бар существует
            self.progress['value'] = 0  # Сброс значения
        if hasattr(self, 'graphs_count_slider') and self.graphs_count_slider.winfo_exists():  # Слайдер графов
            max_val = self.app.settings['max_batch_graphs'].get()  # Максимальное значение
            self.graphs_count_slider.config(to=max_val)  # Обновление максимума
        if hasattr(self, 'simulations_slider') and self.simulations_slider.winfo_exists():  # Слайдер симуляций
            max_val = self.app.settings['max_batch_simulations'].get()  # Максимальное значение
            self.simulations_slider.config(to=max_val)  # Обновление максимума
        self._update_ui_for_state()  # Обновление интерфейса
    
    def load_data_to_ui(self):
        """Загрузка данных из self.data в ui"""
        self.current_graph_vertices = self.data.graph.number_of_nodes()  # Количество вершин
        max_vertices = max(1, self.current_graph_vertices)  # Максимальное количество
        if hasattr(self, 'start_count_slider') and self.start_count_slider.winfo_exists():  # Слайдер существует
            self.start_count_slider.config(to=max_vertices)  # Обновление максимума
        if self.start_vertices_table:  # Таблица существует
            count = self.ui_vars['batch_start_vertices_count'].get()  # Количество ячеек
            self.start_vertices_table.set_count(count, self.current_graph_vertices)  # Установка
        self._update_graphs_count_ui()  # Обновление интерфейса количества графов
        if hasattr(self, 'graphs_count_slider') and self.graphs_count_slider.winfo_exists():  # Слайдер графов
            max_val = self.app.settings['max_batch_graphs'].get()  # Максимальное значение
            self.graphs_count_slider.config(to=max_val)  # Обновление максимума
        if hasattr(self, 'simulations_slider') and self.simulations_slider.winfo_exists():  # Слайдер симуляций
            max_val = self.app.settings['max_batch_simulations'].get()  # Максимальное значение
            self.simulations_slider.config(to=max_val)  # Обновление максимума
        self._update_ui_for_state()  # Обновление интерфейса
    
    def refresh_display(self):
        """Обновление отображения при изменении данных"""
        if self.data and self.data.graph:  # Данные существуют
            self.current_graph_vertices = self.data.graph.number_of_nodes()  # Количество вершин
            if self.start_vertices_table:  # Таблица существует
                count = self.ui_vars['batch_start_vertices_count'].get()  # Количество ячеек
                self.start_vertices_table.set_count(count, self.current_graph_vertices)  # Установка
            self._update_graphs_count_ui()  # Обновление интерфейса
            max_vertices = max(1, self.current_graph_vertices)  # Максимальное количество
            if hasattr(self, 'start_count_slider') and self.start_count_slider.winfo_exists():  # Слайдер существует
                self.start_count_slider.config(to=max_vertices)  # Обновление максимума
    
    def on_activate(self):
        """Вызов при активации вкладки"""
        self.data = self.app.multiple_data  # Обновление данных из приложения
        self.load_data_to_ui()  # Загрузка в ui
    
    def build(self):
        """Создание интерфейса вкладки множественной симуляции"""
        scroll = ScrollableFrame(self.frame, self.app.widget_factory)  # Прокручиваемый фрейм
        scroll.pack(fill='both', expand=True)  # Размещение
        content = scroll.inner  # Внутренний контент
        content.columnconfigure(0, weight=1)  # Растяжение колонки
        main_container = self.app.widget_factory.create_frame(content)  # Главный контейнер
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)  # Размещение
        main_container.columnconfigure(0, weight=1)  # Растяжение колонки
        current_row = 0  # Текущая строка
        self.params_frame = self.app.widget_factory.create_labelframe(main_container, 'batch_generation_params')  # Фрейм параметров
        self.params_frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 75))  # Размещение
        current_row += 1  # Увеличение строки
        params_content = self.params_frame.content  # Внутренний контент
        params_content.columnconfigure(0, weight=0, minsize=180)  # Колонка лейблов
        params_content.columnconfigure(1, weight=1)  # Колонка элементов управления
        row_index = 0  # Строка внутри params_content
        label_graphs = self.app.widget_factory.create_label(params_content, 'batch_graphs_count', 'normal')  # Лейбл количества графов
        label_graphs.grid(row=row_index, column=0, sticky='w', pady=(0, 20))  # Размещение
        graphs_container = self.app.widget_factory.create_frame(params_content)  # Контейнер для выбора
        graphs_container.grid(row=row_index, column=1, sticky='ew', padx=(10, 0), pady=(0, 20))  # Размещение
        self.graphs_count_frame = self.app.widget_factory.create_frame(graphs_container)  # Фрейм для сгенерированных
        self.graphs_count_frame.pack(fill='x', expand=True)  # Размещение
        graphs_controls = self.app.widget_factory.create_frame(self.graphs_count_frame)  # Фрейм управления
        graphs_controls.pack(side='left')  # Размещение
        
        entry = self.app.widget_factory.create_entry(graphs_controls, self.ui_vars['batch_graphs_count'], size='default',
                                            param_name='batch_graphs_count', dist_type='global', domain='global')  # Поле ввода
        entry.pack(side='left', padx=(0, 10))  # Размещение
        self.graphs_count_entry = entry  # Сохранение
        self.param_widgets.append(entry)  # Добавление в список для блокировки
        cfg = self.app.validator.get_param_config('global', 'global', 'batch_graphs_count')  # Конфигурация параметра
        from_val, to_val = cfg['range'] if cfg else (1, 75)  # Диапазон значений
        scale = self.app.widget_factory.create_scale(graphs_controls, self.ui_vars['batch_graphs_count'], 
                                                     from_=from_val, to_=to_val, size='long')  # Слайдер
        scale.pack(side='left', fill='x', expand=True)  # Размещение
        self.graphs_count_slider = scale  # Сохранение
        self.param_widgets.append(scale)  # Добавление в список для блокировки
        self.graphs_count_custom_frame = self.app.widget_factory.create_frame(graphs_container)  # Фрейм для пользовательского
        self.graphs_count_custom_frame.pack(fill='x', expand=True)  # Размещение
        value_label_custom = self.app.widget_factory.create_label(self.graphs_count_custom_frame, '', 'normal')  # Метка значения
        value_label_custom.config(text='1')  # Текст "1"
        value_label_custom.pack(side='right')  # Размещение справа
        self.graphs_count_frame.pack_forget()  # Изначальное скрытие
        self.graphs_count_custom_frame.pack_forget()  # Изначальное скрытие
        row_index += 1  # Увеличение строки
        label_start_count = self.app.widget_factory.create_label(params_content,
                                                    'batch_start_vertices_count', 'normal')  # Лейбл количества стартовых вершин
        label_start_count.grid(row=row_index, column=0, sticky='w', pady=(20, 0))  # Размещение
        start_count_container = self.app.widget_factory.create_frame(params_content)  # Контейнер
        start_count_container.grid(row=row_index, column=1, sticky='ew', padx=(10, 0), pady=(20, 0))  # Размещение
        start_count_controls = self.app.widget_factory.create_frame(start_count_container)  # Фрейм управления
        start_count_controls.pack(side='left')  # Размещение
        start_count_entry = self.app.widget_factory.create_entry(start_count_controls, self.ui_vars['batch_start_vertices_count'],
                                size='default', param_name='batch_start_vertices_count', dist_type='global', domain='global')  # Поле ввода
        start_count_entry.pack(side='left', padx=(0, 10))  # Размещение
        self.start_count_entry = start_count_entry  # Сохранение
        self.param_widgets.append(start_count_entry)  # Добавление в список для блокировки
        cfg = self.app.validator.get_param_config('global', 'global', 'batch_start_vertices_count')  # Конфигурация
        from_val, to_val = cfg['range'] if cfg else (1, 20)  # Диапазон
        start_count_scale = self.app.widget_factory.create_scale(start_count_controls, self.ui_vars['batch_start_vertices_count'],
                                                                 from_=from_val, to_=to_val, size='long')  # Слайдер
        start_count_scale.pack(side='left', fill='x', expand=True)  # Размещение
        self.start_count_slider = start_count_scale  # Сохранение
        self.param_widgets.append(start_count_scale)  # Добавление
        row_index += 1  # Увеличение строки
        
        start_vertices_label = self.app.widget_factory.create_label(params_content,
                                                    'batch_start_vertices', 'normal')  # Лейбл "номера стартовых вершин"
        start_vertices_label.grid(row=row_index, column=0, sticky='w', pady=(20, 0))  # Размещение
        table_container = self.app.widget_factory.create_frame(params_content,
                               height=self.app.size_config['container']['start_vertices_table']['height'])  # Контейнер таблицы
        table_container.grid(row=row_index, column=1, sticky='ew', padx=(10, 0), pady=(20, 0))  # Размещение
        table_container.pack_propagate(False)  # Запрет изменения размера
        self.start_vertices_table = StartVerticesTable(table_container, self.app.widget_factory, self.app)  # Таблица
        self.start_vertices_table.container.pack(fill='both', expand=True)  # Размещение
        initial_count = self.ui_vars['batch_start_vertices_count'].get()  # Начальное количество
        self.start_vertices_table.set_count(initial_count, self.current_graph_vertices or 20)  # Установка
        row_index += 1  # Увеличение строки
        label_sims = self.app.widget_factory.create_label(params_content, 'batch_simulations_per_vertex', 'normal')  # Лейбл количества симуляций
        label_sims.grid(row=row_index, column=0, sticky='w', pady=(20, 0))  # Размещение
        sims_container = self.app.widget_factory.create_frame(params_content)  # Контейнер
        sims_container.grid(row=row_index, column=1, sticky='ew', padx=(10, 0), pady=(20, 0))  # Размещение
        sims_controls = self.app.widget_factory.create_frame(sims_container)  # Фрейм управления
        sims_controls.pack(side='left')  # Размещение
        sims_entry = self.app.widget_factory.create_entry(sims_controls, self.ui_vars['batch_simulations_per_vertex'],
                          size='default', param_name='batch_simulations_per_vertex', dist_type='global', domain='global')  # Поле ввода
        sims_entry.pack(side='left', padx=(0, 10))  # Размещение
        self.simulations_entry = sims_entry  # Сохранение
        self.param_widgets.append(sims_entry)  # Добавление
        cfg = self.app.validator.get_param_config('global', 'global', 'batch_simulations_per_vertex')  # Конфигурация
        from_val, to_val = cfg['range'] if cfg else (1, 100)  # Диапазон
        sims_scale = self.app.widget_factory.create_scale(sims_controls, self.ui_vars['batch_simulations_per_vertex'],
                                                          from_=from_val, to_=to_val, size='long')  # Слайдер
        sims_scale.pack(side='left', fill='x', expand=True)  # Размещение
        self.simulations_slider = sims_scale  # Сохранение
        self.param_widgets.append(sims_scale)  # Добавление
        row_index += 1  # Увеличение строки
        info_frame = self.app.widget_factory.create_frame(main_container)  # Фрейм информации
        info_frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 20))  # Размещение
        current_row += 1  # Увеличение строки
        self.total_info_label = self.app.widget_factory.create_label(info_frame, '', 'normal')  # Метка
        self.total_info_label.pack(side='left')  # Размещение
        self._update_total_generations()  # Обновление текста
        controls_frame = self.app.widget_factory.create_frame(main_container)  # Фрейм кнопок и прогресса
        controls_frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 100))  # Размещение
        current_row += 1  # Увеличение строки
        
        for i in range(6):  # Шесть колонок
            controls_frame.columnconfigure(i, weight=1, uniform='control_col')  # Равномерное распределение
        self.start_button = self.app.widget_factory.create_button(controls_frame, 'start_fire', self.start_batch, 'fire')# Кнопка запуска
        self.start_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))  # Размещение
        self.stop_button = self.app.widget_factory.create_button(controls_frame, 'batch_stop', self.stop_batch, 'reset')# Кнопка остановки
        self.progress = ttk.Progressbar(controls_frame, orient='horizontal', mode='determinate',
                                        style="Accent.Horizontal.TProgressbar")# Прогресс-бар
        self.progress.grid(row=0, column=1, columnspan=5, sticky='ew', padx=(5, 0))  # Размещение
        results_frame = self.app.widget_factory.create_labelframe(main_container, 'batch_results')  # Фрейм результатов
        results_frame.grid(row=current_row, column=0, sticky='ew')  # Размещение
        current_row += 1  # Увеличение строки
        results_scroll = ScrollableFrame(results_frame.content, self.app.widget_factory)  # Прокрутка результатов
        results_scroll.container.config(height=self.app.size_config['container']['result_table']['max_height'])  # Высота
        results_scroll.container.pack_propagate(False)  # Запрет изменения размера
        results_scroll.pack(fill='x', expand=False)  # Размещени
        self.results_container = results_scroll.inner  # Контейнер строк
        self.results_container.columnconfigure(0, weight=1)  # Растяжение
        self._create_all_graphs_row()  # Создание строки "все графы"
        
        def on_params_changed(*args):
            """Обработчик изменения параметров"""
            if not self.is_running:  # Не во время выполнения
                self._update_total_generations()  # Обновление общего количества
                count = self.ui_vars['batch_start_vertices_count'].get()  # Количество ячеек
                if self.start_vertices_table:  # Таблица существует
                    self.start_vertices_table.set_count(count, self.current_graph_vertices or 20)  # Установка
        
        self.ui_vars['batch_graphs_count'].trace_add('write', on_params_changed)  # Отслеживание изменений
        self.ui_vars['batch_start_vertices_count'].trace_add('write', on_params_changed)  # Отслеживание изменений
        self.ui_vars['batch_simulations_per_vertex'].trace_add('write', on_params_changed)  # Отслеживание изменений
        self.load_data_to_ui()  # Загрузка данных в ui

    def refresh(self):
        """Полное перестроение вкладки при смене языка или темы"""
        sim_tab = self.app.tab_manager.tab_instances[2]  # Вкладка симуляции
        if sim_tab and hasattr(sim_tab, 'clear_batch_context'):  # Метод существует
            sim_tab.clear_batch_context()  # Очистка контекста
        
        super().refresh()  # Вызов родительского метода

    def save_state(self):
        """Сохранение состояния перед refresh"""
        super().save_state()  # Вызов родительского метода
        self._saved_state.update({  # Добавление специфичных данных
            'batch_graphs_count': self.ui_vars['batch_graphs_count'].get(),  # Количество графов
            'batch_start_vertices_count': self.ui_vars['batch_start_vertices_count'].get(),  # Количество стартовых вершин
            'batch_simulations_per_vertex': self.ui_vars['batch_simulations_per_vertex'].get(),  # Количество симуляций
            'start_vertices': self.start_vertices_table.get_values() if self.start_vertices_table else [],  # Стартовые вершины
            'result_rows_data': self._serialize_result_rows(),  # Данные строк результатов
            'is_running': self.is_running,  # Состояние выполнения
        })
    
    def _serialize_result_rows(self):
        """Сериализация строк результатов для восстановления"""
        rows_data = []  # Список данных строк
        for row in self.result_rows:  # Перебор строк
            rows_data.append({  # Добавление данных
                'graph_index': row.graph_index,  # Индекс графа
                'graph_data': row.graph_data.copy(),  # Копия данных графа
                'simulations': row.simulations,  # Симуляции
            })
        return rows_data
    
    def restore_state(self):
        """Восстановление состояния после refresh"""
        super().restore_state()  # Вызов родительского метода
        if self._saved_state:  # Сохраненное состояние существует
            self.ui_vars['batch_graphs_count'].set(self._saved_state.get('batch_graphs_count', 1))  # Восстановление
            self.ui_vars['batch_start_vertices_count'].set(self._saved_state.get('batch_start_vertices_count', 5))  # Восстановление
            self.ui_vars['batch_simulations_per_vertex'].set(self._saved_state.get('batch_simulations_per_vertex', 1))  # Восстановление
            self.is_running = self._saved_state.get('is_running', False)  # Восстановление состояния
            self.app.root.after(100, self._restore_result_rows)  # Отложенное восстановление строк
    
    def _restore_result_rows(self):
        """Восстановление строк результатов после refresh"""
        if hasattr(self, '_saved_result_rows') and self._saved_result_rows:  # Сохраненные строки существуют
            for row_data in self._saved_result_rows:  # Перебор данных
                self._add_result_row(row_data['graph_index'], row_data['graph_data'], row_data['simulations'])# Добавление строки
            self._saved_result_rows = None  # Сброс сохраненных строк
            self._update_ui_for_state()  # Обновление интерфейса

    def _get_batch_summary_params(self):
        """Сбор параметров генерации для окна итогов"""
        is_custom = self._is_custom_graph()  # Проверка типа графа
        graphs_count = 1 if is_custom else self.ui_vars['batch_graphs_count'].get()  # Количество графов
        return {  # Словарь параметров
            'graphs_count': graphs_count,  # Количество графов
            'start_vertices_count': self.ui_vars['batch_start_vertices_count'].get(),  # Количество стартовых вершин
            'simulations_per_vertex': self.ui_vars['batch_simulations_per_vertex'].get(),  # Количество симуляций
        }
    
    def show_results(self, graph_index=None):
        """Открытие окна итогов для одного графа или для всех"""
        params = self._get_batch_summary_params()  # Параметры
        
        if graph_index is not None:  # Конкретный граф
            total_simulations = (params['start_vertices_count'] * params['simulations_per_vertex'])# Общее количество симуляций одного графа
            params = params.copy()  # Копия параметров
            params['graphs_count'] = 1  # Один граф
        else:  # Все графы
            total_simulations = (params['graphs_count'] * params['start_vertices_count'] * params['simulations_per_vertex'])# Количество симуляций
        
        all_results = []  # Сбор данных из result_rows
        for row in self.result_rows:  # Перебор строк
            if row and row.winfo_exists():  # Строка существует
                all_results.append({  # Добавление данных
                    'graph_index': row.graph_index,  # Индекс графа
                    'graph_data': row.graph_data,  # Данные графа
                    'simulations': row.simulations  # Симуляции
                })
        BatchSummaryWindow(self.app.root, self.app, params, total_simulations,all_results=all_results,graph_index=graph_index)# Окно итогов


# In[44]:


class HelpTab(Tab):
    """Вкладка справки"""
    
    tab_key = 'tab_help'  # Ключ для перевода названия вкладки
    
    HELP_STRUCTURE = [  # Структура справки: (ключ перевода, вложенные секции)
        ('help_section_overview', []),  # Общий обзор
        ('tab_generation', [  # Вкладка генерации графа
            ('vertex_count', []),  # Количество вершин
            ('edge_distribution', [  # Распределение ребер
                ('Uniform', []),  # Равномерное
                ('Normal', []),  # Нормальное
                ('Student', []),  # Стьюдента
                ('Laplace', []),  # Лапласа
                ('Bimodal', []),  # Бимодальное
                ('Skewed_t', []),  # Скошенное t
                ('Stepwise', []),  # Ступенчатое
            ]),
            ('vertex_distribution', [  # Распределение вершин
                ('Uniform', []),  # Равномерное
                ('Normal', []),  # Нормальное
                ('Lognormal', []),  # Логнормальное
                ('Bimodal', []),  # Бимодальное
                ('Stepwise', []),  # Ступенчатое
            ]),
            ('resistance_type', []),  # Тип устойчивости
            ('influence_type', []),  # Тип влияния
            ('damping_type', []),  # Тип затухания
        ]),
        ('tab_custom', [  # Вкладка пользовательского графа
            ('vertex_distribution', []),  # Распределение вершин
            ('edge_distribution', []),  # Распределение ребер
        ]),
        ('tab_simulation', []),  # Вкладка запуска симуляции
        ('tab_multiple', []),  # Вкладка множественной симуляции
        ('tab_settings', []),  # Вкладка настроек
    ]
    
    def __init__(self, parent, app):
        """Инициализация вкладки справки с оглавлением и контентом"""
        super().__init__(parent, app)  # Вызов конструктора родительского класса
        self.section_widgets = {}  # Словарь {ключ перевода: виджет секции} в правой панели
        self.split = None  # Ссылка на splitscrollframe для прокрутки
        self._saved_state = None  # Сохраненное состояние (не используется)
    
    def build(self):
        """Создание интерфейса вкладки справки"""
        self.split = SplitScrollFrame(self.frame, self.app.widget_factory, self.app)  # Разделяемая панель
        self.split.pack(fill='both', expand=True)  # Размещение с растяжением
        
        left = self.split.get_left()  # Левая панель (оглавление)
        right = self.split.get_right()  # Правая панель с прокруткой (содержимое)
        
        self._build_toc(left, self.HELP_STRUCTURE, depth=0)  # Построение оглавления
        
        main_container = self.app.widget_factory.create_frame(right)  # Основной контейнер правой панели
        main_container.pack(fill='both', expand=True, padx=20, pady=20)  # Размещение с отступами
        
        self._build_content(main_container, self.HELP_STRUCTURE, depth=0)  # Построение контента
    
    def _build_toc(self, parent, structure, depth):
        """Рекурсивное построение оглавления в левой панели"""
        for key, children in structure:  # Перебор элементов структуры
            indent = depth * 10  # Удвоенный отступ для вложенных пунктов
            
            label = self.app.widget_factory.create_label(parent, key, 'card_header')  # Заголовок секции
            label.pack(anchor='w', padx=(indent, 0), pady=(8 if depth == 0 else 3, 1))  # Размещение с отступами
            
            label.bind('<Button-1>', lambda e, k=key: self._scroll_to_section(k))  # Клик для прокрутки
            label.config(cursor='hand2')  # Курсор-рука при наведении
            
            if children:  # Есть вложенные элементы
                self._build_toc(parent, children, depth + 1)  # Рекурсивный вызов для вложенных
    
    def _build_content(self, parent, structure, depth):
        """Рекурсивное построение контентной части с labelframe для каждого заголовка"""
        for key, children in structure:  # Перебор элементов структуры
            frame = self.app.widget_factory.create_labelframe(parent, key)  # Фрейм с заголовком
            frame.pack(fill='x', pady=(0, 10))  # Размещение с отступом снизу
            self.section_widgets[key] = frame  # Сохранение для прокрутки
            
            if children:  # Есть вложенные элементы
                self._build_content(frame.content, children, depth + 1)  # Рекурсивный вызов для вложенных
    
    def _scroll_to_section(self, section_id):
        """Прокрутка правой панели к указанной секции"""
        target = self.section_widgets.get(section_id)  # Поиск виджета секции
        if not target or not self.split:  # Секция или панель не найдены
            return
        
        y = target.winfo_y()  # Y-координата виджета относительно внутреннего фрейма
        inner = self.split.right_content  # Внутренний фрейм с прокруткой
        total = inner.winfo_reqheight()  # Общая высота содержимого
        
        if total > 0:  # Есть содержимое
            fraction = y / total  # Доля от общей высоты
            self.split.yview_moveto(min(fraction, 1.0))  # Прокрутка к позиции
    
    def save_state(self):
        """Сохранение состояния (helptab не имеет состояния)"""
        self._saved_state = None  # Ничего не сохраняем
    
    def restore_state(self):
        """Восстановление состояния (helptab не требует восстановления)"""
        pass  # Ничего не делаем


# In[45]:


class SettingsTab(Tab):
    """Вкладка настроек"""
    
    tab_key = 'tab_settings'  # Ключ для перевода названия вкладки
    
    def __init__(self, parent, app):
        """Инициализация вкладки настроек с переменными для всех параметров"""
        super().__init__(parent, app)  # Вызов конструктора родительского класса
        self._saved_state = None  # Сохраненное состояние
        self.lang_var = tk.StringVar(value='EN')  # Переменная языка (оригинальное значение)
        self.theme_var = tk.StringVar(value='theme_dark')  # Переменная темы (оригинальное значение)
        self.global_seed_mode_var = tk.StringVar(value='seed_fixed')  # Режим глобального seed
        self.global_seed_value_var = tk.IntVar(value=42)  # Значение глобального seed
        self.graph_seed_mode_var = tk.StringVar(value='seed_fixed')  # Режим локального seed графа
        self.graph_seed_value_var = tk.IntVar(value=42)  # Значение локального seed графа
        self.layout_var = tk.StringVar(value='layout_spring')  # Тип расположения вершин
        self.progress_mode_var = tk.StringVar(value='progress_per_vertex')  # Режим обновления прогресса
        self.ignition_method_var = tk.StringVar(value='Sequential')  # Метод поджога
        self.threshold_method_var = tk.StringVar(value='None')  # Тип порога
        self.lang_display = tk.StringVar()  # Отображаемая переменная языка
        self.theme_display = tk.StringVar()  # Отображаемая переменная темы
        self.global_seed_mode_display = tk.StringVar()  # Отображаемый режим глобального seed
        self.graph_seed_mode_display = tk.StringVar()  # Отображаемый режим локального seed
        self.layout_display = tk.StringVar()  # Отображаемый тип расположения
        self.progress_mode_display = tk.StringVar()  # Отображаемый режим прогресса
        self.ignition_method_display = tk.StringVar()  # Отображаемый метод поджога
        self.threshold_method_display = tk.StringVar()  # Отображаемый тип порога
        self.font_size_var = tk.IntVar(value=self.app.settings['font_size'].get())  # Размер шрифта
        self.max_vertices_var = tk.IntVar(value=self.app.settings['max_vertices'].get())  # Максимум вершин
        self.hide_graph_var = tk.BooleanVar(value=self.app.settings['hide_graph_display'].get())  # Скрытие графа
        self.show_edges_var = tk.BooleanVar(value=self.app.settings['show_edges'].get())  # Показ ребер
        self.show_negative_edges_var = tk.BooleanVar(value=self.app.settings['show_negative_edges'].get())  # Показ отрицательных ребер
        self.use_simple_colors_var = tk.BooleanVar(value=self.app.settings['use_simple_edge_colors'].get())  # Упрощенная цветовая схема
        self.threshold_var = tk.IntVar(value=self.app.settings['threshold_add_vertex'].get())  # Порог перерисовки
        self.default_vertex_count_var = tk.IntVar(value=self.app.settings['default_vertex_count'].get())  # Количество вершин по умолчанию
        self.default_vertex_weight_var = tk.DoubleVar(value=self.app.settings['default_vertex_weight'].get())  # Вес вершины по умолчанию
        self.default_edge_weight_var = tk.DoubleVar(value=self.app.settings['default_edge_weight'].get())  # Вес ребра по умолчанию
        self.max_batch_graphs_var = tk.IntVar(value=self.app.settings['max_batch_graphs'].get())  # Максимум графов в пакете
        self.max_batch_simulations_var = tk.IntVar(value=self.app.settings['max_batch_simulations'].get())  # Максимум симуляций
        self.rounding_input_var = tk.IntVar(value=self.app.settings['rounding_input'].get())  # Точность ввода
        self.rounding_stats_var = tk.IntVar(value=self.app.settings['rounding_stats'].get())  # Точность статистик
        self.threshold_value_var = tk.DoubleVar(value=self.app.settings.get('threshold_value', 0.5))  # Значение порога

    def on_activate(self):
        """Загрузка текущих настроек при активации вкладки"""
        self.lang_var.set(self.app.translator.language)  # Текущий язык
        self.theme_var.set(self.app.theme_manager.theme)  # Текущая тема
        self.font_size_var.set(self.app.settings['font_size'].get())  # Размер шрифта
        self.max_vertices_var.set(self.app.settings['max_vertices'].get())  # Максимум вершин
        self.hide_graph_var.set(self.app.settings['hide_graph_display'].get())  # Скрытие графа
        self.layout_var.set(self.app.settings['layout_type'].get())  # Тип расположения
        self.show_edges_var.set(self.app.settings['show_edges'].get())  # Показ ребер
        self.show_negative_edges_var.set(self.app.settings['show_negative_edges'].get())  # Показ отрицательных ребер
        self.use_simple_colors_var.set(self.app.settings['use_simple_edge_colors'].get())  # Упрощенная цветовая схема
        self.threshold_var.set(self.app.settings['threshold_add_vertex'].get())  # Порог перерисовки
        self.default_vertex_count_var.set(self.app.settings['default_vertex_count'].get())  # Количество вершин по умолчанию
        self.default_vertex_weight_var.set(self.app.settings['default_vertex_weight'].get())  # Вес вершины по умолчанию
        self.default_edge_weight_var.set(self.app.settings['default_edge_weight'].get())  # Вес ребра по умолчанию
        self.max_batch_graphs_var.set(self.app.settings['max_batch_graphs'].get())  # Максимум графов
        self.max_batch_simulations_var.set(self.app.settings['max_batch_simulations'].get())  # Максимум симуляций
        self.progress_mode_var.set(self.app.settings['batch_progress_update_mode'].get())  # Режим прогресса
        self.rounding_input_var.set(self.app.settings['rounding_input'].get())  # Точность ввода
        self.rounding_stats_var.set(self.app.settings['rounding_stats'].get())  # Точность статистик
        self._update_display_values()  # Обновление отображаемых значений
    
    def _update_display_values(self):
        """Обновление display переменных из оригинальных через переводчик"""
        self.lang_display.set(self.app.translator.t(self.lang_var.get()))  # Отображение языка
        self.theme_display.set(self.app.translator.t(self.theme_var.get()))  # Отображение темы
        self.global_seed_mode_display.set(self.app.translator.t(self.global_seed_mode_var.get()))  # Отображение режима глобального seed
        self.graph_seed_mode_display.set(self.app.translator.t(self.graph_seed_mode_var.get()))  # Отображение режима локального seed
        self.layout_display.set(self.app.translator.t(self.layout_var.get()))  # Отображение типа расположения
        self.progress_mode_display.set(self.app.translator.t(self.progress_mode_var.get()))  # Отображение режима прогресса
        self.ignition_method_display.set(self.app.translator.t(self.ignition_method_var.get()))  # Отображение метода поджога
        self.threshold_method_display.set(self.app.translator.t(self.threshold_method_var.get()))  # Отображение типа порога
    
    def build(self):
        """Создание интерфейса вкладки настроек"""
        scroll = ScrollableFrame(self.frame, self.app.widget_factory)  # Прокручиваемый фрейм
        scroll.pack(fill='both', expand=True)  # Размещение с растяжением
        content = scroll.inner  # Внутренний контент
        content.columnconfigure(0, weight=1)  # Растяжение колонки
        main_container = self.app.widget_factory.create_frame(content)  # Главный контейнер
        main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)  # Размещение с отступами
        main_container.columnconfigure(0, weight=1)  # Растяжение колонки
        current_row = 0  # Текущая строка
        interface_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'settings_interface')  # Секция интерфейса
        interface_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        current_row += 1  # Увеличение строки
        lang_keys = ['RU', 'EN']  # Ключи языков
        lang_combo = interface_section.add_combo_row('language', lang_keys, self.lang_display)  # Комбобокс языка
        
        def on_lang_change(*args):
            """Обработчик изменения языка"""
            display = self.lang_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.lang_var.set(original)  # Сохранение оригинального значения
        self.lang_display.trace_add('write', on_lang_change)  # Отслеживание изменений
        theme_keys = ['theme_light', 'theme_dark']  # Ключи тем
        theme_combo = interface_section.add_combo_row('settings_theme', theme_keys, self.theme_display)  # Комбобокс темы
        
        def on_theme_change(*args):
            """Обработчик изменения темы"""
            display = self.theme_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.theme_var.set(original)  # Сохранение оригинального значения
        self.theme_display.trace_add('write', on_theme_change)  # Отслеживание изменений
        
        interface_section.add_row(variable=self.font_size_var, param_name='font_size', dist_type='global', 
                                  domain='global', label_key='font_size') # Строка размера шрифта
        rounding_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'rounding_settings')  # Секция округления
        rounding_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        current_row += 1  # Увеличение строки
        rounding_section.add_row(variable=self.rounding_input_var, param_name='rounding_input', dist_type='global', 
                                 domain='global', label_key='rounding_input') # Точность ввода
        rounding_section.add_row(variable=self.rounding_stats_var, param_name='rounding_stats', dist_type='global', 
                                 domain='global', label_key='rounding_stats') # Точность статистик
        reproducibility_section = AlignedSection(main_container, self.app.widget_factory, self.app,
                                                 'settings_reproducibility')  # Секция воспроизводимости
        reproducibility_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        current_row += 1  # Увеличение строки
        global_seed_keys = ['seed_random', 'seed_fixed']  # Ключи режимов глобального seed
        global_seed_config = self.app.validator.get_param_config('global', 'global', 'seed_value')  # Конфигурация seed
        seed_min, seed_max = global_seed_config['range']  # Диапазон значений
        global_seed_combo, global_field_pair = reproducibility_section.add_combo_with_field(combo_label='settings_seed_global',
                            combo_keys=global_seed_keys, combo_var=self.global_seed_mode_display, field_label='',
                            field_var=self.global_seed_value_var, field_param='seed_value', field_dist='global', field_domain='global',
                            hide_when_value='seed_random', scale_size='long')
        
        def on_global_seed_mode_change(*args):
            """Обработчик изменения режима глобального seed"""
            display = self.global_seed_mode_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.global_seed_mode_var.set(original)  # Сохранение
        self.global_seed_mode_display.trace_add('write', on_global_seed_mode_change)  # Отслеживание
        
        graph_seed_keys = ['seed_random', 'seed_fixed']  # Ключи режимов локального seed
        graph_seed_combo, graph_field_pair = reproducibility_section.add_combo_with_field(combo_label='settings_seed_graph',
                            combo_keys=graph_seed_keys, combo_var=self.graph_seed_mode_display, field_label='',
                            field_var=self.graph_seed_value_var, field_param='seed_value', field_dist='global',
                            field_domain='global', hide_when_value='seed_random', scale_size='long')# Строка для seed графа
        
        def on_graph_seed_mode_change(*args):
            """Обработчик изменения режима локального seed графа"""
            display = self.graph_seed_mode_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.graph_seed_mode_var.set(original)  # Сохранение
        self.graph_seed_mode_display.trace_add('write', on_graph_seed_mode_change)  # Отслеживание
        graph_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'graph_parameters')  # Секция параметров графа
        graph_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        current_row += 1  # Увеличение строки
        graph_section.add_row(variable=self.max_vertices_var, param_name='max_vertices', dist_type='global', domain='global',
                              label_key='max_vertex_count', scale_size='long') # Максимум вершин
        ignition_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'ignition_settings')  # Секция поджога
        ignition_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        current_row += 1  # Увеличение строки
        ignition_keys = ['Sequential', 'Simultaneous']  # Ключи методов поджога
        ignition_combo = ignition_section.add_combo_row('ignition_method', ignition_keys, self.ignition_method_display)  # Комбобокс
        
        def on_ignition_change(*args):
            """Обработчик изменения метода поджога"""
            display = self.ignition_method_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.ignition_method_var.set(original)  # Сохранение
        self.ignition_method_display.trace_add('write', on_ignition_change)  # Отслеживание
        self.ignition_method_display.set(self.app.translator.t('Sequential'))  # Значение по умолчанию
        
        threshold_keys = ['None', 'Maximum', 'Mean', 'Median']  # Ключи типов порога
        threshold_combo, field_pair = ignition_section.add_combo_with_field(combo_label='threshold_method', combo_keys=threshold_keys,
                                combo_var=self.threshold_method_display, field_label='threshold_value', field_var=self.threshold_value_var,
                                field_param='threshold_value', field_dist='global', field_domain='global', hide_when_value='None',
                                scale_size='normal', combo_size='default')
        
        def on_threshold_change(*args):
            """Обработчик изменения типа порога"""
            display = self.threshold_method_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.threshold_method_var.set(original)  # Сохранение
        self.threshold_method_display.trace_add('write', on_threshold_change)  # Отслеживание
        self.threshold_method_display.set(self.app.translator.t('None'))  # Значение по умолчанию
        viz_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'visualization_settings')  # Секция визуализации
        viz_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        current_row += 1  # Увеличение строки
        layout_keys = ['layout_spring', 'layout_circular', 'layout_random', 'layout_grid']  # Ключи типов расположения
        self.layout_combo = viz_section.add_combo_row('vertex_layout_type', layout_keys, self.layout_display, size='wide')  # Комбобокс
        
        def on_layout_change(*args):
            """Обработчик изменения типа расположения"""
            display = self.layout_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.layout_var.set(original)  # Сохранение
        self.layout_display.trace_add('write', on_layout_change)  # Отслеживание
        
        self.hide_graph_cb = self.app.widget_factory.create_checkbutton(viz_section.content,
                                                'hide_graph_display', self.hide_graph_var) # Чекбокс скрытия графа
        self.hide_graph_cb.grid(row=viz_section.current_row, column=0, columnspan=2, sticky='w', pady=5)  # Размещение
        viz_section.current_row += 1  # Увеличение строки
        children_container = self.app.widget_factory.create_frame(viz_section.content)  # Контейнер дочерних опций
        children_container.grid(row=viz_section.current_row, column=0, columnspan=2, sticky='w', padx=(20, 0), pady=2)  # Размещение с отступом
        viz_section.current_row += 1  # Увеличение строки
        self.show_edges_cb = self.app.widget_factory.create_checkbutton(children_container,
                                            'show_non_burning_edges', self.show_edges_var) # Чекбокс показа ребер
        self.show_edges_cb.pack(anchor='w', pady=2)  # Размещение
        self.show_negative_cb = self.app.widget_factory.create_checkbutton(children_container,
                                            'settings_show_negative', self.show_negative_edges_var) # Чекбокс показа отрицательных ребер
        self.show_negative_cb.pack(anchor='w', pady=2)  # Размещение
        self.simple_colors_cb = self.app.widget_factory.create_checkbutton(children_container,
                                            'use_simple_edge_colors', self.use_simple_colors_var) # Чекбокс упрощенной цветовой схемы
        self.simple_colors_cb.pack(anchor='w', pady=2)  # Размещение
        threshold_container = self.app.widget_factory.create_frame(viz_section.content)  # Контейнер порога перерисовки
        threshold_container.grid(row=viz_section.current_row, column=0, columnspan=2, sticky='w', padx=(20, 0), pady=(5, 0))  # Размещение
        viz_section.current_row += 1  # Увеличение строки
        threshold_label = self.app.widget_factory.create_label(threshold_container, 'threshold_redraw', 'normal')  # Лейбл
        threshold_label.pack(side='left', padx=(0, 10))  # Размещение
        threshold_controls = self.app.widget_factory.create_frame(threshold_container)  # Контейнер управления
        threshold_controls.pack(side='left', fill='x', expand=True)  # Размещение
        self.threshold_entry = self.app.widget_factory.create_entry(threshold_controls, self.threshold_var, param_name='threshold_add_vertex',
                                                    dist_type='global', domain='global', size='default') # Поле ввода порога
        self.threshold_entry.pack(side='left', padx=(0, 10))  # Размещение
        threshold_cfg = self.app.validator.get_param_config('global', 'global', 'threshold_add_vertex')  # Конфигурация порога
        threshold_from, threshold_to = threshold_cfg['range']  # Диапазон
        self.threshold_slider = self.app.widget_factory.create_scale(threshold_controls, self.threshold_var,
                                                from_=threshold_from, to_=threshold_to, size='normal') # Слайдер порога
        self.threshold_slider.pack(side='left', fill='x', expand=True)  # Размещение
        default_section = AlignedSection(main_container, self.app.widget_factory, self.app, 'default_graph_params')  # Секция графа по умолчанию
        default_section.add_row(variable=self.default_vertex_count_var, param_name='default_vertex_count',  # Количество вершин
                                dist_type='global', domain='global', label_key='default_vertex_count_label', scale_size='long')
        default_section.add_row(variable=self.default_vertex_weight_var, param_name='default_vertex_weight',  # Вес вершины
                                dist_type='global', domain='global', label_key='default_vertex_weight_label', scale_size='long')
        default_section.add_row(variable=self.default_edge_weight_var, param_name='default_edge_weight',  # Вес ребра
                                dist_type='global', domain='global', label_key='default_edge_weight_label', scale_size='long')
        default_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        self.default_section = default_section  # Сохранение
        self.current_row_for_default = current_row  # Сохранение строки
        current_row += 1  # Увеличение строки
        batch_section = AlignedSection(main_container, self.app.widget_factory, self.app,
                                       'batch_generation_params_title')  # Секция множественной генерации
        batch_section.frame.grid(row=current_row, column=0, sticky='ew', pady=(0, 50))  # Размещение
        current_row += 1  # Увеличение строки
        batch_section.add_row(variable=self.max_batch_graphs_var, param_name='max_batch_graphs',  # Максимум графов
                              dist_type='global', domain='global', label_key='max_batch_graphs_label', scale_size='long')
        batch_section.add_row(variable=self.max_batch_simulations_var, param_name='max_batch_simulations',  # Максимум симуляций
                              dist_type='global', domain='global', label_key='max_batch_simulations_label', scale_size='long')
        progress_keys = ['progress_per_vertex', 'progress_per_graph']  # Ключи режимов прогресса
        progress_combo = batch_section.add_combo_row('progress_update_mode', progress_keys, self.progress_mode_display)  # Комбобокс
        
        def on_progress_mode_change(*args):
            """Обработчик изменения режима прогресса"""
            display = self.progress_mode_display.get()  # Отображаемое значение
            original = self.app.translator.to_key(display)  # Оригинальный ключ
            self.progress_mode_var.set(original)  # Сохранение
        self.progress_mode_display.trace_add('write', on_progress_mode_change)  # Отслеживание
        btn_container = self.app.widget_factory.create_frame(main_container)  # Контейнер кнопки
        btn_container.grid(row=current_row, column=0, sticky='ew', pady=(0, 100))  # Размещение
        btn_container.columnconfigure(0, weight=1)  # Растяжение
        apply_btn = self.app.widget_factory.create_button(btn_container, 'apply', self._apply_settings, 'apply')  # Кнопка применить
        apply_btn.pack()  # Размещение
        self.load_data_to_ui()  # Загрузка данных в ui
    
    def _setup_checkbox_dependencies(self):
        """Настройка зависимости дочерних чекбоксов от главных"""
        def on_hide_graph_changed(*args):
            """Обработчик изменения основного чекбокса 'не отображать граф'"""
            is_hidden = self.hide_graph_var.get()  # Состояние скрытия
            if is_hidden:  # Граф скрыт
                self.show_edges_var.set(False)  # Сброс показа ребер
                self.show_negative_edges_var.set(False)  # Сброс показа отрицательных
                self.use_simple_colors_var.set(False)  # Сброс упрощенной схемы
            _update_children_state()  # Обновление состояния дочерних
        
        def on_show_edges_changed(*args):
            """Обработчик изменения чекбокса 'рисовать негорящие ребра'"""
            _update_children_state()  # Обновление состояния
        
        def _update_children_state():
            """Обновление активности дочерних виджетов визуализации"""
            is_hidden = self.hide_graph_var.get()  # Состояние скрытия графа
            show_edges = self.show_edges_var.get()  # Состояние показа ребер
            state = 'disabled' if is_hidden else 'normal'  # Состояние виджетов
            readonly_state = 'readonly' if state == 'normal' else 'disabled'  # Состояние комбобокса
            if hasattr(self, 'layout_combo') and self.layout_combo.winfo_exists():  # Комбобокс расположения
                try:
                    self.layout_combo.entry.config(state=readonly_state)  # Установка состояния
                except:
                    pass
            if hasattr(self, 'show_edges_cb') and self.show_edges_cb.winfo_exists():  # Чекбокс показа ребер
                self.show_edges_cb.config(state=state)  # Установка состояния
            if hasattr(self, 'show_negative_cb') and self.show_negative_cb.winfo_exists():  # Чекбокс отрицательных
                if not is_hidden and not show_edges:  # Ребра не показаны
                    self.show_negative_cb.config(state='disabled')  # Блокировка
                else:  # Ребра показаны
                    self.show_negative_cb.config(state=state)  # Нормальное состояние
            if hasattr(self, 'simple_colors_cb') and self.simple_colors_cb.winfo_exists():  # Чекбокс упрощенной схемы
                if not is_hidden and not show_edges:  # Ребра не показаны
                    self.simple_colors_cb.config(state='disabled')  # Блокировка
                else:  # Ребра показаны
                    self.simple_colors_cb.config(state=state)  # Нормальное состояние
            if hasattr(self, 'threshold_entry') and self.threshold_entry.winfo_exists():  # Поле ввода порога
                self.threshold_entry.config(state=state)  # Установка состояния
            if hasattr(self, 'threshold_slider') and self.threshold_slider.winfo_exists():  # Слайдер порога
                self.threshold_slider.config(state=state)  # Установка состояния
        self.hide_graph_var.trace_add('write', on_hide_graph_changed)  # Отслеживание скрытия
        self.show_edges_var.trace_add('write', on_show_edges_changed)  # Отслеживание показа ребер
        on_hide_graph_changed()  # Инициализация состояния
    
    def load_data_to_ui(self):
        """Загрузка текущих настроек в ui"""
        self._update_display_values()  # Обновление отображаемых значений
        self.font_size_var.set(self.app.settings['font_size'].get())  # Размер шрифта
        self.rounding_input_var.set(self.app.settings['rounding_input'].get())  # Точность ввода
        self.rounding_stats_var.set(self.app.settings['rounding_stats'].get())  # Точность статистик
        self.global_seed_mode_var.set(self.app.settings['seed_mode_global'].get())  # Режим глобального seed
        self.global_seed_value_var.set(self.app.settings['seed_value_global'].get())  # Значение глобального seed
        self.graph_seed_mode_var.set(self.app.settings['seed_mode_graph'].get())  # Режим локального seed
        self.graph_seed_value_var.set(self.app.settings['seed_value_graph'].get())  # Значение локального seed
        self.max_vertices_var.set(self.app.settings['max_vertices'].get())  # Максимум вершин
        self.ignition_method_var.set(self.app.settings.get('ignition_method', 'Sequential'))  # Метод поджога
        self.threshold_method_var.set(self.app.settings.get('threshold_method', 'None'))  # Тип порога
        self.threshold_value_var.set(self.app.settings.get('threshold_value', 0.5))  # Значение порога
        self.show_edges_var.set(self.app.settings['show_edges'].get())  # Показ ребер
        self.show_negative_edges_var.set(self.app.settings['show_negative_edges'].get())  # Показ отрицательных
        self.use_simple_colors_var.set(self.app.settings['use_simple_edge_colors'].get())  # Упрощенная схема
        self.threshold_var.set(self.app.settings['threshold_add_vertex'].get())  # Порог перерисовки
        self.default_vertex_count_var.set(self.app.settings['default_vertex_count'].get())  # Количество вершин по умолчанию
        self.default_vertex_weight_var.set(self.app.settings['default_vertex_weight'].get())  # Вес вершины по умолчанию
        self.default_edge_weight_var.set(self.app.settings['default_edge_weight'].get())  # Вес ребра по умолчанию
        self.max_batch_graphs_var.set(self.app.settings['max_batch_graphs'].get())  # Максимум графов
        self.max_batch_simulations_var.set(self.app.settings['max_batch_simulations'].get())  # Максимум симуляций
        self.progress_mode_var.set(self.app.settings['batch_progress_update_mode'].get())  # Режим прогресса
    
    def save_state(self):
        """Сохранение состояния настроек"""
        self._saved_state = {  # Словарь сохраненных значений
            'lang': self.lang_var.get(),  # Язык
            'theme': self.theme_var.get(),  # Тема
            'font_size': self.font_size_var.get(),  # Размер шрифта
            'global_seed_mode': self.global_seed_mode_var.get(),  # Режим глобального seed
            'global_seed_value': self.global_seed_value_var.get(),  # Значение глобального seed
            'graph_seed_mode': self.graph_seed_mode_var.get(),  # Режим локального seed
            'graph_seed_value': self.graph_seed_value_var.get(),  # Значение локального seed
            'max_vertices': self.max_vertices_var.get(),  # Максимум вершин
            'hide_graph': self.hide_graph_var.get(),  # Скрытие графа
            'layout': self.layout_var.get(),  # Тип расположения
            'show_edges': self.show_edges_var.get(),  # Показ ребер
            'show_negative_edges': self.show_negative_edges_var.get(),  # Показ отрицательных
            'use_simple_colors': self.use_simple_colors_var.get(),  # Упрощенная схема
            'threshold': self.threshold_var.get(),  # Порог перерисовки
            'default_vertex_count': self.default_vertex_count_var.get(),  # Количество вершин по умолчанию
            'default_vertex_weight': self.default_vertex_weight_var.get(),  # Вес вершины по умолчанию
            'default_edge_weight': self.default_edge_weight_var.get(),  # Вес ребра по умолчанию
            'max_batch_graphs': self.max_batch_graphs_var.get(),  # Максимум графов
            'max_batch_simulations': self.max_batch_simulations_var.get(),  # Максимум симуляций
            'progress_mode': self.progress_mode_var.get(),  # Режим прогресса
            'rounding_input': self.rounding_input_var.get(),  # Точность ввода
            'rounding_stats': self.rounding_stats_var.get(),  # Точность статистик
            'ignition_method': self.ignition_method_var.get(),  # Метод поджога
            'threshold_method': self.threshold_method_var.get(),  # Тип порога
            'threshold_value': self.threshold_value_var.get(),  # Значение порога
        }
    
    def restore_state(self):
        """Восстановление состояния настроек после refresh"""
        if self._saved_state:  # Сохраненное состояние существует
            self.lang_var.set(self._saved_state.get('lang', self.app.translator.language))  # Язык
            self.theme_var.set(self._saved_state.get('theme', self.app.theme_manager.theme))  # Тема
            self.font_size_var.set(self._saved_state.get('font_size', self.app.settings['font_size'].get()))  # Размер шрифта
            self.global_seed_mode_var.set(self._saved_state.get('global_seed_mode', 'seed_fixed'))  # Режим глобального seed
            self.global_seed_value_var.set(self._saved_state.get('global_seed_value', 42))  # Значение
            self.graph_seed_mode_var.set(self._saved_state.get('graph_seed_mode', 'seed_fixed'))  # Режим локального seed
            self.graph_seed_value_var.set(self._saved_state.get('graph_seed_value', 42))  # Значение
            self.max_vertices_var.set(self._saved_state.get('max_vertices', self.app.settings['max_vertices'].get()))  # Максимум вершин
            self.hide_graph_var.set(self._saved_state.get('hide_graph', False))  # Скрытие графа
            self.layout_var.set(self._saved_state.get('layout', self.app.settings['layout_type'].get()))  # Тип расположения
            self.show_edges_var.set(self._saved_state.get('show_edges', True))  # Показ ребер
            self.show_negative_edges_var.set(self._saved_state.get('show_negative_edges', True))  # Показ отрицательных
            self.use_simple_colors_var.set(self._saved_state.get('use_simple_colors', False))  # Упрощенная схема
            self.threshold_var.set(self._saved_state.get('threshold', 5))  # Порог перерисовки
            self.default_vertex_count_var.set(self._saved_state.get('default_vertex_count', 20))  # Количество вершин по умолчанию
            self.default_vertex_weight_var.set(self._saved_state.get('default_vertex_weight', 0.99))  # Вес вершины
            self.default_edge_weight_var.set(self._saved_state.get('default_edge_weight', 0.99))  # Вес ребра
            self.max_batch_graphs_var.set(self._saved_state.get('max_batch_graphs', 100))  # Максимум графов
            self.max_batch_simulations_var.set(self._saved_state.get('max_batch_simulations', 100))  # Максимум симуляций
            self.progress_mode_var.set(self._saved_state.get('progress_mode', 'progress_per_vertex'))  # Режим прогресса
            self.rounding_input_var.set(self._saved_state.get('rounding_input', 2))  # Точность ввода
            self.rounding_stats_var.set(self._saved_state.get('rounding_stats', 3))  # Точность статистик
            self.ignition_method_var.set(self._saved_state.get('ignition_method', 'Sequential'))  # Метод поджога
            self.threshold_method_var.set(self._saved_state.get('threshold_method', 'None'))  # Тип порога
            self.threshold_value_var.set(self._saved_state.get('threshold_value', 0.5))  # Значение порога
            self._update_display_values()  # Обновление отображаемых значений
    
    def _apply_settings(self):
        """Обработчик кнопки 'применить'"""
        self.app.apply_settings(  # Вызов метода приложения
            new_lang=self.lang_var.get(),  # Новый язык
            new_theme=self.theme_var.get(),  # Новая тема
            new_font_size=self.font_size_var.get(),  # Новый размер шрифта
            new_global_seed_mode=self.global_seed_mode_var.get(),  # Новый режим глобального seed
            new_global_seed_value=self.global_seed_value_var.get(),  # Новое значение глобального seed
            new_graph_seed_mode=self.graph_seed_mode_var.get(),  # Новый режим локального seed
            new_graph_seed_value=self.graph_seed_value_var.get(),  # Новое значение локального seed
            new_max_vertices=self.max_vertices_var.get(),  # Новый максимум вершин
            new_hide_graph=self.hide_graph_var.get(),  # Новое состояние скрытия графа
            new_layout=self.layout_var.get(),  # Новый тип расположения
            new_show_edges=self.show_edges_var.get(),  # Новое состояние показа ребер
            new_show_negative=self.show_negative_edges_var.get(),  # Новое состояние показа отрицательных
            new_use_simple_colors=self.use_simple_colors_var.get(),  # Упрощенная схема
            new_threshold=self.threshold_var.get(),  # Новый порог перерисовки
            new_default_vertex_count=self.default_vertex_count_var.get(),  # Количество вершин по умолчанию
            new_default_vertex_weight=self.default_vertex_weight_var.get(),  # Вес вершины по умолчанию
            new_default_edge_weight=self.default_edge_weight_var.get(),  # Вес ребра по умолчанию
            new_max_batch_graphs=self.max_batch_graphs_var.get(),  # Максимум графов
            new_max_batch_simulations=self.max_batch_simulations_var.get(),  # Максимум симуляций
            new_progress_mode=self.progress_mode_var.get(),  # Режим прогресса
            new_rounding_input=self.rounding_input_var.get(),  # Точность ввода
            new_rounding_stats=self.rounding_stats_var.get(),  # Точность статистик
            new_ignition_method=self.ignition_method_var.get(),  # Метод поджога
            new_threshold_method=self.threshold_method_var.get(),  # Тип порога
            new_threshold_value=self.threshold_value_var.get()  # Значение порога
        )


# In[46]:


class GraphFireApp:
    """Главный класс приложения Graph Fire"""
    
    def __init__(self, root, progress_callback=None):
        """Инициализация главного приложения с созданием всех компонентов"""
        self.root = root  # Корневое окно tkinter
        self.progress_callback = progress_callback  # Функция обновления прогресса загрузки
        self.root.title("Graph Fire")  # Заголовок окна
        self.root.state('zoomed')  # Полноэкранный режим
        self.root.withdraw()  # Скрытие главного окна до полной загрузки
    
        try:  # Загрузка иконки приложения
            self.icon = tk.PhotoImage(file="GF_logo.png")  # Изображение иконки
            self.root.iconphoto(True, self.icon)  # Установка иконки
        except Exception as e:  # Ошибка загрузки
            print(f"Не удалось загрузить иконку: {e}")  # Вывод сообщения
        
        self._init_basic_components()  # Шаг 1: базовые компоненты
        if self.progress_callback:  # Обновление прогресса
            self.progress_callback(1)
        
        self._init_settings_and_generators()  # Шаг 2: настройки и генераторы
        if self.progress_callback:  # Обновление прогресса
            self.progress_callback(2)
        
        self._init_graph_data()  # Шаг 3: данные графов
        if self.progress_callback:  # Обновление прогресса
            self.progress_callback(3)
        
        self._init_widget_factory()  # Шаг 4: фабрика виджетов
        if self.progress_callback:  # Обновление прогресса
            self.progress_callback(4)
        
        self._create_tabs()  # Шаги 5-10: создание вкладок
        
        self.root.bind('<Map>', self._on_first_show, add=True)  # Обработчик первого показа
        self._first_show_done = False  # Флаг первого показа
    
    def _init_basic_components(self):
        """Инициализация базовых компонентов приложения"""
        self.config = PARAM_CONFIG  # Конфигурация параметров
        self.validator = ValueValidator(self.config)  # Валидатор значений
        self.size_config = SIZE_CONFIG  # Конфигурация размеров
    
        ttk_style = ttk.Style()  # Стиль для ttk виджетов
        try:  # Попытка использования темы 'clam'
            ttk_style.theme_use('clam')
        except tk.TclError:  # Тема недоступна
            pass
            
        self.translator = Translator('EN')  # Переводчик (английский по умолчанию)
        self.theme_manager = ThemeManager('theme_light')  # Менеджер темы (светлая)
        self.root.configure(bg=self.theme_manager.get_color('bg_color'))  # Фон корневого окна
        self.progress_style = ttk.Style()  # Стиль для прогресс-бара
        self.progress_style.configure("Accent.Horizontal.TProgressbar",  # Настройка стиля
                                      troughcolor=self.theme_manager.get_color('slider_trough'),  # Цвет дорожки
                                      background=self.theme_manager.get_color('accent_color'),  # Цвет заполнения
                                      lightcolor=self.theme_manager.get_color('accent_color'),  # Светлая часть
                                      darkcolor=self.theme_manager.get_color('accent_color'))  # Темная часть
    
    def _init_settings_and_generators(self):
        """Инициализация настроек и генераторов"""
        self.dist_generator = DistributionGenerator()  # Генератор распределений
        self.graph_generator = GraphGenerator(self.dist_generator, self.config)  # Генератор графов
        self.prob_calculator = ProbabilityCalculator()  # Калькулятор вероятностей
        self.statistics = StatisticsCalculator()  # Калькулятор статистик
        self.simulation = SimulationEngine(self.prob_calculator)  # Движок симуляции
        self.tier_manager = TierManager()  # Менеджер ступенчатых распределений
        self.settings = self._create_settings()  # Словарь настроек
        self._global_rng = None  # Глобальный генератор случайных чисел
        self._current_global_seed = None  # Текущее значение глобального seed
        self._apply_global_seed()  # Применение глобального seed
        self.settings['seed_value_global'].trace_add('write', lambda *args: self._schedule_apply())  # Отслеживание изменений
        self.settings['seed_mode_global'].trace_add('write', lambda *args: self._schedule_apply())  # Отслеживание изменений
    
    def _init_graph_data(self):
        """Инициализация данных графов для всех вкладок"""
        self.generation_data = GraphData(app=self)  # Данные для вкладки генерации
        self.custom_data = GraphData(app=self)  # Данные для пользовательской вкладки
        self.simulation_data = GraphData(app=self)  # Данные для вкладки симуляции
        self.multiple_data = GraphData(app=self)  # Данные для множественной симуляции
        self.default_graph = GraphData(app=self)  # Граф по умолчанию
        self.default_graph.set_default(app=self)  # Установка значений по умолчанию
        self.custom_data = self.default_graph.copy()  # Копия для пользовательской вкладки
        self.simulation_data = self.default_graph.copy()  # Копия для симуляции
        self.multiple_data = self.default_graph.copy()  # Копия для множественной симуляции
        self.is_copying = False  # Флаг предотвращения рекурсивного копирования
        self._batch_running = False  # Флаг выполнения пакетной симуляции
        self.active_tab_data = self.generation_data  # Активные данные графа
        self.burning_nodes = {}  # Словарь горящих вершин
        self.burned_edges = {}  # Словарь сгоревших ребер
        self.fire_history = []  # История распространения огня
        self.is_fire_running = False  # Флаг выполнения симуляции
    
    def _init_widget_factory(self):
        """Инициализация фабрики виджетов"""
        self.widget_factory = WidgetFactory(self.theme_manager, self.translator, app=self)  # Создание фабрики
        self.widget_factory.update_font_size(self.settings['font_size'].get())  # Установка размера шрифта
        self.main = self.widget_factory.create_frame(self.root)  # Основной фрейм приложения
        self.main.pack(fill='both', expand=True)  # Размещение с растяжением
    
    def _create_tabs(self):
        """Создание вкладок с обновлением прогресса после каждой"""
        self.tab_manager = TabManager(self.main, self)  # Менеджер вкладок
        self.tab_manager.add_tab(GenerationTab, 'tab_generation')  # Вкладка генерации
        self.tab_manager.add_tab(CustomTab, 'tab_custom')  # Пользовательская вкладка
        self.tab_manager.add_tab(SimulationTab, 'tab_simulation')  # Вкладка симуляции
        self.tab_manager.add_tab(MultipleSimTab, 'tab_multiple')  # Множественная симуляция
        self.tab_manager.add_tab(HelpTab, 'tab_help')  # Справка
        self.tab_manager.add_tab(SettingsTab, 'tab_settings')  # Настройки
        
        for i in range(len(self.tab_manager.tab_classes)):  # Создание каждой вкладки
            tab_class = self.tab_manager.tab_classes[i]  # Класс вкладки
            frame = self.tab_manager.frames[i]  # Фрейм для вкладки
            instance = tab_class(frame, self)  # Создание экземпляра
            instance.build()  # Построение интерфейса
            self.tab_manager.tab_instances[i] = instance  # Сохранение экземпляра
            self.tab_manager.frames[i].pack_forget()  # Скрытие фрейма
            if self.progress_callback:  # Обновление прогресса
                self.progress_callback(5 + i)  # Шаг 5-10
        self.tab_manager.active_index = 0  # Активация первой вкладки
        self._sync_vertex_limit()  # Синхронизация лимита вершин
        self.settings['max_vertices'].trace_add('write', lambda *args: self._sync_vertex_limit())  # Отслеживание изменений
    
    def _create_settings(self):
        """Создание словаря с настройками приложения"""
        return {
            'language': tk.StringVar(value=self.translator.language),  # Язык интерфейса
            'theme': tk.StringVar(value='theme_light'),  # Тема оформления
            'font_size': tk.IntVar(value=10),  # Размер шрифта
            'rounding_input': tk.IntVar(value=2),  # Точность ввода
            'rounding_stats': tk.IntVar(value=3),  # Точность статистик
            'seed_mode_global': tk.StringVar(value='seed_fixed'),  # Режим глобального seed
            'seed_value_global': tk.IntVar(value=42),  # Значение глобального seed
            'seed_mode_graph': tk.StringVar(value='seed_fixed'),  # Режим seed графа
            'seed_value_graph': tk.IntVar(value=42),  # Значение seed графа
            'max_vertices': tk.IntVar(value=200),  # Максимум вершин в графе
            'ignition_method': 'Sequential',  # Метод поджога
            'threshold_method': 'None',  # Тип порога
            'threshold_value': 0.5,  # Значение порога
            'hide_graph_display': tk.BooleanVar(value=False),  # Скрытие отображения графа
            'layout_type': tk.StringVar(value='layout_spring'),  # Тип компоновки вершин
            'show_edges': tk.BooleanVar(value=True),  # Показ негорящих ребер
            'show_negative_edges': tk.BooleanVar(value=True),  # Показ отрицательных ребер
            'use_simple_edge_colors': tk.BooleanVar(value=False),  # Упрощенная цветовая схема
            'threshold_add_vertex': tk.IntVar(value=5),  # Порог перерисовки при добавлении вершин
            'default_vertex_count': tk.IntVar(value=20),  # Количество вершин по умолчанию
            'default_vertex_weight': tk.DoubleVar(value=0.99),  # Вес вершины по умолчанию
            'default_edge_weight': tk.DoubleVar(value=0.99),  # Вес ребра по умолчанию
            'max_batch_graphs': tk.IntVar(value=100),  # Максимум графов в пакете
            'max_batch_simulations': tk.IntVar(value=100),  # Максимум симуляций
            'batch_progress_update_mode': tk.StringVar(value='progress_per_vertex'),  # Режим обновления прогресса
        }
    
    def _on_first_show(self, event):
        """Вызов при первом отображении главного окна для корректировки размеров"""
        if not self._first_show_done:  # Первый показ
            self._first_show_done = True  # Установка флага
            self.root.update_idletasks()  # Обновление геометрии
            for instance in self.tab_manager.tab_instances:  # Уведомление вкладок
                if instance and hasattr(instance, 'on_window_shown'):  # Метод существует
                    instance.on_window_shown()  # Вызов метода

    def _apply_global_seed(self):
        """Установка глобального seed и пересоздание генератора"""
        seed_mode = self.settings['seed_mode_global'].get()  # Режим seed
        if seed_mode == 'seed_fixed':  # Фиксированный режим
            seed_value = self.settings['seed_value_global'].get()  # Значение из настроек
            self._global_rng = random.Random(seed_value)  # Создание генератора
            self._current_global_seed = seed_value  # Сохранение значения
        else:  # Случайный режим
            import time
            seed_value = int(time.time() * 1000000) % 99999  # Seed на основе микросекунд
            self._global_rng = random.Random(seed_value)  # Создание генератора
            self._current_global_seed = seed_value  # Сохранение значения

    def get_current_global_seed(self):
        """Возврат текущего значения глобального seed для отображения"""
        return self._current_global_seed  # Текущий seed

    def get_next_graph_seed(self):
        """Возврат следующего seed для нового графа с продвижением генератора"""
        return self._global_rng.randint(1, 999999)  # Случайное число от глобального генератора
    
    def generate_graph_from_params(self, params):
        """Создание нового графа по параметрам с использованием глобального генератора"""
        graph_seed = self.get_next_graph_seed()  # Получение нового seed
        new_data = GraphData(app=self)  # Создание данных графа
        new_data.set_graph_from_params(params, self.graph_generator, self._global_rng)  # Генерация структуры
        if self.settings['seed_mode_graph'].get() == 'seed_fixed':  # Фиксированный режим
            fixed_seed = self.settings['seed_value_graph'].get()  # Фиксированное значение
            new_data.set_graph_seed(fixed_seed, 'seed_fixed')  # Установка фиксированного seed
        else:  # Случайный режим
            new_data.set_graph_seed(graph_seed, 'seed_random')  # Установка случайного seed
        return new_data

    def _sync_vertex_limit(self):
        """Обновление максимального количества вершин в конфиге и на слайдере"""
        max_vertices = self.settings['max_vertices'].get()  # Значение из настроек
        if 'global' in PARAM_CONFIG and 'vertex_count' in PARAM_CONFIG['global']:  # Обновление конфига
            PARAM_CONFIG['global']['vertex_count']['range'] = (2, max_vertices)  # Новый диапазон
        gen_tab = self.tab_manager.tab_instances[0]  # Вкладка генерации
        if gen_tab and hasattr(gen_tab, 'vertex_slider') and gen_tab.vertex_slider:  # Слайдер существует
            gen_tab.vertex_slider.config(to=max_vertices)  # Обновление максимума
            current_val = gen_tab.ui_vars['vertex_count'].get()  # Текущее значение
            if current_val > max_vertices:  # Превышение максимума
                gen_tab.ui_vars['vertex_count'].set(max_vertices)  # Ограничение

    def _schedule_apply(self):
        """Планирование применения настроек после задержки"""
        self.root.after(100, lambda: None)  # Задержка 100 мс
    
    def set_custom_data(self, new_data):
        """Установка данных для вкладки пользовательского графа"""
        self.custom_data = new_data  # Сохранение данных
        custom_tab = self.tab_manager.tab_instances[1]  # Вкладка пользовательского графа
        if custom_tab:  # Вкладка существует
            custom_tab.receive_data(self.custom_data)  # Передача данных
    
    def set_simulation_data(self, new_data):
        """Установка данных для вкладки симуляции"""
        self.simulation_data = new_data  # Сохранение данных
        sim_tab = self.tab_manager.tab_instances[2]  # Вкладка симуляции
        if sim_tab:  # Вкладка существует
            sim_tab.receive_data(self.simulation_data)  # Передача данных
    
    def set_multiple_data(self, new_data):
        """Установка данных для вкладки множественной симуляции"""
        self.multiple_data = new_data  # Сохранение данных
        multi_tab = self.tab_manager.tab_instances[3]  # Вкладка множественной симуляции
        if multi_tab:  # Вкладка существует
            multi_tab.receive_data(self.multiple_data)  # Передача данных
    
    def refresh_all_tabs(self):
        """Обновление всех вкладок при смене языка или темы"""
        saved_data = self._save_all_data()  # Сохранение состояния
        self._full_rebuild(saved_data)  # Полное перестроение
    
    def get_default_vertex_count(self):
        """Возврат количества вершин графа по умолчанию"""
        return self.settings['default_vertex_count'].get()  # Значение из настроек
    
    def get_default_vertex_weight(self):
        """Возврат веса вершины графа по умолчанию"""
        return self.settings['default_vertex_weight'].get()  # Значение из настроек
    
    def get_default_edge_weight(self):
        """Возврат веса ребра графа по умолчанию"""
        return self.settings['default_edge_weight'].get()  # Значение из настроек
    
    def update_default_graph_config(self):
        """Обновление графа по умолчанию при изменении настроек"""
        self.default_graph.set_default(app=self)  # Переустановка значений

    def is_batch_running(self):
        """Возврат флага выполнения множественной симуляции"""
        return hasattr(self, '_batch_running') and self._batch_running  # Состояние флага
    
    def set_batch_running(self, running):
        """Установка флага выполнения множественной симуляции и блокировка вкладок"""
        self._batch_running = running  # Установка флага
        if running:  # Запуск
            self.tab_manager.block_switching()  # Блокировка переключения
        else:  # Остановка
            self.tab_manager.unblock_switching()  # Разблокировка
    
    def _reformat_all_float_entries(self):
        """Переформатирование всех полей ввода вещественных чисел с новой точностью"""
        rounding = self.settings['rounding_input'].get()  # Новая точность
        gen_tab = self.tab_manager.tab_instances[0]  # Вкладка генерации
        if gen_tab:  # Вкладка существует
            for key, var in gen_tab.ui_vars.items():  # Перебор переменных
                if isinstance(var, tk.DoubleVar):  # Вещественная переменная
                    current_value = var.get()  # Текущее значение
                    var.set(current_value)  # Принудительное обновление с новым округлением
        settings_tab = self.tab_manager.tab_instances[5]  # Вкладка настроек
        if settings_tab:  # Вкладка существует
            for var_name in ['default_vertex_weight_var', 'default_edge_weight_var']:  # Переменные весов
                if hasattr(settings_tab, var_name):  # Атрибут существует
                    var = getattr(settings_tab, var_name)  # Получение переменной
                    if isinstance(var, tk.DoubleVar):  # Вещественная переменная
                        current_value = var.get()  # Текущее значение
                        var.set(current_value)  # Принудительное обновление

    def _rebuild_all_float_sliders(self):
        """Пересоздание всех слайдеров для вещественных параметров"""
        gen_tab = self.tab_manager.tab_instances[0]  # Вкладка генерации
        if gen_tab:  # Вкладка существует
            gen_tab.on_edge_dist_change()  # Пересоздание слайдеров ребер
            gen_tab.on_vertex_dist_change()  # Пересоздание слайдеров вершин
        settings_tab = self.tab_manager.tab_instances[5]  # Вкладка настроек
        if settings_tab:  # Вкладка существует
            if hasattr(settings_tab, 'default_section'):  # Секция существует
                frame = settings_tab.default_section.frame  # Фрейм секции
                vertex_count_var = settings_tab.default_vertex_count_var  # Переменная количества
                vertex_weight_var = settings_tab.default_vertex_weight_var  # Вес вершины
                edge_weight_var = settings_tab.default_edge_weight_var  # Вес ребра
                for widget in frame.winfo_children():  # Удаление старых виджетов
                    widget.destroy()
                new_section = AlignedSection(frame.master, self.widget_factory, self, 'default_graph_params')  # Новая секция
                new_section.add_row(label_key='default_vertex_count_label', variable=vertex_count_var,  # Количество
                                    param_name='default_vertex_count', dist_type='global', domain='global', scale_size='long')
                new_section.add_row(label_key='default_vertex_weight_label', variable=vertex_weight_var,  # Вес вершины
                                    param_name='default_vertex_weight', dist_type='global', domain='global', scale_size='long')
                new_section.add_row(label_key='default_edge_weight_label', variable=edge_weight_var,  # Вес ребра
                                    param_name='default_edge_weight', dist_type='global', domain='global', scale_size='long')
                new_section.frame.grid(row=settings_tab.current_row_for_default, column=0, sticky='ew', pady=(0, 30))  # Размещение
                setattr(settings_tab, 'default_section', new_section)  # Сохранение секции
    
    def _refresh_all_stats(self):
        """Обновление всех статистик на вкладке симуляции"""
        sim_tab = self.tab_manager.tab_instances[2]  # Вкладка симуляции
        if sim_tab:  # Вкладка существует
            sim_tab._update_graph_params_column()  # Параметры графа
            sim_tab._update_generation_params_column()  # Параметры генерации
            sim_tab._update_edge_stats_column()  # Статистика ребер
            sim_tab._update_vertex_stats_column()  # Статистика вершин
            sim_tab._update_start_vertex_stats_column()  # Статистика стартовой вершины
            sim_tab._update_simulation_results_column(sim_tab._last_simulation_result)  # Результаты симуляции

    def _save_all_data(self):
        """Сохранение состояния всех вкладок и глобального генератора перед пересозданием"""
        saved_data = {  # Словарь сохраненных данных
            'generation': self.generation_data.copy(),  # Данные генерации
            'custom': self.custom_data.copy(),  # Пользовательские данные
            'simulation': self.simulation_data.copy(),  # Данные симуляции
            'multiple': self.multiple_data.copy(),  # Данные множественной симуляции
            'global_rng_state': self._global_rng.getstate(),  # Состояние глобального rng
            'global_seed_mode': self.settings['seed_mode_global'].get(),  # Режим глобального seed
            'global_seed_value': self.settings['seed_value_global'].get(),  # Значение глобального seed
            'graph_seed_mode': self.settings['seed_mode_graph'].get(),  # Режим seed графа
            'graph_seed_value': self.settings['seed_value_graph'].get(),  # Значение seed графа
        }
        sim_tab = self.tab_manager.tab_instances[2]  # Вкладка симуляции
        if sim_tab:  # Вкладка существует
            saved_data['simulation_state'] = {  # Состояние симуляции
                'last_result': sim_tab._last_simulation_result,  # Последний результат
                'batch_context': sim_tab.batch_context,  # Контекст пакета
                'start_vertex': sim_tab.ui_vars['start_vertex'].get(),  # Стартовая вершина
            }
        multi_tab = self.tab_manager.tab_instances[3]  # Вкладка множественной симуляции
        if multi_tab:  # Вкладка существует
            saved_data['multiple_state'] = {  # Состояние множественной симуляции
                'result_rows_data': multi_tab._serialize_result_rows() if hasattr(multi_tab, '_serialize_result_rows') else [],# Строки результатов
                'is_running': multi_tab.is_running,  # Флаг выполнения
                'ui_vars': {  # Переменные интерфейса
                    'batch_graphs_count': multi_tab.ui_vars['batch_graphs_count'].get(),  # Количество графов
                    'batch_start_vertices_count': multi_tab.ui_vars['batch_start_vertices_count'].get(),  # Количество стартовых
                    'batch_simulations_per_vertex': multi_tab.ui_vars['batch_simulations_per_vertex'].get(),  # Симуляций на вершину
                },
                'start_vertices': multi_tab.start_vertices_table.get_values() if multi_tab.start_vertices_table else [],  # Стартовые вершины
            }
        return saved_data
    
    def _restore_all_data(self, saved_data):
        """Восстановление состояния всех вкладок и глобального генератора после пересоздания"""
        self.generation_data = saved_data.get('generation', self.generation_data)  # Восстановление генерации
        self.custom_data = saved_data.get('custom', self.custom_data)  # Пользовательские данные
        self.simulation_data = saved_data.get('simulation', self.simulation_data)  # Данные симуляции
        self.multiple_data = saved_data.get('multiple', self.multiple_data)  # Множественная симуляция
        if 'global_rng_state' in saved_data:  # Восстановление генератора
            self._global_rng.setstate(saved_data['global_rng_state'])  # Установка состояния
        if 'global_seed_mode' in saved_data:  # Восстановление режима глобального seed
            self.settings['seed_mode_global'].set(saved_data['global_seed_mode'])
        if 'global_seed_value' in saved_data:  # Восстановление значения
            self.settings['seed_value_global'].set(saved_data['global_seed_value'])
        if 'graph_seed_mode' in saved_data:  # Восстановление режима seed графа
            self.settings['seed_mode_graph'].set(saved_data['graph_seed_mode'])
        if 'graph_seed_value' in saved_data:  # Восстановление значения
            self.settings['seed_value_graph'].set(saved_data['graph_seed_value'])
        sim_tab = self.tab_manager.tab_instances[2]  # Вкладка симуляции
        if sim_tab and 'simulation_state' in saved_data:  # Восстановление состояния
            state = saved_data['simulation_state']  # Сохраненное состояние
            sim_tab._last_simulation_result = state.get('last_result')  # Результат
            sim_tab.batch_context = state.get('batch_context')  # Контекст
            sim_tab.ui_vars['start_vertex'].set(state.get('start_vertex', 1))  # Стартовая вершина
            if sim_tab._last_simulation_result:  # Результат существует
                sim_tab._update_simulation_results_column(sim_tab._last_simulation_result)  # Обновление колонки
                if sim_tab.graph_display:  # Виджет графа
                    sim_tab.graph_display.set_fire_data(sim_tab._last_simulation_result['burned_nodes'],
                                                        sim_tab._last_simulation_result['burned_edges']) # Установка данных пожара
            sim_tab._update_new_graph_button_text()  # Обновление текста кнопки
        multi_tab = self.tab_manager.tab_instances[3]  # Вкладка множественной симуляции
        if multi_tab and 'multiple_state' in saved_data:  # Восстановление состояния
            state = saved_data['multiple_state']  # Сохраненное состояние
            multi_tab.is_running = state.get('is_running', False)  # Флаг выполнения
            multi_tab.ui_vars['batch_graphs_count'].set(state['ui_vars']['batch_graphs_count'])  # Количество графов
            multi_tab.ui_vars['batch_start_vertices_count'].set(state['ui_vars']['batch_start_vertices_count'])  # Стартовые
            multi_tab.ui_vars['batch_simulations_per_vertex'].set(state['ui_vars']['batch_simulations_per_vertex'])  # Симуляции
            if multi_tab.start_vertices_table and state.get('start_vertices'):  # Таблица существует
                multi_tab.start_vertices_table.set_count(  # Установка количества
                    len(state['start_vertices']),  # Длина списка
                    multi_tab.current_graph_vertices  # Количество вершин
                )
                for i, val in enumerate(state['start_vertices']):  # Восстановление значений
                    if i < len(multi_tab.start_vertices_table.cell_vars):  # Индекс в пределах
                        multi_tab.start_vertices_table.cell_vars[i].set(str(val))  # Установка
            if state.get('result_rows_data'):  # Строки результатов
                multi_tab._saved_result_rows = state['result_rows_data']  # Сохранение
                multi_tab._restore_result_rows()  # Восстановление
            multi_tab._update_ui_for_state()  # Обновление интерфейса
    
    def _full_rebuild(self, saved_data):
        """Полное пересоздание интерфейса при смене темы, языка или шрифта"""
        self.root.config(cursor="watch")  # Курсор ожидания
        self.root.update()  # Обновление
        try:
            self.progress_style.configure("Accent.Horizontal.TProgressbar", troughcolor=self.theme_manager.get_color('slider_trough'),
                                          background=self.theme_manager.get_color('accent_color')) # Обновление стиля прогресса
            self.tab_manager.refresh_all()  # Обновление всех вкладок
            self._restore_all_data(saved_data)  # Восстановление данных
            self.root.update_idletasks()  # Обновление геометрии
        finally:
            self.root.config(cursor="")  # Сброс курсора
    
    def _full_rebuild_with_new_seed(self, saved_data):
        """Полное перестроение интерфейса с новым глобальным seed-ом с восстановлением данных"""
        self.root.config(cursor="watch")  # Курсор ожидания
        self.root.update()  # Обновление
        try:
            self.progress_style.configure("Accent.Horizontal.TProgressbar",troughcolor=self.theme_manager.get_color('slider_trough'),
                                          background=self.theme_manager.get_color('accent_color'))
            self.tab_manager.refresh_all()  # Обновление всех вкладок
            
            # Восстановление данных графов из сохраненного состояния
            if saved_data:  # Сохраненные данные существуют
                # Восстановление данных всех графов
                self.generation_data = saved_data.get('generation', self.generation_data)
                self.custom_data = saved_data.get('custom', self.custom_data)
                self.simulation_data = saved_data.get('simulation', self.simulation_data)
                self.multiple_data = saved_data.get('multiple', self.multiple_data)
                
                # Восстановление состояния глобального генератора случайных чисел
                if 'global_rng_state' in saved_data:
                    self._global_rng.setstate(saved_data['global_rng_state'])
                
                # Передача восстановленных данных во вкладки
                custom_tab = self.tab_manager.tab_instances[1]  # Вкладка пользовательского графа
                if custom_tab:
                    custom_tab.receive_data(self.custom_data)  # Передача данных
                
                sim_tab = self.tab_manager.tab_instances[2]  # Вкладка симуляции
                if sim_tab:
                    sim_tab.receive_data(self.simulation_data)  # Передача данных
                    # Восстановление специфичного состояния симуляции
                    if 'simulation_state' in saved_data:
                        state = saved_data['simulation_state']  # Сохраненное состояние
                        sim_tab._last_simulation_result = state.get('last_result')  # Последний результат
                        sim_tab.batch_context = state.get('batch_context')  # Контекст пакета
                        sim_tab.ui_vars['start_vertex'].set(state.get('start_vertex', 1))  # Стартовая вершина
                        
                        if sim_tab._last_simulation_result:  # Результат существует
                            sim_tab._update_simulation_results_column(sim_tab._last_simulation_result)  # Обновление колонки
                            if sim_tab.graph_display:  # Виджет графа существует
                                sim_tab.graph_display.set_fire_data(  # Установка данных пожара
                                    sim_tab._last_simulation_result['burned_nodes'],
                                    sim_tab._last_simulation_result['burned_edges'])
                    sim_tab._update_new_graph_button_text()  # Обновление текста кнопки
                
                multi_tab = self.tab_manager.tab_instances[3]  # Вкладка множественной симуляции
                if multi_tab:
                    multi_tab.receive_data(self.multiple_data)  # Передача данных
                    # Восстановление специфичного состояния множественной симуляции
                    if 'multiple_state' in saved_data:
                        state = saved_data['multiple_state']  # Сохраненное состояние
                        multi_tab.is_running = state.get('is_running', False)  # Флаг выполнения
                        
                        # Восстановление ui переменных
                        if 'ui_vars' in state:
                            ui_vars_state = state['ui_vars']
                            multi_tab.ui_vars['batch_graphs_count'].set(ui_vars_state.get('batch_graphs_count', 1))
                            multi_tab.ui_vars['batch_start_vertices_count'].set(ui_vars_state.get('batch_start_vertices_count', 5))
                            multi_tab.ui_vars['batch_simulations_per_vertex'].set(ui_vars_state.get('batch_simulations_per_vertex', 1))
                        
                        # Восстановление стартовых вершин в таблице
                        if multi_tab.start_vertices_table and state.get('start_vertices'):
                            start_vertices = state['start_vertices']
                            multi_tab.start_vertices_table.set_count(
                                len(start_vertices),  # Количество ячеек
                                multi_tab.current_graph_vertices  # Максимальный номер вершины
                            )
                            for i, val in enumerate(start_vertices):  # Восстановление значений
                                if i < len(multi_tab.start_vertices_table.cell_vars):
                                    multi_tab.start_vertices_table.cell_vars[i].set(str(val))
                        
                        # Восстановление строк результатов
                        if state.get('result_rows_data'):
                            multi_tab._saved_result_rows = state['result_rows_data']
                            multi_tab._restore_result_rows()  # Восстановление строк
                        
                        multi_tab._update_ui_for_state()  # Обновление интерфейса
            else:  # Нет сохраненных данных (первый запуск)
                # Только тогда создаем дефолтные данные
                self.default_graph.set_default(app=self)  # Установка значений по умолчанию
                self.custom_data = self.default_graph.copy()  # Копия для пользовательской вкладки
                self.simulation_data = self.default_graph.copy()  # Копия для симуляции
                self.multiple_data = self.default_graph.copy()  # Копия для множественной симуляции
                # Обновление вкладок новыми данными
                custom_tab = self.tab_manager.tab_instances[1]
                if custom_tab:
                    custom_tab.receive_data(self.custom_data)
                sim_tab = self.tab_manager.tab_instances[2]
                if sim_tab:
                    sim_tab.receive_data(self.simulation_data)
                multi_tab = self.tab_manager.tab_instances[3]
                if multi_tab:
                    multi_tab.receive_data(self.multiple_data)
            self.root.update_idletasks()  # Обновление геометрии
        finally:
            self.root.config(cursor="")  # Сброс курсора

    def apply_settings(self, new_lang, new_theme, new_font_size, new_global_seed_mode=None, new_global_seed_value=None, new_graph_seed_mode=None, 
                       new_graph_seed_value=None, new_max_vertices=None, new_hide_graph=None, new_layout=None, new_show_edges=None, 
                       new_show_negative=None, new_use_simple_colors=None, new_threshold=None, new_default_vertex_count=None, 
                       new_default_vertex_weight=None, new_default_edge_weight=None, new_max_batch_graphs=None, new_rounding_input=None, 
                       new_rounding_stats=None, new_max_batch_simulations=None, new_progress_mode=None, new_ignition_method=None, 
                       new_threshold_method=None, new_threshold_value=None):
        """Применение всех настроек приложения и перестроение интерфейса при необходимости"""
        saved_data = self._save_all_data()  # Сохранение текущего состояния
        self._apply_global_seed()  # Пересоздание глобального генератора
        
        # Обновление режимов и значений seed
        if new_global_seed_mode is not None:  # Обновление режима глобального seed
            self.settings['seed_mode_global'].set(new_global_seed_mode)
        if new_global_seed_value is not None:  # Обновление значения глобального seed
            self.settings['seed_value_global'].set(new_global_seed_value)
        if new_graph_seed_mode is not None:  # Обновление режима seed графа
            self.settings['seed_mode_graph'].set(new_graph_seed_mode)
        if new_graph_seed_value is not None:  # Обновление значения seed графа
            self.settings['seed_value_graph'].set(new_graph_seed_value)
        
        # Обновление максимального количества вершин
        if new_max_vertices is not None and new_max_vertices != self.settings['max_vertices'].get():
            self.settings['max_vertices'].set(new_max_vertices)  # Обновление
            self._sync_vertex_limit()  # Синхронизация
        
        # Обновление точности округления
        rounding_input_changed = False  # Флаг изменения точности ввода
        rounding_stats_changed = False  # Флаг изменения точности статистик
        if new_rounding_input is not None and new_rounding_input != self.settings['rounding_input'].get():
            self.settings['rounding_input'].set(new_rounding_input)  # Обновление
            rounding_input_changed = True  # Установка флага
        if new_rounding_stats is not None and new_rounding_stats != self.settings['rounding_stats'].get():
            self.settings['rounding_stats'].set(new_rounding_stats)  # Обновление
            rounding_stats_changed = True  # Установка флага
        
        # Применение изменений точности округления
        if rounding_input_changed:  # Изменение точности ввода
            self._reformat_all_float_entries()  # Переформатирование полей
            self._rebuild_all_float_sliders()  # Пересоздание слайдеров
        if rounding_stats_changed:  # Изменение точности статистик
            self._refresh_all_stats()  # Обновление статистик
        
        # Обновление параметров графа по умолчанию
        if new_default_vertex_count is not None:  # Обновление количества вершин по умолчанию
            self.settings['default_vertex_count'].set(new_default_vertex_count)
        if new_default_vertex_weight is not None:  # Обновление веса вершины по умолчанию
            self.settings['default_vertex_weight'].set(new_default_vertex_weight)
        if new_default_edge_weight is not None:  # Обновление веса ребра по умолчанию
            self.settings['default_edge_weight'].set(new_default_edge_weight)
        
        # Обновление параметров множественной симуляции
        if new_max_batch_graphs is not None:  # Обновление максимума графов
            self.settings['max_batch_graphs'].set(new_max_batch_graphs)
            multi_tab = self.tab_manager.tab_instances[3]  # Вкладка множественной
            if multi_tab and hasattr(multi_tab, 'graphs_count_slider') and multi_tab.graphs_count_slider:
                multi_tab.graphs_count_slider.config(to=new_max_batch_graphs)  # Обновление максимума
        if new_max_batch_simulations is not None:  # Обновление максимума симуляций
            self.settings['max_batch_simulations'].set(new_max_batch_simulations)
            multi_tab = self.tab_manager.tab_instances[3]  # Вкладка множественной
            if multi_tab and hasattr(multi_tab, 'simulations_slider') and multi_tab.simulations_slider:
                multi_tab.simulations_slider.config(to=new_max_batch_simulations)  # Обновление максимума
        if new_progress_mode is not None:  # Обновление режима прогресса
            self.settings['batch_progress_update_mode'].set(new_progress_mode)
        
        # Обновление параметров поджога
        if new_ignition_method is not None:  # Обновление метода поджога
            self.settings['ignition_method'] = new_ignition_method
        if new_threshold_method is not None:  # Обновление типа порога
            self.settings['threshold_method'] = new_threshold_method
        if new_threshold_value is not None:  # Обновление значения порога
            self.settings['threshold_value'] = new_threshold_value
        
        # Обновление настроек визуализации
        layout_changed = False  # Флаг изменения компоновки
        hide_graph_changed = False  # Флаг изменения скрытия графа
        show_edges_changed = False  # Флаг изменения показа ребер
        show_negative_changed = False  # Флаг изменения показа отрицательных ребер
        use_simple_colors_changed = False  # Флаг изменения цветовой схемы
        
        if new_hide_graph is not None:  # Изменение скрытия графа
            old_value = self.settings['hide_graph_display'].get()  # Старое значение
            if new_hide_graph != old_value:  # Значение изменилось
                self.settings['hide_graph_display'].set(new_hide_graph)  # Обновление
                hide_graph_changed = True  # Установка флага
        
        if new_layout is not None:  # Изменение типа компоновки
            old_value = self.settings['layout_type'].get()  # Старое значение
            if new_layout != old_value:  # Значение изменилось
                self.settings['layout_type'].set(new_layout)  # Обновление
                layout_changed = True  # Установка флага
        
        if new_show_edges is not None:  # Изменение показа ребер
            old_value = self.settings['show_edges'].get()  # Старое значение
            if new_show_edges != old_value:  # Значение изменилось
                self.settings['show_edges'].set(new_show_edges)  # Обновление
                show_edges_changed = True  # Установка флага
        
        if new_show_negative is not None:  # Изменение показа отрицательных ребер
            old_value = self.settings['show_negative_edges'].get()  # Старое значение
            if new_show_negative != old_value:  # Значение изменилось
                self.settings['show_negative_edges'].set(new_show_negative)  # Обновление
                show_negative_changed = True  # Установка флага
        
        if new_use_simple_colors is not None:  # Изменение цветовой схемы
            old_value = self.settings['use_simple_edge_colors'].get()  # Старое значение
            if new_use_simple_colors != old_value:  # Значение изменилось
                self.settings['use_simple_edge_colors'].set(new_use_simple_colors)  # Обновление
                use_simple_colors_changed = True  # Установка флага
        
        if new_threshold is not None:  # Обновление порога перерисовки
            self.settings['threshold_add_vertex'].set(new_threshold)
        
        # Применение изменений визуализации
        if hide_graph_changed or layout_changed or show_edges_changed or show_negative_changed or use_simple_colors_changed:
            for instance in self.tab_manager.tab_instances:  # Перебор всех вкладок
                if instance and hasattr(instance, 'graph_display') and instance.graph_display:  # Виджет графа существует
                    if layout_changed:  # Изменилась компоновка
                        instance.graph_display.pos_cache = None  # Сброс кэша позиций
                    else:  # Изменились другие настройки отображения
                        instance.graph_display.invalidate()  # Сброс кэша ребер
                    instance.graph_display.draw()  # Перерисовка графа
        
        # Проверка необходимости полного перестроения интерфейса
        theme_changed = new_theme != self.theme_manager.theme  # Проверка изменения темы
        lang_changed = new_lang != self.translator.language  # Проверка изменения языка
        font_changed = new_font_size != self.widget_factory.base_font_size  # Проверка изменения шрифта
        
        # Применение изменений темы, языка и шрифта
        if theme_changed:  # Изменение темы
            self.theme_manager.set_theme(new_theme)  # Установка новой темы
            self.settings['theme'].set(new_theme)  # Сохранение в настройках
            self.root.configure(bg=self.theme_manager.get_color('bg_color'))  # Обновление фона
        if lang_changed:  # Изменение языка
            self.translator.set_language(new_lang)  # Установка нового языка
            self.settings['language'].set(new_lang)  # Сохранение в настройках
        if font_changed:  # Изменение шрифта
            self.widget_factory.update_font_size(new_font_size)  # Обновление размера шрифта
            self.settings['font_size'].set(new_font_size)  # Сохранение в настройках
        if theme_changed or lang_changed or font_changed: # При смене языка, темы или шрифта перестраиваем интерфейс
            self._full_rebuild_with_new_seed(saved_data)  # Передаем сохраненные данные для восстановления
        else:
            self.update_default_graph_config()  # Обновление конфигурации


# In[47]:


def main():
    """Главная функция запуска приложения Graph Fire"""
    root = tk.Tk()  # Создание корневого окна tkinter
    root.withdraw()  # Скрытие главного окна до полной загрузки
    
    splash = SplashScreen(root)  # Создание splash-экрана
    root.update()  # Принудительное обновление окна
    
    app = GraphFireApp(root, progress_callback=splash.update_progress)  # Создание приложения
    
    splash.close()  # Закрытие splash-экрана
    
    root.state('zoomed')  # Восстановление полноэкранного режима
    
    root.deiconify()  # Показ главного окна
    
    root.update_idletasks()  # Обновление геометрии
    
    app.tab_manager.activate_tab(0)  # Активация первой вкладки
    
    root.mainloop()  # Запуск главного цикла обработки событий


# In[48]:


if __name__ == "__main__":
    main()

