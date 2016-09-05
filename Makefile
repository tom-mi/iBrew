all:	
	@echo iBrew: Generating online help
	@rm -f web/static/info/*.txt
	@python iBrew usage > web/static/info/usage.txt
	@python iBrew examples > web/static/info/examples.txt
	@python iBrew commands > web/static/info/console.txt
	@python iBrew notes > web/static/info/notes.txt
	@python iBrew structure > web/static/info/protocol.txt
	@cp LICENSE web/static/info/license.txt
	@echo iBrew: Fetching python requirements
	@pip install -r requirements.txt
	@echo iBrew: Generating README.md
	@cat README.md_parts/README_part1.md web/static/info/usage.txt README.md_parts/README_part2.md web/static/info/console.txt README.md_parts/README_part3.md web/static/info/examples.txt README.md_parts/README_part4.md LICENSE > README.md

	@echo iBrew: Cleaning up
	@rm -f *.pyc domoticz/*.pyc smarter/*.pyc

