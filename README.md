

## How to contribute (Teach AnimalFactsBot a new animal):

Check the open issues to claim a listed animal, or come up with your own. Be sure to also check currently open pull requests to make sure you don't duplicate someone else's work.

Due to Hacktoberfests pull requests are coming in fast! Comment on an issue you are going to work on - and also check open pull requests before you do work someone else has already done.

Steps:
* Fork/clone the repo.
* Add a tuple of strings of facts (to animalfacts.py) pertaining to a particular animal. Name the tuple variable following the format 'NAMEOFANIMAL_FACTS'. Put the tuple in alphabetical order with the other tuples. Make sure your lines are indented by 4 spaces and please use ' for your strings.
* Add your tuple to the ALL_FACTS tuple.
* Add a line to the check_comment_for_animal() function for your animal following the format.
* Add your animal to the Readme in alphabetical order.
* Add me on Twitter @joelatwar

Please:
* Don't add a very small set of facts (this will cause the bot to be repetitive regarding your animal).
* Each fact must make sense independent of the other facts in the tuple because users will only get one fact at a time.
* Only add TRUE facts. Please no trolling with 'alternative facts'.
* Don't add 'seal', 'bat' or 'duck' facts unless you've figured out how to not reply to homonyms.
* Don't add 'cat' or 'dog' because they are just too common on reddit.

If you have a question the quickest way to reach is me on twitter @joelatwar


# animal-facts-bot

Animal-facts-bot is a Reddit bot that searches for comments on reddit that contain the name of the animal and then replies to the comment with a fact about that animal.

You can see the bot in action at https://www.reddit.com/user/AnimalFactsBot/comments/

### Current supported animals:

* Aardvark
* Albatross
* Alligator
* Alpaca
* Anaconda
* Anglerfish
* Ant
* Anteater
* Antelope
* Armadillo
* Atlantic puffin
* Badger
* Bear
* Beaver
* Bison
* Bobcat
* Buffalo
* Camel
* Capybara
* Chameleon
* Cheetah
* Chimpanzee
* Chinchilla
* Chipmunk
* Clownfish
* Cobra
* Cougar
* Cow
* Crab
* Crane
* Crayfish
* Crocodile
* Cuttlefish
* Deer
* Degu
* Dingo
* Dodo
* Dolphin
* Dugong
* Eagle
* Earthworm
* Echidna
* Eland
* Elephant
* Elephant shrew
* Elk
* Emu
* Falcon
* Flamingo
* Fox
* Fire salamander
* Frog
* Gazelle
* Gecko
* Giraffe
* Goat
* Goose
* Gopher
* Gorilla
* Grasshopper
* Hamster
* Hedgehog
* Hippo
* Honeybee
* Honey badger
* Horse
* House fly
* Hummingbird
* Husky
* Iguana
* Jackal
* Jellyfish
* Jerboa
* Kangaroo
* Kiwi
* Koala
* Ladybug
* Lamprey
* Lemur
* Leopard
* Lion
* Lizard
* Llama
* Lobster
* Lynx
* Manatee
* Mantis shrimp
* Meerkat
* Mink
* Markhor
* Mongoose
* Monkey
* Moose
* Narwhal
* Newt
* Ocelot
* Octopus
* Opossum
* Orangutan
* Orca
* Oryx
* Ostrich
* Otter
* Owl
* Panda
* Pangolin
* Panther
* Parrot
* Peacock
* Peccary
* Penguin
* Pig
* Pigeon
* Platypus
* Porcupine
* Pufferfish
* Puma
* Quokka
* Rabbit
* Raccoon
* Rattlesnake
* Raven
* Salmon
* Scorpion
* Seagull
* Sea cucumber
* Sea urchin
* Shark
* Sheep
* Shrimp
* Skunk
* Sloth
* Snail
* Snake
* Squirrel
* Starfish
* Stingray
* Sturgeon
* Sunfish
* Tarantula
* Tardigrade
* Tasmanian devil
* Tiger
* Toad
* Toucan
* Trout
* Tuatara
* Turtle
* Vampire bat
* Wallaby
* Walrus
* Warthog
* Whale
* Wolf
* Wolverine
* Wombat
* Yak
* Zebra

### AnimalFactsBot will reply to its replies if they contain the phrases:
* good bot
* bad bot
* thank
* more
* silly
* TIL
* AnimalFactsBot

AnimalFactsBot gets these fairly often.
