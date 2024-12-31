from .load_static_data import static_arabic_data, static_english_data


def modify_error_messages(errors, lang='en'):
    modified_errors = {}
    data = static_english_data if lang == 'en' else static_arabic_data
    for field, messages in errors.items():
        modified_errors[field] = [
            data[message]
            for message in messages
        ]
    return modified_errors