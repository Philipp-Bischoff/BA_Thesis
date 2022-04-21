#This is a class representing a site

class Site:

    def __init__(self, idx, quality, probability, bees_at_site):
        self.idx = idx
        self.quality = quality
        self.probability = probability
        self.bees_at_site = bees_at_site

    def empty_site(self):
        self.bees_at_site.clear()

    def add_bee_to_site(self, Bee):
        self.bees_at_site.append(Bee)

    def remove_bee_from_site(self):
        try:
            self.bees_at_site.pop()
        except IndexError:
            pass
            #print("The site is empty now")

    def get_quality(self):
        return self.quality

    def count_bees_at_site(self):
        return len(self.bees_at_site)
    
    def get_site_id(self):
        return self.idx

    def get_site_probability(self):
        return self.probability


    
