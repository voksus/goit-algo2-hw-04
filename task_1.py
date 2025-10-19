import networkx as nx
import matplotlib.pyplot as plt

# Очищуємо консоль
print('\033c', end='', flush=True)

# --- Налаштування кольорів для консолі ---
RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'
ITALIC = '\033[3m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
BLUE   = '\033[34m'
RED    = '\033[31m'

# --- 1. Створення та Моделювання Графа ---
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю (capacity)
# Формат: (джерело, стік, пропускна_здатність)
base_edges = [
    (14,  0, 15),  (14,  1, 10),  (14,  2, 20),  # Склад 1 -> Магазини
    (15,  3, 15),  (15,  4, 10),  (15,  5, 25),  # Склад 2 -> Магазини
    (16,  6, 20),  (16,  7, 15),  (16,  8, 10),  # Склад 3 -> Магазини
    (17,  9, 20),  (17, 10, 10),  (17, 11, 15),  (17, 12,  5),  (17, 13, 10), # Склад 4 -> Магазини
    (18, 14, 25),  (18, 15, 20),  (18, 16, 15),  # Термінал 1 -> Склади
    (19, 15, 10),  (19, 16, 15),  (19, 17, 30),  # Термінал 2 -> Склади
]

# Додаємо ребра. Використовуємо 'capacity' для обчислення потоку та 'weight' для міток
G.add_edges_from([(u, v, {'capacity': c, 'weight': c}) for u, v, c in base_edges])

# --- 2. Моделювання Суперджерела (SS) та Суперстоку (T) ---
# Для перетворення Multi-Source Multi-Sink на Single-Source Single-Sink
SS = 20  # Суперджерело
T  = 21  # Суперстік
INF = float('inf') # Нескінченна пропускна здатність/потреба

# 2.1. З'єднання Терміналів (18, 19) із Суперджерелом (SS)
G.add_edge(SS, 18, capacity=INF, weight='INF') # SS -> Термінал 1
G.add_edge(SS, 19, capacity=INF, weight='INF') # SS -> Термінал 2

# 2.2. З'єднання Магазинів (0-13) із Суперстоком (T)
store_nodes = list(range(14))
for store_node in store_nodes:
    G.add_edge(store_node, T, capacity=INF, weight='INF')

# --- 3. Позиції та Мітки ---
pos = {
     # Магазини (0-13)
     0: ( 1, 4),  1: ( 2, 4),  2: ( 3, 4),  3: ( 4, 4),  4: ( 5, 4),
     5: ( 6, 4),  6: ( 0, 0),  7: ( 1, 0),  8: ( 2, 0),  9: ( 3, 0),
    10: ( 4, 0), 11: ( 5, 0), 12: ( 6, 0), 13: ( 7, 0),
    # Склади (14-17)
    14: (2.5, 3), 15: (4.5, 3), 16: (2.5, 1), 17: (4.5, 1),
    # Термінали (18, 19)
    18: (1.5, 2), 19: (5.5, 2),
    # Віртуальні вузли (20, 21) - потрібні лише для моделювання, не для малювання
    SS: (3.5, 6),   
    T:  (3.5, -2),  
}

lb = ['Магазин ', 'Склад ', 'Термінал ']
node_labels = {
     # Магазини
     0: f'{lb[0]}1' ,    1: f'{lb[0]}2' ,    2: f'{lb[0]}3' ,    3: f'{lb[0]}4' ,   4: f'{lb[0]}5' ,
     5: f'{lb[0]}6' ,    6: f'{lb[0]}7' ,    7: f'{lb[0]}8' ,    8: f'{lb[0]}9' ,   9: f'{lb[0]}10',
    10: f'{lb[0]}11',   11: f'{lb[0]}12',   12: f'{lb[0]}13',   13: f'{lb[0]}14',
    # Склади
    14: f'{lb[1]}1' ,   15: f'{lb[1]}2' ,   16: f'{lb[1]}3' ,   17: f'{lb[1]}4' ,
    # Термінали
    18: f'{lb[2]}1' ,   19: f'{lb[2]}2' ,
    # Віртуальні вузли
    SS: 'СУПЕРДЖЕРЕЛО',
    T:  'СУПЕРСТІК',
}

# --- 4. Обчислення Максимального Потоку ---
# За допомогою `networkx.maximum_flow` знаходимо максимальний потік
flow_value, flow_dict = nx.maximum_flow(G, SS, T, capacity='capacity')
min_cut_value, partition = nx.minimum_cut(G, SS, T, capacity='capacity')

# --- 5. Аналіз Результатів для Звіту ---
print(f'{BOLD}{BLUE}--- АНАЛІЗ МАКСИМАЛЬНОГО ПОТОКУ (МЕРЕЖЕВА ЗДАТНІСТЬ) ---{RESET}\n')
print('Мережа: 2 Термінали, 4 Склади, 14 Магазинів')
print(f'{ITALIC+DIM}> Змодельовано на 22 вершинах.{RESET}')
print(f'{ITALIC}  Де до реальних 20-ти додано ще два віртуальних:\n   * Суперджерело\n   * Суперстік.{RESET}')
print('\n---\n')

# 5.1. Загальний Максимальний Потік
print(f'{BOLD}{GREEN}1. ЗАГАЛЬНИЙ МАКСИМАЛЬНИЙ ПОТІК:{RESET}')
print(f'   Загальна здатність мережі: {BOLD}{flow_value}{RESET} умовних одиниць.')
print(f'{ITALIC+DIM}   (Відповідно до Min-Cut теореми, мінімальний розріз: {min_cut_value}){RESET}')

# 5.2. Розподіл потоку від Терміналів
t1_flow = flow_dict[SS].get(18, 0)
t2_flow = flow_dict[SS].get(19, 0)

print(f'\n{BOLD}{GREEN}2. ПОТІК, ЩО ВИХОДИТЬ З ТЕРМІНАЛІВ:{RESET}')
print(f'   - Потік з {node_labels[18]} (Термінал 1): {BOLD}{t1_flow}{RESET}')
print(f'   - Потік з {node_labels[19]} (Термінал 2): {BOLD}{t2_flow}{RESET}')


# 5.3. Отриманий потік Магазинами
print(f'\n{BOLD}{GREEN}3. ПОТІК, ОТРИМАНИЙ МАГАЗИНАМИ:{RESET}')
for store_node in store_nodes:
    # Потік до магазину - це потік по ребру 'Магазин -> Суперстік'
    flow_to_store = flow_dict.get(store_node, {}).get(T, 0)
    print(f'   - {node_labels[store_node]:<12} (Вершина {store_node:>2}): {flow_to_store}')

# 5.4. Аналіз вузьких місць (Min-Cut)
reachable, unreachable = partition
cut_set = set()
for u, v in G.edges():
    if u in reachable and v in unreachable:
        cut_set.add((u, v))

print(f'\n{BOLD}{GREEN}4. АНАЛІЗ ВУЗЬКИХ МІСЦЬ (МІНІМАЛЬНИЙ РОЗРІЗ):{RESET}')
print(f'   Ребра, що формують Min-Cut (критичні вузькі місця):')

internal_cut_labels = []
for u, v in cut_set:
    capacity = G[u][v].get('capacity', 0)
    if capacity != INF:
        u_label = node_labels.get(u, u)
        v_label = node_labels.get(v, v)
        internal_cut_labels.append(f'   - {u_label} ({u}) -> {v_label} ({v}) [Cap: {capacity}]')
    
if internal_cut_labels:
    for label in internal_cut_labels:
        print(f'{YELLOW}{label}{RESET}')
    print()
else:
    print('   - Усі внутрішні ребра мають запас пропускної здатності, вузьке місце поза логістикою (в моделі INF).\n')


# --- 6. Візуалізація Графа (Тільки Основна Мережа) ---

nodes_to_draw = G.nodes() - {SS, T}
subgraph = G.subgraph(nodes_to_draw)

edge_labels_flow = {}
for u, v in subgraph.edges():
    capacity = G[u][v].get('capacity', 0)
    flow = flow_dict.get(u, {}).get(v, 0)
    edge_labels_flow[(u, v)] = f'{flow}/{capacity}' # Потік/Capacity

node_colors = ['skyblue' if n < 14 else 'lightcoral' if n < 18 else 'lightgreen' for n in subgraph.nodes()]
node_size = [1800 if n < 14 else 2200 for n in subgraph.nodes()] # Магазини менші

plt.figure(figsize=(14, 9))
plt.title(f'Максимальний Потік в Основній Мережі (Max Flow: {flow_value})', fontsize=16)

nx.draw(
    subgraph, pos,
    labels      = node_labels,
    node_size   = node_size,
    node_color  = node_colors,
    font_size   = 10,
    font_weight = 'bold',
    arrows      = True,
    font_color  = 'black',
    with_labels = True,
)

# Малювання міток ребер: Потік/Пропускна здатність
nx.draw_networkx_edge_labels(
    subgraph, pos,
    edge_labels = edge_labels_flow,
    font_color  = 'blue',
    font_size   = 10,
    bbox        = {'facecolor' : 'white',
                   'alpha'     : 0.8,
                   'edgecolor' : 'none'}
)

plt.show()
