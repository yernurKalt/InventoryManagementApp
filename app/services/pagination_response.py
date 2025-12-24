import math


def pagination_response(arr: list, size: int, page: int):
    offset_min = size * page
    offset_max = size * (page + 1)
    response = arr[offset_min:offset_max] + [
        {
            "size": size,
            "page": page + 1,
            "total": math.ceil(len(arr) / size)
        }
    ]
    return response