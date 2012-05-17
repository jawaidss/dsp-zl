#!/usr/bin/env python

from datetime import date
from jinja2 import Environment, FileSystemLoader
import json
import os
import shutil

path = 'out'

environment = Environment(loader=FileSystemLoader('templates'))

def load(json_filename):
    o = open(os.path.join('json', json_filename))
    json_string = o.read()
    o.close()
    return json.loads(json_string)

def mungify(username):
    mailto = 'mailto:%s@rose-hulman.edu' % username
    return ''.join(['&#%s;' % ord(c) for c in mailto])

actives = load('actives.json')
officers = load('officers.json')
pledges = load('pledges.json')

global_context = {
    'president_href': '#',
    'webmaster_href': '#',
    'year': date.today().year
}

president = None
rush_director = None
for officer_type in officers:
    for officer in officer_type['officers']:
        if officer['office'] == 'President':
            global_context['president_href'] = mungify(officer['username'])
            president = officer
        elif officer['office'] == 'Webmaster':
            global_context['webmaster_href'] = mungify(officer['username'])
        elif officer['office'] == 'Rush Director':
            rush_director = officer

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
    render('404.html')
    render('activities.html')
    render('brothers.html', {'actives': actives})
    render('chapter.html')
    render('fraternity.html')
    render('index.html', {'president': president})
    render('officers.html', {'officers': officers})
    render('philanthropy.html')
    render('pledges.html', {'pledges': pledges})
    render('preamble.html')
    render('rush.html', {'rush_director_href': mungify(rush_director['username'])})
    render('social.html')
    for file_ in media['files']:
        shutil.copy(file_, os.path.join(path, file_))
    for folder in media['folders']:
        shutil.copytree(folder, os.path.join(path, folder))

if __name__ == '__main__':
    main()