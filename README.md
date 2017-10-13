## How to contribute (Teach AnimalFactsBot a new animal): 
        Choose an animal listed in the issues or any other real animal.

* Fork/clone the repo
* Add a tuple of strings of facts (to animalfacts.py) pertaining to a particular animal. Name the tuple variable following the format 'NAMEOFANIMAL_FACTS'. Put the tuple in alphabetical order with the other tuples.
* Add your tuple to the ALL_FACTS tuple.
* Add a line to the check_comment_for_animal() function for your animal following the format.
* Add your animal to the Readme

Please: Don't add a very small set of facts (this will cause the bot to be repetetive regarding your animal).
        Each fact must make sense independent of the other facts in the tuple because users will only get one fact at a time.
        Only add TRUE facts. Please no trolling with 'alternative facts'.
        Don't add 'seal', 'bat' or 'duck' facts unless you've figured out how to not reply to homonyms.
        Don't add 'cat' or 'dog' because they are just too common on reddit.
        
If you have a question the quickest way to reach is me on twitter @joelatwar


# animal-facts-bot

A Reddit bot that searches for comments on reddit that contain the name of the animal and then replies to the comment with a fact about that animal.

You can see the bot in action at https://www.reddit.com/user/AnimalFactsBot/comments/

### Current supported animals:
* alligator
* badger
* beaver
* camel
* cheetah
* cow
* crab
* cuttlefish
* dolphin
* dragon
* eagle
* echidna
* elephant
* emu
* flamingo
* fox
* frog
* giraffe
* grasshopper
* gorilla
* hamster
* hedgehog
* hippo
* horse
* hummingbird
* husky
* jellyfish
* kangaroo
* koala
* lion
* leopard
* lizard
* monkey
* narwhal
* ocelot
* octopus
* otter
* owl
* panda
* pangolin
* panther
* peacock
* parrot
* penguin
* pig
* pigeon
* scorpion
* seagull
* shark
* sloth
* snake
* tiger
* turtle
* wolf
* whale
* zebra

### AnimalFactsBot will reply to its replies if they contain the phrases:
* good bot
* bad bot
* thank
* more
* silly
* TIL
* AnimalFactsBot

AnimalFactsBot gets these fairly often.
