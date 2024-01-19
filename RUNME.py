
import re
import sys

where_potential_urls_can_be_proposed_one_per_line = 'FEEDME.txt'
where_new_valid_urls_are_stored_alphabetically = 'README.md'



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

    def __init__(instance):
        instance.addables = list()
        instance.readables = list()
        instance.deletables = list()

    @staticmethod
    def get_unique(entries, alphabetical = True):
        entries = list(set(entries))
        if alphabetical:
            return sorted(entries)
        return entries



class Readme:

    @staticmethod
    def __init__():
        Readme.line_break = '<br />'

    @staticmethod
    def untag(string):
        return string.replace(Readme.line_break, '')



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



class Persistence(List, Readme, File):

    def of(instance):
        File.rewrite(where_potential_urls_can_be_proposed_one_per_line)
        File.rewrite(
            where_new_valid_urls_are_stored_alphabetically,
            Readme.line_break,
            instance.readables,
            True
        )



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
    def help(text):
        print('\n' + Interface.main_divider)
        print(Interface.margin + text)
        print(Interface.main_divider + '\n')

    @staticmethod
    def report(text):
        print('\n' + Interface.margin + text + '\n')




class Interactive(Persistence, Interface, List):

    def run(instance):
        Interface.help('"q" ends, "example\.io" searches')
        while True:
            it = Interactive.ask('Something to delete? ')
            if 'q' == it:
                Interactive.end()
            for each in instance.readables:
                try:
                    instance.deletables.append(
                        re.search(f'(.*)?{it}(.*)?', each).group(0)
                    )
                except:
                    continue
            if len(instance.deletables):
                print(Interface.sub_divider)
                for each in instance.deletables:
                    print(Interface.margin + each)
                Interface.help('"q" ends, "y" confirms, any other choice cancels')
                it = Interactive.ask('Do you confirm deletion? ')
                if 'y' == it:
                    for each in instance.deletables:
                        instance.readables.remove(each)
                    Persistence.of(instance)
                    Interface.report('Deletion done')
                else:
                    Interface.report('Deletion canceled')
                if 'q' == it:
                    Interactive.end()
                instance.deletables = list()
            else:
                Interface.report('No match')

    def ask(question):
        return input(Interface.margin + question)

    def end():
        Interface.report('End of execution')
        quit()



class Boot(Interactive, Persistence, Interface, List, Pattern, Readme, File):

    def __init__(self):
        self.p = len(sys.argv) > 1
        List.__init__(self)
        Pattern.__init__()
        Readme.__init__()
        self.fetch_data()
        self.process_data()
        Persistence.of(self)
        Interface.__init__()
        self.display_state()
        Interactive.run(self)

    def fetch_data(self):
        if self.p:
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
            Readme.untag
        )

    def process_data(self):
        self.previous = len(self.readables)
        self.readables = List.get_unique(self.readables + self.addables)
        self.updated = len(self.readables)

    def display_state(self):
        if self.updated > self.previous:
            if self.p:
                i = f'Command line p{"s" if self.updated - self.previous > 1 else ""}'
                i += f' moved in {where_new_valid_urls_are_stored_alphabetically}'
            else:
                i = f'Content of {where_potential_urls_can_be_proposed_one_per_line}'
                i += f' moved to {where_new_valid_urls_are_stored_alphabetically}'
        else:
            if self.p:
                i = f'There was no valid new URL passed as an p'
            else:
                i = f'There was no valid new URL in {where_potential_urls_can_be_proposed_one_per_line}'
        Interface.report(i)



start = Boot()
