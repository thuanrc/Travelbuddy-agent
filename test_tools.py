import os

os.environ["PYTHONIOENCODING"] = "utf-8"

from travelbuddy.tools.tools import search_flights, search_hotels, calculate_budget


def print_separator(title):
    print()
    print("=" * 60)
    print("  " + title)
    print("=" * 60)


def test_search_flights():
    print_separator("Test 1: search_flights - Tuyen co san")
    result = search_flights.invoke({"origin": "Hà Nội", "destination": "Đà Nẵng"})
    print(result)

    print_separator("Test 2: search_flights - Tuyen nguoc")
    result = search_flights.invoke({"origin": "Đà Nẵng", "destination": "Hà Nội"})
    print(result)

    print_separator("Test 3: search_flights - Khong co tuyen")
    result = search_flights.invoke({"origin": "Hà Nội", "destination": "Nha Trang"})
    print(result)


def test_search_hotels():
    print_separator("Test 4: search_hotels - Tat ca khach san Da Nang")
    result = search_hotels.invoke({"city": "Đà Nẵng"})
    print(result)

    print_separator("Test 5: search_hotels - Loc theo gia max 700k")
    result = search_hotels.invoke({"city": "Đà Nẵng", "max_price_per_night": 700000})
    print(result)

    print_separator("Test 6: search_hotels - Khong co ket qua (gia qua thap)")
    result = search_hotels.invoke({"city": "Đà Nẵng", "max_price_per_night": 100000})
    print(result)

    print_separator("Test 7: search_hotels - Thanh pho khong ton tai")
    result = search_hotels.invoke({"city": "Huế"})
    print(result)


def test_calculate_budget():
    print_separator("Test 8: calculate_budget - Con du")
    result = calculate_budget.invoke(
        {"total_budget": 5000000, "expenses": "ve_may_bay:890000,khach_san:650000"}
    )
    print(result)

    print_separator("Test 9: calculate_budget - Vuot ngan sach")
    result = calculate_budget.invoke(
        {"total_budget": 1000000, "expenses": "ve_may_bay:890000,khach_san:650000"}
    )
    print(result)

    print_separator("Test 10: calculate_budget - Format sai")
    result = calculate_budget.invoke(
        {"total_budget": 5000000, "expenses": "ve_may_bay:890000,khach_san"}
    )
    print(result)


def test_scenario_full():
    print_separator("Test 11: Scenario - Ha Noi -> Phu Quoc 2 dem, budget 5 trieu")

    flights_result = search_flights.invoke(
        {"origin": "Hà Nội", "destination": "Phú Quốc"}
    )
    print("BUOC 1 - Tim chuyen bay:")
    print(flights_result)

    hotels_result = search_hotels.invoke(
        {"city": "Phú Quốc", "max_price_per_night": 1950000}
    )
    print("\nBUOC 2 - Tim khach san:")
    print(hotels_result)

    budget_result = calculate_budget.invoke(
        {"total_budget": 5000000, "expenses": "ve_may_bay:1100000,khach_san:1600000"}
    )
    print("\nBUOC 3 - Tinh ngan sach:")
    print(budget_result)


if __name__ == "__main__":
    test_search_flights()
    test_search_hotels()
    test_calculate_budget()
    test_scenario_full()
