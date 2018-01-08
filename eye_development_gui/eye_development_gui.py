# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Dec 21 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from display_2d.EpitheliumDisplayPanel import EpitheliumDisplayPanel
from eye_development_gui.SimulationPanelWrapper import SimulationPanelWrapper
import wx
import wx.xrc

###########################################################################
## Class MainFrameBase
###########################################################################

class MainFrameBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Eye Development Model", pos = wx.DefaultPosition, size = wx.Size( 719,328 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.view_selection_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.epithelium_generation_panel = wx.Panel( self.view_selection_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_simulation_panel = wx.Panel( self.epithelium_generation_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer31 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = EpitheliumDisplayPanel( self.m_simulation_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer31.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_simulation_panel.SetSizer( bSizer31 )
		self.m_simulation_panel.Layout()
		bSizer31.Fit( self.m_simulation_panel )
		fgSizer3.Add( self.m_simulation_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableRow( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer4.SetMinSize( wx.Size( 100,100 ) ) 
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer6.SetMinSize( wx.Size( 20,20 ) ) 
		self.ep_gen_create_button = wx.Button( self.epithelium_generation_panel, wx.ID_ANY, u"Create", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.ep_gen_create_button, 0, wx.ALL, 5 )
		
		self.ep_gen_save_button = wx.Button( self.epithelium_generation_panel, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.ep_gen_save_button, 0, wx.ALL, 5 )
		
		self.ep_gen_save_as_button = wx.Button( self.epithelium_generation_panel, wx.ID_ANY, u"Save As", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.ep_gen_save_as_button, 0, wx.ALL, 5 )
		
		self.ep_gen_load_button = wx.Button( self.epithelium_generation_panel, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.ep_gen_load_button, 0, wx.ALL, 5 )
		
		
		fgSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		self.epithelium_options_scrolled_window3 = wx.ScrolledWindow( self.epithelium_generation_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.epithelium_options_scrolled_window3.SetScrollRate( 5, 5 )
		epithelium_options_grid = wx.GridSizer( 0, 2, 0, 0 )
		
		self.min_cells_static_text = wx.StaticText( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"Min Cell Count", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.min_cells_static_text.Wrap( -1 )
		epithelium_options_grid.Add( self.min_cells_static_text, 0, wx.ALL, 5 )
		
		self.min_cell_count_text_ctrl = wx.TextCtrl( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
		epithelium_options_grid.Add( self.min_cell_count_text_ctrl, 0, wx.ALL, 5 )
		
		self.min_cell_size_static_text = wx.StaticText( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"Min Cell Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.min_cell_size_static_text.Wrap( -1 )
		epithelium_options_grid.Add( self.min_cell_size_static_text, 0, wx.ALL, 5 )
		
		self.min_cell_size_text_ctrl = wx.TextCtrl( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"50", wx.DefaultPosition, wx.DefaultSize, 0 )
		epithelium_options_grid.Add( self.min_cell_size_text_ctrl, 0, wx.ALL, 5 )
		
		self.max_cell_size_static_text = wx.StaticText( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"Max Cell Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.max_cell_size_static_text.Wrap( -1 )
		epithelium_options_grid.Add( self.max_cell_size_static_text, 0, wx.ALL, 5 )
		
		self.max_cell_size_text_ctrl = wx.TextCtrl( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
		epithelium_options_grid.Add( self.max_cell_size_text_ctrl, 0, wx.ALL, 5 )
		
		
		self.epithelium_options_scrolled_window3.SetSizer( epithelium_options_grid )
		self.epithelium_options_scrolled_window3.Layout()
		epithelium_options_grid.Fit( self.epithelium_options_scrolled_window3 )
		fgSizer4.Add( self.epithelium_options_scrolled_window3, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		fgSizer3.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		
		self.epithelium_generation_panel.SetSizer( fgSizer3 )
		self.epithelium_generation_panel.Layout()
		fgSizer3.Fit( self.epithelium_generation_panel )
		self.view_selection_notebook.AddPage( self.epithelium_generation_panel, u"Epithelium Generation", True )
		self.m_panel4 = wx.Panel( self.view_selection_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel4.Enable( False )
		
		fgSizer31 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer31.AddGrowableCol( 0 )
		fgSizer31.AddGrowableRow( 0 )
		fgSizer31.SetFlexibleDirection( wx.BOTH )
		fgSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer41 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer41.AddGrowableCol( 0 )
		fgSizer41.AddGrowableRow( 0 )
		fgSizer41.SetFlexibleDirection( wx.BOTH )
		fgSizer41.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_panel51 = SimulationPanelWrapper( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer41.Add( self.m_panel51, 1, wx.EXPAND |wx.ALL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel4, wx.ID_ANY, u"Simulation Options" ), wx.VERTICAL )
		
		self.m_scrolledWindow4 = wx.ScrolledWindow( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow4.SetScrollRate( 5, 5 )
		self.m_scrolledWindow4.SetMinSize( wx.Size( 350,-1 ) )
		
		gSizer6 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText85 = wx.StaticText( self.m_scrolledWindow4, wx.ID_ANY, u"Sample Input", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText85.Wrap( -1 )
		gSizer6.Add( self.m_staticText85, 0, wx.ALL, 5 )
		
		self.m_textCtrl14 = wx.TextCtrl( self.m_scrolledWindow4, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_textCtrl14, 0, wx.ALL, 5 )
		
		self.m_staticText86 = wx.StaticText( self.m_scrolledWindow4, wx.ID_ANY, u"Sample Input", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText86.Wrap( -1 )
		gSizer6.Add( self.m_staticText86, 0, wx.ALL, 5 )
		
		self.m_textCtrl15 = wx.TextCtrl( self.m_scrolledWindow4, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_textCtrl15, 0, wx.ALL, 5 )
		
		self.m_staticText87 = wx.StaticText( self.m_scrolledWindow4, wx.ID_ANY, u"Sample Input", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText87.Wrap( -1 )
		gSizer6.Add( self.m_staticText87, 0, wx.ALL, 5 )
		
		self.m_textCtrl16 = wx.TextCtrl( self.m_scrolledWindow4, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_textCtrl16, 0, wx.ALL, 5 )
		
		
		self.m_scrolledWindow4.SetSizer( gSizer6 )
		self.m_scrolledWindow4.Layout()
		gSizer6.Fit( self.m_scrolledWindow4 )
		sbSizer2.Add( self.m_scrolledWindow4, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		fgSizer41.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		
		fgSizer31.Add( fgSizer41, 1, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer31.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		gSizer2 = wx.GridSizer( 0, 4, 0, 0 )
		
		self.m_staticText10 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Cell Count", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gSizer2.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.m_textCtrl4 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl4.Enable( False )
		
		gSizer2.Add( self.m_textCtrl4, 0, wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Avg. Cell Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gSizer2.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.m_textCtrl5 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl5.Enable( False )
		
		gSizer2.Add( self.m_textCtrl5, 0, wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"R8 Count", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		gSizer2.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.m_textCtrl6 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl6.Enable( False )
		
		gSizer2.Add( self.m_textCtrl6, 0, wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"% R8", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		gSizer2.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.m_textCtrl7 = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl7.Enable( False )
		
		gSizer2.Add( self.m_textCtrl7, 0, wx.ALL, 5 )
		
		
		fgSizer31.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( fgSizer31 )
		self.m_panel4.Layout()
		fgSizer31.Fit( self.m_panel4 )
		self.view_selection_notebook.AddPage( self.m_panel4, u"Simulation Overview", False )
		self.m_panel5 = SimulationPanelWrapper( self.view_selection_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel5.Enable( False )
		
		self.view_selection_notebook.AddPage( self.m_panel5, u"Simulation", False )
		
		bSizer3.Add( self.view_selection_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ep_gen_create_button.Bind( wx.EVT_BUTTON, self.ep_gen_create_callback )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def ep_gen_create_callback( self, event ):
		event.Skip()
	

