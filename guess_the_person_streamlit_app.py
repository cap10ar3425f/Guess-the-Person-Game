import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- Page Configuration ---
st.set_page_config(
    page_title="Guess the Person - Party Charades",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Thread-Safe Global Multi-Room Store for Realtime Cross-Device Sync ---
@st.cache_resource
def get_global_rooms():
    # Persistent dict across all connected browsers & users
    return {}

GLOBAL_ROOMS = get_global_rooms()

# --- Master Decks Data ---
MASTER_DECKS = {
    "Sports Legends ⚽": [
        {"name": "Lionel Messi", "hint": "8-time Ballon d’Or winner, Argentine football GOAT"},
        {"name": "Cristiano Ronaldo", "hint": "Portuguese striker, famous 'SIUUU' celebration"},
        {"name": "Virat Kohli", "hint": "Indian cricket maestro, master of chases & king of aggression"},
        {"name": "MS Dhoni", "hint": "Captain Cool, iconic helicopter shot & lightning stumpings"},
        {"name": "Sachin Tendulkar", "hint": "God of Cricket, 100 international centuries"},
        {"name": "Rohit Sharma", "hint": "The Hitman, record 3 ODI double-hundreds"},
        {"name": "LeBron James", "hint": "King James, 4-time NBA Champion, all-time scoring leader"},
        {"name": "Michael Jordan", "hint": "Chicago Bulls #23, Jumpman logo, basketball icon"},
        {"name": "Roger Federer", "hint": "Swiss maestro, elegant 1-handed backhand, 20 Grand Slams"},
        {"name": "Rafael Nadal", "hint": "King of Clay, intense fist pumps, 14 French Opens"},
        {"name": "Usain Bolt", "hint": "Fastest man alive, famous lightning bolt victory pose"},
        {"name": "Muhammad Ali", "hint": "'Float like a butterfly, sting like a bee'"},
        {"name": "Sania Mirza", "hint": "'Six time Grand Slam Champion in women's doubles'"},
        {"name": "Diego Maradona", "hint": "'Hand of God', Argentine legend, iconic 1986 solo World Cup goal"},
        {"name": "Pele", "hint": "'O Rei', 3-time World Cup winner, Brazilian football icon"},
        {"name": "Kylian Mbappe", "hint": "French speedster, 2022 World Cup final hat-trick hero, folded arms pose"},
        {"name": "Erling Haaland", "hint": "Norwegian goal machine, meditation pose celebration, powerhouse striker"},
        {"name": "Neymar Jr", "hint": "Brazilian flair, flashy rainbow flicks, samba dance celebrations"},
        {"name": "Ronaldinho", "hint": "Joga Bonito king, eternal smile, dazzling no-look passes and elastico"},
        {"name": "Zinedine Zidane", "hint": "French maestro, elegant roulette spin, famous 2006 World Cup headbutt"},
        {"name": "David Beckham", "hint": "Iconic curling free-kicks, fashion superstar, 'Bend It Like Beckham'"},
        {"name": "Kapil Dev", "hint": "1983 World Cup winning captain, famous backward running catch to dismiss Richards"},
        {"name": "Sourav Ganguly", "hint": "'Dada', Prince of Kolkata, iconic Lord's balcony shirt-wave celebration"},
        {"name": "Yuvraj Singh", "hint": "Sixer King, smashed 6 sixes in one over off Broad, 2011 World Cup hero"},
        {"name": "Jasprit Bumrah", "hint": "Boom Boom, unique short run-up action, pinpoint lethal yorkers"},
        {"name": "AB de Villiers", "hint": "Mr. 360, impossible ramp scoops, South African batting genius"},
        {"name": "Chris Gayle", "hint": "Universe Boss, towering sixes, famous Gangnam Style celebration"},
        {"name": "Shane Warne", "hint": "King of Spin, 'Ball of the Century', legendary Australian leg-spinner"},
        {"name": "Brian Lara", "hint": "Prince of Trinidad, high backlift, world-record 400 not out in Tests"},
        {"name": "Hardik Pandya", "hint": "Clutch all-rounder, big-hitting swagger, iconic shrug celebration"},
        {"name": "Neeraj Chopra", "hint": "India's Golden Boy, Olympic javelin champion, famous turning roar pose"},
        {"name": "Novak Djokovic", "hint": "24 Grand Slam titles, elastic baseline slides, roaring chest-thumping celebrations"},
        {"name": "Serena Williams", "hint": "23 Grand Slam singles titles, ferocious power serves, tennis queen"},
        {"name": "Mike Tyson", "hint": "Iron Mike, ferocious peek-a-boo boxing style, youngest heavyweight champion"},
        {"name": "Kobe Bryant", "hint": "The Black Mamba, iconic turnaround fadeaway jumper, 5-time NBA champion"},
        {"name": "Stephen Curry", "hint": "Three-point king, deep buzzer-beaters, famous 'Night Night' celebration"},
        {"name": "Michael Phelps", "hint": "The Flying Fish, record 23 Olympic gold medals, legendary arm-slap warmup"},
        {"name": "Lewis Hamilton", "hint": "7-time Formula 1 World Champion, iconic #44 Mercedes racing driver"},
        {"name": "Max Verstappen", "hint": "Dutch F1 sensation, aggressive overtaking, Red Bull Racing world champion"},
        {"name": "PV Sindhu", "hint": "Two-time Olympic medalist, thunderous smashes, Indian badminton superstar"},
        {"name": "Mary Kom", "hint": "'Magnificent Mary', 6-time World Amateur Boxing Champion, Olympic medalist"},
        {"name": "Sunil Chhetri", "hint": "Captain Fantastic, Indian football talisman, all-time leading national goalscorer"},
        {"name": "Tiger Woods", "hint": "Golf icon, famous fist pump, signature Sunday red polo shirt"}
    ],
    "Cinema & Characters 🎬": [
        {"name": "Shah Rukh Khan", "hint": "King of Romance, iconic open-arms pose"},
        {"name": "Amitabh Bachchan", "hint": "The Big B, legendary deep voice, angry young man"},
        {"name": "Iron Man / Tony Stark", "hint": "Billionaire superhero, snap: 'I am Iron Man'"},
        {"name": "Spider-Man / Peter Parker", "hint": "Shoots webs from wrists, 'With great power...'"},
        {"name": "Captain Jack Sparrow", "hint": "Staggering pirate captain, 'Where is the rum?!'"},
        {"name": "The Joker", "hint": "'Why so serious?', maniacal laugh, Batman villain"},
        {"name": "Wednesday Addams", "hint": "Deadpan stare, viral gothic rave dance"},
        {"name": "Barbie", "hint": "Perfect smile, 'Hi Barbie!', walks on permanent tiptoes"},
        {"name": "Charlie Chaplin", "hint": "Little Tramp, bowler hat, twirling cane, silent comedy"},
        {"name": "Deadpool", "hint": "Breaks 4th wall, dual katanas, witty mercenary"},
        {"name": "Feluda / Pradosh C. Mitter", "hint": "Satyajit Ray's sleuth, Charminar cigarette, sharp brain 'Mogojastro'"},
        {"name": "Byomkesh Bakshi", "hint": "Bengal's 'Satyanweshi' (truth-seeker), traditional dhoti, sharp deduction"},
        {"name": "Uttam Kumar", "hint": "Mahanayak of Bengali cinema, hypnotic smile, classic romantic mannerisms"},
        {"name": "Soumitra Chatterjee", "hint": "Apu and original Feluda, intellectual screen presence, Satyajit Ray's muse"},
        {"name": "Prosenjit Chatterjee", "hint": "'Bumba Da', undisputed superstar of Tollywood, intense dramatic dialogue delivery"},
        {"name": "Mithun Chakraborty", "hint": "Disco Dancer, leg swivel moves, 'Koi Shaq?' and ferocious dialogue delivery"},
        {"name": "Dev", "hint": "Commercial Tollywood powerhouse, 'Chander Pahar' adventurer Shankar, energetic dance"},
        {"name": "Jeet", "hint": "'Boss' of Bengali action cinema, aviator sunglasses, stylized punch dialogues"},
        {"name": "Tenida", "hint": "'De-la-grandee mephistopheles', nose twitching, Potoldanga gang leader"},
        {"name": "Goopy & Bagha", "hint": "Clapping hands to freeze people, magical boots, singing and dholak duo"},
        {"name": "Jatayu / Lalmohan Ganguly", "hint": "Thriller writer, quirky gestures, sidekick to Feluda, funny green Ambassador stories"},
        {"name": "Magheswar Goenda / Ekenbabu", "hint": "Bald, quirky gestures, loves delicious food, surprisingly genius detective"},
        {"name": "Bhanu Bandopadhyay", "hint": "Legendary East-Bengal comic accent, wide-eyed expressions, comedic master"},
        {"name": "Robi Ghosh", "hint": "Bagha and comedy legend, exaggerated rubber-face expressions and comedic timing"},
        {"name": "Rabi Ranjan Maitra / Kakababu", "hint": "Sunil Gangopadhyay's crutch-wielding adventurer, brave explorer Raja Roychowdhury"},
        {"name": "Rajinikanth", "hint": "Thalaivar, flipping sunglasses, lighting cigarette with pistol, high-speed walk"},
        {"name": "Kamal Haasan", "hint": "Ulaganayagan, chameleon actor, Indian Thatha finger locks, multifaceted master"},
        {"name": "Allu Arjun / Pushpa Raj", "hint": "'Jhukega nahi saala', signature beard stroke, shoulder shrug walk"},
        {"name": "Yash / Rocky Bhai", "hint": "K.G.F kingpin, smoking cigar, firing machine gun, long bearded gangster swagger"},
        {"name": "Prabhas / Baahubali", "hint": "Lifting massive Shiva Lingam on shoulder, roaring warrior king of Mahishmati"},
        {"name": "Thalapathy Vijay", "hint": "Chewing gum flick, signature energetic hooks, charismatic whistle-worthy swagger"},
        {"name": "Ajith Kumar", "hint": "Thala, salt-and-pepper hair, superbike wheelies, cool collected action star"},
        {"name": "Ram Charan", "hint": "Alluri Sitarama Raju in RRR, bow and arrow, fierce tribal-warrior dance step"},
        {"name": "Jr NTR", "hint": "Komaram Bheem in RRR, fighting wild tigers, high-octane 'Naatu Naatu' suspension kicks"},
        {"name": "Rishab Shetty / Shiva", "hint": "'Kantara' Bhoota Kola roar, wide glaring eyes, divine primal scream"},
        {"name": "Mohanlal", "hint": "The Complete Actor, twisting his traditional mundu, effortless natural subtlety"},
        {"name": "Mammootty", "hint": "Megastar of Malayalam cinema, towering voice, sharp stylish demeanor"},
        {"name": "Dhanush", "hint": "'Kolaveri Di' star, lungi-clad underdog, hyper-realistic emotional acting"},
        {"name": "Suriya / Rolex", "hint": "Menacing villain cameo in Vikram, gold watch obsession, ruthless psychotic grin"},
        {"name": "Vijay Sethupathi / Bhavani", "hint": "Makkal Selvan, punch-clenched knuckles, casual deadpan gangster dialogue"},
        {"name": "Salman Khan / Chulbul Pandey", "hint": "Sunglasses hanging on back of collar, belt dance step, 'Dabangg' swagger"},
        {"name": "Aamir Khan", "hint": "Mr. Perfectionist, PK wide alien eyes, quirky earnest expressions"},
        {"name": "Hrithik Roshan", "hint": "'Kaho Naa Pyaar Hai' iconic shoulder move, robotic popping dance, Greek God"},
        {"name": "Ranveer Singh", "hint": "Unmatched hyper-energy, eccentric colorful outfits, fierce Khilji beast dance"},
        {"name": "Ranbir Kapoor", "hint": "'Rockstar' guitar scream, intense emotional brooding, 'Animal' machine-gun swagger"},
        {"name": "Gabbar Singh", "hint": "'Kitne aadmi the?', dragging leather belt on rocks, Sholay's terrifying dacoit"},
        {"name": "Mogambo", "hint": "'Mogambo khush hua!', tapping silver finger ring on golden throne"},
        {"name": "Crime Master Gogo", "hint": "'Aankhen nikaal kar gotiyan khelunga', villain cape, Andaaz Apna Apna comic"},
        {"name": "Deepika Padukone", "hint": "Dimpled smile, regal 'Padmaavat' graceful walk, Shanti Priya wave"},
        {"name": "Kareena Kapoor / Geet", "hint": "'Main apni favorite hoon!', non-stop chatterbox, Jab We Met icon"},
        {"name": "Batman / Bruce Wayne", "hint": "'I am vengeance', dark cape, gravelly deep whisper voice, Bat-signal"},
        {"name": "Superman / Clark Kent", "hint": "Ripping open business shirt to reveal 'S' logo, heat vision, flying pose"},
        {"name": "Captain America", "hint": "Vibranium shield throw, 'I can do this all day', righteous hero posture"},
        {"name": "Thor", "hint": "God of Thunder, summoning flying hammer Mjolnir, roaring lightning strike"},
        {"name": "Hulk", "hint": "'Hulk Smash!', turning green with rage, giant chest beating roar"},
        {"name": "Wolverine / Logan", "hint": "Extending adamantium claws from knuckles, cigar chew, feral animal growl"},
        {"name": "Thanos", "hint": "The Mad Titan, golden Infinity Gauntlet, universal snap of his fingers"},
        {"name": "Harry Potter", "hint": "Lightning bolt scar, circular glasses, swish and flick wand incantation"},
        {"name": "Lord Voldemort", "hint": "No nose, serpentine hissing voice, 'Avada Kedavra' wand flourish"},
        {"name": "Jack Dawson", "hint": "Titanic bow pose, 'I'm the king of the world!', sketchpad artist"},
        {"name": "Neo / The Matrix", "hint": "Dodging bullets backward in slow motion, black trench coat, sunglasses"},
        {"name": "John Wick", "hint": "Pencil fighting assassin, sharp suit, reloading pistols at lighting speed"},
        {"name": "James Bond / 007", "hint": "Straightening tuxedo bowtie, drinking martini 'shaken, not stirred'"},
        {"name": "Vito Corleone / The Godfather", "hint": "Stroking a cat, raspy voice, 'An offer he can't refuse'"},
        {"name": "Gollum", "hint": "Crouching on all fours, raspy whisper: 'My Preciousss!', split personality"},
        {"name": "Sherlock Holmes", "hint": "Deerstalker hat, curved calabash pipe, examining footprints with magnifying glass"},
        {"name": "Darth Vader", "hint": "Heavy mechanical breathing sound, black helmet, red lightsaber, force choke"},
        {"name": "Yoda", "hint": "Tiny green Jedi master, speaking in reversed grammar: 'Do, or do not'"},
        {"name": "Marilyn Monroe", "hint": "Blowing a kiss, dress flying up over subway grate, breathy voice"},
        {"name": "Tom Cruise / Ethan Hunt", "hint": "Sprinting at top speed with flat palms, hanging off planes and cliffs"},
        {"name": "Lord Krishna", "hint": "Playing the divine flute (bansuri), peacock feather on head, butter thief"},
        {"name": "Lord Shiva / Mahadev", "hint": "Third eye on forehead, holding a trident (Trishul) and damru, Nataraja dance"},
        {"name": "Lord Hanuman", "hint": "Carrying the Sanjeevani mountain in one hand, mace (Gada) in the other, tearing chest open"},
        {"name": "Lord Rama", "hint": "Maryada Purushottam, holding a divine bow and arrow, righteous royal poise"},
        {"name": "Goddess Durga", "hint": "Ten arms wielding celestial weapons, riding a roaring lion, slaying Mahishasura"},
        {"name": "Lord Ganesha", "hint": "Elephant head, broken tusk, holding a modak, riding a tiny mouse"},
        {"name": "Ravana", "hint": "Ten-headed demon king of Lanka, playing the Veena, arrogant booming laughter"},
        {"name": "Arjuna", "hint": "Peerless archer of the Pandavas, aiming at the rotating fish's eye, drawing the Gandiva bow"},
        {"name": "Karna", "hint": "Danveer, born with golden armor (Kavacha) and earrings (Kundala), tragic master warrior"},
        {"name": "Bhima", "hint": "Vrikodara, immense brute strength, roaring while swinging a massive iron mace"},
        {"name": "Draupadi", "hint": "Born from sacred fire, refusing to tie her hair until avenged, endless saree miracle"},
        {"name": "Kumbhakarna", "hint": "Giant demon warrior who sleeps for six months, eating heaps of feast when awoken"},
        {"name": "Goddess Kali", "hint": "Garland of skulls, protruding red tongue, holding a scimitar, stepping on Shiva"},
        {"name": "Narada Muni", "hint": "Strumming the Tanpura, chanting 'Narayan Narayan', celestial traveler and instigator"},
        {"name": "Bhishma Pitamaha", "hint": "Vow of lifelong celibacy, boon of choosing his time of death, lying on a bed of arrows"},
        {"name": "Shakuni Mama", "hint": "Walking with a distinct limp, rolling enchanted dice, mischievous evil laugh"},
        {"name": "Indra", "hint": "King of the Devas, hurling the thunderbolt (Vajra), riding the multi-tusked white elephant Airavata"},
        {"name": "Goddess Saraswati", "hint": "Dressed in pure white, playing the celestial Veena, seated on a white swan"},
        {"name": "Goddess Lakshmi", "hint": "Bestower of wealth, standing on a pink lotus flower, showering golden coins from her palm"},
        {"name": "Parashurama", "hint": "Fierce warrior sage carrying an indestructible battle-axe (Parashu), vowed to rid the earth of corrupt rulers"},
        {"name": "Abhimanyu", "hint": "Brave young son of Arjuna, masterfully penetrating the Chakravyuha military formation"},
        {"name": "Surpanakha", "hint": "Ravana's sister whose nose was severed by Lakshmana after attempting to attack Sita"},
        {"name": "Yama", "hint": "God of justice and death, carrying a noose (Pasha), riding a dark water buffalo"},
        {"name": "Valmiki", "hint": "Robber turned revered sage, composed the epic Ramayana after anthills formed around his deep meditation"}
    ],
    "Leaders & Innovators 👑": [
        {"name": "Albert Einstein", "hint": "Sticky-out tongue photo, wild hair, E=mc²"},
        {"name": "APJ Abdul Kalam", "hint": "Missile Man of India, visionary scientist and President"},
        {"name": "Mahatma Gandhi", "hint": "Round spectacles, walking stick, leader of Ahimsa"},
        {"name": "Steve Jobs", "hint": "Black turtleneck, unveiled the original iPhone"},
        {"name": "Elon Musk", "hint": "Launches rockets to Mars, loves memes and Cybertrucks"},
        {"name": "Isaac Newton", "hint": "Apple fell on head, universal law of gravitation"},
        {"name": "Julius Caesar", "hint": "Roman laurel wreath, 'Et tu, Brute?'"},
        {"name": "Netaji Subhas Chandra Bose", "hint": "Military uniform and round spectacles, 'Give me blood and I will give you freedom', INA founder"},
        {"name": "Bhagat Singh", "hint": "Tilted fedora hat, twirled mustache, 'Inquilab Zindabad', fearlessly embraced martyrdom"},
        {"name": "Sardar Vallabhbhai Patel", "hint": "Iron Man of India, draped khadi shawl, unified 565 princely states, Statue of Unity"},
        {"name": "Dr. B.R. Ambedkar", "hint": "Father of the Indian Constitution, blue suit, holding the Constitution book, spectacles"},
        {"name": "Rani Lakshmibai", "hint": "Queen of Jhansi, infant tied to her back, riding a warhorse with swords drawn in both hands"},
        {"name": "Chhatrapati Shivaji Maharaj", "hint": "Maratha empire founder, crescent tilak, curved talwar, pioneer of guerrilla warfare"},
        {"name": "Swami Vivekananda", "hint": "Saffron turban and robe, folded arms pose, 'Sisters and brothers of America' Chicago address"},
        {"name": "Jawaharlal Nehru", "hint": "Red rose pinned to achkan jacket, Nehru cap, independent India's first Prime Minister"},
        {"name": "Rabindranath Tagore", "hint": "Flowing white beard and robe, Nobel Prize for Gitanjali, penned national anthems"},
        {"name": "Lal Bahadur Shastri", "hint": "Short stature, khadi topi, coined the rousing slogan 'Jai Jawan Jai Kisan'"},
        {"name": "Indira Gandhi", "hint": "Iron Lady of India, signature white streak in short hair, draped saree border over head"},
        {"name": "Atal Bihari Vajpayee", "hint": "Poet Prime Minister, iconic slow dramatic hand gestures, fiery parliamentary speeches"},
        {"name": "Mangal Pandey", "hint": "Sepoy mutiny pioneer of 1857, biting the Enfield rifle cartridge, fiery rebel gaze"},
        {"name": "Bal Gangadhar Tilak", "hint": "Pugree turban, thick white mustache, declared 'Swaraj is my birthright and I shall have it'"},
        {"name": "Ashoka the Great", "hint": "Maurya emperor, Ashoka Chakra lion capital, renounced warfare after the Kalinga war"},
        {"name": "Homi J. Bhabha", "hint": "Father of the Indian Nuclear Programme, founded TIFR, brilliant theoretical physicist"},
        {"name": "Vikram Sarabhai", "hint": "Father of the Indian Space Programme, visionary founder of ISRO"},
        {"name": "Sir C.V. Raman", "hint": "Traditional turban, Nobel laureate in Physics for discovering the Raman Scattering of light"},
        {"name": "Srinivasa Ramanujan", "hint": "Mathematical genius, infinite series and partition formulas, 'the man who knew infinity'"},
        {"name": "Jagadish Chandra Bose", "hint": "Invented crescograph to prove plants feel pain, pioneer of wireless radio waves"},
        {"name": "Ratan Tata", "hint": "Legendary visionary industrialist, philanthropic icon, created the affordable Nano car"},
        {"name": "J.R.D. Tata", "hint": "Father of Indian civil aviation, first licensed pilot of India, Tata empire builder"},
        {"name": "Dhirubhai Ambani", "hint": "Polyester yarn trader who built the Reliance empire, pioneering shareholder culture in India"},
        {"name": "Sundar Pichai", "hint": "Alphabet & Google CEO, IIT Kharagpur alumnus, keynote stage product announcements"},
        {"name": "Satya Nadella", "hint": "Microsoft CEO who transformed the tech giant into a cloud and AI powerhouse"},
        {"name": "Abraham Lincoln", "hint": "Tall top hat, chin-curtain beard, delivered the Gettysburg Address, abolished slavery"},
        {"name": "Nelson Mandela", "hint": "'Madiba', bright patterned shirts, 27 years imprisoned on Robben Island, anti-apartheid hero"},
        {"name": "Winston Churchill", "hint": "Chomping a cigar, flashing the 'V for Victory' sign, British wartime Prime Minister"},
        {"name": "Nikola Tesla", "hint": "Slick parted hair, wireless alternating current (AC) motor, holding glowing light bulbs"},
        {"name": "Marie Curie", "hint": "Two Nobel Prizes in Physics and Chemistry, pioneer of radioactivity, test tubes in lab coat"}
    ],
    "Pop & Internet Icons 🌟": [
        {"name": "Michael Jackson", "hint": "King of Pop, Moonwalk, fedora hat, 'Hee-hee!'"},
        {"name": "Taylor Swift", "hint": "Eras Tour sensation, heartbreaks with acoustic guitar"},
        {"name": "Freddie Mercury", "hint": "Live Aid 'Ay-Oh!', mic stand in clenched fist"},
        {"name": "MrBeast", "hint": "YouTube creator giving away millions in cash and challenges"},
        {"name": "Gordon Ramsay", "hint": "'It\\'s raw!', slam two slices of bread: idiot sandwich"},
        {"name": "Khaby Lame", "hint": "Silent reaction shrug with outstretched palms"},
        {"name": "A.R. Rahman", "hint": "Mozart of Madras, keyboard maestro, Oscars for 'Jai Ho', calm humble demeanor"},
        {"name": "Lata Mangeshkar", "hint": "Nightingale of India, pure white saree with border, legendary soulful high-pitch singing"},
        {"name": "Kishore Kumar", "hint": "Eccentric musical genius, yodeling maestro, comical expressions and stage antics"},
        {"name": "Arijit Singh", "hint": "Soulful heartbreak king, acoustic guitar, head turban/beanie, raw emotional vocals"},
        {"name": "Diljit Dosanjh", "hint": "Vibrant turban, 'Punjabi aa gaye oye!', high-energy concert roar and swagger"},
        {"name": "CarryMinati / Ajey Nagar", "hint": "'Toh kaise hain aap log?', fiery roaster, intense screaming gaming reactions"},
        {"name": "Bhuvan Bam / BB Ki Vines", "hint": "One-man comedy skits, playing Titu Mama and Bancho, front camera format"},
        {"name": "Zakir Khan", "hint": "'Sakht launda', sitting casually with mic, relatable storytelling and 'Badal pe paon hai'"},
        {"name": "Kapil Sharma", "hint": "King of Indian TV comedy, quick-witted punchlines, clapping hands laughing at guests"},
        {"name": "Honey Singh", "hint": "'Yo Yo Honey Singh', chunky gold chains, oversized sunglasses, pioneer of Desi hip-hop"},
        {"name": "Badshah", "hint": "'It's your boy Badshah!', oversized jackets, neon sunglasses, viral party hook steps"},
        {"name": "Sanjeev Kapoor", "hint": "'Khana Khazana' masterchef, white apron, sprinkle salt with iconic smile: 'Namak swaadanusaar'"},
        {"name": "Ranveer Brar", "hint": "Poetic masterchef, Lucknowi charm, slicing onions talking about food memories"},
        {"name": "Usha Uthup", "hint": "Kanjeevaram silk saree, large bindi, deep booming jazz/pop voice, 'Hari Om Hari'"},
        {"name": "Sonu Nigam", "hint": "Versatile singing maestro, effortless mimicry of other singers, live stage energy"},
        {"name": "Shreya Ghoshal", "hint": "Melody queen, sweet dimpled smile, effortless classical and romantic playback vocals"},
        {"name": "Mona Darling", "hint": "'Boss' villain sidekick, glamorous 70s Bollywood cabaret walk and exaggerated pose"},
        {"name": "Ashish Chanchlani", "hint": "Loud comedic skits, exaggerated hand movements, high-decibel youth humor"},
        {"name": "Samay Raina", "hint": "Chess streaming humor, edgy deadpan roasting, 'India's Got Latent' host"},
        {"name": "Tanmay Bhat", "hint": "AIB co-founder, infectious wheezing laugh, 'Bot army' YouTube reaction vlogs"}
    ],
    "Cartoon Characters" : [
        {"name": "Chhota Bheem", "hint": "Orange dhoti, eating heaps of laddoos for instant super strength, Dholakpur hero"},
        {"name": "Kalia Ustad", "hint": "Fat bully of Dholakpur, always accompanied by Dholu-Bholu, jealous of Bheem"},
        {"name": "Chacha Chaudhary", "hint": "Red turban, walking stick, wooden waistcoat, 'brain works faster than a computer'"},
        {"name": "Sabu", "hint": "Giant alien from Jupiter, trusted companion of Chacha Chaudhary, 'when he gets angry a volcano erupts'"},
        {"name": "Shaktimaan (Animated)", "hint": "Red and gold suit with chest chakra, spinning into a whirlwind while saying 'Sorry Shaktimaan'"},
        {"name": "Motu", "hint": "Loves eating hot samosas to gain bursts of energy, best buddy of Patlu"},
        {"name": "Patlu", "hint": "Bald with glasses and yellow kurta, 'Idea!' lightbulb popping over his head"},
        {"name": "John the Don", "hint": "Rhyming villain in Motu Patlu, short height with henchmen, 'John banega Don'"},
        {"name": "Roll No 21 / Kanishk", "hint": "Principal of Mathura Anath Ashram, secretly demon king Kamsa scheming against Kris"},
        {"name": "Kris (Roll No 21)", "hint": "Blue-skinned boy with peacock feather hairstyle, plays flute and performs miracles"},
        {"name": "Bantul the Great", "hint": "Narayan Debnath's superhero, pink vest and black shorts, bullets bounce off his bare chest"},
        {"name": "Handa Bhonda", "hint": "Bengali comic duo, skinny mischievous prankster and his stout gullible companion"},
        {"name": "Nante Fante", "hint": "Boarding school prankster duo, outsmarting strict hostel superintendent Keltuda"},
        {"name": "Shinchan / Shinnosuke Nohara", "hint": "Thick eyebrows, funny 'Buri Buri' dance, flirting with older girls and embarrassing his mom"},
        {"name": "Doraemon", "hint": "Blue robotic earless cat from the future, magic 4D pocket, obsessed with Doracakes"},
        {"name": "Nobita Nobi", "hint": "Round spectacles, yellow shirt, clumsy, cries and begs Doraemon for gadgets"},
        {"name": "Gian / Takeshi Goda", "hint": "Neighborhood bully, terrible singer who forces friends to attend his horrible concerts"},
        {"name": "Suneo Honekawa", "hint": "Fox-faced rich kid, bragging about expensive imported toys, sucking up to Gian"},
        {"name": "Hattori Hanzo (Ninja Hattori)", "hint": "Blue ninja suit, round spiral cheeks, throws shurikens, signature 'Ding Ding!' catchphrase"},
        {"name": "Kemumaki (Ninja Hattori)", "hint": "Sneaky rival Koga ninja, disguised as school kid, paired with black cat Kagechiyo"},
        {"name": "Shishimaru", "hint": "Ninja Hattori's chubby yellow dog who loves chocolate rolls and turns into a ball"},
        {"name": "Perman / Mitsuo Suwa", "hint": "Blue helmet, flying cape giving 119 km/h speed, chest badge communicator"},
        {"name": "Bo-chan (Shinchan)", "hint": "Always has a single droplet of mucus hanging from his nose, stone collector, quiet genius"},
        {"name": "Action Kamen", "hint": "Shinchan's favorite superhero, shoots Action Beam from crossed wrists with a booming laugh"},
        {"name": "Son Goku", "hint": "Orange martial arts gi, spiky hair turning golden Super Saiyan, 'Kamehameha!' charge pose"},
        {"name": "Vegeta", "hint": "Proud Saiyan prince, crossed arms, widow's peak hair, shouting 'It's over 9000!'"},
        {"name": "Naruto Uzumaki", "hint": "Orange jumpsuit, whisker marks on cheeks, 'Dattebayo!', Shadow Clone jutsu and Rasengan"},
        {"name": "Pikachu", "hint": "Yellow electric mouse, red rosy cheeks, lightning-bolt tail, crying 'Pika-Pika-Chuuu!'"},
        {"name": "Ash Ketchum", "hint": "Turned-back baseball cap, throwing a Pokéball shouting 'I choose you!'"},
        {"name": "Monkey D. Luffy", "hint": "Straw hat, red vest, stretchy rubber limbs, shouting 'I'm gonna be King of the Pirates!'"},
        {"name": "Tom", "hint": "Gray cat running into walls, setting mousetraps that backfire, letting out painful shrieks"},
        {"name": "Jerry", "hint": "Tiny clever brown mouse, stealing cheese triangles and outsmarting the house cat"},
        {"name": "Ben 10 / Ben Tennyson", "hint": "Slapping down dial on wrist watch Omnitrix to transform into alien heroes"},
        {"name": "Gwen Tennyson", "hint": "Ben's cousin, red hair, casting pink-magenta mana magic shields and energy blasts"},
        {"name": "Kevin 11", "hint": "Absorbing matter like steel, stone, and wood by touching surfaces with bare hands"},
        {"name": "Courage the Cowardly Dog", "hint": "Timid pink dog who screams with eyes popping out to save Muriel from monsters"},
        {"name": "Eustace Bagge", "hint": "Grumpy farmer with round glasses and cap, scaring Courage shouting 'Ooga Booga Booga!'"},
        {"name": "Dexter", "hint": "Boy genius with thick orange hair, glasses, white lab coat and purple gloves in a secret lab"},
        {"name": "Dee Dee", "hint": "Tall blonde sister in ballerina tutu, pressing forbidden lab buttons: 'Ooh, what does this button do?'"},
        {"name": "Johnny Bravo", "hint": "Huge pompadour blonde hair, sunglasses, flexing biceps shouting 'Whoa, mama!'"},
        {"name": "Powerpuff Girls / Blossom", "hint": "Leader of the trio, big red bow on head, pink dress, eye laser beams"},
        {"name": "Mojo Jojo", "hint": "Super-intelligent chimpanzee villain with an oversized exposed brain helmet and long cape"},
        {"name": "Samurai Jack", "hint": "White kimono, magical katana sword, stoic time-traveling warrior fighting Aku"},
        {"name": "Scooby-Doo", "hint": "Cowardly Great Dane dog, shaking with fear, running for Scooby Snacks, 'Scooby-Dooby-Doo!'"},
        {"name": "Shaggy Rogers", "hint": "Green V-neck shirt, scruffy goatee, eating towering giant sandwiches while running from ghosts"},
        {"name": "Fred Flintstone", "hint": "Caveman in orange tunic, bowling with bare feet, yelling 'Yabba-Dabba-Doo!'"},
        {"name": "Popeye the Sailor", "hint": "Corncob pipe, anchor forearm tattoos, squeezing open a can of spinach for instant muscle"},
        {"name": "Bluto / Brutus", "hint": "Bearded muscular sailor bully, constantly picking fights with Popeye over Olive Oyl"},
        {"name": "Oswald the Lucky Rabbit / Oswald the Octopus", "hint": "Gentle blue octopus wearing a bowler hat, walking his hotdog dog Weenie"},
        {"name": "Bob the Builder", "hint": "Yellow hard hat, checkered shirt, tool belt, shouting 'Can we fix it? Yes we can!'"},
        {"name": "SpongeBob SquarePants", "hint": "Yellow sea sponge in square brown trousers, flipping Krabby Patties, high-pitch laugh"},
        {"name": "Patrick Star", "hint": "Pink chubby starfish in green-and-purple floral shorts, delightfully clueless best friend"},
        {"name": "Squidward Tentacles", "hint": "Grumpy turquoise octopus, playing screechy clarinet, hates cheerful neighbors"},
        {"name": "Mickey Mouse", "hint": "Round black mouse ears, red shorts with white buttons, yellow shoes, cheerful whistle"},
        {"name": "Donald Duck", "hint": "Sailor shirt and cap, completely incomprehensible quacking rage fits when annoyed"},
        {"name": "Goofy", "hint": "Tall clumsy hound dog in tall green fedora and vest, signature 'Ahyuck!' chuckle and holler"},
        {"name": "Po (Kung Fu Panda)", "hint": "Chubby giant panda, loves steamed dumplings, master of the 'Wuxi Finger Hold' (Skadoosh!)"},
        {"name": "Shrek", "hint": "Green ogre with trumpet ears, living in a muddy swamp, roaring to scare villagers"},
        {"name": "Donkey (Shrek)", "hint": "Chatterbox grey donkey, singing annoying pop songs, obsessed with morning waffles"},
        {"name": "Simba (The Lion King)", "hint": "Lion cub raised on Pride Rock, roaring atop the cliff, living by 'Hakuna Matata'"}
    ]
}

# --- State Initialization ---
def init_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = "user_" + str(int(time.time() * 1000)) + "_" + str(random.randint(100, 999))
    if "game_stage" not in st.session_state:
        st.session_state.game_stage = "home"
    if "game_mode" not in st.session_state:
        st.session_state.game_mode = "pass_play"  # 'pass_play' or 'online_room'
    if "room_code" not in st.session_state:
        st.session_state.room_code = ""
    if "player_name" not in st.session_state:
        st.session_state.player_name = "Player"
    if "local_players" not in st.session_state:
        st.session_state.local_players = ["Player 1", "Player 2", "Player 3"]
    if "local_scores" not in st.session_state:
        st.session_state.local_scores = {p: 0 for p in st.session_state.local_players}
    if "total_rounds" not in st.session_state:
        st.session_state.total_rounds = 3
    if "current_round" not in st.session_state:
        st.session_state.current_round = 1
    if "current_player_idx" not in st.session_state:
        st.session_state.current_player_idx = 0
    if "selected_categories" not in st.session_state:
        st.session_state.selected_categories = list(MASTER_DECKS.keys())
    if "custom_cards" not in st.session_state:
        st.session_state.custom_cards = []
    if "deck" not in st.session_state:
        st.session_state.deck = []
    if "current_card" not in st.session_state:
        st.session_state.current_card = None
    if "round_history" not in st.session_state:
        st.session_state.round_history = []
    if "scoring" not in st.session_state:
        st.session_state.scoring = {
            "actor_correct": 10,
            "guesser_correct": 5,
            "actor_fail": 3,
            "guesser_fail": 3
        }

init_state()

# --- Helper Functions ---
def build_deck(selected_cats, custom_cards):
    cards = []
    for cat in selected_cats:
        if cat in MASTER_DECKS:
            for c in MASTER_DECKS[cat]:
                cards.append({**c, "category": cat})
    for custom in custom_cards:
        cards.append({"name": custom["name"], "hint": custom.get("hint", "Custom Card"), "category": "Custom Deck ✨"})
    random.shuffle(cards)
    if not cards:
        cards = [{**c, "category": "Sports Legends ⚽"} for c in MASTER_DECKS["Sports Legends ⚽"]]
        random.shuffle(cards)
    return cards

def create_shared_room(code, host_id, host_name, rounds, scoring, categories, custom_cards):
    GLOBAL_ROOMS[code] = {
        "host_id": host_id,
        "state": "lobby",  # 'lobby', 'acting', 'round_summary', 'game_over'
        "rounds_total": rounds,
        "round_current": 1,
        "player_idx": 0,
        "scoring": scoring,
        "categories": categories,
        "custom_cards": custom_cards,
        "deck": build_deck(categories, custom_cards),
        "current_card": None,
        "players": [{"id": host_id, "name": host_name}],
        "scores": {host_id: 0},
        "history": [],
        "last_update": time.time()
    }

def draw_room_card(room):
    if not room["deck"]:
        room["deck"] = build_deck(room["categories"], room["custom_cards"])
    room["current_card"] = room["deck"].pop()

# --- Auto Sync Polling for Online Multiplayer ---
if st.session_state.game_mode == "online_room" and st.session_state.room_code in GLOBAL_ROOMS:
    # Refresh every 1.5 seconds to sync actions across different phones/computers
    st_autorefresh(interval=1500, key="multiplayer_sync")

# --- Sidebar Controls ---
with st.sidebar:
    st.title("🎭 Game Controls")
    
    if st.session_state.game_mode == "online_room" and st.session_state.room_code in GLOBAL_ROOMS:
        room = GLOBAL_ROOMS[st.session_state.room_code]
        st.success(f"📡 Connected to Room: **{st.session_state.room_code}**")
        st.info(
            f"**Marks Scheme:**\n"
            f"- Actor Correct: **+{room['scoring']['actor_correct']}**\n"
            f"- Guessers Correct: **+{room['scoring']['guesser_correct']}**\n"
            f"- Actor Failed: **-{room['scoring']['actor_fail']}**\n"
            f"- Guessers Failed: **-{room['scoring']['guesser_fail']}**"
        )
        st.subheader("📊 Live Room Scores")
        sorted_sc = sorted(room["players"], key=lambda p: room["scores"].get(p["id"], 0), reverse=True)
        actor_id = room["players"][room["player_idx"]]["id"] if room["players"] and room["state"] == "acting" else None
        
        for rank, p in enumerate(sorted_sc, 1):
            sc = room["scores"].get(p["id"], 0)
            is_actor = " 🎭 (Acting)" if p["id"] == actor_id else ""
            is_you = " ⭐ (You)" if p["id"] == st.session_state.user_id else ""
            color = "green" if sc >= 0 else "red"
            st.markdown(f"**#{rank} {p['name']}{is_you}{is_actor}**: :{color}[{sc} pts]")
    else:
        st.info(
            f"**Marks Scheme:**\n"
            f"- Actor Correct: **+{st.session_state.scoring['actor_correct']}**\n"
            f"- Guessers Correct: **+{st.session_state.scoring['guesser_correct']}**\n"
            f"- Actor Failed: **-{st.session_state.scoring['actor_fail']}**\n"
            f"- Guessers Failed: **-{st.session_state.scoring['guesser_fail']}**"
        )

    st.divider()
    if st.button("🚪 Exit to Main Menu", use_container_width=True):
        st.session_state.game_stage = "home"
        st.session_state.game_mode = "pass_play"
        st.session_state.room_code = ""
        st.rerun()

# ==========================================
# 1. SCREEN: HOME
# ==========================================
if st.session_state.game_stage == "home":
    st.markdown("<h1 style='text-align: center;'>🎭 Guess the Person</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Act. Guess. Score Big with Friends across devices!</p>", unsafe_allow_html=True)
    st.write("---")

    with st.container(border=True):
        st.subheader("📱 Pass & Play (Single Device)")
        st.write("Pass one phone around the room with a privacy shield.")
        if st.button("Start Pass & Play", type="primary", use_container_width=True):
            st.session_state.game_mode = "pass_play"
            st.session_state.game_stage = "setup"
            st.rerun()

    with st.container(border=True):
        st.subheader("📡 Create Online Room (Multi-Device)")
        st.write("Host a real-time room. Friends on other phones or laptops can join via room code!")
        if st.button("Host Online Room", use_container_width=True):
            st.session_state.game_mode = "online_room"
            chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
            st.session_state.room_code = "".join(random.choices(chars, k=5))
            st.session_state.game_stage = "setup"
            st.rerun()

    with st.container(border=True):
        st.subheader("🔍 Search / Join Room")
        st.write("Have a room code from a friend? Enter your nickname and join immediately.")
        if st.button("Join Room", use_container_width=True):
            st.session_state.game_mode = "online_room"
            st.session_state.game_stage = "search_room"
            st.rerun()

# ==========================================
# 2. SCREEN: SEARCH ROOM (JOIN ONLINE)
# ==========================================
elif st.session_state.game_stage == "search_room":
    st.subheader("🔍 Join an Online Room")
    with st.container(border=True):
        name_input = st.text_input("Your Player Nickname", value="Alex", max_chars=15)
        code_input = st.text_input("5-Letter Room Code", max_chars=5, placeholder="e.g. ACT88").strip().upper()
        
        col_back, col_join = st.columns(2)
        with col_back:
            if st.button("⬅️ Back to Menu", use_container_width=True):
                st.session_state.game_stage = "home"
                st.rerun()
        with col_join:
            if st.button("Connect & Join", type="primary", use_container_width=True):
                if not name_input.strip():
                    st.error("Please enter a nickname.")
                elif code_input not in GLOBAL_ROOMS:
                    st.error(f"Room '{code_input}' not found. Please double-check with the host!")
                else:
                    st.session_state.player_name = name_input.strip()
                    st.session_state.room_code = code_input
                    st.session_state.game_mode = "online_room"
                    
                    room = GLOBAL_ROOMS[code_input]
                    existing_p = [p for p in room["players"] if p["id"] == st.session_state.user_id]
                    if not existing_p:
                        room["players"].append({"id": st.session_state.user_id, "name": st.session_state.player_name})
                        room["scores"][st.session_state.user_id] = 0
                        room["last_update"] = time.time()
                    
                    st.session_state.game_stage = "online_lobby"
                    st.rerun()

# ==========================================
# 3. SCREEN: SETUP (PASS & PLAY OR HOST ROOM)
# ==========================================
elif st.session_state.game_stage == "setup":
    is_online = (st.session_state.game_mode == "online_room")
    
    if is_online:
        st.subheader(f"📡 Setting up Room: `{st.session_state.room_code}`")
        host_name = st.text_input("Your Host Nickname", value="Host", max_chars=15)
        st.session_state.player_name = host_name
    else:
        st.subheader("📱 Pass & Play Setup")

    with st.container(border=True):
        st.markdown("### 🧮 Custom Marks Scheme")
        p_cols = st.columns(3)
        with p_cols[0]:
            if st.button("Standard (+10/+5, -3/-3)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 10, "guesser_correct": 5, "actor_fail": 3, "guesser_fail": 3}
                st.rerun()
        with p_cols[1]:
            if st.button("High Stakes (+5/+3, -3/-5)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 5, "guesser_correct": 3, "actor_fail": 3, "guesser_fail": 5}
                st.rerun()
        with p_cols[2]:
            if st.button("No Penalty (0 on fail)", use_container_width=True):
                st.session_state.scoring = {"actor_correct": 10, "guesser_correct": 5, "actor_fail": 0, "guesser_fail": 0}
                st.rerun()

        sc1, sc2 = st.columns(2)
        with sc1:
            st.session_state.scoring["actor_correct"] = st.number_input("Actor Correct (+pts)", 0, 50, st.session_state.scoring["actor_correct"])
            st.session_state.scoring["actor_fail"] = st.number_input("Actor Failed (-pts)", 0, 50, st.session_state.scoring["actor_fail"])
        with sc2:
            st.session_state.scoring["guesser_correct"] = st.number_input("Guessers Correct (+pts)", 0, 50, st.session_state.scoring["guesser_correct"])
            st.session_state.scoring["guesser_fail"] = st.number_input("Guessers Failed (-pts)", 0, 50, st.session_state.scoring["guesser_fail"])

    with st.container(border=True):
        st.markdown("### 🔄 Number of Rounds")
        r_options = [1, 3, 5, 10, 15, 20, "Unlimited"]
        st.session_state.total_rounds = st.radio("Total rounds:", r_options, index=1, horizontal=True)

    with st.container(border=True):
        st.markdown("### 🎴 Categories")
        st.session_state.selected_categories = st.multiselect(
            "Select Decks",
            options=list(MASTER_DECKS.keys()),
            default=list(MASTER_DECKS.keys())
        )
        custom_p = st.text_input("Add Custom Personality / Inside Joke", max_chars=30)
        if st.button("➕ Add Custom") and custom_p.strip():
            st.session_state.custom_cards.append({"name": custom_p.strip(), "hint": "Custom party addition"})
            st.success(f"Added {custom_p.strip()}")

    if not is_online:
        with st.container(border=True):
            st.markdown("### 👥 Player Turn Order")
            for i, p in enumerate(st.session_state.local_players):
                c_name, c_del = st.columns([4, 1])
                with c_name:
                    st.write(f"**{i+1}.** {p}")
                with c_del:
                    if len(st.session_state.local_players) > 2 and st.button("❌", key=f"del_loc_{i}"):
                        st.session_state.local_players.pop(i)
                        st.rerun()
            new_p = st.text_input("Add Player", max_chars=20)
            if st.button("➕ Add Player") and new_p.strip() and new_p.strip() not in st.session_state.local_players:
                st.session_state.local_players.append(new_p.strip())
                st.rerun()

    c_back, c_start = st.columns(2)
    with c_back:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.game_stage = "home"
            st.rerun()
    with c_start:
        start_txt = "Open Lobby & Wait for Players" if is_online else "🚀 Start Match"
        if st.button(start_txt, type="primary", use_container_width=True):
            if is_online:
                create_shared_room(
                    st.session_state.room_code,
                    st.session_state.user_id,
                    st.session_state.player_name,
                    st.session_state.total_rounds,
                    st.session_state.scoring,
                    st.session_state.selected_categories,
                    st.session_state.custom_cards
                )
                st.session_state.game_stage = "online_lobby"
                st.rerun()
            else:
                st.session_state.local_scores = {p: 0 for p in st.session_state.local_players}
                st.session_state.current_round = 1
                st.session_state.current_player_idx = 0
                st.session_state.deck = build_deck(st.session_state.selected_categories, st.session_state.custom_cards)
                st.session_state.current_card = st.session_state.deck.pop()
                st.session_state.round_history = []
                st.session_state.game_stage = "turn_shield"
                st.rerun()

# ==========================================
# 4. SCREEN: ONLINE LOBBY
# ==========================================
elif st.session_state.game_stage == "online_lobby":
    code = st.session_state.room_code
    if code not in GLOBAL_ROOMS:
        st.error("Room closed or expired.")
        st.session_state.game_stage = "home"
        st.rerun()

    room = GLOBAL_ROOMS[code]
    is_host = (room["host_id"] == st.session_state.user_id)

    # If match already started by host, automatically jump in!
    if room["state"] in ["acting", "round_summary", "game_over"]:
        st.session_state.game_stage = "online_gameplay"
        st.rerun()

    st.markdown(f"<h2 style='text-align:center;'>Room: <span style='color:#38BDF8; font-family:monospace;'>{code}</span></h2>", unsafe_allow_html=True)
    st.info("Share this 5-letter Room Code with your friends! They can open this app, tap **Search Room**, and join instantly from their phones.")

    with st.container(border=True):
        st.markdown(f"### 👥 Connected Players ({len(room['players'])})")
        for idx, p in enumerate(room["players"], 1):
            h_tag = " 👑 (Host)" if p["id"] == room["host_id"] else ""
            you_tag = " ⭐ (You)" if p["id"] == st.session_state.user_id else ""
            st.write(f"**{idx}.** {p['name']}{h_tag}{you_tag}")

    if is_host:
        if len(room["players"]) < 2:
            st.warning("Waiting for at least 1 more player to join before starting...")
        else:
            if st.button("🚀 Start Match for Everyone", type="primary", use_container_width=True):
                room["state"] = "acting"
                room["round_current"] = 1
                room["player_idx"] = 0
                draw_room_card(room)
                room["last_update"] = time.time()
                st.session_state.game_stage = "online_gameplay"
                st.rerun()
    else:
        st.info("⏳ Waiting for the Host to start the game...")

# ==========================================
# 5. SCREEN: ONLINE GAMEPLAY (REAL-TIME SYNCED)
# ==========================================
elif st.session_state.game_stage == "online_gameplay":
    code = st.session_state.room_code
    if code not in GLOBAL_ROOMS:
        st.error("Room closed.")
        st.session_state.game_stage = "home"
        st.rerun()

    room = GLOBAL_ROOMS[code]
    
    # State A: Acting Turn
    if room["state"] == "acting":
        actor = room["players"][room["player_idx"]]
        is_actor = (actor["id"] == st.session_state.user_id)
        card = room["current_card"]
        r_disp = f"Round {room['round_current']}" if room["rounds_total"] == "Unlimited" else f"Round {room['round_current']} of {room['rounds_total']}"

        st.markdown(f"<div style='text-align:center; font-weight:bold; color:#A78BFA;'>{r_disp} &bull; Turn {room['player_idx'] + 1} of {len(room['players'])}</div>", unsafe_allow_html=True)

        if is_actor:
            st.success("🎭 **IT'S YOUR TURN TO ACT!**")
            with st.container(border=True):
                st.caption(f"Category: {card['category']}")
                st.markdown(f"<h1 style='text-align: center; color: #38BDF8;'>{card['name']}</h1>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray;'><em>Clue: {card['hint']}</em></p>", unsafe_allow_html=True)
                st.caption("No speaking or mouthing words! Act it out silently.")

            col_fail, col_succ = st.columns(2)
            with col_fail:
                if st.button(f"❌ Failed (-{room['scoring']['actor_fail']}/-{room['scoring']['guesser_fail']})", use_container_width=True):
                    # Record fail
                    for p in room["players"]:
                        if p["id"] == actor["id"]:
                            room["scores"][p["id"]] -= abs(room["scoring"]["actor_fail"])
                        else:
                            room["scores"][p["id"]] -= abs(room["scoring"]["guesser_fail"])
                    room["history"].append({
                        "round": room["round_current"],
                        "actor": actor["name"],
                        "person": card["name"],
                        "success": False
                    })
                    room["player_idx"] += 1
                    if room["player_idx"] >= len(room["players"]):
                        room["state"] = "round_summary"
                    else:
                        draw_room_card(room)
                    room["last_update"] = time.time()
                    st.rerun()

            with col_succ:
                if st.button(f"✅ Got It! (+{room['scoring']['actor_correct']}/+{room['scoring']['guesser_correct']})", type="primary", use_container_width=True):
                    for p in room["players"]:
                        if p["id"] == actor["id"]:
                            room["scores"][p["id"]] += room["scoring"]["actor_correct"]
                        else:
                            room["scores"][p["id"]] += room["scoring"]["guesser_correct"]
                    room["history"].append({
                        "round": room["round_current"],
                        "actor": actor["name"],
                        "person": card["name"],
                        "success": True
                    })
                    room["player_idx"] += 1
                    if room["player_idx"] >= len(room["players"]):
                        room["state"] = "round_summary"
                    else:
                        draw_room_card(room)
                    room["last_update"] = time.time()
                    st.rerun()
        else:
            st.info(f"👀 **Guessing Mode:** Watch **{actor['name']}** act!")
            with st.container(border=True):
                st.markdown(f"<h3 style='text-align: center;'>Actor: <span style='color: #EC4899;'>{actor['name']}</span></h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray;'>Category: <strong>{card['category']}</strong></p>", unsafe_allow_html=True)
                st.write("Shout your guesses out loud to the actor! When someone gets it right, the actor will submit the score.")

    # State B: Round Summary
    elif room["state"] == "round_summary":
        st.balloons()
        st.markdown(f"<h2 style='text-align: center;'>🎉 Round {room['round_current']} Complete!</h2>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("### 🏆 Leaderboard")
            sorted_p = sorted(room["players"], key=lambda p: room["scores"].get(p["id"], 0), reverse=True)
            for rank, p in enumerate(sorted_p, 1):
                trophy = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
                sc = room["scores"].get(p["id"], 0)
                color = "green" if sc >= 0 else "red"
                st.markdown(f"{trophy} **{p['name']}** — :{color}[**{sc} pts**]")

        with st.expander("📜 Round History", expanded=True):
            curr_recap = [h for h in room["history"] if h["round"] == room["round_current"]]
            for h in curr_recap:
                st.write(f"{'✅' if h['success'] else '❌'} **{h['actor']}** acted *\"{h['person']}\"*")

        is_host = (room["host_id"] == st.session_state.user_id)
        is_final = (room["rounds_total"] != "Unlimited" and room["round_current"] >= int(room["rounds_total"]))

        if is_host:
            c1, c2 = st.columns(2)
            with c1:
                btn_lbl = "🏆 Crown Final Champions" if is_final else f"Start Round {room['round_current'] + 1} ➡️"
                if st.button(btn_lbl, type="primary", use_container_width=True):
                    if is_final:
                        room["state"] = "game_over"
                    else:
                        room["round_current"] += 1
                        room["player_idx"] = 0
                        room["state"] = "acting"
                        draw_room_card(room)
                    room["last_update"] = time.time()
                    st.rerun()
            with c2:
                if not is_final and st.button("🏁 End Match Now", use_container_width=True):
                    room["state"] = "game_over"
                    room["last_update"] = time.time()
                    st.rerun()
        else:
            st.info("⏳ Waiting for host to advance to the next round...")

    # State C: Final Game Over
    elif room["state"] == "game_over":
        st.balloons()
        sorted_p = sorted(room["players"], key=lambda p: room["scores"].get(p["id"], 0), reverse=True)
        winner = sorted_p[0]
        
        st.markdown("<h1 style='text-align: center;'>👑 Match Over!</h1>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center; color: #F59E0B;'>🏆 Champion: {winner['name']}</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 22px; font-weight: bold;'>Score: {room['scores'].get(winner['id'], 0)} Points</p>", unsafe_allow_html=True)

        if room["host_id"] == st.session_state.user_id:
            if st.button("🔄 Play Again with Same Room", type="primary", use_container_width=True):
                room["round_current"] = 1
                room["player_idx"] = 0
                for p in room["players"]:
                    room["scores"][p["id"]] = 0
                room["history"] = []
                room["deck"] = build_deck(room["categories"], room["custom_cards"])
                draw_room_card(room)
                room["state"] = "acting"
                room["last_update"] = time.time()
                st.rerun()

# ==========================================
# 6. PASS & PLAY LOCAL GAMEPLAY
# ==========================================
elif st.session_state.game_stage == "turn_shield":
    actor = st.session_state.local_players[st.session_state.current_player_idx]
    round_disp = f"Round {st.session_state.current_round}" if st.session_state.total_rounds == "Unlimited" else f"Round {st.session_state.current_round} of {st.session_state.total_rounds}"
    
    st.markdown(f"<h3 style='text-align: center;'>{round_disp}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: gray;'>Turn {st.session_state.current_player_idx + 1} of {len(st.session_state.local_players)}</p>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<h2 style='text-align: center;'>🙈 Privacy Shield</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #EC4899;'>Pass device to: {actor}</h3>", unsafe_allow_html=True)
        st.write("Other players look away!")
        if st.button("👁️ Reveal Card & Act", type="primary", use_container_width=True):
            st.session_state.game_stage = "turn_active"
            st.rerun()

elif st.session_state.game_stage == "turn_active":
    actor = st.session_state.local_players[st.session_state.current_player_idx]
    card = st.session_state.current_card
    
    st.markdown(f"**Acting Now:** 🎭 **{actor}**")
    with st.container(border=True):
        st.caption(f"Category: {card['category']}")
        st.markdown(f"<h1 style='text-align: center; color: #38BDF8;'>{card['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'><em>Clue: {card['hint']}</em></p>", unsafe_allow_html=True)

    col_fail, col_success = st.columns(2)
    with col_fail:
        if st.button(f"❌ Failed (-{st.session_state.scoring['actor_fail']}/-{st.session_state.scoring['guesser_fail']})", use_container_width=True):
            for p in st.session_state.local_players:
                if p == actor:
                    st.session_state.local_scores[p] -= abs(st.session_state.scoring["actor_fail"])
                else:
                    st.session_state.local_scores[p] -= abs(st.session_state.scoring["guesser_fail"])
            st.session_state.current_player_idx += 1
            if st.session_state.current_player_idx >= len(st.session_state.local_players):
                st.session_state.game_stage = "round_summary"
            else:
                st.session_state.current_card = st.session_state.deck.pop() if st.session_state.deck else build_deck(st.session_state.selected_categories, st.session_state.custom_cards).pop()
                st.session_state.game_stage = "turn_shield"
            st.rerun()

    with col_success:
        if st.button(f"✅ Got It! (+{st.session_state.scoring['actor_correct']}/+{st.session_state.scoring['guesser_correct']})", type="primary", use_container_width=True):
            for p in st.session_state.local_players:
                if p == actor:
                    st.session_state.local_scores[p] += st.session_state.scoring["actor_correct"]
                else:
                    st.session_state.local_scores[p] += st.session_state.scoring["guesser_correct"]
            st.session_state.current_player_idx += 1
            if st.session_state.current_player_idx >= len(st.session_state.local_players):
                st.session_state.game_stage = "round_summary"
            else:
                st.session_state.current_card = st.session_state.deck.pop() if st.session_state.deck else build_deck(st.session_state.selected_categories, st.session_state.custom_cards).pop()
                st.session_state.game_stage = "turn_shield"
            st.rerun()

elif st.session_state.game_stage == "round_summary":
    st.balloons()
    st.markdown(f"<h2 style='text-align: center;'>🎉 Round {st.session_state.current_round} Complete!</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 🏆 Leaderboard")
        sorted_sc = sorted(st.session_state.local_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_sc, 1):
            trophy = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
            color = "green" if score >= 0 else "red"
            st.markdown(f"{trophy} **{player}** — :{color}[**{score} pts**]")

    is_final = (st.session_state.total_rounds != "Unlimited" and st.session_state.current_round >= int(st.session_state.total_rounds))
    c1, c2 = st.columns(2)
    with c1:
        lbl = "🏆 View Final Winners" if is_final else f"Start Round {st.session_state.current_round + 1} ➡️"
        if st.button(lbl, type="primary", use_container_width=True):
            if is_final:
                st.session_state.game_stage = "game_over"
            else:
                st.session_state.current_round += 1
                st.session_state.current_player_idx = 0
                st.session_state.current_card = st.session_state.deck.pop() if st.session_state.deck else build_deck(st.session_state.selected_categories, st.session_state.custom_cards).pop()
                st.session_state.game_stage = "turn_shield"
            st.rerun()
    with c2:
        if not is_final and st.button("🏁 End Match Now", use_container_width=True):
            st.session_state.game_stage = "game_over"
            st.rerun()

elif st.session_state.game_stage == "game_over":
    st.balloons()
    sorted_sc = sorted(st.session_state.local_scores.items(), key=lambda x: x[1], reverse=True)
    w_name, w_score = sorted_sc[0]
    st.markdown("<h1 style='text-align: center;'>👑 Match Over!</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center; color: #F59E0B;'>🏆 Winner: {w_name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-size: 22px; font-weight: bold;'>Score: {w_score} Points</p>", unsafe_allow_html=True)
    if st.button("🔄 Play Again", type="primary", use_container_width=True):
        st.session_state.local_scores = {p: 0 for p in st.session_state.local_players}
        st.session_state.current_round = 1
        st.session_state.current_player_idx = 0
        st.session_state.deck = build_deck(st.session_state.selected_categories, st.session_state.custom_cards)
        st.session_state.current_card = st.session_state.deck.pop()
        st.session_state.game_stage = "turn_shield"
        st.rerun()
