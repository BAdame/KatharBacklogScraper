Python scripts for analyzing HTML files.

### html_to_text.py
Converts HTML files to text files. This is done once on the data set, as rendering HTML is very expensive. 
To render files in parallel use the below command, where 'input.txt' contains the complete list of all files to render.
```bash
for file in $(cat input.txt); do\
  sem --no-notice -j 2 python html_to_text.py $file;\
done
```

### wrds_rendered_files_scraper.py 
This is where the bulk of the scraping logic lives.
