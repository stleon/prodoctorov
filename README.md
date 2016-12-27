run 

scrapy crawl doctors -o doctors.json -s LOG_FILE=doctors.log


scrapy parse --spider=doctors -c parse_doctor_list -v https://prodoctorov.ru/belgorod/allergolog/ -d 2



365195

js https://prodoctorov.ru/belgorod/vrach/#all_spec