from langchain_core.tools import tool
from travelbuddy.data.mock_data import FLIGHTS_DB, HOTELS_DB


def format_price(price: int) -> str:
    """Format price with dot separators and 'đ' suffix. E.g., 1450000 → '1.450.000đ'."""
    return f"{price:,.0f}".replace(",", ".") + "đ"


@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố.

    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')

    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    # Tra cứu FLIGHTS_DB với key (origin, destination)
    flights = FLIGHTS_DB.get((origin, destination))

    # Nếu không tìm thấy → thử tra ngược (destination, origin)
    if flights is None:
        flights = FLIGHTS_DB.get((destination, origin))

    # Nếu cũng không có → thông báo không tìm thấy
    if flights is None:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # Format danh sách chuyến bay dễ đọc
    result_lines = [f"✈️ Chuyến bay từ {origin} đến {destination}:\n"]
    for i, flight in enumerate(flights, 1):
        result_lines.append(
            f"{i}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
            f"{flight['class']} | Giá: {format_price(flight['price'])}"
        )

    return "\n".join(result_lines)


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    # Tra cứu HOTELS_DB[city]
    hotels = HOTELS_DB.get(city)

    # Nếu không tìm thấy thành phố
    if hotels is None:
        return f"Không tìm thấy khách sạn tại {city}."

    # Lọc theo max_price_per_night
    filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

    # Sắp xếp theo rating giảm dần
    filtered.sort(key=lambda h: h["rating"], reverse=True)

    # Nếu không có kết quả
    if not filtered:
        return (
            f"Không tìm thấy khách sạn tại {city} "
            f"với giá dưới {format_price(max_price_per_night)}/đêm. "
            f"Hãy thử tăng ngân sách."
        )

    # Format đẹp
    result_lines = [
        f"🏨 Khách sạn tại {city} (tối đa {format_price(max_price_per_night)}/đêm):\n"
    ]
    for i, hotel in enumerate(filtered, 1):
        stars_display = "⭐" * hotel["stars"]
        result_lines.append(
            f"{i}. {hotel['name']} | {stars_display} | "
            f"Khu vực: {hotel['area']} | Rating: {hotel['rating']}/5 | "
            f"Giá: {format_price(hotel['price_per_night'])}/đêm"
        )

    return "\n".join(result_lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')

    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    # Parse chuỗi expenses thành dict {tên: số_tiền}
    try:
        expense_items = {}
        for item in expenses.split(","):
            item = item.strip()
            if ":" not in item:
                return f"Lỗi: format expenses sai. Mong muốn 'tên:số_tiền', nhận được '{item}'."
            name, amount_str = item.split(":", 1)
            amount = int(amount_str.strip())
            expense_items[name.strip()] = amount
    except ValueError:
        return "Lỗi: không thể parse số tiền từ expenses. Kiểm tra lại format."

    # Tính tổng chi phí
    total_expenses = sum(expense_items.values())

    # Tính số tiền còn lại
    remaining = total_budget - total_expenses

    # Format bảng chi tiết
    lines = ["📊 Bảng chi phí:"]
    for name, amount in expense_items.items():
        lines.append(f"  - {name}: {format_price(amount)}")
    lines.append("---")
    lines.append(f"Tổng chi: {format_price(total_expenses)}")
    lines.append(f"Ngân sách: {format_price(total_budget)}")

    if remaining >= 0:
        lines.append(f"Còn lại: {format_price(remaining)}")
    else:
        deficit = abs(remaining)
        lines.append(f"⚠️ Vượt ngân sách {format_price(deficit)}! Cần điều chỉnh.")

    return "\n".join(lines)
