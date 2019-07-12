#!/bin/bash
mkdir -p test-results/python

docker run tetherlessworld/whyis:master bash -c "python3 manage.py test --ci &>/dev/null && cat test-results/python/results.xml" >test-results/python/results.xml

cat test-results/python/results.xml

if [ "$(grep -c "failure " test-results/python/results.xml)" -ge 1 ]; then
    exit 1
else
    exit 0
fi