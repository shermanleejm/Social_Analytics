from scrapy import cmdline

cmdline.execute("scrapy crawl hwz -o ../data/hwz.json -t json".split())