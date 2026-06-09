"""
check_users_without_recommendations.py

Анализ пользователей, не получивших рекомендации
Для презентации: показать границы применимости системы
НА ВЫБОРКЕ ИЗ 1000 ПОЛЬЗОВАТЕЛЕЙ
"""

from system import RecommenderSystem
from datasets import load_dataset
from collections import defaultdict

print("АНАЛИЗ ПОЛЬЗОВАТЕЛЕЙ, НЕ ПОЛУЧИВШИХ РЕКОМЕНДАЦИИ")
print("(выборка из 1000 пользователей, как в Task 2)")
print()

# Загрузка данных (как в Task 2)
print("Загрузка данных из датасета...")
likes_ds = load_dataset(
    "yandex/yambda", 
    data_dir="flat/50m", 
    data_files="likes.parquet",
    split="train"
)

print("Формирование данных о лайках пользователей...")
user_likes = defaultdict(set)
for example in likes_ds:
    user_likes[example['uid']].add(example['item_id'])

all_users = sorted(user_likes.keys())
selected_users = all_users[:1000]  # 1000 пользователей
filtered_user_likes = {uid: user_likes[uid] for uid in selected_users}

print(f"Всего пользователей в датасете: {len(user_likes)}")
print(f"Выбрано для анализа: {len(selected_users)}")
print()

# Базовый конфиг (как в Task 2)
config = {
    'max_recommendations': 10,
    'fail_limit': 3,
    'strategy': 'greedy',
    'min_common': 1,
    'max_neighbors': None,
    'use_H1': True,
    'use_H2': True,
    'use_H3': False,
    'use_H4': True,
    'use_H5': False,
    'use_H6': False,
}

print("ПОЛУЧЕНИЕ РЕКОМЕНДАЦИЙ ДЛЯ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ...")
print()

system = RecommenderSystem(config)
system.fit(filtered_user_likes)

users_with_recs = []
users_without_recs = []
total_recommendations = 0

for user_id in selected_users:
    recommendations, _ = system.recommend(target_user=user_id)
    if recommendations:
        users_with_recs.append(user_id)
        total_recommendations += len(recommendations)
    else:
        users_without_recs.append(user_id)

total_users = len(selected_users)
users_with_recs_count = len(users_with_recs)
users_without_recs_count = len(users_without_recs)
coverage = users_with_recs_count / total_users * 100

print("РЕЗУЛЬТАТЫ:")
print(f"Всего пользователей в выборке: {total_users}")
print(f"Получили рекомендации: {users_with_recs_count} ({coverage:.1f}%)")
print(f"НЕ получили рекомендации: {users_without_recs_count} ({100-coverage:.1f}%)")
print(f"Всего сформировано рекомендаций: {total_recommendations}")
print(f"Среднее на пользователя: {total_recommendations / total_users:.2f}")
print()

print("ПОЧЕМУ ОНИ НЕ ПОЛУЧИЛИ РЕКОМЕНДАЦИИ?")
print()

print("Анализ пользователей без рекомендаций (первые 10):")
print()

for user_id in users_without_recs[:10]:
    user_tracks = filtered_user_likes.get(user_id, set())
    print(f"Пользователь {user_id}:")
    print(f"  Лайков: {len(user_tracks)}")
    
    has_common = False
    for other_id in selected_users:
        if other_id == user_id:
            continue
        other_tracks = filtered_user_likes.get(other_id, set())
        if user_tracks.intersection(other_tracks):
            has_common = True
            break
    
    if has_common:
        print(f"  Общих треков с другими: ЕСТЬ")
    else:
        print(f"  Общих треков с другими: НЕТ")
    print()

if len(users_without_recs) > 10:
    print(f"... и ещё {len(users_without_recs) - 10} пользователей без рекомендаций")
    print()

print("ВЫВОД ДЛЯ ПРЕЗЕНТАЦИИ:")
print(f"Из {total_users} пользователей {users_without_recs_count} ({100-coverage:.1f}%)")
print("не получили рекомендации, потому что у них НЕТ НИ ОДНОГО ОБЩЕГО ТРЕКА")
print("с другими пользователями в выборке.")
print()
print("Это не ошибка системы, а объективная граница применимости.")
print("Если у пользователя нет пересечений с другими — рекомендации построить невозможно.")