import os
import sys
import json

from datetime import datetime
from datetime import date

def page_to_md(page, path):
    md = ''

    if isinstance(page["contentJSON"], str):
        contentData = json.loads(page["contentJSON"])
        for c in contentData:
            if c["type"] == 'p':
                md += '{}\n'.format(block_to_p(c))
            elif c["type"] == 'h1':
                md += '{}\n'.format(block_to_h1(c))
            elif c["type"] == 'h2':
                md += '{}\n'.format(block_to_h2(c))
            elif c["type"] == 'h3':
                md += '{}\n'.format(block_to_h3(c))
            elif c["type"] == 'list':
                md += '{}\n'.format(block_to_list(c))
            elif c["type"] == 'code_block':
                md += '{}\n'.format(block_to_codeblock(c))

    filename = page["title"]
    
    for c in ['#', '$', '&', '{', '}', '\\', '<', '>', '*', '?', '/', '$', '!', '\'', '"', ':', '@', '+', '`', '|', '=']:
        filename = filename.replace(c, '')

    f = open('{}{}.md'.format(path, filename), 'w+')
    f.write(md)
    f.close()

def block_to_p(block):
    ret = ''

    for c in block["children"]:
        ret += child_to_md(c)

    return ret

def block_to_h1(block):
    ret = '# '

    for c in block["children"]:
        ret += child_to_md(c)

    return ret

def block_to_h2(block):
    ret = '## '

    for c in block["children"]:
        ret += child_to_md(c)

    return ret

def block_to_h3(block):
    ret = '### '

    for c in block["children"]:
        ret += child_to_md(c)

    return ret

def block_to_list(block):
    ret = ''

    for c in block["children"]:
        ret += '{}\n'.format(child_to_md(c))

    return ret

def block_to_codeblock(block):
    lang = ''

    if 'lang' in block:
        lang = block["lang"]

    ret = '```{}\n'.format(lang)

    for c in block["children"]:
        ret += '{}\n'.format(child_to_md(c))

    ret += '```'

    return ret

def block_to_blockquote(block):
    ret = ''

    for c in block["children"]:
        ret += '> {}\n'.format(child_to_md(c))

    return ret

def child_to_md(child):
    # text block
    if 'text' in child and not 'type' in child:
        if 'bold' in child and child["bold"]:
            return '**{}**'.format(child["text"])

        return child["text"]
    
    # list block
    if 'type' in child and child["type"] == 'list_item':
        ret = ''

        for c in child["children"]:
            for cc in c["children"]:
                text = child_to_md(cc)
                
                if len(text) > 0:
                    if 'listType' in child and child["listType"] == 'todoList':
                        if 'checked' in child and child["checked"]:
                            ret += '- [x] {}'.format(text)
                        else:
                            ret += '- [ ] {}'.format(text)
                    else:
                        ret +=  '- {}'.format(text)

        return ret

    # backlink
    if 'type' in child and child["type"] == 'backlink':
        for c in child["children"]:
            return '[[{}]]'.format(child_to_md(c))

    # a
    if 'type' in child and child["type"] == 'a':
        url = child["url"]
        text = child["children"][0]["text"]
        return '[{}]({})'.format(text, url)
    
    # code line
    if 'type' in child and child["type"] == 'code_line':
        ret = ''
        
        for c in child["children"]:
            text = child_to_md(c)

            if len(text) > 0:
                ret += '{}'.format(text)

        return ret

    return ''

if __name__ == '__main__':
    f = open(sys.argv[1])
    data = json.load(f)
    f.close()

    foldername = date.today().strftime("%Y%m%d") + datetime.now().strftime("%H%M%S")
    path = './{}/'.format(foldername)
    os.mkdir(path, 0o666)

    for p in data["pages"]:
        page_to_md(p, path)
