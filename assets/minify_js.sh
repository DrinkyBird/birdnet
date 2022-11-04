#!/usr/bin/env bash

for f in *.js; do
	if [[ "$f" == *.min.js ]]; then
		continue
	fi
	if [[ "$f" == "closure_externs.js" ]]; then
		continue
	fi
	
	fn=`basename "$f" .js`
	
	echo $f
	java -jar "$HOME/bin/closure-compiler-v20220202.jar" --compilation_level ADVANCED_OPTIMIZATIONS --externs closure_externs.js --js "$f" --js_output_file "$fn".min.js
done
