# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct 21 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class SimulationPanel
###########################################################################

class SimulationPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		main_fg_sizer = wx.FlexGridSizer( 2, 0, 0, 0 )
		main_fg_sizer.AddGrowableCol( 0 )
		main_fg_sizer.AddGrowableRow( 1 )
		main_fg_sizer.SetFlexibleDirection( wx.BOTH )
		main_fg_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		control_b_sizer = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bpButton10 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		control_b_sizer.Add( self.m_bpButton10, 0, wx.ALL, 5 )
		
		self.m_bpButton11 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		control_b_sizer.Add( self.m_bpButton11, 0, wx.ALL, 5 )
		
		self.m_bpButton12 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		control_b_sizer.Add( self.m_bpButton12, 0, wx.ALL, 5 )
		
		
		main_fg_sizer.Add( control_b_sizer, 1, wx.EXPAND, 5 )
		
		self.m_epithelium_display = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		main_fg_sizer.Add( self.m_epithelium_display, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( main_fg_sizer )
		self.Layout()
	
	def __del__( self ):
		pass
	

