API_KEY="change this to your API key"
INPUT="Derivative of x^2"

# Run the Python script with the desired arguments
python3 ../app/play.py --api_key "$API_KEY" \
-i "$INPUT" \
--temperature 0.7 \
--max_tokens 50 \
--model gpt-4 \
--output_file output.txt