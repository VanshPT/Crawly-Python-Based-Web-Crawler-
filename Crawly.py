from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *


class Crawly:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Crawly.project_name = project_name
        Crawly.base_url = base_url
        Crawly.domain_name = domain_name
        Crawly.queue_file = Crawly.project_name + '/queue.txt'
        Crawly.crawled_file = Crawly.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Crawly', Crawly.base_url)

    # Creates directory and files for project on first run and starts the Crawly
    @staticmethod
    def boot():
        create_project_dir(Crawly.project_name)
        create_data_files(Crawly.project_name, Crawly.base_url)
        Crawly.queue = file_to_set(Crawly.queue_file)
        Crawly.crawled = file_to_set(Crawly.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Crawly.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Crawly.queue)) + ' | Crawled  ' + str(len(Crawly.crawled)))
            Crawly.add_links_to_queue(Crawly.gather_links(page_url))
            Crawly.queue.remove(page_url)
            Crawly.crawled.add(page_url)
            Crawly.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Crawly.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Crawly.queue) or (url in Crawly.crawled):
                continue
            if Crawly.domain_name != get_domain_name(url):
                continue
            Crawly.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Crawly.queue, Crawly.queue_file)
        set_to_file(Crawly.crawled, Crawly.crawled_file)
