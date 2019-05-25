from bmo.bmo_import import import_URLs
from crawler.crawl_bmo import crawler
from parser.parse_bmo import request_urls

from optparse import OptionParser
import threading

from cStringIO import StringIO
import sys

# For purposes of capturing std output
class Capture(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout

def download_script(bmo_output, data_folder):
    # Generate config.ini file
    parser = OptionParser()
    parser.add_option('-t', '--types', dest='types', default=False)
    parser.add_option('-n', '--no-cache', dest='cache', default=True)
    parser.add_option('-b', '--buildings', dest='buildings', default=False)
    parser.add_option('-p', '--progress', dest='progress', default=False)
    parser.add_option('-l', '--load', dest='load', default=True)
    parser.add_option('-d', '--database', dest='db', default=False)
    (opts, args) = parser.parse_args()

    print "Creating config.ini, devices.json files..."
    crawler(opts, args)
    print "Created config.ini, devices.json files successfully."

    # Retrieve Building Data URLs with config.ini
    print "Beginning to retrieve URLs for building data..."
    with Capture() as output:
        import_URLs("config.ini", "04-01-2019", "2")
    print "Completed gathering of URLs"
    output_file = open(bmo_output, "w+")
    output_file.write("\n".join(output))
    print "Created", bmo_output, "file successfully."

    # Request Data per URL from parsing bmo_import output
    request_urls(bmo_output, data_folder)

if __name__ == '__main__':
    download_script("bmo_output.txt", "data")
