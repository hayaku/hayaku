python hayaku_test.py 2> test.txt
python segmentation_test.py 2>> test.txt
python templates_test.py 2>> test.txt
python semantic_test.py 2>> test.txt
# python formatter.py
grep FAILED test.txt