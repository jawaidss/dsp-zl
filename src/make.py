#!/usr/bin/env python

from datetime import date
from jinja2 import Environment, FileSystemLoader
import os
import shutil

path = 'out'

environment = Environment(loader=FileSystemLoader('templates'))

global_context = {
    'year': date.today().year
}

media = {
    'files': [
        '.htaccess',
        'robots.txt',
        'sitemap.xml',
    ],
    'folders': [
        'static',
    ]
}

def render(template_name, context=None):
    if context is None:
        context = {}
    context['template_name'] = template_name
    context.update(global_context)
    template = environment.get_template(template_name)
    rendered_template = template.render(context)
    o = open(os.path.join(path, template_name), 'w')
    o.write(rendered_template)
    o.close()

def main():
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    render('activities.html')
    render('brothers.html')
    render('chapter.html')
    render('fraternity.html')
    render('index.html')
    render('officers.html')
    render('philanthropy.html')
    render('pledges.html')
    render('preamble.html')
    render('rush.html')
    render('social.html')
    for file_ in media['files']:
        shutil.copy(file_, os.path.join(path, file_))
    for folder in media['folders']:
        shutil.copytree(folder, os.path.join(path, folder))

if __name__ == '__main__':
    main()