# ABOUT THIS APP
One of the biggest and most time consuming problems with meal planning is writing down all the ingredients you need to buy for a meal.  this problem is made worse when you are planning a weekly shop and need to aggregate the ingredients for multiple recipes.

This code is designed to simplify aggregating recipe ingredients to create one single shopping list. If you see a recipe you like either online or in a cookbook, all you need to do is provide the link to the recipe or an image of the recipe.  this program will scrape the text from either the website or the image and use chatGPT to extract the ingredients required to make the recipe.  you can add as many recipes as you want.  Once you are finished - the code will aggregate all the ingredients together to create one singular shopping list that you can copy and paste into your notebook.

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

> 📝 **Note 1:**  
> If you're taking an image of a recipe to use with this app, make sure the image filename matches the recipe name, using underscores to separate words.  
>  
> **Example:**  
> For a recipe named "Cacio e Pepe," name the image file `cacio_e_pepe.jpg`.  
>  
> The program will automatically remove the underscores and format the recipe name accordingly.

> 🌐 **Note 2:**  
> When providing an HTML link, ensure you include the entire address, including the protocol (`http://` or `https://`).  
>  
> **Example:**  
> Use the full URL like `https://chejorge.com/2020/07/24/vegan-dan-dan-noodles/`.


# Next Improvements for MVP Release

- Allowing for an intermediary step to adjust individual recipe quantities before storing in a shopping list in case some recipes are for too many (or not enough) people.
- Developing a GUI / Webapp using Bubble.io (this will be final step for MVP...probably).

# Future Considerations

- Option to save recipes into a permanent, personal cookbook.
- Integration with Tesco, Sainsbury's, Amazon Fresh, Ocado.
- Meal suggestions based on ingredients.
