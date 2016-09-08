all:	
	@echo iBrew: Generating online help
	@python iBrew usage > usage.tmp
	@python iBrew examples > examples.tmp
	@python iBrew license > LICENSE
	@python iBrew commands > console.tmp
	@python iBrew notes > notes.tmp
	@python iBrew structure > protocol.tmp
	@echo iBrew: Fetching python requirements
	@pip install -r requirements.txt
	@echo iBrew: Generating README.md
	@cat README.md_parts/README_part1.md usage.tmp README.md_parts/README_part2.md console.tmp README.md_parts/README_part3.md examples.tmp README.md_parts/README_part4.md LICENSE > README.md

	@echo iBrew: Cleaning up
	@rm -f *.pyc domoticz/*.pyc smarter/*.pyc
	@rm -f *.tmp

