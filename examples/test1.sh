API_KEY=""
INPUT="Can you explain this in Thai how to use it"

# Run the Python script with the desired arguments
python3 ../app/play.py ../README.md --api_key "$API_KEY" \
-t 0.5 \
--max_tokens 300 \
--model gpt-4 \
--output output.txt
