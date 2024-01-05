

## How to contribute (Teach AnimalFactsBot a new animal):

Check the open issues to claim a listed animal, or come up with your own. Be sure to also check currently open pull requests to make sure you don't duplicate someone else's work.

Due to Hacktoberfests pull requests are coming in fast! Comment on an issue you are going to work on - and also check open pull requests before you do work someone else has already done.

**Huge changes have been made lately! Please rebase and check your changes still fit the rules below!**

Steps:
* Fork/clone the repo.
* Add a tuple of strings of facts (to animalfacts.py) pertaining to a particular animal. Name the tuple variable following the format 'NAMEOFANIMAL_FACTS'. Put the tuple in alphabetical order with the other tuples. Make sure your lines are indented by 4 spaces and please use ' for your strings. Use escape characters where necessary.
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
* Do use American spellings of words like 'color' or 'meter'.

If you have a question the quickest way to reach is me on twitter @joelatwar


# animal-facts-bot

Animal-facts-bot is a Reddit bot that searches for comments on reddit that contain the name of the animal and then replies to the comment with a fact about that animal.

You can see the bot in action at https://www.reddit.com/user/AnimalFactsBot/comments/

### Current supported animals:

* Aardvark
* Aardwolf
* African grey
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
* Avocet
* Axolotl
* Badger
* Ball Python
* Barnacle
* Bear
* Beaver
* Bison
* Blobfish
* Bobcat
* Buffalo
* Butterfly
* Camel
* Capybara
* Chameleon
* Cheetah
* Chevrotain
* Chicken
* Chimpanzee
* Chinchilla
* Chipmunk
* Clownfish
* Cobra
* Cougar
* Cow
* Coyote
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
* Earwig
* Echidna
* Eland
* Elephant
* Elephant shrew
* Elk
* Emu
* Falcon
* Ferret
* Fire salamander
* Flamingo
* Fox
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
* Hawk
* Hedgehog
* Hippo
* Honeybee
* Honey badger
* Horse
* House fly
* Hummingbird
* Husky
* Ibex
* Iguana
* Jackal
* Jellyfish
* Jerboa
* Kangaroo
* Kiwi
* Koala
* Kookaburra
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
* Markhor
* Meerkat
* Mink
* Mongoose
* Monkey
* Moose
* Narwhal
* Newt
* Nightjar
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
* Praying Mantis
* Quokka
* Rabbit
* Raccoon
* Rattlesnake
* Raven
* Reindeer
* Rhino
* Salmon
* Scorpion
* Seagull
* Seahorse
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
* Stoat
* Sturgeon
* Sunfish
* Tarantula
* Tardigrade
* Tarsier
* Tasmanian devil
* Tiger
* Toad
* Toucan
* Trouser Snake
* Trout
* Tuatara
* Turtle
* Vampire bat
* Vulture
* Wallaby
* Walrus
* Warthog
* Whale
* Wildebeest
* Wolf
* Wolverine
* Yak
* Zebra
* Zebrafish

### AnimalFactsBot will reply to its replies if they contain the phrases:
* good bot
* bad bot
* thank
* more
* silly
* TIL
* AnimalFactsBot

AnimalFactsBot gets these fairly often.
