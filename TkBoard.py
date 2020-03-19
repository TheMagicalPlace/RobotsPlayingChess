from tkinter import *
import time
from ChessPieces import *
class ChessBoard:


    def _init_piece(self,x):
        s = 'abcdefgh'
        canvas = self.canvas
        back_row = lambda owner: [Rook(owner), Knight(owner), Bishop(owner),
                                  Queen(owner), self.kings[owner], Bishop(owner), Knight(owner),
                                  Rook(owner)]
        dDummy = lambda: [Dummy() for _ in range(1, 9)]
        dPawn = lambda owner: [Pawn(owner) for _ in range(1, 9)]

        rules = {1: back_row('Black'), 2: dPawn('Black'), 3: dDummy(), 4: dDummy(),
                 5: dDummy(), 6: dDummy(), 7: dPawn('White'), 8: back_row('White')}
        for j in range(0, 8):
            jj = x * j // 8 + 2
            pieces = rules[j+1]
            for i in range(0, 8):
                ii = x * i // 8 + 2
                if (not i % 2 and not j % 2) or (i % 2 and j % 2):

                    cobj = canvas.create_rectangle((ii, jj), (ii + x // 8, jj + x // 8), fill='#5d432c')
                else:
                    cobj = canvas.create_rectangle((ii, jj), (ii + x // 8, jj + x // 8), fill='black')
                cobj_text = canvas.create_text(ii + x // 16, jj + x // 16, text=pieces[i].piece,
                                               fill=('black' if j < 2 else 'white'))
                self.space_contents[(8 - j, s[i])] = [cobj, cobj_text,pieces[i]]
                pieces[i].position = (8-j, s[i])
        canvas.itemconfigure(self.space_contents[(1, 'h')][0], fill='green')
    def config_board_asthetic(self):
        x = self.x
        root = Tk()
        bgcolor = '#91672c'
        #root = Frame(master=rt,bg=bgcolor,borderwidth=0)
        root.configure(background=bgcolor)
        lflank = Canvas(master=root,width=50,bg=bgcolor,bd=0, highlightthickness=0, relief='ridge')
        rflank = Canvas(master=root, width=50,bg=bgcolor,bd=0, highlightthickness=0, relief='ridge')
        tflank = Canvas(master=root,height=50,bg=bgcolor,bd=0, highlightthickness=0, relief='ridge')
        bflank = Canvas(master=root, height=50,bg=bgcolor,bd=0, highlightthickness=0, relief='ridge')
        canvas = Canvas(master=root, width=402, height=402,)
        s = 'ABCDEFGH'
        for i in range(0,8):
            ii = x*i//8+2
            lflank.create_text(40,ii+x//16,text=str(8-i))
            rflank.create_text(10,ii+x//16,text=str(8-i))
            tflank.create_text(ii+x//16,40,text=s[i])
            bflank.create_text(ii + x // 16, 10, text=s[i])
        canvas.grid(row=1, column=1,padx=0, pady=0)
        tflank.grid(row=0,column=1,padx=0, pady=0,sticky='NSEW')
        lflank.grid(row=1,column=0,padx=0, pady=0,sticky='NSEW')
        rflank.grid(row=1,column=2,padx=0, pady=0,sticky='NSEW')
        bflank.grid(row=2,column=1,padx=0, pady=0,sticky='NSEW')
        self.canvas = canvas
        self.root = root

    def __init__(self):
        self.board = {}
        s = 'ABCDEFGH'
        self.kings = {'White': King('White'), 'Black': King('Black')}
        self.space_contents = {}

        self.x = 400




        self.config_board_asthetic()
        self._init_piece(self.x)

        self. root.mainloop()



if __name__ == '__main__':
    _ = ChessBoard()