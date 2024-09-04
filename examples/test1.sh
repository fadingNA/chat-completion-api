API_KEY="....."
INPUT="Please convert json into csv format"

# Run the Python script with the desired arguments
python3 ../app/play.py ../examples/sample2.json --api_key "$API_KEY" \
-i "$INPUT" \
--temperature 0.7 \
--max_tokens 600 \
--model gpt-4 \
--output_file output.txt
