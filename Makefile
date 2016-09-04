all:	
	@echo iBrew: Generating README.md
	@rm -f *.tmp
	@python iBrew structure > structure.tmp
	@python iBrew messages > index.tmp
	@python iBrew messages all > messages.tmp
	@python iBrew usage > usage.tmp
	@python iBrew examples > examples.tmp
	@python iBrew commands > commands.tmp
	@python iBrew notes > notes.tmp
	@cat help/README_part1.md usage.tmp help/README_part2.md commands.tmp help/README_part3.md examples.tmp help/README_part4.md structure.tmp help/README_part5.md index.tmp help/README_part6.md messages.tmp help/README_part7.md notes.tmp help/README_part8.md LICENSE help/README_part9.md > README.md
	@echo iBrew: Generating help
	@pandoc --from markdown_github --to html -s --template=help/template.pandoc --toc README.md > help.tmp
	@cat help/head.html help.tmp help/foot.html > web/manual.html
	@pandoc --from markdown_github --to html -s --toc README.md > manual.html
	@echo iBrew: Cleaning up
	@rm -f *.pyc domoticz/*.pyc smarter/*.pyc
	@rm -f *.tmp
