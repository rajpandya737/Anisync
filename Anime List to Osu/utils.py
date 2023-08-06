get_first_non_empty = lambda data: next((item for item in data if item), [None])

remove_blank_entries = lambda lst: [entry.strip() for entry in lst if entry.strip()]

decode_unicode = lambda lst: [
    entry.encode("ascii", "ignore").decode("utf-8") for entry in lst
]

convert_to_string = lambda input_string: input_string.encode().decode("unicode_escape")
