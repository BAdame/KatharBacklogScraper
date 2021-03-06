Python scripts for analyzing HTML files.

### Running the transcript analyzer
The `src/wrds_transcript_scraper.py` file is used to analyze transcript files. See the 'exampleFiles' directory for an example of a file to use as input, and an example of what the transcripts should look like.

#### Running the script
```bash
python src/wrds_transcript_scraper.py --transcript-files-root ./inputFiles/transcripts --output-file ./output/transcript-test.csv --input-file ./inputFiles/transcript_test_input.cs
```

Use `python src/wrds_transcript_scraper.py --help` to see examples for running the script.

## Downloading new files
1. ssh to the wrds server 
2. Define a file of all the files you want
3. Zip them all `zip zippedFiles -@ < ListOfFilesToPull.txt`
4. `scp` the zip to the project's root directory
5. unzip them to the common directory `unzip zippedFiles.zip -d wrds-files/`
6. render them with the steps below

## Other scripts
### html_to_text.py
Converts HTML files to text files. This is done once on the data set, as rendering HTML is very expensive. 
To render files in parallel use the below command, where 'input.txt' contains the complete list of all files to render.
```bash
for file in $(cat input.txt); do\
  # Run (NUM_CPUS - 1) processes
  sem --no-notice -j -1 python html_to_text.py $file;\
done
```

### wrds_rendered_files_scraper.py 
This is where the bulk of the scraping logic lives.

### Running on AWS
1. Go to project's root directory
1. Spin up an EC2 host
```bash
HOST=<ec2-dns-name>
KEY=<keypair-location>

# Probably not necessary every time
tar -zcvf Files.tar.gz wrds-files

# Copy files to EC2 (zip, input, bin)
scp -i $KEY $FILE_TO_COPY  ec2-user@$HOST:/home/ec2-user

# SSH to the host
ssh -i $KEY ec2-user@$HOST

# Run the setup script
./bin/ec2-setup.sh

# Run the python script
for file in $(cat input.txt); do\
  sem --no-notice -j -1 python html_to_text.py $file;\
done

# zip the rendered files
tar -zcvf RenderedFiles.tar.gz textfiles

# Exit EC2
exit

# Copy rendered files
scp -i $KEY  ec2-user@$HOST:/home/ec2-user/project/RenderedFiles.tar.gz .

# Extract rendered files
```

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
