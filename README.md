# ABOUT THIS APP
Meal planning can be a hassle, especially when it comes to writing down all the ingredients you need for each meal. This becomes even more time-consuming when planning a weekly shop and needing to combine ingredients from multiple recipes.

ChefBuddy is designed to make this process easier by automatically gathering ingredients from your chosen recipes into one unified shopping list. Simply provide a link to an online recipe or upload an image of a recipe from a cookbook. ChefBuddy will extract the text from the source, identify the ingredients using advanced AI, and allow you to add as many recipes as you like. When you're done, it combines all the ingredients into a single shopping list, ready for you to copy and use.

# TRY THIS CODE YOURSELF!
Currently this is a work-in-progress POC.  It works - though like all things it can be improved.  Right now it is only accessible via a command line interface, but the goal is to eventually turn this into a full GUI-enabled webapp built with bubble.io.  Follow the instructions if you want to try out the CLI today, or check back later to try the MVP webapp.

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
- `anthropic`
- `opencv-python` (for `cv2`)
- `numpy`

# OpenAI Notes

**This application requires a paid tier of OpenAI because it uses the GPT-4 model.**

Future improvements to the application will likely also surpass the rate-per-minute limits of the free model, so you need to use the paid model.  I'm also exploring using Anthropic as their context window is larger meaning fewer calls need to be made.

# Running Instructions

1. **Get an API key from OpenAI.**
   
2. **Create a `.env` file at the application root level.**  
   Include the field named `OPENAI_API_KEY` and add your API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
3. **Run main() in _main_.py.**

4. **Follow the instructions in the terminal, and that's it!**

> 📝 **Note 1a: Images: file naming conventions**  
> If you're taking an image of a recipe to use with this code, make sure the image filename matches the recipe name, using underscores to separate words.  
>  
> **Example:**  
> For a recipe named "Cacio e Pepe," name the image file `cacio_e_pepe.jpg`.  
>  
> The program will automatically remove the underscores and format the recipe name accordingly.

> 📝 **Note 1b: Images: Watch out for spine curves**  
> make sure the image is as flat as possible.  ingredient lists near the spine of a book tend to have slightly curved text which confuses text recognition software.  I've tried various techniques including using deep-learning algorithms like easyOCR or modifying PSM values with pytesseract and none of them work to properly identify the ingredients.  This means the best solution for now is to just have a flat image for best results and to improve results even better, try to isolate the ingredients in the image.

> 🌐 **Note 2:**  
> When providing an HTML link, ensure you include the entire address, including the protocol (`http://` or `https://`).  
>  
> **Example:**  
> Use the full URL like `https://chejorge.com/2020/07/24/vegan-dan-dan-noodles/`.


# Next Improvements for MVP Release

- ~~enhance prompt to remove redundancies and minor LLM response inconsistencies~~
- ~~allow for recipe adjustments / portion size adjustements~~
- Developing a GUI / Webapp using Bubble.io

# Future Considerations

- Option to save recipes into a permanent, personal cookbook.
- Integration with Tesco, Sainsbury's, Amazon Fresh, Ocado.
- Meal suggestions based on ingredients.
