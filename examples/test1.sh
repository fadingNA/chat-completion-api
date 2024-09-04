API_KEY="YOUR_API_KEY"
INPUT="Please summarize the key points from the following text:"

# Run the Python script with the desired arguments
python3 ../app/play.py ../examples/computer_vision.txt --api_key "$API_KEY" \
-i "$INPUT" \
--temperature 0.7 \
--max_tokens 300 \
--model gpt-4 \
--output_file output.txt
