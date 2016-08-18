all:
	@echo iBrew: Generating README.md
	@python iBrew structure > structure.tmp
	@python iBrew messages > index.tmp
	@python iBrew messages all > messages.tmp
	@python iBrew usage > usage.tmp
	@python iBrew examples > examples.tmp
	@python iBrew commands > commands.tmp
	@python iBrew domoticz > domoticz.tmp
	@python iBrew notes > notes.tmp
	@cat help/README_part1.md usage.tmp help/README_part2.md commands.tmp help/README_part2a.md examples.tmp help/README_part3.md domoticz.tmp help/README_part4.md structure.tmp help/README_part5.md index.tmp help/README_part6.md messages.tmp help/README_part7.md notes.tmp help/README_part8.md > README.md
	
	@echo iBrew: Cleaning up
	@rm -f *.pyc
	@rm -f *.tmp


	

