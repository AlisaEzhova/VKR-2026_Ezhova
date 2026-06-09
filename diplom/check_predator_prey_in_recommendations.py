"""
check_predator_prey_in_recommendations.py

Проверка: есть ли треки-хищники или жертвы среди рекомендаций пользователей
"""

import pickle

# Загрузка кэша с данными
CACHE_FILE = "processed_data_task4.pkl"

print("Загрузка данных из кэша...")
with open(CACHE_FILE, "rb") as f:
    cached = pickle.load(f)
filtered_user_likes = cached["filtered_user_likes"]
filtered_user_dislikes = cached["filtered_user_dislikes"]
filtered_user_strong = cached["filtered_user_strong"]
print("  Данные загружены")
print()

# Списки хищников и жертв из Task 3 (таблица 3.2 ВКР)
predators = [3882210, 1874437]
preys = [4767032, 8250570, 1525699]

print("ИЗВЕСТНЫЕ ХИЩНИКИ И ЖЕРТВЫ (из Task 3):")
print(f"  Хищники: {predators}")
print(f"  Жертвы: {preys}")
print()

# Функция для получения рекомендаций для пользователя
def get_recommendations(user_id, use_H3=False, use_H5=False, use_H6=False):
    from system import RecommenderSystem
    
    config = {
        'max_recommendations': 10,
        'fail_limit': 3,
        'strategy': 'greedy',
        'min_common': 1,
        'max_neighbors': None,
        'use_H1': True,
        'use_H2': True,
        'use_H3': use_H3,
        'use_H4': True,
        'use_H5': use_H5,
        'use_H6': use_H6,
    }
    
    system = RecommenderSystem(config)
    system.fit(filtered_user_likes, user_strong=filtered_user_strong, user_dislikes=filtered_user_dislikes)
    recommendations, _ = system.recommend(target_user=user_id)
    return recommendations

# Пользователи для проверки
test_users = [
    (55500, "55500 (5 лайков)"),
    (31300, "31300 (3 лайка)"),
    (39400, "39400 (162 лайка)"),
]

print("ПОИСК ПЕРЕСЕЧЕНИЙ С ХИЩНИКАМИ И ЖЕРТВАМИ")
print()

all_recommended_tracks = set()

for user_id, user_desc in test_users:
    print(f"Пользователь: {user_desc} (ID: {user_id})")
    
    # Получаем рекомендации для разных конфигураций
    recs_base = get_recommendations(user_id, use_H3=False, use_H5=False, use_H6=False)
    recs_h3 = get_recommendations(user_id, use_H3=True, use_H5=False, use_H6=False)
    recs_h6 = get_recommendations(user_id, use_H3=False, use_H5=False, use_H6=True)
    recs_all = get_recommendations(user_id, use_H3=True, use_H5=True, use_H6=True)
    
    all_recs = set(recs_base + recs_h3 + recs_h6 + recs_all)
    all_recommended_tracks.update(all_recs)
    
    # Проверяем пересечения
    pred_intersection = all_recs.intersection(predators)
    prey_intersection = all_recs.intersection(preys)
    
    print(f"  Всего уникальных рекомендованных треков: {len(all_recs)}")
    print(f"  Из них хищников: {pred_intersection if pred_intersection else 'нет'}")
    print(f"  Из них жертв: {prey_intersection if prey_intersection else 'нет'}")
    print()

print(f"ИТОГО уникальных треков во всех рекомендациях: {len(all_recommended_tracks)}")
print()

final_pred_intersection = all_recommended_tracks.intersection(predators)
final_prey_intersection = all_recommended_tracks.intersection(preys)

print("ОБЩЕЕ ПЕРЕСЕЧЕНИЕ:")
print(f"  Хищники в рекомендациях: {final_pred_intersection if final_pred_intersection else 'нет'}")
print(f"  Жертвы в рекомендациях: {final_prey_intersection if final_prey_intersection else 'нет'}")