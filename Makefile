all:	
	@echo iBrew: Generating README.md
	@rm -f *.tmp
	@python iBrew usage > usage.tmp
	@python iBrew examples > examples.tmp
	@python iBrew commands > commands.tmp
	@python iBrew notes > notes.tmp
	@cat help/README_part1.md usage.tmp help/README_part2.md commands.tmp help/README_part3.md examples.tmp help/README_part4.md LICENSE > README.md
	@echo iBrew: Generating help
	@pandoc --from markdown_github --to html -s --template=help/template.pandoc --toc README.md > help.tmp
	@cat help/head.html help.tmp help/foot.html > web/manual.html
	@pandoc --from markdown_github --to html -s --toc README.md > manual.html
	@echo iBrew: Cleaning up
	@rm -f *.pyc domoticz/*.pyc smarter/*.pyc
	@rm -f *.tmp
