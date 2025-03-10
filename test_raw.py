# my_dict = {"a": 1, "b": 2, "c": 3}
# print(
#     "list: ",
#     [
#         {
#             "_id": "420e72a4-7a71-4045-b29d-a5a3f8aff4bf",
#             "title": "tablezzzz",
#             "description": "a device with four legs and a flat surface.",
#             "_updated": "2025-01-10T18:04:03.664666+00:00",
#         },
#         {
#             "_id": "6984c72a-6e24-4d6c-b4d5-a7e00add74ff",
#             "title": "chairzzz",
#             "description": "a seat for one person that has a back, usually four legs, and sometimes two arms.",
#             "_updated": "2025-01-11T09:07:07.233888+00:00",
#         },
#     ],
# )
# print("my_dict.items(): ", my_dict.items())
# print("enumerate(my_dict.items()): ", enumerate(my_dict.items()))

# for index, (key, value) in enumerate(my_dict.items()):
#     print(f"Index: {index}, Key: {key}, Value: {value}")


# my_list = [10, 20, 30, 40, 50]

# for index, item in enumerate(my_list):
#     print(f"my_list Index: {index}, Item: {item}")

# name = input("what is your name?: ")
# print(f"Hello {name}")
# age = input("How old are you?: ")
# age = int(age)
# print(f"You are {age} years old")

# CALCULATE RECTANGLE SQUARE FROM LENGTH & WIDTH
# length = float(input("Input rectangle length: "))
# width = float(input("Input rectangle width: "))
# print(f"Rectangle square is {length * width} m²")

# [Python] List comprehension technical
arr_of_arr = [[1, 2], [3, 4], [5, 6], [7, 8]]
for item in arr_of_arr:
    print("couple", item)
new_arr = [item[0] for item in arr_of_arr]
print("arr", new_arr)
