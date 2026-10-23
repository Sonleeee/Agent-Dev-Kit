@echo off
if exist "tools\session_curator.py" (
    py "tools\session_curator.py" --hook %*
) else if exist "..\tools\session_curator.py" (
    py "..\tools\session_curator.py" --hook %*
) else (
    echo {"decision": "allow", "status": "skipped"}
)
