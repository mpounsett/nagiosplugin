all:

.PHONY: clean docs

docs:
	# Run from the tox environment so that the correct Python version is used
	uv run tox -e docs

clean:
	rm -f 
	rm -Rf bin build develop-eggs dist docs/_build eggs htmlcov \
		nagiosplugin.egg-info parts src
	find . -name __pycache__ -exec rm -Rf '{}' +
	find . -name "*.pyc*" -exec rm '{}' +
