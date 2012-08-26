# -*- coding: utf-8 -*-
import re

TEST_NAME = re.compile(r'.*\stest_([:\w]+)\s.*')
TEST_RESULTS = re.compile(r".*'(.*)'.*'(.*)'.*")

tests = []
with open('test_data.py') as f:
    for i, l in enumerate(f):
        tests.append((l, i+1))

with open('test.txt') as text:
    with open('readable.txt', 'w') as out:
        for line in text:
            if line.startswith('FAIL:') or line.startswith('AssertionError:'):
                res = TEST_NAME.search(line)
                if res is not None:
                    test_name = res.group(1)
                    pat = '"{0}"'.format(test_name)
                    line_n = 0
                    for te, line_num in tests:
                        if pat in te:
                            line_n = line_num
                            break
                    out.write('{0} (line {1})\n'.format(test_name, line_n))
                res = TEST_RESULTS.search(line)
                if res is not None:
                    out.write('  {0}\n'.format(res.group(1)))
                    out.write('  {0}\n\n'.format(res.group(2)))
            
            if line.startswith('Ran') or line.startswith('FAILED'):
                out.write(line)
