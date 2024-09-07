# Python Notes

**The following Python libraries must be installed on your local device before running the program:**

- `os`
- `json`
- `re`
- `openai`
- `selenium`
- `time`
- `beautifulsoup4` (for `BeautifulSoup`)
- `urllib.parse` (for `urlparse`)
- `pytesseract`
- `Pillow` (for `Image`)
- `python-dotenv` (for `dotenv`)

# OpenAI Notes

**This application requires a paid tier of OpenAI because it uses the GPT-4 model.**

Future improvements to the application will likely also surpass the rate-per-minute limits of the free model, so you need to use the paid model.

# Running Instructions

1. **Get an API key from OpenAI.**
   
2. **Create a `.env` file at the application root level.**  
   Include the field named `OPENAI_API_KEY` and add your API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
3. **Run main() in _main_.py.**

4. **Follow the instructions in the terminal, and that's it!**

# Next Improvements for MVP Release

- Allowing for an intermediary step to adjust individual recipe quantities before storing in a shopping list in case some recipes are for too many (or not enough) people.
- Developing a GUI / Webapp using Bubble.io (this will be MVP).

# Future Considerations

- Option to save recipes into a permanent, personal cookbook.
- Integration with Tesco, Sainsbury's, Amazon Fresh, Ocado.
- Meal suggestions based on ingredients.
