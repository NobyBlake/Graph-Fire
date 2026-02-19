#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import numpy as np
import networkx as nx
from scipy.stats import truncnorm, t as stats_t, laplace, nct, lognorm, gaussian_kde, norm
import os
from scipy import stats

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# In[2]:


# Словарь для интерфейса
TRANSLATIONS = {
    'ru': {
        # Основные кнопки
        'build_graph': 'Построить граф',
        'back': 'Назад',
        'start_fire': 'Запуск',
        'reset': 'Сброс',
        'new_graph': 'Новый граф',
        
        # Разделы интерфейса
        'graph_parameters': 'Параметры графа',
        'graph_stats': 'Статистика графа',
        'edge_stats': 'Статистика ребер',
        'vertex_stats': 'Статистика вершин',
        'legend': 'Легенда',
        'simulation_results': 'Итоги симуляции возгорания',
        'start_vertex_title': 'Выбор стартовой вершины',
        'start_vertex_stats': 'Статистика стартовой вершины',
        
        # Параметры графа
        'vertex_count': 'Количество вершин',
        'edge_distribution': 'Распределение толщины ребер',
        'vertex_distribution': 'Распределение весов вершин',
        'vertex_resistance': 'Разная устойчивость вершин',
        'vertex_influence': 'Разное влияние вершин',
        'damping': 'Затухание',
        
        # Значения для combobox (используем английские ключи как идентификаторы)
        'Uniform': 'Равномерное',
        'Normal': 'Нормальное',
        'Student': 'Стьюдента',
        'Laplace': 'Лапласа',
        'Bimodal': 'Бимодальное',
        'Skewed_t': 'Скошенное t',
        
        'None': 'Нет',
        'Lognormal': 'Логнормальное',
        'Stepwise': 'Ступенчатое',
        
        'resistance_none': 'Нет',
        'resistance_direct': 'Прямо пропорционально размеру',
        'resistance_inverse': 'Обратно пропорционально размеру',
        
        'influence_none': 'Нет',
        'influence_direct': 'Прямо пропорционально размеру',
        'influence_inverse': 'Обратно пропорционально размеру',
        
        'damping_none': 'Нет',
        'damping_exponential': 'Экспоненциальное',
        'damping_hyperbolic': 'Гиперболическое',
        'damping_discrete': 'Дискретное',
        
        # Параметры распределений (заголовки)
        'uniform_params': 'Параметры равномерного распределения',
        'normal_params': 'Параметры нормального распределения',
        'student_params': 'Параметры распределения Стьюдента',
        'laplace_params': 'Параметры распределения Лапласа',
        'bimodal_params': 'Параметры бимодального распределения',
        'skewed_t_params': 'Параметры скошенного t-распределения',
        'vertex_uniform_params': 'Равномерное распределение',
        'vertex_normal_params': 'Нормальное распределение',
        'vertex_lognormal_params': 'Усеченное логнормальное распределение',
        'vertex_stepwise_params': 'Ступенчатое распределение вершин',
        'edge_stepwise_params': 'Ступенчатое распределение ребер',
        
        # Лейблы параметров (что видит пользователь)
        'mean': 'среднее',
        'std': 'ст. откл.',
        'df': 'степ. св.',
        'scale': 'масштаб',
        'loc': 'локация',
        'shape': 'скошенность',
        'weight1': 'Вес первого режима',
        'gamma': 'сдвиг',
        'mu': 'масштаб',
        'sigma': 'форма',
        'mode1': 'Первый режим',
        'mode2': 'Второй режим',
        
        # Ступенчатое распределение
        'stages_count': 'Количество ступеней',
        'vertex_count_stage': 'Количество вершин в ступени',
        'edges_count_stage': 'Количество ребер в ступени',
        'presets': 'Шаблоны',
        'stage': 'Ступень',
        'left_bound': 'Левая граница',
        'right_bound': 'Правая граница',
        'market': 'Рыночный',
        'oligopoly': 'Олигополия',
        'uniform_preset': 'Равномерный',
        'pyramid': 'Пирамида',
        'exponential': 'Экспоненциальный',
        'social': 'Социальный',
        'economic': 'Экономический',
        'information': 'Информационный',
        'hierarchical': 'Иерархический',
        'ecosystem': 'Экосистемный',
        'infrastructure': 'Критический',
        'epidemic': 'Эпидемиологический',
        
        # Статистика (метки)
        'min_stat': 'Мин',
        'max_stat': 'Макс',
        'mean_stat': 'Среднее',
        'std_stat': 'Стд.откл.',
        'median': 'Медиана',
        'skewness': 'Асимметрия',
        'kurtosis': 'Эксцесс',
        'q05': 'Квантиль 5%',
        'q95': 'Квантиль 95%',
        'positive_connections': 'Положительных связей',
        'negative_connections': 'Отрицательных связей',
        'positive_sum': 'Сумма положительных',
        'negative_sum': 'Сумма отрицательных',
        'positive_mean': 'Среднее положительных',
        'negative_mean': 'Среднее отрицательных',
        
        # Статистика вершины
        'vertex_number': 'Вершина №',
        'vertex_weight': 'Вес вершины',
        'avg_edge_weight': 'Среднее связей',
        'positive_count': 'Положительных связей',
        'negative_count': 'Отрицательных связей',
        
        # Результаты симуляции
        'total_burned': 'Сгорело вершин',
        'total_iterations': 'Всего итераций',
        'spread_rate': 'Новые возгорания на шаге',
        'peak_new_burns': 'Макс. новых возгораний',
        'time_to_peak': 'Шагов до пика',
        'time_from_peak': 'Шагов от пика до конца',
        
        # Легенда
        'small_vertex': 'Маленькая вершина',
        'large_vertex': 'Большая вершина',
        'edge_neg1': 'Толщина ребра = -1',
        'edge_pos1': 'Толщина ребра = +1',
        'not_burned': 'Вершина не сгорела',
        'first_burned': 'Первая сгоревшая',
        'last_burned': 'Последняя сгоревшая',
        
        # Тексты для гистограмм
        'actual_edge_distribution': 'Распределение ребер',
        'actual_vertex_distribution': 'Распределение вершин',
        'num_bins': 'Бинов',
        
        # Заглушки
        'no_params': 'Нет дополнительных параметров',
        
        # Тексты в статистике (статичные)
        'vertex_count_stat': 'Количество вершин',
        'edge_count_stat': 'Количество ребер',
        'edge_dist_stat': 'Распределение ребер',
        'vertex_dist_stat': 'Распределение вершин',
        'resistance_stat': 'Устойчивость',
        'influence_stat': 'Влияние',
        'damping_stat': 'Затухание',
        
        # Коэффициенты
        'coeff': 'коэф.',

        'tab_generation': 'Генерация графа',
        'tab_custom': 'Пользовательский граф',
        'tab_simulation': 'Запуск симуляции',
        'tab_multiple': 'Множественная симуляция',
        'tab_help': 'Как пользоваться',
        'tab_settings': 'Настройки',

        # Текст для пустого состояния
        'no_graph_selected': 'Граф не выбран',
        'no_data': 'Нет данных',
        'build_graph_first': 'Постройте граф на вкладке "Генерация графа" или "Пользовательский граф"',
        
        # Настройки
        'settings_interface': 'Параметры интерфейса',
        'language': 'Язык',
        'settings_theme': 'Тема',
        'theme_light': 'Светлая',
        'theme_dark': 'Темная',
        'settings_reproducibility': 'Воспроизводимость',
        'settings_seed': 'Seed генерации',
        'settings_seed_random': 'Случайный',
        'settings_seed_fixed': 'Фиксированный',
        'settings_seed_note': 'Фиксированный seed гарантирует одинаковые графы при повторных запусках',
        'settings_visualization': 'Визуализация графа',
        'settings_layout_iterations': 'Итерации компоновки',
        'settings_layout_note': 'Количество итераций алгоритма компоновки. Больше = точнее, но медленнее',
        'settings_show_negative': 'Показывать отрицательные ребра',
        'settings_show_negative_note': 'Отрицательные связи отображаются фиолетовым',
    },
    
    'en': {
        # Основные кнопки
        'build_graph': 'Build graph',
        'back': 'Back',
        'start_fire': 'Start',
        'reset': 'Reset',
        'new_graph': 'New graph',
        
        # Разделы интерфейса
        'graph_parameters': 'Graph parameters',
        'graph_stats': 'Graph statistics',
        'edge_stats': 'Edge statistics',
        'vertex_stats': 'Vertex statistics',
        'legend': 'Legend',
        'simulation_results': 'Fire simulation results',
        'start_vertex_title': 'Starting vertex selection',
        'start_vertex_stats': 'Starting vertex statistics',
        
        # Параметры графа
        'vertex_count': 'Vertex count',
        'edge_distribution': 'Edge weight distribution',
        'vertex_distribution': 'Vertex weight distribution',
        'vertex_resistance': 'Vertex resistance',
        'vertex_influence': 'Vertex influence',
        'damping': 'Damping',
        
        # Значения для combobox (используем те же английские ключи)
        'Uniform': 'Uniform',
        'Normal': 'Normal',
        'Student': "Student",
        'Laplace': 'Laplace',
        'Bimodal': 'Bimodal',
        'Skewed_t': 'Skewed_t',
        
        'None': 'None',
        'Lognormal': 'Lognormal',
        'Stepwise': 'Stepwise',
        
        'resistance_none': 'None',
        'resistance_direct': 'Direct proportional to size',
        'resistance_inverse': 'Inversely proportional to size',
        
        'influence_none': 'None',
        'influence_direct': 'Direct proportional to size',
        'influence_inverse': 'Inversely proportional to size',
        
        'damping_none': 'None',
        'damping_exponential': 'Exponential',
        'damping_hyperbolic': 'Hyperbolic',
        'damping_discrete': 'Discrete',
        
        # Параметры распределений
        'uniform_params': 'Uniform distribution parameters',
        'normal_params': 'Normal distribution parameters',
        'student_params': "Student distribution parameters",
        'laplace_params': 'Laplace distribution parameters',
        'bimodal_params': 'Bimodal distribution parameters',
        'skewed_t_params': 'Skewed_t distribution parameters',
        'vertex_uniform_params': 'Uniform distribution',
        'vertex_normal_params': 'Normal distribution',
        'vertex_lognormal_params': 'Truncated lognormal distribution',
        'vertex_stepwise_params': 'Stepwise vertex distribution',
        'edge_stepwise_params': 'Stepwise edge distribution',
        
        # Лейблы параметров
        'mean': 'mean',
        'std': 'std',
        'df': 'degrees',
        'scale': 'scale',
        'loc': 'location',
        'shape': 'skewness',
        'weight1': 'Weight of first mode',
        'gamma': 'shift',
        'mu': 'scale',
        'sigma': 'shape',
        'mode1': 'First mode',
        'mode2': 'Second mode',
        
        # Ступенчатое распределение
        'stages_count': 'Number of stages',
        'vertex_count_stage': 'Number of vertices',
        'edges_count_stage': 'Number of edges',
        'presets': 'Presets',
        'stage': 'Stage',
        'left_bound': 'Left bound',
        'right_bound': 'Right bound',
        'market': 'Market',
        'oligopoly': 'Oligopoly',
        'uniform_preset': 'Uniform',
        'pyramid': 'Pyramid',
        'exponential': 'Exponential',
        'social': 'Social',
        'economic': 'Economic',
        'information': 'Information',
        'hierarchical': 'Hierarchical',
        'ecosystem': 'Ecosystem',
        'infrastructure': 'Critical',
        'epidemic': 'Epidemiological',
        
        # Статистика
        'min_stat': 'Min',
        'max_stat': 'Max',
        'mean_stat': 'Mean',
        'std_stat': 'Std',
        'median': 'Median',
        'skewness': 'Skewness',
        'kurtosis': 'Kurtosis',
        'q05': '5% Quantile',
        'q95': '95% Quantile',
        'positive_connections': 'Positive connections',
        'negative_connections': 'Negative connections',
        'positive_sum': 'Positive sum',
        'negative_sum': 'Negative sum',
        'positive_mean': 'Positive mean',
        'negative_mean': 'Negative mean',
        
        # Статистика вершины
        'vertex_number': 'Vertex #',
        'vertex_weight': 'Vertex weight',
        'avg_edge_weight': 'Average edge weight',
        'positive_count': 'Positive connections',
        'negative_count': 'Negative connections',
        
        # Результаты симуляции
        'total_burned': 'Total burned vertices',
        'total_iterations': 'Total iterations',
        'spread_rate': 'New fires at step',
        'peak_new_burns': 'Peak new fires',
        'time_to_peak': 'Steps to peak',
        'time_from_peak': 'Steps from peak to end',
        
        # Легенда
        'small_vertex': 'Small vertex',
        'large_vertex': 'Large vertex',
        'edge_neg1': 'Edge weight = -1',
        'edge_pos1': 'Edge weight = +1',
        'not_burned': 'Not burned vertex',
        'first_burned': 'First burned',
        'last_burned': 'Last burned',

        # Тексты для гистограмм
        'actual_edge_distribution': 'Actual edge distribution',
        'actual_vertex_distribution': 'Actual vertex distribution',
        'num_bins': 'Bins',
        
        # Заглушки
        'no_params': 'No additional parameters',
        
        # Тексты в статистике
        'vertex_count_stat': 'Vertex count',
        'edge_count_stat': 'Edge count',
        'edge_dist_stat': 'Edge distribution',
        'vertex_dist_stat': 'Vertex distribution',
        'resistance_stat': 'Resistance',
        'influence_stat': 'Influence',
        'damping_stat': 'Damping',
        
        # Коэффициенты
        'coeff': 'coeff.',

        'tab_generation': 'Graph Generation',
        'tab_custom': 'Custom Graph',
        'tab_simulation': 'Run Simulation',
        'tab_multiple': 'Multiple Simulation',
        'tab_help': 'How to Use',
        'tab_settings': 'Settings',

        # Текст для пустого состояния
        'no_graph_selected': 'No graph selected',
        'no_data': 'No data',
        'build_graph_first': 'Build a graph on the "Graph Generation" or "Custom Graph" tab',
        
        # Настройки
        'settings_interface': 'Interface parameters',
        'language': 'Language',
        'settings_theme': 'Theme',
        'theme_light': 'Light',
        'theme_dark': 'Dark',
        'settings_reproducibility': 'Reproducibility',
        'settings_seed': 'Generation seed',
        'settings_seed_random': 'Random',
        'settings_seed_fixed': 'Fixed',
        'settings_seed_note': 'Fixed seed ensures identical graphs in repeated runs',
        'settings_visualization': 'Graph visualization',
        'settings_layout_iterations': 'Layout iterations',
        'settings_layout_note': 'Number of layout algorithm iterations. Higher = more precise, slower',
        'settings_show_negative': 'Show negative edges',
        'settings_show_negative_note': 'Negative edges are displayed in purple',
        
    }
}

class Translator:
    def __init__(self, language='ru'):
        self.language = language
    
    def t(self, key, *args):
        """Переводчик"""
        global TRANSLATIONS
        text = TRANSLATIONS.get(self.language, {}).get(key, key)
        if args:
            try:
                if '{}' in text:
                    return text.format(*args)
                else:
                    return f"{text} {' '.join(str(arg) for arg in args)}"
            except:
                return text
        return text
    
    def get_english_key(self, localized_value):
        """Получает английский ключ по локализованному значению"""
        if localized_value is None:
            return "None"
        if localized_value in TRANSLATIONS['en']:
            return localized_value
        for lang in TRANSLATIONS:
            for eng_key, localized in TRANSLATIONS[lang].items():
                if localized == localized_value:
                    return eng_key
        return localized_value
    
    def set_language(self, language):
        if language in TRANSLATIONS:
            self.language = language
            return True
        return False


# In[3]:


# Цветовые темы
THEME_COLORS = {
    'light': {
        # Основные цвета фона
        'bg_color': "#ffffff",              # Основной фон приложения
        'frame_bg': "#ffffff",              # Фон рамок и панелей
        'plot_bg': "#ffffff",               # Фон графиков
        'plot_grid': "#f0f0f0",             # Сетка на графиках
        
        # Акцентные цвета
        'accent_color': "#4a6fa5",          # Основной акцентный цвет
        'input_highlight': "#4a6fa5",       # Выделение в полях ввода
        
        # Цвета текста
        'text_color': "#000000",            # Основной текст
        'text_secondary': "#666666",        # Вторичный текст
        'plot_text': "#000000",             # Текст на графиках
        'btn_text': "#222222",              # Текст на кнопках
        
        # Цвета границ и разделителей
        'border_color': "#cccccc",          # Основные границы
        'separator': "#e1e1e1",             # Разделительные линии
        
        # Цвета полей ввода
        'input_bg': "#f0f0f0",              # Фон полей ввода
        'input_fg': "#000000",              # Текст в полях ввода
        'input_cursor': "#000000",          # Курсор в полях ввода
        
        # Цвета стандартных кнопок
        'btn_color': "#e0e0e0",             # Фон обычных кнопок
        'btn_hover': "#d0d0d0",             # Кнопки при наведении
        
        # Цвета специальных кнопок симуляции
        'fire_start': "#D2691E",            # Кнопка "Начать пожар"
        'fire_hover': "#B85A1A",            # Кнопка "Начать пожар" при наведении
        'reset_color': "#6B8E23",           # Кнопка "Сбросить"
        'reset_hover': "#5A771E",           # Кнопка "Сбросить" при наведении
        'new_graph_color': "#9370DB",       # Кнопка "Новый граф"
        'new_graph_hover': "#7D5FC5",       # Кнопка "Новый граф" при наведении
        
        # Цвета элементов графа
        'graph_vertex': "#bbdefb",          # Фон вершин
        'graph_vertex_border': "#000000",   # Границы вершин
        'graph_edge_negative': "#762a83",   # Отрицательные рёбра
        'graph_edge_positive': "#1b7837",   # Положительные рёбра
        
        # Цвета легенды графа
        'graph_legend_small': "#bbdefb",    # Маленькие вершины
        'graph_legend_large': "#bbdefb",    # Большие вершины
        'graph_legend_not_burned': "#bbdefb", # Не сгоревшие вершины
        'graph_legend_first_burned': "#b71c1c", # Первые сгоревшие вершины
        'graph_legend_last_burned': "#ffd54f",  # Последние сгоревшие вершины
        
        # Цвета для ступенчатого распределения
        'edge_stepwise_colors': ['#80ccff', '#66b8ff', '#4da3f2', '#338fe6', '#1a7ad9', '#0066cc'],
        'stepwise_colors': ['#ffe4ec', '#ffb7d5', '#ff8abf', '#ff5da8', '#ff3092', '#ff037b'],   
    
        # Цвета для плотности распределения
        'density_color': "#2196f3",         # Линия плотности
        'vertex_density_color': "#c2185b",  # Плотность вершин
        
        # Цвета слайдеров
        'slider_trough': "#f0f0f0",         # Дорожка слайдера
        'slider_thumb': "#ffffff",          # Ползунок слайдера
        'slider_thumb_active': "#ffffff",   # Ползунок при активации
        'slider_frame': "#cccccc",          # Рамка слайдера
        
        # Цвета полос прокрутки
        'scrollbar_trough': "#cccccc",      # Дорожка прокрутки
        'scrollbar_slider': "#ffffff",      # Ползунок прокрутки
        'scrollbar_slider_active': "#ffffff", # Ползунок при активации
        'scrollbar_frame': "#cccccc",       # Рамка прокрутки
        'scrollbar_arrow': "#666666",       # Стрелки прокрутки
        
        # Цвета для Spinbox
        'spinbox_bg': "#f0f0f0",            # Фон Spinbox
        'spinbox_fg': "#000000",            # Текст Spinbox
        'spinbox_button': "#f0f0f0",        # Кнопки Spinbox
        'spinbox_button_hover': "#f0f0f0",  # Кнопки при наведении

        'tab1_inactive': '#E4DFF0',
        'tab1_active': '#B3A5CC',
        'tab2_inactive': '#F0DEE8',
        'tab2_active': '#C0B2C0',
        'tab3_inactive': '#F8E4D9',
        'tab3_active': '#C6B6AD',
        'tab4_inactive': '#F3E5DD',
        'tab4_active': '#C2B7B1',
        'tab5_inactive': '#E6EDE0',
        'tab5_active': '#B8BEB3',
        'tab6_inactive': '#F0EBDF',
        'tab6_active': '#C0BCB2',
        'tab_border': '#CCCCCC',
        'tab_text_inactive': '#000000',
        'tab_text_active': '#000000',
    },
    
    'dark': {
        # Основные цвета фона
        'bg_color': "#1a1a1a",              # Основной фон приложения
        'frame_bg': "#1a1a1a",              # Фон рамок и панелей
        'plot_bg': "#1a1a1a",               # Фон графиков
        'plot_grid': "#3d3d3d",             # Сетка на графиках
        
        # Акцентные цвета
        'accent_color': "#5d8cc8",          # Основной акцентный цвет
        'input_highlight': "#5d8cc8",       # Выделение в полях ввода
        
        # Цвета текста
        'text_color': "#ffffff",            # Основной текст
        'text_secondary': "#aaaaaa",        # Вторичный текст
        'plot_text': "#ffffff",             # Текст на графиках
        'btn_text': "#ffffff",              # Текст на кнопках
        
        # Цвета границ и разделителей
        'border_color': "#666666",          # Основные границы
        'separator': "#666666",             # Разделительные линии
        
        # Цвета полей ввода
        'input_bg': "#444444",              # Фон полей ввода
        'input_fg': "#ffffff",              # Текст в полях ввода
        'input_cursor': "#ffffff",          # Курсор в полях ввода
        
        # Цвета стандартных кнопок
        'btn_color': "#2d2d2d",             # Фон обычных кнопок
        'btn_hover': "#262626",             # Кнопки при наведении
        
        # Цвета специальных кнопок симуляции
        'fire_start': "#FF7043",            # Кнопка "Начать пожар"
        'fire_hover': "#E55C2E",            # Кнопка "Начать пожар" при наведении
        'reset_color': "#4CAF50",           # Кнопка "Сбросить"
        'reset_hover': "#3E8C41",           # Кнопка "Сбросить" при наведении
        'new_graph_color': "#7E57C2",       # Кнопка "Новый граф"
        'new_graph_hover': "#6A45A5",       # Кнопка "Новый граф" при наведении
        
        # Цвета элементов графа
        'graph_vertex': "#37474f",          # Фон вершин
        'graph_vertex_border': "#ffffff",   # Границы вершин
        'graph_edge_negative': "#ab47bc",   # Отрицательные рёбра
        'graph_edge_positive': "#66bb6a",   # Положительные рёбра
        
        # Цвета легенды графа
        'graph_legend_small': "#546e7a",    # Маленькие вершины
        'graph_legend_large': "#546e7a",    # Большие вершины
        'graph_legend_not_burned': "#546e7a", # Не сгоревшие вершины
        'graph_legend_first_burned': "#ef5350", # Первые сгоревшие вершины
        'graph_legend_last_burned': "#ffca28",  # Последние сгоревшие вершины
        
        # Цвета для ступенчатого распределения
        'edge_stepwise_colors': ['#4d94ff', '#4282e7', '#3871d0', '#2d60b9', '#224fa3', '#183e8c'], 
        'stepwise_colors': ['#ff478c', '#e74282', '#d03d78', '#b9386e', '#a13364', '#8a2e5a'],  
        
        # Цвета для плотности распределения
        'density_color': "#5d8cc8",         # Линия плотности
        'vertex_density_color': "#e91e63",  # Плотность вершин
        
        # Цвета слайдеров
        'slider_trough': "#444444",         # Дорожка слайдера
        'slider_thumb': "#2d2d2d",          # Ползунок слайдера
        'slider_thumb_active': "#2d2d2d",   # Ползунок при активации
        'slider_frame': "#444444",          # Рамка слайдера
        
        # Цвета полос прокрутки
        'scrollbar_trough': "#444444",      # Дорожка прокрутки
        'scrollbar_slider': "#2d2d2d",      # Ползунок прокрутки
        'scrollbar_slider_active': "#2d2d2d", # Ползунок при активации
        'scrollbar_frame': "#444444",       # Рамка прокрутки
        'scrollbar_arrow': "#aaaaaa",       # Стрелки прокрутки
        
        # Цвета для Spinbox
        'spinbox_bg': "#3d3d3d",            # Фон Spinbox
        'spinbox_fg': "#ffffff",            # Текст Spinbox
        'spinbox_button': "#3d3d3d",        # Кнопки Spinbox
        'spinbox_button_hover': "#3d3d3d",  # Кнопки при наведении

        'tab1_inactive': '#2B1E40',
        'tab1_active': '#684999',
        'tab2_inactive': '#481931',
        'tab2_active': '#AD3D76',
        'tab3_inactive': '#592F11',
        'tab3_active': '#D67129',
        'tab4_inactive': '#422009',
        'tab4_active': '#9F4E15',
        'tab5_inactive': '#313C1C',
        'tab5_active': '#779144',
        'tab6_inactive': '#463618',
        'tab6_active': '#A8833B',
        'tab_border': '#444444',
        'tab_text_inactive': '#FFFFFF',
        'tab_text_active': '#FFFFFF',
    }
}


# In[4]:


# Пресеты для вершин
VERTEX_TIER_PRESETS = {
    "market": {  # Рыночное распределение
        2: {"bounds": [(0.0, 0.2), (0.2, 1.0)], "counts": [80, 20]},
        3: {"bounds": [(0.0, 0.1), (0.1, 0.35), (0.35, 1.0)], "counts": [70, 20, 10]},
        4: {"bounds": [(0.0, 0.05), (0.05, 0.2), (0.2, 0.5), (0.5, 1.0)], "counts": [60, 25, 10, 5]},
        5: {"bounds": [(0.0, 0.03), (0.03, 0.15), (0.15, 0.35), (0.35, 0.65), (0.65, 1.0)], "counts": [50, 25, 15, 7, 3]},
        6: {"bounds": [(0.0, 0.02), (0.02, 0.1), (0.1, 0.25), (0.25, 0.45), (0.45, 0.75), (0.75, 1.0)], "counts": [40, 25, 15, 10, 7, 3]}
    },
    "oligopoly": {  # Олигополия
        2: {"bounds": [(0.0, 0.05), (0.05, 1.0)], "counts": [95, 5]},
        3: {"bounds": [(0.0, 0.03), (0.03, 0.2), (0.2, 1.0)], "counts": [85, 12, 3]},
        4: {"bounds": [(0.0, 0.02), (0.02, 0.12), (0.12, 0.35), (0.35, 1.0)], "counts": [75, 15, 7, 3]},
        5: {"bounds": [(0.0, 0.01), (0.01, 0.08), (0.08, 0.25), (0.25, 0.5), (0.5, 1.0)], "counts": [65, 20, 10, 4, 1]},
        6: {"bounds": [(0.0, 0.005), (0.005, 0.06), (0.06, 0.2), (0.2, 0.4), (0.4, 0.65), (0.65, 1.0)], "counts": [55, 25, 12, 5, 2, 1]}
    },
    "uniform": {  # Равномерное
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
        5: {"bounds": [(0.0, 0.03), (0.03, 0.18), (0.18, 0.38), (0.38, 0.65), (0.65, 1.0)], "counts": [50, 25, 15, 7, 3]},
        6: {"bounds": [(0.0, 0.02), (0.02, 0.13), (0.13, 0.28), (0.28, 0.48), (0.48, 0.73), (0.73, 1.0)], "counts": [40, 25, 15, 10, 7, 3]}
    },
    "exponential": {  # Экспоненциальное
        2: {"bounds": [(0.0, 0.1), (0.1, 1.0)], "counts": [90, 10]},
        3: {"bounds": [(0.0, 0.05), (0.05, 0.25), (0.25, 1.0)], "counts": [80, 15, 5]},
        4: {"bounds": [(0.0, 0.03), (0.03, 0.15), (0.15, 0.4), (0.4, 1.0)], "counts": [70, 20, 8, 2]},
        5: {"bounds": [(0.0, 0.02), (0.02, 0.1), (0.1, 0.25), (0.25, 0.5), (0.5, 1.0)], "counts": [60, 25, 10, 4, 1]},
        6: {"bounds": [(0.0, 0.01), (0.01, 0.07), (0.07, 0.18), (0.18, 0.35), (0.35, 0.6), (0.6, 1.0)], "counts": [50, 25, 15, 6, 3, 1]}
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
    "uniform": {  # Равномерное
        2: {"bounds": [(-1.0, 0.0), (0.0, 1.0)], "counts": [50, 50]},
        3: {"bounds": [(-1.0, -0.33), (-0.33, 0.33), (0.33, 1.0)], "counts": [33, 34, 33]},
        4: {"bounds": [(-1.0, -0.5), (-0.5, 0.0), (0.0, 0.5), (0.5, 1.0)], "counts": [25, 25, 25, 25]},
        5: {"bounds": [(-1.0, -0.6), (-0.6, -0.2), (-0.2, 0.2), (0.2, 0.6), (0.6, 1.0)], "counts": [20, 20, 20, 20, 20]},
        6: {"bounds": [(-1.0, -0.66), (-0.66, -0.33), (-0.33, 0.0), (0.0, 0.33), (0.33, 0.66), (0.66, 1.0)], "counts": [17, 17, 16, 17, 16, 17]}
    }
}


# In[5]:


def get_vertex_preset(preset_key, stages_count):
    """Получает пресет для вершин по ключу и количеству ступеней"""
    if preset_key not in VERTEX_TIER_PRESETS:
        preset_key = 'uniform'
    preset_dict = VERTEX_TIER_PRESETS[preset_key]
    if stages_count in preset_dict:
        return preset_dict[stages_count]
    else:
        available_stages = list(preset_dict.keys())
        nearest_stage = min(available_stages, key=lambda x: abs(x - stages_count))
        return preset_dict[nearest_stage]

def get_edge_preset(preset_key, stages_count):
    """Получает пресет для ребер по ключу и количеству ступеней"""
    if preset_key not in EDGE_TIER_PRESETS:
        preset_key = 'uniform'
    preset_dict = EDGE_TIER_PRESETS[preset_key]
    if stages_count in preset_dict:
        return preset_dict[stages_count]
    else:
        available_stages = list(preset_dict.keys())
        nearest_stage = min(available_stages, key=lambda x: abs(x - stages_count))
        return preset_dict[nearest_stage]

def get_all_vertex_preset_keys():
    """Возвращает все ключи пресетов для вершин"""
    return list(VERTEX_TIER_PRESETS.keys())

def get_all_edge_preset_keys():
    """Возвращает все ключи пресетов для ребер"""
    return list(EDGE_TIER_PRESETS.keys())


# In[6]:


class ThemeObserver:
    """Подписка на изменения темы"""
    def __init__(self, *args, theme_manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        if theme_manager is not None:
            self._theme_manager = theme_manager
        elif hasattr(self, 'master') and self.master and hasattr(self.master, '_theme_manager'):
            self._theme_manager = self.master._theme_manager
        else:
            self._theme_manager = None
        if self._theme_manager:
            self._theme_manager.subscribe(self)
            self._theme_attrs = {}
            self._update_theme_colors()
            self._apply_theme()
    
    def on_theme_changed(self, theme_name):
        """Вызывается при смене темы"""
        self._update_theme_colors()
        self._apply_theme()
    
    def _update_theme_colors(self):
        """Обновляет словарь цветов - переопределяется в наследниках"""
        pass
    
    def _apply_theme(self):
        """Применяет цвета"""
        for attr, value in self._theme_attrs.items():
            try:
                self.configure(**{attr: value})
            except (tk.TclError, AttributeError):
                pass
    
    def destroy(self):
        """Отписываемся при уничтожении"""
        if self._theme_manager:
            self._theme_manager.unsubscribe(self)
        try:
            super().destroy()
        except:
            pass


# In[7]:


class ThemeManager:
    def __init__(self, theme='light'):
        self.theme = theme
        self.colors = THEME_COLORS.get(theme, THEME_COLORS['light'])
        self.palettes = self._get_palettes_for_theme(theme)
        self._observers = []
        self._updating = False
    
    def _get_palettes_for_theme(self, theme):
        if theme == 'dark':
            return {
                'edge_cmap': 'PRGn',
                'fire_cmap': 'YlOrRd',
                'vertex_cmap': 'viridis'
            }
        else:
            return {
                'edge_cmap': 'PRGn',
                'fire_cmap': 'YlOrRd',
                'vertex_cmap': 'viridis'
            }
    
    def get_color(self, color_name):
        return self.colors.get(color_name, self.colors['bg_color'])
    
    def get_palette(self, palette_name):
        return self.palettes.get(palette_name, 'viridis')
    
    def subscribe(self, observer):
        """Виджет подписывается"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def unsubscribe(self, observer):
        """Виджет отписывается"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def set_theme(self, theme):
        """Изменяем тему и уведомляем всех"""
        if theme in THEME_COLORS and not self._updating:
            self._updating = True
            self.theme = theme
            self.colors = THEME_COLORS[theme]
            self.palettes = self._get_palettes_for_theme(theme)
            # Уведомляем всех наблюдателей
            for observer in self._observers[:]:
                try:
                    observer.on_theme_changed(theme)
                except:
                    if observer in self._observers:
                        self._observers.remove(observer)
            
            self._updating = False
            return True
        return False


# In[8]:


class ThemedFrame(ThemeObserver, tk.Frame):
    """Фрейм с поддержкой тем"""
    def _update_theme_colors(self):
        if not self._theme_manager:
            return
        self._theme_attrs = {
            'bg': self._theme_manager.get_color('frame_bg'),
            'highlightbackground': self._theme_manager.get_color('border_color'),
            'highlightcolor': self._theme_manager.get_color('border_color')
        }

class ThemedLabel(ThemeObserver, tk.Label):
    """Метка с поддержкой тем"""
    def _update_theme_colors(self):
        if not self._theme_manager:
            return
        self._theme_attrs = {
            'bg': self._theme_manager.get_color('frame_bg'),
            'fg': self._theme_manager.get_color('text_color')
        }

class ThemedButton(ThemeObserver, tk.Button):
    """Кнопка с поддержкой тем"""
    def _update_theme_colors(self):
        if not self._theme_manager:
            return
        self._theme_attrs = {
            'bg': self._theme_manager.get_color('btn_color'),
            'fg': self._theme_manager.get_color('btn_text'),
            'activebackground': self._theme_manager.get_color('btn_hover'),
            'activeforeground': self._theme_manager.get_color('btn_text')
        }

class ThemedEntry(ThemeObserver, tk.Entry):
    """Поле ввода с поддержкой тем"""
    def _update_theme_colors(self):
        if not self._theme_manager:
            return
        self._theme_attrs = {
            'bg': self._theme_manager.get_color('input_bg'),
            'fg': self._theme_manager.get_color('input_fg'),
            'insertbackground': self._theme_manager.get_color('input_cursor')
        }

class ThemedScale(ThemeObserver, tk.Scale):
    """Слайдер с поддержкой тем"""
    def _update_theme_colors(self):
        if not self._theme_manager:
            return
        self._theme_attrs = {
            'bg': self._theme_manager.get_color('slider_thumb'),
            'troughcolor': self._theme_manager.get_color('slider_trough'),
            'highlightbackground': self._theme_manager.get_color('slider_frame'),
            'fg': self._theme_manager.get_color('text_color')
        }

class ThemedSpinbox(ThemeObserver, tk.Spinbox):
    """Spinbox с поддержкой тем"""
    def _update_theme_colors(self):
        if not self._theme_manager:
            return
        self._theme_attrs = {
            'bg': self._theme_manager.get_color('spinbox_bg'),
            'fg': self._theme_manager.get_color('spinbox_fg'),
            'buttonbackground': self._theme_manager.get_color('spinbox_button')
        }

class ThemedCanvas(ThemeObserver, tk.Canvas):
    """Canvas с поддержкой тем"""
    def _update_theme_colors(self):
        if not self._theme_manager:
            return
        self._theme_attrs = {
            'bg': self._theme_manager.get_color('frame_bg'),
            'highlightbackground': self._theme_manager.get_color('border_color')
        }


# In[9]:


class ThemedGraphWidget(ThemeObserver):
    """Класс для графиков matplotlib с поддержкой тем"""
    def __init__(self, parent, theme_manager=None, translator=None, **kwargs):
        self.parent = parent
        self.theme_manager = theme_manager
        self.translator = translator
        self.frame = tk.Frame(parent, bg=self.theme_manager.get_color('frame_bg') if theme_manager else '#ffffff')
        # Подписываемся на изменения темы
        if self.theme_manager:
            self.theme_manager.subscribe(self)
        self.fig = Figure(figsize=(2, 1.5), dpi=80, facecolor=self.theme_manager.get_color('plot_bg') if theme_manager else '#ffffff')
        self.ax = self.fig.add_subplot(111)
        self._apply_theme_to_plot()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().config(width=160, height=120)
        self.canvas.get_tk_widget().pack(padx=5, pady=5)
        self._init_custom(**kwargs)
    
    def _init_custom(self, **kwargs):
        """Для переопределения в наследниках"""
        pass
    
    def on_theme_changed(self, theme_name):
        """Обновление цвета графика"""
        self._apply_theme_to_plot()
        self.redraw()
        self.canvas.draw()
    
    def _apply_theme_to_plot(self):
        """Применяет текущую тему к графику"""
        if not self.theme_manager:
            return
        plot_bg = self.theme_manager.get_color('plot_bg')
        plot_text = self.theme_manager.get_color('plot_text')
        plot_grid = self.theme_manager.get_color('plot_grid')
        self.fig.set_facecolor(plot_bg)
        self.ax.set_facecolor(plot_bg)
        self.ax.tick_params(axis='both', colors=plot_text)
        for spine in self.ax.spines.values():
            spine.set_color(plot_text)
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_color(plot_text)
        self.ax.grid(True, alpha=0.3, linestyle='--', color=plot_grid)
    
    def redraw(self):
        """Перерисовка данных - переопределяется в наследниках"""
        pass
    
    def destroy(self):
        """Отписываемся при уничтожении"""
        if self.theme_manager:
            self.theme_manager.unsubscribe(self)
        self.frame.destroy()
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def place(self, **kwargs):
        self.frame.place(**kwargs)


# In[10]:


class EdgeWeightPlotWidget(ThemedGraphWidget):
    """Виджет для отображения плотности распределения ребер"""
    
    def __init__(self, parent, theme_manager=None, translator=None):
        super().__init__(parent, theme_manager, translator)

        if self.theme_manager:
            self.edge_color = self.theme_manager.get_color('density_color')
            self.edge_stepwise_colors = self.theme_manager.get_color('edge_stepwise_colors')
        else:
            self.edge_color = "#2196f3"
            self.edge_stepwise_colors = ['#0066cc', '#1a7ad9', '#338fe6', '#4da3f2', '#66b8ff', '#80ccff']

        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(0, 5)
        self.ax.set_xticks([-1, -0.5, 0, 0.5, 1])
        self.ax.set_yticks([])
        self.ax.tick_params(axis='both', which='major', labelsize=7)
        self._last_params = None
    
    def on_theme_changed(self, theme_name):
        """Обновляем цвета при смене темы"""
        if self.theme_manager:
            self.edge_color = self.theme_manager.get_color('density_color')
            self.edge_stepwise_colors = self.theme_manager.get_color('edge_stepwise_colors')
        self._apply_theme_to_plot()
        if self._last_params:
            self.update_plot(self._last_params)
        else:
            self.canvas.draw()
    
    def update_plot(self, dist_params):
        """Обновление графика плотности распределения ребер"""
        self.ax.clear()
        self._last_params = dist_params
        try:
            dist_type = dist_params.get("type", "Unknown")
            if self.translator:
                dist_type = self.translator.get_english_key(dist_type)
            
            x = np.linspace(-1, 1, 400)
            y = np.zeros_like(x)
        
            if dist_type == "Uniform":
                min_val = dist_params["min"]
                max_val = dist_params["max"]
                if min_val >= max_val:
                    raise ValueError("min должен быть меньше max")
                mask = (x >= min_val) & (x <= max_val)
                y[mask] = 1 / (max_val - min_val)
                self.ax.fill_between(x, y, where=mask, alpha=0.3, color=self.edge_color)
                self.ax.plot(x, y, self.edge_color, linewidth=1.5)
                
            elif dist_type == "Normal":
                mu = dist_params["mu"]
                sigma = dist_params["sigma"]
                if sigma <= 0:
                    raise ValueError("sigma должен быть > 0")
                a, b = (-1 - mu) / sigma, (1 - mu) / sigma
                y = truncnorm.pdf(x, a, b, loc=mu, scale=sigma)
                self.ax.fill_between(x, y, alpha=0.3, color=self.edge_color)
                self.ax.plot(x, y, self.edge_color, linewidth=1.5)
                
            elif dist_type == "Student":
                df = dist_params["df"]
                scale = dist_params["scale"]
                if df <= 0 or scale <= 0:
                    raise ValueError("df и scale должны быть > 0")
                mask = (x >= -1) & (x <= 1)
                y_full = stats_t.pdf(x, df, scale=scale)
                if np.sum(y_full[mask]) > 0:
                    y = np.where(mask, y_full, 0)
                    area = np.trapezoid(y[mask], x[mask])
                    if area > 0:
                        y = y / area
                self.ax.fill_between(x, y, where=mask, alpha=0.3, color=self.edge_color)
                self.ax.plot(x, y, self.edge_color, linewidth=1.5)
                
            elif dist_type == "Laplace":
                loc = dist_params["loc"]
                scale = dist_params["scale"]
                if scale <= 0:
                    raise ValueError("scale должен быть > 0")
                mask = (x >= -1) & (x <= 1)
                y_full = laplace.pdf(x, loc=loc, scale=scale)
                if np.sum(y_full[mask]) > 0:
                    y = np.where(mask, y_full, 0)
                    area = np.trapezoid(y[mask], x[mask])
                    if area > 0:
                        y = y / area
                self.ax.fill_between(x, y, where=mask, alpha=0.3, color=self.edge_color)
                self.ax.plot(x, y, self.edge_color, linewidth=1.5)
                
            elif dist_type == "Bimodal":
                mu1 = dist_params["mu1"]
                sigma1 = dist_params["sigma1"]
                mu2 = dist_params["mu2"]
                sigma2 = dist_params["sigma2"]
                weight1 = dist_params["weight1"]
                if sigma1 <= 0 or sigma2 <= 0 or weight1 < 0 or weight1 > 1:
                    raise ValueError("Некорректные параметры бимодального распределения")
                a1, b1 = (-1 - mu1) / sigma1, (1 - mu1) / sigma1
                a2, b2 = (-1 - mu2) / sigma2, (1 - mu2) / sigma2
                y1 = truncnorm.pdf(x, a1, b1, loc=mu1, scale=sigma1) * weight1
                y2 = truncnorm.pdf(x, a2, b2, loc=mu2, scale=sigma2) * (1 - weight1)
                y = y1 + y2
                self.ax.fill_between(x, y, alpha=0.3, color=self.edge_color)
                self.ax.plot(x, y, self.edge_color, linewidth=1.5)
                
            elif dist_type == "Skewed_t":
                df = dist_params["df"]
                shape = dist_params["shape"]
                scale = dist_params["scale"]
                if df <= 0 or scale <= 0:
                    raise ValueError("df и scale должны быть > 0")
                samples = nct.rvs(df, shape, scale=scale, size=5000)
                samples = np.clip(samples, -1, 1)
                if len(samples) == 0 or np.std(samples) <= 0:
                    raise ValueError("Не удалось сгенерировать выборку для KDE")
                kde = gaussian_kde(samples)
                y = kde(x)
                self.ax.fill_between(x, y, alpha=0.3, color=self.edge_color)
                self.ax.plot(x, y, self.edge_color, linewidth=1.5)
                
            elif dist_type == "Stepwise":
                stages = dist_params.get("stages", [])
                if not stages:
                    raise ValueError("Не заданы ступени")
                
                self.ax.set_xlim(-1, 1)
                
                total_count = sum(max(0.0, stage["weight"]) for stage in stages)
                if total_count <= 0:
                    total_count = 1.0
                
                max_height = 0
                for i, stage in enumerate(stages):
                    left = max(-1.0, min(1.0, stage["left"]))
                    right = max(-1.0, min(1.0, stage["right"]))
                    if right <= left:
                        right = min(1.0, left + 0.1)
                    
                    count = max(0.0, stage["weight"])
                    height = (count / total_count) * 8.0
                    max_height = max(max_height, height)
                    
                    color = self._get_stepwise_color(i / max(len(stages) - 1, 1))
                    self.ax.bar(left, height, width=right - left, align='edge', 
                               color=color, edgecolor=self.edge_color, alpha=0.7, linewidth=1)
                    
                    # Вертикальные линии
                    self.ax.axvline(x=left, color=self.edge_color, linestyle='--', alpha=0.5, linewidth=0.8)
                    if i == len(stages) - 1:
                        self.ax.axvline(x=right, color=self.edge_color, linestyle='--', alpha=0.5, linewidth=0.8)
                
                self.ax.set_ylim(0, max_height * 1.3)
                
            else:
                # Если тип не распознан
                self.ax.set_xlim(-1, 1)
                self.ax.set_ylim(0, 5)
                self.ax.set_xticks([-1, -0.5, 0, 0.5, 1])
                self.ax.set_yticks([])
                self.ax.tick_params(axis='both', which='major', labelsize=7)
                self._apply_theme_to_plot()
                self.canvas.draw()
                return
            
            # Настройка осей для непрерывных распределений
            if dist_type != "Stepwise":
                if len(y) > 0 and np.max(y) > 0:
                    y_max = np.max(y) * 1.2
                    self.ax.set_ylim(0, max(y_max, 0.5))
                else:
                    self.ax.set_ylim(0, 5)
            
            self.ax.set_xlim(-1, 1)
            self.ax.set_xticks([-1, -0.5, 0, 0.5, 1])
            self.ax.set_yticks([])
            self.ax.tick_params(axis='both', which='major', labelsize=7)
            
        except Exception as e:
            print(f"Ошибка при построении графика плотности: {e}")
            self.ax.clear()
            self.ax.set_xlim(-1, 1)
            self.ax.set_ylim(0, 5)
            self.ax.set_xticks([-1, -0.5, 0, 0.5, 1])
            self.ax.set_yticks([])
            self.ax.set_title("Ошибка", fontsize=8, pad=2, color='red')
        
        # Применяем тему
        self._apply_theme_to_plot()
        self.canvas.draw()
    
    def _get_stepwise_color(self, intensity):
        """Генерация градиентного цвета для ступеней ребер"""
        intensity = max(0.0, min(1.0, intensity))
        idx = int(intensity * (len(self.edge_stepwise_colors) - 1))
        return self.edge_stepwise_colors[idx]
    
    def pack(self, **kwargs):
        """Упаковка виджета"""
        self.frame.pack(**kwargs)
        
    def place(self, **kwargs):
        """Размещение виджета"""
        self.frame.place(**kwargs)


# In[11]:


class VertexWeightPlotWidget(ThemedGraphWidget):
    """Виджет для отображения плотности распределения весов вершин"""
    
    def __init__(self, parent, theme_manager=None, translator=None):
        super().__init__(parent, theme_manager, translator)

        if self.theme_manager:
            self.vertex_color = self.theme_manager.get_color('vertex_density_color')
            self.stepwise_colors = self.theme_manager.get_color('stepwise_colors')
        else:
            self.vertex_color = "#c2185b"
            self.stepwise_colors = ['#f8bbd0', '#f48fb1', '#ec407a', '#d81b60', '#c2185b', '#880e4f']
            
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 10)
        self.ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        self.ax.set_yticks([])
        self.ax.tick_params(axis='both', which='major', labelsize=7)
        self._last_dist_type = None
        self._last_params = None
    
    def on_theme_changed(self, theme_name):
        """Обновляет цвета при смене темы"""
        if self.theme_manager:
            self.vertex_color = self.theme_manager.get_color('vertex_density_color')
            self.stepwise_colors = self.theme_manager.get_color('stepwise_colors')
        self._apply_theme_to_plot()
        if self._last_dist_type and self._last_params:
            self.update_plot(self._last_dist_type, self._last_params)
        else:
            self.canvas.draw()
    
    def update_plot(self, dist_type, dist_params):
        """Обновление графика плотности весов вершин"""
        self.ax.clear()
        self._last_dist_type = dist_type
        self._last_params = dist_params
        try:
            if dist_type == "Uniform":
                min_val = dist_params["min"]
                max_val = dist_params["max"]
                if min_val >= max_val:
                    raise ValueError("min должен быть меньше max")
                x = np.linspace(0, 1, 400)
                mask = (x >= min_val) & (x <= max_val)
                y = np.zeros_like(x)
                y[mask] = 1 / (max_val - min_val)
                self.ax.fill_between(x, y, where=mask, alpha=0.3, color=self.vertex_color)
                self.ax.plot(x, y, self.vertex_color, linewidth=1.5)
                
            elif dist_type == "Normal":
                mu = dist_params["mu"]
                sigma = dist_params["sigma"]
                if sigma <= 0:
                    raise ValueError("sigma должен быть > 0")
                x = np.linspace(0, 1, 400)
                a, b = (0 - mu) / sigma, (1 - mu) / sigma
                y = truncnorm.pdf(x, a, b, loc=mu, scale=sigma)
                self.ax.fill_between(x, y, alpha=0.3, color=self.vertex_color)
                self.ax.plot(x, y, self.vertex_color, linewidth=1.5)
                
            elif dist_type == "Lognormal":
                gamma = float(dist_params["gamma"])
                mu = float(dist_params["mu"])
                sigma = float(dist_params["sigma"])
                if sigma < 0.01:
                    raise ValueError("σ должен быть > 0")
                x_min = max(gamma + 1e-10, 0.0)
                x_max = 1.0
                if x_max - x_min < 0.01:
                    x_min = max(gamma - 0.05, 0.0)
                x = np.linspace(x_min, x_max, 500)
                y = np.zeros_like(x)
                mask = x > gamma
                if np.any(mask):
                    x_valid = x[mask]
                    x_minus_gamma = np.maximum(x_valid - gamma, 1e-10)
                    log_term = np.log(x_minus_gamma)
                    z = (log_term - mu) / sigma
                    y_valid = np.exp(-0.5 * z**2) / (x_minus_gamma * sigma * np.sqrt(2 * np.pi))
                    y_valid = np.nan_to_num(y_valid, nan=0.0, posinf=0.0, neginf=0.0)
                    y[mask] = y_valid
                # Нормализация
                if np.trapezoid(y, x) > 0:
                    y = y / np.trapezoid(y, x)
                self.ax.fill_between(x, y, where=(x >= 0) & (x <= 1), alpha=0.3, color=self.vertex_color)
                self.ax.plot(x, y, self.vertex_color, linewidth=1.5)
                
            elif dist_type == "Stepwise":
                stages = dist_params.get("stages", [])
                if not stages:
                    raise ValueError("Не заданы ступени")
                x = np.linspace(0, 1, 400)
                self.ax.set_xlim(0, 1)
                total_count = sum(max(0.0, stage["weight"]) for stage in stages)
                if total_count <= 0:
                    total_count = 1.0
                max_height = 0
                for i, stage in enumerate(stages):
                    left = max(0.0, min(1.0, stage["left"]))
                    right = max(0.0, min(1.0, stage["right"]))
                    if right <= left:
                        right = min(1.0, left + 0.1)
                    count = max(0.0, stage["weight"])
                    height = (count / total_count) * 8.0
                    max_height = max(max_height, height)
                    color = self._get_stepwise_color(i / max(len(stages) - 1, 1))
                    self.ax.bar(left, height, width=right - left, align='edge', color=color, edgecolor=self.vertex_color, alpha=0.7, linewidth=1)
                    self.ax.axvline(x=left, color=self.vertex_color, linestyle='--', alpha=0.5, linewidth=0.8)
                    if i == len(stages) - 1:
                        self.ax.axvline(x=right, color=self.vertex_color, linestyle='--', alpha=0.5, linewidth=0.8)
                
                self.ax.set_ylim(0, max_height * 1.3)
                
            else:
                return
            
            # Общие настройки осей для непрерывных распределений
            if dist_type != "Stepwise":
                if 'y' in locals() and len(y) > 0 and np.max(y) > 0:
                    y_max = np.max(y) * 1.2
                    self.ax.set_ylim(0, max(y_max, 0.5))
                else:
                    self.ax.set_ylim(0, 5)
            
            self.ax.set_xlim(0, 1)
            self.ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
            self.ax.set_yticks([])
            self.ax.tick_params(axis='both', which='major', labelsize=7)
            
        except Exception as e:
            print(f"Ошибка при построении графика вершин: {e}")
            # Очищаем график при ошибке
            self.ax.clear()
            self.ax.set_title("Ошибка", fontsize=8, pad=2, color='red')

        self._apply_theme_to_plot()
        self.canvas.draw()
    
    def _get_stepwise_color(self, intensity):
        """Генерация градиентного цвета для ступеней"""
        intensity = max(0.0, min(1.0, intensity))
        idx = int(intensity * (len(self.stepwise_colors) - 1))
        return self.stepwise_colors[idx]
    
    def pack(self, **kwargs):
        """Упаковка виджета"""
        self.frame.pack(**kwargs)
        
    def place(self, **kwargs):
        """Размещение виджета"""
        self.frame.place(**kwargs)


# In[12]:


class WidgetFactory:
    """Класс кастомных виджетов"""
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.colors = theme_manager.colors

    def create_frame(self, parent, **kwargs):
        """Создает темизированный фрейм"""
        defaults = {'bg': self.colors['frame_bg'], 'highlightbackground': self.colors['border_color'],
                    'highlightthickness': 0, 'highlightcolor': self.colors['border_color']}
        defaults.update(kwargs)
        return tk.Frame(parent, **defaults)
    
    def create_label_frame(self, parent, text, **kwargs):
        """Создает стилизованный LabelFrame с ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TLabelframe', background=self.colors['frame_bg'], foreground=self.colors['accent_color'], 
                        bordercolor=self.colors['border_color'], relief='solid', borderwidth=1)
        style.configure('Custom.TLabelframe.Label', background=self.colors['frame_bg'], foreground=self.colors['accent_color'], 
                        font=("Segoe UI", 10, "bold"))
        defaults = {'text': text, 'style': 'Custom.TLabelframe', 'labelanchor': 'nw', 'padding': (10, 5)}
        defaults.update(kwargs)
        return ttk.LabelFrame(parent, **defaults)
    
    def create_label(self, parent, text="", **kwargs):
        """Универсальный метод для всех меток"""
        defaults = {'text': text, 'bg': self.colors['frame_bg'], 'fg': self.colors['text_color']}
        defaults.update(kwargs)
        return tk.Label(parent, **defaults)
    
    def create_label_h1(self, parent, text, **kwargs):
        """Заголовок h1"""
        kwargs.update({'font': ("Segoe UI", 14, "bold"), 'anchor': 'w'})
        return self.create_label(parent, text, **kwargs)
    
    def create_label_h2(self, parent, text, **kwargs):
        """Заголовок h2"""
        kwargs.update({'font': ("Segoe UI", 10, "bold"), 'fg': self.colors['accent_color'], 'anchor': 'w'})
        return self.create_label(parent, text, **kwargs)
    
    def create_label_normal(self, parent, text, **kwargs):
        """Обычная метка"""
        kwargs.update({'font': ("Segoe UI", 10), 'anchor': 'w'})
        return self.create_label(parent, text, **kwargs)
    
    def create_label_small(self, parent, text, **kwargs):
        """Мелкая метка"""
        kwargs.update({'font': ("Segoe UI", 9), 'anchor': 'w'})
        return self.create_label(parent, text, **kwargs)
    
    def create_label_small_bold(self, parent, text=None, textvariable=None, **kwargs):
        """Жирная мелкая метка"""
        defaults = {'font': ("Segoe UI", 9, "bold"), 'bg': self.colors['frame_bg'],'fg': self.colors['text_color'], 'anchor': 'w'}
        if text is not None:
            defaults['text'] = text
        if textvariable is not None:
            defaults['textvariable'] = textvariable
        defaults.update(kwargs)
        return tk.Label(parent, **defaults)
    
    def create_label_bold(self, parent, text="", **kwargs):
        """Жирная метка"""
        kwargs.update({'font': ("Segoe UI", 10, "bold"), 'anchor': 'w'})
        return self.create_label(parent, text, **kwargs)
    
    def create_label_tiny(self, parent, text, **kwargs):
        """Очень мелкая метка"""
        kwargs.update({'font': ("Segoe UI", 8), 'anchor': 'w'})
        return self.create_label(parent, text, **kwargs)
    
    def create_button(self, parent, text, command, button_type="primary", **kwargs):
        """Кнопка с поддержкой тем"""
        defaults = {'font': ("Segoe UI", 10), 'bd': 0, 'cursor': "hand2", 'command': command}
        
        type_configs = {
            "primary": {
                'font': ("Segoe UI", 10, "bold"),
                'bg': self.colors['btn_color'],
                'fg': self.colors['btn_text'],
                'activebackground': self.colors['btn_hover'],
                'activeforeground': self.colors['btn_text'],
                'padx': 20,
                'pady': 8
            },
            "fire": {
                'font': ("Segoe UI", 12, "bold"),
                'bg': self.colors['fire_start'],
                'fg': '#ffffff',
                'activebackground': self.colors['fire_hover'],
                'activeforeground': '#ffffff',
                'padx': 10,
                'pady': 1
            },
            "reset": {
                'font': ("Segoe UI", 12, "bold"),
                'bg': self.colors['reset_color'],
                'fg': '#ffffff', 
                'activebackground': self.colors['reset_hover'],
                'activeforeground': '#ffffff',
                'padx': 10,
                'pady': 1
            },
            "new_graph": {
                'font': ("Segoe UI", 12, "bold"),
                'bg': self.colors['new_graph_color'],
                'fg': '#ffffff',
                'activebackground': self.colors['new_graph_hover'],
                'activeforeground': '#ffffff',
                'padx': 10,
                'pady': 1
            },
            "small": {
                'font': ("Segoe UI", 8),
                'bg': self.colors['btn_color'],
                'fg': self.colors['btn_text'],
                'activebackground': self.colors['btn_hover'],
                'activeforeground': self.colors['btn_text'],
                'padx': 8,
                'pady': 2
            }
        }
        
        if button_type in type_configs:
            defaults.update(type_configs[button_type])
        defaults['text'] = text
        defaults.update(kwargs)
        btn = tk.Button(parent, **defaults)
        
        if 'activebackground' in defaults:
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=defaults['activebackground']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=defaults['bg']))
        return btn
    
    def create_primary_button(self, parent, text, command, **kwargs):
        return self.create_button(parent, text, command, button_type="primary", **kwargs)
    
    def create_small_button(self, parent, text, command, **kwargs):
        return self.create_button(parent, text, command, button_type="small", **kwargs)
    
    def create_fire_button(self, parent, text, command, **kwargs):
        return self.create_button(parent, text, command, button_type="fire", **kwargs)
    
    def create_reset_button(self, parent, text, command, **kwargs):
        return self.create_button(parent, text, command, button_type="reset", **kwargs)
    
    def create_new_graph_button(self, parent, text, command, **kwargs):
        return self.create_button(parent, text, command, button_type="new_graph", **kwargs)
    
    def create_entry(self, parent, width=6, font=("Segoe UI", 9), justify="center", **kwargs):
        defaults = {'width': width, 'font': font, 'justify': justify, 'bg': self.colors['input_bg'], 
                    'bd': 1, 'fg': self.colors['input_fg'], 'insertbackground': self.colors['input_cursor']}
        defaults.update(kwargs)
        return tk.Entry(parent, **defaults)
    
    def create_slider(self, parent, **kwargs):
        defaults = {'orient': "horizontal", 'font': ("Segoe UI", 8), 'showvalue': 0, 'bg': self.colors['slider_thumb'], 
                    'activebackground': self.colors['slider_thumb_active'], 'troughcolor': self.colors['slider_trough'],
                    'highlightbackground': self.colors['slider_frame']}
        defaults.update(kwargs)
        return tk.Scale(parent, **defaults)
    
    def create_spinbox(self, parent, **kwargs):
        defaults = {'font': ("Segoe UI", 9), 'bg': self.colors['spinbox_bg'], 'fg': self.colors['spinbox_fg'],
                    'buttonbackground': self.colors['spinbox_button'], 'bd': 1, 'relief': 'solid', 'justify': 'center'}
        defaults.update(kwargs)
        return tk.Spinbox(parent, **defaults)
    
    def create_scrollbar(self, parent, orient="vertical", command=None, **kwargs):
        """Полоса прокрутки с поддержкой тем"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Custom.Vertical.TScrollbar",
            background=self.colors['scrollbar_slider'],
            troughcolor=self.colors['scrollbar_trough'],
            arrowcolor=self.colors['scrollbar_arrow'],
            bordercolor=self.colors['border_color'],
            lightcolor=self.colors['scrollbar_slider'],
            darkcolor=self.colors['scrollbar_slider'],
        )
        style.map("Custom.Vertical.TScrollbar",
            background=[('pressed', self.colors['scrollbar_slider']),
                       ('active', self.colors['scrollbar_slider']),
                       ('!active', self.colors['scrollbar_slider'])],
            arrowcolor=[('pressed', self.colors['scrollbar_arrow']),
                       ('active', self.colors['scrollbar_arrow']),
                       ('!active', self.colors['scrollbar_arrow'])]
        )

        style.configure("Custom.Horizontal.TScrollbar",
            background=self.colors['scrollbar_slider'],
            troughcolor=self.colors['scrollbar_trough'],
            arrowcolor=self.colors['scrollbar_arrow'],
            bordercolor=self.colors['border_color'],
            lightcolor=self.colors['scrollbar_slider'],
            darkcolor=self.colors['scrollbar_slider'],
            relief="flat"
        )
        style.map("Custom.Horizontal.TScrollbar",
            background=[('pressed', self.colors['scrollbar_slider']),
                       ('active', self.colors['scrollbar_slider']),
                       ('!active', self.colors['scrollbar_slider'])],
            arrowcolor=[('pressed', self.colors['scrollbar_arrow']),
                       ('active', self.colors['scrollbar_arrow']),
                       ('!active', self.colors['scrollbar_arrow'])]
        )
        
        style_name = f"Custom.{orient.capitalize()}.TScrollbar"
        return ttk.Scrollbar(parent, orient=orient, command=command, style=style_name)
    
    def create_canvas(self, parent, **kwargs):
        defaults = {'bg': self.colors['frame_bg'], 'highlightthickness': 0}
        defaults.update(kwargs)
        return tk.Canvas(parent, **defaults)
    
    def create_combobox(self, parent, values, variable, **kwargs):
        """Кастомный комбобокс"""
        width = kwargs.get('width', 20)
        font = kwargs.get('font', ("Segoe UI", 10))
        arrow_color = self.colors['text_secondary']
        frame = tk.Frame(parent, bg=self.colors['input_bg'])
        entry_frame = tk.Frame(frame, bg=self.colors['input_bg'], highlightbackground=self.colors['border_color'],
                               highlightthickness=1, highlightcolor=self.colors['border_color'])
        entry_frame.pack(side='left', fill='both', expand=True)
        
        entry = tk.Entry(entry_frame, bg=self.colors['input_bg'], fg=self.colors['input_fg'], font=font, bd=0,
                         relief='flat', state='readonly', cursor='arrow', justify='left', readonlybackground=self.colors['input_bg'],
                         insertwidth=0, highlightthickness=0, width=width)
        entry.pack(side='left', fill='both', expand=True, padx=(5, 0))
        arrow_label = tk.Label(entry_frame, text='▼', bg=self.colors['input_bg'], fg=arrow_color, font=("Arial", 8), cursor='arrow', padx=5)
        arrow_label.pack(side='right')
        
        def update_entry_text(*args):
            try:
                current_val = variable.get()
                entry.config(state='normal')
                entry.delete(0, tk.END)
                entry.insert(0, current_val)
                entry.config(state='readonly')
            except:
                pass
        
        variable.trace_add('write', update_entry_text)
        update_entry_text()
        
        frame.entry = entry
        frame.entry_frame = entry_frame
        frame.arrow_label = arrow_label
        frame.values = values
        frame.var = variable
        frame.width = width
        frame.font = font
        frame.arrow_color = arrow_color
        frame.dropdown_data = {'is_visible': False, 'dropdown': None, 'listbox': None, 'close_handler_id': None}
        
        def open_dropdown(e):
            self._toggle_combobox_dropdown(frame, values, variable, entry)
        
        entry.bind('<Button-1>', open_dropdown)
        arrow_label.bind('<Button-1>', open_dropdown)
        entry_frame.bind('<Button-1>', open_dropdown)
        
        return frame
    
    def _toggle_combobox_dropdown(self, frame, values, variable, entry):
        dropdown_data = frame.dropdown_data
        if dropdown_data['is_visible']:
            self._close_combobox_dropdown(frame)
            return
        self._open_combobox_dropdown(frame, values, variable)
    
    def _open_combobox_dropdown(self, frame, values, variable):
        dropdown_data = frame.dropdown_data
        frame.update_idletasks()
        entry_width = frame.winfo_width()
        listbox_width = entry_width
        ITEM_HEIGHT = 20 # Высота одной строки записи
        listbox_height = len(values) * ITEM_HEIGHT # Высота выпадающего списка
        
        screen_height = frame.winfo_screenheight()
        max_height = screen_height - frame.winfo_rooty() - 100
        if listbox_height > max_height:
            listbox_height = max_height
        
        dropdown = tk.Toplevel(frame)
        dropdown.wm_overrideredirect(True)
        dropdown.configure(bg=self.colors['input_bg'])
        
        border_color = self.colors['border_color']
        dropdown_frame = tk.Frame(dropdown, bg=border_color, padx=1, pady=1)
        dropdown_frame.pack(fill='both', expand=True)
        
        x = frame.winfo_rootx()
        y = frame.winfo_rooty() + frame.winfo_height()
        dropdown.geometry(f"{listbox_width}x{listbox_height}+{x}+{y}")
        dropdown.attributes('-topmost', True)
        
        visible_items = min(len(values), int(listbox_height / ITEM_HEIGHT))
        
        listbox = tk.Listbox(dropdown_frame, bg=self.colors['input_bg'], fg=self.colors['input_fg'],
                             selectbackground=self.colors['slider_thumb_active'], selectforeground=self.colors['btn_text'],
                             borderwidth=0, highlightthickness=0, font=frame.font, activestyle='none', exportselection=False, height=visible_items)
        
        for value in values:
            listbox.insert('end', f"  {value}")
        
        if visible_items < len(values):
            scrollbar = tk.Scrollbar(dropdown_frame)
            scrollbar.pack(side='right', fill='y')
            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)
            listbox.pack(side='left', fill='both', expand=True)
        else:
            listbox.pack(fill='both', expand=True)
        
        def on_select(event):
            if listbox.curselection():
                idx = listbox.curselection()[0]
                selected_value = values[idx]
                variable.set(selected_value)
                self._close_combobox_dropdown(frame)
        listbox.bind('<<ListboxSelect>>', on_select)
        listbox.bind('<Double-Button-1>', on_select)
        
        def on_focus_out(event):
            if dropdown and dropdown.winfo_exists():
                dropdown.after(10, lambda: self._check_and_close_dropdown(frame, dropdown))
        dropdown.bind('<FocusOut>', on_focus_out)
        
        def on_escape(event):
            self._close_combobox_dropdown(frame)
            return "break"
        
        dropdown.bind('<Escape>', on_escape)
        listbox.bind('<Escape>', on_escape)
        
        current_value = variable.get()
        if current_value in values:
            idx = values.index(current_value)
            listbox.selection_set(idx)
            listbox.see(idx)
        dropdown_data.update({ 'is_visible': True, 'dropdown': dropdown, 'listbox': listbox})
        dropdown.listbox = listbox
        listbox.focus_set()
        
        def setup_close_handler():
            def close_on_window_click(event):
                if not dropdown_data['is_visible'] or not dropdown_data['dropdown']:
                    return
                dropdown = dropdown_data['dropdown']
                if not dropdown.winfo_exists():
                    return
                dropdown_x = dropdown.winfo_rootx()
                dropdown_y = dropdown.winfo_rooty()
                dropdown_width = dropdown.winfo_width()
                dropdown_height = dropdown.winfo_height()
                entry_x = frame.winfo_rootx()
                entry_y = frame.winfo_rooty()
                entry_width = frame.winfo_width()
                entry_height = frame.winfo_height()
                click_x = event.x_root
                click_y = event.y_root
                
                in_dropdown = dropdown_x <= click_x <= dropdown_x + dropdown_width and dropdown_y <= click_y <= dropdown_y + dropdown_height
                in_entry = entry_x <= click_x <= entry_x + entry_width and entry_y <= click_y <= entry_y + entry_height
                if not in_dropdown and not in_entry:
                    self._close_combobox_dropdown(frame)
            
            if dropdown_data['close_handler_id']:
                try:
                    frame.winfo_toplevel().unbind('<Button-1>', dropdown_data['close_handler_id'])
                except:
                    pass
            handler_id = frame.winfo_toplevel().bind('<Button-1>', close_on_window_click, add='+')
            dropdown_data['close_handler_id'] = handler_id
        dropdown.after(10, setup_close_handler)
    
    def _close_combobox_dropdown(self, frame):
        dropdown_data = frame.dropdown_data
        if dropdown_data['close_handler_id']:
            try:
                frame.winfo_toplevel().unbind('<Button-1>', dropdown_data['close_handler_id'])
            except:
                pass
        if dropdown_data['dropdown'] and dropdown_data['dropdown'].winfo_exists():
            dropdown_data['dropdown'].destroy()
        dropdown_data.update({'is_visible': False, 'dropdown': None, 'listbox': None, 'close_handler_id': None})
    
    def _check_and_close_dropdown(self, frame, dropdown):
        if dropdown and dropdown.winfo_exists():
            focused_widget = dropdown.focus_get()
            dropdown_widgets = [dropdown]
            for child in dropdown.winfo_children():
                dropdown_widgets.append(child)
                if hasattr(child, 'winfo_children'):
                    for grandchild in child.winfo_children():
                        dropdown_widgets.append(grandchild)
            focus_in_dropdown = False
            for widget in dropdown_widgets:
                if focused_widget == widget:
                    focus_in_dropdown = True
                    break
                if focused_widget:
                    parent = focused_widget.winfo_parent()
                    while parent:
                        if parent == widget.winfo_pathname(widget.winfo_id()):
                            focus_in_dropdown = True
                            break
                        try:
                            parent_widget = dropdown.nametowidget(parent)
                            parent = parent_widget.winfo_parent()
                        except:
                            break
            if not focus_in_dropdown:
                self._close_combobox_dropdown(frame)
    
    def create_parameter_row(self, parent, label_text, var, from_val, to_val, entry_width=6, slider_length=180, resolution=0.01,
                            row=0, label_col=0, entry_col=1, slider_col=2, padx_label=(0, 5), padx_entry=(0, 15), pady=(0, 5),
                            combobox_var=None, combobox_values=None, coeff_var=None, coeff_label_col=None, coeff_entry_col=None, 
                            coeff_slider_col=None, translator=None, combobox_width=25):
        t = translator.t if translator else lambda key, *args: key
        widgets_dict = {}
        label = self.create_label_normal(parent, text=f"{label_text}:")
        label.grid(row=row, column=label_col, sticky="w", padx=padx_label, pady=pady)
        widgets_dict["label"] = label
        
        if combobox_var is not None and combobox_values is not None:
            combobox_frame = self.create_combobox(parent, combobox_values, combobox_var, width=combobox_width)
            combobox_frame.grid(row=row, column=entry_col, sticky="w", padx=padx_entry, pady=pady)
            widgets_dict["combobox"] = combobox_frame
            
            if coeff_var is not None:
                coeff_label = self.create_label_small(parent, text=f"{t('coeff')}:")
                coeff_label_col_pos = coeff_label_col if coeff_label_col is not None else slider_col
                coeff_label.grid(row=row, column=coeff_label_col_pos, sticky="w", padx=(20, 5), pady=pady)
                widgets_dict["coeff_label"] = coeff_label
                
                coeff_entry = self.create_entry(parent, width=6, font=("Segoe UI", 9))
                coeff_entry_col_pos = coeff_entry_col if coeff_entry_col is not None else coeff_label_col_pos + 1
                coeff_entry.grid(row=row, column=coeff_entry_col_pos, sticky="w", padx=(0, 10), pady=pady)
                coeff_entry.insert(0, str(round(coeff_var.get(), 2)))
                widgets_dict["coeff_entry"] = coeff_entry
                
                coeff_slider = self.create_slider(parent, from_=from_val, to=to_val, length=slider_length,resolution=resolution, variable=coeff_var)
                coeff_slider_col_pos = coeff_slider_col if coeff_slider_col is not None else coeff_entry_col_pos + 1
                coeff_slider.grid(row=row, column=coeff_slider_col_pos, sticky="w", padx=(0, 0), pady=pady)
                widgets_dict["coeff_slider"] = coeff_slider
                
                def update_coeff_from_entry(event=None):
                    try:
                        value = float(coeff_entry.get())
                        value = max(from_val, min(to_val, value))
                        coeff_var.set(round(value, 2))
                    except ValueError:
                        coeff_entry.delete(0, tk.END)
                        coeff_entry.insert(0, str(round(coeff_var.get(), 2)))
                
                coeff_entry.bind('<Return>', update_coeff_from_entry)
                coeff_entry.bind('<FocusOut>', update_coeff_from_entry)
                
                def update_coeff_entry(*args):
                    if coeff_entry and coeff_entry.winfo_exists():
                        coeff_entry.delete(0, tk.END)
                        coeff_entry.insert(0, str(round(coeff_var.get(), 2)))
                
                coeff_var.trace_add("write", update_coeff_entry)
            
            return widgets_dict
        
        else:
            entry = self.create_entry(parent, width=entry_width, font=("Segoe UI", 9))
            entry.grid(row=row, column=entry_col, sticky="w", padx=padx_entry, pady=pady)
            entry.insert(0, str(round(var.get(), 2)))
            widgets_dict["entry"] = entry
            slider = self.create_slider(parent, from_=from_val, to=to_val, resolution=resolution, variable=var, length=slider_length)
            slider.grid(row=row, column=slider_col, sticky="w", padx=(0, 0), pady=pady)
            widgets_dict["slider"] = slider
            
            def update_from_entry(event=None):
                try:
                    value = float(entry.get())
                    value = max(from_val, min(to_val, value))
                    var.set(round(value, 2))
                except ValueError:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(round(var.get(), 2)))
            
            entry.bind('<Return>', update_from_entry)
            entry.bind('<FocusOut>', update_from_entry)
            
            def update_entry(*args):
                if entry and entry.winfo_exists():
                    entry.delete(0, tk.END)
                    entry.insert(0, str(round(var.get(), 2)))
            
            var.trace_add("write", update_entry)
            
            return widgets_dict
    
    def create_tier_stage_row(self, parent, idx, label_text, left_var, right_var, weight_var, is_edge_tier=False,
                              on_plot_update_callback=None, translator=None):
        t = translator.t if translator else lambda key, *args: key
        stage_frame = self.create_frame(parent)
        stage_frame.pack(fill="x", pady=(0, 10), padx=5)
        self.create_label_small_bold(stage_frame, text=f"{label_text} {idx+1}:").pack(anchor="w", pady=(5, 10))
        params_frame = self.create_frame(stage_frame)
        params_frame.pack(anchor="w", pady=(0, 10), padx=5)
        if is_edge_tier:
            left_min, left_max = -1.0, 0.99
            right_min, right_max = -0.99, 1.0
        else:
            left_min, left_max = 0.0, 0.99
            right_min, right_max = 0.01, 1.0
        left_widgets = self.create_parameter_row(params_frame, t('left_bound'), left_var, from_val=left_min, to_val=left_max, 
                                                 resolution=0.01, row=0, translator=translator)
        right_widgets = self.create_parameter_row(params_frame, t('right_bound'), right_var, from_val=right_min, to_val=right_max, 
                                                  resolution=0.01, row=1, translator=translator)
        
        if is_edge_tier:
            weight_text = t('edges_count_stage')
        else:
            weight_text = t('vertex_count_stage')
        
        weight_label = self.create_label_small(params_frame, text=f"{weight_text}:")
        weight_label.grid(row=2, column=0, sticky="w", padx=(0, 5), pady=(8, 0))
        
        weight_slider = self.create_slider(params_frame, from_=1, to=100, resolution=1, variable=weight_var, length=180)
        weight_slider.grid(row=2, column=2, sticky="w", padx=(0, 0), pady=(8, 0))
        
        if is_edge_tier:
            min_range, max_range = -1.0, 1.0
        else:
            min_range, max_range = 0.0, 1.0
        
        self.create_synchronized_sliders(left_widgets["slider"], right_widgets["slider"], left_var, right_var, 
                                         min_range=min_range, max_range=max_range, min_gap=0.01)
        
        trace_ids = []
        if on_plot_update_callback:
            for var in [left_var, right_var, weight_var]:
                trace_id = var.trace_add("write", lambda *args, idx=idx: on_plot_update_callback(idx))
                trace_ids.append((var, trace_id))
        
        return {
            'stage_frame': stage_frame,
            'left_entry': left_widgets["entry"],
            'left_slider': left_widgets["slider"],
            'right_entry': right_widgets["entry"],
            'right_slider': right_widgets["slider"],
            'weight_slider': weight_slider,
            'trace_ids': trace_ids
        }
    
    def create_synchronized_sliders(self, left_slider, right_slider, left_var, right_var, min_range=-1.0, max_range=1.0, min_gap=0.01):
        def on_left_slider_change(val):
            try:
                left_val = float(val)
                right_val = right_var.get()
                
                if left_val >= right_val - min_gap:
                    new_right = left_val + min_gap
                    if new_right <= max_range:
                        right_var.set(round(new_right, 2))
            except Exception:
                pass
        
        def on_right_slider_change(val):
            try:
                right_val = float(val)
                left_val = left_var.get()
                if right_val <= left_val + min_gap:
                    new_left = right_val - min_gap
                    if new_left >= min_range:
                        left_var.set(round(new_left, 2))
            except Exception:
                pass
                
        left_slider.config(command=on_left_slider_change)
        right_slider.config(command=on_right_slider_change)


# In[13]:


class GraphLegendWidget:
    """Класс отображения легенды и гистограм справа от графа"""
    def __init__(self, parent, theme_manager, translator, colors, widget_factory):
        self.parent = parent
        self.theme_manager = theme_manager
        self.translator = translator
        self.t = translator.t
        self.colors = colors
        self.widget_factory = widget_factory
        self.frame = self.widget_factory.create_frame(self.parent)
        
        self.edge_hist_fig = None
        self.edge_hist_ax = None
        self.edge_hist_canvas = None
        self.edge_bins_var = tk.IntVar(value=10)
        self.vertex_hist_fig = None
        self.vertex_hist_ax = None
        self.vertex_hist_canvas = None
        self.vertex_bins_var = tk.IntVar(value=10)
        self.current_graph = None
    
    def create_legend(self):
        """Легенда для графа"""
        legend_container = self.widget_factory.create_frame(self.frame)
        legend_container.pack(fill="x", padx=(5, 15), pady=(5, 25))
        
        if self.theme_manager.theme == 'dark':
            RED_START = 0.9
            YELLOW_END = 0.1
        else:
            RED_START = 1.0
            YELLOW_END = 0.1
    
        first_burned_color_rgba = plt.cm.YlOrRd(RED_START)
        last_burned_color_rgba = plt.cm.YlOrRd(YELLOW_END)
        
        def rgba_to_hex(rgba):
            r, g, b, _ = rgba
            return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        
        first_burned_color_hex = rgba_to_hex(first_burned_color_rgba)
        last_burned_color_hex = rgba_to_hex(last_burned_color_rgba)
        
        border_color = self.colors['graph_vertex_border']
        edge_neg1_color = self.colors['graph_edge_negative']
        edge_pos1_color = self.colors['graph_edge_positive']
        vertex_small_color = self.colors['graph_legend_small']
        vertex_large_color = self.colors['graph_legend_large']
        not_burned_color = self.colors['graph_legend_not_burned']
        
        legend_items = [
            (self.t('small_vertex'), vertex_small_color, "small", 1.0, border_color),
            (self.t('large_vertex'), vertex_large_color, "large", 1.0, border_color),
            (self.t('edge_neg1'), edge_neg1_color, "edge", 1.0, border_color),
            (self.t('edge_pos1'), edge_pos1_color, "edge", 1.0, border_color),
            (self.t('not_burned'), not_burned_color, "circle", 0.8, border_color),
            (self.t('first_burned'), first_burned_color_hex, "circle", 1.0, border_color),
            (self.t('last_burned'), last_burned_color_hex, "circle", 1.0, border_color)
        ]
        
        for text, color, item_type, alpha, border_color in legend_items:
            item_frame = self.widget_factory.create_frame(legend_container)
            item_frame.pack(fill="x", pady=1)
            canvas = tk.Canvas(item_frame, width=25, height=20, bg=self.colors['frame_bg'], highlightthickness=0)
            canvas.pack(side="left", padx=(0, 8))
            if alpha < 1.0 and color.startswith('#'):
                bg_r = int(self.colors['frame_bg'][1:3], 16)
                bg_g = int(self.colors['frame_bg'][3:5], 16)
                bg_b = int(self.colors['frame_bg'][5:7], 16)
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                r = int(r * alpha + bg_r * (1 - alpha))
                g = int(g * alpha + bg_g * (1 - alpha))
                b = int(b * alpha + bg_b * (1 - alpha))
                color = f'#{r:02x}{g:02x}{b:02x}'
            
            if item_type == "small":
                canvas.create_oval(3, 3, 10, 10, fill=color, outline=border_color, width=1)
            elif item_type == "large":
                canvas.create_oval(1, 1, 19, 19, fill=color, outline=border_color, width=1)
            elif item_type == "edge":
                canvas.create_rectangle(3, 7, 22, 12, fill=color, outline=border_color, width=1)
            elif item_type == "circle":
                canvas.create_oval(3, 3, 17, 17, fill=color, outline=border_color, width=1)
            
            text_label = self.widget_factory.create_label_tiny(item_frame, text=text)
            text_label.pack(side="left", fill="x", expand=True)
    
    def create_histogram_panel(self, data_type='edge'):
        """Панель с гистограммой и управлением количеством бинов"""
        panel_frame = self.widget_factory.create_frame(self.frame)
        panel_frame.pack(fill="x", pady=(0, 10))
        
        if data_type == 'edge':
            title = self.t('actual_edge_distribution')
            bins_var = self.edge_bins_var
        else:
            title = self.t('actual_vertex_distribution')
            bins_var = self.vertex_bins_var
        
        title_label = self.widget_factory.create_label_small_bold(panel_frame, text=f"{title}:")
        title_label.pack(anchor="w", pady=(0, 2))
        
        hist_container = self.widget_factory.create_frame(panel_frame)
        hist_container.pack(fill="x", pady=(0, 2))
        
        hist_frame = self.widget_factory.create_frame(hist_container, width=200, height=100)
        hist_frame.pack(fill="x")
        hist_frame.pack_propagate(False)
        
        fig = Figure(figsize=(2.0, 1.0), dpi=80, facecolor=self.colors['frame_bg'])
        ax = fig.add_subplot(111)
        
        ax.set_facecolor(self.colors['plot_bg'])
        ax.tick_params(axis='both', colors=self.colors['plot_text'], labelsize=6)
        ax.spines['bottom'].set_color(self.colors['border_color'])
        ax.spines['top'].set_color(self.colors['border_color'])
        ax.spines['left'].set_color(self.colors['border_color'])
        ax.spines['right'].set_color(self.colors['border_color'])
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        if data_type == 'edge':
            ax.set_xlim(-1.0, 1.0)
        else:
            ax.set_xlim(0.0, 1.0)

        canvas = FigureCanvasTkAgg(fig, master=hist_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=2, pady=2)
        
        if data_type == 'edge':
            self.edge_hist_fig = fig
            self.edge_hist_ax = ax
            self.edge_hist_canvas = canvas
        else:
            self.vertex_hist_fig = fig
            self.vertex_hist_ax = ax
            self.vertex_hist_canvas = canvas
        
        controls_frame = self.widget_factory.create_frame(panel_frame)
        controls_frame.pack(fill="x", pady=(2, 0))
        
        bins_label = self.widget_factory.create_label_tiny(controls_frame, text=f"{self.t('num_bins')}:")
        bins_label.pack(side="left", padx=(0, 5))
        
        bins_spinbox = self.widget_factory.create_spinbox(controls_frame, from_=5, to=20, width=4,
                                                          textvariable=bins_var, font=("Segoe UI", 7), justify="center")
        bins_spinbox.pack(side="left")
        
        if data_type == 'edge':
            self.edge_bins_spinbox = bins_spinbox
        else:
            self.vertex_bins_spinbox = bins_spinbox
    
    def set_histogram_update_callback(self, data_type, callback):
        """Устанавливает функцию обратного вызова для обновления гистограммы"""
        def update_wrapper(*args):
            if self.current_graph is not None:
                callback(data_type, self.current_graph)
                
        if data_type == 'edge':
            self.edge_bins_var.trace_add("write", update_wrapper)
            if hasattr(self, 'edge_bins_spinbox'):
                self.edge_bins_spinbox.bind('<Return>', lambda e: callback(data_type, self.current_graph))
                self.edge_bins_spinbox.bind('<FocusOut>', lambda e: callback(data_type, self.current_graph))
        else:
            self.vertex_bins_var.trace_add("write", update_wrapper)
            if hasattr(self, 'vertex_bins_spinbox'):
                self.vertex_bins_spinbox.bind('<Return>', lambda e: callback(data_type, self.current_graph))
                self.vertex_bins_spinbox.bind('<FocusOut>', lambda e: callback(data_type, self.current_graph))
    
    def set_current_graph(self, graph):
        """Сохраняет текущий граф для обновления гистограмм"""
        self.current_graph = graph
    
    def update_histogram(self, data_type, graph):
        """Обновляет гистограмму для указанного типа данных"""
        if graph is None:
            return
        try:
            if data_type == 'edge':
                if not hasattr(self, 'edge_hist_ax') or self.edge_hist_ax is None:
                    return
                edge_weights = []
                for u, v, data in graph.edges(data=True):
                    weight = data['weight']
                    edge_weights.append(weight)
                if not edge_weights:
                    return
                bins = self.edge_bins_var.get()
                bins = max(5, min(20, bins))
                self.edge_hist_ax.clear()
                self.edge_hist_ax.set_facecolor(self.colors['plot_bg'])
                self.edge_hist_ax.tick_params(axis='both', colors=self.colors['plot_text'], labelsize=6)
                self.edge_hist_ax.spines['bottom'].set_color(self.colors['border_color'])
                self.edge_hist_ax.spines['top'].set_color(self.colors['border_color'])
                self.edge_hist_ax.spines['left'].set_color(self.colors['border_color'])
                self.edge_hist_ax.spines['right'].set_color(self.colors['border_color'])
                self.edge_hist_ax.set_xlim(-1.0, 1.0)
                hist_color = self.colors['density_color']
                border_color = self.colors['border_color']
                self.edge_hist_ax.hist(edge_weights, bins=bins, color=hist_color, 
                                      edgecolor=border_color, linewidth=0.5, alpha=0.8)
                self.edge_hist_fig.tight_layout(pad=0.3)
                self.edge_hist_canvas.draw()
                
            elif data_type == 'vertex':
                if not hasattr(self, 'vertex_hist_ax') or self.vertex_hist_ax is None:
                    return
                vertex_weights = []
                for node in graph.nodes():
                    weight = graph.nodes[node]['weight']
                    vertex_weights.append(weight)
                if not vertex_weights:
                    return
                bins = self.vertex_bins_var.get()
                bins = max(5, min(20, bins))
                self.vertex_hist_ax.clear()
                self.vertex_hist_ax.set_facecolor(self.colors['plot_bg'])
                self.vertex_hist_ax.tick_params(axis='both', colors=self.colors['plot_text'], labelsize=6)
                self.vertex_hist_ax.spines['bottom'].set_color(self.colors['border_color'])
                self.vertex_hist_ax.spines['top'].set_color(self.colors['border_color'])
                self.vertex_hist_ax.spines['left'].set_color(self.colors['border_color'])
                self.vertex_hist_ax.spines['right'].set_color(self.colors['border_color'])
                self.vertex_hist_ax.set_xlim(0.0, 1.0)
                hist_color = self.colors['vertex_density_color']
                border_color = self.colors['border_color']
                self.vertex_hist_ax.hist(vertex_weights, bins=bins, color=hist_color, edgecolor=border_color, linewidth=0.5, alpha=0.8)
                self.vertex_hist_fig.tight_layout(pad=0.3)
                self.vertex_hist_canvas.draw()
        except Exception as e:
            print(f"Ошибка при обновлении гистограммы {data_type}: {e}")
    
    def create_full_panel(self):
        """Создает полную панель с легендой и обеими гистограммами"""
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.create_legend()
        self.create_histogram_panel(data_type='edge')
        self.create_histogram_panel(data_type='vertex')
        return self.frame
    
    def pack(self, **kwargs):
        """Упаковка виджета"""
        self.frame.pack(**kwargs)
        
    def place(self, **kwargs):
        """Размещение виджета"""
        self.frame.place(**kwargs)


# In[14]:


class HelpContentBuilder:
    """Построитель содержимого для вкладки справки"""
    def __init__(self, parent, theme_manager, translator, widget_factory):
        self.parent = parent
        self.theme_manager = theme_manager
        self.translator = translator
        self.t = translator.t
        self.widget_factory = widget_factory
        self.colors = theme_manager.colors
        
        # Ссылки на канвасы для прокрутки
        self.left_canvas = None
        self.right_canvas = None
        self.left_scrollbar = None
        self.right_scrollbar = None
        self.left_scrollable_frame = None
        self.right_scrollable_frame = None
    
    def build(self, parent_frame):
        """Строит полное содержимое вкладки справки"""
        # Очищаем родительский фрейм
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        # Создаем панель с двумя частями как на вкладке симуляции
        main_container = self.widget_factory.create_frame(parent_frame)
        main_container.pack(fill="both", expand=True, padx=5, pady=10)
        
        # Горизонтальный PanedWindow для разделения на левую и правую части
        main_paned = tk.PanedWindow(
            main_container, 
            orient=tk.HORIZONTAL,
            bg=self.theme_manager.get_color('bg_color'), 
            sashwidth=5
        )
        main_paned.pack(fill="both", expand=True)
        
        # Левая панель (пустая, с прокруткой)
        left_frame = self.widget_factory.create_frame(main_paned, width=300, bd=0, relief="flat")
        main_paned.add(left_frame, minsize=250, width=300)
        self._create_scrollable_panel(left_frame, is_left=True)
        
        # Правая панель (с содержимым, с прокруткой)
        right_frame = self.widget_factory.create_frame(main_paned, width=600, bd=0, relief="flat")
        main_paned.add(right_frame, minsize=400, width=600)
        self._create_scrollable_panel(right_frame, is_left=False)
        
        # Заполняем правую панель содержимым
        self._fill_right_panel(self.right_scrollable_frame)
        
        # Привязываем обработчик колесика мыши
        self._bind_mousewheel()
    
    def _create_scrollable_panel(self, parent_frame, is_left=True):
        """Создает панель с вертикальной прокруткой"""
        canvas = self.widget_factory.create_canvas(
            parent_frame, 
            bg=self.theme_manager.get_color('bg_color'), 
            highlightthickness=0
        )
        
        scrollbar = self.widget_factory.create_scrollbar(
            parent_frame, 
            orient="vertical", 
            command=canvas.yview
        )
        
        scrollable_frame = self.widget_factory.create_frame(
            canvas, 
            bd=0, 
            relief="flat"
        )
        
        scrollable_frame.bind(
            "<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window(
            (0, 0), 
            window=scrollable_frame, 
            anchor="nw"
        )
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Обновляем ширину scrollable_frame при изменении размеров canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width - 20)
        
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Сохраняем ссылки
        if is_left:
            self.left_canvas = canvas
            self.left_scrollbar = scrollbar
            self.left_scrollable_frame = scrollable_frame
        else:
            self.right_canvas = canvas
            self.right_scrollbar = scrollbar
            self.right_scrollable_frame = scrollable_frame
        
        # Упаковываем
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _bind_mousewheel(self):
        """Привязывает обработчик колесика мыши для прокрутки активной панели"""
        def on_mousewheel(event):
            # Определяем, в каком канвасе находится курсор
            widget = event.widget
            x = event.x_root
            y = event.y_root
            
            # Проверяем левый канвас
            if self.left_canvas and self.left_canvas.winfo_exists():
                left_x1 = self.left_canvas.winfo_rootx()
                left_x2 = left_x1 + self.left_canvas.winfo_width()
                left_y1 = self.left_canvas.winfo_rooty()
                left_y2 = left_y1 + self.left_canvas.winfo_height()
                
                if left_x1 <= x <= left_x2 and left_y1 <= y <= left_y2:
                    self.left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                    return
            
            # Проверяем правый канвас
            if self.right_canvas and self.right_canvas.winfo_exists():
                right_x1 = self.right_canvas.winfo_rootx()
                right_x2 = right_x1 + self.right_canvas.winfo_width()
                right_y1 = self.right_canvas.winfo_rooty()
                right_y2 = right_y1 + self.right_canvas.winfo_height()
                
                if right_x1 <= x <= right_x2 and right_y1 <= y <= right_y2:
                    self.right_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                    return
        
        # Привязываем глобально
        self.parent.winfo_toplevel().bind_all("<MouseWheel>", on_mousewheel)
        
        # Также привязываем к самим канвасам для случаев, когда курсор над ними
        if self.left_canvas:
            self.left_canvas.bind("<MouseWheel>", lambda e: self.left_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        if self.right_canvas:
            self.right_canvas.bind("<MouseWheel>", lambda e: self.right_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def _fill_right_panel(self, parent_frame):
        """Заполняет правую панель содержимым"""
        main_container = self.widget_factory.create_frame(parent_frame, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)
        
        # Контейнер для трех карточек в ряд
        cards_container = self.widget_factory.create_frame(main_container)
        cards_container.pack(fill="x", pady=(0, 30))
        
        # Создаем три карточки с одинаковыми размерами
        self._create_step_card(
            cards_container, 
            step_num="1", 
            title="ПОСТРОЙТЕ", 
            colors=('tab1_inactive', 'tab1_active'),
            description=["","","",
                "Постройте граф на вкладке \"Graph Generation\" или \"Custom Graph\"","",
                "Вставьте сформированный граф на вкладки запуска симуляций нажатием на кнопку \"Построить граф\""
            ]
        )
        
        self._create_step_card(
            cards_container, 
            step_num="2", 
            title="ЗАПУСТИТЕ", 
            colors=('tab3_inactive', 'tab3_active'),
            description=["","","",
                "Запустите симуляцию на одном графе на вкладке \"Run Simulation\"","",
                "или запустите множественную генерацию и сбор данных по графам с заданными распределениями на вкладке \"Multiple Simulation\""
            ]
        )
        
        self._create_step_card(
            cards_container, 
            step_num="3", 
            title="АНАЛИЗИРУЙТЕ", 
            colors=('tab5_inactive', 'tab5_active'),
            description=[]
        )
        
        # Разделы по вкладкам
        self._create_tab_sections(main_container)
    
    def _create_step_card(self, parent, step_num, title, colors, description):
        """Создает одну карточку шага"""
        from_color_key, active_color_key = colors
        
        # Получаем реальные цвета из менеджера тем
        border_color = self.theme_manager.get_color('tab_border')
        from_color = self.theme_manager.get_color(from_color_key)
        text_color = self.theme_manager.get_color('text_color')
        
        # Контейнер карточки с одинаковыми размерами
        card = tk.Frame(
            parent, 
            bg=border_color,
            bd=0,
            highlightthickness=0,
            width=150,
            height=330
        )
        card.pack(side="left", fill="both", expand=True, padx=5)
        card.pack_propagate(False)
        
        # Внутренний фон карточки
        inner_card = self.widget_factory.create_frame(card, bg=from_color)
        inner_card.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Контент карточки с отступами по краям
        content = self.widget_factory.create_frame(inner_card, padx=12, pady=15, bg=from_color)
        content.pack(fill="both", expand=True)
        
        # Верхняя часть с номером и заголовком
        header_frame = self.widget_factory.create_frame(content, bg=from_color)
        header_frame.pack(fill="x", pady=(5, 35))  # Увеличен отступ снизу до 35
        
        # Номер шага
        number_label = self.widget_factory.create_label(
            header_frame,
            text=step_num,
            font=("Segoe UI", 42, "bold"),
            fg=text_color,
            bg=from_color
        )
        number_label.pack(anchor="center")
        
        # Заголовок
        title_label = self.widget_factory.create_label(
            header_frame,
            text=title,
            font=("Segoe UI", 18),
            fg=text_color,
            bg=from_color
        )
        title_label.pack(anchor="center", pady=(0, 0))
        
        if step_num == "3":
            # Для третьей карточки - эмодзи лампочки
            center_frame = self.widget_factory.create_frame(content, bg=from_color)
            center_frame.pack(expand=True, fill="both", pady=10)
            
            emoji_label = self.widget_factory.create_label(
                center_frame,
                text="💡",
                font=("Segoe UI", 70),
                fg=text_color,
                bg=from_color
            )
            emoji_label.pack(expand=True, pady=(2, 0))
            
        else:
            # Для первой и второй карточек - описание
            desc_frame = self.widget_factory.create_frame(content, bg=from_color)
            desc_frame.pack(fill="both", expand=True, pady=(10, 5))
            
            for i, text in enumerate(description):
                if text and text.strip():
                    # Создаем фрейм для каждого абзаца
                    text_frame = self.widget_factory.create_frame(desc_frame, bg=from_color)
                    text_frame.pack(fill="x", pady=(0 if i == 0 else 10, 0))
                    
                    # Обычный текст без жирного начертания
                    label = tk.Label(
                        text_frame,
                        text=text,
                        font=("Segoe UI", 10),
                        fg=text_color,
                        bg=from_color,
                        justify="left",
                        wraplength=350,  # Ограничиваем ширину для переноса
                        anchor="w"
                    )
                    label.pack(fill="x")  # Растягиваем по ширине
    
    def _create_tab_sections(self, parent):
        """Создает разделы для каждой вкладки"""
        tab_keys = [
            'tab_generation',
            'tab_custom', 
            'tab_simulation',
            'tab_multiple'
        ]
        
        for tab_key in tab_keys:
            section_frame = self.widget_factory.create_label_frame(
                parent, 
                text=self.t(tab_key)
            )
            section_frame.pack(fill="x", pady=(0, 20))
            
            # Содержимое для вкладки генерации графа
            if tab_key == 'tab_generation':
                # Добавляем описание для распределения РЕБЕР
                self._create_edge_distribution_help(section_frame)
                
                # Добавляем описание для распределения ВЕРШИН
                self._create_vertex_distribution_help(section_frame)
            else:
                # Для остальных вкладок пока заглушка
                content_frame = self.widget_factory.create_frame(section_frame)
                content_frame.pack(fill="x", padx=10, pady=10)
                
                placeholder = self.widget_factory.create_label_normal(
                    content_frame,
                    text="Содержимое раздела будет добавлено позже..."
                )
                placeholder.pack(anchor="w", pady=5)

    def _create_generation_section_content(self, parent_frame):
        """Создает содержимое для раздела генерации графа"""
        content_frame = self.widget_factory.create_frame(parent_frame)
        content_frame.pack(fill="x", padx=10, pady=10)
        
        # Список заголовков разделов из вкладки генерации
        section_titles = [
            'vertex_count',
            'edge_distribution',
            'vertex_distribution',
            'vertex_resistance',
            'vertex_influence',
            'damping'
        ]
        
        for title_key in section_titles:
            # Создаем заголовок раздела
            title_label = self.widget_factory.create_label_h2(
                content_frame,
                text=self.t(title_key)
            )
            title_label.pack(anchor="w", pady=(10 if title_key != 'vertex_count' else 0, 2))
            
            # Добавляем соответствующий контент для каждого раздела
            if title_key == 'vertex_count':
                self._create_vertex_count_help(content_frame)
            elif title_key == 'edge_distribution':
                self._create_edge_distribution_help(content_frame)
            else:
                # Для остальных разделов пока просто отступ
                spacing_frame = self.widget_factory.create_frame(content_frame, height=5)
                spacing_frame.pack(fill="x", pady=(0, 5))

    def _create_vertex_count_help(self, parent_frame):
        """Создает детальное описание для блока количества вершин"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Создаем рамку как на вкладке генерации (сразу под заголовком, без отступов)
        section_frame = self.widget_factory.create_label_frame(
            parent_frame,
            text=""  # Без заголовка, так как заголовок уже есть выше
        )
        section_frame.pack(fill="x", pady=(0, 15), padx=0)  # Убрал верхний отступ полностью
        
        # Внутренний контейнер с отступами
        inner_frame = self.widget_factory.create_frame(section_frame)
        inner_frame.pack(fill="x", padx=10, pady=10)
        
        # Описание функционала (оставляем слева)
        desc_text = "Этот параметр определяет количество вершин, которые будут созданы в графе."
        desc_label = self.widget_factory.create_label_normal(
            inner_frame,
            text=desc_text,
            wraplength=550,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 15))
        
        # Создаем canvas для размещения текста со стрелками и элементов управления
        demo_canvas = tk.Canvas(
            inner_frame,
            height=160,
            bg=self.theme_manager.get_color('frame_bg'),
            highlightthickness=0
        )
        demo_canvas.pack(fill="x", pady=(0, 5))
        
        # Константа для отступа всего контента вправо (2-3 см ≈ 80-100 пикселей)
        RIGHT_OFFSET = 90
        
        # Текст с указателями - все со сдвигом вправо
        # Обычный текст начала фразы
        demo_canvas.create_text(
            10 + RIGHT_OFFSET, 30,
            text="Выберите количество вершин в ",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Текст "поле для ввода" (цветной) - возвращаем как было, без пробела в начале
        entry_text_id = demo_canvas.create_text(
            210 + RIGHT_OFFSET, 30,
            text="поле для ввода",
            font=("Segoe UI", 10, "bold"),
            fill=accent_color,
            anchor="w"
        )
        
        # Текст " или на "
        demo_canvas.create_text(
            310 + RIGHT_OFFSET, 30,
            text=" или на ",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Текст "слайдере" (цветной) - возвращаем как было
        slider_text_id = demo_canvas.create_text(
            360 + RIGHT_OFFSET, 30,
            text="слайдере",
            font=("Segoe UI", 10, "bold"),
            fill=accent_color,
            anchor="w"
        )
        
        # Двоеточие обычным цветом и обычным весом
        demo_canvas.create_text(
            422 + RIGHT_OFFSET, 30,
            text=":",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Демонстрационное поле ввода - сильно вправо
        entry_demo = self.widget_factory.create_entry(
            demo_canvas,
            width=6,
            font=("Segoe UI", 10),
            justify="center"
        )
        entry_demo.insert(0, "50")
        entry_demo.config(state="disabled", disabledbackground=self.theme_manager.get_color('input_bg'),
                          disabledforeground=self.theme_manager.get_color('input_fg'))
        
        # Демонстрационный слайдер - сильно вправо
        slider_demo = self.widget_factory.create_slider(
            demo_canvas,
            from_=10,
            to=100,
            orient="horizontal",
            length=300,
            showvalue=0,
            state="disabled"
        )
        
        # Устанавливаем ползунок в среднее положение
        slider_demo.config(state="normal")
        slider_demo.set(55)
        slider_demo.config(state="disabled")
        
        # Размещаем элементы на canvas со сдвигом вправо
        entry_window = demo_canvas.create_window(150 + RIGHT_OFFSET, 70, window=entry_demo, anchor="w")
        slider_window = demo_canvas.create_window(280 + RIGHT_OFFSET, 70, window=slider_demo, anchor="w")
        
        # Текст с ограничениями - тоже со сдвигом вправо
        demo_canvas.create_text(
            10 + RIGHT_OFFSET, 120,
            text="Минимальное количество вершин — 10",
            font=("Segoe UI", 9),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        demo_canvas.create_text(
            10 + RIGHT_OFFSET, 140,
            text="Максимальное количество вершин — 100",
            font=("Segoe UI", 9),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Функция для рисования стрелок
        def draw_arrows():
            # Стрелка к полю ввода
            entry_text_bbox = demo_canvas.bbox(entry_text_id)
            if entry_text_bbox:
                entry_text_x = (entry_text_bbox[0] + entry_text_bbox[2]) / 2
                entry_text_y = entry_text_bbox[3] + 5
                
                entry_bbox = demo_canvas.bbox(entry_window)
                if entry_bbox:
                    entry_center_x = (entry_bbox[0] + entry_bbox[2]) / 2
                    entry_top_y = entry_bbox[1] - 5
                    
                    demo_canvas.create_line(
                        entry_text_x, entry_text_y,
                        entry_center_x, entry_top_y,
                        arrow='last',
                        fill=accent_color,
                        width=2,
                        smooth=True,
                        tags="static_arrow"
                    )
            
            # Стрелка к слайдеру
            slider_text_bbox = demo_canvas.bbox(slider_text_id)
            if slider_text_bbox:
                slider_text_x = (slider_text_bbox[0] + slider_text_bbox[2]) / 2
                slider_text_y = slider_text_bbox[3] + 5
                
                slider_bbox = demo_canvas.bbox(slider_window)
                if slider_bbox:
                    slider_length = slider_bbox[2] - slider_bbox[0]
                    thumb_position = slider_bbox[0] + slider_length * 0.5
                    slider_top_y = slider_bbox[1] - 5
                    
                    demo_canvas.create_line(
                        slider_text_x, slider_text_y,
                        thumb_position, slider_top_y,
                        arrow='last',
                        fill=accent_color,
                        width=2,
                        smooth=True,
                        tags="static_arrow"
                    )
            
            demo_canvas.update_idletasks()
        
        # Рисуем стрелки после размещения всех элементов
        inner_frame.after(100, draw_arrows)

    def _create_edge_distribution_help(self, parent_frame):
        """Создает детальное описание для блока распределения ребер"""
        # Создаем рамку как на вкладке генерации
        section_frame = self.widget_factory.create_label_frame(
            parent_frame,
            text=""
        )
        section_frame.pack(fill="x", pady=(0, 15), padx=0)
        
        # Внутренний контейнер с отступами
        inner_frame = self.widget_factory.create_frame(section_frame)
        inner_frame.pack(fill="x", padx=10, pady=10)
        
        # Описание функционала
        desc_text = "Этот параметр определяет, как будут распределены веса связей между вершинами в графе."
        desc_label = self.widget_factory.create_label_normal(
            inner_frame,
            text=desc_text,
            wraplength=700,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 15))
        
        # Часть 1: Демонстрация интерфейса выбора распределения
        self._create_distribution_selector_demo(inner_frame)
        
        # Сепаратор
        separator1 = ttk.Separator(inner_frame, orient='horizontal')
        separator1.pack(fill='x', pady=20)
        
        # Часть 2: Равномерное распределение
        self._create_uniform_distribution_info(inner_frame)
        
        # Сепаратор
        separator2 = ttk.Separator(inner_frame, orient='horizontal')
        separator2.pack(fill='x', pady=20)
        
        # Часть 3: Нормальное распределение
        self._create_normal_distribution_info(inner_frame)
        
        # Сепаратор
        separator3 = ttk.Separator(inner_frame, orient='horizontal')
        separator3.pack(fill='x', pady=20)
        
        # Часть 4: Распределение Стьюдента
        self._create_student_distribution_info(inner_frame)
        
        # Сепаратор
        separator4 = ttk.Separator(inner_frame, orient='horizontal')
        separator4.pack(fill='x', pady=20)
        
        # Часть 5: Распределение Лапласа
        self._create_laplace_distribution_info(inner_frame)
        
        # Сепаратор
        separator5 = ttk.Separator(inner_frame, orient='horizontal')
        separator5.pack(fill='x', pady=20)
        
        # Часть 6: Бимодальное распределение (заглушка)
        self._create_bimodal_distribution_info(inner_frame)
        
        # Сепаратор
        separator6 = ttk.Separator(inner_frame, orient='horizontal')
        separator6.pack(fill='x', pady=20)
        
        # Часть 7: Скошенное t-распределение (заглушка)
        self._create_skewed_t_distribution_info(inner_frame)
        
        # Сепаратор
        separator7 = ttk.Separator(inner_frame, orient='horizontal')
        separator7.pack(fill='x', pady=20)
        
        # Часть 8: Ступенчатое распределение (заглушка)
        self._create_stepwise_distribution_info(inner_frame)
    
    def _create_distribution_selector_demo(self, parent_frame):
        """Создает демонстрацию интерфейса выбора распределения"""
        accent_color = self.theme_manager.get_color('accent_color')
        RIGHT_OFFSET = 90
        
        # Создаем canvas для размещения всех элементов
        demo_canvas = tk.Canvas(
            parent_frame,
            height=350,
            bg=self.theme_manager.get_color('frame_bg'),
            highlightthickness=0
        )
        demo_canvas.pack(fill="x", pady=(0, 5))
        
        # Текст с указателями
        demo_canvas.create_text(
            10 + RIGHT_OFFSET, 15,
            text="Выберите тип ",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Текст "распределения" (цветной)
        distribution_word_id = demo_canvas.create_text(
            94 + RIGHT_OFFSET, 15,
            text="распределения",
            font=("Segoe UI", 10, "bold"),
            fill=accent_color,
            anchor="w"
        )
        
        # Продолжение текста
        demo_canvas.create_text(
            190 + RIGHT_OFFSET, 15,
            text=" ребер и задайте значения ",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Текст "параметров" (цветной)
        params_word_id = demo_canvas.create_text(
            357 + RIGHT_OFFSET, 15,
            text="параметров",
            font=("Segoe UI", 10, "bold"),
            fill=accent_color,
            anchor="w"
        )
        
        # Завершение текста
        demo_canvas.create_text(
            435 + RIGHT_OFFSET, 15,
            text=":",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Комбобокс
        combobox_values = [
            "Равномерное",
            "Нормальное",
            "Стьюдента",
            "Лапласа",
            "Бимодальное",
            "Скошенное t",
            "Ступенчатое"
        ]
        
        combobox_var = tk.StringVar(value="Равномерное")
        
        # Создаем кастомный комбобокс
        combobox = self.widget_factory.create_combobox(
            demo_canvas,
            combobox_values,
            combobox_var,
            width=20
        )
        
        # Размещаем комбобокс
        combobox_window = demo_canvas.create_window(
            100 + RIGHT_OFFSET, 55,
            window=combobox,
            anchor="nw"
        )
        
        # Создаем простой список опций прямо на canvas
        list_x = 100 + RIGHT_OFFSET
        list_y = 78  # Сразу под комбобоксом
        list_width = 173
        
        # Рамка для списка
        demo_canvas.create_rectangle(
            list_x, list_y,
            list_x + list_width, list_y + 7 * 25,  # 7 опций по 25px
            outline=self.theme_manager.get_color('border_color'),
            fill=self.theme_manager.get_color('input_bg'),
            width=1
        )
        
        # Опции списка
        for i, value in enumerate(combobox_values):
            item_y = list_y + 2 + i * 25
            
            # Выделяем выбранный элемент
            if value == "Равномерное":
                bg_color = self.theme_manager.get_color('slider_thumb_active')
                fg_color = self.theme_manager.get_color('btn_text')
                
                # Заливка для выбранного элемента
                demo_canvas.create_rectangle(
                    list_x + 1, item_y,
                    list_x + list_width - 1, item_y + 23,
                    fill=bg_color,
                    outline=bg_color
                )
            else:
                bg_color = self.theme_manager.get_color('input_bg')
                fg_color = self.theme_manager.get_color('input_fg')
            
            # Текст опции
            demo_canvas.create_text(
                list_x + 10, item_y + 12,
                text=value,
                font=("Segoe UI", 10),
                fill=fg_color,
                anchor="w"
            )
        
        # Первый параметр - справа от комбобокса
        param1_y = 55
        
        demo_canvas.create_text(
            370 + RIGHT_OFFSET, param1_y + 8,
            text="Параметр:",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Поле ввода для первого параметра
        param1_entry = self.widget_factory.create_entry(
            demo_canvas,
            width=6,
            font=("Segoe UI", 9),
            justify="center"
        )
        param1_entry.insert(0, "0.1")
        param1_entry.config(state="disabled", disabledbackground=self.theme_manager.get_color('input_bg'),
                            disabledforeground=self.theme_manager.get_color('input_fg'))
        
        param1_entry_window = demo_canvas.create_window(
            450 + RIGHT_OFFSET, param1_y,
            window=param1_entry,
            anchor="nw"
        )
        
        # Слайдер для первого параметра
        param1_slider = self.widget_factory.create_slider(
            demo_canvas,
            from_=0,
            to=100,
            orient="horizontal",
            length=150,
            showvalue=0,
            state="normal"
        )
        param1_slider.set(10)
        param1_slider.update()
        param1_slider.config(state="disabled")
        
        param1_slider_window = demo_canvas.create_window(
            510 + RIGHT_OFFSET, param1_y - 4,
            window=param1_slider,
            anchor="nw"
        )
        
        # Второй параметр
        param2_y = 85
        
        demo_canvas.create_text(
            370 + RIGHT_OFFSET, param2_y + 8,
            text="Параметр:",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )
        
        # Поле ввода для второго параметра
        param2_entry = self.widget_factory.create_entry(
            demo_canvas,
            width=6,
            font=("Segoe UI", 9),
            justify="center"
        )
        param2_entry.insert(0, "0.5")
        param2_entry.config(state="disabled", disabledbackground=self.theme_manager.get_color('input_bg'),
                            disabledforeground=self.theme_manager.get_color('input_fg'))
        
        param2_entry_window = demo_canvas.create_window(
            450 + RIGHT_OFFSET, param2_y,
            window=param2_entry,
            anchor="nw"
        )
        
        # Слайдер для второго параметра
        param2_slider = self.widget_factory.create_slider(
            demo_canvas,
            from_=0,
            to=100,
            orient="horizontal",
            length=150,
            showvalue=0,
            state="normal"
        )
        param2_slider.set(50)
        param2_slider.update()
        param2_slider.config(state="disabled")
        
        param2_slider_window = demo_canvas.create_window(
            510 + RIGHT_OFFSET, param2_y - 4,
            window=param2_slider,
            anchor="nw"
        )
        
        # Функция для рисования стрелок
        def draw_arrows():
            # Стрелка от слова "распределения" к комбобоксу
            dist_word_bbox = demo_canvas.bbox(distribution_word_id)
            if dist_word_bbox:
                word_x = (dist_word_bbox[0] + dist_word_bbox[2]) / 2
                word_y = dist_word_bbox[3] + 5
                
                combobox_bbox = demo_canvas.bbox(combobox_window)
                if combobox_bbox:
                    combobox_center_x = (combobox_bbox[0] + combobox_bbox[2]) / 2
                    combobox_top_y = combobox_bbox[1] - 5
                    
                    demo_canvas.create_line(
                        word_x, word_y,
                        combobox_center_x, combobox_top_y,
                        arrow='last',
                        fill=accent_color,
                        width=2,
                        smooth=True,
                        tags="static_arrow"
                    )
            
            # Стрелка от слова "параметров" к первому полю ввода
            params_word_bbox = demo_canvas.bbox(params_word_id)
            if params_word_bbox:
                word_x = (params_word_bbox[0] + params_word_bbox[2]) / 2
                word_y = params_word_bbox[3] + 5
                
                param1_bbox = demo_canvas.bbox(param1_entry_window)
                if param1_bbox:
                    param1_center_x = (param1_bbox[0] + param1_bbox[2]) / 2
                    param1_top_y = param1_bbox[1] - 5
                    
                    demo_canvas.create_line(
                        word_x, word_y,
                        param1_center_x, param1_top_y,
                        arrow='last',
                        fill=accent_color,
                        width=2,
                        smooth=True,
                        tags="static_arrow"
                    )
            
            demo_canvas.update_idletasks()
        
        # Рисуем стрелки после размещения всех элементов
        parent_frame.after(100, draw_arrows)

    def _create_uniform_distribution_info(self, parent_frame):
        """Создает описание равномерного распределения с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Заголовок "Равномерное распределение"
        uniform_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Равномерное распределение"
        )
        uniform_title.pack(anchor="w", pady=(0, 10))
        
        # Описание равномерного распределения
        uniform_desc = "Распределение случайной величины, которая с равной вероятностью принимает любое значение в заданном интервале [a, b]."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=uniform_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        # Вспомогательный серый текст с информацией о реализации
        code_desc = "Для равномерного распределения весов ребер в коде используется numpy.random.uniform(a, b)."
        code_label = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label.pack(anchor="w", pady=(0, 15))
        
        # Создаем контейнер для трех примеров в одну линию
        examples_frame = self.widget_factory.create_frame(parent_frame)
        examples_frame.pack(fill="x", pady=(0, 15))
        
        # Параметры для трех примеров
        examples = [
            {"min": -1.0, "max": 1.0},
            {"min": -0.9, "max": 0.1},
            {"min": -0.2, "max": 0.6}
        ]
        
        for i, example in enumerate(examples):
            min_val = example["min"]
            max_val = example["max"]
            
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов (мин/макс)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"мин: {min_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"макс: {max_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            # Создаем график используя существующий класс EdgeWeightPlotWidget
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры для равномерного распределения
            dist_params = {
                "type": "Uniform",
                "min": min_val,
                "max": max_val
            }
            plot_widget.update_plot(dist_params)
        
        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))
        
        limits_text = "Минимальное значение — -1\nМаксимальное значение — +1\nМинимальное расстояние между границами — 0.01"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")

    def _create_normal_distribution_info(self, parent_frame):
        """Создает описание нормального распределения с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Заголовок "Нормальное распределение"
        normal_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Нормальное распределение"
        )
        normal_title.pack(anchor="w", pady=(0, 10))
        
        # Описание нормального распределения
        normal_desc = "Непрерывное распределение вероятностей с пиком в центре и симметричными боковыми сторонами. "
        normal_desc += "Параметр μ задает центр распределения, параметр σ — стандартное отклонение (ширину)."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=normal_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        # Вспомогательный серый текст с информацией о реализации
        code_desc = "В коде используется scipy.stats.truncnorm.rvs(a, b, loc=μ, scale=σ) для усечения значений в диапазон [-1, 1]."
        code_label = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label.pack(anchor="w", pady=(0, 15))
        
        # ПРИМЕР 1: Разные μ при фиксированном σ
        mu_examples = [
            {"mu": -0.8, "sigma": 0.3},
            {"mu": 0.0, "sigma": 0.3},
            {"mu": 0.8, "sigma": 0.3}
        ]
        
        # Создаем контейнер для первого ряда примеров
        mu_examples_frame = self.widget_factory.create_frame(parent_frame)
        mu_examples_frame.pack(fill="x", pady=(0, 20))
        
        for i, example in enumerate(mu_examples):
            mu_val = example["mu"]
            sigma_val = example["sigma"]
            
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(mu_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов (μ/σ)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ: {mu_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ: {sigma_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            # Создаем график используя существующий класс EdgeWeightPlotWidget
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры для нормального распределения
            dist_params = {
                "type": "Normal",
                "mu": mu_val,
                "sigma": sigma_val
            }
            plot_widget.update_plot(dist_params)
        
        # ПРИМЕР 2: Разные σ при фиксированном μ
        sigma_examples = [
            {"mu": 0.0, "sigma": 0.1},
            {"mu": 0.0, "sigma": 0.4},
            {"mu": 0.0, "sigma": 0.8}
        ]
        
        # Создаем контейнер для второго ряда примеров
        sigma_examples_frame = self.widget_factory.create_frame(parent_frame)
        sigma_examples_frame.pack(fill="x", pady=(0, 15))
        
        for i, example in enumerate(sigma_examples):
            mu_val = example["mu"]
            sigma_val = example["sigma"]
            
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(sigma_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов (μ/σ)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ: {mu_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ: {sigma_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            # Создаем график используя существующий класс EdgeWeightPlotWidget
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры для нормального распределения
            dist_params = {
                "type": "Normal",
                "mu": mu_val,
                "sigma": sigma_val
            }
            plot_widget.update_plot(dist_params)
        
        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))
        
        limits_text = "Диапазон μ: от -1 до +1\nДиапазон σ: от 0.01 до 1\nЗначения усекаются до интервала [-1, +1]"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")

    def _create_student_distribution_info(self, parent_frame):
        """Создает описание распределения Стьюдента с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Заголовок "Распределение Стьюдента"
        student_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Распределение Стьюдента"
        )
        student_title.pack(anchor="w", pady=(0, 10))
        
        # Описание распределения Стьюдента
        student_desc = "Распределение Стьюдента (t-распределение) похоже на нормальное, но имеет более тяжелые хвосты. Параметр df (degrees of freedom) определяет форму распределения: чем меньше df, тем тяжелее хвосты. Параметр scale масштабирует распределение."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=student_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        # Вспомогательный серый текст с информацией о реализации
        code_desc1 = "В коде используется scipy.stats.t.rvs(df, scale=scale) с последующим усечением значений в диапазон [-1, 1]."
        code_label1 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc1,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label1.pack(anchor="w", pady=(0, 2))
        
        code_desc2 = "Для усечения используется метод исключения (генерация в 2 раза больше элементов и отбор попавших в [-1, 1])."
        code_label2 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc2,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label2.pack(anchor="w", pady=(0, 5))
        
        # ПРИМЕР 1: Разные df при фиксированном scale
        df_examples = [
            {"df": 2, "scale": 0.3},
            {"df": 5, "scale": 0.3},
            {"df": 30, "scale": 0.3}
        ]
        
        # Создаем контейнер для первого ряда примеров
        df_examples_frame = self.widget_factory.create_frame(parent_frame)
        df_examples_frame.pack(fill="x", pady=(0, 20))
        
        for i, example in enumerate(df_examples):
            df_val = example["df"]
            scale_val = example["scale"]
            
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(df_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов (df/scale)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"df: {df_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"scale: {scale_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            # Создаем график используя существующий класс EdgeWeightPlotWidget
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры для распределения Стьюдента
            dist_params = {
                "type": "Student",
                "df": df_val,
                "scale": scale_val
            }
            plot_widget.update_plot(dist_params)
        
        # ПРИМЕР 2: Разные scale при фиксированном df
        scale_examples = [
            {"df": 5, "scale": 0.2},
            {"df": 5, "scale": 0.4},
            {"df": 5, "scale": 0.8}
        ]
        
        # Создаем контейнер для второго ряда примеров
        scale_examples_frame = self.widget_factory.create_frame(parent_frame)
        scale_examples_frame.pack(fill="x", pady=(0, 15))
        
        for i, example in enumerate(scale_examples):
            df_val = example["df"]
            scale_val = example["scale"]
            
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(scale_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов (df/scale)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"df: {df_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"scale: {scale_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            # Создаем график используя существующий класс EdgeWeightPlotWidget
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры для распределения Стьюдента
            dist_params = {
                "type": "Student",
                "df": df_val,
                "scale": scale_val
            }
            plot_widget.update_plot(dist_params)
        
        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))
        
        limits_text = "Диапазон df: от 1 до 30\nДиапазон scale: от 0.01 до 1\nЗначения усекаются до интервала [-1, +1]"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")

    def _create_laplace_distribution_info(self, parent_frame):
        """Создает описание распределения Лапласа с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Заголовок "Распределение Лапласа"
        laplace_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Распределение Лапласа"
        )
        laplace_title.pack(anchor="w", pady=(0, 10))
        
        # Описание распределения Лапласа
        laplace_desc = "Распределение Лапласа (двойное показательное) имеет более острый пик и тяжелые хвосты по сравнению с нормальным. Параметр loc задает центр распределения, параметр scale — масштаб (разброс)."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=laplace_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        # Вспомогательный серый текст с информацией о реализации
        code_desc1 = "В коде используется scipy.stats.laplace.rvs(loc=loc, scale=scale) с последующим усечением значений в диапазон [-1, 1]."
        code_label1 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc1,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label1.pack(anchor="w", pady=(0, 2))
        
        code_desc2 = "Для усечения используется метод исключения (генерация в 2 раза больше элементов и отбор попавших в [-1, 1])."
        code_label2 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc2,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label2.pack(anchor="w", pady=(0, 15))
        
        # ПРИМЕР 1: Разные loc при фиксированном scale
        loc_examples = [
            {"loc": -0.6, "scale": 0.2},
            {"loc": 0.0, "scale": 0.2},
            {"loc": 0.6, "scale": 0.2}
        ]
        
        # Создаем контейнер для первого ряда примеров
        loc_examples_frame = self.widget_factory.create_frame(parent_frame)
        loc_examples_frame.pack(fill="x", pady=(0, 20))
        
        for i, example in enumerate(loc_examples):
            loc_val = example["loc"]
            scale_val = example["scale"]
            
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(loc_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов (loc/scale)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"loc: {loc_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"scale: {scale_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            # Создаем график используя существующий класс EdgeWeightPlotWidget
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры для распределения Лапласа
            dist_params = {
                "type": "Laplace",
                "loc": loc_val,
                "scale": scale_val
            }
            plot_widget.update_plot(dist_params)
        
        # ПРИМЕР 2: Разные scale при фиксированном loc
        scale_examples = [
            {"loc": 0.0, "scale": 0.1},
            {"loc": 0.0, "scale": 0.3},
            {"loc": 0.0, "scale": 0.6}
        ]
        
        # Создаем контейнер для второго ряда примеров
        scale_examples_frame = self.widget_factory.create_frame(parent_frame)
        scale_examples_frame.pack(fill="x", pady=(0, 15))
        
        for i, example in enumerate(scale_examples):
            loc_val = example["loc"]
            scale_val = example["scale"]
            
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(scale_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов (loc/scale)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"loc: {loc_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"scale: {scale_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))
            
            # Создаем график используя существующий класс EdgeWeightPlotWidget
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры для распределения Лапласа
            dist_params = {
                "type": "Laplace",
                "loc": loc_val,
                "scale": scale_val
            }
            plot_widget.update_plot(dist_params)
        
        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))
        
        limits_text = "Диапазон loc: от -1 до +1\nДиапазон scale: от 0.01 до 1\nЗначения усекаются до интервала [-1, +1]"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")

    def _create_bimodal_distribution_info(self, parent_frame):
        """Создает описание бимодального распределения с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Заголовок "Бимодальное распределение"
        bimodal_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Бимодальное распределение"
        )
        bimodal_title.pack(anchor="w", pady=(0, 10))
        
        # Описание бимодального распределения
        bimodal_desc = "Бимодальное распределение представляет собой смесь двух нормальных распределений с разными центрами. Параметры μ₁ и μ₂ задают положения пиков, σ₁ и σ₂ — их ширину, weight₁ — долю первого распределения в смеси."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=bimodal_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        # Вспомогательный серый текст с информацией о реализации
        code_desc1 = "В коде используется смесь двух усеченных нормальных распределений: scipy.stats.truncnorm.rvs() с весами weight₁ и (1-weight₁)."
        code_label1 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc1,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label1.pack(anchor="w", pady=(0, 2))
        
        code_desc2 = "Каждая компонента генерируется сразу в диапазоне [-1, 1] через параметры a и b."
        code_label2 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc2,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label2.pack(anchor="w", pady=(0, 15))
        
        # РЯД 1: Разные положения пиков (симметричные и асимметричные)
        pos_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разное положение пиков:"
        )
        pos_title.pack(anchor="w", pady=(0, 10))
        
        pos_examples = [
            {"mu1": -0.7, "mu2": 0.7, "sigma1": 0.2, "sigma2": 0.2, "weight1": 0.5},
            {"mu1": -0.7, "mu2": 0.1, "sigma1": 0.2, "sigma2": 0.2, "weight1": 0.5},
            {"mu1": -0.1, "mu2": 0.7, "sigma1": 0.2, "sigma2": 0.2, "weight1": 0.5}
        ]
        
        pos_frame = self.widget_factory.create_frame(parent_frame)
        pos_frame.pack(fill="x", pady=(0, 20))
        
        for i, example in enumerate(pos_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(pos_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ₁: {example['mu1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ₂: {example['mu2']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ₁: {example['sigma1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ₂: {example['sigma2']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"w₁: {example['weight1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            # Создаем график
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры
            dist_params = {
                "type": "Bimodal",
                "mu1": example["mu1"],
                "sigma1": example["sigma1"],
                "mu2": example["mu2"],
                "sigma2": example["sigma2"],
                "weight1": example["weight1"]
            }
            plot_widget.update_plot(dist_params)
        
        # РЯД 2: Разная ширина пиков
        width_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разная ширина пиков:"
        )
        width_title.pack(anchor="w", pady=(0, 10))
        
        width_examples = [
            {"mu1": -0.7, "mu2": 0.7, "sigma1": 0.1, "sigma2": 0.1, "weight1": 0.5},
            {"mu1": -0.7, "mu2": 0.7, "sigma1": 0.6, "sigma2": 0.1, "weight1": 0.5},
            {"mu1": -0.7, "mu2": 0.7, "sigma1": 0.1, "sigma2": 0.6, "weight1": 0.5}
        ]
        
        width_frame = self.widget_factory.create_frame(parent_frame)
        width_frame.pack(fill="x", pady=(0, 20))
        
        for i, example in enumerate(width_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(width_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ₁: {example['mu1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ₂: {example['mu2']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ₁: {example['sigma1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ₂: {example['sigma2']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"w₁: {example['weight1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            # Создаем график
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры
            dist_params = {
                "type": "Bimodal",
                "mu1": example["mu1"],
                "sigma1": example["sigma1"],
                "mu2": example["mu2"],
                "sigma2": example["sigma2"],
                "weight1": example["weight1"]
            }
            plot_widget.update_plot(dist_params)
        
        # РЯД 3: Разные веса компонент
        weight_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разные веса компонент:"
        )
        weight_title.pack(anchor="w", pady=(0, 10))
        
        weight_examples = [
            {"mu1": -0.7, "mu2": 0.7, "sigma1": 0.2, "sigma2": 0.2, "weight1": 0.1},
            {"mu1": -0.7, "mu2": 0.7, "sigma1": 0.2, "sigma2": 0.2, "weight1": 0.4},
            {"mu1": -0.7, "mu2": 0.7, "sigma1": 0.2, "sigma2": 0.2, "weight1": 0.9}
        ]
        
        weight_frame = self.widget_factory.create_frame(parent_frame)
        weight_frame.pack(fill="x", pady=(0, 15))
        
        for i, example in enumerate(weight_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(weight_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ₁: {example['mu1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ₂: {example['mu2']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ₁: {example['sigma1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ₂: {example['sigma2']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"w₁: {example['weight1']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            # Создаем график
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры
            dist_params = {
                "type": "Bimodal",
                "mu1": example["mu1"],
                "sigma1": example["sigma1"],
                "mu2": example["mu2"],
                "sigma2": example["sigma2"],
                "weight1": example["weight1"]
            }
            plot_widget.update_plot(dist_params)
        
        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))
        
        limits_text = "Диапазон μ: от -1 до +1\nДиапазон σ: от 0.01 до 1\nДиапазон weight₁: от 0 до 1"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")
    
    def _create_skewed_t_distribution_info(self, parent_frame):
        """Создает описание скошенного t-распределения с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Заголовок "Скошенное t-распределение"
        skewed_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Скошенное t-распределение"
        )
        skewed_title.pack(anchor="w", pady=(0, 10))
        
        # Описание скошенного t-распределения
        skewed_desc = "Скошенное t-распределение (skewed t) сочетает свойства распределения Стьюдента (тяжелые хвосты) с возможностью асимметрии. Параметр df определяет тяжесть хвостов, shape задает скошенность, scale масштабирует распределение."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=skewed_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))
        
        # Вспомогательный серый текст с информацией о реализации
        code_desc1 = "В коде используется scipy.stats.nct.rvs(df, shape, scale=scale) с последующим усечением значений в диапазон [-1, 1]."
        code_label1 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc1,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label1.pack(anchor="w", pady=(0, 2))
        
        code_desc2 = "Для усечения используется метод исключения (генерация в 2 раза больше элементов и отбор попавших в [-1, 1])."
        code_label2 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc2,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label2.pack(anchor="w", pady=(0, 15))
        
        # РЯД 1: Разные значения shape (скошенность) при фиксированных df и scale
        shape_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разная скошенность:"
        )
        shape_title.pack(anchor="w", pady=(0, 10))
        
        shape_examples = [
            {"df": 10, "shape": -3, "scale": 0.3},
            {"df": 10, "shape": 0, "scale": 0.3},
            {"df": 10, "shape": 3, "scale": 0.3}
        ]
        
        shape_frame = self.widget_factory.create_frame(parent_frame)
        shape_frame.pack(fill="x", pady=(0, 20))
        
        for i, example in enumerate(shape_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(shape_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"df: {example['df']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"shape: {example['shape']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"scale: {example['scale']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            # Создаем график
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры
            dist_params = {
                "type": "Skewed_t",
                "df": example["df"],
                "shape": example["shape"],
                "scale": example["scale"]
            }
            plot_widget.update_plot(dist_params)
        
        # РЯД 2: Разные значения df (тяжесть хвостов) при фиксированных shape и scale
        df_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разная тяжесть хвостов:"
        )
        df_title.pack(anchor="w", pady=(0, 10))
        
        df_examples = [
            {"df": 3, "shape": 2, "scale": 0.3},
            {"df": 10, "shape": 2, "scale": 0.3},
            {"df": 30, "shape": 2, "scale": 0.3}
        ]
        
        df_frame = self.widget_factory.create_frame(parent_frame)
        df_frame.pack(fill="x", pady=(0, 20))
        
        for i, example in enumerate(df_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(df_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"df: {example['df']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"shape: {example['shape']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"scale: {example['scale']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            # Создаем график
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры
            dist_params = {
                "type": "Skewed_t",
                "df": example["df"],
                "shape": example["shape"],
                "scale": example["scale"]
            }
            plot_widget.update_plot(dist_params)
        
        # РЯД 3: Разные значения scale (масштаб) при фиксированных df и shape
        scale_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разный масштаб:"
        )
        scale_title.pack(anchor="w", pady=(0, 10))
        
        scale_examples = [
            {"df": 10, "shape": 2, "scale": 0.2},
            {"df": 10, "shape": 2, "scale": 0.4},
            {"df": 10, "shape": 2, "scale": 0.7}
        ]
        
        scale_frame = self.widget_factory.create_frame(parent_frame)
        scale_frame.pack(fill="x", pady=(0, 15))
        
        for i, example in enumerate(scale_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(scale_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))
            
            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"df: {example['df']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"shape: {example['shape']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            self.widget_factory.create_label_small(
                text_frame,
                text=f"scale: {example['scale']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))
            
            # Создаем график
            plot_widget = EdgeWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")
            
            # Передаем параметры
            dist_params = {
                "type": "Skewed_t",
                "df": example["df"],
                "shape": example["shape"],
                "scale": example["scale"]
            }
            plot_widget.update_plot(dist_params)
        
        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))
        
        limits_text = "Диапазон df: от 1 до 30\nДиапазон shape: от -5 до +5\nДиапазон scale: от 0.01 до 1\nЗначения усекаются до интервала [-1, +1]"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")
    
    def _create_stepwise_distribution_info(self, parent_frame):
        """Заглушка для ступенчатого распределения"""
        accent_color = self.theme_manager.get_color('accent_color')
        
        # Заголовок "Ступенчатое распределение"
        stepwise_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Ступенчатое распределение"
        )
        stepwise_title.pack(anchor="w", pady=(0, 10))
        
        # Описание
        desc_text = "Описание ступенчатого распределения будет добавлено позже."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=desc_text,
            wraplength=700,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))


    # ================== БЛОК ДЛЯ РАСПРЕДЕЛЕНИЙ ВЕРШИН ==================
    def _create_vertex_distribution_help(self, parent_frame):
        """Создает детальное описание для блока распределения весов вершин"""
        # Создаем рамку как на вкладке генерации
        section_frame = self.widget_factory.create_label_frame(
            parent_frame,
            text=""
        )
        section_frame.pack(fill="x", pady=(0, 15), padx=0)

        # Внутренний контейнер с отступами
        inner_frame = self.widget_factory.create_frame(section_frame)
        inner_frame.pack(fill="x", padx=10, pady=10)

        # Описание функционала
        desc_text = "Этот параметр определяет, как будут распределены веса (размеры) вершин в графе."
        desc_label = self.widget_factory.create_label_normal(
            inner_frame,
            text=desc_text,
            wraplength=700,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 15))

        # Часть 1: Демонстрация интерфейса выбора распределения
        self._create_vertex_distribution_selector_demo(inner_frame)

        # Сепаратор
        separator1 = ttk.Separator(inner_frame, orient='horizontal')
        separator1.pack(fill='x', pady=20)

        # Часть 2: Нет (None)
        self._create_vertex_none_distribution_info(inner_frame)

        # Сепаратор
        separator2 = ttk.Separator(inner_frame, orient='horizontal')
        separator2.pack(fill='x', pady=20)

        # Часть 3: Равномерное распределение
        self._create_vertex_uniform_distribution_info(inner_frame)

        # Сепаратор
        separator3 = ttk.Separator(inner_frame, orient='horizontal')
        separator3.pack(fill='x', pady=20)

        # Часть 4: Нормальное распределение
        self._create_vertex_normal_distribution_info(inner_frame)

        # Сепаратор
        separator4 = ttk.Separator(inner_frame, orient='horizontal')
        separator4.pack(fill='x', pady=20)

        # Часть 5: Логнормальное распределение
        self._create_vertex_lognormal_distribution_info(inner_frame)

        # Сепаратор
        separator5 = ttk.Separator(inner_frame, orient='horizontal')
        separator5.pack(fill='x', pady=20)

        # Часть 6: Ступенчатое распределение (заглушка)
        self._create_vertex_stepwise_distribution_info(inner_frame)

    def _create_vertex_distribution_selector_demo(self, parent_frame):
        """Создает демонстрацию интерфейса выбора распределения для вершин"""
        accent_color = self.theme_manager.get_color('accent_color')
        RIGHT_OFFSET = 90

        # Создаем canvas для размещения всех элементов
        demo_canvas = tk.Canvas(
            parent_frame,
            height=350,
            bg=self.theme_manager.get_color('frame_bg'),
            highlightthickness=0
        )
        demo_canvas.pack(fill="x", pady=(0, 5))

        # Текст с указателями
        demo_canvas.create_text(
            10 + RIGHT_OFFSET, 15,
            text="Выберите тип ",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )

        # Текст "распределения" (цветной)
        distribution_word_id = demo_canvas.create_text(
            94 + RIGHT_OFFSET, 15,
            text="распределения",
            font=("Segoe UI", 10, "bold"),
            fill=accent_color,
            anchor="w"
        )

        # Продолжение текста
        demo_canvas.create_text(
            190 + RIGHT_OFFSET, 15,
            text=" вершин и задайте значения ",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )

        # Текст "параметров" (цветной)
        params_word_id = demo_canvas.create_text(
            357 + RIGHT_OFFSET, 15,
            text="параметров",
            font=("Segoe UI", 10, "bold"),
            fill=accent_color,
            anchor="w"
        )

        # Завершение текста
        demo_canvas.create_text(
            435 + RIGHT_OFFSET, 15,
            text=":",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )

        # Комбобокс для вершин
        combobox_values = [
            "Нет",
            "Равномерное",
            "Нормальное",
            "Логнормальное",
            "Ступенчатое"
        ]

        combobox_var = tk.StringVar(value="Равномерное")

        # Создаем кастомный комбобокс
        combobox = self.widget_factory.create_combobox(
            demo_canvas,
            combobox_values,
            combobox_var,
            width=20
        )

        # Размещаем комбобокс
        combobox_window = demo_canvas.create_window(
            100 + RIGHT_OFFSET, 55,
            window=combobox,
            anchor="nw"
        )

        # Создаем простой список опций прямо на canvas
        list_x = 100 + RIGHT_OFFSET
        list_y = 78  # Сразу под комбобоксом
        list_width = 173

        # Рамка для списка
        demo_canvas.create_rectangle(
            list_x, list_y,
            list_x + list_width, list_y + 5 * 25,  # 5 опций по 25px
            outline=self.theme_manager.get_color('border_color'),
            fill=self.theme_manager.get_color('input_bg'),
            width=1
        )

        # Опции списка
        for i, value in enumerate(combobox_values):
            item_y = list_y + 2 + i * 25

            # Выделяем выбранный элемент
            if value == "Равномерное":
                bg_color = self.theme_manager.get_color('slider_thumb_active')
                fg_color = self.theme_manager.get_color('btn_text')

                # Заливка для выбранного элемента
                demo_canvas.create_rectangle(
                    list_x + 1, item_y,
                    list_x + list_width - 1, item_y + 23,
                    fill=bg_color,
                    outline=bg_color
                )
            else:
                bg_color = self.theme_manager.get_color('input_bg')
                fg_color = self.theme_manager.get_color('input_fg')

            # Текст опции
            demo_canvas.create_text(
                list_x + 10, item_y + 12,
                text=value,
                font=("Segoe UI", 10),
                fill=fg_color,
                anchor="w"
            )

        # Первый параметр - справа от комбобокса
        param1_y = 55

        demo_canvas.create_text(
            370 + RIGHT_OFFSET, param1_y + 8,
            text="Параметр:",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )

        # Поле ввода для первого параметра
        param1_entry = self.widget_factory.create_entry(
            demo_canvas,
            width=6,
            font=("Segoe UI", 9),
            justify="center"
        )
        param1_entry.insert(0, "0.5")
        param1_entry.config(state="disabled", disabledbackground=self.theme_manager.get_color('input_bg'),
                            disabledforeground=self.theme_manager.get_color('input_fg'))

        param1_entry_window = demo_canvas.create_window(
            450 + RIGHT_OFFSET, param1_y,
            window=param1_entry,
            anchor="nw"
        )

        # Слайдер для первого параметра
        param1_slider = self.widget_factory.create_slider(
            demo_canvas,
            from_=0,
            to=100,
            orient="horizontal",
            length=150,
            showvalue=0,
            state="normal"
        )
        param1_slider.set(50)
        param1_slider.update()
        param1_slider.config(state="disabled")

        param1_slider_window = demo_canvas.create_window(
            510 + RIGHT_OFFSET, param1_y - 4,
            window=param1_slider,
            anchor="nw"
        )

        # Второй параметр
        param2_y = 85

        demo_canvas.create_text(
            370 + RIGHT_OFFSET, param2_y + 8,
            text="Параметр:",
            font=("Segoe UI", 10),
            fill=self.theme_manager.get_color('text_color'),
            anchor="w"
        )

        # Поле ввода для второго параметра
        param2_entry = self.widget_factory.create_entry(
            demo_canvas,
            width=6,
            font=("Segoe UI", 9),
            justify="center"
        )
        param2_entry.insert(0, "0.2")
        param2_entry.config(state="disabled", disabledbackground=self.theme_manager.get_color('input_bg'),
                            disabledforeground=self.theme_manager.get_color('input_fg'))

        param2_entry_window = demo_canvas.create_window(
            450 + RIGHT_OFFSET, param2_y,
            window=param2_entry,
            anchor="nw"
        )

        # Слайдер для второго параметра
        param2_slider = self.widget_factory.create_slider(
            demo_canvas,
            from_=0,
            to=100,
            orient="horizontal",
            length=150,
            showvalue=0,
            state="normal"
        )
        param2_slider.set(20)
        param2_slider.update()
        param2_slider.config(state="disabled")

        param2_slider_window = demo_canvas.create_window(
            510 + RIGHT_OFFSET, param2_y - 4,
            window=param2_slider,
            anchor="nw"
        )

        # Функция для рисования стрелок
        def draw_arrows():
            # Стрелка от слова "распределения" к комбобоксу
            dist_word_bbox = demo_canvas.bbox(distribution_word_id)
            if dist_word_bbox:
                word_x = (dist_word_bbox[0] + dist_word_bbox[2]) / 2
                word_y = dist_word_bbox[3] + 5

                combobox_bbox = demo_canvas.bbox(combobox_window)
                if combobox_bbox:
                    combobox_center_x = (combobox_bbox[0] + combobox_bbox[2]) / 2
                    combobox_top_y = combobox_bbox[1] - 5

                    demo_canvas.create_line(
                        word_x, word_y,
                        combobox_center_x, combobox_top_y,
                        arrow='last',
                        fill=accent_color,
                        width=2,
                        smooth=True,
                        tags="static_arrow"
                    )

            # Стрелка от слова "параметров" к первому полю ввода
            params_word_bbox = demo_canvas.bbox(params_word_id)
            if params_word_bbox:
                word_x = (params_word_bbox[0] + params_word_bbox[2]) / 2
                word_y = params_word_bbox[3] + 5

                param1_bbox = demo_canvas.bbox(param1_entry_window)
                if param1_bbox:
                    param1_center_x = (param1_bbox[0] + param1_bbox[2]) / 2
                    param1_top_y = param1_bbox[1] - 5

                    demo_canvas.create_line(
                        word_x, word_y,
                        param1_center_x, param1_top_y,
                        arrow='last',
                        fill=accent_color,
                        width=2,
                        smooth=True,
                        tags="static_arrow"
                    )

            demo_canvas.update_idletasks()

        # Рисуем стрелки после размещения всех элементов
        parent_frame.after(100, draw_arrows)

    def _create_vertex_none_distribution_info(self, parent_frame):
        """Создает описание для 'Нет' распределения вершин"""
        accent_color = self.theme_manager.get_color('accent_color')

        # Заголовок "Нет распределения"
        none_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Нет распределения (Все вершины равны)"
        )
        none_title.pack(anchor="w", pady=(0, 10))

        # Описание
        none_desc = "При выборе этого параметра веса всех вершин устанавливаются равными 1.0. Это означает, что все вершины в графе имеют одинаковый размер и свойства (устойчивость, влияние), если они не изменяются другими параметрами."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=none_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))

        # Вспомогательный серый текст с информацией о реализации
        code_desc = "В коде каждому узлу графа присваивается вес 1.0."
        code_label = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label.pack(anchor="w", pady=(0, 15))

    def _create_vertex_uniform_distribution_info(self, parent_frame):
        """Создает описание равномерного распределения для вершин с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')

        # Заголовок "Равномерное распределение"
        uniform_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Равномерное распределение"
        )
        uniform_title.pack(anchor="w", pady=(0, 10))

        # Описание равномерного распределения
        uniform_desc = "Вес каждой вершины выбирается случайно и равномерно из заданного интервала [a, b] в диапазоне от 0 до 1."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=uniform_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))

        # Вспомогательный серый текст с информацией о реализации
        code_desc = "Для равномерного распределения весов вершин в коде используется numpy.random.uniform(a, b)."
        code_label = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label.pack(anchor="w", pady=(0, 15))

        # Создаем контейнер для трех примеров в одну линию
        examples_frame = self.widget_factory.create_frame(parent_frame)
        examples_frame.pack(fill="x", pady=(0, 15))

        # Параметры для трех примеров (в диапазоне 0..1)
        examples = [
            {"min": 0.0, "max": 1.0},
            {"min": 0.0, "max": 0.3},
            {"min": 0.7, "max": 1.0}
        ]

        for i, example in enumerate(examples):
            min_val = example["min"]
            max_val = example["max"]

            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))

            # Фрейм для текстов (мин/макс)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"мин: {min_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"макс: {max_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))

            # Создаем график используя класс для вершин VertexWeightPlotWidget
            plot_widget = VertexWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")

            # Передаем параметры для равномерного распределения
            dist_type = "Uniform"
            dist_params = {
                "min": min_val,
                "max": max_val
            }
            plot_widget.update_plot(dist_type, dist_params)

        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))

        limits_text = "Минимальное значение — 0.0\nМаксимальное значение — 1.0\nМинимальное расстояние между границами — 0.01"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")

    def _create_vertex_normal_distribution_info(self, parent_frame):
        """Создает описание нормального распределения для вершин с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')

        # Заголовок "Нормальное распределение"
        normal_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Нормальное распределение"
        )
        normal_title.pack(anchor="w", pady=(0, 10))

        # Описание нормального распределения
        normal_desc = "Вершины распределяются по нормальному закону. Параметр μ задает центр распределения, параметр σ — стандартное отклонение (ширину). Значения усекаются до интервала [0, 1]."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=normal_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))

        # Вспомогательный серый текст с информацией о реализации
        code_desc = "В коде используется scipy.stats.truncnorm.rvs(a, b, loc=μ, scale=σ) для усечения значений в диапазон [0, 1]."
        code_label = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label.pack(anchor="w", pady=(0, 15))

        # ПРИМЕР 1: Разные μ при фиксированном σ
        mu_examples = [
            {"mu": 0.3, "sigma": 0.15},
            {"mu": 0.5, "sigma": 0.15},
            {"mu": 0.7, "sigma": 0.15}
        ]

        # Создаем контейнер для первого ряда примеров
        mu_examples_frame = self.widget_factory.create_frame(parent_frame)
        mu_examples_frame.pack(fill="x", pady=(0, 20))

        for i, example in enumerate(mu_examples):
            mu_val = example["mu"]
            sigma_val = example["sigma"]

            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(mu_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))

            # Фрейм для текстов (μ/σ)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ: {mu_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ: {sigma_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))

            # Создаем график используя класс для вершин
            plot_widget = VertexWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")

            # Передаем параметры для нормального распределения
            dist_type = "Normal"
            dist_params = {
                "mu": mu_val,
                "sigma": sigma_val
            }
            plot_widget.update_plot(dist_type, dist_params)

        # ПРИМЕР 2: Разные σ при фиксированном μ
        sigma_examples = [
            {"mu": 0.5, "sigma": 0.1},
            {"mu": 0.5, "sigma": 0.2},
            {"mu": 0.5, "sigma": 0.4}
        ]

        # Создаем контейнер для второго ряда примеров
        sigma_examples_frame = self.widget_factory.create_frame(parent_frame)
        sigma_examples_frame.pack(fill="x", pady=(0, 15))

        for i, example in enumerate(sigma_examples):
            mu_val = example["mu"]
            sigma_val = example["sigma"]

            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(sigma_examples_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))

            # Фрейм для текстов (μ/σ)
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ: {mu_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ: {sigma_val}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(2, 2))

            # Создаем график
            plot_widget = VertexWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")

            # Передаем параметры
            dist_type = "Normal"
            dist_params = {
                "mu": mu_val,
                "sigma": sigma_val
            }
            plot_widget.update_plot(dist_type, dist_params)

        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))

        limits_text = "Диапазон μ: от 0 до 1\nДиапазон σ: от 0.01 до 1\nЗначения усекаются до интервала [0, 1]"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")

    def _create_vertex_lognormal_distribution_info(self, parent_frame):
        """Создает описание логнормального распределения для вершин с примерами"""
        accent_color = self.theme_manager.get_color('accent_color')

        # Заголовок "Логнормальное распределение"
        lognormal_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Логнормальное распределение"
        )
        lognormal_title.pack(anchor="w", pady=(0, 10))

        # Описание логнормального распределения
        lognormal_desc = "Распределение случайной величины, логарифм которой распределен нормально. Параметр γ (гамма) задает сдвиг вправо, μ (мю) — масштаб, σ (сигма) — форму распределения. Позволяет моделировать асимметричные распределения с длинным правым хвостом."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=lognormal_desc,
            wraplength=1000,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 5))

        # Вспомогательный серый текст с информацией о реализации
        code_desc1 = "В коде используется scipy.stats.lognorm с параметрами s=σ, scale=exp(μ)."
        code_label1 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc1,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label1.pack(anchor="w", pady=(0, 2))

        code_desc2 = "Генерация происходит методом обратного преобразования через нормальное распределение с последующим сдвигом на γ и усечением до [0, 1]."
        code_label2 = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc2,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label2.pack(anchor="w", pady=(0, 15))

        # ПРИМЕР 1: Разные γ (сдвиг)
        gamma_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разный сдвиг (γ):"
        )
        gamma_title.pack(anchor="w", pady=(0, 10))

        gamma_examples = [
            {"gamma": 0.0, "mu": -1.0, "sigma": 0.5},
            {"gamma": 0.2, "mu": -1.0, "sigma": 0.5},
            {"gamma": 0.4, "mu": -1.0, "sigma": 0.5}
        ]

        gamma_frame = self.widget_factory.create_frame(parent_frame)
        gamma_frame.pack(fill="x", pady=(0, 20))

        for i, example in enumerate(gamma_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(gamma_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))

            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"γ: {example['gamma']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ: {example['mu']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ: {example['sigma']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            # Создаем график
            plot_widget = VertexWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")

            # Передаем параметры
            dist_type = "Lognormal"
            dist_params = {
                "gamma": example["gamma"],
                "mu": example["mu"],
                "sigma": example["sigma"]
            }
            plot_widget.update_plot(dist_type, dist_params)

        # ПРИМЕР 2: Разные μ (масштаб)
        mu_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разный масштаб (μ):"
        )
        mu_title.pack(anchor="w", pady=(0, 10))

        mu_examples = [
            {"gamma": 0.1, "mu": -2.0, "sigma": 0.5},
            {"gamma": 0.1, "mu": -1.0, "sigma": 0.5},
            {"gamma": 0.1, "mu": 0.0, "sigma": 0.5}
        ]

        mu_frame = self.widget_factory.create_frame(parent_frame)
        mu_frame.pack(fill="x", pady=(0, 20))

        for i, example in enumerate(mu_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(mu_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))

            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"γ: {example['gamma']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ: {example['mu']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ: {example['sigma']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            # Создаем график
            plot_widget = VertexWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")

            # Передаем параметры
            dist_type = "Lognormal"
            dist_params = {
                "gamma": example["gamma"],
                "mu": example["mu"],
                "sigma": example["sigma"]
            }
            plot_widget.update_plot(dist_type, dist_params)

        # ПРИМЕР 3: Разные σ (форма)
        sigma_title = self.widget_factory.create_label_small_bold(
            parent_frame,
            text="Разная форма (σ):"
        )
        sigma_title.pack(anchor="w", pady=(0, 10))

        sigma_examples = [
            {"gamma": 0.1, "mu": -1.0, "sigma": 0.3},
            {"gamma": 0.1, "mu": -1.0, "sigma": 0.7},
            {"gamma": 0.1, "mu": -1.0, "sigma": 1.2}
        ]

        sigma_frame = self.widget_factory.create_frame(parent_frame)
        sigma_frame.pack(fill="x", pady=(0, 15))

        for i, example in enumerate(sigma_examples):
            # Контейнер для одного примера (текст + график)
            example_container = self.widget_factory.create_frame(sigma_frame)
            example_container.pack(side="left", padx=(0, 110 if i < 2 else 0))

            # Фрейм для текстов
            text_frame = self.widget_factory.create_frame(example_container)
            text_frame.pack(side="left", padx=(0, 10))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"γ: {example['gamma']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"μ: {example['mu']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            self.widget_factory.create_label_small(
                text_frame,
                text=f"σ: {example['sigma']}",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(1, 1))

            # Создаем график
            plot_widget = VertexWeightPlotWidget(example_container, self.theme_manager, self.translator)
            plot_widget.pack(side="left")

            # Передаем параметры
            dist_type = "Lognormal"
            dist_params = {
                "gamma": example["gamma"],
                "mu": example["mu"],
                "sigma": example["sigma"]
            }
            plot_widget.update_plot(dist_type, dist_params)

        # Текст с ограничениями
        limits_frame = self.widget_factory.create_frame(parent_frame)
        limits_frame.pack(fill="x", pady=(15, 5))

        limits_text = "Диапазон γ (сдвиг): от 0 до 0.5\nДиапазон μ (масштаб): от -3 до 1\nДиапазон σ (форма): от 0.01 до 2\nЗначения усекаются до интервала [0, 1]"
        limits_label = self.widget_factory.create_label_normal(
            limits_frame,
            text=limits_text,
            wraplength=700,
            justify="left"
        )
        limits_label.pack(anchor="w")

    def _create_vertex_stepwise_distribution_info(self, parent_frame):
        """Заглушка для ступенчатого распределения вершин"""
        accent_color = self.theme_manager.get_color('accent_color')

        # Заголовок "Ступенчатое распределение"
        stepwise_title = self.widget_factory.create_label_h2(
            parent_frame,
            text="Ступенчатое распределение"
        )
        stepwise_title.pack(anchor="w", pady=(0, 10))

        # Описание
        desc_text = "Позволяет вручную задать несколько диапазонов (ступеней) весов и количество вершин в каждом из них. Поддерживаются готовые шаблоны для моделирования различных структур: рыночной, олигополии, пирамидальной и др."
        desc_label = self.widget_factory.create_label_normal(
            parent_frame,
            text=desc_text,
            wraplength=700,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 15))

        # Вспомогательный серый текст
        code_desc = "В коде для каждой ступени генерируется заданное количество вершин с равномерным распределением внутри заданного диапазона."
        code_label = self.widget_factory.create_label_small(
            parent_frame,
            text=code_desc,
            foreground=self.theme_manager.get_color('text_secondary')
        )
        code_label.pack(anchor="w", pady=(0, 15))

        # Сообщение о том, что подробная информация будет добавлена позже
        placeholder_frame = self.widget_factory.create_frame(parent_frame, height=50)
        placeholder_frame.pack(fill="x", pady=10)

        self.widget_factory.create_label_normal(
            placeholder_frame,
            text="Подробное описание и примеры для ступенчатого распределения будут добавлены позже.",
            wraplength=700,
            justify="center",
            foreground=self.theme_manager.get_color('text_secondary')
        ).pack()


# In[15]:


class GraphStatisticsManager:
    """Менеджер для расчета и управления статистиками графа"""
    
    def __init__(self, parent_app):
        self.parent = parent_app
        self.translator = parent_app.translator
        self.t = self.translator.t
        # Хранилище для статистик
        self.edge_stats = {}
        self.vertex_stats = {}
        self.adj_matrix = None
        # Статистика стартовой вершины
        self.start_vertex_stats = {
            'weight': tk.StringVar(value="0.00"),
            'positive_count': tk.StringVar(value="0"),
            'negative_count': tk.StringVar(value="0"),
            'positive_sum': tk.StringVar(value="0.00"),
            'negative_sum': tk.StringVar(value="0.00"),
            'positive_mean': tk.StringVar(value="0.000"),
            'negative_mean': tk.StringVar(value="0.000"),
            'avg_edge_weight': tk.StringVar(value="0.000")
        }
        # Результаты симуляции пожара
        self.fire_results = {
            'total_burned_nodes': tk.StringVar(value="0"),
            'total_iterations': tk.StringVar(value="0"),
            'spread_rate_1': tk.StringVar(value="0"),
            'spread_rate_2': tk.StringVar(value="0"),
            'spread_rate_3': tk.StringVar(value="0"),
            'spread_rate_4': tk.StringVar(value="0"),
            'spread_rate_5': tk.StringVar(value="0"),
            'time_to_peak': tk.StringVar(value="0"),
            'peak_new_burns': tk.StringVar(value="0"),
            'time_from_peak_to_end': tk.StringVar(value="0")
        }
    
    def calculate_graph_statistics(self, graph, node_weights=None):
        """Вычисление полной статистики графа"""
        if graph is None:
            return {}, {}, None
        
        adj_matrix = nx.to_numpy_array(graph)
        n_nodes = adj_matrix.shape[0]
        
        # Статистика ребер
        mask = ~np.eye(n_nodes, dtype=bool)
        edge_weights = adj_matrix[mask]
        self.edge_stats = self._calculate_descriptive_stats(edge_weights, "edges")
        
        # Статистика положительных и отрицательных ребер
        positive_weights = edge_weights[edge_weights > 0]
        negative_weights = edge_weights[edge_weights < 0]
        
        self.edge_stats.update({
            'edges_positive_count': np.sum(edge_weights > 0),
            'edges_negative_count': np.sum(edge_weights < 0),
            'edges_positive_sum': np.sum(positive_weights),
            'edges_negative_sum': np.sum(negative_weights),
            'edges_q95': np.quantile(edge_weights, 0.95) if len(edge_weights) > 0 else 0,
            'edges_q05': np.quantile(edge_weights, 0.05) if len(edge_weights) > 0 else 0,
            'edges_median': np.median(edge_weights) if len(edge_weights) > 0 else 0,
            'edges_positive_mean': np.mean(positive_weights) if len(positive_weights) > 0 else 0,
            'edges_negative_mean': np.mean(negative_weights) if len(negative_weights) > 0 else 0
        })
        
        # Статистика вершин
        self.vertex_stats = {}
        weights_to_use = node_weights if node_weights is not None else self.parent.node_weights
        if weights_to_use:
            vertex_weights = np.array(list(weights_to_use.values()))
            self.vertex_stats = self._calculate_descriptive_stats(vertex_weights, "vertices")
            if len(vertex_weights) > 0:
                self.vertex_stats.update({'vertices_q95': np.quantile(vertex_weights, 0.95), 'vertices_q05': np.quantile(vertex_weights, 0.05),
                                          'vertices_median': np.median(vertex_weights)})
        self.adj_matrix = adj_matrix
        return self.edge_stats, self.vertex_stats, adj_matrix
    
    def _calculate_descriptive_stats(self, data, name):
        """Вычисление основных описательных статистик"""
        if len(data) == 0:
            return {}
        stats_dict = {
            f'{name}_mean': float(np.mean(data)),
            f'{name}_min': float(np.min(data)),
            f'{name}_max': float(np.max(data)),
            f'{name}_median': float(np.median(data)),
            f'{name}_std': float(np.std(data)),
        }
        # Асимметрия и эксцесс
        if len(data) > 1:
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore')
                    stats_dict[f'{name}_skewness'] = float(stats.skew(data, nan_policy='omit'))
                    stats_dict[f'{name}_kurtosis'] = float(stats.kurtosis(data, nan_policy='omit'))
            except:
                stats_dict[f'{name}_skewness'] = 0.0
                stats_dict[f'{name}_kurtosis'] = 0.0
        
        return stats_dict
    
    def update_start_vertex_stats(self, graph, vertex_idx, node_weights=None):
        """Обновляет статистику выбранной стартовой вершины"""
        if graph is None:
            return
        vertex_id = f'V{vertex_idx}'
        if vertex_id not in graph.nodes():
            vertex_id = f'V0'
            self.parent.start_vertex.set(1)
        neighbors = list(graph.neighbors(vertex_id))
        positive_count = 0
        negative_count = 0
        positive_sum = 0.0
        negative_sum = 0.0
        positive_weights = []
        negative_weights = []
        all_weights = []
        for neighbor in neighbors:
            if graph.has_edge(vertex_id, neighbor):
                edge_data = graph.get_edge_data(vertex_id, neighbor)
                if edge_data:
                    weight = edge_data['weight']
                    all_weights.append(weight)
                    
                    if weight > 0:
                        positive_count += 1
                        positive_sum += weight
                        positive_weights.append(weight)
                    elif weight < 0:
                        negative_count += 1
                        negative_sum += weight
                        negative_weights.append(weight)
        
        positive_mean = positive_sum / positive_count if positive_count > 0 else 0.0
        negative_mean = negative_sum / negative_count if negative_count > 0 else 0.0
        avg_weight = sum(all_weights) / len(all_weights) if all_weights else 0.0
        
        weights_to_use = node_weights if node_weights is not None else self.parent.node_weights
        weight = weights_to_use.get(vertex_id, 0.0) if weights_to_use else 0.0
        
        self.start_vertex_stats['weight'].set(f"{weight:.3f}")
        self.start_vertex_stats['avg_edge_weight'].set(f"{avg_weight:.3f}")
        self.start_vertex_stats['positive_count'].set(str(positive_count))
        self.start_vertex_stats['positive_sum'].set(f"{positive_sum:.3f}")
        self.start_vertex_stats['positive_mean'].set(f"{positive_mean:.3f}")
        self.start_vertex_stats['negative_count'].set(str(negative_count))
        self.start_vertex_stats['negative_sum'].set(f"{negative_sum:.3f}")
        self.start_vertex_stats['negative_mean'].set(f"{negative_mean:.3f}")
    
    def calculate_fire_statistics(self, burning_nodes, fire_spread_history, fire_iteration):
        """Вычисляет статистику пожара"""
        if not burning_nodes:
            return
        
        total_burned = len(burning_nodes)
        total_iterations = fire_iteration
        self.fire_results['total_burned_nodes'].set(str(total_burned))
        self.fire_results['total_iterations'].set(str(total_iterations))
        
        # Скорость распространения по первым 5 итерациям
        if fire_spread_history:
            for i in range(1, 6):
                if i < len(fire_spread_history):
                    rate = fire_spread_history[i]
                    self.fire_results[f'spread_rate_{i}'].set(f"{rate}")
                else:
                    self.fire_results[f'spread_rate_{i}'].set("0")
        
        # Пик и время
        if fire_spread_history:
            peak_value = max(fire_spread_history)
            peak_time = fire_spread_history.index(peak_value)
            end_time = len(fire_spread_history) - 1
            self.fire_results['peak_new_burns'].set(str(peak_value))
            self.fire_results['time_to_peak'].set(str(peak_time))
            self.fire_results['time_from_peak_to_end'].set(str(end_time - peak_time))
    
    def reset_fire_statistics(self):
        """Сбрасывает статистику пожара"""
        for key in self.fire_results:
            if key in ['total_burned_nodes', 'total_iterations', 'spread_rate_1', 'spread_rate_2', 'spread_rate_3',
                       'spread_rate_4', 'spread_rate_5', 'time_to_peak', 'peak_new_burns', 'time_from_peak_to_end']:
                self.fire_results[key].set("0")
    
    def get_graph_parameters_summary(self):
        """Формирует строковое представление параметров графа для отображения"""
        params_lines = [
            f"{self.t('vertex_count_stat')}: {self.parent.vertex_count.get()}",
            f"{self.t('edge_count_stat')}: {self.parent.current_graph.number_of_edges() if self.parent.current_graph else 0}",
            f"{self.t('edge_dist_stat')}: {self.parent.edge_distribution.get()}",
            f"{self.t('vertex_dist_stat')}: {self.parent.vertex_distribution.get()}",
        ]
        
        # Устойчивость
        resistance_text = self.parent.vertex_resistance.get()
        resistance_eng = self.translator.get_english_key(resistance_text)
        
        if resistance_eng != 'None':
            params_lines.append(f"{self.t('resistance_stat')}:")
            params_lines.append(f"  {resistance_text}")
            params_lines.append(f"  ({self.t('coeff')} {self.parent.resistance_coeff.get():.2f})")
        else:
            params_lines.append(f"{self.t('resistance_stat')}: {self.t('None')}")
        
        # Влияние
        influence_text = self.parent.vertex_influence.get()
        influence_eng = self.translator.get_english_key(influence_text)
        
        if influence_eng != 'None':
            params_lines.append(f"{self.t('influence_stat')}:")
            params_lines.append(f"  {influence_text}")
            params_lines.append(f"  ({self.t('coeff')} {self.parent.influence_coeff.get():.2f})")
        else:
            params_lines.append(f"{self.t('influence_stat')}: {self.t('None')}")
        
        # Затухание
        damping_text = self.parent.damping_type.get()
        damping_eng = self.translator.get_english_key(damping_text)
        
        if damping_eng != 'None':
            params_lines.append(f"{self.t('damping_stat')}:")
            params_lines.append(f"  {damping_text}")
            params_lines.append(f"  ({self.t('coeff')} {self.parent.damping_value.get():.2f})")
        else:
            params_lines.append(f"{self.t('damping_stat')}: {self.t('None')}")
        
        return params_lines
    
    def format_edge_stats_for_display(self):
        """Форматирует статистику ребер для отображения"""
        if not self.edge_stats:
            return []
        stats_data = [
            (self.t('min_stat'), f"{self.edge_stats['edges_min']:.3f}"),
            (self.t('max_stat'), f"{self.edge_stats['edges_max']:.3f}"),
            (self.t('mean_stat'), f"{self.edge_stats['edges_mean']:.3f}"),
            (self.t('std_stat'), f"{self.edge_stats['edges_std']:.3f}"),
            (self.t('median'), f"{self.edge_stats['edges_median']:.3f}"),
            (self.t('skewness'), f"{self.edge_stats['edges_skewness']:.3f}"),
            (self.t('kurtosis'), f"{self.edge_stats['edges_kurtosis']:.3f}"),
            (self.t('q05'), f"{self.edge_stats['edges_q05']:.3f}"),
            (self.t('q95'), f"{self.edge_stats['edges_q95']:.3f}"),
            ("", ""),
            (self.t('positive_connections'), str(self.edge_stats['edges_positive_count'])),
            (self.t('positive_sum'), f"{self.edge_stats['edges_positive_sum']:.3f}"),
            (self.t('positive_mean'), f"{self.edge_stats['edges_positive_mean']:.3f}"),
            (self.t('negative_connections'), str(self.edge_stats['edges_negative_count'])),
            (self.t('negative_sum'), f"{self.edge_stats['edges_negative_sum']:.3f}"),
            (self.t('negative_mean'), f"{self.edge_stats['edges_negative_mean']:.3f}")
        ]
        return stats_data
    
    def format_vertex_stats_for_display(self):
        """Форматирует статистику вершин для отображения"""
        if not self.vertex_stats:
            return []
        stats_data = [
            (self.t('min_stat'), f"{self.vertex_stats['vertices_min']:.3f}"),
            (self.t('max_stat'), f"{self.vertex_stats['vertices_max']:.3f}"),
            (self.t('mean_stat'), f"{self.vertex_stats['vertices_mean']:.3f}"),
            (self.t('std_stat'), f"{self.vertex_stats['vertices_std']:.3f}"),
            (self.t('median'), f"{self.vertex_stats['vertices_median']:.3f}"),
            (self.t('skewness'), f"{self.vertex_stats['vertices_skewness']:.3f}"),
            (self.t('kurtosis'), f"{self.vertex_stats['vertices_kurtosis']:.3f}"),
            (self.t('q05'), f"{self.vertex_stats['vertices_q05']:.3f}"),
            (self.t('q95'), f"{self.vertex_stats['vertices_q95']:.3f}")
        ]
        return stats_data
    
    def format_start_vertex_stats_for_display(self):
        """Форматирует статистику стартовой вершины для отображения"""
        stats_data = [
            (self.t('vertex_weight'), self.start_vertex_stats['weight']),
            (self.t('avg_edge_weight'), self.start_vertex_stats['avg_edge_weight']),
            ("", tk.StringVar(value="")),
            (self.t('positive_count'), self.start_vertex_stats['positive_count']),
            (self.t('positive_sum'), self.start_vertex_stats['positive_sum']),
            (self.t('positive_mean'), self.start_vertex_stats['positive_mean']),
            ("", tk.StringVar(value="")),
            (self.t('negative_count'), self.start_vertex_stats['negative_count']),
            (self.t('negative_sum'), self.start_vertex_stats['negative_sum']),
            (self.t('negative_mean'), self.start_vertex_stats['negative_mean'])
        ]
        return stats_data
    
    def format_fire_results_for_display(self):
        """Форматирует результаты симуляции пожара для отображения"""
        results_data = [
            (self.t('total_burned'), self.fire_results['total_burned_nodes']),
            (self.t('total_iterations'), self.fire_results['total_iterations']),
            ("", tk.StringVar(value="")),
            (f"{self.t('spread_rate')} 1", self.fire_results['spread_rate_1']),
            (f"{self.t('spread_rate')} 2", self.fire_results['spread_rate_2']),
            (f"{self.t('spread_rate')} 3", self.fire_results['spread_rate_3']),
            (f"{self.t('spread_rate')} 4", self.fire_results['spread_rate_4']),
            (f"{self.t('spread_rate')} 5", self.fire_results['spread_rate_5']),
            ("", tk.StringVar(value="")),
            (self.t('peak_new_burns'), self.fire_results['peak_new_burns']),
            (self.t('time_to_peak'), self.fire_results['time_to_peak']),
            (self.t('time_from_peak'), self.fire_results['time_from_peak_to_end'])
        ]
        return results_data
    
    def reset_all_statistics(self):
        """Сбрасывает все статистики"""
        self.edge_stats = {}
        self.vertex_stats = {}
        self.adj_matrix = None
        # Сброс статистики стартовой вершины
        for key in self.start_vertex_stats:
            if key == 'weight':
                self.start_vertex_stats[key].set("0.00")
            elif key.endswith('count'):
                self.start_vertex_stats[key].set("0")
            else:
                self.start_vertex_stats[key].set("0.000")
        # Сброс статистики пожара
        self.reset_fire_statistics()


# In[16]:


class TabManager:
    """Менеджер для управления вкладками приложения"""
    def __init__(self, parent, theme_manager, translator, widget_factory, parent_app):
        self.parent = parent
        self.theme_manager = theme_manager
        self.translator = translator
        self.t = translator.t
        self.widget_factory = widget_factory
        self.parent_app = parent_app
        
        self.tabs = []
        self.tab_frames = []
        self.active_tab_index = 0
        self.tab_state = {}
        
        # Главный контейнер
        self.main_container = self.widget_factory.create_frame(self.parent)
        self.main_container.pack(fill="both", expand=True)
        # Верхняя панель с вкладками
        self.tab_bar = self.widget_factory.create_frame(self.main_container, height=40)
        self.tab_bar.pack(fill="x", padx=0, pady=0)
        self.tab_bar.pack_propagate(False)
        # Контейнер для содержимого
        self.content_container = self.widget_factory.create_frame(self.main_container)
        self.content_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._create_tabs()
    
    def _create_tabs(self):
        """Создает все вкладки с цветами из темы"""
        tab_keys = [
            'tab_generation',
            'tab_custom',
            'tab_simulation',
            'tab_multiple',
            'tab_help',
            'tab_settings'
        ]
        
        for i, tab_key in enumerate(tab_keys):
            tab_button = self._create_tab_button(self.tab_bar, self.t(tab_key), i)
            tab_button.pack(side="left", padx=(0, 2), pady=5)
            self.tabs.append(tab_button)
            
            tab_frame = self.widget_factory.create_frame(self.content_container)
            self.tab_frames.append(tab_frame)
        
        # Активирует первую вкладку
        self.active_tab_index = 0
        self._update_tab_colors()
        
        # Показывает фрейм первой вкладки
        for i, frame in enumerate(self.tab_frames):
            if i == 0:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()
    
    def _create_tab_button(self, parent, text, index):
        """Создает кнопку вкладки"""
        tab_frame = tk.Frame(parent, bg=self.theme_manager.get_color('tab_border'), bd=0, highlightthickness=0)

        # Внутренний фрейм - цвет вкладки
        inner_frame = self.widget_factory.create_frame(tab_frame)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)
        # Текст вкладки
        button = self.widget_factory.create_label(inner_frame, text=text, font=("Segoe UI", 11, "bold"), padx=20, pady=8, cursor="hand2")
        button.pack(fill="both", expand=True)
        
        # Сохраняем ссылки
        button.index = index
        tab_frame.inner_frame = inner_frame
        tab_frame.button = button
        
        # Привязка событий
        button.bind('<Enter>', lambda e: self._on_tab_enter(index))
        button.bind('<Leave>', lambda e: self._on_tab_leave(index))
        button.bind('<Button-1>', lambda e: self.activate_tab(index))
        inner_frame.bind('<Enter>', lambda e: self._on_tab_enter(index))
        inner_frame.bind('<Leave>', lambda e: self._on_tab_leave(index))
        inner_frame.bind('<Button-1>', lambda e: self.activate_tab(index))
        tab_frame.bind('<Enter>', lambda e: self._on_tab_enter(index))
        tab_frame.bind('<Leave>', lambda e: self._on_tab_leave(index))
        tab_frame.bind('<Button-1>', lambda e: self.activate_tab(index))
        
        return tab_frame
    
    def _on_tab_enter(self, index):
        """Обработчик наведения на вкладку"""
        if index != self.active_tab_index:
            active_color = self.theme_manager.get_color(f'tab{index+1}_active')
            tab = self.tabs[index]
            tab.inner_frame.configure(bg=active_color)
            tab.button.configure(bg=active_color, fg=self.theme_manager.get_color('tab_text_active'))
    
    def _on_tab_leave(self, index):
        """Обработчик ухода мыши с вкладки"""
        if index != self.active_tab_index:
            inactive_color = self.theme_manager.get_color(f'tab{index+1}_inactive')
            tab = self.tabs[index]
            tab.inner_frame.configure(bg=inactive_color)
            tab.button.configure(bg=inactive_color, fg=self.theme_manager.get_color('tab_text_inactive'))
    
    def _update_tab_colors(self):
        """Обновляет цвета всех вкладок"""
        for i, tab in enumerate(self.tabs):
            if i == self.active_tab_index: # Активная вкладка
                active_color = self.theme_manager.get_color(f'tab{i+1}_active')
                tab.inner_frame.configure(bg=active_color)
                tab.button.configure(bg=active_color, fg=self.theme_manager.get_color('tab_text_active'))
            else: # Неактивная вкладка
                inactive_color = self.theme_manager.get_color(f'tab{i+1}_inactive')
                tab.inner_frame.configure(bg=inactive_color)
                tab.button.configure(bg=inactive_color, fg=self.theme_manager.get_color('tab_text_inactive'))
            tab.configure(bg=self.theme_manager.get_color('tab_border'))
    
    def activate_tab(self, index):
        """Активирует вкладку с указанным индексом"""
        if self.active_tab_index == index:
            return
        
        # Сохраняет состояние текущей вкладки
        self._save_tab_state(self.active_tab_index)
        self.active_tab_index = index
        self._update_tab_colors()
        
        # Переключает видимость фреймов
        for i, frame in enumerate(self.tab_frames):
            if i == index:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()
        
        # Восстанавливаем состояние новой вкладки
        self._restore_tab_state(index)
    
    def _save_tab_state(self, index):
        """Сохраняет состояние вкладки"""
        if index == 2 and hasattr(self.parent_app, 'current_graph'):
            self.tab_state['simulation_graph'] = self.parent_app.current_graph
            self.tab_state['simulation_node_weights'] = self.parent_app.node_weights
            if hasattr(self.parent_app, 'burning_nodes'):
                self.tab_state['simulation_burning_nodes'] = self.parent_app.burning_nodes.copy()
            if hasattr(self.parent_app, 'burned_edges'):
                self.tab_state['simulation_burned_edges'] = self.parent_app.burned_edges.copy()
    
    def _restore_tab_state(self, index):
        """Восстанавливает состояние вкладки"""
        if index == 2 and 'simulation_graph' in self.tab_state:
            self.parent_app.current_graph = self.tab_state['simulation_graph']
            self.parent_app.node_weights = self.tab_state['simulation_node_weights']
            if 'simulation_burning_nodes' in self.tab_state:
                self.parent_app.burning_nodes = self.tab_state['simulation_burning_nodes'].copy()
            if 'simulation_burned_edges' in self.tab_state:
                self.parent_app.burned_edges = self.tab_state['simulation_burned_edges'].copy()
            self.parent_app._build_simulation_tab_content()
    
    def get_tab_frame(self, index):
        """Возвращает фрейм содержимого вкладки"""
        return self.tab_frames[index]
    
    def clear_simulation_state(self):
        """Очищает сохраненное состояние симуляции"""
        keys = ['simulation_graph', 'simulation_node_weights', 'simulation_burning_nodes', 'simulation_burned_edges']
        for key in keys:
            if key in self.tab_state:
                del self.tab_state[key]


# In[17]:


class DistributionManager:
    """Менеджер распределений для генерации графов и весов"""
    def __init__(self, app_instance=None):
        self.app = app_instance
        if app_instance:
            self.t = app_instance.t
            self.translator = app_instance.translator
            self.translations = app_instance.translations

# Ребра    
    def create_graph_uniform(self, n_nodes, min_corr, max_corr):
        """Граф с равномерным распределением корреляций"""
        matrix = np.triu(np.random.uniform(min_corr, max_corr, (n_nodes, n_nodes)))
        matrix += np.triu(matrix, 1).T
        np.fill_diagonal(matrix, 0)
        G = nx.Graph()
        for i in range(n_nodes):
            G.add_node(f'V{i}')
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                G.add_edge(f'V{i}', f'V{j}', weight=matrix[i, j])
        return G
    
    def create_graph_normal(self, n_nodes, mu, sigma):
        """Граф с усеченным нормальным распределением"""
        a, b = (-1 - mu) / sigma, (1 - mu) / sigma
        correlations = truncnorm.rvs(a, b, loc=mu, scale=sigma, size=(n_nodes, n_nodes))
        matrix = np.triu(correlations) + np.triu(correlations, 1).T
        np.fill_diagonal(matrix, 0)
        G = nx.Graph()
        for i in range(n_nodes):
            G.add_node(f'V{i}')
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                G.add_edge(f'V{i}', f'V{j}', weight=matrix[i, j])
        return G
    
    def create_graph_student(self, n_nodes, df, scale):
        """Граф с распределением Стьюдента"""
        correlations = np.zeros((n_nodes, n_nodes))
        total = n_nodes * n_nodes
        generated = 0
        while generated < total:
            samples = stats_t.rvs(df, scale=scale, size=total*2)
            valid = samples[(samples >= -1) & (samples <= 1)]
            if len(valid) > 0:
                need = total - generated
                take = min(len(valid), need)
                correlations.flat[generated:generated+take] = valid[:take]
                generated += take
        matrix = np.triu(correlations) + np.triu(correlations, 1).T
        np.fill_diagonal(matrix, 0)
        G = nx.Graph()
        for i in range(n_nodes):
            G.add_node(f'V{i}')
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                G.add_edge(f'V{i}', f'V{j}', weight=matrix[i, j])
        return G
    
    def create_graph_laplace(self, n_nodes, loc, scale):
        """Граф с распределением Лапласа"""
        correlations = np.zeros((n_nodes, n_nodes))
        total = n_nodes * n_nodes
        generated = 0
        while generated < total:
            samples = laplace.rvs(loc=loc, scale=scale, size=total*2)
            valid = samples[(samples >= -1) & (samples <= 1)]
            if len(valid) > 0:
                need = total - generated
                take = min(len(valid), need)
                correlations.flat[generated:generated+take] = valid[:take]
                generated += take
        matrix = np.triu(correlations) + np.triu(correlations, 1).T
        np.fill_diagonal(matrix, 0)
        G = nx.Graph()
        for i in range(n_nodes):
            G.add_node(f'V{i}')
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                G.add_edge(f'V{i}', f'V{j}', weight=matrix[i, j])
        return G
    
    def create_graph_bimodal(self, n_nodes, mu1, sigma1, mu2, sigma2, weight1):
        """Граф с бимодальным распределением"""
        size = (n_nodes, n_nodes)
        part1 = truncnorm.rvs((-1 - mu1)/sigma1, (1 - mu1)/sigma1, loc=mu1, scale=sigma1, size=size)
        part2 = truncnorm.rvs((-1 - mu2)/sigma2, (1 - mu2)/sigma2, loc=mu2, scale=sigma2, size=size)
        mask = np.random.random(size) < weight1
        correlations = np.where(mask, part1, part2)
        matrix = np.triu(correlations) + np.triu(correlations, 1).T
        np.fill_diagonal(matrix, 0)
        G = nx.Graph()
        for i in range(n_nodes):
            G.add_node(f'V{i}')
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                G.add_edge(f'V{i}', f'V{j}', weight=matrix[i, j])
        return G
    
    def create_graph_skewed_t(self, n_nodes, df, shape, scale):
        """Граф со скошенным распределением Стьюдента"""
        correlations = np.zeros((n_nodes, n_nodes))
        total = n_nodes * n_nodes
        generated = 0
        while generated < total:
            samples = nct.rvs(df, shape, scale=scale, size=total*2)
            valid = samples[(samples >= -1) & (samples <= 1)]
            if len(valid) > 0:
                need = total - generated
                take = min(len(valid), need)
                correlations.flat[generated:generated+take] = valid[:take]
                generated += take
        matrix = np.triu(correlations) + np.triu(correlations, 1).T
        np.fill_diagonal(matrix, 0)
        G = nx.Graph()
        for i in range(n_nodes):
            G.add_node(f'V{i}')
        for i in range(n_nodes):
            for j in range(i+1, n_nodes):
                G.add_edge(f'V{i}', f'V{j}', weight=matrix[i, j])
        return G
    
    def create_graph_stepwise(self, n_nodes, stages_config):
        """Создание графа со ступенчатым распределением весов ребер"""
        G = nx.complete_graph(n_nodes)
        mapping = {i: f'V{i}' for i in range(n_nodes)}
        G = nx.relabel_nodes(G, mapping)
        total_edges = G.number_of_edges()
        total_weight = sum(max(0.0, stage['weight']) for stage in stages_config)
        if total_weight <= 0:
            print(f"Ошибка: сумма весов ступеней <= 0 ({total_weight})")
            return nx.Graph()
        edges = list(G.edges())
        random.shuffle(edges)
        edge_index = 0
        for stage in stages_config:
            left = float(stage['left'])
            right = float(stage['right'])
            weight = float(stage['weight'])
            left = max(-1.0, min(1.0, left))
            right = max(-1.0, min(1.0, right))
            if right <= left:
                right = min(1.0, left + 0.1)
            n_edges_in_stage = int(round(total_edges * (weight / total_weight)))
            for j in range(n_edges_in_stage):
                if edge_index < len(edges):
                    u, v = edges[edge_index]
                    edge_weight = np.random.uniform(left, right)
                    G[u][v]['weight'] = float(edge_weight)
                    edge_index += 1
        while edge_index < len(edges):
            u, v = edges[edge_index]
            G[u][v]['weight'] = float(np.random.uniform(-1.0, 1.0))
            edge_index += 1
        return G
    

# Веса вершин    
    def generate_weights_uniform(self, min_val, max_val):
        """Генерация весов из равномерного распределения"""
        def uniform_weights(n_nodes):
            if min_val >= max_val:
                raise ValueError("min должен быть меньше max")
            else:
                weights = np.random.uniform(min_val, max_val, n_nodes)
            return np.clip(weights, 0.0, 1.0).tolist()
        return uniform_weights
    
    def generate_weights_normal(self, mean, std):
        """Генерация весов из усеченного нормального распределения"""
        def normal_weights(n_nodes):
            if std <= 0:
                raise ValueError(f"Стандартное отклонение должно быть положительным, получено: {std}")
            a, b = (0 - mean) / std, (1 - mean) / std
            weights = truncnorm.rvs(a, b, loc=mean, scale=std, size=n_nodes)
            return np.clip(weights, 0.0, 1.0).tolist()
        return normal_weights
    
    def generate_weights_lognormal(self, gamma, mu, sigma):
        """Генерация весов из усеченного логнормального распределения"""
        def lognormal_weights(n_nodes):
            gamma_safe = max(0.0, min(0.5, gamma))
            mu_safe = max(-3.0, min(1.0, mu))
            sigma_safe = max(0.1, min(2.0, sigma))
            if gamma_safe > 0.9:
                gamma_safe = 0.9
            if n_nodes == 0:
                return []
            u = np.random.uniform(0, 1, n_nodes)
            a = gamma_safe
            b = 1.0
            dist = lognorm(s=sigma_safe, scale=np.exp(mu_safe))
            actual_b = b - gamma_safe
            if actual_b <= 0:
                return [gamma_safe] * n_nodes
            cdf_a = 0.0
            cdf_b = dist.cdf(actual_b)
            u_scaled = cdf_a + u * (cdf_b - cdf_a)
            norm_ppf = norm.ppf(u_scaled)
            norm_ppf = np.clip(norm_ppf, -10, 10)
            lognormal_samples = np.exp(mu_safe + sigma_safe * norm_ppf)
            shifted_samples = gamma_safe + lognormal_samples
            final_samples = np.clip(shifted_samples, 0.0, 1.0)
            return final_samples.tolist()
        return lognormal_weights
    
    def generate_weights_stepwise(self, stages_config, weight_range='vertex'):
        """Генерация весов со ступенчатым распределением"""
        def stepwise_weights(n_nodes):
            if not stages_config:
                if weight_range == 'edge':
                    return list(np.random.uniform(-1, 1, n_nodes))
                else:
                    return list(np.random.uniform(0, 1, n_nodes))
            
            total_config_vertices = sum(stage['count'] for stage in stages_config)
            if total_config_vertices <= 0:
                print(f"Ошибка: сумма количества вершин в ступенях <= 0 ({total_config_vertices})")
                if weight_range == 'edge':
                    return list(np.random.uniform(-1, 1, n_nodes))
                else:
                    return list(np.random.uniform(0, 1, n_nodes))
            
            weights = []
            remaining_nodes = n_nodes
            for i, stage in enumerate(stages_config):
                count = stage['count']
                proportion = count / total_config_vertices
                stage_node_count = int(round(proportion * n_nodes))
                if i == len(stages_config) - 1:
                    stage_node_count = remaining_nodes
                if stage_node_count > 0:
                    if weight_range == 'edge':
                        min_val, max_val = -1.0, 1.0
                    else:
                        min_val, max_val = 0.0, 1.0
                    
                    left = max(min_val, min(max_val, stage['left']))
                    right = max(min_val, min(max_val, stage['right']))
                    if right <= left:
                        right = min(max_val, left + 0.1)
                    
                    stage_weights = np.random.uniform(left, right, stage_node_count)
                    weights.extend(list(stage_weights))
                    remaining_nodes -= stage_node_count
            
            if remaining_nodes > 0 and stages_config:
                last_stage = stages_config[-1]
                if weight_range == 'edge':
                    min_val, max_val = -1.0, 1.0
                else:
                    min_val, max_val = 0.0, 1.0
                left = max(min_val, min(max_val, last_stage['left']))
                right = max(min_val, min(max_val, last_stage['right']))
                if right <= left:
                    right = min(max_val, left + 0.1)
                extra_weights = np.random.uniform(left, right, remaining_nodes)
                weights.extend(list(extra_weights))
            
            weights = weights[:n_nodes]
            if weight_range == 'edge':
                return np.clip(weights, -1.0, 1.0).tolist()
            else:
                return np.clip(weights, 0.0, 1.0).tolist()
        
        return stepwise_weights
    

# Итоговое создание графа    
    def create_graph_with_weights(self, n_nodes, edge_params, vertex_weight_func=None):
        """Создание графа с весами вершин"""
        edge_type = edge_params["type"]
        graph_creators = {
            "Uniform": lambda: self.create_graph_uniform(
                n_nodes, 
                edge_params["min"], 
                edge_params["max"]
            ),
            "Normal": lambda: self.create_graph_normal(
                n_nodes,
                edge_params["mu"],
                edge_params["sigma"]
            ),
            "Student": lambda: self.create_graph_student(
                n_nodes,
                edge_params["df"],
                edge_params["scale"]
            ),
            "Laplace": lambda: self.create_graph_laplace(
                n_nodes,
                edge_params["loc"],
                edge_params["scale"]
            ),
            "Bimodal": lambda: self.create_graph_bimodal(
                n_nodes,
                edge_params["mu1"],
                edge_params["sigma1"],
                edge_params["mu2"],
                edge_params["sigma2"],
                edge_params["weight1"]
            ),
            "Skewed_t": lambda: self.create_graph_skewed_t(
                n_nodes,
                edge_params["df"],
                edge_params["shape"],
                edge_params["scale"]
            ),
            "Stepwise": lambda: self.create_graph_stepwise(
                n_nodes,
                edge_params["stages_config"]
            )
        }
        
        if edge_type in graph_creators:
            G = graph_creators[edge_type]()
        else:
            raise ValueError(f"Неизвестный тип распределения ребер: {edge_type}")
        
        node_weights = {}
        if vertex_weight_func is not None:
            try:
                weights_list = vertex_weight_func(n_nodes)
                if isinstance(weights_list, (list, np.ndarray)) and len(weights_list) == n_nodes:
                    for i in range(n_nodes):
                        weight = float(weights_list[i])
                        weight = max(0.0, min(1.0, weight))
                        G.nodes[f'V{i}']['weight'] = weight
                        node_weights[f'V{i}'] = weight
            except Exception as e:
                print(f"Ошибка при применении весов вершин: {e}")
                for i in range(n_nodes):
                    G.nodes[f'V{i}']['weight'] = 1.0
                    node_weights[f'V{i}'] = 1.0
        else:
            for i in range(n_nodes):
                G.nodes[f'V{i}']['weight'] = 1.0
                node_weights[f'V{i}'] = 1.0
        
        return G, node_weights
    

# Методы    
    def get_edge_distribution_params(self, dist_name):
        """Возвращает параметры распределения ребер из GUI переменных"""
        if not self.app:
            return {"type": dist_name}
        dist_name = self.translator.get_english_key(dist_name)
        params = {"type": dist_name}
        if dist_name == "Uniform":
            params.update({
                "min": self.app.edge_min.get(),
                "max": self.app.edge_max.get()
            })
        elif dist_name == "Normal":
            params.update({
                "mu": self.app.edge_mean.get(),
                "sigma": self.app.edge_std.get()
            })
        elif dist_name == "Student":
            params.update({
                "df": self.app.student_df.get(),
                "scale": self.app.student_scale.get()
            })
        elif dist_name == "Laplace":
            params.update({
                "loc": self.app.laplace_loc.get(),
                "scale": self.app.laplace_scale.get()
            })
        elif dist_name == "Bimodal":
            params.update({
                "mu1": self.app.bimodal_mu1.get(),
                "sigma1": self.app.bimodal_sigma1.get(),
                "mu2": self.app.bimodal_mu2.get(),
                "sigma2": self.app.bimodal_sigma2.get(),
                "weight1": self.app.bimodal_weight.get()
            })
        elif dist_name == "Skewed_t":
            params.update({
                "df": self.app.skewed_df.get(),
                "shape": self.app.skewed_shape.get(),
                "scale": self.app.skewed_scale.get()
            })
        elif dist_name == "Stepwise": 
            stages_config = []
            for i in range(len(self.app.edge_tier_left_bounds)):
                left = max(-1.0, min(1.0, self.app.edge_tier_left_bounds[i].get()))
                right = max(-1.0, min(1.0, self.app.edge_tier_right_bounds[i].get()))
                if right <= left:
                    right = left + 0.1 if left + 0.1 <= 1.0 else 1.0
                
                edge_count = max(1.0, self.app.edge_tier_weights[i].get())
                stage_config = {
                    'left': left,
                    'right': right,
                    'count': float(edge_count),
                    'weight': float(edge_count)
                }
                stages_config.append(stage_config)
            params.update({"stages_config": stages_config})
        
        return params
    
    def get_vertex_weight_func(self, dist_name, n_nodes):
        """Возвращает функцию для генерации весов вершин"""
        if not self.app:
            return None
        
        dist_eng = self.translator.get_english_key(dist_name)
        
        if dist_eng == "None":
            return None
        
        elif dist_eng == "Uniform":
            min_val = self.app.vertex_min.get()
            max_val = self.app.vertex_max.get()
            return self.generate_weights_uniform(min_val, max_val)
        
        elif dist_eng == "Normal":
            mean = self.app.vertex_mean.get()
            std = self.app.vertex_std.get()
            return self.generate_weights_normal(mean, std)
        
        elif dist_eng == "Lognormal":
            gamma = self.app.lognormal_gamma.get()
            mu = self.app.lognormal_mu.get()
            sigma = self.app.lognormal_sigma.get()
            return self.generate_weights_lognormal(gamma, mu, sigma)
        
        elif dist_eng == "Stepwise":
            stages_config = []
            for i in range(len(self.app.tier_left_bounds)):
                left = max(0.0, min(1.0, self.app.tier_left_bounds[i].get()))
                right = max(0.0, min(1.0, self.app.tier_right_bounds[i].get()))
                if right <= left:
                    right = left + 0.1 if left + 0.1 <= 1.0 else 1.0
                vertex_count = max(1.0, self.app.tier_weights[i].get())
                stage_config = {
                    'left': left,
                    'right': right,
                    'count': float(vertex_count),
                    'weight': float(vertex_count)
                }
                stages_config.append(stage_config)
            return self.generate_weights_stepwise(stages_config, weight_range='vertex')
        
        return None


# In[18]:


class SplashScreen:
    """Экран загрузки приложения"""
    def __init__(self, root):
        self.splash = tk.Toplevel(root)
        self.splash.title("Graph Fire")
        self.splash.geometry("600x400")
        self.splash.overrideredirect(True)
        # Параметры позиционирования текста
        self.title_offset_x = 40
        self.title_offset_y = -20
        # Центрирование окна
        self._center_window()
        # Настройка внешнего вида окна
        self.splash.configure(bg='#cccccc')
        self.splash.attributes('-alpha', 0.99)
        # Цветовая схема
        self.bg_color = "#FFFFFF"
        self.accent_color = "#3b6ea5"
        self.text_color = "#2c3e50"
        self.light_gray = "#dde1e3"
        self.medium_gray = "#6c757d"
        self.dark_gray = "#1E2939"
        # Создание canvas
        self.canvas = tk.Canvas(self.splash, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=1, pady=1)
        # Отрисовка интерфейса
        self._draw_interface()
        self.splash.update()

    def _center_window(self):
        """Центрирование окна на экране"""
        self.splash.update_idletasks()
        width = self.splash.winfo_width()
        height = self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() - width) // 2
        y = (self.splash.winfo_screenheight() - height) // 2
        self.splash.geometry(f'{width}x{height}+{x}+{y}')

    def _draw_interface(self):
        """Отрисовка всего интерфейса splash screen"""
        width, height = 600, 400
        top_height = int(height * 0.55)
        self._draw_text_section(width, top_height) # Левая часть - текст
        self._draw_logo_section(width, top_height) # Правая часть - логотип
        self.canvas.create_line(40, top_height - 10, width - 40, top_height - 10, fill="#d5d5d5", width=1)# Разделительная линия
        self.canvas.create_text(width // 2, height // 2 + 130, text="Loading...", font=("Segoe UI", 11), fill=self.medium_gray) # Текст "Loading..."
        self._draw_progress_indicator() # Граф-индикатор прогресса

    def _draw_text_section(self, width, top_height):
        """Отрисовка текстовой секции с заголовком и версией"""
        text_x = self.title_offset_x
        text_y = top_height // 2 + self.title_offset_y
        # Заголовок приложения
        self.canvas.create_text(text_x, text_y, text="Graph Fire", font=("Segoe UI", 36, "bold"), fill=self.accent_color, anchor="w")
        # Версия приложения
        self.canvas.create_text(text_x, text_y + 70, text="Version 1.0", font=("Segoe UI", 12), fill=self.dark_gray, anchor="w")

    def _draw_logo_section(self, width, top_height):
        """Отрисовка логотипа"""
        logo_x, logo_y = int(width * 0.65) - 20, top_height // 2
        try:
            logo_path = "logo_graph_fire.png"
            if os.path.exists(logo_path):
                self.logo_img = tk.PhotoImage(file=logo_path)
                self.canvas.create_image(logo_x + 80, logo_y, image=self.logo_img, anchor="center")
            else:
                self._draw_fallback_logo(logo_x, logo_y)
        except Exception:
            self._draw_fallback_logo(logo_x, logo_y)

    def _draw_fallback_logo(self, x, y):
        """Отрисовка запасного логотипа"""
        circle_size = 120
        self.canvas.create_oval(x + 21, y - circle_size//2 + 1, x + 21 + circle_size, y + circle_size//2 + 1, fill="#e0e0e0", outline="#e0e0e0")
        self.canvas.create_oval(x + 20, y - circle_size//2, x + 20 + circle_size, y + circle_size//2, fill=self.accent_color, outline=self.accent_color)
        self.canvas.create_text(x + 20 + circle_size//2, y, text="G", font=("Segoe UI", 48, "bold"), fill=self.bg_color)

    def _draw_progress_indicator(self):
        """Отрисовка индикатора прогресса в виде графа"""
        width, height = 600, 400
        self.vertex_count = 10
        self.vertices = []
        self.vertex_texts = []
        self.edges = []
        # Параметры для расположения вершин
        start_x = 100
        end_x = width - 100
        y_pos = height // 2 + 70
        radius = 16
        # Расчет промежутков между вершинами
        if self.vertex_count > 1:
            spacing = (end_x - start_x - 2 * radius * self.vertex_count) / (self.vertex_count - 1)
        else:
            spacing = 0
        # Создание вершин и ребер
        for i in range(self.vertex_count):
            x = start_x + i * (2 * radius + spacing) + radius
            # Ребро между вершинами
            if i < self.vertex_count - 1:
                next_x = start_x + (i + 1) * (2 * radius + spacing) + radius
                edge = self.canvas.create_line(x + radius, y_pos, next_x - radius, y_pos, fill=self.medium_gray, width=1.5, capstyle='round')
                self.edges.append(edge)
            # Тень для вершины
            self.canvas.create_oval(x - radius + 1, y_pos - radius + 1, x + radius + 1, y_pos + radius + 1, fill="#e8e8e8", outline="#e8e8e8")
            # Основная вершина
            vertex = self.canvas.create_oval(x - radius, y_pos - radius, x + radius, y_pos + radius, fill=self.light_gray, outline=self.medium_gray,width=1)
            # Номер вершины
            text = self.canvas.create_text(x, y_pos, text=str(i + 1), font=("Segoe UI", 11, "bold"), fill="#95a5a6")
            self.vertices.append(vertex)
            self.vertex_texts.append(text)
        # Текущий шаг прогресса
        self.current_step = 0
        self.splash.update()

    def update_progress(self, step):
        """Обновление индикатора прогресса"""
        if 0 <= step <= self.vertex_count:
            for i in range(self.vertex_count):
                if i < step:
                    self._activate_element(i)
                else:
                    self._deactivate_element(i)
            self.current_step = step
            self.splash.update()

    def _activate_element(self, index):
        """Активация элемента прогресса"""
        self.canvas.itemconfig(self.vertices[index], fill=self.accent_color, outline=self.accent_color, width=1)
        self.canvas.itemconfig(self.vertex_texts[index], fill="#ffffff")
        if index > 0 and index - 1 < len(self.edges):
            self.canvas.itemconfig(self.edges[index-1], fill=self.accent_color, width=2)

    def _deactivate_element(self, index):
        """Деактивация элемента прогресса"""
        self.canvas.itemconfig(self.vertices[index], fill=self.light_gray, outline=self.medium_gray, width=1)
        self.canvas.itemconfig(self.vertex_texts[index], fill="#95a5a6")
        if index > 0 and index - 1 < len(self.edges) and index >= self.current_step:
            self.canvas.itemconfig(self.edges[index-1], fill=self.medium_gray, width=1.5)

    def close(self):
        """Плавное закрытие splash screen"""
        for alpha in range(99, 0, -5):
            try:
                self.splash.attributes('-alpha', alpha/100)
                self.splash.update()
                self.splash.update_idletasks()
                self.splash.after(20)
            except:
                break
        self.splash.destroy()


# In[19]:


class GraphBuilderApp:
    """Основной класс приложения"""
    def __init__(self, root):
        self.translator = Translator('en')
        self._updating_ui = False
        self.t = self.translator.t
        self.translations = TRANSLATIONS
        
        # Настройка главного окна
        self.root = root
        self.root.title("Graph Fire | version 1.0")
        
        # Загрузка иконки
        try:
            self.icon = tk.PhotoImage(file="logo_graph_fire.png")
            self.root.iconphoto(True, self.icon)
        except Exception as e:
            print(f"Не удалось загрузить иконку: {e}")
        self.root.state('zoomed')
        
        # Настройка стиля для ttk
        style = ttk.Style()
        style.theme_use("clam")
        # Тема и цвета
        self.theme_manager = ThemeManager('light')
        self.colors = self.theme_manager.colors
        self.root.configure(bg=self.theme_manager.get_color('bg_color'))
        # Инициализация фабрики виджетов с менеджером тем
        self.widget_factory = WidgetFactory(self.theme_manager)
        
        self.bg_color = self.theme_manager.get_color('bg_color')
        self.frame_bg = self.theme_manager.get_color('frame_bg')
        self.accent_color = self.theme_manager.get_color('accent_color')
        self.btn_color = self.theme_manager.get_color('btn_color')
        self.btn_hover = self.theme_manager.get_color('btn_hover')
        self.fire_start_color = self.theme_manager.get_color('fire_start')
        self.fire_hover_color = self.theme_manager.get_color('fire_hover')
        self.reset_color = self.theme_manager.get_color('reset_color')
        self.reset_hover_color = self.theme_manager.get_color('reset_hover')
        self.new_graph_color = self.theme_manager.get_color('new_graph_color')
        self.new_graph_hover_color = self.theme_manager.get_color('new_graph_hover')
        
        # Инициализация менеджеров
        self.dist_manager = DistributionManager(self)
        self.stats_manager = GraphStatisticsManager(self)
        
        # Менеджер вкладок
        self.tab_manager = TabManager(self.root, self.theme_manager, self.translator, self.widget_factory, self)
        self.root.update_idletasks()
        
        # Фреймы вкладок
        self.generation_tab = self.tab_manager.get_tab_frame(0)
        self.custom_tab = self.tab_manager.get_tab_frame(1)
        self.simulation_tab = self.tab_manager.get_tab_frame(2)
        self.multiple_tab = self.tab_manager.get_tab_frame(3)
        self.help_tab = self.tab_manager.get_tab_frame(4)
        self.settings_tab = self.tab_manager.get_tab_frame(5)
        
        # Флаг для отслеживания первого посещения вкладки симуляции
        self.simulation_tab_first_visit = True
        
        # Переменные параметров графа
        self.vertex_count = tk.IntVar(value=50)
        
        self.edge_distribution = tk.StringVar(value=self.t('Uniform'))
        self.vertex_distribution = tk.StringVar(value=self.t('None'))
        
        self.vertex_resistance = tk.StringVar(value=self.t('None'))
        self.vertex_influence = tk.StringVar(value=self.t('None'))   
        self.damping_type = tk.StringVar(value=self.t('damping_none'))
        
        self.damping_value = tk.DoubleVar(value=0.5)
        self.resistance_coeff = tk.DoubleVar(value=0.5)
        self.influence_coeff = tk.DoubleVar(value=0.5)

        self.edge_min = tk.DoubleVar(value=0.0)
        self.edge_max = tk.DoubleVar(value=1.0)
        self.edge_mean = tk.DoubleVar(value=0.3)
        self.edge_std = tk.DoubleVar(value=0.5)
        
        self.student_df = tk.DoubleVar(value=10.0)
        self.student_scale = tk.DoubleVar(value=0.5)
        
        self.laplace_loc = tk.DoubleVar(value=0.0)
        self.laplace_scale = tk.DoubleVar(value=0.5)
        
        self.bimodal_mu1 = tk.DoubleVar(value=-0.5)
        self.bimodal_sigma1 = tk.DoubleVar(value=0.3)
        self.bimodal_mu2 = tk.DoubleVar(value=0.5)
        self.bimodal_sigma2 = tk.DoubleVar(value=0.3)
        self.bimodal_weight = tk.DoubleVar(value=0.5)
        
        self.skewed_df = tk.DoubleVar(value=10.0)
        self.skewed_shape = tk.DoubleVar(value=0.0)
        self.skewed_scale = tk.DoubleVar(value=0.5)
        
        self.vertex_min = tk.DoubleVar(value=0.0)
        self.vertex_max = tk.DoubleVar(value=1.0)
        self.vertex_mean = tk.DoubleVar(value=0.5)
        self.vertex_std = tk.DoubleVar(value=0.2)
        
        self.lognormal_gamma = tk.DoubleVar(value=0.0)
        self.lognormal_mu = tk.DoubleVar(value=-1.0)
        self.lognormal_sigma = tk.DoubleVar(value=0.5)

        self.tier_n_stages = tk.IntVar(value=3)
        self.edge_tier_n_stages = tk.IntVar(value=3)
        
        # Инициализация списков для виджетов вершин
        self.tier_left_entries = []
        self.tier_left_sliders = []
        self.tier_right_entries = []
        self.tier_right_sliders = []
        self.tier_weight_sliders = []
        self.tier_plot_pending_flags = []
        self.tier_trace_ids = []
        # Инициализация списков для виджетов ребер
        self.edge_tier_left_entries = []
        self.edge_tier_left_sliders = []
        self.edge_tier_right_entries = []
        self.edge_tier_right_sliders = []
        self.edge_tier_weight_sliders = []
        self.edge_tier_trace_ids = []
        # Инициализация переменных ступеней
        self.initialize_tier_variables()
        self.initialize_edge_tier_variables()
        
        self.current_graph = None
        self.node_weights = {}
        self.normalized_weights = {}

        # надо как-то считать вероятности !!!!!!!!
        self.probability_functions = {
            "Новый метод": self.calculate_probability
        }
        
        # Ссылки на виджеты
        self.resistance_combobox = None
        self.influence_combobox = None
        self.props_frame = None
        
        self.saved_state = None
        self._params_built = False
        
        # Переменные для симуляции
        self.start_vertex = tk.IntVar(value=1)
        self.burning_nodes = {}
        self.burned_edges = {}
        self.fire_iteration = 0
        self.max_fire_iteration = 0
        self.is_fire_running = False
        self.fire_spread_history = []
        
        # Кэш для графа
        self._last_graph = None
        self._graph_positions_cache = None
        self.show_negative_edges = True
        
        # Ссылки на виджеты
        self.canvas = None
        self.scrollbar = None
        self.scrollable_frame = None
        self.canvas_window = None
        self.edge_combobox = None
        self.vertex_combobox = None
        self.damping_combobox = None
        
        # Настройки приложения
        self.settings_language = tk.StringVar(value='EN')
        self.settings_theme = tk.StringVar(value=self.t('theme_light'))
        self.settings_seed_mode = tk.StringVar(value=self.t('settings_seed_random'))
        self.settings_seed_value = tk.IntVar(value=42)
        self.settings_layout_iterations = tk.IntVar(value=200)
        self.settings_show_negative = tk.BooleanVar(value=True)
        
        # Параметры компоновки
        self.layout_iterations = self.settings_layout_iterations.get()
        
        # Seed
        self.layout_seed = self.settings_seed_value.get()
        random.seed(self.layout_seed)
        np.random.seed(self.layout_seed)
        
        # Флаги
        self._updating_language = False
        
        # Ссылки на комбобоксы
        self._edge_combobox = None
        self._vertex_combobox = None
        self._resistance_combobox = None
        self._influence_combobox = None
        self._damping_combobox = None
        self._seed_mode_combobox = None
        self._theme_combobox = None
        self._lang_combobox = None
        
        # Построение вкладок
        self._build_generation_tab()
        self._build_simulation_tab_empty()
        self._build_custom_tab()
        self._build_multiple_tab()
        self._build_help_tab()
        self._build_settings_tab()

        
    def _build_generation_tab(self):
        """Строит интерфейс вкладки генерации графа"""
        for widget in self.generation_tab.winfo_children():
            widget.destroy()
        # Canvas с прокруткой
        self.canvas = self.widget_factory.create_canvas(self.generation_tab, bg=self.theme_manager.get_color('bg_color'), highlightthickness=0)
        self.scrollbar = self.widget_factory.create_scrollbar(self.generation_tab, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = self.widget_factory.create_frame(self.canvas, bd=0, relief="flat")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.focus_set()
        # Интерфейс параметров в scrollable_frame
        self._build_generation_content(self.scrollable_frame)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _build_generation_content(self, parent_frame):
        """Строит содержимое вкладки генерации"""
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        main_container = self.widget_factory.create_frame(parent_frame, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)
        
        # Количество вершин
        vertex_count_frame = self.widget_factory.create_label_frame(main_container, text=self.t('vertex_count'))
        vertex_count_frame.pack(fill="x", pady=(0, 40))
        
        vertex_count_content = self.widget_factory.create_frame(vertex_count_frame)
        vertex_count_content.pack(fill="x", padx=10, pady=10)
        
        vertex_count_row = self.widget_factory.create_frame(vertex_count_content)
        vertex_count_row.pack(fill="x")
        
        self.vertex_entry = self.widget_factory.create_entry(vertex_count_row, width=6, font=("Segoe UI", 9))
        self.vertex_entry.pack(side="left", padx=(0, 15))
        self.vertex_entry.insert(0, str(self.vertex_count.get()))
        
        self.vertex_slider = self.widget_factory.create_slider(vertex_count_row, from_=10, to=100, resolution=1,
                                                               variable=self.vertex_count, length=400)
        self.vertex_slider.pack(side="left")
        
        def update_vertex_from_entry(event=None):
            try:
                value = int(self.vertex_entry.get())
                value = max(10, min(100, value))
                self.vertex_count.set(value)
            except ValueError:
                self.vertex_entry.delete(0, tk.END)
                self.vertex_entry.insert(0, str(self.vertex_count.get()))
        
        def update_vertex_entry_from_slider(*args):
            if hasattr(self, 'vertex_entry') and self.vertex_entry.winfo_exists():
                self.vertex_entry.delete(0, tk.END)
                self.vertex_entry.insert(0, str(self.vertex_count.get()))
        
        self.vertex_entry.bind('<Return>', update_vertex_from_entry)
        self.vertex_entry.bind('<FocusOut>', update_vertex_from_entry)
        self.vertex_count.trace_add("write", update_vertex_entry_from_slider)
        
        # Распределение ребер 
        edge_frame = self.widget_factory.create_label_frame(main_container, text=self.t('edge_distribution'))
        edge_frame.pack(fill="x", pady=(0, 40))
        
        edge_content = self.widget_factory.create_frame(edge_frame)
        edge_content.pack(fill="x", padx=10, pady=10)
        
        # Верхняя строка с выбором распределения
        edge_row = self.widget_factory.create_frame(edge_content)
        edge_row.pack(anchor="w", fill="x", pady=(0, 10))
        
        self.widget_factory.create_label_normal(edge_row, text=f"{self.t('edge_distribution')}:").pack(side="left", padx=(0, 10))
        
        edge_values = [
            self.t('Uniform'), 
            self.t('Normal'), 
            self.t('Student'), 
            self.t('Laplace'), 
            self.t('Bimodal'), 
            self.t('Skewed_t'), 
            self.t('Stepwise')
        ]
        self._edge_combobox = self.widget_factory.create_combobox(edge_row, edge_values, self.edge_distribution)
        self._edge_combobox.pack(side="left", padx=(0, 20))
        
        # Фрейм для параметров распределения
        self.edge_param_frame = self.widget_factory.create_frame(edge_row)
        self.edge_param_frame.pack(side="left")
        
        # График распределения
        self.dist_plot_widget = EdgeWeightPlotWidget(edge_row, self.theme_manager, self.translator)
        self.dist_plot_widget.pack(side="left", padx=(20, 0))
        
        # Распределение вершин
        vertex_frame = self.widget_factory.create_label_frame(main_container, text=self.t('vertex_distribution'))
        vertex_frame.pack(fill="x", pady=(0, 40))
        
        vertex_content = self.widget_factory.create_frame(vertex_frame)
        vertex_content.pack(fill="x", padx=10, pady=10)
        
        # Верхняя строка с выбором распределения
        vertex_dist_row = self.widget_factory.create_frame(vertex_content)
        vertex_dist_row.pack(anchor="w", fill="x", pady=(0, 10))
        
        self.widget_factory.create_label_normal(vertex_dist_row, text=f"{self.t('vertex_distribution')}:").pack(side="left", padx=(0, 10))
        
        vertex_values = [
            self.t('None'), 
            self.t('Uniform'), 
            self.t('Normal'), 
            self.t('Lognormal'), 
            self.t('Stepwise')
        ]
        self._vertex_combobox = self.widget_factory.create_combobox(vertex_dist_row, vertex_values, self.vertex_distribution)
        self._vertex_combobox.pack(side="left", padx=(0, 20))
        
        # Фрейм для параметров распределения вершин
        self.vertex_param_frame = self.widget_factory.create_frame(vertex_dist_row)
        self.vertex_param_frame.pack(side="left")
        
        # Контейнер для графика вершин
        self.vertex_plot_container = self.widget_factory.create_frame(vertex_dist_row)
        self.vertex_plot_container.pack(side="left", padx=(20, 0))
        self.vertex_dist_plot_widget = None
        
        # Фрейм для устойчивости и влияния
        self.props_frame = self.widget_factory.create_frame(vertex_content)
        self.props_frame.pack_forget()
        
        # Контейнер для выровненного расположения
        props_container = self.widget_factory.create_frame(self.props_frame)
        props_container.pack(fill="x", pady=5)
        
        # Контейнер сетки для выравнивания
        props_grid = self.widget_factory.create_frame(props_container)
        props_grid.pack(fill="x", pady=(0, 10))
        
        props_grid.columnconfigure(1, weight=0, minsize=200)
        props_grid.columnconfigure(2, weight=0, minsize=40)
        props_grid.columnconfigure(3, weight=0, minsize=60)
        props_grid.columnconfigure(4, weight=0)
        
        # Устойчивость
        resistance_widgets = self.widget_factory.create_parameter_row(props_grid, self.t('vertex_resistance'), self.resistance_coeff,
            from_val=0, to_val=1, resolution=0.01, row=0, combobox_var=self.vertex_resistance,
            combobox_values=[self.t('None'), self.t('resistance_direct'), self.t('resistance_inverse')],
            coeff_var=self.resistance_coeff, translator=self.translator, combobox_width=35)
        
        # Влияние
        influence_widgets = self.widget_factory.create_parameter_row(props_grid, self.t('vertex_influence'), self.influence_coeff,
            from_val=0, to_val=1, resolution=0.01, row=1, combobox_var=self.vertex_influence,
            combobox_values=[self.t('None'), self.t('influence_direct'), self.t('influence_inverse')],
            coeff_var=self.influence_coeff, translator=self.translator, combobox_width=35)
        
        self.resistance_widgets = resistance_widgets
        self.influence_widgets = influence_widgets
        self.props_widgets = [resistance_widgets, influence_widgets]
        
        def update_resistance_entry(*args):
            if 'coeff_entry' in self.resistance_widgets:
                try:
                    self.resistance_widgets['coeff_entry'].delete(0, tk.END)
                    self.resistance_widgets['coeff_entry'].insert(0, str(round(self.resistance_coeff.get(), 2)))
                except tk.TclError:
                    pass
        
        def update_influence_entry(*args):
            if 'coeff_entry' in self.influence_widgets:
                try:
                    self.influence_widgets['coeff_entry'].delete(0, tk.END)
                    self.influence_widgets['coeff_entry'].insert(0, str(round(self.influence_coeff.get(), 2)))
                except tk.TclError:
                    pass
        
        def update_resistance_from_entry(event=None):
            try:
                value = float(self.resistance_widgets['coeff_entry'].get())
                value = max(0.0, min(1.0, value))
                self.resistance_coeff.set(round(value, 2))
            except ValueError:
                update_resistance_entry()
        
        def update_influence_from_entry(event=None):
            try:
                value = float(self.influence_widgets['coeff_entry'].get())
                value = max(0.0, min(1.0, value))
                self.influence_coeff.set(round(value, 2))
            except ValueError:
                update_influence_entry()
        
        self.resistance_widgets['coeff_entry'].bind('<Return>', update_resistance_from_entry)
        self.resistance_widgets['coeff_entry'].bind('<FocusOut>', update_resistance_from_entry)
        self.influence_widgets['coeff_entry'].bind('<Return>', update_influence_from_entry)
        self.influence_widgets['coeff_entry'].bind('<FocusOut>', update_influence_from_entry)
        
        self.resistance_coeff.trace_add("write", update_resistance_entry)
        self.influence_coeff.trace_add("write", update_influence_entry)
        self.vertex_resistance.trace_add("write", self.update_resistance_coeff_state)
        self.vertex_influence.trace_add("write", self.update_influence_coeff_state)
        
        # Затухание
        damping_frame = self.widget_factory.create_label_frame(main_container, text=self.t('damping'))
        damping_frame.pack(fill="x", pady=(0, 40))
        damping_content = self.widget_factory.create_frame(damping_frame)
        damping_content.pack(fill="x", padx=10, pady=10)
        damp_row = self.widget_factory.create_frame(damping_content)
        damp_row.pack(anchor="w", fill="x")
        self.widget_factory.create_label_normal(damp_row, text=f"{self.t('damping')}:").pack(side="left", padx=(0, 10))
        damping_values = [
            self.t('damping_none'), 
            self.t('damping_exponential'), 
            self.t('damping_hyperbolic'), 
            self.t('damping_discrete')
        ]
        self._damping_combobox = self.widget_factory.create_combobox(damp_row, damping_values, self.damping_type, width=20)
        self._damping_combobox.pack(side="left", padx=(0, 20))
        self.damping_param_frame = self.widget_factory.create_frame(damp_row)
        self.damping_param_frame.pack(side="left")
        
        # Кнопка построения
        button_frame = self.widget_factory.create_frame(main_container)
        button_frame.pack(fill="x", pady=30)
        build_btn = self.widget_factory.create_primary_button(button_frame,self.t('build_graph'),self._on_build_graph_click)
        build_btn.pack()
        
        # Привязка событий
        self.edge_distribution.trace_add("write", lambda *args: self.update_edge_params())
        self.vertex_distribution.trace_add("write", lambda *args: self.update_vertex_params())
        self.vertex_distribution.trace_add("write", self.update_vertex_props_state)
        self.damping_type.trace_add("write", lambda *args: self.update_damping_param())
        
        # Инициализация состояния
        self.update_vertex_props_state()
        self.update_damping_param()
        self.update_resistance_coeff_state()
        self.update_influence_coeff_state()
        
        # Инициализация графиков
        self.root.after(100, self._initialize_default_plots)
        
        # Обновление параметров
        self.update_edge_params()
        self.update_vertex_params()
        
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_build_graph_click(self):
        """Обработчик клика по кнопке построения графа"""
        self.build_graph()
        # Переключаемся на вкладку симуляции
        self.tab_manager.activate_tab(2)
        # Обновляем содержимое вкладки симуляции
        self._build_simulation_tab_content()
        # Сбрасываем флаг первого посещения
        self.simulation_tab_first_visit = False    
    
    def _build_simulation_tab_empty(self):
        for widget in self.simulation_tab.winfo_children():
            widget.destroy()
        
        center_frame = self.widget_factory.create_frame(self.simulation_tab)
        center_frame.pack(expand=True, fill="both")
        empty_frame = self.widget_factory.create_frame(center_frame)
        empty_frame.pack(expand=True)

        self.widget_factory.create_label_h1(empty_frame, text=self.t('no_graph_selected'), font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        self.widget_factory.create_label_normal(empty_frame, text=self.t('build_graph_first'), font=("Segoe UI", 12)).pack()
        
        # Кнопка перехода на генерацию
        btn_frame = self.widget_factory.create_frame(empty_frame)
        btn_frame.pack(pady=30)
        
        go_to_gen_btn = self.widget_factory.create_primary_button(btn_frame, self.t('tab_generation'), lambda: self.tab_manager.activate_tab(0))
        go_to_gen_btn.pack()
    
    def _build_simulation_tab_content(self):
        """Строит интерфейс вкладки симуляции с графом"""
        if self.current_graph is None:
            self._build_simulation_tab_empty()
            return
        for widget in self.simulation_tab.winfo_children():
            widget.destroy()
        self._build_graph_interface_in_frame(self.simulation_tab, self.current_graph, self.node_weights)
    
    def _build_graph_interface_in_frame(self, parent_frame, graph, node_weights=None):
        """Строит интерфейс отображения графа в указанном фрейме"""
        main_container = self.widget_factory.create_frame(parent_frame)
        main_container.pack(fill="both", expand=True, padx=5, pady=10)
        main_paned = tk.PanedWindow(main_container, orient=tk.HORIZONTAL,bg=self.theme_manager.get_color('bg_color'), sashwidth=5)
        main_paned.pack(fill="both", expand=True)
        
        # Левая панель со статистикой 
        left_frame = self.widget_factory.create_frame(main_paned, width=290, bd=0, relief="flat")
        main_paned.add(left_frame, minsize=250, width=290)
        left_canvas = self.widget_factory.create_canvas(left_frame, highlightthickness=0)
        scrollbar = self.widget_factory.create_scrollbar(left_frame, orient="vertical", command=left_canvas.yview)
        stats_container = self.widget_factory.create_frame(left_canvas)
        left_canvas.create_window((0, 0), window=stats_container, anchor="nw", width=260)
        left_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Вычисляет статистику
        edge_stats, vertex_stats, adj_matrix = self.stats_manager.calculate_graph_statistics(graph, self.node_weights)
        
        # Параметры графа
        params_frame = self.widget_factory.create_label_frame(stats_container, text=self.t('graph_parameters'))
        params_frame.pack(fill="x", padx=0, pady=(10, 30))
        params_lines = self.stats_manager.get_graph_parameters_summary()
        for param in params_lines:
            if param.startswith("  ("):
                coeff_frame = self.widget_factory.create_frame(params_frame)
                coeff_frame.pack(fill="x", pady=(0, 2))
                self.widget_factory.create_label_small_bold(
                    coeff_frame, text=param, anchor="e"
                ).pack(fill="x", side="right", padx=5)
            elif param.startswith("  "):
                type_frame = self.widget_factory.create_frame(params_frame)
                type_frame.pack(fill="x", pady=(0, 0))
                self.widget_factory.create_label_small_bold(
                    type_frame, text=param, anchor="e"
                ).pack(fill="x", side="right", padx=5)
            elif ":" in param:
                parts = param.split(":")
                if len(parts) == 2:
                    label = parts[0] + ":"
                    value = parts[1].strip()
                    row = self.widget_factory.create_frame(params_frame)
                    row.pack(fill="x", pady=2, padx=0)
                    self.widget_factory.create_label_small(row, text=label).pack(side="left")
                    self.widget_factory.create_label_small_bold(row, text=value).pack(side="right")
        
        # Статистика ребер
        if edge_stats:
            edges_frame = self.widget_factory.create_label_frame(stats_container, text=self.t('edge_stats'))
            edges_frame.pack(fill="x", padx=0, pady=(0, 10))
            edge_stats_data = self.stats_manager.format_edge_stats_for_display()
            for label, value in edge_stats_data:
                if label == "":
                    empty_frame = self.widget_factory.create_frame(edges_frame, height=5)
                    empty_frame.pack(fill="x")
                    continue
                    
                row = self.widget_factory.create_frame(edges_frame)
                row.pack(fill="x", pady=2, padx=0)
                self.widget_factory.create_label_small(row, text=f"{label}:").pack(side="left")
                self.widget_factory.create_label_small_bold(row, text=value).pack(side="right")
        
        # Статистика вершин
        if vertex_stats:
            vertices_frame = self.widget_factory.create_label_frame(stats_container, text=self.t('vertex_stats'))
            vertices_frame.pack(fill="x", padx=0, pady=(20, 10))
            vertex_stats_data = self.stats_manager.format_vertex_stats_for_display()
            for label, value in vertex_stats_data:
                row = self.widget_factory.create_frame(vertices_frame)
                row.pack(fill="x", pady=2, padx=0)  # Уменьшен padx до 2
                self.widget_factory.create_label_small(row, text=f"{label}:").pack(side="left")
                self.widget_factory.create_label_small_bold(row, text=value).pack(side="right")
        
        stats_container.update_idletasks()
        left_canvas.config(scrollregion=left_canvas.bbox("all"))
        scrollbar.pack(side="right", fill="y")
        left_canvas.pack(side="left", fill="both", expand=True)
        
        # Правая панель
        right_main_frame = self.widget_factory.create_frame(main_paned)
        main_paned.add(right_main_frame, minsize=1000)
        right_paned = tk.PanedWindow(right_main_frame, orient=tk.VERTICAL, bg=self.theme_manager.get_color('bg_color'), sashwidth=5)
        right_paned.pack(fill="x", expand=True)
        
        # Верхний фрейм. Граф и легенда
        top_right_frame = self.widget_factory.create_frame(right_paned)
        right_paned.add(top_right_frame, minsize=500, height=800)
        graph_legend_paned = tk.PanedWindow(top_right_frame, orient=tk.HORIZONTAL, bg=self.theme_manager.get_color('frame_bg'), sashwidth=5)
        graph_legend_paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Фрейм для графа
        graph_frame = self.widget_factory.create_frame(graph_legend_paned)
        graph_legend_paned.add(graph_frame, minsize=1000, width=2000)
        # Фрейм для легенды и гистограмм
        legend_frame = self.widget_factory.create_frame(graph_legend_paned, width=220)
        graph_legend_paned.add(legend_frame, minsize=200, width=220)
        legend_frame.pack_propagate(False)
        
        #Рисование графа
        self.graph_fig = Figure(facecolor=self.theme_manager.get_color('frame_bg'))
        self.graph_ax = self.graph_fig.add_subplot(111)
        
        try:
            self.draw_graph(self.graph_ax, graph, show_fire=bool(self.burning_nodes))
            self.graph_canvas = FigureCanvasTkAgg(self.graph_fig, master=graph_frame)
            self.graph_canvas.draw()
            self.graph_canvas.get_tk_widget().pack(fill="both", expand=True)
            
            def on_graph_frame_configure(event):
                width = graph_frame.winfo_width()
                height = graph_frame.winfo_height()
                if width > 10 and height > 10:
                    width_inches = width / 100
                    height_inches = height / 100
                    self.graph_fig.set_size_inches(width_inches, height_inches)
                    self.graph_ax.clear()
                    self.draw_graph(self.graph_ax, graph, show_fire=bool(self.burning_nodes))
                    self.graph_canvas.draw()
            
            graph_frame.bind('<Configure>', on_graph_frame_configure)
            graph_frame.after(100, lambda: on_graph_frame_configure(None))
            
        except Exception as e:
            self.widget_factory.create_label_normal(graph_frame, text=f"Ошибка визуализации:\n{str(e)}", fg="red").pack(expand=True, pady=50)
        
        # Легенда и гистограммы
        self.graph_legend_widget = GraphLegendWidget(legend_frame, self.theme_manager, self.translator,
                                                     self.colors, widget_factory=self.widget_factory)
        legend_panel = self.graph_legend_widget.create_full_panel()
        legend_panel.pack(fill="both", expand=True, padx=2, pady=2)
        self.graph_legend_widget.set_current_graph(graph)
        self.graph_legend_widget.set_histogram_update_callback('edge', self.update_histogram)
        self.graph_legend_widget.set_histogram_update_callback('vertex', self.update_histogram)
        self.root.after(100, lambda: self.graph_legend_widget.update_histogram('edge', graph))
        self.root.after(100, lambda: self.graph_legend_widget.update_histogram('vertex', graph))
        
        # Нижняя панель с симуляцией
        bottom_right_frame = self.widget_factory.create_frame(right_paned)
        right_paned.add(bottom_right_frame, minsize=180, height=180)
        self._create_simulation_panel(bottom_right_frame, graph)
        
        # Обновление статистики
        self.stats_manager.update_start_vertex_stats(graph, self.start_vertex.get() - 1, self.node_weights)
    
    def _build_custom_tab(self):
        """Строит интерфейс вкладки пользовательского графа"""
        for widget in self.custom_tab.winfo_children():
            widget.destroy()
        
        center_frame = self.widget_factory.create_frame(self.custom_tab)
        center_frame.pack(expand=True)
        
        self.widget_factory.create_label_h1(
            center_frame,
            text="Пользовательский граф\n(Custom Graph)",
            font=("Segoe UI", 20, "bold")
        ).pack()
        
        self.widget_factory.create_label_normal(
            center_frame,
            text="В разработке\n(Under construction)",
            font=("Segoe UI", 14)
        ).pack(pady=20)
        
    def _build_multiple_tab(self):
        """Строит интерфейс вкладки множественной симуляции"""
        for widget in self.multiple_tab.winfo_children():
            widget.destroy()
        
        center_frame = self.widget_factory.create_frame(self.multiple_tab)
        center_frame.pack(expand=True)
        
        self.widget_factory.create_label_h1(
            center_frame,
            text="Множественная симуляция\n(Multiple Simulation)",
            font=("Segoe UI", 20, "bold")
        ).pack()
        
        self.widget_factory.create_label_normal(
            center_frame,
            text="В разработке\n(Under construction)",
            font=("Segoe UI", 14)
        ).pack(pady=20)
    
    def _build_help_tab(self):
        """Строит интерфейс вкладки справки"""
        # Создаем построитель контента для справки
        self.help_content_builder = HelpContentBuilder(
            self.help_tab,
            self.theme_manager,
            self.translator,
            self.widget_factory
        )
        
        # Строим содержимое
        self.help_content_builder.build(self.help_tab)
    
    def _build_settings_tab(self):
        """Строит интерфейс вкладки настроек"""
        for widget in self.settings_tab.winfo_children():
            widget.destroy()
        
        # Создаем canvas с прокруткой для длинного содержимого
        canvas = self.widget_factory.create_canvas(self.settings_tab, highlightthickness=0)
        scrollbar = self.widget_factory.create_scrollbar(
            self.settings_tab, orient="vertical", command=canvas.yview
        )
        scrollable_frame = self.widget_factory.create_frame(canvas, bd=0, relief="flat")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw"
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width - 20)
        
        canvas.bind('<Configure>', on_canvas_configure)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_container = self.widget_factory.create_frame(scrollable_frame, padx=20, pady=20)
        main_container.pack(fill="both", expand=True)
        
        # Фиксированная позиция для всех полей
        FIELD_X_POSITION = 180 
        
        # Глобальные настройки
        global_frame = self.widget_factory.create_label_frame(main_container, text=self.t('settings_interface'))
        global_frame.pack(fill="x", pady=(0, 40))
        
        # Язык
        lang_row = self.widget_factory.create_frame(global_frame)
        lang_row.pack(fill="x", pady=(10, 0))
        lang_label = tk.Label(lang_row, text=f"{self.t('language')}:", width=20,anchor="w",
                              bg=self.colors['frame_bg'], fg=self.colors['text_color'], font=("Segoe UI", 10))
        lang_label.pack(side="left")
        lang_value = 'EN' if self.translator.language == 'en' else 'RU'
        self.settings_language = tk.StringVar(value=lang_value)
        lang_values = ['RU', 'EN']
        self._lang_combobox = self.widget_factory.create_combobox(lang_row, lang_values, self.settings_language)
        self._lang_combobox.place(x=FIELD_X_POSITION, y=0)
        
        # Тема
        theme_row = self.widget_factory.create_frame(global_frame)
        theme_row.pack(fill="x", pady=(5, 0))
        
        theme_label = tk.Label(theme_row, text=f"{self.t('settings_theme')}:", width=15, anchor="w",
                               bg=self.colors['frame_bg'], fg=self.colors['text_color'], font=("Segoe UI", 10))
        theme_label.pack(side="left")
        theme_values = [self.t('theme_light'), self.t('theme_dark')]
        
        if self.theme_manager.theme == 'light':
            theme_display_value = self.t('theme_light')
        else:
            theme_display_value = self.t('theme_dark')
        
        if not hasattr(self, 'settings_theme'):
            self.settings_theme = tk.StringVar(value=theme_display_value)
        else:
            self.settings_theme.set(theme_display_value)
        
        self._theme_combobox = self.widget_factory.create_combobox(theme_row, theme_values, self.settings_theme)
        self._theme_combobox.place(x=FIELD_X_POSITION, y=0)
        
        # Воспроизводимость
        seed_frame = self.widget_factory.create_label_frame(main_container, text=self.t('settings_reproducibility'))
        seed_frame.pack(fill="x", pady=(0, 40))
        seed_row = self.widget_factory.create_frame(seed_frame)
        seed_row.pack(fill="x", pady=(10, 0))
        seed_label = tk.Label(seed_row, text=f"{self.t('settings_seed')}:", width=20,anchor="w",
                              bg=self.colors['frame_bg'], fg=self.colors['text_color'], font=("Segoe UI", 10))
        seed_label.pack(side="left")
        seed_mode_values = [self.t('settings_seed_random'), self.t('settings_seed_fixed')]
        
        if not hasattr(self, 'settings_seed_mode'):
            self.settings_seed_mode = tk.StringVar(value=self.t('settings_seed_random'))
        if not hasattr(self, 'settings_seed_value'):
            self.settings_seed_value = tk.IntVar(value=42)

        self._seed_mode_combobox = self.widget_factory.create_combobox(seed_row, seed_mode_values, self.settings_seed_mode)
        self._seed_mode_combobox.place(x=FIELD_X_POSITION, y=0)

        self.seed_value_entry = self.widget_factory.create_entry(seed_row, width=6, font=("Segoe UI", 9), justify="center")
        self.seed_value_entry.insert(0, str(self.settings_seed_value.get()))
        
        if self.settings_seed_mode.get() == self.t('settings_seed_fixed'):
            self.seed_value_entry.place(x=FIELD_X_POSITION + 160, y=0)
        
        seed_note = tk.Label(seed_frame, text=f"* {self.t('settings_seed_note')}", fg=self.colors['text_secondary'],
                             bg=self.colors['frame_bg'], font=("Segoe UI", 9), anchor="w")
        seed_note.pack(anchor="w", padx=(0, 0), pady=(2, 0))
        
        # Визуализация графа
        viz_frame = self.widget_factory.create_label_frame(main_container, text=self.t('settings_visualization'))
        viz_frame.pack(fill="x", pady=(0, 40))
        
        # Итерации компоновки
        layout_row = self.widget_factory.create_frame(viz_frame)
        layout_row.pack(fill="x", pady=(10, 0))
        
        layout_label = tk.Label(layout_row, text=f"{self.t('settings_layout_iterations')}:", width=15,anchor="w", 
                                bg=self.colors['frame_bg'], fg=self.colors['text_color'], font=("Segoe UI", 10))
        layout_label.pack(side="left")
        
        if not hasattr(self, 'settings_layout_iterations'):
            self.settings_layout_iterations = tk.IntVar(value=200)
        
        layout_spinbox = self.widget_factory.create_spinbox(layout_row, from_=50, to=500, increment=10, width=6,
                                                            textvariable=self.settings_layout_iterations, justify="center")
        layout_spinbox.place(x=FIELD_X_POSITION, y=0)
        
        layout_note = tk.Label(viz_frame, text=f"* {self.t('settings_layout_note')}", fg=self.colors['text_secondary'],
                               bg=self.colors['frame_bg'], font=("Segoe UI", 9), anchor="w")
        layout_note.pack(anchor="w", padx=(0, 0), pady=(2, 0))
        
        # Чекбокс для отрицательных ребер
        neg_row = self.widget_factory.create_frame(viz_frame)
        neg_row.pack(fill="x", pady=(15, 0))
        neg_row.config(height=30)
        
        # Фрейм для чекбокса
        check_frame = self.widget_factory.create_frame(neg_row)
        check_frame.place(x=0, y=10)
        
        if not hasattr(self, 'settings_show_negative'):
            self.settings_show_negative = tk.BooleanVar(value=True)
        
        check_btn = tk.Checkbutton(
            check_frame,
            text=self.t('settings_show_negative'),
            variable=self.settings_show_negative,
            onvalue=True,
            offvalue=False,
            bg=self.colors['frame_bg'],
            fg=self.colors['text_color'],
            selectcolor=self.colors['frame_bg'],
            activebackground=self.colors['frame_bg'],
            activeforeground=self.colors['text_color'],
            font=("Segoe UI", 10),
            cursor="hand2"
        )
        check_btn.pack(side="left")
        
        neg_note = tk.Label(viz_frame, text=f"* {self.t('settings_show_negative_note')}", fg=self.colors['text_secondary'],
                            bg=self.colors['frame_bg'], font=("Segoe UI", 9), anchor="w")
        neg_note.pack(anchor="w", padx=(0, 0), pady=(2, 10))
        
        # Привязка обработчиков
        def on_language_change(*args):
            if not self._updating_ui:
                self._on_setting_changed('language')
        
        def on_theme_change(*args):
            if not self._updating_ui:
                self._on_setting_changed('theme')
        
        def on_seed_mode_change(*args):
            if not self._updating_ui:
                self._on_seed_mode_changed()
        
        def on_seed_value_change(*args):
            if not self._updating_ui:
                self._on_setting_changed('seed_value')
        
        def on_layout_change(*args):
            if not self._updating_ui:
                self._on_setting_changed('layout')
        
        def on_show_negative_change(*args):
            if not self._updating_ui:
                self._on_setting_changed('show_negative')
        
        self.settings_language.trace_add("write", on_language_change)
        self.settings_theme.trace_add("write", on_theme_change)
        self.settings_seed_mode.trace_add("write", on_seed_mode_change)
        self.settings_seed_value.trace_add("write", on_seed_value_change)
        self.settings_layout_iterations.trace_add("write", on_layout_change)
        self.settings_show_negative.trace_add("write", on_show_negative_change)
        
        def on_seed_entry_change(event=None):
            if self._updating_ui:
                return
            try:
                value = int(self.seed_value_entry.get())
                value = max(0, min(9999, value))
                self.settings_seed_value.set(value)
            except ValueError:
                self.seed_value_entry.delete(0, tk.END)
                self.seed_value_entry.insert(0, str(self.settings_seed_value.get()))
        
        self.seed_value_entry.bind('<Return>', on_seed_entry_change)
        self.seed_value_entry.bind('<FocusOut>', on_seed_entry_change)
        
        def update_seed_entry(*args):
            if hasattr(self, 'seed_value_entry') and self.seed_value_entry.winfo_exists():
                self.seed_value_entry.delete(0, tk.END)
                self.seed_value_entry.insert(0, str(self.settings_seed_value.get()))
        
        self.settings_seed_value.trace_add("write", update_seed_entry)
        
        
    def _update_seed_entry_visibility(self):
        """Показывает/скрывает поле ввода seed в зависимости от режима"""
        if not hasattr(self, 'seed_value_entry'):
            return
        
        mode = self.settings_seed_mode.get()
        mode_eng = self.translator.get_english_key(mode)
        if mode_eng == 'Fixed':
            self.seed_value_entry.pack(side="left", padx=(0, 10))
        else:
            self.seed_value_entry.pack_forget()
        
    def _on_seed_mode_changed(self):
        """Обработчик изменения режима seed"""
        self._update_seed_entry_visibility()
        self._on_setting_changed('seed_mode')
            
    def _on_setting_changed(self, setting_name):
        """Обработчик изменения любой настройки"""
        if self._updating_ui:
            return
        
        try:
            self._updating_ui = True
            if setting_name == 'language':
                new_lang = self.settings_language.get().lower()
                if new_lang != self.translator.language:
                    self.translator.set_language(new_lang)
                    current_tab = self.tab_manager.active_tab_index
                    current_graph = self.current_graph
                    current_weights = self.node_weights
                    current_burning = self.burning_nodes.copy() if self.burning_nodes else {}
                    current_edges = self.burned_edges.copy() if self.burned_edges else {}
                    current_start = self.start_vertex.get() if hasattr(self, 'start_vertex') else 1
                    
                    current_seed_mode = self.settings_seed_mode.get()
                    current_seed_value = self.settings_seed_value.get()
                    
                    saved_edge_key = self.translator.get_english_key(self.edge_distribution.get())
                    saved_vertex_key = self.translator.get_english_key(self.vertex_distribution.get())
                    saved_resistance_key = self.translator.get_english_key(self.vertex_resistance.get())
                    saved_influence_key = self.translator.get_english_key(self.vertex_influence.get())
                    saved_damping_key = self.translator.get_english_key(self.damping_type.get())
                    saved_seed_mode_key = self.translator.get_english_key(current_seed_mode)
                    saved_theme_key = self.translator.get_english_key(self.settings_theme.get())
                    
                    saved_edge_params = {
                        'min': self.edge_min.get(),
                        'max': self.edge_max.get(),
                        'mean': self.edge_mean.get(),
                        'std': self.edge_std.get(),
                        'student_df': self.student_df.get(),
                        'student_scale': self.student_scale.get(),
                        'laplace_loc': self.laplace_loc.get(),
                        'laplace_scale': self.laplace_scale.get(),
                        'bimodal_mu1': self.bimodal_mu1.get(),
                        'bimodal_sigma1': self.bimodal_sigma1.get(),
                        'bimodal_mu2': self.bimodal_mu2.get(),
                        'bimodal_sigma2': self.bimodal_sigma2.get(),
                        'bimodal_weight': self.bimodal_weight.get(),
                        'skewed_df': self.skewed_df.get(),
                        'skewed_shape': self.skewed_shape.get(),
                        'skewed_scale': self.skewed_scale.get(),
                    }
                    
                    saved_vertex_params = {
                        'min': self.vertex_min.get(),
                        'max': self.vertex_max.get(),
                        'mean': self.vertex_mean.get(),
                        'std': self.vertex_std.get(),
                        'gamma': self.lognormal_gamma.get(),
                        'mu': self.lognormal_mu.get(),
                        'sigma': self.lognormal_sigma.get(),
                    }
                    
                    saved_coeffs = {
                        'damping': self.damping_value.get(),
                        'resistance': self.resistance_coeff.get(),
                        'influence': self.influence_coeff.get(),
                    }
                    
                    saved_tier_params = {
                        'n_stages': self.tier_n_stages.get(),
                        'left': [v.get() for v in self.tier_left_bounds],
                        'right': [v.get() for v in self.tier_right_bounds],
                        'weights': [v.get() for v in self.tier_weights],
                    }
                    
                    saved_edge_tier_params = {
                        'n_stages': self.edge_tier_n_stages.get(),
                        'left': [v.get() for v in self.edge_tier_left_bounds],
                        'right': [v.get() for v in self.edge_tier_right_bounds],
                        'weights': [v.get() for v in self.edge_tier_weights],
                    }
                    
                    saved_settings = {
                        'seed_value': current_seed_value,
                        'layout_iterations': self.settings_layout_iterations.get(),
                        'show_negative': self.settings_show_negative.get(),
                    }
                    
                    # ОБНОВЛЯЕМ ТЕКСТ НА КНОПКАХ ВКЛАДОК
                    tab_keys = [
                        'tab_generation',
                        'tab_custom',
                        'tab_simulation',
                        'tab_multiple',
                        'tab_help',
                        'tab_settings'
                    ]
                    
                    for i, tab_button in enumerate(self.tab_manager.tabs):
                        if i < len(tab_keys):
                            tab_button.button.config(text=self.t(tab_keys[i]))
                    
                    self._build_generation_tab()
                    self._build_custom_tab()
                    self._build_settings_tab()
                    self._build_help_tab()
                    self._build_multiple_tab()
                    self.vertex_count.set(self.vertex_count.get())
                    
                    self.edge_min.set(saved_edge_params.get('min', 0.0))
                    self.edge_max.set(saved_edge_params.get('max', 1.0))
                    self.edge_mean.set(saved_edge_params.get('mean', 0.3))
                    self.edge_std.set(saved_edge_params.get('std', 0.5))
                    self.student_df.set(saved_edge_params.get('student_df', 10.0))
                    self.student_scale.set(saved_edge_params.get('student_scale', 0.5))
                    self.laplace_loc.set(saved_edge_params.get('laplace_loc', 0.0))
                    self.laplace_scale.set(saved_edge_params.get('laplace_scale', 0.5))
                    self.bimodal_mu1.set(saved_edge_params.get('bimodal_mu1', -0.5))
                    self.bimodal_sigma1.set(saved_edge_params.get('bimodal_sigma1', 0.3))
                    self.bimodal_mu2.set(saved_edge_params.get('bimodal_mu2', 0.5))
                    self.bimodal_sigma2.set(saved_edge_params.get('bimodal_sigma2', 0.3))
                    self.bimodal_weight.set(saved_edge_params.get('bimodal_weight', 0.5))
                    self.skewed_df.set(saved_edge_params.get('skewed_df', 10.0))
                    self.skewed_shape.set(saved_edge_params.get('skewed_shape', 0.0))
                    self.skewed_scale.set(saved_edge_params.get('skewed_scale', 0.5))
                    
                    self.vertex_min.set(saved_vertex_params.get('min', 0.0))
                    self.vertex_max.set(saved_vertex_params.get('max', 1.0))
                    self.vertex_mean.set(saved_vertex_params.get('mean', 0.5))
                    self.vertex_std.set(saved_vertex_params.get('std', 0.2))
                    self.lognormal_gamma.set(saved_vertex_params.get('gamma', 0.0))
                    self.lognormal_mu.set(saved_vertex_params.get('mu', -1.0))
                    self.lognormal_sigma.set(saved_vertex_params.get('sigma', 0.5))
                    
                    self.damping_value.set(saved_coeffs.get('damping', 0.5))
                    self.resistance_coeff.set(saved_coeffs.get('resistance', 0.5))
                    self.influence_coeff.set(saved_coeffs.get('influence', 0.5))
                    
                    self.settings_seed_value.set(saved_settings['seed_value'])
                    self.settings_layout_iterations.set(saved_settings['layout_iterations'])
                    self.settings_show_negative.set(saved_settings['show_negative'])
                    
                    self.edge_distribution.set(self.t(saved_edge_key))
                    self.vertex_distribution.set(self.t(saved_vertex_key))
                    self.vertex_resistance.set(self.t(saved_resistance_key))
                    self.vertex_influence.set(self.t(saved_influence_key))
                    self.damping_type.set(self.t(saved_damping_key))
                    self.settings_theme.set(self.t(saved_theme_key))
                    
                    self.settings_seed_mode.set(self.t(saved_seed_mode_key))
                    self.root.after(100, self._update_seed_entry_visibility)
                    
                    if 'n_stages' in saved_tier_params:
                        self.tier_n_stages.set(saved_tier_params['n_stages'])
                        lefts = saved_tier_params.get('left', [])
                        rights = saved_tier_params.get('right', [])
                        weights = saved_tier_params.get('weights', [])
                        
                        if len(lefts) != len(self.tier_left_bounds):
                            self.tier_n_stages.set(len(lefts))
                            self.update_tier_stage_count()
                        
                        for i in range(min(len(lefts), len(self.tier_left_bounds))):
                            self.tier_left_bounds[i].set(lefts[i])
                        for i in range(min(len(rights), len(self.tier_right_bounds))):
                            self.tier_right_bounds[i].set(rights[i])
                        for i in range(min(len(weights), len(self.tier_weights))):
                            self.tier_weights[i].set(weights[i])
                    
                    if 'n_stages' in saved_edge_tier_params:
                        self.edge_tier_n_stages.set(saved_edge_tier_params['n_stages'])
                        lefts = saved_edge_tier_params.get('left', [])
                        rights = saved_edge_tier_params.get('right', [])
                        weights = saved_edge_tier_params.get('weights', [])
                        
                        if len(lefts) != len(self.edge_tier_left_bounds):
                            self.edge_tier_n_stages.set(len(lefts))
                            self.update_edge_tier_stage_count()
                        
                        for i in range(min(len(lefts), len(self.edge_tier_left_bounds))):
                            self.edge_tier_left_bounds[i].set(lefts[i])
                        for i in range(min(len(rights), len(self.edge_tier_right_bounds))):
                            self.edge_tier_right_bounds[i].set(rights[i])
                        for i in range(min(len(weights), len(self.edge_tier_weights))):
                            self.edge_tier_weights[i].set(weights[i])
                    
                    self.update_edge_params()
                    self.update_vertex_params()
                    self.update_vertex_props_state()
                    self.update_damping_param()
                    
                    self.current_graph = current_graph
                    self.node_weights = current_weights
                    self.burning_nodes = current_burning
                    self.burned_edges = current_edges
                    
                    if hasattr(self, 'start_vertex'):
                        self.start_vertex.set(current_start)
                    
                    if self.current_graph:
                        self._build_simulation_tab_content()
                    else:
                        self._build_simulation_tab_empty()
                    
                    self.root.update_idletasks()
                    self.tab_manager.activate_tab(current_tab)
            
            elif setting_name == 'theme':
                theme_display = self.settings_theme.get()
                new_theme = 'light' if theme_display == self.t('theme_light') else 'dark'
                
                if new_theme != self.theme_manager.theme:
                    current_tab = self.tab_manager.active_tab_index
                    current_graph = self.current_graph
                    current_weights = self.node_weights
                    current_burning = self.burning_nodes.copy() if self.burning_nodes else {}
                    current_edges = self.burned_edges.copy() if self.burned_edges else {}
                    current_start = self.start_vertex.get() if hasattr(self, 'start_vertex') else 1
                    
                    current_seed_mode = self.settings_seed_mode.get()
                    current_seed_value = self.settings_seed_value.get()
                    
                    saved_edge_key = self.translator.get_english_key(self.edge_distribution.get())
                    saved_vertex_key = self.translator.get_english_key(self.vertex_distribution.get())
                    saved_resistance_key = self.translator.get_english_key(self.vertex_resistance.get())
                    saved_influence_key = self.translator.get_english_key(self.vertex_influence.get())
                    saved_damping_key = self.translator.get_english_key(self.damping_type.get())
                    saved_seed_mode_key = self.translator.get_english_key(current_seed_mode)
                    saved_theme_key = self.translator.get_english_key(self.settings_theme.get())
                    
                    saved_edge_params = {
                        'min': self.edge_min.get(),
                        'max': self.edge_max.get(),
                        'mean': self.edge_mean.get(),
                        'std': self.edge_std.get(),
                        'student_df': self.student_df.get(),
                        'student_scale': self.student_scale.get(),
                        'laplace_loc': self.laplace_loc.get(),
                        'laplace_scale': self.laplace_scale.get(),
                        'bimodal_mu1': self.bimodal_mu1.get(),
                        'bimodal_sigma1': self.bimodal_sigma1.get(),
                        'bimodal_mu2': self.bimodal_mu2.get(),
                        'bimodal_sigma2': self.bimodal_sigma2.get(),
                        'bimodal_weight': self.bimodal_weight.get(),
                        'skewed_df': self.skewed_df.get(),
                        'skewed_shape': self.skewed_shape.get(),
                        'skewed_scale': self.skewed_scale.get(),
                    }
                    
                    saved_vertex_params = {
                        'min': self.vertex_min.get(),
                        'max': self.vertex_max.get(),
                        'mean': self.vertex_mean.get(),
                        'std': self.vertex_std.get(),
                        'gamma': self.lognormal_gamma.get(),
                        'mu': self.lognormal_mu.get(),
                        'sigma': self.lognormal_sigma.get(),
                    }
                    
                    saved_coeffs = {
                        'damping': self.damping_value.get(),
                        'resistance': self.resistance_coeff.get(),
                        'influence': self.influence_coeff.get(),
                    }
                    
                    saved_tier_params = {
                        'n_stages': self.tier_n_stages.get(),
                        'left': [v.get() for v in self.tier_left_bounds],
                        'right': [v.get() for v in self.tier_right_bounds],
                        'weights': [v.get() for v in self.tier_weights],
                    }
                    
                    saved_edge_tier_params = {
                        'n_stages': self.edge_tier_n_stages.get(),
                        'left': [v.get() for v in self.edge_tier_left_bounds],
                        'right': [v.get() for v in self.edge_tier_right_bounds],
                        'weights': [v.get() for v in self.edge_tier_weights],
                    }
                    
                    saved_settings = {
                        'seed_value': current_seed_value,
                        'layout_iterations': self.settings_layout_iterations.get(),
                        'show_negative': self.settings_show_negative.get(),
                    }
                    
                    self.root.config(cursor="watch")
                    self.root.update()
                    
                    self.theme_manager.set_theme(new_theme)
                    self.colors = self.theme_manager.colors
                    
                    self.widget_factory.theme_manager = self.theme_manager
                    self.widget_factory.colors = self.colors
                    
                    self.root.configure(bg=self.colors['bg_color'])
                    
                    if hasattr(self, 'tab_manager'):
                        self.tab_manager.main_container.destroy()
                    
                    self.tab_manager = TabManager(self.root, self.theme_manager, self.translator, 
                                                 self.widget_factory, self)
                    
                    self.generation_tab = self.tab_manager.get_tab_frame(0)
                    self.custom_tab = self.tab_manager.get_tab_frame(1)
                    self.simulation_tab = self.tab_manager.get_tab_frame(2)
                    self.multiple_tab = self.tab_manager.get_tab_frame(3)
                    self.help_tab = self.tab_manager.get_tab_frame(4)
                    self.settings_tab = self.tab_manager.get_tab_frame(5)
                    
                    for frame in self.tab_manager.tab_frames:
                        frame.pack_forget()
                    
                    self._build_generation_tab()
                    self._build_custom_tab()
                    self._build_settings_tab()
                    self._build_multiple_tab()
                    self._build_help_tab()
                    
                    self.vertex_count.set(self.vertex_count.get())
                    
                    self.edge_min.set(saved_edge_params.get('min', 0.0))
                    self.edge_max.set(saved_edge_params.get('max', 1.0))
                    self.edge_mean.set(saved_edge_params.get('mean', 0.3))
                    self.edge_std.set(saved_edge_params.get('std', 0.5))
                    self.student_df.set(saved_edge_params.get('student_df', 10.0))
                    self.student_scale.set(saved_edge_params.get('student_scale', 0.5))
                    self.laplace_loc.set(saved_edge_params.get('laplace_loc', 0.0))
                    self.laplace_scale.set(saved_edge_params.get('laplace_scale', 0.5))
                    self.bimodal_mu1.set(saved_edge_params.get('bimodal_mu1', -0.5))
                    self.bimodal_sigma1.set(saved_edge_params.get('bimodal_sigma1', 0.3))
                    self.bimodal_mu2.set(saved_edge_params.get('bimodal_mu2', 0.5))
                    self.bimodal_sigma2.set(saved_edge_params.get('bimodal_sigma2', 0.3))
                    self.bimodal_weight.set(saved_edge_params.get('bimodal_weight', 0.5))
                    self.skewed_df.set(saved_edge_params.get('skewed_df', 10.0))
                    self.skewed_shape.set(saved_edge_params.get('skewed_shape', 0.0))
                    self.skewed_scale.set(saved_edge_params.get('skewed_scale', 0.5))
                    
                    self.vertex_min.set(saved_vertex_params.get('min', 0.0))
                    self.vertex_max.set(saved_vertex_params.get('max', 1.0))
                    self.vertex_mean.set(saved_vertex_params.get('mean', 0.5))
                    self.vertex_std.set(saved_vertex_params.get('std', 0.2))
                    self.lognormal_gamma.set(saved_vertex_params.get('gamma', 0.0))
                    self.lognormal_mu.set(saved_vertex_params.get('mu', -1.0))
                    self.lognormal_sigma.set(saved_vertex_params.get('sigma', 0.5))
                    
                    self.damping_value.set(saved_coeffs.get('damping', 0.5))
                    self.resistance_coeff.set(saved_coeffs.get('resistance', 0.5))
                    self.influence_coeff.set(saved_coeffs.get('influence', 0.5))
                    
                    self.settings_seed_value.set(saved_settings['seed_value'])
                    self.settings_layout_iterations.set(saved_settings['layout_iterations'])
                    self.settings_show_negative.set(saved_settings['show_negative'])
                    
                    self.edge_distribution.set(self.t(saved_edge_key))
                    self.vertex_distribution.set(self.t(saved_vertex_key))
                    self.vertex_resistance.set(self.t(saved_resistance_key))
                    self.vertex_influence.set(self.t(saved_influence_key))
                    self.damping_type.set(self.t(saved_damping_key))
                    self.settings_theme.set(self.t(saved_theme_key))
                    
                    self.settings_seed_mode.set(self.t(saved_seed_mode_key))
                    self.root.after(200, self._update_seed_entry_visibility)
                    
                    if 'n_stages' in saved_tier_params:
                        self.tier_n_stages.set(saved_tier_params['n_stages'])
                        lefts = saved_tier_params.get('left', [])
                        rights = saved_tier_params.get('right', [])
                        weights = saved_tier_params.get('weights', [])
                        
                        if len(lefts) != len(self.tier_left_bounds):
                            self.tier_n_stages.set(len(lefts))
                            self.update_tier_stage_count()
                        
                        for i in range(min(len(lefts), len(self.tier_left_bounds))):
                            self.tier_left_bounds[i].set(lefts[i])
                        for i in range(min(len(rights), len(self.tier_right_bounds))):
                            self.tier_right_bounds[i].set(rights[i])
                        for i in range(min(len(weights), len(self.tier_weights))):
                            self.tier_weights[i].set(weights[i])
                    
                    if 'n_stages' in saved_edge_tier_params:
                        self.edge_tier_n_stages.set(saved_edge_tier_params['n_stages'])
                        lefts = saved_edge_tier_params.get('left', [])
                        rights = saved_edge_tier_params.get('right', [])
                        weights = saved_edge_tier_params.get('weights', [])
                        
                        if len(lefts) != len(self.edge_tier_left_bounds):
                            self.edge_tier_n_stages.set(len(lefts))
                            self.update_edge_tier_stage_count()
                        
                        for i in range(min(len(lefts), len(self.edge_tier_left_bounds))):
                            self.edge_tier_left_bounds[i].set(lefts[i])
                        for i in range(min(len(rights), len(self.edge_tier_right_bounds))):
                            self.edge_tier_right_bounds[i].set(rights[i])
                        for i in range(min(len(weights), len(self.edge_tier_weights))):
                            self.edge_tier_weights[i].set(weights[i])
                    
                    self.update_edge_params()
                    self.update_vertex_params()
                    self.update_vertex_props_state()
                    self.update_damping_param()
                    
                    self.current_graph = current_graph
                    self.node_weights = current_weights
                    self.burning_nodes = current_burning
                    self.burned_edges = current_edges
                    
                    if hasattr(self, 'start_vertex'):
                        self.start_vertex.set(current_start)
                    
                    if self.current_graph:
                        self._build_simulation_tab_content()
                    else:
                        self._build_simulation_tab_empty()
                    
                    self.tab_manager.active_tab_index = current_tab
                    self.tab_manager.tab_frames[current_tab].pack(fill="both", expand=True)
                    self.tab_manager._update_tab_colors()
                    
                    self.root.config(cursor="")
                    self.root.update_idletasks()
            
            elif setting_name == 'seed_mode':
                self._update_seed_entry_visibility()
                self._apply_current_settings()
            
            elif setting_name == 'seed_value':
                self._apply_current_settings()
                
                if self.current_graph and hasattr(self, 'graph_ax') and hasattr(self, 'graph_canvas'):
                    self._graph_positions_cache = None
                    self.graph_ax.clear()
                    self.draw_graph(self.graph_ax, self.current_graph, 
                                  show_fire=bool(self.burning_nodes))
                    self.graph_canvas.draw()
            
            elif setting_name == 'layout':
                self._apply_current_settings()
                
                if self.current_graph and hasattr(self, 'graph_ax') and hasattr(self, 'graph_canvas'):
                    self._graph_positions_cache = None
                    self.graph_ax.clear()
                    self.draw_graph(self.graph_ax, self.current_graph, 
                                  show_fire=bool(self.burning_nodes))
                    self.graph_canvas.draw()
            
            elif setting_name == 'show_negative':
                self._apply_current_settings()
                
                if self.current_graph and hasattr(self, 'graph_ax') and hasattr(self, 'graph_canvas'):
                    self.graph_ax.clear()
                    self.draw_graph(self.graph_ax, self.current_graph, 
                                  show_fire=bool(self.burning_nodes))
                    self.graph_canvas.draw()
                
        except Exception as e:
            print(f"Ошибка при применении настроек: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._updating_ui = False
    
    def _apply_current_settings(self):
        """Применяет текущие настройки к работающему приложению"""
        mode = self.settings_seed_mode.get()
        mode_eng = self.translator.get_english_key(mode)
        if mode_eng == 'Fixed':
            self.layout_seed = self.settings_seed_value.get()
        else:
            self.layout_seed = random.randint(1, 10000)
        random.seed(self.layout_seed)
        np.random.seed(self.layout_seed)
        self.layout_iterations = self.settings_layout_iterations.get()
        self.show_negative_edges = self.settings_show_negative.get()
    
    def update_resistance_coeff_state(self, *args):
        """Показывает или скрывает коэффициент устойчивости в зависимости от выбора"""
        if not hasattr(self, 'resistance_widgets'):
            return
        resistance_value = self.vertex_resistance.get()
        resistance_eng = self.translator.get_english_key(resistance_value)
        is_none = resistance_eng == 'None'
        widgets = self.resistance_widgets
        if 'coeff_label' in widgets and 'coeff_entry' in widgets and 'coeff_slider' in widgets:
            if is_none:
                widgets['coeff_label'].grid_remove()
                widgets['coeff_entry'].grid_remove()
                widgets['coeff_slider'].grid_remove()
            else:
                widgets['coeff_label'].grid()
                widgets['coeff_entry'].grid()
                widgets['coeff_slider'].grid()
    
    def update_influence_coeff_state(self, *args):
        """Показывает или скрывает коэффициент влияния в зависимости от выбора"""
        if not hasattr(self, 'influence_widgets'):
            return
        influence_value = self.vertex_influence.get()
        influence_eng = self.translator.get_english_key(influence_value)
        is_none = influence_eng == 'None'
        widgets = self.influence_widgets
        if 'coeff_label' in widgets and 'coeff_entry' in widgets and 'coeff_slider' in widgets:
            if is_none:
                widgets['coeff_label'].grid_remove()
                widgets['coeff_entry'].grid_remove()
                widgets['coeff_slider'].grid_remove()
            else:
                widgets['coeff_label'].grid()
                widgets['coeff_entry'].grid()
                widgets['coeff_slider'].grid()
        
    def calculate_probability(self, edge_weight, source_node, target_node, influence_strength, influence_type):
        """Расчитывает вероятность возгорания с учетом разного влияния"""
        if edge_weight <= 0:
            return 0.0
        base_probability = min(edge_weight, 1.0)
        source_norm_weight = self.normalized_weights.get(source_node, 1.0)
        scale_factor = 1.0
        influence_eng = self.translator.get_english_key(influence_type)
        if influence_eng == 'influence_direct':
            k = influence_strength * scale_factor
            multiplier = math.exp(k * (source_norm_weight - 1.0))
        elif influence_eng == 'influence_inverse':
            k = influence_strength * scale_factor
            inverse_weight = 2.0 - source_norm_weight
            multiplier = math.exp(k * (inverse_weight - 1.0))
        else:
            multiplier = 1.0
        probability = base_probability * multiplier
        return max(0.0, min(1.0, probability))

    def calculate_resistance_factor(self, target_node, resistance_strength, resistance_type):
        """Расчитывает коэффициент устойчивости"""
        target_norm_weight = self.normalized_weights.get(target_node, 1.0)
        scale_factor = 1.0
        resistance_eng = self.translator.get_english_key(resistance_type)
        if resistance_eng == 'resistance_direct':
            k = resistance_strength * scale_factor
            resistance_factor = math.exp(k * (target_norm_weight - 1.0))
        elif resistance_eng == 'resistance_inverse':
            k = resistance_strength * scale_factor
            inverse_weight = 2.0 - target_norm_weight
            resistance_factor = math.exp(k * (inverse_weight - 1.0))
        else:
            resistance_factor = 1.0
        return max(0.1, min(10.0, resistance_factor))

    def calculate_adjusted_vertex_weights(self, base_weights):
        """Рассчитывает фактические веса вершин"""
        if not base_weights:
            return base_weights
        adjusted_weights = {}
        resistance_eng = self.translator.get_english_key(self.vertex_resistance.get())
        influence_eng = self.translator.get_english_key(self.vertex_influence.get())
        for node_id, base_weight in base_weights.items():
            adjusted_weight = base_weight
            # Устойчивость
            if resistance_eng == 'resistance_direct':
                adjusted_weight *= (1 + self.resistance_coeff.get() * base_weight)
            elif resistance_eng == 'resistance_inverse':
                adjusted_weight *= (1 + self.resistance_coeff.get() * (1 - base_weight))
            # Влияние
            if influence_eng == 'influence_direct':
                adjusted_weight *= (1 + self.influence_coeff.get() * base_weight)
            elif influence_eng == 'influence_inverse':
                adjusted_weight *= (1 + self.influence_coeff.get() * (1 - base_weight))
            adjusted_weight = max(0.0, min(1.0, adjusted_weight))
            adjusted_weights[node_id] = adjusted_weight
        # Нормировка
        self.normalized_weights = self.normalize_vertex_weights(adjusted_weights)
        return adjusted_weights


    def normalize_vertex_weights(self, weights):
        """Нормирует веса в диапазон 0-2"""
        if not weights:
            return {}
        
        values = list(weights.values())
        if len(values) == 0:
            return {}
        
        min_val = min(values)
        max_val = max(values)
        
        if max_val - min_val == 0:
            return {node_id: 1.0 for node_id in weights.keys()}
        
        normalized = {}
        for node_id, weight in weights.items():
            norm_weight = 2.0 * (weight - min_val) / (max_val - min_val)
            normalized[node_id] = norm_weight
        
        return normalized

    def initialize_tier_variables(self):
        """Инициализирует переменные для ступенчатого распределения"""
        if not hasattr(self, 'tier_left_bounds'):
            self.tier_left_bounds = []
        if not hasattr(self, 'tier_right_bounds'):
            self.tier_right_bounds = []
        if not hasattr(self, 'tier_weights'):
            self.tier_weights = []
        
        # Значения по умолчанию для 3 ступеней
        lefts = [0.0, 0.3, 0.7]
        rights = [0.3, 0.7, 1.0]
        counts = [40, 30, 10]
        
        # Очистить существующие, если есть
        self.tier_left_bounds.clear()
        self.tier_right_bounds.clear()
        self.tier_weights.clear()
        
        for i in range(3):
            self.tier_left_bounds.append(tk.DoubleVar(value=lefts[i]))
            self.tier_right_bounds.append(tk.DoubleVar(value=rights[i]))
            self.tier_weights.append(tk.DoubleVar(value=counts[i]))

    def update_vertex_entry_from_slider(self, *args):
        """Обновление поля ввода из слайдера"""
        try:
            if hasattr(self, 'vertex_entry') and self.vertex_entry.winfo_exists():
                self.vertex_entry.delete(0, tk.END)
                self.vertex_entry.insert(0, str(self.vertex_count.get()))
        except tk.TclError:
            pass
    
    def _initialize_default_plots(self):
        """Инициализация графиков по умолчанию"""
        self.update_edge_params()
        if hasattr(self, 'vertex_distribution'):
            current_dist = self.vertex_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            if current_dist_eng != 'None':
                self.update_vertex_params()
                # Принудительно обновляем график вершин
                if hasattr(self, 'vertex_dist_plot_widget'):
                    # Получаем текущие параметры в зависимости от типа
                    if current_dist_eng == 'Uniform':
                        dist_params = {
                            "min": self.vertex_min.get(),
                            "max": self.vertex_max.get()
                        }
                    elif current_dist_eng == 'Normal':
                        dist_params = {
                            "mu": self.vertex_mean.get(),
                            "sigma": self.vertex_std.get()
                        }
                    elif current_dist_eng == 'Lognormal':
                        dist_params = {
                            "gamma": self.lognormal_gamma.get(),
                            "mu": self.lognormal_mu.get(),
                            "sigma": self.lognormal_sigma.get()
                        }
                    elif current_dist_eng == 'Stepwise':
                        stages = []
                        for i in range(len(self.tier_left_bounds)):
                            stages.append({
                                "left": self.tier_left_bounds[i].get(),
                                "right": self.tier_right_bounds[i].get(),
                                "weight": self.tier_weights[i].get()
                            })
                        dist_params = {"stages": stages}
                    else:
                        return
                    self.vertex_dist_plot_widget.update_plot(current_dist_eng, dist_params)

    def _on_canvas_configure(self, event):
        """Обновляет ширину scrollable_frame"""
        self.canvas.itemconfig(self.canvas_window, width=event.width - 20)

    def _on_mousewheel(self, event):
        """Обработка прокрутки колесиком мыши"""
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_edge_params(self):
        """Обновляет виджеты параметров распределения ребер"""
        self._clear_edge_param_traces()
        for widget in self.edge_param_frame.winfo_children():
            widget.destroy()
        # Получаем текущее значение из комбобокса
        current_value = self.edge_distribution.get()
        if current_value == self.t('Uniform'):
            self._create_uniform_edge_params()
        elif current_value == self.t('Normal'):
            self._create_normal_edge_params()
        elif current_value == self.t('Student'):
            self._create_student_edge_params()
        elif current_value == self.t('Laplace'):
            self._create_laplace_edge_params()
        elif current_value == self.t('Bimodal'):
            self._create_bimodal_edge_params()
        elif current_value == self.t('Skewed_t'):
            self._create_skewed_t_edge_params()
        elif current_value == self.t('Stepwise'):
            self._create_stepwise_edge_params(self.edge_param_frame)
        else:
            pass
            
    def _clear_edge_param_traces(self):
        """Очищает все trace связи для параметров ребер"""
        edge_vars = [
            self.edge_min, self.edge_max,
            self.edge_mean, self.edge_std,
            self.student_df, self.student_scale,
            self.laplace_loc, self.laplace_scale,
            self.bimodal_mu1, self.bimodal_sigma1,
            self.bimodal_mu2, self.bimodal_sigma2, self.bimodal_weight,
            self.skewed_df, self.skewed_shape, self.skewed_scale
        ]
        for var in edge_vars:
            try:
                traces = var.trace_info()
                for trace in traces:
                    var.trace_remove("write", trace[1])
            except:
                pass
            
    def _create_uniform_edge_params(self):
        """Создает виджеты для равномерного распределения ребер с синхронизированными слайдерами"""
        for widget in self.edge_param_frame.winfo_children():
            widget.destroy()
        
        param_frame = self.widget_factory.create_frame(self.edge_param_frame)
        param_frame.pack(side="left", fill="both", expand=True)
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('uniform_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        min_widgets = self.widget_factory.create_parameter_row(grid_container, self.t('min_stat'), self.edge_min,
                                                               from_val=-1.0, to_val=0.99, row=0, translator=self.translator)
        max_widgets = self.widget_factory.create_parameter_row(grid_container, self.t('max_stat'), self.edge_max,
                                                               from_val=-0.99, to_val=1.0, row=1, translator=self.translator)
        
        min_entry = min_widgets["entry"]
        min_scale = min_widgets["slider"]
        max_entry = max_widgets["entry"]
        max_scale = max_widgets["slider"]
        
        # Функции синхронизации полей ввода
        def sync_min_entry(*args):
            if min_entry and min_entry.winfo_exists():
                try:
                    min_entry.delete(0, tk.END)
                    min_entry.insert(0, f"{self.edge_min.get():.2f}")
                except tk.TclError:
                    pass
        
        def sync_max_entry(*args):
            if max_entry and max_entry.winfo_exists():
                try:
                    max_entry.delete(0, tk.END)
                    max_entry.insert(0, f"{self.edge_max.get():.2f}")
                except tk.TclError:
                    pass
        
        # Функции валидации и обновления из полей ввода
        def validate_and_update_min_from_entry(event=None):
            try:
                value = float(min_entry.get())
                current_max = self.edge_max.get()
                value = max(-1.0, min(0.99, value))
                if value >= current_max - 0.001:
                    value = max(-1.0, current_max - 0.01)
                self.edge_min.set(round(value, 2))
            except ValueError:
                sync_min_entry()
        
        def validate_and_update_max_from_entry(event=None):
            try:
                value = float(max_entry.get())
                current_min = self.edge_min.get()
                value = max(-0.99, min(1.0, value))
                if value <= current_min + 0.001:
                    value = min(1.0, current_min + 0.01)
                self.edge_max.set(round(value, 2))
            except ValueError:
                sync_max_entry()
        
        # Функции проверки и корректировки значений при изменении переменных
        def check_and_adjust_min(*args):
            try:
                current_min = self.edge_min.get()
                current_max = self.edge_max.get()
                if current_min >= current_max - 0.001:
                    new_min = max(-1.0, current_max - 0.01)
                    if new_min != current_min:
                        self.edge_min.set(round(new_min, 2))
                        
            except (tk.TclError, AttributeError):
                pass
        
        def check_and_adjust_max(*args):
            try:
                current_min = self.edge_min.get()
                current_max = self.edge_max.get()
                if current_max <= current_min + 0.001:
                    new_max = min(1.0, current_min + 0.01)
                    if new_max != current_max:
                        self.edge_max.set(round(new_max, 2))
                        
            except (tk.TclError, AttributeError):
                pass
        
        # Функция обновления графика
        def update_plot(*args):
            try:
                current_min = self.edge_min.get()
                current_max = self.edge_max.get()
                if current_min >= current_max:
                    return
                current_dist = self.edge_distribution.get()
                current_dist_eng = self.translator.get_english_key(current_dist)
                dist_params = {"type": current_dist_eng, "min": current_min, "max": current_max}
                if hasattr(self, 'dist_plot_widget'):
                    self.dist_plot_widget.update_plot(dist_params)
            except Exception:
                pass
        
        # Привязка событий для полей ввода
        min_entry.bind('<Return>', validate_and_update_min_from_entry)
        min_entry.bind('<FocusOut>', validate_and_update_min_from_entry)
        max_entry.bind('<Return>', validate_and_update_max_from_entry)
        max_entry.bind('<FocusOut>', validate_and_update_max_from_entry)

        self.widget_factory.create_synchronized_sliders(min_scale, max_scale, self.edge_min, self.edge_max,
                                                        min_range=-1.0, max_range=1.0, min_gap=0.01)
        
        # Привязка проверок и обновлений
        self.edge_min.trace_add("write", check_and_adjust_min)
        self.edge_max.trace_add("write", check_and_adjust_max)
        self.edge_min.trace_add("write", sync_min_entry)
        self.edge_max.trace_add("write", sync_max_entry)
        self.edge_min.trace_add("write", update_plot)
        self.edge_max.trace_add("write", update_plot)
        
        # Инициализация значений
        current_min = self.edge_min.get()
        current_max = self.edge_max.get()
        
        # Принудительный первый вызов синхронизации
        sync_min_entry()
        sync_max_entry()
        
        # Ссылки на виджеты
        self.min_entry = min_entry
        self.max_entry = max_entry
        self.min_scale = min_scale
        self.max_scale = max_scale
        update_plot()

    
    def _create_normal_edge_params(self):
        """Создает виджеты для нормального распределения"""
        for widget in self.edge_param_frame.winfo_children():
            widget.destroy()
        
        param_frame = self.widget_factory.create_frame(self.edge_param_frame)
        param_frame.pack(side="left", fill="both", expand=True)
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('normal_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        mean_widgets = self.widget_factory.create_parameter_row(grid_container, f"μ ({self.t('mean')})", self.edge_mean, 
                                                                from_val=-1, to_val=1, row=0, translator=self.translator)
        std_widgets = self.widget_factory.create_parameter_row(grid_container, f"σ ({self.t('std')})", self.edge_std, 
                                                       from_val=0.01, to_val=1, row=1, translator=self.translator)
        mean_entry = mean_widgets["entry"]
        mean_scale = mean_widgets["slider"]
        std_entry = std_widgets["entry"]
        std_scale = std_widgets["slider"]
        
        def update_min_entry(*args):
            if mean_entry.winfo_exists():
                mean_entry.delete(0, tk.END)
                mean_entry.insert(0, str(round(self.edge_mean.get(), 2)))
        
        def update_std_entry(*args):
            if std_entry.winfo_exists():
                std_entry.delete(0, tk.END)
                std_entry.insert(0, str(round(self.edge_std.get(), 2)))
        
        def update_plot(*args):
            current_dist = self.edge_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            dist_params = {
                "type": current_dist_eng,
                "mu": self.edge_mean.get(),
                "sigma": self.edge_std.get()
            }
            if hasattr(self, 'dist_plot_widget'):
                self.dist_plot_widget.update_plot(dist_params)
        
        # Привязка событий
        mean_entry.bind('<Return>', lambda e: self._update_from_entry(mean_entry, self.edge_mean, -1, 1))
        mean_entry.bind('<FocusOut>', lambda e: self._update_from_entry(mean_entry, self.edge_mean, -1, 1))
        std_entry.bind('<Return>', lambda e: self._update_from_entry(std_entry, self.edge_std, 0.01, 1))
        std_entry.bind('<FocusOut>', lambda e: self._update_from_entry(std_entry, self.edge_std, 0.01, 1))
        self.edge_mean.trace_add("write", update_min_entry)
        self.edge_std.trace_add("write", update_std_entry)
        self.edge_mean.trace_add("write", update_plot)
        self.edge_std.trace_add("write", update_plot)
        self.mean_entry = mean_entry
        self.std_entry = std_entry
        self.mean_scale = mean_scale
        self.std_scale = std_scale
        # Инициализация графика
        update_plot()
    
    def _create_student_edge_params(self):
        """Создает виджеты для распределения Стьюдента"""
        for widget in self.edge_param_frame.winfo_children():
            widget.destroy()
        
        param_frame = self.widget_factory.create_frame(self.edge_param_frame)
        param_frame.pack(side="left", fill="both", expand=True)
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('student_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        df_widgets = self.widget_factory.create_parameter_row(grid_container, f"df ({self.t('df')})", self.student_df, 
                                                              from_val=1, to_val=30, row=0, resolution=0.1, translator=self.translator)
        scale_widgets = self.widget_factory.create_parameter_row(grid_container, f"scale ({self.t('scale')})", self.student_scale, 
                                                                 from_val=0.01, to_val=1, row=1, translator=self.translator)
        
        df_entry = df_widgets["entry"]
        df_scale = df_widgets["slider"]
        scale_entry = scale_widgets["entry"]
        scale_scale = scale_widgets["slider"]
    
        def update_df_entry(*args):
            if df_entry.winfo_exists():
                df_entry.delete(0, tk.END)
                df_entry.insert(0, str(round(self.student_df.get(), 1)))
        
        def update_scale_entry(*args):
            if scale_entry.winfo_exists():
                scale_entry.delete(0, tk.END)
                scale_entry.insert(0, str(round(self.student_scale.get(), 2)))
        
        def update_plot(*args):
            current_dist = self.edge_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            dist_params = {
                "type": current_dist_eng,
                "df": self.student_df.get(),
                "scale": self.student_scale.get()
            }
            if hasattr(self, 'dist_plot_widget'):
                self.dist_plot_widget.update_plot(dist_params)
        
        # Привязка событий
        df_entry.bind('<Return>', lambda e: self._update_from_entry(df_entry, self.student_df, 1, 30))
        df_entry.bind('<FocusOut>', lambda e: self._update_from_entry(df_entry, self.student_df, 1, 30))
        scale_entry.bind('<Return>', lambda e: self._update_from_entry(scale_entry, self.student_scale, 0.01, 1))
        scale_entry.bind('<FocusOut>', lambda e: self._update_from_entry(scale_entry, self.student_scale, 0.01, 1))
        self.student_df.trace_add("write", update_df_entry)
        self.student_scale.trace_add("write", update_scale_entry)
        self.student_df.trace_add("write", update_plot)
        self.student_scale.trace_add("write", update_plot)
        self.df_entry = df_entry
        self.scale_entry = scale_entry
        self.df_scale = df_scale
        self.scale_scale = scale_scale
        # Инициализация графика
        update_plot()
    
    def _create_laplace_edge_params(self):
        """Создает виджеты для распределения Лапласа"""
        for widget in self.edge_param_frame.winfo_children():
            widget.destroy()
        
        param_frame = self.widget_factory.create_frame(self.edge_param_frame)
        param_frame.pack(side="left", fill="both", expand=True)
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('laplace_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        loc_widgets = self.widget_factory.create_parameter_row(grid_container, f"loc ({self.t('loc')})", self.laplace_loc, 
                                                               from_val=-1, to_val=1, row=0, translator=self.translator)
        scale_widgets = self.widget_factory.create_parameter_row(grid_container, f"scale ({self.t('scale')})", self.laplace_scale, 
                                                                 from_val=0.01, to_val=1, row=1, translator=self.translator)

        loc_entry = loc_widgets["entry"]
        loc_scale = loc_widgets["slider"]
        scale_entry = scale_widgets["entry"]
        scale_scale = scale_widgets["slider"]
    
        def update_loc_entry(*args):
            if loc_entry.winfo_exists():
                loc_entry.delete(0, tk.END)
                loc_entry.insert(0, str(round(self.laplace_loc.get(), 2)))
        
        def update_scale_entry(*args):
            if scale_entry.winfo_exists():
                scale_entry.delete(0, tk.END)
                scale_entry.insert(0, str(round(self.laplace_scale.get(), 2)))
        
        def update_plot(*args):
            current_dist = self.edge_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            dist_params = {
                "type": current_dist_eng,
                "loc": self.laplace_loc.get(),
                "scale": self.laplace_scale.get()
            }
            if hasattr(self, 'dist_plot_widget'):
                self.dist_plot_widget.update_plot(dist_params)
        
        # Привязка событий (оставляем оригинальные вызовы)
        loc_entry.bind('<Return>', lambda e: self._update_from_entry(loc_entry, self.laplace_loc, -1, 1))
        loc_entry.bind('<FocusOut>', lambda e: self._update_from_entry(loc_entry, self.laplace_loc, -1, 1))
        scale_entry.bind('<Return>', lambda e: self._update_from_entry(scale_entry, self.laplace_scale, 0.01, 1))
        scale_entry.bind('<FocusOut>', lambda e: self._update_from_entry(scale_entry, self.laplace_scale, 0.01, 1))
        
        # Привязываем обновления
        self.laplace_loc.trace_add("write", update_loc_entry)
        self.laplace_scale.trace_add("write", update_scale_entry)
        self.laplace_loc.trace_add("write", update_plot)
        self.laplace_scale.trace_add("write", update_plot)
        
        # Инициализация графика
        update_plot()
        
        # Сохраняем ссылки на виджеты как в оригинале
        self.loc_entry = loc_entry
        self.scale_entry = scale_entry
        self.loc_scale = loc_scale
        self.scale_scale = scale_scale
    
    def _create_bimodal_edge_params(self):
        """Создает виджеты для бимодального распределения"""
        for widget in self.edge_param_frame.winfo_children():
            widget.destroy()
        
        param_frame = self.widget_factory.create_frame(self.edge_param_frame)
        param_frame.pack(side="left", fill="both", expand=True)
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('bimodal_params')}:").pack(anchor="w", pady=(0, 5))
        
        main_container = self.widget_factory.create_frame(param_frame)
        main_container.pack(anchor="w", pady=(0, 5))
        
        # Первый режим
        self.widget_factory.create_label_small_bold(main_container, text=f"{self.t('mode1')}:").pack(anchor="w", pady=(5, 0))
        mode1_grid = self.widget_factory.create_frame(main_container)
        mode1_grid.pack(anchor="w", pady=(2, 5))
        
        mu1_widgets = self.widget_factory.create_parameter_row(mode1_grid, f"μ₁ ({self.t('mean')})", self.bimodal_mu1, 
                                                               from_val=-1, to_val=1, row=0, translator=self.translator)
        sigma1_widgets = self.widget_factory.create_parameter_row(mode1_grid, f"σ₁ ({self.t('std')})", self.bimodal_sigma1, 
                                                          from_val=0.01, to_val=1, row=1, translator=self.translator)
        
        mu1_entry = mu1_widgets["entry"]
        mu1_scale = mu1_widgets["slider"]
        sigma1_entry = sigma1_widgets["entry"]
        sigma1_scale = sigma1_widgets["slider"]
    
        # Второй режим
        self.widget_factory.create_label_small_bold(main_container, text=f"{self.t('mode2')}:").pack(anchor="w", pady=(5, 0))
        mode2_grid = self.widget_factory.create_frame(main_container)
        mode2_grid.pack(anchor="w", pady=(2, 5))
        
        mu2_widgets = self.widget_factory.create_parameter_row(mode2_grid, f"μ₂ ({self.t('mean')})", self.bimodal_mu2, 
                                                               from_val=-1, to_val=1, row=0, translator=self.translator)
        sigma2_widgets = self.widget_factory.create_parameter_row(mode2_grid, f"σ₂ ({self.t('std')})", self.bimodal_sigma2, 
                                                          from_val=0.01, to_val=1, row=1, translator=self.translator)

        mu2_entry = mu2_widgets["entry"]
        mu2_scale = mu2_widgets["slider"]
        sigma2_entry = sigma2_widgets["entry"]
        sigma2_scale = sigma2_widgets["slider"]
        
        # Вес
        weight_grid = self.widget_factory.create_frame(main_container)
        weight_grid.pack(anchor="w", pady=(10, 0))
        
        weight_widgets = self.widget_factory.create_parameter_row(weight_grid, f"{self.t('weight1')}", self.bimodal_weight, 
                                                                  from_val=0, to_val=1, row=0, translator=self.translator)

        weight_entry = weight_widgets["entry"]
        weight_scale = weight_widgets["slider"]
        
        def update_mu1_entry(*args):
            if mu1_entry.winfo_exists():
                mu1_entry.delete(0, tk.END)
                mu1_entry.insert(0, str(round(self.bimodal_mu1.get(), 2)))
        
        def update_sigma1_entry(*args):
            if sigma1_entry.winfo_exists():
                sigma1_entry.delete(0, tk.END)
                sigma1_entry.insert(0, str(round(self.bimodal_sigma1.get(), 2)))
        
        def update_mu2_entry(*args):
            if mu2_entry.winfo_exists():
                mu2_entry.delete(0, tk.END)
                mu2_entry.insert(0, str(round(self.bimodal_mu2.get(), 2)))
        
        def update_sigma2_entry(*args):
            if sigma2_entry.winfo_exists():
                sigma2_entry.delete(0, tk.END)
                sigma2_entry.insert(0, str(round(self.bimodal_sigma2.get(), 2)))
        
        def update_weight_entry(*args):
            if weight_entry.winfo_exists():
                weight_entry.delete(0, tk.END)
                weight_entry.insert(0, str(round(self.bimodal_weight.get(), 2)))
        
        def update_plot(*args):
            current_dist = self.edge_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            dist_params = {
                "type": current_dist_eng,
                "mu1": self.bimodal_mu1.get(),
                "sigma1": self.bimodal_sigma1.get(),
                "mu2": self.bimodal_mu2.get(),
                "sigma2": self.bimodal_sigma2.get(),
                "weight1": self.bimodal_weight.get()
            }
            if hasattr(self, 'dist_plot_widget'):
                self.dist_plot_widget.update_plot(dist_params)
        
        # Привязка событий
        mu1_entry.bind('<Return>', lambda e: self._update_from_entry(mu1_entry, self.bimodal_mu1, -1, 1))
        mu1_entry.bind('<FocusOut>', lambda e: self._update_from_entry(mu1_entry, self.bimodal_mu1, -1, 1))
        sigma1_entry.bind('<Return>', lambda e: self._update_from_entry(sigma1_entry, self.bimodal_sigma1, 0.01, 1))
        sigma1_entry.bind('<FocusOut>', lambda e: self._update_from_entry(sigma1_entry, self.bimodal_sigma1, 0.01, 1))
        mu2_entry.bind('<Return>', lambda e: self._update_from_entry(mu2_entry, self.bimodal_mu2, -1, 1))
        mu2_entry.bind('<FocusOut>', lambda e: self._update_from_entry(mu2_entry, self.bimodal_mu2, -1, 1))
        sigma2_entry.bind('<Return>', lambda e: self._update_from_entry(sigma2_entry, self.bimodal_sigma2, 0.01, 1))
        sigma2_entry.bind('<FocusOut>', lambda e: self._update_from_entry(sigma2_entry, self.bimodal_sigma2, 0.01, 1))
        weight_entry.bind('<Return>', lambda e: self._update_from_entry(weight_entry, self.bimodal_weight, 0, 1))
        weight_entry.bind('<FocusOut>', lambda e: self._update_from_entry(weight_entry, self.bimodal_weight, 0, 1))
        
        # Привязываем обновления
        self.bimodal_mu1.trace_add("write", update_mu1_entry)
        self.bimodal_sigma1.trace_add("write", update_sigma1_entry)
        self.bimodal_mu2.trace_add("write", update_mu2_entry)
        self.bimodal_sigma2.trace_add("write", update_sigma2_entry)
        self.bimodal_weight.trace_add("write", update_weight_entry)
        
        # Привязываем обновление графика ко всем переменным
        self.bimodal_mu1.trace_add("write", update_plot)
        self.bimodal_sigma1.trace_add("write", update_plot)
        self.bimodal_mu2.trace_add("write", update_plot)
        self.bimodal_sigma2.trace_add("write", update_plot)
        self.bimodal_weight.trace_add("write", update_plot)
        
        # Инициализация графика
        update_plot()
        
        # Сохраняем ссылки на виджеты как в оригинале
        self.mu1_entry = mu1_entry
        self.sigma1_entry = sigma1_entry
        self.mu2_entry = mu2_entry
        self.sigma2_entry = sigma2_entry
        self.weight_entry = weight_entry
        self.mu1_scale = mu1_scale
        self.sigma1_scale = sigma1_scale
        self.mu2_scale = mu2_scale
        self.sigma2_scale = sigma2_scale
        self.weight_scale = weight_scale
    
    def _create_skewed_t_edge_params(self):
        """Создает виджеты для скошенного распределения Стьюдента"""
        for widget in self.edge_param_frame.winfo_children():
            widget.destroy()
        
        param_frame = self.widget_factory.create_frame(self.edge_param_frame)
        param_frame.pack(side="left", fill="both", expand=True)
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('skewed_t_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        df_widgets = self.widget_factory.create_parameter_row(grid_container, f"df ({self.t('df')})", self.skewed_df, 
                                                              from_val=1, to_val=30, row=0, resolution=0.1, translator=self.translator)
        shape_widgets = self.widget_factory.create_parameter_row(grid_container, f"shape ({self.t('shape')})", self.skewed_shape, 
                                                                 from_val=-5, to_val=5, row=1, resolution=0.1, translator=self.translator)
        scale_widgets = self.widget_factory.create_parameter_row(grid_container, f"scale ({self.t('scale')})", self.skewed_scale, 
                                                                 from_val=0.01, to_val=1, row=2, translator=self.translator)

        df_entry = df_widgets["entry"]
        df_scale = df_widgets["slider"]
        shape_entry = shape_widgets["entry"]
        shape_scale = shape_widgets["slider"]
        scale_entry = scale_widgets["entry"]
        scale_scale = scale_widgets["slider"]
        
        def update_df_entry(*args):
            if df_entry.winfo_exists():
                df_entry.delete(0, tk.END)
                df_entry.insert(0, str(round(self.skewed_df.get(), 1)))
        
        def update_shape_entry(*args):
            if shape_entry.winfo_exists():
                shape_entry.delete(0, tk.END)
                shape_entry.insert(0, str(round(self.skewed_shape.get(), 1)))
        
        def update_scale_entry(*args):
            if scale_entry.winfo_exists():
                scale_entry.delete(0, tk.END)
                scale_entry.insert(0, str(round(self.skewed_scale.get(), 2)))
        
        def update_plot(*args):
            current_dist = self.edge_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            dist_params = {
                "type": current_dist_eng,
                "df": self.skewed_df.get(),
                "shape": self.skewed_shape.get(),
                "scale": self.skewed_scale.get()
            }
            if hasattr(self, 'dist_plot_widget'):
                self.dist_plot_widget.update_plot(dist_params)
        
        # Привязка событий
        df_entry.bind('<Return>', lambda e: self._update_from_entry(df_entry, self.skewed_df, 1, 30))
        df_entry.bind('<FocusOut>', lambda e: self._update_from_entry(df_entry, self.skewed_df, 1, 30))
        shape_entry.bind('<Return>', lambda e: self._update_from_entry(shape_entry, self.skewed_shape, -5, 5))
        shape_entry.bind('<FocusOut>', lambda e: self._update_from_entry(shape_entry, self.skewed_shape, -5, 5))
        scale_entry.bind('<Return>', lambda e: self._update_from_entry(scale_entry, self.skewed_scale, 0.01, 1))
        scale_entry.bind('<FocusOut>', lambda e: self._update_from_entry(scale_entry, self.skewed_scale, 0.01, 1))
        
        # Привязываем обновления
        self.skewed_df.trace_add("write", update_df_entry)
        self.skewed_shape.trace_add("write", update_shape_entry)
        self.skewed_scale.trace_add("write", update_scale_entry)
        
        # Привязываем обновление графика
        self.skewed_df.trace_add("write", update_plot)
        self.skewed_shape.trace_add("write", update_plot)
        self.skewed_scale.trace_add("write", update_plot)
        
        # Инициализация графика
        update_plot()
        
        # Сохраняем ссылки на виджеты как в оригинале
        self.skewed_df_entry = df_entry
        self.skewed_shape_entry = shape_entry
        self.skewed_scale_entry = scale_entry
        self.df_scale = df_scale
        self.shape_scale = shape_scale
        self.scale_scale = scale_scale

        
    def _create_edge_tier_row(self, parent, idx):
        """Создает строку с параметрами для одной ступени ребер"""
        # Удаляем лишние trace_id перед созданием новых
        if idx < len(self.edge_tier_trace_ids):
            for var, trace_id in self.edge_tier_trace_ids[idx]:
                try:
                    var.trace_remove("write", trace_id)
                except:
                    pass
        
        widgets = self.widget_factory.create_tier_stage_row(
            parent, idx, self.t('stage'),
            self.edge_tier_left_bounds[idx], self.edge_tier_right_bounds[idx], 
            self.edge_tier_weights[idx],
            is_edge_tier=True,
            on_plot_update_callback=lambda i=idx: self._schedule_edge_tier_plot_update(),
            translator=self.translator
        )
        
        # Сохраняем trace_id для этого индекса
        if idx >= len(self.edge_tier_trace_ids):
            self.edge_tier_trace_ids.append([])
        self.edge_tier_trace_ids[idx] = widgets['trace_ids']
        
        # Сохраняем виджеты в соответствующие списки
        self.edge_tier_left_entries.append(widgets['left_entry'])
        self.edge_tier_left_sliders.append(widgets['left_slider'])
        self.edge_tier_right_entries.append(widgets['right_entry'])
        self.edge_tier_right_sliders.append(widgets['right_slider'])
        self.edge_tier_weight_sliders.append(widgets['weight_slider'])
        
        return widgets


    def update_edge_tier_stage_count(self):
        """Обновляет количество ступеней ребер"""
        try:
            current_count = len(self.edge_tier_left_bounds)
            new_count = self.edge_tier_n_stages.get()
            new_count = max(2, min(6, new_count))
            
            if new_count != current_count:
                if hasattr(self, 'edge_tier_trace_ids'):
                    for trace_ids in self.edge_tier_trace_ids:
                        for var, trace_id in trace_ids:
                            try:
                                var.trace_remove("write", trace_id)
                            except:
                                pass
                    self.edge_tier_trace_ids = []
                
                if new_count > current_count:
                    # Добавляем новые ступени
                    for i in range(current_count, new_count):
                        # Равномерное распределение по диапазону -1..1
                        segment_width = 2.0 / new_count
                        left_val = -1.0 + i * segment_width
                        right_val = -1.0 + (i + 1) * segment_width
                        # Зазор между ступенями
                        left_val = max(-1.0, left_val + 0.01)
                        right_val = min(1.0, right_val - 0.01)
                        if right_val <= left_val:
                            right_val = left_val + 0.1
                            if right_val > 1.0:
                                right_val = 1.0
                        
                        # Добавляем новые переменные
                        self.edge_tier_left_bounds.append(tk.DoubleVar(value=round(left_val, 2)))
                        self.edge_tier_right_bounds.append(tk.DoubleVar(value=round(right_val, 2)))
                        self.edge_tier_weights.append(tk.DoubleVar(value=round(100.0 / new_count, 1)))
                else:
                    # Удаляем последние ступени
                    self.edge_tier_left_bounds = self.edge_tier_left_bounds[:new_count]
                    self.edge_tier_right_bounds = self.edge_tier_right_bounds[:new_count]
                    self.edge_tier_weights = self.edge_tier_weights[:new_count]
                
                # Сбрасываем списки виджетов
                self.edge_tier_left_entries = []
                self.edge_tier_left_sliders = []
                self.edge_tier_right_entries = []
                self.edge_tier_right_sliders = []
                self.edge_tier_weight_sliders = []
                
                # Немедленное обновление интерфейса
                if self.edge_distribution.get() == self.t('Stepwise'):
                    self.root.after(10, self._safe_update_edge_params)
                    
        except Exception as e:
            print(f"Ошибка при изменении количества ступеней ребер: {e}")
            import traceback
            traceback.print_exc()
    
    def _safe_update_edge_params(self):
        """Безопасное обновление параметров ребер"""
        try:
            if self.edge_distribution.get() == self.t('Stepwise'):
                # Находим frame параметров ребер
                if hasattr(self, 'edge_param_frame') and self.edge_param_frame.winfo_exists():
                    # Создаем новые виджеты
                    self._create_stepwise_edge_params(self.edge_param_frame)
        except Exception as e:
            print(f"Ошибка при безопасном обновлении: {e}")

    def apply_edge_tier_preset(self, preset_key):
        """Применение пресета для ребер"""
        try:
            # Получаем текущее количество ступеней
            current_stages = self.edge_tier_n_stages.get()
            current_stages = max(2, min(6, current_stages))
            preset = get_edge_preset(preset_key, current_stages)
            
            if not preset or "bounds" not in preset or "counts" not in preset:
                print(f"Пресет ребер '{preset_key}' не найден или имеет неверный формат")
                return
            
            # Применяем пресет
            bounds = preset["bounds"]
            counts = preset["counts"]
            
            # Если количество ступеней изменилось, обновляем переменные
            if len(bounds) != len(self.edge_tier_left_bounds):
                self.edge_tier_n_stages.set(len(bounds))
                self.update_edge_tier_stage_count()
                self.root.after(100, lambda: self._apply_edge_preset_values(bounds, counts))
            else:
                self._apply_edge_preset_values(bounds, counts)
            self._update_edge_tier_plot()
        except Exception as e:
            print(f"Ошибка при применении пресета ребер: {e}")
            import traceback
            traceback.print_exc()
    
    def _apply_edge_preset_values(self, bounds, counts):
        """Применяет значения пресета для ребер"""
        try:
            for i in range(min(len(self.edge_tier_left_bounds), len(bounds), len(counts))):
                left, right = bounds[i]
                count = counts[i]
                # Границы для диапазона -1..1
                left = max(-1.0, min(0.99, left))
                right = max(left + 0.01, min(1.0, right))
                self.edge_tier_left_bounds[i].set(round(left, 2))
                self.edge_tier_right_bounds[i].set(round(right, 2))
                self.edge_tier_weights[i].set(count)
            self.root.after(150, self._update_edge_tier_plot)
        except Exception as e:
            print(f"Ошибка при применении значений пресета: {e}")
            
    def _create_stepwise_edge_params(self, param_frame=None):
        """Создает виджеты для ступенчатого распределения ребер"""
        if param_frame is None:
            param_frame = self.edge_param_frame
        for widget in param_frame.winfo_children():
            try:
                widget.destroy()
            except:
                pass
        current_count = len(self.edge_tier_left_bounds)
        expected_count = self.edge_tier_n_stages.get()
        if current_count != expected_count:
            print(f"Количество ступеней ребер не совпадает ({current_count} != {expected_count})")
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('edge_stepwise_params')}:").pack(anchor="w", pady=(0, 10))
    
        # Верхняя строка - количество ступеней
        top_frame = self.widget_factory.create_frame(param_frame)
        top_frame.pack(anchor="w", pady=(0, 10))
        self.widget_factory.create_label_small(top_frame, text=f"{self.t('stages_count')}:").pack(side="left", padx=(0, 10))
    
        stage_spinbox = self.widget_factory.create_spinbox(top_frame, from_=2, to=6, width=4,
                                                           textvariable=self.edge_tier_n_stages, command=self.update_edge_tier_stage_count)
        stage_spinbox.pack(side="left")
    
        def on_stage_spinbox_enter(event):
            self.update_edge_tier_stage_count()
    
        stage_spinbox.bind('<Return>', on_stage_spinbox_enter)
        stage_spinbox.bind('<FocusOut>', on_stage_spinbox_enter)
    
        # Строка для шаблонов
        presets_label_frame = self.widget_factory.create_frame(param_frame)
        presets_label_frame.pack(anchor="w", pady=(5, 5))
        self.widget_factory.create_label_small(presets_label_frame, text=f"{self.t('presets')}:").pack(side="left")
    
        # Фрейм для кнопок шаблонов
        presets_frame = self.widget_factory.create_frame(param_frame)
        presets_frame.pack(anchor="w", pady=(0, 15))
    
        edge_preset_keys = get_all_edge_preset_keys()
        edge_preset_name_mapping = {
            "social": self.t('social'),
            "economic": self.t('economic'),
            "information": self.t('information'),
            "hierarchical": self.t('hierarchical'),
            "ecosystem": self.t('ecosystem'),
            "infrastructure": self.t('infrastructure'),
            "epidemic": self.t('epidemic'),
            "uniform": self.t('uniform_preset')
        }
    
        buttons_per_row = 4
        for row_index in range(0, len(edge_preset_keys), buttons_per_row):
            row_frame = self.widget_factory.create_frame(presets_frame)
            row_frame.pack(fill="x", pady=2)
    
            for preset_key in edge_preset_keys[row_index:row_index + buttons_per_row]:
                preset_name = edge_preset_name_mapping.get(preset_key, preset_key)
                btn = self.widget_factory.create_small_button(row_frame, preset_name,lambda k=preset_key: self.apply_edge_tier_preset(k))
                btn.pack(side="left", padx=2)
    
        stages_container = self.widget_factory.create_frame(param_frame)
        stages_container.pack(fill="both", expand=True, pady=(0, 10))
    
        self.edge_tier_left_entries.clear()
        self.edge_tier_left_sliders.clear()
        self.edge_tier_right_entries.clear()
        self.edge_tier_right_sliders.clear()
        self.edge_tier_weight_sliders.clear()
        self.edge_tier_trace_ids.clear()
    
        for i in range(len(self.edge_tier_left_bounds)):
            self._create_edge_tier_row(stages_container, i)
    
        self._update_edge_tier_plot()
    
    def _schedule_edge_tier_plot_update(self):
        """Запланировать обновление графика ребер"""
        if not hasattr(self, 'edge_tier_plot_pending') or not self.edge_tier_plot_pending:
            self.edge_tier_plot_pending = True
            self.root.after(100, self._update_edge_tier_plot)
    
    def _update_edge_tier_plot(self):
        """Обновить график ступенчатого распределения ребер"""
        try:
            stages = []
            for i in range(len(self.edge_tier_left_bounds)):
                stages.append({
                    "left": self.edge_tier_left_bounds[i].get(),
                    "right": self.edge_tier_right_bounds[i].get(),
                    "weight": self.edge_tier_weights[i].get()
                })
            
            current_dist = self.edge_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            dist_params = {
                "type": current_dist_eng,
                "display_name": current_dist,
                "stages": stages
            }
            
            if hasattr(self, 'dist_plot_widget'):
                self.dist_plot_widget.update_plot(dist_params)
        except Exception as e:
            print(f"Ошибка при обновлении графика ступеней ребер: {e}")
        finally:
            self.edge_tier_plot_pending = False            

    def _update_from_entry(self, entry, var, min_val, max_val):
        """Обновляет переменную из поля ввода"""
        try:
            value = float(entry.get())
            value = max(min_val, min(max_val, value))
            var.set(round(value, 2))
        except ValueError:
            if entry.winfo_exists():
                entry.delete(0, tk.END)
                entry.insert(0, str(round(var.get(), 2)))

    
    def update_vertex_params(self):
        """Обновляет виджеты параметров распределения вершин"""
        # Очищаем старые трассировки если они есть
        if hasattr(self, 'tier_trace_ids'):
            for trace_ids in self.tier_trace_ids:
                for var, trace_id in trace_ids:
                    try:
                        var.trace_remove("write", trace_id)
                    except:
                        pass
            self.tier_trace_ids = []
        
        # Очищаем списки виджетов
        self.tier_left_entries = []
        self.tier_left_sliders = []
        self.tier_right_entries = []
        self.tier_right_sliders = []
        self.tier_weight_sliders = []
        self.tier_plot_pending = False
        
        # Очищаем фрейм параметров
        for widget in self.vertex_param_frame.winfo_children():
            widget.destroy()
    
        self.vertex_param_frame.update_idletasks()
        
        # Очищаем контейнер для графика, если он существует
        if hasattr(self, 'vertex_plot_container'):
            for widget in self.vertex_plot_container.winfo_children():
                widget.destroy()
            self.vertex_plot_container.update_idletasks()
        
        dist = self.vertex_distribution.get()
        dist_eng = self.translator.get_english_key(dist)
        
        # Если распределение "None", уничтожаем виджет графика
        if dist_eng == 'None':
            if hasattr(self, 'vertex_dist_plot_widget') and self.vertex_dist_plot_widget is not None:
                try:
                    self.vertex_dist_plot_widget.destroy()
                except:
                    pass
                self.vertex_dist_plot_widget = None
            return
        
        # Создаем контейнер для параметров и графика
        main_container = self.widget_factory.create_frame(self.vertex_param_frame)
        main_container.pack(side="left", fill="both", expand=True)
        
        param_frame = self.widget_factory.create_frame(main_container)
        param_frame.pack(side="left", padx=(0, 20), fill="both", expand=True)
        
        # Виджет для графика
        self.vertex_dist_plot_widget = VertexWeightPlotWidget(main_container, self.theme_manager, self.translator)
        self.vertex_dist_plot_widget.pack(side="right", padx=(10, 0))

        try:
            if dist_eng == 'Uniform':
                self._create_uniform_vertex_params(param_frame, dist)
            elif dist_eng == 'Normal':
                self._create_normal_vertex_params(param_frame, dist)
            elif dist_eng == 'Lognormal':
                self._create_lognormal_vertex_params(param_frame, dist)
            elif dist_eng == 'Stepwise':
                self._create_stepwise_vertex_settings(param_frame, dist)
        except Exception as e:
            print(f"Ошибка при создании параметров вершин: {e}")
        

    def _create_uniform_vertex_params(self, param_frame, dist):
        """Создает виджеты для равномерного распределения вершин"""
        for widget in param_frame.winfo_children():
            widget.destroy()
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('vertex_uniform_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        min_widgets = self.widget_factory.create_parameter_row(grid_container, self.t('min_stat'), self.vertex_min, 
                                                               from_val=0.0, to_val=0.99, row=0, translator=self.translator)
        max_widgets = self.widget_factory.create_parameter_row(grid_container, self.t('max_stat'), self.vertex_max, 
                                                               from_val=0.01, to_val=1.0, row=1, translator=self.translator)
        
        min_entry = min_widgets["entry"]
        min_scale = min_widgets["slider"]
        max_entry = max_widgets["entry"]
        max_scale = max_widgets["slider"]
        
        # Функции синхронизации полей ввода
        def sync_min_entry(*args):
            if min_entry and min_entry.winfo_exists():
                try:
                    min_entry.delete(0, tk.END)
                    min_entry.insert(0, f"{self.vertex_min.get():.2f}")
                except tk.TclError:
                    pass
        
        def sync_max_entry(*args):
            if max_entry and max_entry.winfo_exists():
                try:
                    max_entry.delete(0, tk.END)
                    max_entry.insert(0, f"{self.vertex_max.get():.2f}")
                except tk.TclError:
                    pass
        
        # Функции валидации и обновления из полей ввода
        def validate_and_update_min_from_entry(event=None):
            try:
                value = float(min_entry.get())
                current_max = self.vertex_max.get()
                value = max(0.0, min(0.99, value))
                if value >= current_max - 0.001:
                    value = max(0.0, current_max - 0.01)
                self.vertex_min.set(round(value, 2))
            except ValueError:
                sync_min_entry()
        
        def validate_and_update_max_from_entry(event=None):
            try:
                value = float(max_entry.get())
                current_min = self.vertex_min.get()
                value = max(0.01, min(1.0, value))
                if value <= current_min + 0.001:
                    value = min(1.0, current_min + 0.01)
                self.vertex_max.set(round(value, 2))
            except ValueError:
                sync_max_entry()
        
        # Функции проверки и корректировки значений
        def check_and_adjust_min(*args):
            try:
                current_min = self.vertex_min.get()
                current_max = self.vertex_max.get()
                if current_min >= current_max - 0.001:
                    new_min = max(0.0, current_max - 0.01)
                    if new_min != current_min:
                        self.vertex_min.set(round(new_min, 2))
            except (tk.TclError, AttributeError):
                pass
        
        def check_and_adjust_max(*args):
            try:
                current_min = self.vertex_min.get()
                current_max = self.vertex_max.get()
                if current_max <= current_min + 0.001:
                    new_max = min(1.0, current_min + 0.01)
                    if new_max != current_max:
                        self.vertex_max.set(round(new_max, 2))
            except (tk.TclError, AttributeError):
                pass
        
        def update_vertex_plot(*args):
            try:
                current_min = self.vertex_min.get()
                current_max = self.vertex_max.get()
                if current_min >= current_max:
                    return
                
                current_dist = self.vertex_distribution.get()
                current_dist_eng = self.translator.get_english_key(current_dist)
                dist_params = {
                    "min": current_min, 
                    "max": current_max
                }
                if hasattr(self, 'vertex_dist_plot_widget'):
                    self.vertex_dist_plot_widget.update_plot(current_dist_eng, dist_params)
            except Exception as e:
                print(f"Ошибка при обновлении графика вершин: {e}")
        
        # Привязка событий для полей ввода
        min_entry.bind('<Return>', validate_and_update_min_from_entry)
        min_entry.bind('<FocusOut>', validate_and_update_min_from_entry)
        max_entry.bind('<Return>', validate_and_update_max_from_entry)
        max_entry.bind('<FocusOut>', validate_and_update_max_from_entry)
        
        # Синхронизированные слайдеры
        self.widget_factory.create_synchronized_sliders(min_scale, max_scale, self.vertex_min, self.vertex_max, 
                                                        min_range=0.0, max_range=1.0, min_gap=0.01)
        
        # Привязка проверок и обновлений
        self.vertex_min.trace_add("write", check_and_adjust_min)
        self.vertex_max.trace_add("write", check_and_adjust_max)
        self.vertex_min.trace_add("write", sync_min_entry)
        self.vertex_max.trace_add("write", sync_max_entry)
        self.vertex_min.trace_add("write", update_vertex_plot)
        self.vertex_max.trace_add("write", update_vertex_plot)
        # Инициализация
        sync_min_entry()
        sync_max_entry()
        update_vertex_plot()
        param_frame.update_idletasks()
    
    def _create_normal_vertex_params(self, param_frame, dist):
        """Создает виджеты для нормального распределения вершин"""
        for widget in param_frame.winfo_children():
            widget.destroy()
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('vertex_normal_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        mean_widgets = self.widget_factory.create_parameter_row(grid_container, f"μ ({self.t('mean')})", self.vertex_mean, 
                                                                from_val=0, to_val=1, row=0, translator=self.translator)
        std_widgets = self.widget_factory.create_parameter_row(grid_container, f"σ ({self.t('std')})", self.vertex_std, 
                                                               from_val=0.01, to_val=1, row=1, translator=self.translator)
        
        mean_entry = mean_widgets["entry"]
        mean_scale = mean_widgets["slider"]
        std_entry = std_widgets["entry"]
        std_scale = std_widgets["slider"]
        
        # Функции обновления полей ввода
        def update_mean_entry(*args):
            if mean_entry and mean_entry.winfo_exists():
                try:
                    mean_entry.delete(0, tk.END)
                    mean_entry.insert(0, str(round(self.vertex_mean.get(), 2)))
                except tk.TclError:
                    pass
        
        def update_std_entry(*args):
            if std_entry and std_entry.winfo_exists():
                try:
                    std_entry.delete(0, tk.END)
                    std_entry.insert(0, str(round(self.vertex_std.get(), 2)))
                except tk.TclError:
                    pass
        
        def update_plot(*args):
            try:
                current_dist = self.vertex_distribution.get()
                current_dist_eng = self.translator.get_english_key(current_dist)
                dist_params = {
                    "mu": self.vertex_mean.get(),
                    "sigma": self.vertex_std.get()
                }
                if hasattr(self, 'vertex_dist_plot_widget'):
                    self.vertex_dist_plot_widget.update_plot(current_dist_eng, dist_params)
            except Exception as e:
                print(f"Ошибка при обновлении графика вершин: {e}")
        
        # Привязка событий для полей ввода
        mean_entry.bind('<Return>', lambda e: self._update_from_entry(mean_entry, self.vertex_mean, 0, 1))
        mean_entry.bind('<FocusOut>', lambda e: self._update_from_entry(mean_entry, self.vertex_mean, 0, 1))
        std_entry.bind('<Return>', lambda e: self._update_from_entry(std_entry, self.vertex_std, 0.01, 1))
        std_entry.bind('<FocusOut>', lambda e: self._update_from_entry(std_entry, self.vertex_std, 0.01, 1))
        
        # Привязываем trace
        self.vertex_mean.trace_add("write", update_mean_entry)
        self.vertex_std.trace_add("write", update_std_entry)
        self.vertex_mean.trace_add("write", update_plot)
        self.vertex_std.trace_add("write", update_plot)
        # Инициализация графика
        update_plot()
    
    def _create_lognormal_vertex_params(self, param_frame, dist):
        """Создает виджеты для логнормального распределения вершин"""
        for widget in param_frame.winfo_children():
            widget.destroy()
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('vertex_lognormal_params')}:").pack(anchor="w", pady=(0, 5))
        
        grid_container = self.widget_factory.create_frame(param_frame)
        grid_container.pack(anchor="w", pady=(0, 5))
        
        gamma_widgets = self.widget_factory.create_parameter_row(grid_container, f"γ ({self.t('gamma')})", self.lognormal_gamma, 
                                                                 from_val=0.0, to_val=0.5, row=0, translator=self.translator)
        mu_widgets = self.widget_factory.create_parameter_row(grid_container, f"μ ({self.t('mu')})", self.lognormal_mu, 
                                                              from_val=-3.0, to_val=1.0, row=1, translator=self.translator)
        sigma_widgets = self.widget_factory.create_parameter_row(grid_container, f"σ ({self.t('sigma')})", self.lognormal_sigma, 
                                                                 from_val=0.01, to_val=2.0, row=2, translator=self.translator)
        
        gamma_entry = gamma_widgets["entry"]
        gamma_scale = gamma_widgets["slider"]
        mu_entry = mu_widgets["entry"]
        mu_scale = mu_widgets["slider"]
        sigma_entry = sigma_widgets["entry"]
        sigma_scale = sigma_widgets["slider"]
        
        # Функции для синхронизации полей ввода
        def update_gamma_entry(*args):
            if gamma_entry.winfo_exists():
                gamma_entry.delete(0, tk.END)
                gamma_entry.insert(0, f"{self.lognormal_gamma.get():.2f}")
        
        def update_mu_entry(*args):
            if mu_entry.winfo_exists():
                mu_entry.delete(0, tk.END)
                mu_entry.insert(0, f"{self.lognormal_mu.get():.1f}")
        
        def update_sigma_entry(*args):
            if sigma_entry.winfo_exists():
                sigma_entry.delete(0, tk.END)
                sigma_entry.insert(0, f"{self.lognormal_sigma.get():.2f}")
        
        # Функции обновления из полей ввода
        def update_from_gamma_entry(event=None):
            try:
                value = float(gamma_entry.get())
                value = max(0.0, min(0.5, value))
                self.lognormal_gamma.set(value)
            except ValueError:
                update_gamma_entry()
        
        def update_from_mu_entry(event=None):
            try:
                value = float(mu_entry.get())
                value = max(-3.0, min(1.0, value))
                self.lognormal_mu.set(value)
            except ValueError:
                update_mu_entry()
        
        def update_from_sigma_entry(event=None):
            try:
                value = float(sigma_entry.get())
                value = max(0.01, min(2.0, value))
                self.lognormal_sigma.set(value)
            except ValueError:
                update_sigma_entry()
        
        def update_plot(*args):
            try:
                gamma_val = self.lognormal_gamma.get()
                mu_val = self.lognormal_mu.get()
                sigma_val = self.lognormal_sigma.get()
                
                current_dist = self.vertex_distribution.get()
                current_dist_eng = self.translator.get_english_key(current_dist)
                dist_params = {"gamma": gamma_val, "mu": mu_val, "sigma": sigma_val}
                
                if hasattr(self, 'vertex_dist_plot_widget'):
                    self.vertex_dist_plot_widget.update_plot(current_dist_eng, dist_params)
            except Exception as e:
                print(f"Ошибка в update_plot: {e}")
        
        # Привязка событий для полей ввода
        gamma_entry.bind('<Return>', update_from_gamma_entry)
        gamma_entry.bind('<FocusOut>', update_from_gamma_entry)
        mu_entry.bind('<Return>', update_from_mu_entry)
        mu_entry.bind('<FocusOut>', update_from_mu_entry)
        sigma_entry.bind('<Return>', update_from_sigma_entry)
        sigma_entry.bind('<FocusOut>', update_from_sigma_entry)
        # Привязываем обновление полей ввода
        self.lognormal_gamma.trace_add('write', update_gamma_entry)
        self.lognormal_mu.trace_add('write', update_mu_entry)
        self.lognormal_sigma.trace_add('write', update_sigma_entry)
        # Привязываем обновление графика
        self.lognormal_gamma.trace_add('write', update_plot)
        self.lognormal_mu.trace_add('write', update_plot)
        self.lognormal_sigma.trace_add('write', update_plot)
        # Инициализация графика
        update_plot()
    
    
    def update_damping_param(self):
        """Обновляет виджет параметра затухания с синхронизацией"""
        for widget in self.damping_param_frame.winfo_children():
            widget.destroy()
        damping_value_text = self.damping_type.get()
        damping_eng = self.translator.get_english_key(damping_value_text)
        if damping_eng != 'None':
            self.damping_value.set(0.5)
            widgets = self.widget_factory.create_parameter_row(self.damping_param_frame, self.t('coeff'), self.damping_value, 
                                    from_val=0, to_val=1, resolution=0.01, row=0, translator=self.translator)
            
            if 'label' in widgets:
                widgets['label'].config(text=f"{self.t('coeff')}:")
            
            if 'entry' in widgets and 'slider' in widgets:
                entry = widgets['entry']
                slider = widgets['slider']
                
                def update_entry_from_slider(*args):
                    if entry and entry.winfo_exists():
                        try:
                            entry.delete(0, tk.END)
                            entry.insert(0, f"{self.damping_value.get():.2f}")
                        except tk.TclError:
                            pass
                
                def update_slider_from_entry(event=None):
                    try:
                        value = float(entry.get())
                        value = max(0.0, min(1.0, value))
                        self.damping_value.set(round(value, 2))
                    except ValueError:
                        update_entry_from_slider()
                
                entry.bind('<Return>', update_slider_from_entry)
                entry.bind('<FocusOut>', update_slider_from_entry)
                self.damping_value.trace_add("write", update_entry_from_slider)
                update_entry_from_slider()
                
    def initialize_edge_tier_variables(self):
        """Инициализирует переменные для ступенчатого распределения ребер"""
        # Проверим, существуют ли уже списки
        if not hasattr(self, 'edge_tier_left_bounds'):
            self.edge_tier_left_bounds = []
        if not hasattr(self, 'edge_tier_right_bounds'):
            self.edge_tier_right_bounds = []
        if not hasattr(self, 'edge_tier_weights'):
            self.edge_tier_weights = []
        
        # Значения по умолчанию для 3 ступеней
        lefts = [-1.0, -0.3, 0.3]
        rights = [-0.3, 0.3, 1.0]
        counts = [40, 30, 10]
        
        # Очистить существующие, если есть
        self.edge_tier_left_bounds.clear()
        self.edge_tier_right_bounds.clear()
        self.edge_tier_weights.clear()
        
        for i in range(3):
            self.edge_tier_left_bounds.append(tk.DoubleVar(value=lefts[i]))
            self.edge_tier_right_bounds.append(tk.DoubleVar(value=rights[i]))
            self.edge_tier_weights.append(tk.DoubleVar(value=counts[i]))
        
        # Инициализация списков для виджетов (если еще не инициализированы)
        if not hasattr(self, 'edge_tier_left_entries'):
            self.edge_tier_left_entries = []
        if not hasattr(self, 'edge_tier_left_sliders'):
            self.edge_tier_left_sliders = []
        if not hasattr(self, 'edge_tier_right_entries'):
            self.edge_tier_right_entries = []
        if not hasattr(self, 'edge_tier_right_sliders'):
            self.edge_tier_right_sliders = []
        if not hasattr(self, 'edge_tier_weight_sliders'):
            self.edge_tier_weight_sliders = []
        if not hasattr(self, 'edge_tier_trace_ids'):
            self.edge_tier_trace_ids = []
    
    def update_vertex_props_state(self, *args):
        """Показывает или скрывает блок устойчивости и влияния"""
        vertex_dist = self.vertex_distribution.get()
        vertex_dist_eng = self.translator.get_english_key(vertex_dist)
        
        if hasattr(self, 'props_frame'):
            if vertex_dist_eng != 'None':
                self.props_frame.pack(fill="x", pady=15)
                self.update_resistance_coeff_state()
                self.update_influence_coeff_state()
            else:
                self.props_frame.pack_forget()
                self.vertex_resistance.set(self.t('None'))
                self.vertex_influence.set(self.t('None'))
                self.update_resistance_coeff_state()
                self.update_influence_coeff_state()

    
    def _create_stepwise_vertex_settings(self, param_frame, dist):
        """Показывает настройки ступенчатого распределения вершин"""
        for widget in param_frame.winfo_children():
            widget.destroy()
        
        self.widget_factory.create_label_small_bold(param_frame, text=f"{self.t('vertex_stepwise_params')}:").pack(anchor="w", pady=(0, 10))
        
        # Верхняя строка - количество ступеней
        top_frame = self.widget_factory.create_frame(param_frame)
        top_frame.pack(anchor="w", pady=(0, 10))
        self.widget_factory.create_label_small(top_frame, text=f"{self.t('stages_count')}:").pack(side="left", padx=(0, 10))
        
        stage_spinbox = self.widget_factory.create_spinbox(top_frame, from_=2, to=6, width=4, 
                                                           textvariable=self.tier_n_stages, command=self.update_tier_stage_count)
        stage_spinbox.pack(side="left", padx=(0, 40))
        
        def on_stage_spinbox_enter(event):
            self.update_tier_stage_count()
        
        stage_spinbox.bind('<Return>', on_stage_spinbox_enter)
        stage_spinbox.bind('<FocusOut>', on_stage_spinbox_enter)
        
        self.widget_factory.create_label_small(top_frame, text=f"{self.t('presets')}:").pack(side="left", padx=(0, 10))
        
        vertex_preset_keys = get_all_vertex_preset_keys()
        
        preset_name_mapping = {
            "market": self.t('market'),
            "oligopoly": self.t('oligopoly'),
            "uniform": self.t('uniform_preset'),
            "pyramid": self.t('pyramid'),
            "exponential": self.t('exponential')
        }
        
        for preset_key in vertex_preset_keys:
            preset_name = preset_name_mapping.get(preset_key, preset_key)
            btn = self.widget_factory.create_small_button(
                top_frame, preset_name, 
                lambda k=preset_key: self.apply_vertex_tier_preset(k)
            )
            btn.pack(side="left", padx=2)
        
        stages_container = self.widget_factory.create_frame(param_frame)
        stages_container.pack(fill="both", expand=True, pady=(0, 10))
        
        self.tier_left_entries.clear()
        self.tier_left_sliders.clear()
        self.tier_right_entries.clear()
        self.tier_right_sliders.clear()
        self.tier_weight_sliders.clear()
        self.tier_trace_ids.clear()
        
        for i in range(len(self.tier_left_bounds)):
            self._create_tier_row(stages_container, i)
        
        self._update_tier_plot()

    def _create_tier_row(self, parent, idx):
        """Создает строку с параметрами для одной ступени вершин"""
        if idx < len(self.tier_trace_ids):
            for var, trace_id in self.tier_trace_ids[idx]:
                try:
                    var.trace_remove("write", trace_id)
                except:
                    pass
        
        widgets = self.widget_factory.create_tier_stage_row(
            parent, idx, self.t('stage'),
            self.tier_left_bounds[idx], self.tier_right_bounds[idx], 
            self.tier_weights[idx],
            is_edge_tier=False,
            on_plot_update_callback=lambda i=idx: self._schedule_tier_plot_update(),
            translator=self.translator
        )
        
        # Сохраняем trace_id для этого индекса
        if idx >= len(self.tier_trace_ids):
            self.tier_trace_ids.append([])
        self.tier_trace_ids[idx] = widgets['trace_ids']
        
        # Сохраняем виджеты в соответствующие списки
        self.tier_left_entries.append(widgets['left_entry'])
        self.tier_left_sliders.append(widgets['left_slider'])
        self.tier_right_entries.append(widgets['right_entry'])
        self.tier_right_sliders.append(widgets['right_slider'])
        self.tier_weight_sliders.append(widgets['weight_slider'])
        return widgets

    def update_tier_stage_count(self):
        """Обновляет количество ступеней с немедленным обновлением интерфейса"""
        try:
            current_count = len(self.tier_left_bounds)
            new_count = self.tier_n_stages.get()
            new_count = max(2, min(6, new_count))
            
            if new_count != current_count:
                if new_count > current_count:
                    # Добавляем новые ступени
                    for i in range(current_count, new_count):
                        # Равномерное распределение по диапазону
                        segment_width = 1.0 / new_count
                        left_val = i * segment_width
                        right_val = (i + 1) * segment_width
                        left_val = max(0.0, left_val + 0.01)
                        right_val = min(1.0, right_val - 0.01)
                        if right_val <= left_val:
                            right_val = left_val + 0.1
                            if right_val > 1.0:
                                right_val = 1.0
                        
                        # Добавляем новые переменные
                        self.tier_left_bounds.append(tk.DoubleVar(value=round(left_val, 2)))
                        self.tier_right_bounds.append(tk.DoubleVar(value=round(right_val, 2)))
                        self.tier_weights.append(tk.DoubleVar(value=round(100.0 / new_count, 1)))
                else:
                    # Удаляем последние ступени
                    self.tier_left_bounds = self.tier_left_bounds[:new_count]
                    self.tier_right_bounds = self.tier_right_bounds[:new_count]
                    self.tier_weights = self.tier_weights[:new_count]
                # Обновление интерфейса
                if self.vertex_distribution.get() == self.t('Stepwise'):
                    self.update_vertex_params()
        except Exception as e:
            print(f"Ошибка при изменении количества ступеней: {e}")

    def _schedule_tier_plot_update(self):
        """Запланировать обновление графика"""
        if not hasattr(self, 'tier_plot_pending') or not self.tier_plot_pending:
            self.tier_plot_pending = True
            self.root.after(100, self._update_tier_plot)

    def _update_tier_plot(self):
        """Обновить график ступенчатого распределения"""
        try:
            if not hasattr(self, 'tier_left_bounds') or not self.tier_left_bounds:
                self.tier_plot_pending = False
                return
            if len(self.tier_left_bounds) == 0:
                self.tier_plot_pending = False
                return
            stages = []
            for i in range(len(self.tier_left_bounds)):
                if i >= len(self.tier_left_bounds) or i >= len(self.tier_right_bounds) or i >= len(self.tier_weights):
                    continue 
                stages.append({
                    "left": self.tier_left_bounds[i].get(),
                    "right": self.tier_right_bounds[i].get(),
                    "weight": self.tier_weights[i].get()
                })
            if not stages:
                self.tier_plot_pending = False
                return
            current_dist = self.vertex_distribution.get()
            current_dist_eng = self.translator.get_english_key(current_dist)
            dist_params = {"stages": stages}
            if hasattr(self, 'vertex_dist_plot_widget') and self.vertex_dist_plot_widget is not None:
                self.vertex_dist_plot_widget.update_plot(current_dist_eng, dist_params)
        except Exception as e:
            print(f"Ошибка при обновлении графика ступеней: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.tier_plot_pending = False
    
    def apply_vertex_tier_preset(self, preset_key):
        """Применение пресета для текущего количества ступеней вершин"""
        try:
            # Получаем текущее количество ступеней
            current_stages = self.tier_n_stages.get()
            current_stages = max(2, min(6, current_stages))
            preset = get_vertex_preset(preset_key, current_stages)
            
            if not preset or "bounds" not in preset or "counts" not in preset:
                print(f"Пресет '{preset_key}' не найден или имеет неверный формат")
                return
            
            # Применяем пресет
            bounds = preset["bounds"]
            counts = preset["counts"]
            for i in range(min(len(self.tier_left_bounds), len(bounds), len(counts))):
                left, right = bounds[i]
                count = counts[i]
                left = max(0.0, min(0.99, left))
                right = max(left + 0.01, min(1.0, right))
                self.tier_left_bounds[i].set(round(left, 2))
                self.tier_right_bounds[i].set(round(right, 2))
                self.tier_weights[i].set(count)
            self._update_tier_plot()
        except Exception as e:
            print(f"Ошибка при применении пресета: {e}")
            import traceback
            traceback.print_exc()


    def build_graph(self):
        """Строит граф на основе выбранных параметров"""
        try:
            self._reset_simulation_state()
            self.save_current_state()
            
            n_nodes = self.vertex_count.get()
            
            edge_dist = self.edge_distribution.get()
            edge_params = self.dist_manager.get_edge_distribution_params(edge_dist)
            
            vertex_dist = self.vertex_distribution.get()
            vertex_dist_eng = self.translator.get_english_key(vertex_dist)
            vertex_func = self.dist_manager.get_vertex_weight_func(vertex_dist_eng, n_nodes)
            
            graph, base_node_weights = self.dist_manager.create_graph_with_weights(n_nodes, edge_params, vertex_func)
            if vertex_dist_eng != "None" and base_node_weights:
                self.node_weights = self.calculate_adjusted_vertex_weights(base_node_weights)
                for node_id, weight in self.node_weights.items():
                    if node_id in graph.nodes():
                        graph.nodes[node_id]['weight'] = weight
            else:
                self.node_weights = base_node_weights if base_node_weights else {}
            
            self.current_graph = graph
            self._last_graph = id(graph)
            self._graph_positions_cache = None
            self.tab_manager.clear_simulation_state()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить граф:\n{str(e)}")
            import traceback
            traceback.print_exc()

    def _reset_simulation_state(self):
        """Сбрасывает состояние симуляции"""
        self.burning_nodes.clear()
        self.burned_edges.clear()
        self.fire_spread_history = []
        self.fire_iteration = 0
        self.max_fire_iteration = 0
        self.is_fire_running = False
        self.stats_manager.reset_all_statistics()
        self._graph_positions_cache = None

    def save_current_state(self):
        """Сохраняет текущие значения параметров"""
        self.saved_state = {
            'vertex_count': self.vertex_count.get(),
            'edge_distribution': self.edge_distribution.get(),
            'vertex_distribution': self.vertex_distribution.get(),
        }
        
    def update_histogram(self, data_type, graph):
        """Обновляет гистограмму фактического распределения"""
        if hasattr(self, 'graph_legend_widget'):
            self.graph_legend_widget.update_histogram(data_type, graph)

    def _create_simulation_panel(self, parent_frame, graph):
        """Создает панель управления симуляцией"""
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        main_container = self.widget_factory.create_frame(parent_frame)
        main_container.pack(fill="both", expand=True, padx=5, pady=10)
        
        left_col = self.widget_factory.create_frame(main_container, width=250)
        left_col.pack(side="left", fill="both", expand=True)
        
        center_col = self.widget_factory.create_frame(main_container, width=200)
        center_col.pack(side="left", fill="both", expand=True, padx=20)
        
        right_col = self.widget_factory.create_frame(main_container, width=300)
        right_col.pack(side="left", fill="both", expand=True)
        
        # Левая колонка. Стартовая вершина
        vertex_frame = self.widget_factory.create_frame(left_col)
        vertex_frame.pack(fill="both", expand=True)
        
        self.widget_factory.create_label_h2(vertex_frame, text=self.t('start_vertex_title')).pack(anchor="w", pady=(0, 10))
        
        input_frame = self.widget_factory.create_frame(vertex_frame)
        input_frame.pack(fill="x", pady=(0, 15))
        
        self.widget_factory.create_label_small(input_frame, text=f"{self.t('vertex_number')}:").pack(side="left", padx=(0, 10))
        
        self.start_vertex_entry = self.widget_factory.create_entry(input_frame, width=8, font=("Segoe UI", 10))
        self.start_vertex_entry.pack(side="left", padx=(0, 10))
        self.start_vertex_entry.insert(0, "1")
        
        max_vertices = graph.number_of_nodes()
        self.start_vertex_slider = self.widget_factory.create_slider(input_frame, from_=1, to=max_vertices, length=150, variable=self.start_vertex)
        self.start_vertex_slider.pack(side="left", fill="x", expand=True)
        
        # Статистика вершины
        stats_frame = self.widget_factory.create_label_frame(vertex_frame, text=self.t('start_vertex_stats'))
        stats_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        stats_canvas = self.widget_factory.create_canvas(stats_frame, highlightthickness=0, height=130)
        stats_scrollbar = self.widget_factory.create_scrollbar(stats_frame, orient="vertical", command=stats_canvas.yview)
        stats_inner_frame = self.widget_factory.create_frame(stats_canvas)
        stats_inner_frame.columnconfigure(0, weight=1)
        stats_inner_frame.columnconfigure(1, weight=0)
        
        stats_canvas.create_window((0, 0), window=stats_inner_frame, anchor="nw", width=240)
        stats_canvas.configure(yscrollcommand=stats_scrollbar.set)
        
        stats_data = self.stats_manager.format_start_vertex_stats_for_display()
        row_num = 0
        
        for label, var in stats_data:
            if label == "":
                # Пустая строка-разделитель
                empty_frame = self.widget_factory.create_frame(stats_inner_frame, height=5)
                empty_frame.grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=2)
                row_num += 1
                continue
                
            # Метка
            left_label = self.widget_factory.create_label_small(stats_inner_frame, text=f"{label}:")
            left_label.grid(row=row_num, column=0, sticky="w", padx=(5, 5), pady=2)
            # Значение
            value_label = self.widget_factory.create_label_small_bold(stats_inner_frame, textvariable=var)
            value_label.grid(row=row_num, column=1, sticky="e", padx=(5, 10), pady=2)
            row_num += 1
        
        stats_inner_frame.update_idletasks()
        stats_canvas.config(scrollregion=stats_canvas.bbox("all"), height=min(130, stats_inner_frame.winfo_reqheight()))
        stats_scrollbar.pack(side="right", fill="y")
        stats_canvas.pack(side="left", fill="both", expand=True)
        
        # Кнопки
        btn_container = self.widget_factory.create_frame(center_col)
        btn_container.pack(fill="both", expand=True)
        
        btn_frame = self.widget_factory.create_frame(btn_container)
        btn_frame.pack(fill="both", expand=True)
        
        button_padding = 10
        button_width = 12
        
        self.fire_start_btn = self.widget_factory.create_fire_button(
            btn_frame, f"{self.t('start_fire')}   🔥",
            lambda: self.start_fire_simulation(graph), width=button_width, height=1
        )
        self.fire_start_btn.pack(fill="both", expand=True, pady=(0, button_padding))
        
        self.reset_btn = self.widget_factory.create_reset_button(
            btn_frame, self.t('reset'),
            lambda: self.reset_fire_simulation(graph), width=button_width, height=1
        )
        self.reset_btn.pack(fill="both", expand=True, pady=(0, button_padding))
        
        new_graph_btn = self.widget_factory.create_new_graph_button(
            btn_frame, self.t('new_graph'),
            self.generate_new_graph, width=button_width, height=1
        )
        new_graph_btn.pack(fill="both", expand=True)
        
        # Итоги симуляции
        results_frame = self.widget_factory.create_label_frame(right_col, text=self.t('simulation_results'))
        results_frame.pack(fill="both", expand=True)
        
        results_canvas = self.widget_factory.create_canvas(results_frame, highlightthickness=0)
        scrollbar = self.widget_factory.create_scrollbar(results_frame, orient="vertical", command=results_canvas.yview)
        results_container = self.widget_factory.create_frame(results_canvas)
        results_container.columnconfigure(0, weight=1)
        results_container.columnconfigure(1, weight=0)
        results_canvas.create_window((0, 0), window=results_container, anchor="nw", width=270)
        results_canvas.configure(yscrollcommand=scrollbar.set)
        
        results_data = self.stats_manager.format_fire_results_for_display()
        row_num = 0
        
        for label, var in results_data:
            if label == "":
                # Пустая строка-разделитель
                empty_frame = self.widget_factory.create_frame(results_container, height=5)
                empty_frame.grid(row=row_num, column=0, columnspan=2, sticky="ew", pady=2)
                row_num += 1
                continue
                
            # Метка
            left_label = self.widget_factory.create_label_small(results_container, text=f"{label}:")
            left_label.grid(row=row_num, column=0, sticky="w", padx=(5, 5), pady=3)
            # Значение
            value_label = self.widget_factory.create_label_small_bold(results_container, textvariable=var)
            value_label.grid(row=row_num, column=1, sticky="e", padx=(5, 10), pady=3)
            row_num += 1
        
        results_container.update_idletasks()
        results_canvas.config(scrollregion=results_canvas.bbox("all"))
        scrollbar.pack(side="right", fill="y")
        results_canvas.pack(side="left", fill="both", expand=True)
        
        # Привязка событий
        def validate_vertex_input(event=None):
            try:
                value = int(self.start_vertex_entry.get())
                value = max(1, min(max_vertices, value))
                self.start_vertex.set(value)
                self.stats_manager.update_start_vertex_stats(
                    self.current_graph, 
                    self.start_vertex.get() - 1, 
                    self.node_weights
                )
            except ValueError:
                self.start_vertex_entry.delete(0, tk.END)
                self.start_vertex_entry.insert(0, str(self.start_vertex.get()))
        
        def update_vertex_entry(*args):
            if hasattr(self, 'start_vertex_entry') and self.start_vertex_entry.winfo_exists():
                self.start_vertex_entry.delete(0, tk.END)
                self.start_vertex_entry.insert(0, str(self.start_vertex.get()))
        
        self.start_vertex_entry.bind('<Return>', validate_vertex_input)
        self.start_vertex_entry.bind('<FocusOut>', validate_vertex_input)
        self.start_vertex.trace_add("write", update_vertex_entry)
        self.start_vertex.trace_add("write", lambda *args: 
            self.stats_manager.update_start_vertex_stats(self.current_graph, self.start_vertex.get() - 1, self.node_weights)
        )
        self.start_vertex.set(1)


    def calculate_ignition_probability(self, graph, edge_weight, source, target, current_iteration):
        """Рассчитывает вероятность загорания вершины"""
        if edge_weight <= 0:
            return 0.0
        influence_value = self.vertex_influence.get()
        influence_eng = self.translator.get_english_key(influence_value)
        has_influence = influence_eng != 'None'
        
        resistance_value = self.vertex_resistance.get()
        resistance_eng = self.translator.get_english_key(resistance_value)
        has_resistance = resistance_eng != 'None'
        
        damping_value = self.damping_type.get()
        damping_eng = self.translator.get_english_key(damping_value)
        has_damping = damping_eng != 'None'
        
        # Базовая вероятность
        if has_influence:
            probability = self.calculate_probability(edge_weight, source, target, self.influence_coeff.get(), influence_eng)
        else:
            probability = min(edge_weight, 1.0) if edge_weight > 0 else 0.0
        # Учет устойчивости
        if has_resistance:
            resistance_factor = self.calculate_resistance_factor(target, self.resistance_coeff.get(), resistance_eng)
            probability = probability / resistance_factor
        # Учет затухания
        if has_damping:
            time_damping = self.calculate_time_damping(current_iteration-1, self.damping_value.get(), damping_eng)
            probability = probability * time_damping
        
        return max(0.0, min(1.0, probability))

    def calculate_time_damping(self, current_iteration, damping_value, damping_type):
        """Рассчитывает затухание по номеру итерации"""
        damping_eng = self.translator.get_english_key(damping_type)
        if damping_eng == 'damping_exponential':
            return math.exp(-damping_value * current_iteration)
        elif damping_eng == 'damping_hyperbolic':
            return 1.0 / (1.0 + damping_value * current_iteration)
        elif damping_eng == 'damping_discrete':
            return math.pow(1.0 / (1.0 + damping_value), current_iteration)
        else:
            return 1.0


    def start_fire_simulation(self, graph):
        """Запускает симуляцию пожара"""
        if self.is_fire_running or graph is None:
            return
        
        self.is_fire_running = True
        self.fire_start_btn.config(state="disabled")
        
        try:
            self.burning_nodes.clear()
            self.burned_edges.clear()
            self.fire_iteration = 0
            self.max_fire_iteration = 0
            self.fire_spread_history = []
            
            start_vertex_idx = self.start_vertex.get() - 1
            start_node = f'V{start_vertex_idx}'
            
            if start_node not in graph.nodes():
                start_node = f'V0'
                self.start_vertex.set(1)
                start_vertex_idx = 0
            
            self.burning_nodes[start_node] = 0
            new_fires_by_iteration = [1]
            
            max_iterations = 100
            for iteration in range(1, max_iterations + 1):
                self.fire_iteration = iteration
                new_fires = 0
                
                for burning_node in list(self.burning_nodes.keys()):
                    burning_iteration = self.burning_nodes[burning_node]
                    
                    for neighbor in graph.neighbors(burning_node):
                        if neighbor not in self.burning_nodes:
                            edge = (min(burning_node, neighbor), max(burning_node, neighbor))
                            
                            if edge not in self.burned_edges:
                                edge_weight = graph.edges[edge]['weight']
                                
                                ignition_prob = self.calculate_ignition_probability(
                                    graph, edge_weight, burning_node, neighbor,
                                    iteration
                                )
                                
                                if random.random() < ignition_prob:
                                    self.burning_nodes[neighbor] = iteration
                                    self.burned_edges[edge] = iteration
                                    self.max_fire_iteration = max(self.max_fire_iteration, iteration)
                                    new_fires += 1
                
                new_fires_by_iteration.append(new_fires)
                
                if new_fires == 0:
                    break
            
            self.fire_spread_history = new_fires_by_iteration
            self.draw_fire_on_graph(graph)
            self.stats_manager.calculate_fire_statistics(self.burning_nodes, self.fire_spread_history, self.fire_iteration)
            self.fire_start_btn.config(state="normal", text=f"{self.t('start_fire')}   🔥")
            
        except Exception as e:
            messagebox.showerror("Ошибка симуляции", f"Ошибка: {str(e)}")
            import traceback
            traceback.print_exc()
            self.fire_start_btn.config(state="normal", text=f"{self.t('start_fire')}   🔥")
        
        finally:
            self.is_fire_running = False


    def reset_fire_simulation(self, graph):
        """Сбрасывает симуляцию пожара"""
        self.burning_nodes.clear()
        self.burned_edges.clear()
        self.fire_iteration = 0
        self.max_fire_iteration = 0
        self.fire_spread_history = []
        self.is_fire_running = False
        
        self.stats_manager.reset_fire_statistics()
        
        if hasattr(self, 'graph_ax') and hasattr(self, 'graph_fig'):
            self.graph_ax.clear()
            self.draw_graph(self.graph_ax, graph, show_fire=False)
            self.graph_canvas.draw()
        
        if hasattr(self, 'fire_start_btn'):
            self.fire_start_btn.config(state="normal", text=f"{self.t('start_fire')}   🔥")

    def generate_new_graph(self):
        """Генерирует новый граф с теми же параметрами"""
        try:
            # Сохраняем текущее состояние перед генерацией
            current_vertex = self.start_vertex.get()
            self._reset_simulation_state()
            n_nodes = self.vertex_count.get()
            # Параметры ребер
            edge_dist = self.edge_distribution.get()
            edge_params = self.dist_manager.get_edge_distribution_params(edge_dist)
            # Параметры вершин
            vertex_dist = self.vertex_distribution.get()
            vertex_dist_eng = self.translator.get_english_key(vertex_dist)
            vertex_func = self.dist_manager.get_vertex_weight_func(vertex_dist_eng, n_nodes)
            # Создаем новый граф через менеджер распределений
            graph, base_node_weights = self.dist_manager.create_graph_with_weights(n_nodes, edge_params, vertex_func)
            
            # Применяем веса вершин с учетом устойчивости и влияния
            if vertex_dist_eng != 'None' and base_node_weights:
                self.node_weights = self.calculate_adjusted_vertex_weights(base_node_weights)
                for node_id, weight in self.node_weights.items():
                    if node_id in graph.nodes():
                        graph.nodes[node_id]['weight'] = weight
            else:
                self.node_weights = base_node_weights if base_node_weights else {}
            
            # Обновляем текущий граф
            self.current_graph = graph
            self._last_graph = None
            self.current_graph = graph
            self.node_weights = self.node_weights
            # Перестраиваем интерфейс на вкладке симуляции
            self._build_simulation_tab_content()
            
            if hasattr(self, 'graph_legend_widget'):
                self.graph_legend_widget.set_current_graph(graph)
                self.root.after(250, lambda: self.graph_legend_widget.update_histogram('edge', graph))
                self.root.after(250, lambda: self.graph_legend_widget.update_histogram('vertex', graph))
            
            # Обновляем максимальное значение для слайдера стартовой вершины
            max_vertices = graph.number_of_nodes()
            self.start_vertex.set(min(current_vertex, max_vertices))
            if hasattr(self, 'start_vertex_slider') and self.start_vertex_slider.winfo_exists():
                self.start_vertex_slider.config(to=max_vertices)
            # Обновляем статистику стартовой вершины
            self.stats_manager.update_start_vertex_stats(graph, self.start_vertex.get() - 1, self.node_weights)
            # Сбрасываем кэш позиций графа
            self._graph_positions_cache = None
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать новый граф:\n{str(e)}")
            import traceback
            traceback.print_exc()


    def draw_fire_on_graph(self, graph):
        """Перерисовывает граф с отображением пожара"""
        if not hasattr(self, 'graph_ax') or not hasattr(self, 'graph_canvas'):
            return
        self.graph_ax.clear()
        self.draw_graph(self.graph_ax, graph, show_fire=True)
        self.graph_canvas.draw()

    def draw_graph(self, ax, graph, show_fire=True):
        """Рисует граф на axes matplotlib"""
        import matplotlib.pyplot as plt
        ax.clear()
        if not hasattr(self, '_graph_positions_cache') or self._graph_positions_cache is None:
            self._graph_positions_cache = nx.spring_layout(graph, seed=42)
        pos = self._graph_positions_cache
        
        # Рисует НЕ горящие ребра
        edges = list(graph.edges(data=True))
        if self.show_negative_edges:
            filtered_edges = edges
        else:
            filtered_edges = [(u, v, data) for u, v, data in edges if data['weight'] > 0]
        
        if filtered_edges:
            edge_weights = [data['weight'] for _, _, data in filtered_edges]
            edge_list = [(u, v) for u, v, _ in filtered_edges]
            try:
                cmap = matplotlib.colormaps.get_cmap(self.theme_manager.get_palette('edge_cmap'))
            except (AttributeError, KeyError):
                try:
                    cmap = matplotlib.colormaps[self.theme_manager.get_palette('edge_cmap')]
                except (AttributeError, KeyError):
                    cmap = plt.cm.get_cmap(self.theme_manager.get_palette('edge_cmap'))
            
            # Нормализация к 0..1 для цветовой шкалы
            all_edge_colors = [cmap((w + 1) / 2) for w in edge_weights]
            all_edge_widths = [abs(w) * 0.5 + 0.5 for w in edge_weights]
            
            nx.draw_networkx_edges(graph, pos, ax=ax, edgelist=edge_list, edge_color=all_edge_colors, 
                                   width=all_edge_widths, alpha=0.8, arrows=False)
        
        if self.theme_manager.theme == 'dark':
            RED_START = 0.9
            YELLOW_END = 0.3
            vertex_color = self.theme_manager.get_color('graph_vertex')
            vertex_border = self.theme_manager.get_color('graph_vertex_border')
        else:
            RED_START = 1.0
            YELLOW_END = 0.1
            vertex_color = self.theme_manager.get_color('graph_vertex')
            vertex_border = self.theme_manager.get_color('graph_vertex_border')
        
        # Рисуем ГОРЯЩИЕ ребра
        if show_fire and hasattr(self, 'burned_edges') and self.burned_edges:
            import matplotlib.pyplot as plt
            burning_edges_by_target = {}
            burning_edge_weights_by_target = {}
            burning_edge_iterations = {}
            all_edge_iterations = []
            
            for (u, v), iteration in self.burned_edges.items():
                if graph.has_edge(u, v):
                    weight = graph.edges[(u, v)]['weight']
                    if not self.show_negative_edges and weight <= 0:
                        continue
                    
                    u_iter = self.burning_nodes.get(u, float('inf'))
                    v_iter = self.burning_nodes.get(v, float('inf'))
                    
                    if u_iter < v_iter:
                        source, target = u, v
                        target_iter = v_iter
                    elif v_iter < u_iter:
                        source, target = v, u
                        target_iter = u_iter
                    else:
                        continue
                    
                    if target not in burning_edges_by_target:
                        burning_edges_by_target[target] = []
                        burning_edge_weights_by_target[target] = []
                        burning_edge_iterations[target] = []
                    
                    burning_edges_by_target[target].append((source, target))
                    burning_edge_weights_by_target[target].append(weight)
                    burning_edge_iterations[target].append(target_iter)
                    all_edge_iterations.append(target_iter)
            
            # Рисуем ребра
            for target, edges_list in burning_edges_by_target.items():
                if edges_list:
                    weights = burning_edge_weights_by_target[target]
                    iterations = burning_edge_iterations[target]
                    
                    edge_colors = []
                    for iteration in iterations:
                        if self.max_fire_iteration > 0 and len(set(all_edge_iterations)) > 0:
                            unique_iters = sorted(set(all_edge_iterations))
                            if len(unique_iters) == 1:
                                normalized = YELLOW_END
                            else:
                                order_index = unique_iters.index(iteration)
                                t = order_index / (len(unique_iters) - 1)
                                normalized = RED_START - t * (RED_START - YELLOW_END)
                            
                            normalized = max(0.0, min(1.0, normalized))
                            color = plt.cm.YlOrRd(normalized)
                        else:
                            normalized = RED_START - 0.5 * (RED_START - YELLOW_END)
                            color = plt.cm.YlOrRd(normalized)
                        edge_colors.append(color)
                    
                    nx.draw_networkx_edges(
                        graph, pos, ax=ax,
                        edgelist=edges_list,
                        edge_color=edge_colors,
                        width=[abs(w) * 1.0 + 1.5 for w in weights],
                        alpha=1.0,
                        arrows=False
                    )
        
        # Рисуем НЕ горящие вершины
        non_burning_nodes = []
        if show_fire and hasattr(self, 'burning_nodes'):
            non_burning_nodes = [n for n in graph.nodes() if n not in self.burning_nodes]
        else:
            non_burning_nodes = list(graph.nodes())
        
        label_font_size = 8
        label_font_weight = 'bold'
        label_color = self.theme_manager.get_color('plot_text')
        
        if self.node_weights and len(self.node_weights) > 0 and non_burning_nodes:
            min_size, max_size = 100, 800
            node_sizes = []
            nodes_to_draw = []
            
            for node in non_burning_nodes:
                if node in self.node_weights:
                    weight = self.node_weights[node]
                    try:
                        weight_float = float(weight)
                    except (ValueError, TypeError):
                        weight_float = 0.5
                    
                    scaled_weight = max(0.0, min(1.0, weight_float))
                    node_size = min_size + scaled_weight * (max_size - min_size)
                    node_sizes.append(node_size)
                    nodes_to_draw.append(node)
            
            if nodes_to_draw:
                nx.draw_networkx_nodes(graph, pos, ax=ax, nodelist=nodes_to_draw, node_size=node_sizes, node_color=vertex_color,
                                       alpha=1.0, edgecolors=vertex_border, linewidths=0.5,)
                for node in nodes_to_draw:
                    x, y = pos[node]
                    try:
                        node_num = int(node[1:]) + 1
                    except:
                        node_num = node
                    if node in self.node_weights:
                        weight = self.node_weights[node]
                        try:
                            weight_float = float(weight)
                        except (ValueError, TypeError):
                            weight_float = 0.5
                        scaled_weight = max(0.0, min(1.0, weight_float))
                        font_size = label_font_size + int(scaled_weight * 2)
                    else:
                        font_size = label_font_size
                    ax.text(x, y, str(node_num), fontsize=font_size, fontweight=label_font_weight, ha='center', va='center', color=label_color)
        else:
            if non_burning_nodes:
                nx.draw_networkx_nodes(graph, pos, ax=ax, nodelist=non_burning_nodes, node_color=vertex_color,
                                       node_size=400, alpha=1.0, edgecolors=vertex_border, linewidths=0.5,)
                labels = {}
                for node in non_burning_nodes:
                    try:
                        node_num = int(node[1:]) + 1
                        labels[node] = str(node_num)
                    except:
                        labels[node] = node
                nx.draw_networkx_labels(graph, pos, ax=ax, labels=labels, font_size=label_font_size,
                                        font_weight=label_font_weight, font_color=label_color)
        
        # Рисуем ГОРЯЩИЕ вершины
        if show_fire and hasattr(self, 'burning_nodes') and self.burning_nodes:
            burning_items = sorted(self.burning_nodes.items(), key=lambda x: x[1])
            
            burning_nodes_list = []
            burning_sizes = []
            burning_colors = []
            
            # Уникальные итерации для вычисления порядка
            all_iterations = [iteration for _, iteration in burning_items]
            
            for node, iteration in burning_items:
                if node in graph.nodes():
                    burning_nodes_list.append(node)
                    node_size = 400
                    if self.node_weights and node in self.node_weights:
                        weight = self.node_weights[node]
                        try:
                            weight_float = float(weight)
                        except (ValueError, TypeError):
                            weight_float = 0.5
                        min_size, max_size = 100, 800
                        scaled_weight = max(0.0, min(1.0, weight_float))
                        node_size = min_size + scaled_weight * (max_size - min_size)
                    burning_sizes.append(node_size)
                    
                    if len(all_iterations) > 0:
                        # Относительный порядок этой вершины
                        unique_iters = sorted(set(all_iterations))
                        if len(unique_iters) == 1:
                            normalized = RED_START
                        else:
                            # Порядковый номер этой итерации среди всех итераций
                            order_index = unique_iters.index(iteration)
                            t = order_index / (len(unique_iters) - 1)
                            # Инвертируем. красный (первые), желтый (последние)
                            normalized = RED_START - t * (RED_START - YELLOW_END)
                        normalized = max(0.0, min(1.0, normalized))
                        vertex_color_fire = plt.cm.YlOrRd(normalized)
                    else:
                        # Средний цвет
                        normalized = RED_START - 0.5 * (RED_START - YELLOW_END)
                        vertex_color_fire = plt.cm.YlOrRd(normalized)
                    burning_colors.append(vertex_color_fire)
            
            if burning_nodes_list:
                nx.draw_networkx_nodes(graph, pos, ax=ax, nodelist=burning_nodes_list, node_size=burning_sizes, 
                                       node_color=burning_colors, edgecolors=vertex_border, linewidths=0.5, alpha=1.0)
                for node, iteration in burning_items:
                    if node in graph.nodes():
                        x, y = pos[node]
                        try:
                            node_num = int(node[1:]) + 1
                        except:
                            node_num = node
                        font_size = label_font_size
                        if self.node_weights and node in self.node_weights:
                            weight = self.node_weights[node]
                            try:
                                weight_float = float(weight)
                            except (ValueError, TypeError):
                                weight_float = 0.5
                            scaled_weight = max(0.0, min(1.0, weight_float))
                            font_size = label_font_size + int(scaled_weight * 2)
                        ax.text(x, y, str(node_num), fontsize=font_size, fontweight=label_font_weight, ha='center', va='center', color=label_color)
        # Настройки осей
        ax.set_axis_off()
        ax.set_aspect('auto')
        ax.margins()
        self.graph_fig.tight_layout(pad=-5, rect=[0.11, 0.1, 0.85, 0.9])
        ax.figure.canvas.draw_idle()


# In[20]:


def main():
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно
    
    try:
        # Экран загрузки
        splash = SplashScreen(root)
        # Обновляем окно, чтобы splash screen отобразился
        root.update_idletasks()
        
        # Имитация процесса загрузки
        for step in range(1, splash.vertex_count + 1):
            splash.update_progress(step)
            splash.splash.update()
            root.update_idletasks()
            root.after(200)  # Пауза 200 мс между шагами
        
        # Пауза перед закрытием splash screen
        root.after(300)
        # Закрываем splash screen
        splash.close()
        
        # Создаем основное приложение
        app = GraphBuilderApp(root)
        # Показываем главное окно
        root.deiconify()
        # Запускаем главный цикл
        root.mainloop()
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()
        try:
            splash.close()
        except:
            pass
            
        # Показываем главное окно даже при ошибке
        root.deiconify()
        messagebox.showerror("Ошибка запуска", f"Не удалось запустить приложение:\n{str(e)}")
        root.destroy()

        

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




