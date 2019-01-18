import re
import glob
import os

## List of regex to sanitise the data
CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION = re.compile(r"""<(?P<variable>[^/>]*)>
                                                                (?P<content>.*)
                                                                </\1>
                                                                (?P<trailing_chars>[^<(\w\s]*)
                                                                """, re.VERBOSE)

def repl(obj):
    var = obj.group('variable')
    content = obj.group('content')

    if obj.group('trailing_chars'):
        if content[-1] == obj.group('trailing_chars')[0]:
            trailing_chars = obj.group('trailing_chars')[1:]
        else:
            trailing_chars = obj.group('trailing_chars')
        return f"<{var}>{content}{trailing_chars}</{var}>"
    return f"<{var}>{content}</{var}>"

PARENTHESES_SURROUND_YEAR = re.compile(r"(\()<(year)>(?P<content>\d{4})</year>(\))")
SPACE_PRECEDE_CLOSING_TAG = re.compile(r"\s{1}</(?P<variable>[a-zA-Z\-|^<]+)>")
LEFT_PARENTHESES_ON_YEAR = re.compile(r"(?P<leading>\()<(?P<variable>year)>(?P<content>\d{4}\)\W?)</year>")
SPACE_END_BEGIN = re.compile(r"x")


assert CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub(repl, "<author>Amsterdam D, Phillips SB, Richter MW</author>.") == "<author>Amsterdam D, Phillips SB, Richter MW.</author>"
assert SPACE_PRECEDE_CLOSING_TAG.sub(r"</\g<variable>> ", "<citation-number>1. </citation-number>") == "<citation-number>1.</citation-number> "
assert LEFT_PARENTHESES_ON_YEAR.sub(r"<\g<variable>>(\g<content></\g<variable>>", "(<year>1976).</year>") == "<year>(1976).</year>"
assert PARENTHESES_SURROUND_YEAR.sub(r"<year>(\g<content>)</year>", "(<year>1976</year>)") == '<year>(1976)</year>'

# Change the path to where the BibTeX files are
files = glob.iglob('/Users/yuanchuan/Downloads/data/ETD/annotated/journals/*/output.presanitised.txt')

for f in files:
    fp = os.path.abspath(f)
    print(fp)
    with open(os.path.join(os.path.dirname(fp), 'output.sanitised.txt'), 'w') as sout:
        with open(fp, 'r') as fin:
            line = fin.readline()
            while line:
                out = CAPTURE_TEXT_BETWEEN_TAG_WITH_TRAILING_PUNCTUATION.sub(repl, line)
                out = SPACE_PRECEDE_CLOSING_TAG.sub(r"</\g<variable>> ", out)
                out = LEFT_PARENTHESES_ON_YEAR.sub(r"<\g<variable>>(\g<content></\g<variable>>", out)

                sout.write(out)

                line = fin.readline()
