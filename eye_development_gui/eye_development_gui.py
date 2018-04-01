# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct 21 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from display_2d.EpitheliumDisplayPanel import EpitheliumDisplayPanel
from eye_development_gui.SimulationPanel import SimulationPanel
import wx
import wx.xrc

###########################################################################
## Class MainFrameBase
###########################################################################

class MainFrameBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Eye Development Model", pos = wx.DefaultPosition, size = wx.Size( 719,403 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.view_selection_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.epithelium_generation_panel = wx.Panel( self.view_selection_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_epithelium_gen_display_container_panel = wx.Panel( self.epithelium_generation_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer31 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_epithelium_gen_display_panel = EpitheliumDisplayPanel( self.m_epithelium_gen_display_container_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer31.Add( self.m_epithelium_gen_display_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_epithelium_gen_display_container_panel.SetSizer( bSizer31 )
		self.m_epithelium_gen_display_container_panel.Layout()
		bSizer31.Fit( self.m_epithelium_gen_display_container_panel )
		fgSizer3.Add( self.m_epithelium_gen_display_container_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
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
		self.min_cells_static_text.SetToolTip( u"The number of cells that will Initially be generated for the epithelium." )
		
		epithelium_options_grid.Add( self.min_cells_static_text, 0, wx.ALL, 5 )
		
		self.min_cell_count_text_ctrl = wx.TextCtrl( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.min_cell_count_text_ctrl.SetToolTip( u"The number of cells that will Initially be generated for the epithelium." )
		
		epithelium_options_grid.Add( self.min_cell_count_text_ctrl, 0, wx.ALL, 5 )
		
		self.avg_cell_size_static_text = wx.StaticText( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"Average Cell Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.avg_cell_size_static_text.Wrap( -1 )
		self.avg_cell_size_static_text.SetToolTip( u"All initially generated cells will have a radius of Average Cell Size +/- Cell Size Variance." )
		
		epithelium_options_grid.Add( self.avg_cell_size_static_text, 0, wx.ALL, 5 )
		
		self.avg_cell_size_text_ctrl = wx.TextCtrl( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.avg_cell_size_text_ctrl.SetToolTip( u"All initially generated cells will have a radius of Average Cell Size +/- Cell Size Variance." )
		
		epithelium_options_grid.Add( self.avg_cell_size_text_ctrl, 0, wx.ALL, 5 )
		
		self.cell_size_variance_static_text = wx.StaticText( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"Cell Size Variance", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cell_size_variance_static_text.Wrap( -1 )
		self.cell_size_variance_static_text.SetToolTip( u"All initially generated cells will have a radius of Average Cell Size +/- Cell Size Variance." )
		
		epithelium_options_grid.Add( self.cell_size_variance_static_text, 0, wx.ALL, 5 )
		
		self.cell_size_variance_text_ctrl = wx.TextCtrl( self.epithelium_options_scrolled_window3, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cell_size_variance_text_ctrl.SetToolTip( u"All initially generated cells will have a radius of Average Cell Size +/- Cell Size Variance." )
		
		epithelium_options_grid.Add( self.cell_size_variance_text_ctrl, 0, wx.ALL, 5 )
		
		
		self.epithelium_options_scrolled_window3.SetSizer( epithelium_options_grid )
		self.epithelium_options_scrolled_window3.Layout()
		epithelium_options_grid.Fit( self.epithelium_options_scrolled_window3 )
		fgSizer4.Add( self.epithelium_options_scrolled_window3, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		fgSizer3.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		
		self.epithelium_generation_panel.SetSizer( fgSizer3 )
		self.epithelium_generation_panel.Layout()
		fgSizer3.Fit( self.epithelium_generation_panel )
		self.view_selection_notebook.AddPage( self.epithelium_generation_panel, u"Epithelium Generation", True )
		self.m_simulation_overview_panel = wx.Panel( self.view_selection_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer31 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer31.AddGrowableCol( 0 )
		fgSizer31.AddGrowableRow( 0 )
		fgSizer31.SetFlexibleDirection( wx.BOTH )
		fgSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer41 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer41.AddGrowableCol( 0 )
		fgSizer41.AddGrowableRow( 0 )
		fgSizer41.SetFlexibleDirection( wx.VERTICAL )
		fgSizer41.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_sim_overview_display_panel = SimulationPanel( self.m_simulation_overview_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer41.Add( self.m_sim_overview_display_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer5 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer5.AddGrowableCol( 0 )
		fgSizer5.AddGrowableRow( 2 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer5.SetMinSize( wx.Size( 300,-1 ) ) 
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_sim_overview_save_button = wx.Button( self.m_simulation_overview_panel, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_sim_overview_save_button, 0, wx.ALL, 5 )
		
		self.m_sim_overview_save_as_button = wx.Button( self.m_simulation_overview_panel, wx.ID_ANY, u"Save As", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_sim_overview_save_as_button, 0, wx.ALL, 5 )
		
		self.m_sim_overview_load_button = wx.Button( self.m_simulation_overview_panel, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_sim_overview_load_button, 0, wx.ALL, 5 )
		
		
		fgSizer5.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		sim_overview_sim_options_box_sizer = wx.StaticBoxSizer( wx.StaticBox( self.m_simulation_overview_panel, wx.ID_ANY, u"Simulation Options" ), wx.VERTICAL )
		
		sim_overview_sim_options_box_sizer.SetMinSize( wx.Size( -1,80 ) ) 
		self.m_sim_overview_sim_options_scrolled_window = wx.ScrolledWindow( sim_overview_sim_options_box_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_sim_overview_sim_options_scrolled_window.SetScrollRate( 5, 5 )
		gSizer4 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.cell_max_size_static_text = wx.StaticText( self.m_sim_overview_sim_options_scrolled_window, wx.ID_ANY, u"Cell Max Size", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cell_max_size_static_text.Wrap( -1 )
		self.cell_max_size_static_text.SetToolTip( u"All initially generated cells will be unable to grow beyond this size." )
		
		gSizer4.Add( self.cell_max_size_static_text, 0, wx.ALL, 5 )
		
		self.cell_max_size_text_ctrl = wx.TextCtrl( self.m_sim_overview_sim_options_scrolled_window, wx.ID_ANY, u"25", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cell_max_size_text_ctrl.SetToolTip( u"All initially generated cells will be unable to grow beyond this size." )
		
		gSizer4.Add( self.cell_max_size_text_ctrl, 0, wx.ALL, 5 )
		
		self.cell_growth_rate_static_text = wx.StaticText( self.m_sim_overview_sim_options_scrolled_window, wx.ID_ANY, u"Cell Growth Rate", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cell_growth_rate_static_text.Wrap( -1 )
		self.cell_growth_rate_static_text.SetToolTip( u"All initially generated cells will grow by this much every simulation cycle if they are experiencing growth." )
		
		gSizer4.Add( self.cell_growth_rate_static_text, 0, wx.ALL, 5 )
		
		self.cell_growth_rate_text_ctrl = wx.TextCtrl( self.m_sim_overview_sim_options_scrolled_window, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.cell_growth_rate_text_ctrl.SetToolTip( u"All initially generated cells will grow by this much every simulation cycle if they are experiencing growth." )
		
		gSizer4.Add( self.cell_growth_rate_text_ctrl, 0, wx.ALL, 5 )
		
		self.furrow_velocity_static_text = wx.StaticText( self.m_sim_overview_sim_options_scrolled_window, wx.ID_ANY, u"Furrow Velocity", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.furrow_velocity_static_text.Wrap( -1 )
		self.furrow_velocity_static_text.SetToolTip( u"The furrow will move by this much every cycle of the simulation." )
		
		gSizer4.Add( self.furrow_velocity_static_text, 0, wx.ALL, 5 )
		
		self.furrow_velocity_text_ctrl = wx.TextCtrl( self.m_sim_overview_sim_options_scrolled_window, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.furrow_velocity_text_ctrl.SetToolTip( u"The furrow will move by this much every cycle of the simulation." )
		
		gSizer4.Add( self.furrow_velocity_text_ctrl, 0, wx.ALL, 5 )
		
		
		self.m_sim_overview_sim_options_scrolled_window.SetSizer( gSizer4 )
		self.m_sim_overview_sim_options_scrolled_window.Layout()
		gSizer4.Fit( self.m_sim_overview_sim_options_scrolled_window )
		sim_overview_sim_options_box_sizer.Add( self.m_sim_overview_sim_options_scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		fgSizer5.Add( sim_overview_sim_options_box_sizer, 1, wx.EXPAND, 5 )
		
		sim_overview_specialization_options_box_sizer = wx.StaticBoxSizer( wx.StaticBox( self.m_simulation_overview_panel, wx.ID_ANY, u"Specialization Options" ), wx.VERTICAL )
		
		self.m_sim_overview_spec_options_scrolled_window = wx.ScrolledWindow( sim_overview_specialization_options_box_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_sim_overview_spec_options_scrolled_window.SetScrollRate( 5, 5 )
		sim_overview_specialization_options_box_sizer.Add( self.m_sim_overview_spec_options_scrolled_window, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		fgSizer5.Add( sim_overview_specialization_options_box_sizer, 1, wx.EXPAND, 5 )
		
		
		fgSizer41.Add( fgSizer5, 1, wx.EXPAND|wx.FIXED_MINSIZE, 5 )
		
		
		fgSizer31.Add( fgSizer41, 1, wx.EXPAND, 5 )
		
		
		self.m_simulation_overview_panel.SetSizer( fgSizer31 )
		self.m_simulation_overview_panel.Layout()
		fgSizer31.Fit( self.m_simulation_overview_panel )
		self.view_selection_notebook.AddPage( self.m_simulation_overview_panel, u"Simulation Overview", False )
		self.m_simulation_display_panel = SimulationPanel( self.view_selection_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.view_selection_notebook.AddPage( self.m_simulation_display_panel, u"Simulation", False )
		
		bSizer3.Add( self.view_selection_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_SIZE, self.on_size )
		self.ep_gen_create_button.Bind( wx.EVT_BUTTON, self.ep_gen_create_callback )
		self.ep_gen_save_button.Bind( wx.EVT_BUTTON, self.on_epithelium_save )
		self.ep_gen_save_as_button.Bind( wx.EVT_BUTTON, self.on_epithelium_save_as )
		self.ep_gen_load_button.Bind( wx.EVT_BUTTON, self.on_epithelium_load )
		self.min_cell_count_text_ctrl.Bind( wx.EVT_TEXT, self.on_ep_gen_user_input )
		self.avg_cell_size_text_ctrl.Bind( wx.EVT_TEXT, self.on_ep_gen_user_input )
		self.cell_size_variance_text_ctrl.Bind( wx.EVT_TEXT, self.on_ep_gen_user_input )
		self.m_sim_overview_save_button.Bind( wx.EVT_BUTTON, self.on_sim_overview_save )
		self.m_sim_overview_save_as_button.Bind( wx.EVT_BUTTON, self.on_sim_overview_save_as )
		self.m_sim_overview_load_button.Bind( wx.EVT_BUTTON, self.on_sim_overview_load )
		self.cell_max_size_text_ctrl.Bind( wx.EVT_TEXT, self.on_sim_overview_user_input )
		self.cell_growth_rate_text_ctrl.Bind( wx.EVT_TEXT, self.on_sim_overview_user_input )
		self.furrow_velocity_text_ctrl.Bind( wx.EVT_TEXT, self.on_sim_overview_user_input )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_size( self, event ):
		event.Skip()
	
	def ep_gen_create_callback( self, event ):
		event.Skip()
	
	def on_epithelium_save( self, event ):
		event.Skip()
	
	def on_epithelium_save_as( self, event ):
		event.Skip()
	
	def on_epithelium_load( self, event ):
		event.Skip()
	
	def on_ep_gen_user_input( self, event ):
		event.Skip()
	
	
	
	def on_sim_overview_save( self, event ):
		event.Skip()
	
	def on_sim_overview_save_as( self, event ):
		event.Skip()
	
	def on_sim_overview_load( self, event ):
		event.Skip()
	
	def on_sim_overview_user_input( self, event ):
		event.Skip()
	
	
	

