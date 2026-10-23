#!/usr/bin/env bash
if [ -f "tools/session_curator.py" ]; then
    python3 "tools/session_curator.py" --hook "$@"
elif [ -f "../tools/session_curator.py" ]; then
    python3 "../tools/session_curator.py" --hook "$@"
else
    echo '{"decision": "allow", "status": "skipped"}'
fi
