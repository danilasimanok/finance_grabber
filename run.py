import subprocess
import sys
from time import sleep
import os
from datetime import datetime

def collect_all_links(depth, links_to_analyze):
    for currency in links_to_analyze:
        with open('all_links_{}.txt'.format(currency), 'w') as all_links:
            subprocess.call(['python', 'click_to_get_info.py', links_to_analyze[currency], depth], stdout = all_links)

def fill_table(table_name, authors_dump_name, links_name_pattern, links_to_analyze):
    for currency in links_to_analyze:
        with open(links_name_pattern.format(currency), 'r') as all_links:
            subprocess.call(['python', 'fill_table.py', table_name, authors_dump_name, currency], stdin = all_links)

if __name__ == '__main__':
    
    links_to_analyze = {}
    with open('links_to_analyze.txt', 'r') as initial_links_file:
        line = initial_links_file.readline()
        while line != '\n':
            splet = line.split()
            links_to_analyze[splet[0]] = splet[1]
            line = initial_links_file.readline()
    
    initial_collecting_needed = bool(sys.argv[1])
    initial_depth = sys.argv[2]
    table_name = sys.argv[3]
    authors_dump_name = sys.argv[4]
    interval = int(sys.argv[5])

    time_start = datetime.now()

    if initial_collecting_needed:
        print('Initial data collecting...')
        
        collect_all_links(initial_depth, links_to_analyze)
        
        # define links to be excluded while continious calls
        for currency in links_to_analyze:
            with open('all_links_{}.txt'.format(currency), 'r') as all_links:
                with open('to_be_excluded_{}.txt'.format(currency), 'w') as to_be_excluded:
                    for i in range(12): #12 -- number of links in main page
                        to_be_excluded.write(all_links.readline())
        
        fill_table(table_name, authors_dump_name, 'all_links_{}.txt', links_to_analyze)
    
    print('Initial data collection done in {}'.format(datetime.now() - time_start))
    print('The solution may be closed until cycle start.')

    running = True
    while running:
        try:
            sleep(interval)
            print('Cycle started. Please, do not interrupt.')

            collect_all_links('0', links_to_analyze)
            print('Collected.')
            
            for currency in links_to_analyze:
                subprocess.call(['python', 'exclude.py', currency])
            print('Excluded.')
            
            fill_table(table_name, authors_dump_name, 'links_{}.txt', links_to_analyze)
            print('Filled.')

            for currency in links_to_analyze:
                os.replace('all_links_{}.txt'.format(currency), 'to_be_excluded_{}.txt'.format(currency))
            
            print('Cycle ended. The solution may be closed.')
        except KeyboardInterrupt:
            running = False