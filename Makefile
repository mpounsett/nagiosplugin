all:

.PHONY: clean

docs:
	$(MAKE) -C docs html

clean:
	rm -f 
	rm -Rf bin build develop-eggs dist docs/_build eggs htmlcov \
		nagiosplugin.egg-info parts src
	find . -name __pycache__ -exec rm -Rf '{}' +
	find . -name "*.pyc*" -exec rm '{}' +
