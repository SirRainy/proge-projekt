__author__ = 'mihkel'

from .shipport import ShipPort
from .grid import Grid
from .gameState import GameState

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.graphics import *
from kivy.graphics import Color, Ellipse, Line
from kivy.core.text import Label as CoreLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty
import random

#---------------------------------------------------------------------------------------------------
#       MainMenuView
#---------------------------------------------------------------------------------------------------
class MainMenuView( Widget ):
    game = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def draw(self):
        self.addStartButtonLabel()
        self.game = self.parent.game

    def addStartButtonLabel(self):
        randomlabel = Label(text='[ref=startGame]START[/ref]', markup=True)
        self.add_widget( randomlabel )
        def drawGameScreenView( object, value ):
            self.game.startGame()
        randomlabel.bind(on_ref_press=drawGameScreenView)

#---------------------------------------------------------------------------------------------------
#       GameScreenView
#---------------------------------------------------------------------------------------------------
class GameScreenView( BoxLayout ):
    game = None
    #shipPort = None
    #smallerGrid = None
    #mainGrid = None
    startingButton = None
    leftPane = None
    rightPane = None

    def __init__(self, **kwargs):
        super().__init__(cols=2,**kwargs)
        self.leftPane = BoxLayout()
        self.rightPane = BoxLayout(orientation='vertical')
        self.add_widget(self.leftPane)
        self.add_widget(self.rightPane)
        #self.size_hint = (1,1)
        #self.size = (900,600)

    def draw(self):
        self.game = self.parent.game
        #self.game = self.get_root_window().children[0]
        self.size = self.parent.size
        self.drawShipPlacementArea()
        self.drawShipPort()

    def addWidgetToGameScreenViewLeft(self, widgetToAdd):
        #self.add_widget( widgetToAdd )
        self.leftPane.add_widget( widgetToAdd )

    def addWidgetToGameScreenViewRight(self, widgetToAdd):
        #self.add_widget( widgetToAdd )
        self.rightPane.add_widget( widgetToAdd )

    def removeWidgetFromGameScreenView(self, widgetToRemove):
        if widgetToRemove in self.rightPane.children:
            self.rightPane.remove_widget( widgetToRemove )
        if widgetToRemove in self.leftPane.children:
            self.leftPane.remove_widget( widgetToRemove )

    def drawShipPlacementArea(self):
        self.game.shipPlacementArea = GridArea()
        self.game.activeArea = self.game.shipPlacementArea
        self.addWidgetToGameScreenViewLeft( self.game.shipPlacementArea )
        self.game.shipPlacementArea.draw(1)

    def drawOwnShipGridArea(self):
        self.game.ownShipGridArea = GridArea()
        self.addWidgetToGameScreenViewRight( self.game.ownShipGridArea )
        self.game.ownShipGridArea.draw(2)

    def drawEnemyShipGridArea(self):
        self.game.enemyShipGridArea = GridArea()
        self.addWidgetToGameScreenViewLeft( self.game.enemyShipGridArea )
        self.game.enemyShipGridArea.draw(1)

    def drawShipPort(self):
        self.game.shipPort = ShipPort(game=self.game)
        self.addWidgetToGameScreenViewRight( self.game.shipPort )
        self.game.shipPort.draw()

    def drawStartingButton(self):
        self.startingButton = Button(text='ALUSTA MÄNGU!')
        self.startingButton.bind(on_press=self.game.startBattle)
        self.addWidgetToGameScreenViewRight( self.startingButton )

    def drawGameOverText(self, youWon):
        self.rightPane.clear_widgets()
        print(youWon)
        if youWon == True:
            text = 'MÄNG LÄBI !!! VÕITSID !'
        else:
            text = "MÄNG LÄBI !!! Kaotasid.... :'("
        self.addWidgetToGameScreenViewRight( Label(font_size='40sp',text=text) )

    def removeShipPort(self):
        self.removeWidgetFromGameScreenView( self.game.shipPort )

#---------------------------------------------------------------------------------------------------
#       BattleArea
#---------------------------------------------------------------------------------------------------
class GridArea( RelativeLayout ):
    grid = None

    def __init__(self, **kwargs):
        self.ships = []
        super().__init__(**kwargs)

    def draw(self, sizeMultiplier):
        self.drawGrid( sizeMultiplier )

    def drawGrid(self, sizeMultiplier):
        self.grid = Grid(sizeMultiplier=sizeMultiplier)
        #self.parent.mainGrid = self.mainGrid
        self.add_widget( self.grid )
        self.grid.draw()
