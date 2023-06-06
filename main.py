from helper import read_data, save_data


def count_models(data) -> dict:
    count_dict = {}
    for line in data[1:]:
        model = line["car_model"]
        if count_dict.get(model) is not None:
            count_dict[model] += 1
        else:
            count_dict[model] = 1
    return count_dict


def keep_models(count_dict: dict) -> list:
    keep_models = []
    for key in count_dict.keys():
        if count_dict[key] >= 3:
            keep_models.append(key)
    return keep_models


def clean_data(data: list, keep_models: list) -> list:
    i = 1
    while i < len(data):
        if not (data[i]["car_model"] in keep_models):
            data.pop(i)
        else:
            i += 1
    return data


def prep_data(data: list) -> list:
    return clean_data(data, keep_models(count_models(data)))


if __name__ == "__main__":
    save_data(prep_data(read_data()))
