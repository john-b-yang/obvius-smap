from bmo.bmo_import import import_URLs
from crawler.crawl_bmo import crawler
from parser.parse_bmo import request_urls

from optparse import OptionParser

from cStringIO import StringIO
import os, re, sys

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

def download_script(options):
    bmo_output = "bmo_output.txt"

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
    if options.hide:
        f = open(os.devnull, 'w')
        sys.stdout=f
    crawler(opts, args)
    sys.stdout = sys.__stdout__
    print "Created config.ini, devices.json files successfully."

    # Retrieve Building Data URLs with config.ini
    print "Retrieving URLs for building data..."
    with Capture() as output:
        import_URLs("config.ini", options.date, options.days)
    print "Completed gathering of URLs"
    output_file = open(bmo_output, "w+")
    output_file.write("\n".join(output))
    print "Created", bmo_output, "file successfully."

    # Request Data per URL from parsing bmo_import output
    print "Gathering building data per URL"
    if options.hide:
        f = open(os.devnull, 'w')
        sys.stdout=f
    request_urls(bmo_output, options.folder)
    sys.stdout = sys.__stdout__

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', dest='date', action="store", default=None, type="string", help='[REQUIRED] specify start date of data collection (MM-DD-YYYY format)')
    parser.add_option('-f', dest='folder', action="store", default="data", type="string", help='specify name of directory to store building data (default data)')
    parser.add_option('-n', dest='days', action="store", default="1", type="string", help='specify number of days starting from \'date\' to collect data (default 1)')
    parser.add_option('-p', dest='hide', action="store_true", help='hide standard output from data retrieval process')
    (opts, args) = parser.parse_args()
    if not opts.date:
        parser.error('Start Date parameter not given (type python app.py --help for list of arguments)')
    download_script(opts)
