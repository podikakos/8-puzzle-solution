import queue
import random
from copy import deepcopy
#from Queue import Queue()

STHLES = 3
SEIRES = 3
ANAKATANOMH = 80


class board:

    def __init__(self):
        self.goal = [["_", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]
        self.start = [["7", "2", "4"], ["5", "_", "6"], ["8", "3", "1"]]
        # self.board = deepcopy(self.goal) #Πριν το shuffle για αρχικοποίηση στην θέση GOAL
        self.board = deepcopy(self.start) #Deepcopy() γιατι self.board = self.start θα έχει άλλο αποτέλεσμα
        # self.e_loc = [0, 0] #Για αρχικό κενό πάνω αριστερά θέση: 0,0
        self.e_loc = [1, 1] #Για αρχικό κενό στην μέση: θέση 1,1
        self.moves = {0: self.move_up, 1: self.move_right, 2: self.move_down, 3: self.move_left} # Λεξικό για τις κινήσεις της shuffle συνάρτησης αλλά και γενικά


    def __repr__(self):     #Για απεικόνιση του πίνακα
        for i in range(SEIRES):
            for j in range(STHLES):
                print(self.board[i][j], end=" ")
            print()
        return "" # Κάθε εντολή πρέπει να έχει ένα return.
    def refresh(self):
        #print(self) # Κολλάει για μεγάλο αριθμό
        if self.board == self.goal:
            print("\nΛύθηκε! :)")
            print(self)
            return False
        return True

    def shuffle(self): #Τεστ του αλγορίθμου εαν μπορεί να λύσει προβλήματα μικρών κινήσεων

        random.seed()
        for i in range(ANAKATANOMH):
            m = random.randint(0, 3)
            self.moves[m](self.board, self.e_loc)

        # Μετακινεί το κενό κάτω δεξιά (μπορεί να παραληφθεί)
        # for i in range(SEIRES):
        #     self.moves[2](self.board, self.e_loc)
        # for i in range(STHLES):
        #     self.moves[1](self.board, self.e_loc)


    def move(self, board, e_loc, x, y):

        #Έλεγχος για το αν η κίνηση ξεπερνά τα όρια του Πίνακα
        if e_loc[0] + x < 0 or e_loc[0] + x > 2 or e_loc[1] + y < 0 or e_loc[1] + y > 2:
            return board, e_loc

        #Αλλαγή θέσης δηλαδή "SWAP" των δύο θέσεων μεταξύ τους
        board[e_loc[0]][e_loc[1]], board[e_loc[0] + x][e_loc[1] + y] \
        = board[e_loc[0] + x][e_loc[1] + y], board[e_loc[0]][e_loc[1]]
        # x, y = y, x Στην Γενική ιδέα

        #Ενημέρωση της θέσης
        e_loc[0] += x
        e_loc[1] += y

        return board, e_loc


    def move_up(self, board, e_loc):
        return self.move(board, e_loc, -1, 0)

    def move_right(self, board, e_loc):
        return self.move(board, e_loc, 0, 1)

    def move_down(self, board, e_loc):
        return self.move(board, e_loc, 1, 0)

    def move_left(self, board, e_loc):
        return self.move(board, e_loc, 0, -1)

    def solve(self):
        # Δημιουργία Children/successors
        def successors(board, e_loc):
            b_lst = [deepcopy(board), deepcopy(board), deepcopy(board), deepcopy(board)]
            e_loc_lst = [list(e_loc), list(e_loc), list(e_loc), list(e_loc)]
            b_lst[0], e_loc_lst[0] = self.move_up(b_lst[0], e_loc_lst[0])
            b_lst[1], e_loc_lst[1] = self.move_right(b_lst[1], e_loc_lst[1])
            b_lst[2], e_loc_lst[2] = self.move_down(b_lst[2], e_loc_lst[2])
            b_lst[3], e_loc_lst[3] = self.move_left(b_lst[3], e_loc_lst[3])

            return[[b_lst[0], e_loc_lst[0], 0], [b_lst[1], e_loc_lst[1], 1], [b_lst[2], e_loc_lst[2], 2], [b_lst[3], e_loc_lst[3], 3]]
            # 4 Πιθανές κινήσεις για κάθε παιδί (child) ανα layer/level


        searched =set() #Αποθήκευση καταστάσεων που έχουν ήδη αξιολογηθεί set αντί για list λόγω μνήμης
        fringe = queue.Queue() #Αποθήκευση των children που είναι για έλεγχο-FIFO style
        # root = self.board #Απο ποιό αρχικό πίνακα ξεκινά η αξιολόγηση kick-off
        fringe.put({"board": self.board, "e_loc": self.e_loc, "path": []}) #root αντι για self.board στην περίπτωση enable
        # Dictionary με τα στοιχεία που θέλουμε (Πίνακα, θέση κενού και το μονοπάτι που ακουλουθείται).

        while True:
            # Ασφάλεια στην περίπτωση που δεν λύνεται. Άρα όταν fringe είναι κενό να σταματά
            if fringe.empty():
                return []

            # Μας δίνει τον κόμβο (Queue Function) για επιθεώρηση (τον αφαιρεί απο την λίστα FIFO)
            node = fringe.get()

            # Έλεγχος για τον εαν ο κόμβος είναι και η λύση (Quit εάν είναι)
            if node["board"] == self.goal:
                return node["path"]

            # Πρόσθεση του κόμβου στο searched και προσθήκη των children/successor στο fringe
            if str(node["board"]) not in searched:
                searched.add(str(node["board"]))
                for child in successors(node["board"], node["e_loc"]):
                    if str(child[0]) not in searched:
                        fringe.put({"board": child[0], "e_loc": child[1], "path": node["path"] + [child[2]]})
                        #Πρόσθέτει σε μια λίστα το επόμενο path δλδ [1,2,3] + [4] Concatenate Style



        #self.board = deepcopy(self.goal) #Για να κλέψουμε ;)

