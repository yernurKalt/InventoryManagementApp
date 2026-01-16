def low_stock_service(reorder_level: int, current_stock: int):
    if current_stock <= reorder_level:
        return True
    else:
        return False