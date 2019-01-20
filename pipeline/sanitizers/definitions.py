from functools import partial
from pipeline.sanitizers.regex import (
    CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION,
    SPACE_PRECEDE_CLOSING_TAG,
    SPACE_FOLLOW_OPENING_TAG,
    LEFT_PARENTHESE,
    CONNECTING_TAGS,
    TOKEN_AFTER_TAGS
)

def translocate_trailing_punct(regex_obj):
    var = regex_obj.group('variable')
    content = regex_obj.group('content')

    if regex_obj.group('trailing_chars'):
        if content[-1] == regex_obj.group('trailing_chars')[0]:
            trailing_chars = regex_obj.group('trailing_chars')[1:]
        else:
            trailing_chars = regex_obj.group('trailing_chars')
        return f"<{var}>{content}{trailing_chars}</{var}>"
    return f"<{var}>{content}</{var}>"

DEFINITIONS = {
    'conferences': {

    },
    'journals': {
        'african-online-scientific-information-systems-harvard': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(LEFT_PARENTHESE.sub, r"<\g<variable>>\g<leading>\g<content></\g<variable>>"),
        ],
        'annual-reviews': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(SPACE_PRECEDE_CLOSING_TAG.sub, r"</\g<variable>> "),
        ],
        'cambridge-university-press-author-date': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(LEFT_PARENTHESE.sub, r"<\g<variable>>\g<leading>\g<content></\g<variable>>"),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4")
        ],
        'nature': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(SPACE_PRECEDE_CLOSING_TAG.sub, r"</\g<variable>> "),
            partial(LEFT_PARENTHESE.sub, r"<\g<variable>>\g<leading>\g<content></\g<variable>>"),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4")
        ],
        'apa': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(LEFT_PARENTHESE.sub, r"<\g<variable>>\g<leading>\g<content></\g<variable>>"),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4")
        ],
        'ieee': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(SPACE_PRECEDE_CLOSING_TAG.sub, r"</\g<variable>> "),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4")
        ],
        'chicago-author-date': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(LEFT_PARENTHESE.sub, r"<\g<variable>>\g<leading>\g<content></\g<variable>>"),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4")
        ],
        'elsevier-harvard': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct)
        ],
        'taylor-and-francis-harvard-x': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct)
        ],
        'oxford-the-university-of-new-south-wales': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(TOKEN_AFTER_TAGS.sub, r"\1\2\3 \4")
        ],
        'wiley-vch-books': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4"),
            partial(SPACE_FOLLOW_OPENING_TAG.sub, r"<\g<variable>>"),
        ],
        'elsevier-vancouver': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4"),
        ]
    },
    'thesis': {
        'wiley-vch-books': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4"),
            partial(SPACE_FOLLOW_OPENING_TAG.sub, r"<\g<variable>>"),
        ],
        'annual-reviews': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4"),
        ],
        'cambridge-university-press-author-date': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(LEFT_PARENTHESE.sub, r"<\g<variable>>\g<leading>\g<content></\g<variable>>"),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4"),
        ],
        'chicago-author-date': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
        ],
        'ieee': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4"),
        ],
        'taylor-and-francis-harvard-x': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
        ],
        'springer-mathphys-brackets': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(SPACE_PRECEDE_CLOSING_TAG.sub, r"</\g<variable>> "),
            partial(CONNECTING_TAGS.sub, r"\1\2> <\3\4"),
        ],
        'apa': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
            partial(LEFT_PARENTHESE.sub, r"<\g<variable>>\g<leading>\g<content></\g<variable>>"),
        ],
        'african-online-scientific-information-systems-harvard': [
            partial(CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub, translocate_trailing_punct),
        ]
    }
}

# for t, styles in DEFINITIONS.items():
#     for s, rules in styles.items():
#         print(t, s)
