import asyncio
import nest_asyncio

from dtc_assistant import DataTalksClubAssistant


async def main():
    assistant = DataTalksClubAssistant()
    print("Welcome to DataTalksClub Assistant!")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        response = await assistant.run(user_input, "default_chat")
        print("Assistant:", response)


if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
