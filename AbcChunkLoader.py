#--------------------------------------------------------#
#                                                        #
#                                                        #
#                                                        #
#      UI designed to load specificed Geometry files     #
#        into maya and keyframe then for the frames      #
#          needed which is specificed by the user.       #
#                                                        #
#              Created on August, 15, 2015               #
#              by: Jordan Alphonso                       #
#              email: jordanalphonso1@yahoo.com          #
#                                                        #
#                                                        #
#                                                        #
#--------------------------------------------------------#


import maya.cmds as cmds
import sys

class ChunkLoader():

    def __init__( self ):

        #empty dictionary to store local variable
        self.widgets = {}

        #call up the main window
        self.mainWindow()


    def mainWindow( self, *args ):

        #if window exists, then delete it
        if cmds.window( "mainWin", exists=True ):
            cmds.deleteUI( "mainWin" )

        #window GUI
        self.widgets[ "mWindow" ] = cmds.window( "mainWin", title='Load Alembic Chunks', width=500, height=230, mxb=False, mnb=False, sizeable=False )
        self.widgets[ "mLayout" ]  = cmds.columnLayout(columnOffset=( 'left', 20 ))

        cmds.separator( h=10 )
        cmds.text( label='Please select the folder of the alembic chunks you want to import.', parent=self.widgets[ "mLayout" ], align='center', w=500 )
        cmds.separator( h=5 )

        cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 460),(2, 50)], co=(2, 'left', 10) )
        self.widgets[ "folderField" ] = cmds.textField( editable=False )
        cmds.button( label="+", c=self.browseButton )

        cmds.columnLayout()
        cmds.separator( h=10 )
        cmds.text( label='Please enter the first chunk number.', align='center', w=500 )
        intLayout = cmds.columnLayout( columnOffset=('left', 200) )
        self.widgets[ "firstChunkField" ] = cmds.intField( editable=True, parent=intLayout )

        cmds.columnLayout( parent=self.widgets[ "mLayout" ] )
        cmds.text( label='Please enter the last chunk number.', align='center', w=500)
        cmds.columnLayout( columnOffset=('left', 200) )
        self.widgets[ "lastChunkField" ] = cmds.intField( editable=True )

        cmds.columnLayout()
        cmds.separator( h=5, parent=self.widgets[ "mLayout" ] )
        self.widgets[ "loadButton" ] = cmds.button( label='Load', command=self.loadChunks, w=500, parent=self.widgets[ "mLayout" ] )
        cmds.separator( h=5, parent=self.widgets[ "mLayout" ] )
        self.widgets[ "closeButton" ] = cmds.button( label='Close', command=self.cancelButton, w=500, parent=self.widgets[ "mLayout" ] )


        cmds.showWindow( self.widgets[ "mWindow" ] )



    def loadChunks( self, *args ):

        #grab folder path
        folderPath = cmds.textField( self.widgets[ "folderField" ], query=True, text=True )

        #grab first chunk num
        chunkNum = cmds.intField( self.widgets[ "firstChunkField" ], query=True, value=True )

        #grab last chunk num
        lastChunknum = cmds.intField( self.widgets[ "lastChunkField" ], query=True, value=True )

        #create digit padding for numbers
        n = '%04d' %chunkNum

        #add folder to chunk name
        chunkPath = ( folderPath + 'bifrostMesh1_chunk' + str(n) + '.abc' )

        #append chunk to chunkNum
        chunkName = ( 'chunk' + str(n) )

        #import first chunk
        cmds.AbcImport( chunkPath )
        cmds.rename( "bifrostMesh1", chunkName )
        cmds.select( chunkName )
        cmds.currentTime( (int(chunkNum) - 1) )
        cmds.setAttr( (chunkName + ".v"), 0 )
        cmds.setKeyframe( (chunkName + ".v") )
        cmds.currentTime( chunkNum )
        cmds.setAttr( (chunkName + ".v"), 1 )
        cmds.setKeyframe( (chunkName + ".v") )
        cmds.currentTime( (int(chunkNum) + 9) )
        cmds.setAttr( (chunkName + ".v"), 1 )
        cmds.setKeyframe( (chunkName + ".v") )
        cmds.currentTime( (int(chunkNum) + 10) )
        cmds.setAttr( (chunkName + ".v"), 0 )
        cmds.setKeyframe( (chunkName + ".v") )

        #print successful load
        sys.stderr.write( 'bifrostMesh1_' + chunkName + '.abc has been successfully loaded.' )

        #loop through all chunks
        while chunkNum < lastChunknum:

            #counter
            chunkNum = (chunkNum + 10)

            #create digit padding for numbers
            c = '%04d' % chunkNum

            #append chunk to chunkNum
            countName = ( 'chunk' + str(c) )

        	#add folder to chunk name
            countPath = (str(folderPath)+"bifrostMesh1_chunk"+str(c)+".abc")

            #import rest of chunks
            cmds.AbcImport( countPath )
            cmds.rename( "bifrostMesh1", countName )
            cmds.select( countName )
            cmds.currentTime( (int(chunkNum) - 1) )
            cmds.setAttr( (countName + ".v"), 0 )
            cmds.setKeyframe( (countName + ".v") )
            cmds.currentTime( chunkNum )
            cmds.setAttr( (countName + ".v"), 1 )
            cmds.setKeyframe( (countName + ".v") )
            cmds.currentTime( (int(chunkNum) + 9) )
            cmds.setAttr( (countName + ".v"), 1 )
            cmds.setKeyframe( (countName + ".v") )
            cmds.currentTime( (int(chunkNum) + 10) )
            cmds.setAttr( (countName + ".v"), 0 )
            cmds.setKeyframe( (countName + ".v") )

            #print successful load
            sys.stderr.write( 'bifrostMesh1_' + countName + '.abc has been successfully loaded.' )



        #close window when finished
        cmds.deleteUI( self.widgets[ "mWindow" ] )

    def browseButton( self, *args ):

        Filefilter = "*.*"
        folder = cmds.fileDialog2(fm=3, cap="Select Folder", ff=Filefilter, okc="Select")

        cmds.textField( self.widgets[ "folderField" ], edit=True, text=folder[0]+"/" )


    def cancelButton( self, *args ):


        cmds.deleteUI( self.widgets[ "mWindow" ] )


