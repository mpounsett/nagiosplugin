all:

<<<<<<< HEAD
docs:
	$(MAKE) -C doc html

=======
>>>>>>> aa554d8... adding a Makefile for cleaning up a working repository
clean:
	rm -f 
	rm -Rf bin develop-eggs doc/_build eggs htmlcov nagiosplugin.egg-info \
		parts src
	find . -name __pycache__ -exec rm -Rf '{}' +
	find . -name "*.pyc*" -exec rm '{}' +
