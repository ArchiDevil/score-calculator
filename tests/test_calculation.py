from flaskr.calculation import predict_points, calculate_points
# predict_points - формула для старта
# calculate_points - формула для финиша

#START

# Передаем правильные данные в старт


def test_calculating_predicted_points():
    # 4 спринта
    result = predict_points(array_ideal_points=[4, 8, 12, 16],
                            workdays=10,
                            missing_array=[0, 0])
    assert result == 10

    # меньше, чем 4 спринта
    result = predict_points(array_ideal_points=[3, 6, 9],
                            workdays=100,
                            missing_array=[10, 10])
    assert result == 5


# Передаем не правильные данные в старт
def test_calculating_predicted_points_false():
    # missing_array ничего не передано
    try:
        predict_points(array_ideal_points=[3, 6, 9],
                       workdays="10",
                       missing_array=[])
        assert False
    except:
        pass

    # спринтов = 0
    try:
        predict_points(array_ideal_points=[],
                       workdays="10",
                       missing_array=[5, 1])
        assert False
    except:
        pass

    # workdays ничего не передано
    try:
        predict_points(array_ideal_points=[3, 6, 9],
                       workdays="",
                       missing_array=[3, 5])
        assert False
    except:
        pass

    # workdays = 0
    try:
        predict_points(array_ideal_points=[3, 6, 9],
                       workdays=0,
                       missing_array=[3, 5])
        assert False
    except:
        pass

       # в missing значение больше чем в workdays
    try:
        predict_points(array_ideal_points=[3, 6, 9],
                       workdays=34,
                       missing_array=[3, 500])
        assert False
    except:
        pass


# FINISH
# правильные данные в финиш
def test_calculating_points():
    result = calculate_points(real_score=7, totaldays=44,
                              missing_array=[2, 3])
    assert result == 7


# пропущенных дней больше рабочих
def test_calculating_points_error():
    try:
        calculate_points(real_score=7, totaldays=4,
                         missing_array=[2, 43])
        assert False
    except:
        pass

    # непредвиденная строка
    try:
        calculate_points(real_score=7, totaldays="str",
                         missing_array=[3, 4])
        assert False
    except:
        pass

    try:
        calculate_points(real_score="str", totaldays=44,
                         missing_array=[3, 5])
        assert False
    except:
        pass

    try:
        calculate_points(real_score=7, totaldays=44,
                         missing_array=["str", 5])
        assert False
    except:
        pass

    # totaldays=0,
    try:
        calculate_points(real_score=7, totaldays=0,
                         missing_array=[5, 5])
        assert False
    except:
        pass

    try:
        calculate_points(real_score=7, totaldays=0,
                         missing_array=[])
        assert False
    except:
        pass


# проверяет что будет если все разработчики отсутвовали во время спринта
def test_calculating_points_sum_zero():
    try:
        calculate_points(real_score=7, totaldays=1,
                         missing_array=[1])
        assert False
    except:
        pass
