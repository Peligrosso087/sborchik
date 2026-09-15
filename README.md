# Сборщик костей

Аддон для **Blender 5.2 LTS**. Собирает кости арматуры в коллекции и строит анатомический гуманоидный скелет.

Работает с Mixamo, Rigify-префиксами и именами Blender. Красит кости по группам, прячет механику, умеет переназначать коллекции.

## Установка

1. Скачай [`collector.py`](./collector.py).
2. Blender → **Edit → Preferences → Add-ons**.
3. **Install from Disk** → выбери `collector.py`.
4. Включи **Сборщик костей**.
5. В 3D Viewport нажми **N** — вкладка **Сборщик**.

## Что умеет

| Кнопка | Действие |
| --- | --- |
| **Собрать кости** | Раскладывает кости активной арматуры по коллекциям |
| **Создать скелет** | Строит гуманоид 1.8 м, 53 кости, пальцы, octahedral display |
| **Очистить коллекции** | Снимает только коллекции сборщика |

Чекбоксы на панели:

- **Переназначить** — сначала снимает старые коллекции сборщика
- **Окрасить кости** — кастомные цвета по группам
- **Скрыть механизмы** — прячет коллекции IK / Механика

Кликни имя коллекции в списке — выделятся её кости в Pose Mode.

## Коллекции

Корень · Позвоночник · Голова · Рука L/R · Кисть L/R · Нога L/R · IK · Механика · без группы

Схема анатомическая, конвенция имён — Blender (`spine.001`, `upper_arm.L`, `thumb.01.L` …). Правила также ловят Mixamo (`mixamorig:LeftArm`) и Rigify (`DEF-`, `ORG-`, `MCH-`).

## Совместимость

- Blender **5.2** и новее (Bone Collections API)
- Один файл, без зависимостей
- Установка как классический add-on (`bl_info`)

---

# Bone Collector

Blender **5.2 LTS** add-on. Sorts armature bones into collections and builds an anatomical humanoid skeleton.

## Install

1. Download [`collector.py`](./collector.py).
2. **Edit → Preferences → Add-ons → Install from Disk**.
3. Enable **Сборщик костей**.
4. 3D Viewport → **N** → **Сборщик**.

**Collect Bones** classifies the active armature. **Create Skeleton** builds a 1.8 m humanoid (53 bones, fingers, octahedral). MIT license.
