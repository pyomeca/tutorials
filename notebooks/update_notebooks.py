import itertools
import re
from operator import itemgetter
from pathlib import Path

import nbformat
import yaml
from nbformat.v4.nbbase import new_markdown_cell


class NoteBooks:
    def __init__(self, nb_dir, config_file):
        self.nb_dir = nb_dir
        self.config_file = config_file
        self.reg = re.compile(r'(\d\d)\.(\d\d)-(.*)')

    def iter_notebooks(self):
        return sorted(nb for nb in self.nb_dir.glob("*.ipynb") if self.reg.match(nb.stem))

    @staticmethod
    def is_comment(cell, comment):
        return cell.source.startswith(comment)

    @staticmethod
    def get_notebook_title(nb_file):
        nb = nbformat.read(str(nb_file), as_version=4)
        for cell in nb.cells:
            if cell.source.startswith('#'):
                return cell.source[1:].splitlines()[0].strip()

    @staticmethod
    def get_config(conf, keys):
        with open(conf, 'r') as stream:
            data_loaded = yaml.load(stream)
        return itemgetter(*keys)(data_loaded)


class KernelSpec(NoteBooks):
    def __init__(self, nb_dir, config_file):
        super().__init__(nb_dir, config_file)

    def update(self):
        for nb_name in self.iter_notebooks():
            nb = nbformat.read(str(nb_name), as_version=4)

            print(f"- Updating kernelspec for {nb_name.stem}")
            nb['metadata']['kernelspec']['display_name'] = 'Python 3'

            nbformat.write(nb, str(nb_name))
        print('\n')


class Index(NoteBooks):
    def __init__(self, nb_dir, config_file):
        super().__init__(nb_dir, config_file)
        self.comment = "<!--INDEX_COMMENT-->\n## Table of Contents\n"

    def update(self):
        nb_name = self.nb_dir / 'Index.ipynb'

        nb = nbformat.read(str(nb_name), as_version=4)

        md_cell = f"{self.comment}{self.print_contents()}"

        if self.is_comment(nb.cells[-1], self.comment):
            print(f'- amending index for {nb_name.stem}')
            nb.cells[1].source = md_cell
        else:
            print(f'- inserting index for {nb_name.stem}')
            nb.cells.append(new_markdown_cell(md_cell))
        nbformat.write(nb, str(nb_name))
        print('\n')

    def gen_contents(self, directory=None):
        # TODO : HERE
        for nb in self.iter_notebooks():
            if directory:
                nb_url = Path(directory) / nb.stem
            else:
                nb_url = nb.parts[-1]
            chapter, section, title = self.reg.match(nb.stem).groups()
            title = self.get_notebook_title(nb)
            if section == '00':
                yield f'\n### [{int(chapter)}. {title}]({nb_url})'
            else:
                yield f"- [{title}]({nb_url})"

    def print_contents(self, directory=None):
        return '\n'.join(self.gen_contents(directory))


class Navigation(NoteBooks):
    def __init__(self, nb_dir, config_file):
        super().__init__(nb_dir, config_file)
        self.comment = "<!--NAVIGATION-->\n"
        self.prev_template = "< [{title}]({url}) "
        self.contents = "| [Contents](Index.ipynb) |"
        self.next_template = " [{title}]({url}) >"

    def update(self):
        for nb_name, navbar in self.iter_navbars(self.comment):
            nb = nbformat.read(str(nb_name), as_version=4)

            if self.is_comment(nb.cells[1], self.comment):
                print(f"- amending navigation for {nb_name.stem}")
                nb.cells[1].source = navbar
            else:
                print(f"- inserting navigation for {nb_name.stem}")
                nb.cells.insert(1, new_markdown_cell(source=navbar))

            if self.is_comment(nb.cells[-1], self.comment):
                nb.cells[-1].source = navbar
            else:
                nb.cells.append(new_markdown_cell(source=navbar))
            nbformat.write(nb, str(nb_name))
        print('\n')

    def iter_navbars(self, comment):
        for prev_nb, nb, next_nb in self.prev_this_next(self.iter_notebooks()):
            navbar = comment
            if prev_nb:
                navbar += self.prev_template.format(title=self.get_notebook_title(prev_nb),
                                                    url=prev_nb.parts[-1])
            navbar += self.contents
            if next_nb:
                navbar += self.next_template.format(title=self.get_notebook_title(next_nb),
                                                    url=next_nb.parts[-1])
            yield nb, navbar

    @staticmethod
    def prev_this_next(it):
        a, b, c = itertools.tee(it, 3)
        next(c)
        return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))


class Info(NoteBooks):
    def __init__(self, nb_dir, config_file):
        super().__init__(nb_dir, config_file)
        self.comment = "<!--BOOK_INFORMATION-->\n"
        self.repo_info = self.comment + self.get_config(self.config_file, keys=['repo_info'])

    def update(self):
        for nb_name in self.iter_notebooks():
            nb = nbformat.read(str(nb_name), as_version=4)

            if self.is_comment(nb.cells[0], self.comment):
                print(f'- amending info for {nb_name.stem}')
                nb.cells[0].source = self.repo_info
            else:
                print(f'- inserting info for {nb_name.stem}')
                nb.cells.insert(0, new_markdown_cell(self.repo_info))
            nbformat.write(nb, str(nb_name))
        print('\n')


if __name__ == '__main__':
    NB_DIR = Path.cwd()
    CONFIG_FILE = NB_DIR / ".." / "config.yml"

    # 1. Update kernelspec
    KernelSpec(NB_DIR, CONFIG_FILE).update()

    # 2. Update repo info
    Info(NB_DIR, CONFIG_FILE).update()

    # 3. Add navigation
    Navigation(NB_DIR, CONFIG_FILE).update()

    # 4. update index
    index = Index(NB_DIR, CONFIG_FILE)
    index.update()
