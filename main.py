from board import board
from pynput import keyboard
# from time import sleep

b = board()

def main():
    print("Καλώς ήρθατε στο 8 puzzle")
    # b.shuffle()
    print(b)
    # Πάρθηκε έτοιμο απο pynput https://pypi.org/project/pynput/
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def on_press(key):
    #b.refresh() # Υπάρχει για άλλη εφαρμογή (Να αγνοηθεί)
    pass

def on_release(key, x=1):
    if key == keyboard.Key.esc:
        # Stop listener
        return False
    elif key == keyboard.Key.up:
        print("Πάνω")
        b.board, b.e_loc = b.move_up(b.board, b.e_loc)
    elif key == keyboard.Key.right:
        print("Δεξιά")
        b.board, b.e_loc = b.move_right(b.board, b.e_loc)
    elif key == keyboard.Key.down:
        print("Κάτω")
        b.board, b.e_loc = b.move_down(b.board, b.e_loc)
    elif key == keyboard.Key.left:
        print("Αριστερά")
        b.board, b.e_loc = b.move_left(b.board, b.e_loc)
    elif key == keyboard.Key.shift:
        print("Χμμ... για να δώ πως λύνεται. (Σκέφτομαι)")
        moves = b.solve()
        for m in moves:
            b.moves[m](b.board, b.e_loc) # Τα 0,1,2,3 είναι απο το dictionary στο board.py
            if m == 0:
                print("Κίνηση: Πάνω")
            elif m == 1:
                print("Κίνηση: Δεξιά")
            elif m == 2:
                print("Κίνηση: Κάτω")
            else:
                print("Κίνηση: Αριστερά")
            x += 1 # Μετράει τα βήματα μέχρι την λύση
            print(b.board) #Επιστρέφει την μορφή κάθε βήματος
            print("Αριθμός Βήματος:", x) #Επιστρέφει τον αριθμό κάθε βήματος
            print("---------------------------")
            b.refresh()
            # sleep(1) #Περιτό για την αυτόματη λύση.


    return b.refresh()


if __name__ == "__main__":
    main()