#!/bin/bash

URL="http://localhost:8258/comments"

echo "Testing comments-s07 with wrk"
echo "Endpoint: $URL"

echo ""
echo "Concurrency: 1"
wrk -t1 -c1 -d30s --latency "$URL"

echo ""
echo "Concurrency: 10"
wrk -t2 -c10 -d30s --latency "$URL"

echo ""
echo "Concurrency: 100"
wrk -t4 -c100 -d30s --latency "$URL"
