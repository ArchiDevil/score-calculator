# в эти функции приходят только числа
def predict_points(array_ideal_points, workdays, missing_array):
    """
    Предсказывает количество очков на следующий спринт

    Параметры:
    array_ideal_points -- массив с 4 или менее значениями идеальных спринтов
    workdays           -- количество рабочих дней
    missing_array      -- количество пропускаемых дней каждого учатника
    """
    if not missing_array or not array_ideal_points:
        raise RuntimeError("No data")

    members = len(missing_array)
    number_of_sprints = len(array_ideal_points)
    middle_points = 0
    for ideal_point in array_ideal_points:
        middle_points = middle_points + ideal_point/number_of_sprints


    middle_days = 0
    for missing in missing_array:
        middle_days = middle_days + (workdays-missing)/(workdays*members)


    predicted_points = int(middle_points*middle_days)
    return predicted_points


def calculate_points(real_score, totaldays, missing_array):
    """
    Вычисляет идеальное количество очков

    Параметры:
    real_score    -- реальное количестов очков
    totaldays     -- количество рабочих дней в спринте
    missing_array -- массив с количеством пропущенных дней от каждого разработчика
    """
    if not missing_array:
        raise RuntimeError("No data")

    number_members = len(missing_array)
    sum = 0

    for missing in missing_array:
        sum += (totaldays - missing) / (totaldays*number_members)
    if sum==0:
        return False
    ideal_score = int(real_score/sum)
    return ideal_score
