from sites import Site

#This is a class representing a bee

class Bee:
    
    def __init__(self, idx, dance_duration, state, current_site, probability):
        self.idx = idx
        self.dance_duration = dance_duration
        self.state = state
        self.current_site = current_site
        self.probability = probability 

    def reduce_dance_duration(self):
        self.dance_duration = self.dance_duration - 1 

    def get_dance_duration(self):
        return self.dance_duration

    def set_dance_duration(self, new_dance_duration):
        self.dance_duration = new_dance_duration

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_site(self):
        return self.current_site

    def set_site(self, site):
        self.current_site = site

    def get_id(self):
        return self.idx

