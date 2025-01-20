import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from crewai import Crew
from textwrap import dedent
from agents import TravelAgents
from tasks import TravelTasks
from dotenv import load_dotenv

load_dotenv()

# Define conversation states
ORIGIN, CITIES, DATE_RANGE, INTERESTS = range(4)

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        agents = TravelAgents()
        tasks = TravelTasks()

        # Define agents
        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        # Define tasks
        plan_itinerary = tasks.plan_itinerary(expert_travel_agent, self.cities, self.date_range, self.interests)
        identify_city = tasks.identify_city(city_selection_expert, self.origin, self.cities, self.interests, self.date_range)
        gather_city_info = tasks.gather_city_info(local_tour_guide, self.cities, self.date_range, self.interests)

        # Create crew and run the tasks
        crew = Crew(
            agents=[expert_travel_agent, city_selection_expert, local_tour_guide],
            tasks=[plan_itinerary, identify_city, gather_city_info],
            verbose=True,
        )
        result = crew.kickoff()
        try:
            # Convert the result to a string
            return str(result)  # This ensures that the result is returned as a string
        except Exception as e:
            return f"An error occurred while processing the result: {str(e)}"


class TripBot:
    def __init__(self):
        self.trip_data = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Starts the conversation and asks for origin."""
        await update.message.reply_text(
            "Welcome to the Travel Planning Bot! 🌎✈️\n\n"
            "I'll help you plan your perfect trip. "
            "First, please tell me: Where will you be traveling from?"
        )
        return ORIGIN

    async def origin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stores origin and asks for cities."""
        user_id = update.message.from_user.id
        if user_id not in self.trip_data:
            self.trip_data[user_id] = {}

        self.trip_data[user_id]['origin'] = update.message.text

        await update.message.reply_text(
            "Great! Now, what cities are you interested in visiting?\n"
            "Please list them separated by commas (e.g., 'Paris, London, Rome')"
        )
        return CITIES

    async def cities(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stores cities and asks for date range."""
        user_id = update.message.from_user.id
        self.trip_data[user_id]['cities'] = update.message.text

        await update.message.reply_text(
            "Perfect! When are you planning to travel?\n"
            "Please provide the date range (e.g., 'June 15-22, 2024')"
        )
        return DATE_RANGE

    async def date_range(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stores date range and asks for interests."""
        user_id = update.message.from_user.id
        self.trip_data[user_id]['date_range'] = update.message.text

        await update.message.reply_text(
            "Almost done! Finally, what are your interests and hobbies?\n"
            "This will help me personalize your trip recommendations."
        )
        return INTERESTS

    async def interests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stores interests and starts trip planning."""
        user_id = update.message.from_user.id
        self.trip_data[user_id]['interests'] = update.message.text

        await update.message.reply_text(
            "Thanks! I'm now planning your perfect trip. This might take a few minutes... ⏳"
        )

        try:
            # Create and run the trip crew
            trip_crew = TripCrew(
                self.trip_data[user_id]['origin'],
                self.trip_data[user_id]['cities'],
                self.trip_data[user_id]['date_range'],
                self.trip_data[user_id]['interests']
            )

            result = trip_crew.run()

            # Send result
            await update.message.reply_text(result)

            # Clean up stored data
            del self.trip_data[user_id]

            await update.message.reply_text(
                "Planning complete! Feel free to start a new trip planning session with /start"
            )
        except Exception as e:
            await update.message.reply_text(
                f"Sorry, there was an error planning your trip. Please try again with /start\nError: {str(e)}"
            )
            del self.trip_data[user_id]

        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancels and ends the conversation."""
        user_id = update.message.from_user.id
        if user_id in self.trip_data:
            del self.trip_data[user_id]

        await update.message.reply_text(
            "Trip planning cancelled. Feel free to start a new session with /start"
        )
        return ConversationHandler.END

def main():
    # Get your token from environment variables
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables")

    # Create the bot
    trip_bot = TripBot()

    # Create the Application
    application = Application.builder().token(token).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', trip_bot.start)],
        states={
            ORIGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, trip_bot.origin)],
            CITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, trip_bot.cities)],
            DATE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, trip_bot.date_range)],
            INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, trip_bot.interests)],
        },
        fallbacks=[CommandHandler('cancel', trip_bot.cancel)],
    )

    application.add_handler(conv_handler)

    # Start the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
