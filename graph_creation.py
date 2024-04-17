#Dictionary Creation
import pandas as pd
from unidecode import unidecode
from collections import defaultdict

class TitleDictionary:

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df["primaryTitle"] = self.df["primaryTitle"].apply(unidecode)
        self.title_dict = self._create_title_dict()
        self.profession_dict = self._create_profession_dict()

    def _create_title_dict(self):
        # Dictionary structure:
            # key: nconst
            # value: list of movie_names(primaryTitle's) actors/directors involved in
        #Create a dictionary in the format:
        #{nconst:[movie_names actors/directors involved in], here the actor/director is determined by id: nconst}
        #example dictionary looks like:
        #{'nm6551690': ['The Dreaded Hong Kong SneezeThe Great Bank Robbery',
         #  'The Reluctant RobotThe Royal Foil',
         #  'Theres No Business Like Snow Business'],
         #
         #  'nm8002705': ['The Awful Awakening of Claudius Brodequin',
         #  'The Dreaded Arrival of Captain Tardivaux',
         #  'The Glorious Triumph of Barthelemey Piechut',
         #  'The Magnificent Idea of Barthelemey Piechut the Mayor',
         #  'The Painful Infliction of Nicholas the Beadle',
         #  'The Scandalous Outcome of a Night of Destruction',
         #  'The Spirited Protest of Justine Pulet',
         #  'The Triumphant Inauguration of a Municipal Amenity']}
        title_dict = defaultdict(list)
        for index,row in self.df.iterrows():
            title_dict[row['nconst']].append(row['primaryTitle'])

        print(len(title_dict))
        return title_dict #return the Created {nconst:[movie_titles]} dictionary

    def _create_profession_dict(self):
        # Dictionary structure:
            # key: nconst
            # value: actors/directors names with tail as '_a' or '_d'
        #Create a dictionary in the format:
        #{nconst:[actors/directors names], here the actor/director is determined by id: nconst}
        #while creating this dictionary values put _d at end of the name to indicate the person name as director and _a to represent the actor.
        #See the below example to understand more clearly.
        #example dictionary looks like:
        #{'nm0465106': 'Hal Roach Jr._d',
         # 'nm6081065': 'Benjamin H. Kline_d',
         # 'nm0962553': 'William Asher_d',
         # 'nm4337938': 'Rod Serling_a',
         # 'nm5829291': 'Sydney Newman_d',
         # 'nm7171552': 'Wolfgang Menge_a',
         # 'nm0231693': 'Blake Edwards_d',
         # 'nm6446679': 'Bob Wehling_a'}
        profession_dict = defaultdict(list)

        for index,row in self.df.iterrows():
            if row['primaryProfession'].lower()=='actor':
                if row['primaryName']+"_a" not in profession_dict[row['nconst']]:
                    profession_dict[row['nconst']].append(row['primaryName']+"_a")

            if row['primaryProfession'].lower()=='director':
                if row['primaryName']+"_d" not in profession_dict[row['nconst']]:
                    profession_dict[row['nconst']].append(row['primaryName']+"_d")

        return profession_dict #return the Created {nconst:person_name_a/d} dictionary


#Graph Network Creation
class MovieNetwork:
    def __init__(self, name_movie_dict, nconst_ar_dr):
        self.graph = {} #graph dictionary initialization
        self.name_movie_dict = name_movie_dict #name_movie_dict is nothing but "title_dict" dictionary refer to above example in TitleDictionary.
        self.nconst_ar_dr = nconst_ar_dr #it is "profession_dict" dictionary refer to above example in TitleDictionary.


    def add_node(self, node):
        self.graph[node]={}
        #write code to add node to the graph (dictionary data-structure)

    def add_edge(self, node1, node2, nconst_ar_dr, weight=1):
        if weight>2:
            v1=nconst_ar_dr[node1][0]
            v2=nconst_ar_dr[node2][0]
            # print(v1[-2:],v2[-2:])
            if (v1[-2:]=="_d" and v2[-2:]=="_d") or (v1[-2:]=="_a" and v2[-2:]=="_a"):
                self.graph[node1][node2]=weight
                self.graph[node2][node1]=weight
            elif v1[-2:]=="_a" and v2[-2:]=="_d":
                self.graph[node2][node1]=weight
            elif v1[-2:]=="_d" and v2[-2:]=="_a":
                self.graph[node1][node2]=weight

        #node 1, node 2: nconst id's
        #nconst_ar_dr is nothing but "profession_dict" dictionary refer to above example in TitleDictionary.
        #weight is number of common movie titles exists in node1 and node2
        #Before adding Edge weights you must follow the below Instructions:
            #1. consider only the node1->node2 connection or edge, only if node1 and node2 have more than 2 movies in common.
            #2. Let node1="actor" and node2="director" then node1->node2 edge should not be taken implies {actor:{director:6}} must not be taken.
                # But node2->node1 should be taken implies {director:{actor:6}} must be taken.
            #3. if node1 and node2 are assigned with both actors or directors then bi-directional edge must be added implies
                #{actor1:{actor2:4}} and {actor2:{actor1:4}} or {director1:{director2:7}} and {director2:{director1:7}} both ways are true
                #and must consider in dictionary.
        #write code to add edge to the graph implies add weight between node1 and node 2
        #Example weight assignment looks like:
        # {'nm1172995': {'nm0962553': 7}} here the weight 7 is nothing but the number of common
        #movies between two persons either actor/director (nm1172995 and nm0962553)
    def calculate_weight(self,node1,node2):
        return len(set(self.name_movie_dict[node1]).intersection(set(self.name_movie_dict[node2])))

    def create_graph(self):
        for i in self.name_movie_dict:
            self.add_node(i)
        nodes=[i for i in self.name_movie_dict.keys()]
        for i in range(len(nodes)):
            # self.calculate_weight(nodes[i],None)
            for j in range(i+1,len(nodes)):
                # print(self.calculate_weight(nodes[i],nodes[j]))
                self.add_edge(nodes[i],nodes[j],self.nconst_ar_dr,self.calculate_weight(nodes[i],nodes[j]))
        #By following the above conditions create a graph (use only dictionary datastructure: self.graph)
        #example graph looks like:
          # {'nm0962553': {'nm8630849': 3,
             #  'nm1172995': 7,
             #  'nm8742830': 16,
             #  'nm6225202': 4,
             #  'nm4366294': 4},
             # 'nm8630849': {},
             # 'nm1172995': {'nm0962553': 7},
             # 'nm8742830': {'nm0962553': 16},
             # 'nm6225202': {}}
        return self.graph

