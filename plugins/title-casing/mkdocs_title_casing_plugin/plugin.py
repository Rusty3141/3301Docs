from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import (Navigation, Section)
from titlecase import titlecase


def traverse(tree):
    if not isinstance(tree, (Navigation, Section)):
        yield tree
    else:
        if isinstance(tree, Navigation):
            for sublist in tree:
                yield from traverse(sublist)
        elif isinstance(tree, Section):
            yield tree
            for sublist in tree.children:
                yield from traverse(sublist)


class TitleCasingPlugin(BasePlugin):
    def on_nav(self, nav, config, files):
        for descendant in traverse(nav):
            if isinstance(descendant, Section):
                descendant.title = titlecase(descendant.title)
