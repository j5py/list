
import re
import sys

where_potential_urls_can_be_proposed_one_per_line = 'FEEDME.txt'
where_new_valid_urls_are_stored_alphabetically = 'README.md'



class File:

    @staticmethod
    def rewrite(file, prefix = '', entries = False, line_feed = False):
        with open(file, 'w') as opened:
            if entries:
                for each in entries:
                    opened.write(prefix + each + '\n' if line_feed else '')
            else:
                opened.write('')
            opened.close()

    @staticmethod
    def get_processed_entries(file, invokable_process):
        entries = list()
        opened = open(file)
        for each in opened:
            each = invokable_process(each.strip('\n'))
            if each:
                entries.append(each)
        opened.close()
        return entries



class Readme:

    @staticmethod
    def __init__():
        Readme.line_break = '<br />'

    @staticmethod
    def undo_as_line(string):
        return string.replace(Readme.line_break, '')



class Pattern:

    @staticmethod
    def __init__():
        Pattern.regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[\w\-/?=&.:]*'

    @staticmethod
    def clean(string):
        return string.strip(' /')

    @staticmethod
    def valid_url(string):
        try:
            match = re.search(Pattern.regex, string).group(0)
            return Pattern.clean(match)
        except:
            return None



class List:

    def __init__(boot):
        boot.addables = list()
        boot.readables = list()
        boot.deletables = list()

    @staticmethod
    def get_unique(entries, alphabetical = True):
        entries = list(set(entries))
        if alphabetical:
            return sorted(entries)
        return entries



class Interface:

    @staticmethod
    def __init__():
        Interface.main_divider = Interface.get_divider(64, '=')
        Interface.sub_divider = Interface.get_divider(64, '-')
        Interface.margin = Interface.get_margin(4)

    def get_divider(length, symbol, string = '', i = 0):
        while i < length:
            string += symbol
            i += 1
        return string

    def get_margin(length, string = '', i = 0):
        while i < length:
            string += ' '
            i += 1
        return string

    @staticmethod
    def demarcate(divider, prefix = None):
        if prefix is True:
            print('\n' + divider)
        elif prefix is False:
            print(divider + '\n')
        elif prefix is None:
            print(divider)

    @staticmethod
    def help(instructions):
        Interface.demarcate(Interface.main_divider, True)
        print(f'{Interface.margin}HELP {instructions}')
        Interface.demarcate(Interface.main_divider, False)

    @staticmethod
    def display(text, initial = False):
        if initial:
            Interface.demarcate(Interface.sub_divider)
        print(("\n" if initial else "") + Interface.margin + text)
        if not initial:
            Interface.demarcate(Interface.sub_divider)



class Persistence(List, Readme, File):
    def update(boot):
        File.rewrite(where_potential_urls_can_be_proposed_one_per_line)
        File.rewrite(
            where_new_valid_urls_are_stored_alphabetically,
            Readme.line_break,
            boot.readables,
            True
        )



class Interactive(Persistence, Interface, List):

    def ask(question):
        return input(Interface.margin + question)

    def run(boot):
        Interface.help('"q" ends, "example\.io" searches')
        while True:
            it = Interactive.ask('Something to delete? ')
            if 'q' == it:
                Interface.display('End of execution')
                quit()
            for each in boot.readables:
                try:
                    boot.deletables.append(
                        re.search(f'(.*)?{it}(.*)?', each).group(0)
                    )
                except:
                    continue
            if len(boot.deletables):
                for each in boot.deletables:
                    print(Interface.margin + each)
                Interface.help('"q" ends, "y" confirms, any other choice cancels')
                it = Interactive.ask('Do you confirm deletion? ')
                if 'y' == it:
                    for each in boot.deletables:
                        boot.readables.remove(each)
                    Persistence.update(boot)
                    Interface.display('Deletion done')
                else:
                    Interface.display('Deletion canceled')
                if 'q' == it:
                    Interface.display('End of execution')
                    quit()
                boot.deletables = list()
            else:
                Interface.display('No match')



class Boot(Interactive, Persistence, Interface, List, Pattern, Readme, File):

    def __init__(self):
        self.argument = len(sys.argv) > 1
        Readme.__init__()
        Pattern.__init__()
        List.__init__(self)
        Interface.__init__()
        self.fetch_data()
        self.process_data()
        Persistence.update(self)
        self.update_report()
        Interactive.run(self)

    def fetch_data(self):
        if self.argument:
            for each in sys.argv[1:]:
                each = Pattern.valid_url(each)
                if each:
                    self.addables.append(each)
        else:
            self.addables = File.get_processed_entries(
                where_potential_urls_can_be_proposed_one_per_line,
                Pattern.valid_url
            )
        self.readables = File.get_processed_entries(
            where_new_valid_urls_are_stored_alphabetically,
            Readme.undo_as_line
        )

    def process_data(self):
        self.previous = len(self.readables)
        self.readables = List.get_unique(self.readables + self.addables)
        self.updated = len(self.readables)

    def update_report(self):
        if self.updated > self.previous:
            if self.argument:
                up = f'Command line argument{"s" if self.updated - self.previous > 1 else ""}'
                up += f' moved in {where_new_valid_urls_are_stored_alphabetically}'
            else:
                up = f'Content of {where_potential_urls_can_be_proposed_one_per_line}'
                up += f' moved to {where_new_valid_urls_are_stored_alphabetically}'
        else:
            if self.argument:
                up = f'There was no valid new URL passed as an argument'
            else:
                up = f'There was no valid new URL in {where_potential_urls_can_be_proposed_one_per_line}'
        Interface.display(up, True)



start = Boot()
