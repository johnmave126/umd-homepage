import json
import os
import errno
import shutil

from jinja2 import Environment, FileSystemLoader


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def main():
    pages = json.load(open('pages.json', 'r'))
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl_complete = env.get_template('generic/complete.html')
    tmpl_body = env.get_template('generic/body.html')
    shutil.rmtree('output', True)
    mkdir_p(os.path.join('output', 'body'))
    print "[Generate HTML files]"
    for page in pages:
        if page['type'] == 'page':
            print "%s.html..." % page['prefix'],
            ofp = open(os.path.join('output', "%s.html" %
                                    page['prefix']), 'w+')
            ofp.write(tmpl_complete.render(page=page, pages=pages))
            ofp.close()
            ofp = open(os.path.join('output', 'body', "%s.html" %
                                    page['prefix']), 'w+')
            ofp.write(tmpl_body.render(page=page))
            ofp.close()
        print "Done"
    print '[Done]'
    print "[Copy static files]"
    shutil.copytree('assets', os.path.join('output', 'assets'))
    print '[Done]'


if __name__ == '__main__':
    main()
