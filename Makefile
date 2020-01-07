.PHONY : lint execute_all_notebooks update_notebooks clean all

lint:
	black .

update_notebooks:
	python src/update_notebooks.py

execute_all_notebooks:
	jupyter nbconvert --to notebook --inplace --execute notebooks/*.ipynb --ExecutePreprocessor.kernel_name=python

export_nb_to_single_md:
	jupyter nbconvert --to markdown notebooks/*.ipynb
	cat notebooks/*.md >> all.md
	rm notebooks/*.md

clean:
	rm -rf .pytest_cache .coverage site notebooks/.ipynb_checkpoints .ipynb_checkpoints

all: lint execute_all_notebooks update_notebooks clean