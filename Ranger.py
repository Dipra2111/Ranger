import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import random
import requests
import sys

last_topic = None
last_content = None
memory = {}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning! Sir")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! Sir")

    else:
        speak("Good Evening! Sir")

    speak("I am Ranger. Please tell me how may I assist you today")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

        if "goodbye ranger" in query.lower():
            speak("Goodbye sir Have a nice day! Ranger is going offline.")
            sys.exit()
    
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # ⚠️ Change email & password before running
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Wikipedia search
        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        # Websites
        elif 'open youtube' in query:
            speak("Opening Youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")

        # Friendly talk
        elif 'who are you' in query:
            speak("My name is Ranger and I am your personal assistant and friend")

        elif 'how have you been' in query:
            speak("I am doing great! How are you today?")

        elif 'how are you' in query:
            speak("I am always good. How about you?")

        elif 'my name' in query:
            speak("Your name is Dipra Banerjee, my boss!")

        elif 'who is your friend' in query:
            speak("You are my best friend, always!")

        elif 'whats the best thing about me?' in query:
            speak("You are a very sincere person")

        elif 'best actor' in query:
            speak("If I had to pick one, I’d say Leonardo DiCaprio. His versatility, emotional depth, and dedication to every role make him stand out as the best actor.")

        elif 'best actress' in query:
            speak("If I had to pick one, I’d go with Meryl Streep. HSer unmatched versatility, ability to transform into any character, and decades of consistently powerful performances make her the best actress in my view.")


        elif 'best cricketer' in query:
            speak("Virat Kohli for sure sir. He is one of the greatest cricketers of all time, known for his consistency and passion for the game.")

        
        elif 'best footballer' in query:
            speak("If I had to choose one, I’d say Lionel Messi has an upper hand. His vision, dribbling, consistency, and record-breaking achievements make him the greatest footballer of all time.")
        

        elif 'i am sad' in query:
            speak("Don’t be sad. You are stronger than you think, Dipra. Want me to play some music?")

        elif 'what is love' in query:
            speak("Love is a beautiful feeling, but I think you should ask your crush, not me, haha!")

        # Time
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        # Media & Apps
        elif 'play music' in query:
            music_dir = "C:\\Users\\Dipro Banerjee\\Music\\Favourites"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'play movies' in query:
            movPath = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"
            os.startfile(movPath)
            speak("Play the movie you want to watch")

        elif 'play fifa' in query:
            fifaPath = "C:\\Games\\FIFA 19 CPY\\Setup\\FIFA19.exe"
            os.startfile(fifaPath)

        elif 'open word' in query:
            wordPath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.exe"
            speak("Opening Microsoft Word")
            os.startfile(wordPath)

        elif 'open powerpoint' in query:
            powPath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.exe"
            speak("Opening Microsoft Powerpoint")
            os.startfile(powPath)

        elif 'open notepad' in query:
            speak("Opening Notepad")
            os.startfile("C:\\Windows\\System32\\notepad.exe")

        elif 'open calculator' in query:
            speak("Opening Calculator")
            os.startfile("C:\\Windows\\System32\\calc.exe")

        # Email
        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "someone@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I can't send this email right now.")

        # Fun & Facts
        elif 'tell me a joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)
            last_topic = "joke"
            last_content = joke


        elif 'tell me a fact' in query:
            try:
                res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
                fact = res.json()["text"]
                speak("Here’s a random fact for you.")
                speak(fact)
                print(fact)
                last_topic = "fact"
                last_content = fact
            except:
                speak("Sorry, I couldn’t fetch a fact right now.")

        elif 'explain it' in query or "i didn't get" in query:
            if last_topic == "joke":
                speak("Okay, let me explain the joke.")
                speak("It’s meant to be funny because it uses wordplay and exaggeration.")
            elif last_topic == "fact":
                speak("That fact is interesting because it shows how amazing the world can be!")
            else:
                speak("Explain what? I don’t remember telling you something.")
        elif 'that\'s interesting' in query or 'tell me more' in query:
            if last_topic == "fact":
                speak("Sure! Let me give you another cool fact.")
                res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
                new_fact = res.json()["text"]
                speak(new_fact)
                print(new_fact)
                last_content = new_fact
            elif last_topic == "joke":
                speak("I can tell you another joke if you want.")
            else:
                speak("Tell you more about what?")
        elif 'another one' in query:
            if last_topic == "joke":
                joke = pyjokes.get_joke()
                speak(joke)
                print(joke)
                last_content = joke
            elif last_topic == "fact":
                res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
                fact = res.json()["text"]
                speak(fact)
                print(fact)
                ast_content = fact
            else:
                speak("Another what? Joke, fact, or something else?")


        # Notes
        elif 'make a note' in query:
            speak("What should I write?")
            note = takeCommand()
            with open("notes.txt", "a") as f:
                f.write(f"{datetime.datetime.now()}: {note}\n")
            speak("I have made a note for you.")

        elif 'read my notes' in query:
            try:
                with open("notes.txt", "r") as f:
                    notes = f.read()
                speak("Here are your notes.")
                print(notes)
                speak(notes)
            except:
                speak("You don’t have any notes yet.")

        # Weather (replace with your OpenWeather API key)
        elif 'weather' in query:
            try:
                api_key = "dcd239398d3d5e4680683dc39f548e17"
                city = "Kolkata"
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                res = requests.get(url).json()
                temp = res['main']['temp']
                desc = res['weather'][0]['description']
                speak(f"The weather in {city} is {desc} with a temperature of {temp} degree Celsius.")
            except:
                speak("Sorry, I couldn't fetch the weather right now.")

        # News (replace with your NewsAPI key)
        elif 'news' in query:
            try:
                api_key = "7d239ac5453f47c0b552cdce0f8d6a75"
                url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
                res = requests.get(url).json()
                articles = res["articles"][:5]
                speak("Here are the top 5 news headlines")
                for i, article in enumerate(articles, 1):
                    speak(f"News {i}: {article['title']}")
            except:
                speak("Sorry, I couldn't fetch the news right now.")

        # Mini Games
        elif 'flip a coin' in query:
            coin = random.choice(["Heads", "Tails"])
            speak(f"I flipped a coin and it landed on {coin}")

        elif 'roll a dice' in query:
            dice = random.randint(1, 6)
            speak(f"You rolled a {dice}")

        elif 'guess a number' in query:
            num = random.randint(1, 10)
            speak("I am thinking of a number between 1 and 10. Try to guess it.")
            guess = takeCommand()
            if guess.isdigit() and int(guess) == num:
                speak("Wow! You guessed it right.")
            else:
                speak(f"Oops, I was thinking of {num}. Better luck next time.")
        
        elif "remember that my favorite" in query:
            try:
                item = query.replace("remember that my favorite", "").strip()
                if item:
                    key, value = item.split(" is ")
                    memory[key.strip()] = value.strip()
                    speak(f"Okay, I’ll remember your favorite {key} is {value}")
            except:
                speak("Sorry, I couldn’t save that properly.")
        
        elif "what's my favorite" in query:
            key = query.replace("what's my favorite", "").strip()
            if key in memory:
                speak(f"Your favorite {key} is {memory[key]}")
            else:
                speak(f"I don’t know your favorite {key} yet. You can tell me by saying remember.")

        elif 'i am bored' in query:
            choice = random.choice(["joke", "fact", "music"])
            if choice == "joke":
                joke = pyjokes.get_joke()
                speak("Here’s a joke to cheer you up.")
                speak(joke)
            elif choice == "fact":
                res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
                fact = res.json()["text"]
                speak("Here’s a cool fact.")
                speak(fact)
            else:
                music_dir = "C:\\Users\\Dipro Banerjee\\Music\\Favourites"
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, random.choice(songs)))
                speak("Here’s some music for you!")
        
        elif 'i am tired' in query:
            speak("Take a deep breath, relax, and remember you’re doing great. Want to share whats going on lately?")

        elif 'i have been feeling alone' in query:
            speak("I am here if you need to talk about anything.")
        

        elif 'cricket score' in query:
            try:
                res = requests.get("https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent", 
                                   headers={"X-RapidAPI-Key": "your_api_key"}).json()
                match = res["typeMatches"][0]["seriesMatches"][0]["seriesAdWrapper"]["matches"][0]
                team1 = match["matchInfo"]["team1"]["teamName"]
                team2 = match["matchInfo"]["team2"]["teamName"]
                status = match["matchInfo"]["status"]
                speak(f"{team1} versus {team2}. Current status: {status}")
            except:
                speak("Sorry, I couldn’t fetch the cricket score right now.")
        

        elif 'set reminder' in query:
            speak("What should I remind you about?")
            task = takeCommand()
            speak("In how many minutes?")
            minutes = int(takeCommand())
            speak(f"Okay, I’ll remind you about {task} in {minutes} minutes.")
            import threading, time
            def reminder(task, minutes):
                time.sleep(minutes*60)
                speak(f"Reminder! {task}")
            threading.Thread(target=reminder, args=(task, minutes)).start()

        elif 'rock paper scissors' in query:
            speak("Okay, let’s play Rock Paper Scissors. Say your choice!")
            user = takeCommand()
            computer = random.choice(["rock", "paper", "scissors"])
            speak(f"I chose {computer}")
            if user == computer:
                speak("It’s a tie!")
            elif (user == "rock" and computer == "scissors") or (user == "scissors" and computer == "paper") or (user == "paper" and computer == "rock"):
                speak("You win!")
            else:
                speak("I win!")




        
