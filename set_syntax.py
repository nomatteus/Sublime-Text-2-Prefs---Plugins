import os.path
import re

import sublime
import sublime_plugin


class SetSyntaxListener(sublime_plugin.EventListener):
    def on_load(self, view):
        filename = view.file_name()
        map = view.settings().get('set_syntax_map')

        if view.is_scratch() or not filename or not map:
            return

        name = os.path.basename(filename)

        if name in map:
            self.set_syntax(view, name, map[name])
        else:
            # Still haven't found syntax, check shebang line
            shebang = view.substr(view.line(0))

            if shebang.startswith('#!'):
                m = re.match(r'#![ ]*(?:/usr)?/bin/env[ ]+(\w+)', shebang)

                if m and m.group(1):
                    syntax = m.group(1)
                else:
                    syntax = os.path.basename(shebang)

                syntax = '#!' + syntax

                if syntax in map:
                    self.set_syntax(view, syntax, map[syntax])

    def set_syntax(self, view, name, syntax):
        packages_dir = os.path.dirname(sublime.packages_path())

        if '/' in syntax:
            syntax_dir = os.path.dirname(syntax)
            syntax = os.path.basename(syntax)
        else:
            syntax_dir = syntax

        syntax_path = os.path.join('Packages', syntax_dir, syntax + '.tmLanguage')

        if os.path.exists(os.path.join(packages_dir, syntax_path)):
            print 'SetSyntax: "{0}" => {1}'.format(name, syntax_path)
            view.set_syntax_file(syntax_path)
