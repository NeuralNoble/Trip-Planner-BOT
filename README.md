# Trip Planning Agentic Bot 
TripBot is a Telegram bot designed to help users plan their perfect trips by guiding them through a series of easy steps. From selecting cities and dates to recommending personalized activities based on your interests, TripBot uses AI-powered agents to create customized itineraries. With a simple, conversational interface, TripBot makes travel planning seamless and hassle-free, ensuring you never miss out on key attractions, local experiences, or cultural events. Just chat, and let TripBot handle the rest!



<img width="540" alt="Screenshot 2025-01-20 at 4 16 44 PM" src="https://github.com/user-attachments/assets/c0c8d540-2007-44ca-b0c7-f4baf49fe990" />

## **How It Works**
TravelBot delegates tasks to three specialized agents to plan the trip:
1. **Expert Travel Agent**: Creates the detailed itinerary with day-by-day activities, restaurant suggestions, hotel recommendations, and a budget breakdown.
2. **City Selection Expert**: Analyzes cities based on user preferences (weather, prices, interests) and selects the best city for the trip.
3. **Local Tour Guide**: Gathers city-specific information, including cultural insights, key attractions, special events, and hidden gems.

### **Workflow**
1. **User Input**: The user provides their origin, cities they're interested in, date range, and their interests.
2. **Bot Processing**: The bot delegates tasks to the appropriate agents for city selection, itinerary planning, and gathering local insights.
3. **Results Compilation**: Once the agents complete their tasks, the bot assembles the results into a comprehensive travel plan and sends it to the user.

### **How to Use**
1. **Install Dependencies**: Make sure you have the necessary dependencies installed.
   
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Telegram Bot**: Create a Telegram bot and obtain the **API Token** from [BotFather](https://core.telegram.org/bots#botfather).
   
3. **Create a `.env` File**: Add your Telegram bot token and any other required API keys or configuration values in the `.env` file.

   Example `.env`:
   ```
   TELEGRAM_API_TOKEN=your_telegram_api_token
   ```

4. **Run the Bot**: Start the bot by running the following command:
   
   ```bash
   python bot.py
   ```

   The bot will now be active and ready to interact with users on Telegram.

## **Files**
- **bot.py**: Main file for running the Telegram bot.
- **agents.py**: Contains the logic for creating the different agents (Expert Travel Agent, City Selection Expert, Local Tour Guide).
- **tasks.py**: Defines the tasks for the agents, including itinerary planning, city selection, and gathering city info.
- **.env**: Stores sensitive environment variables (API keys, bot token).

## Demo
https://youtu.be/An9VvKUXGwI
