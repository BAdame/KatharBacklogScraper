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

### Generating parser files
ANTLR is used to generate a language parser for some of the scripts.

To install:
```bash
curl -O http://www.antlr.org/download/antlr-4.7.1-complete.jar
sudo mv antlr-4.7.1-complete.jar /usr/local/lib

export CLASSPATH=".:/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH"

alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.7.1-complete.jar:$CLASSPATH" org.antlr.v4.Tool' 
alias grun='java org.antlr.v4.gui.TestRig'
```
