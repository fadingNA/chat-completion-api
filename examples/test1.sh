API_KEY="Get Your API KEY FROM OpenAi.com"
INPUT="Please edit your question here"

# Run the Python script with the desired arguments
python3 play.py --api_key "$API_KEY" \
-i "$INPUT" \
--temperature 0.7 \
--max_tokens 50 \
--model gpt-4 \
--output_file output.txt