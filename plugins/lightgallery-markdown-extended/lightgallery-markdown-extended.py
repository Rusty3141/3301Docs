from markdown import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
import os
import re


class ImagesTreeprocessor(Treeprocessor):
    def __init__(self, config, md):
        Treeprocessor.__init__(self, md)
        self.re = re.compile(r'^!.*')
        self.captionre = re.compile(r'^caption!.*')
        self.config = config

    def run(self, root):
        parent_map = {c: p for p in root.iter() for c in p}
        try:
            images = root.iter("img")
        except AttributeError:
            images = root.getiterator("img")
        for image in images:
            desc = image.attrib["alt"]
            if self.re.match(desc) or self.captionre.match(desc):
                new_node = etree.Element('a')
                new_node.set("class", "lightgallery-item")
                new_node.set("href", image.attrib["src"])
                image.set("src", "{0}{2}{1}".format(
                    *os.path.splitext(image.attrib["src"]), ".thumbnail"))
                parent = parent_map[image]
                ix = list(parent).index(image)

                if self.captionre.match(desc) or self.config["show_description_as_inline_caption"]:
                    desc = desc.lstrip("caption!")
                    inline_caption_node = etree.Element('p')
                    inline_caption_node.set(
                        "class", self.config["custom_inline_caption_css_class"])
                    inline_caption_node.text = desc
                    parent.insert(ix + 1, inline_caption_node)
                else:
                    desc = desc.lstrip("!")

                if self.config["show_description_in_lightgallery"]:
                    new_node.set("data-sub-html", desc)

                image.set("alt", desc)

                parent.insert(ix, new_node)
                new_node.append(image)
                parent.remove(image)


class LightGalleryExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'show_description_in_lightgallery': [True, 'Adds the description as caption in lightgallery dialog. Default: True'],
            'show_description_as_inline_caption': [False, 'Adds the description as inline caption below the image. Default: False'],
            'custom_inline_caption_css_class': ['', 'Custom CSS classes which are applied to the inline caption paragraph. Multiple classes are separated via space. Default: empty']
        }
        super(LightGalleryExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        config = self.getConfigs()
        md.treeprocessors.add(
            "lightbox", ImagesTreeprocessor(config, md), "_end")


def makeExtension(*args, **kwargs):
    return LightGalleryExtension(**kwargs)
