import engine_helpers as helpers
import file_handler.file_lib as files

class Room(object):
    def __init__(self, room=None):
        self._current_room = room

    @property
    def current_room(self):
        return self._current_room

    @current_room.setter
    def current_room(self, room):
        self._current_room = room

    @current_room.deleter
    def current_room(self):
        del self._current_room
    #------------------------------------------------------------------------
    # This begins room getters section
    #------------------------------------------------------------------------
    @property
    def title(self):
        """returns the room's title"""
        return self._current_room['title']

    @property
    def feature_searched(self):
        """returns bool of the featured_searched field"""
        return self._current_room['feature_searched']

    @property
    def get_room_desc(self):
        """returns either the long or short description if the room has been visited"""
        if self.visited == False:
            return self.long_desc
        else:
            return self.short_desc

    @property
    def long_desc(self):
        """returns a string of the long description and items in room"""
        return self._current_room['long_description'] + self.get_items_in_room()

    @property
    def short_desc(self):
        """returns a string of the short description and items in room"""
        return self._current_room['short_description'] + self.get_items_in_room()

    @property
    def get_room_artifact(self):
        """if the room has ascii art then return it here"""
        if 'room_artifact' in self._current_room:
            return self._current_room['room_artifact']
        else:
            return []

    def get_items_in_room(self):
        """
        if the room has been searched appropriately and there are items in the room
        then returns the items in the room as a string for descriptive purposes
        """
        text = " Looking around you see "
        if (self._current_room['feature_searched'] == True and
                self._current_room['items_in_room'] and
                len(self._current_room['items_in_room']) > 0):
            items = self._current_room['items_in_room']
            for item in items:
                text += "a " + item + ", "
            text = text[:-2]
            text += ". "
        else:
            text = ""
        return text

    @property
    def visited(self):
        """
        returns the boolean in visited
        """
        return self._current_room['visited']
    @visited.setter
    def visited(self, value):
        self._current_room['visited'] = value

    @property
    def temp(self):
        return self._current_room['room_temp']
    #------------------------------------------------------------------------
    # This ends room getters section
    #------------------------------------------------------------------------
    #------------------------------------------------------------------------
    # This begins room modifiers section
    #------------------------------------------------------------------------
    def remove_item_from_room(self, title):
        """
        removes an items from the inventory of a room
        do not attempt to remove something not already there
        """
        if title in self._current_room['items_in_room']:
            self._current_room['items_in_room'].remove(title)
    def add_item_to_room(self, title):
        """
        adds an item to the room, does not allowed for duplicates
        """
        if title not in self._current_room['items_in_room']:
            self._current_room['items_in_room'].append(title)
    #------------------------------------------------------------------------
    # This ends the room  section
    #------------------------------------------------------------------------
    #------------------------------------------------------------------------
    # This begins the feature related section
    #------------------------------------------------------------------------
    def feature_action(self, title, verb):
        """
            looks up to see if the title passed in is a feature in the current room
            if so and the verb is in the list of possible verbs for that feature then
        """
        res = helpers.response_struct()
        if title in self._current_room['features']:
            feature = self._current_room['features'][title]
            if verb in feature['verbs']:
                res.description = feature['verbs'][verb]['description']
                res.modifiers = feature['verbs'][verb]['modifiers']
                if 'artifact' in feature['verbs'][verb]:
                    res.artifact = feature['verbs'][verb]['artifact']
            else:
                res.description = 'You are not able to ' + verb + ' the ' + title
        else:
            res.description = 'Sorry, ' + title + ' not found in this room.'
        return res
    #------------------------------------------------------------------------
    # This ends the feature section
    #------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    # This section dedicated to functions relating to moving from one
    # room to another
    #-------------------------------------------------------------------------

    def check_connections(self, title_dir, items):
        """
        when given an official room title or compass direction, iterates
        through the current room's connected_rooms object to see if the compass
        or room title exist
        checks if an item is required to pass into this room
        Also checks if the rooms is accessible meaning passable
        if an item is required checks to see if that item is active as in worn or on
        writes the appropriate response into
        description
        move = boolean whether or not the move was successful
        title = the new room's title
        distance_from_room = distance traveled to the new room
        """
        res = helpers.response_struct()
        res.success = False
        for room_key in self._current_room['connected_rooms']:
            #this line added as a result of the connected_rooms refactoring
            #all other functionality remains the same
            room = self._current_room['connected_rooms'][room_key]
            if (title_dir in {room['title'], room['compass_direction']} or
                title_dir in room['aliases']):
                res.title = room['title']

                if 'modifiers' in room: res.modifiers = room['modifiers']

                if (room['item_required'] == True and
                    room['accessible'] == True):
                    item_title = room['item_required_title']
                    items = [item for item in items if item['title'] == item_title]
                    if items: item = items[0]
                    else: item = None
                    if item and item['active'] == True:
                        res.success = True
                        res.distance_from_room = room['distance_from_room']
                    else:
                        res.description = room['pre_item_description']
                elif room['item_required'] == False and room['accessible'] == True:
                    res.success = True
                    res.distance_from_room = room['distance_from_room']
                    res.description = room['pre_item_description']
                else:
                    res.description = room['pre_item_description']
                #we can break the for loop as soon as we have found a match
                break
        return res
    #------------------------------------------------------------------------
    # This ends the movement related functions
    #------------------------------------------------------------------------
