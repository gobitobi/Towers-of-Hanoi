import pygame as py
from disk import Disk

py.init()
py.font.init()
py.display.set_caption("Towers of Hanoi")

# global variables
WIDTH = 640
HEIGHT = 480
FPS = 60
PEG_MIDPOINTS = [120, 320, 520]
N_DISKS = 3

screen = py.display.set_mode((WIDTH, HEIGHT))
clock = py.time.Clock()

# game variables
allDisks = []
pointerLocation = 0
steps = 0
selectedDiskIndex = 0
isDiskSelected = False
isWin = False

def drawPegs():
    global screen
    
    # for xpos in range(40, 460+1, 200): # range(40, 460+1, 200) = [40, 240, 440]
    for xpos in PEG_MIDPOINTS:
        baseBlock = py.Rect(0, 400, 160, 20)
        baseBlock.midtop = (xpos, 400)
        
        peg = py.Rect(0, 200, 11, 200)
        peg.midtop = (xpos, 200)
        
        py.draw.rect(screen, 'black', baseBlock)
        py.draw.rect(screen, 'black', peg)
                  
def initDisks():
    global allDisks, screen # N_DISKS = 3
    
    allDisks = []
    height = 20
    posY = 397 - height
    width = N_DISKS * 23
    for i in range(N_DISKS):
        
        value = N_DISKS-i
        disk = Disk(screen, width, height, posY, value)
        
        allDisks.append(disk)
        posY -= height+3 
        width -= 23
        
def drawDisks():
    global screen, allDisks
    
    for disk in allDisks:
        disk.draw()
    return

def drawPointer():
    global screen, pointerLocation, PEG_MIDPOINTS
    
    pointerPoints = [
        (PEG_MIDPOINTS[pointerLocation]-5, 440), # bottom left corner
        (PEG_MIDPOINTS[pointerLocation]+5, 440), # bottom right corner
        (PEG_MIDPOINTS[pointerLocation], 435) # top corner
    ]
    py.draw.polygon(screen, 'red', pointerPoints)
    return

def checkWin():
    global allDisks, isWin, N_DISKS
    
    isWin = True
    for disk in allDisks:
        if disk.tower != 2: # if there is a disk NOT on last tower, isWin = False
            isWin =  False
    if isWin:
        if steps >= 10:
            print('Game Lose. Did not complete in less than 10 steps.')
        elif steps == 2**N_DISKS-1:
            print('Congratulations! You completed the game in the minimum number of steps.')
        else:
            print(f'Congratulations! You completed the game in {steps} steps.')

def resetGame():
    global allDisks, steps, pointerLocation, isDiskSelected, selectedDiskIndex, isWin
    
    allDisks = []
    steps = 0
    pointerLocation = 0
    isDiskSelected = False
    selectedDiskIndex = 0
    isWin = False
    
    initDisks()
    print('game reset!')

def renderText(text, midtop):
    global screen
    
    font = py.font.SysFont('Comic Sans MS', 30)
    text_surface = font.render(text, False, (0, 0, 0))
    font_rect = text_surface.get_rect()
    font_rect.midtop = midtop
    screen.blit(text_surface, font_rect)
    

def arrowButtonsClickHandler(key):
    global pointerLocation, isDiskSelected, selectedDiskIndex, PEG_MIDPOINTS, allDisks, steps
    
    # LEFT
    if key == py.K_LEFT:
        pointerLocation = (pointerLocation-1)%3 # 0, 1, 2
        if isDiskSelected:
            disk = allDisks[selectedDiskIndex]
            disk.rect.midtop = (PEG_MIDPOINTS[pointerLocation], 100)
            disk.tower = pointerLocation
            
    # RIGHT
    if key == py.K_RIGHT:
        pointerLocation = (pointerLocation+1)%3 # 0, 1, 2
        if isDiskSelected:
            disk = allDisks[selectedDiskIndex]
            disk.rect.midtop = (PEG_MIDPOINTS[pointerLocation], 100)
            disk.tower = pointerLocation
        
    # UP              
    if key == py.K_UP and not isDiskSelected:
        for disk in allDisks[::-1]:
            if disk.tower == pointerLocation:
                isDiskSelected = True
                selectedDiskIndex = allDisks.index(disk)
                disk.rect.midtop = (PEG_MIDPOINTS[pointerLocation], 100)
                break
                
    # DOWN
    if key == py.K_DOWN and isDiskSelected:
        for disk in allDisks[::-1]:
            if disk.tower == pointerLocation and allDisks.index(disk) != selectedDiskIndex:
                if disk.value > allDisks[selectedDiskIndex].value:
                    isDiskSelected = False
                    allDisks[selectedDiskIndex].rect.midtop = (PEG_MIDPOINTS[pointerLocation], disk.rect.top-23)
                    steps += 1
                    checkWin()
                break
        else:
            isDiskSelected = False
            allDisks[selectedDiskIndex].rect.midtop = (PEG_MIDPOINTS[pointerLocation], 400-23)
            steps += 1
            checkWin()

def endscreen(): # game over screen
    global screen, steps, isWin, N_DISKS
    
    minimumSteps = 2**N_DISKS-1
    
    if isWin:
        screen.fill('white')
        if steps > 10:
            text = 'Lose. More than 10 steps.'
            renderText(text, (320, 200))
        elif steps == minimumSteps:
            text = 'Congratulations! Perfect Game!'
            renderText(text, (320, 200))
        else:
            text = f'Kinda-Win. Completed in {steps} steps.'
            renderText(text, (320, 200))
            
        renderText('Press r to play again.', (320, 360))
        renderText('Press ESC to quit.', (320, 420))
        
        py.display.flip()


#### MAIN LOOP ####
def main():
    global screen, clock, pointerLocation, isDiskSelected, selectedDiskIndex, steps, PEG_MIDPOINTS
    
    initDisks() # initialize all N disks before game loop
    
    for xpos in range(40, 460+1, 200):
        print(xpos)
    
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            
            if event.type == py.KEYDOWN:
                arrowButtonsClickHandler(event.key)
                
                if event.key == py.K_ESCAPE:
                    running = False
                
                if event.key == py.K_r:
                    resetGame()
                
        
        screen.fill("dark gray")
        drawPegs()
        drawDisks()
        drawPointer()
        
        stepsText = f'Steps: {steps}'
        renderText(stepsText, (320, 20))
        
        endscreen()
        
        clock.tick(FPS)
        py.display.flip()



if __name__ == '__main__':
    main()
