PYTHON NOTES: 
ALL THE FOLLOWING PYTHON LIBRARIES WILL NEED TO BE 
INSTALLED ON YOUR LOCAL DEVICE BEFORE RUNNING THE PROGRAM:
-os
-json
-re
-openai
-selenium
-time
-BeautifulSoup
-urlparse
-pytesseract
-Image
-dotenv

OPENAI NOTES:
THIS APPLICATION REQUIRES A PAID TIER OF OPENAI BECAUSE IT USES THE GPT-4 MODEL.
LATER IMPROVEMENTS THIS APPLICATION WILL LIKELY ALSO SURPASS THE RATE-PER-MINUTE LIMITS OF THE FREE MODEL, SO YOU NEED TO USE THE PAID MODEL.

RUNNING INSTRUCTIONS:
STEP 1: Get an API key from Open AI
STEP 2: create a .env file at the application root level. inclue field named OPENAI_API_KEY and add your API key.
STEP 3: run main() in _main_.py
STEP 4: follow the instructions in the terminal, and that's it!

NEXT IMPROVEMENTS FOR MVP RELEASE:
- allowing for an intermediary step to adjust individual recipe quantities before storing in a shopping list in case some recipes are for too many (or not enough) people
- GUI / Webapp using bubble.io (this will be MVP)

FUTURE CONSIDERATION:
- option to save recipes into a permanent, personal cookbook
- integration with tesco, sainsbury, amazon fresh, ocado
- meal suggestions based on ingredients