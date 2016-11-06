function sim = task1f(queryInput, objectInput)
    sim = python('task1f.py', sprintf('%s',queryInput), sprintf('%s', objectInput));
end