#! /bin/bash
# generates a .patch file with coding style issues.
# this should be empty after each commit, otherwise, need to amend the commit

autopep8 --aggressive --aggressive --diff *.py &> fix_codingstyle.patch
number_of_lines="$(cat fix_codingstyle.patch | wc -l)"
if [[ $number_of_lines -gt 0 ]]; then
    echo "__ERROR: please fix coding style by appling fix_codingstyle.patch" >&2
    echo "__ERROR: this can be done with:" >&2
    echo "git apply fix_codingstyle.patch && git commit --amend" >&2
    exit 1
fi

rm fix_codingstyle.patch
exit 0
