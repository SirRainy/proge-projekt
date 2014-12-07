__author__ = 'mihkel'
#from .ships import Ship

class GameStateMatrixElement():

    STATE_EMPTY = 'empty'
    STATE_SHIPZONE = 'shipzone'

    gameState = None
    rowNr = int
    colChar = str
    childrenStates = []
    ship = None

    def __init__(self, gameState, colChar, rowNr):
        self.childrenStates = []
        self.gameState = gameState
        self.rowNr = rowNr
        self.colChar = colChar

    def addShip(self, ship):
        if ship not in self.gameState.ships:
            self.gameState.ships.append( ship )
        self.ship = ship
        self.addChild( ship )
        ship.shipStateMatrixElements.append( self )

    def removeShip(self):
        if self.ship in self.gameState.ships:
            self.gameState.ships.remove( self.ship )
        self.ship.shipStateMatrixElements.remove(self)
        self.childrenStates.remove(self.ship)
        self.ship = None

    def getCountOfZones(self):
        return len([x for x in self.childrenStates if x==self.STATE_SHIPZONE ])

    def hasShip(self):
        #return len([x for x in self.children if isinstance(x, Ship) ])>0
        return self.ship!=None

    def isEmpty(self):
        return len(self.childrenStates)==0

    def setChildren(self, children):
        self.childrenStates = children

    def addChild(self, child):
        self.childrenStates.append(child)

    def removeChild(self, child):
        if self.childrenStates.__contains__(child):
            self.childrenStates.remove(child)

    #def setAsEmpty(self):
    #    self.setChildren([])

    def getSimplifiedElement(self):
        if self.isEmpty():
            simplifiedElement = '0'
        elif self.hasShip():
            simplifiedElement = 'S'
        elif self.STATE_SHIPZONE in self.childrenStates:
            simplifiedElement = 'Z'
        else: #todo: proper check for ship
            simplifiedElement = '.'
        return simplifiedElement



