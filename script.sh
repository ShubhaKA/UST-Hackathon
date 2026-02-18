#!/bin/bash

 

LOGFILE="$1"

if [ -z "$LOGFILE" ]; then
    echo "Usage: $0 logfile"
    exit 1
fi


tr '[:upper:]' '[:lower:]' < "$LOGFILE" | \
tr -c '[:alnum:]' '\n' > words.txt

# Count total words
TOTAL_WORDS=$(wc -l < words.txt)

# Count occurrences of each unique word
sort words.txt | uniq -c > word_count.txt

# Calculate 1% threshold
THRESHOLD=$((TOTAL_WORDS / 100))

echo "Total words: $TOTAL_WORDS"
echo "Threshold (1%): $THRESHOLD"
echo "-----------------------------------"
echo "Lines containing rare words:"
echo "-----------------------------------"

# Find rare words (appear less than 1%)
awk -v threshold="$THRESHOLD" '$1 < threshold {print $2}' word_count.txt > rare_words.txt

# Highlight lines containing rare words
while read word; do
    grep -i --color=always "$word" "$LOGFILE"
done < rare_words.txt
