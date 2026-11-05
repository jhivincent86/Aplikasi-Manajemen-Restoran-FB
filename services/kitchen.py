from models.order import OrderItem

class Kitchen:
    @staticmethod
    def update_status_item(order_item: OrderItem, status_baru: str):
        order_item.status = status_baru
        print(f"👨‍🍳 Dapur: Status '{order_item.menu_item.nama}' (Qty: {order_item.qty}) diupdate menjadi -> {status_baru}")