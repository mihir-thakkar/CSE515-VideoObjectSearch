function sim = task1e(queryInput, objectInput)
    sim = python('task1e.py', sprintf('%s',queryInput), sprintf('%s', objectInput));
end