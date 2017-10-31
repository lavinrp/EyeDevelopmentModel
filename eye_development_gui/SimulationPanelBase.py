# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct 21 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from display_2d.EpitheliumDisplayPanel import EpitheliumDisplayPanel
import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class SimulationPanel
###########################################################################

class SimulationPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 197,181 ), style = wx.TAB_TRAVERSAL )
		
		main_fg_sizer = wx.FlexGridSizer( 2, 0, 0, 0 )
		main_fg_sizer.AddGrowableCol( 0 )
		main_fg_sizer.AddGrowableRow( 1 )
		main_fg_sizer.SetFlexibleDirection( wx.BOTH )
		main_fg_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		control_b_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button4 = wx.Button( self, wx.ID_ANY, _(u"Start"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		control_b_sizer.Add( self.m_button4, 0, wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self, wx.ID_ANY, _(u"Pause"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		control_b_sizer.Add( self.m_button5, 0, wx.ALL, 5 )
		
		self.m_button6 = wx.Button( self, wx.ID_ANY, _(u"Stop"), wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		control_b_sizer.Add( self.m_button6, 0, wx.ALL, 5 )
		
		
		main_fg_sizer.Add( control_b_sizer, 1, wx.EXPAND, 5 )
		
		self.m_epithelium_display = EpitheliumDisplayPanel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		main_fg_sizer.Add( self.m_epithelium_display, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( main_fg_sizer )
		self.Layout()
	
	def __del__( self ):
		pass
	

