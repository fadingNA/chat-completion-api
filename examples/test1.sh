API_KEY="fill-in-your-api-key"
INPUT="Please use this application and provide me a readme.md file"

# Run the Python script with the desired arguments
python3 ../app/play.py --api_key "$API_KEY" \
-i "$INPUT" \
--temperature 0.7 \
--max_tokens 600 \
--model gpt-4 \
--output_file output.txt \
--source ../app/play.py