import sys

if __name__ == '__main__':
    currency = sys.argv[1]

    all_links = set()
    with open('all_links_{}.txt'.format(currency), 'r') as all_links_file:
        for line in all_links_file:
            if line != '\n':
                all_links.add(line)
    
    to_be_excluded = set()
    with open('to_be_excluded_{}.txt'.format(currency), 'r') as to_be_excluded_file:
        for line in to_be_excluded_file:
            if line != '\n':
                to_be_excluded.add(line)
    
    links = all_links.difference(to_be_excluded)
    with open('links_{}.txt'.format(currency), 'w') as links_file:
        for link in links:
            links_file.write(link)
        links_file.write('\n')