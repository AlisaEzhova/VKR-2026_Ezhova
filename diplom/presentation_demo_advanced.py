"""
presentation_all_combinations.py

ДЛЯ ПРЕЗЕНТАЦИИ
"""

from system import RecommenderSystem
from collections import defaultdict
import pickle
import os
import itertools

print("ПРЕЗЕНТАЦИЯ: ВСЕ ВОЗМОЖНЫЕ КОМБИНАЦИИ ГИПОТЕЗ")
print("(H1 всегда включена, так как без неё система не работает)")
print()

CACHE_FILE = "processed_data_task4.pkl"

if not os.path.exists(CACHE_FILE):
    print("Ошибка: кэш не найден.")
    exit()

print("Загрузка данных из кэша...")
with open(CACHE_FILE, "rb") as f:
    cached = pickle.load(f)
filtered_user_likes = cached["filtered_user_likes"]
filtered_user_dislikes = cached["filtered_user_dislikes"]
filtered_user_strong = cached["filtered_user_strong"]
print("  Данные загружены")
print()

# Пользователи из таблицы 3.1 ВКР
demo_users = [
    (55500, "55500 (5 лайков)"),
    (31300, "31300 (3 лайка)"),
    (39400, "39400 (162 лайка)"),
    (52300, "52300 (63 лайка)"),
    (18600, "18600 (41 лайк)"),
]

# Все комбинации H2, H3, H4, H5, H6 (2^5 = 32)
hypotheses = ['H2', 'H3', 'H4', 'H5', 'H6']
combinations = []
for r in range(len(hypotheses) + 1):
    for combo in itertools.combinations(hypotheses, r):
        combinations.append(combo)

print(f"Всего комбинаций: {len(combinations)} (H1 всегда включён)")
print()

for user_id, user_desc in demo_users:
    if user_id not in filtered_user_likes:
        print(f"Пользователь {user_id} не найден в выборке, пропускаем")
        continue
    
    likes_count = len(filtered_user_likes.get(user_id, set()))
    dislikes_count = len(filtered_user_dislikes.get(user_id, set()))
    strong_count = len(filtered_user_strong.get(user_id, set()))
    
    print(f"\nПОЛЬЗОВАТЕЛЬ: {user_desc} (ID: {user_id})")
    print(f"  Лайков: {likes_count}, Дизлайков: {dislikes_count}, Strong: {strong_count}")
    print()
    print(f"Комбинация                      Первые 5 рекомендаций")
    print()
    
    for combo in combinations:
        if not combo:
            combo_name = "Только H1"
        else:
            combo_name = "H1 + " + " + ".join(sorted(combo))
        
        use_H2 = 'H2' in combo
        use_H3 = 'H3' in combo
        use_H4 = 'H4' in combo
        use_H5 = 'H5' in combo
        use_H6 = 'H6' in combo
        
        config = {
            'max_recommendations': 10,
            'fail_limit': 3,
            'strategy': 'greedy',
            'min_common': 1,
            'max_neighbors': None,
            'use_H1': True,
            'use_H2': use_H2,
            'use_H3': use_H3,
            'use_H4': use_H4,
            'use_H5': use_H5,
            'use_H6': use_H6,
        }
        
        system = RecommenderSystem(config)
        system.fit(filtered_user_likes, user_strong=filtered_user_strong, user_dislikes=filtered_user_dislikes)
        recommendations, _ = system.recommend(target_user=user_id)
        
        recs_str = str(recommendations[:5]) if recommendations else "[]"
        print(f"{combo_name:<35} {recs_str}")
    
    print()

print("ВЫВОДЫ:")
print("- H1 — обязательная базовая гипотеза (без неё нет соседей)")
print("- H2, H3, H4, H5, H6 могут включаться в любых сочетаниях")
print("- Результаты показывают, как каждая гипотеза влияет на рекомендации")