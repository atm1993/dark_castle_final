import os
import json

class Parse:
  def __init__(self):
    self.verbs = {"activate":"activate",
                  "add":"add",
                  "chew":"eat", 
                  "chug":"drink", 
                  "cut":"cut", 
                  "drink":"drink", 
                  "drop":"drop",
                  "eat":"eat", 
                  "enter":"enter", 
                  "exit":"quit",
                  "get":"get", 
                  "go":"go", 
                  "grab":"grab", 
                  "leave":"quit", 
                  "look":"look",
                  "look at":"look at",
                  "look under":"look under",
                  "move":"go", 
                  "munch":"eat", 
                  "open":"open", 
                  "pick up":"pick up",
                  "pick":"pick up",
                  "play":"play", 
                  "push":"push",
                  "q":"quit",
                  "quit":"quit",
                  "read":"read", 
                  "rescue":"rescue", 
                  "sip":"drink", 
                  "sit":"sit",
                  "swig":"drink", 
                  "take":"take", 
                  "talk to":"talk to",
                  "try on":"try on",
                  "turn on":"turn on",
                  "use":"use", 
                  "watch":"watch",
    }
    self.determiner = [
          "a",
          "an",
          "some",
          "that",
          "the",
          "these"
          "this",
          "those"
    ]
    self.direction = {
          "down":"down",
          "e":"east",
          "east":"east",
          "north":"north",
          "n":"north",
          "south":"south",
          "s":"south",
          "up":"up",
          "west":"west",
          "w":"west",
          "above":"up",
          "below":"down"
    }

    self.objects = {"aged wine":"aged_wine",
                    "aged_wine":"aged_wine",
                    "agedwine":"aged_wine",
                    "jeweled pendant":"jeweled_pendant",
                    "jeweled_pendant":"jeweled_pendant",
                    "jeweledpendant":"jeweled_pendant",
                    "lamp":"lamp",
                    "mirror":"mirror",
                    "musty tome":"musty_tome",
                    "musty_tome":"musty_tome",
                    "mustytome":"musty_tome",
                    "mutton":"mutton",
                    "royal crown":"royal_crown",
                    "royal_crown":"royal_crown",
                    "royalcrown":"royal_crown",
                    "rusty key":"rusty_key",
                    "rusty_key":"rusty_key",
                    "rustykey":"rusty_key",
      }

    self.items = {"altar":"altar",
    "ball_gown":"ball_gown",
    "ball gown":"ball_gown",
    "ballgown":"ball_gown",
    "barrel":"barrel",
    "bed":"bed",
    "bench":"bench",
    "bookshelf":"bookshelf",
    "cell_door":"cell_door",
    "cell door":"cell_door",
    "celldoor":"cell_door",
    "chess_board":"chess_board",
    "chessboard":"chess_board",
    "chess board":"chess_board",
    "chest":"chest",
    "crumbling_stones":"crumbling_stones",
    "crumbling stones":"crumbling_stones",
    "crumblingstones":"crumbling_stones",
    "dead_tulip":"dead_tulip",
    "dead tulip":"dead_tulip",
    "deadtulip":"dead_tulip",
    "desk":"desk",
    "dirt_mound":"dirt_mound",
    "dir mound":"dirt_mound",
    "dir_mound":"dirt_mound",
    "dresser":"dresser",
    "garden":"garden",
    "grave":"grave",
    "greatsword":"greatsword",
    "journal":"journal",
    "ledger":"ledger",
    "pack":"pack",
    "painting":"painting",
    "pew":"pew",
    "plaque":"plaque",
    "scroll":"scroll",
    "skeleton":"skeleton",
    "statue":"statue",
    "table":"table",
    "tattered_clothing":"tattered_clothing",
    "tattered clothing":"tattered_clothing",
    "tatteredclothing":"tattered_clothing",
    "telescope":"telescope",
    "throne":"throne",
    "violin":"violin",
    "water":"water",
    "wine_goblet":"wine_goblet",
    "wine goblet":"wine_goblet",
    "winegoblet":"wine_goblet",
    "wine_rack":"wine_rack",
    "wine rack":"wine_rack",
    "winerack":"wine_rack",
    "wooden_sign":"wooden_sign",
    "wooden sign":"wooden_sign",
    "woodensign":"wooden_sign",

    
    }

    self.prepositions = ["about", "above", "across", "after", "against", "along", "among", "around", "at",
                        "before", "behind", "below", "beneath", "beside", "between", "by", "down", "during", 
                        "except", "for", "from", "front", "in", "inside","instead", "into", "like", "near", "of", 
                        "off", "on", "onto", "out", "outside", "over", "past","since", "through", "to", "top", 
                        "toward", "under", "underneath", "until", "up", "upon", "with", "within", "without"]

    self.rooms = {"bailey":"bailey",
                  "ballroom":"ballroom",
                  "barracks":"barracks",
                  "castle_gate":"castle_gate",
                  "chapel":"chapel",
                  "dungeon":"dungeon",
                  "great hall":"great_hall",
                  "great_hall":"great_hall",
                  "greathall":"great_hall",
                  "guard house":"guard_house",
                  "guard_house":"guard_house",
                  "guardhouse":"guard_house",
                  "hidden chamber":"hidden_chamber",
                  "hidden_chamber":"hidden_chamber",
                  "hiddenchamber":"hidden_chamber",
                  "kings bed chambers":"kings_bedchambers",
                  "kings bedchambers":"kings_bedchambers",
                  "kings gardens":"kings_gardens",
                  "kings_bedchambers":"kings_bedchambers",
                  "kings_gardens":"kings_gardens",
                  "kingsbedchambers":"kings_bedchambers",
                  "kingsgardens":"kings_gardens",
                  "kitchen":"kitchen",
                  "library":"library",
                  "moat":"moat",
                  "observatory":"observatory",
                  "scribes room":"scribes_room",
                  "scribes_room":"scribes_room",
                  "scribesroom":"scribes_room",
                  "servants quarters":"servants_quarters",
                  "servants_quarters":"servants_quarters",
                  "servantsquarters":"servants_quarters",
                  "testroom":"testroom",
                  "throne room":"throne_room",
                  "throne_room":"throne_room",
                  "throneroom":"throne_room",
                  "wine cellar":"wine_cellar",
                  "wine_cellar":"wine_cellar",
                  "winecellar":"wine_cellar",
      }

  def parse_user_input(self, input_string):
    if self.is_string_empty(input_string):
      return(None, None, None, None, None)
    
    word_list = self.convert_string_to_word_list(input_string.lower())
    word_list = self.remove_definitive_articles(word_list)
    
    if len(word_list) == 0:
      return None, None, None, None, None
    
    cmd = self.get_command_prompt(word_list)
    if cmd is None and len(word_list) == 0:
      return None, None, None, None, None
    
    if cmd is None:
      cmd = "go"
    if cmd == "go":

      cardinal_direction = self.get_direction(word_list)
      room = self.match_noun(word_list, self.rooms)

      if cardinal_direction and room is None:
        return cmd, None, cardinal_direction, None, None

      if cardinal_direction is None and room:
        return cmd, room, None, None, None

      if cardinal_direction and room:
        return None, None, None, None, None
      
      if cardinal_direction is None and room is None:
        return None, None, None, None, None

    objects = self.match_noun(word_list, self.objects)
    item = self.match_noun(word_list, self.items)

    return cmd, None, None, item, objects

  def match_noun(self, user_input_list, reference_list):
    number_of_user_input_elements = len(user_input_list)
    for word in reference_list:
      new_word_list = self.convert_string_to_word_list(word)
      
      for index in range(number_of_user_input_elements):
        if new_word_list == user_input_list[index:(index + len(new_word_list))]:
          return "_".join(new_word_list)
    
    return None

  def convert_string_to_word_list(self, string):
    return string.split()
  
  def remove_definitive_articles(self, word_list):
    return [word for word in word_list if word not in self.determiner]

  def get_command_prompt(self, word_list):

    cmd = None
    preposition = None
    if len(word_list) > 1:
      preposition = self.match_noun([word_list[1]], self.prepositions)

    if word_list[0] in self.verbs:
      cmd = self.verbs[word_list[0]]
      del word_list[0]
      if preposition:
        new_action = cmd + " " + preposition
        if new_action in self.verbs:
          cmd = self.verbs[new_action]
          del word_list[0]

    elif len(word_list) > 1 and cmd is None and preposition is not None:
      new_action = word_list[0] + " " + preposition
      if new_action in self.verbs:
        cmd = self.verbs[new_action]
        del word_list[0]
        del word_list[0]

    return cmd
  
  def get_direction(self, word_list):
    direction = None
    if word_list[0] in self.direction:
      direction = self.direction[word_list[0]]
    
    return direction

  def is_string_empty(self, string):
    if string is None:
      return True
    else:
      return False

# def main():
#   parser = Parse()
#   while True:
#     prompt = input("What Move Would You Like to Do? ")
#     if prompt ==  "q":
#       break
#     action, room, direction, room_item, objects = parser.parse_user_input(prompt)
#     print("This is the action: ", action)
#     print("This is the direction: ", direction)
#     print("This is the room: ", room) 
#     print("This is the room_item: ", room_item) 
#     print("This is the object: ", objects) 

# main()