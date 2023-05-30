
import re
import sys



#-----> CONFIGURABLE

where_to_find_new_urls = 'FEEDME.txt'
# list the URLs to add, one per line

where_to_save_all_changes = 'README.md'
# alphabetical list of unique clickables



#-----> USABLE

addables = list()
readables = list()
deletables = list()

url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[\w\-/?=&.]*'

def rewrite(file, prefix = '', lines = False, suffix = '\n'):
    with open(file, 'w') as opened:
        if lines:
            for line in lines:
                opened.write(prefix + line + suffix)
        else:
            opened.write('')
        opened.close()

def get_list_of_unique(entries, alphabetical = True):
    entries = list(set(entries))
    if alphabetical:
        return sorted(entries)
    return entries

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

# ( i ) See class or namespace to group the following functions and highlight their interdependency

def get_list_from(file, invokable, pattern, sensitive, match): # invokable = get_valid
    results = list()
    opened = open(file)
    for line in opened:
        result = invokable(line, pattern, sensitive, match)
        if result:
            results.append(result)
    opened.close()
    return results

def get_valid(string, pattern, sensitive, match):
    try:
        if sensitive:
            string = re.search(pattern, string).group(match)
        else:
            string = re.search(pattern, string, re.IGNORECASE).group(match)
        return string.strip(' /')
    except:
        return None

# ( i ) See class or namespace to group the following functions and highlight their interdependency

def print_manual(margin, instructions):
    print_separator(built_main_divider, True)
    print(f'{margin}HELP {instructions}')
    print_separator(built_main_divider, False)

def print_status(margin, message, initial = False):
    if initial:
        print_separator(built_sub_divider,)
    print(("\n" if initial else "") + margin + message)
    if not initial:
        print_separator(built_sub_divider,)

def print_separator(divider, prefix = None):
    if prefix is True:
        print('\n' + divider)
    elif prefix is False:
        print(divider + '\n')
    elif prefix is None:
        print(divider)

def get_input(margin, question):
    string = input(margin + question)
    print_separator(built_sub_divider,)
    return string



#-----> INITIAL

built_main_divider = get_divider(48, '=')
built_sub_divider = get_divider(48, '-')
built_margin = get_margin(4)

argument = len(sys.argv) > 1

if argument:
    for key in sys.argv[1:]:
        key = get_valid(key, url_pattern, True, 0)
        if key:
            addables.append(key)
else:
    addables = get_list_from(
        where_to_find_new_urls,
        get_valid,
        url_pattern,
        True,
        0
    )
    
readables = get_list_from(
    where_to_save_all_changes,
    get_valid,
    '<br />(.+)',
    False,
    1
)

previous = len(readables)
readables = get_list_of_unique(readables + addables)
update = len(readables)

rewrite(where_to_save_all_changes, '<br />', readables)
rewrite(where_to_find_new_urls)

if update > previous:
    if argument:
        done = f'Command line argument{"s" if update - previous > 1 else ""}'
        done += f' moved in {where_to_save_all_changes}'
    else:
        done = f'Content of {where_to_find_new_urls}'
        done += f' moved to {where_to_save_all_changes}'
else:
    if argument:
        done = f'There was no valid new URL passed as an argument'
    else:
        done = f'There was no valid new URL in {where_to_find_new_urls}'

print_status(built_margin, done, True)



#-----> INTERACTIVE

print_manual(built_margin, '"x" ends, "examples\.io" searches')

while True:
    choice = get_input(built_margin, 'Something to delete? ')

    if choice == 'x':
        print_status(built_margin, 'End of execution')
        quit()

    for key in readables:
        try:
            deletables.append(re.search(f'(.*)?{choice}(.*)?', key).group(0))
        except:
            continue

    if len(deletables):
        for key in deletables:
            print(built_margin + key)

        print_manual(built_margin, '"x" ends, "v" valids, other cancels')

        choice = get_input(built_margin, 'Do you confirm deletion? ')

        if choice == 'v':
            for key in deletables:
                readables.remove(key)
            rewrite(where_to_save_all_changes, '<br />', readables)
            rewrite(where_to_find_new_urls)
            print_status(built_margin, 'Deletion done')
        else:
            print_status(built_margin, 'Deletion canceled')

        if choice == 'x':
            print_status(built_margin, 'End of execution')
            quit()

        deletables = list()
    else:
        print_status(built_margin, 'No match')
        