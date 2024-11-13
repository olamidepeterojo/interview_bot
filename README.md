# interview_bot
* This script serves as an interactive interview preparation bot designed to help users practice technical coding interview questions. The bot asks users a set of 40 common coding interview questions randomly, collects the user's responses, and provides feedback or guidance where applicable. 

* Key Features:
- Asks the user interview-related questions from a predefined set of 40 questions.
- Randomly selects questions until all questions are asked or the user decides to quit.
- Accepts user inputs for each question, allowing flexibility in their answers.
- Detects if a user asks non-interview-related questions and provides answers based on a general knowledge base.

* Dependencies:
- Requires the `openai` package if utilizing OpenAI's API to provide responses to non-predefined questions.
- Other dependencies can be found in `requirements.txt`

* How to run
- Create a virtual environment
`python -m venv .venv`

- Install dependencies
`pip install -r requirements.txt`

* Add info to `.env`
- Your OpenAI API key should be stored safely in your `.env` file as this information is very sensitive. 

* Run project
`python interview_bot.py`

TODO
- Add instructions on how to run
- Add `requirements.txt`