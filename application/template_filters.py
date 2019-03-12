from application.middleware import (clean_javascript_text,
                                    format_error_message, slugify,
                                    remove_whitespace)

template_filters = [clean_javascript_text, format_error_message, slugify,
                    remove_whitespace]
