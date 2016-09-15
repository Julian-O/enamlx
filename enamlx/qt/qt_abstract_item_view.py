# -*- coding: utf-8 -*-
'''
Created on Aug 20, 2015

@author: jrm
'''
from atom.api import Instance
from enaml.qt.qt_control import QtControl
from enaml.qt.QtGui import QAbstractItemView,QItemSelectionModel
from enamlx.widgets.abstract_item_view import ProxyAbstractItemView

SELECTION_MODES = {
    'extended':QAbstractItemView.ExtendedSelection,
    'single':QAbstractItemView.SingleSelection,
    'contiguous':QAbstractItemView.ContiguousSelection,
    'multi':QAbstractItemView.MultiSelection,
    'none':QAbstractItemView.NoSelection,
}

SELECTION_BEHAVIORS = {
    'items':QAbstractItemView.SelectItems,
    'rows':QAbstractItemView.SelectRows,
    'columns':QAbstractItemView.SelectColumns,
}

class QtAbstractItemView(QtControl, ProxyAbstractItemView):
    widget = Instance(QAbstractItemView)
    
    #: Hold reference to selection model to PySide segfault
    selection_model = Instance(QItemSelectionModel)
    
    @property
    def model(self):
        return self.widget.model()
        
    def init_widget(self):
        super(QtAbstractItemView, self).init_widget()
        
        d = self.declaration
        
        self.set_selection_mode(d.selection_mode)
        self.set_selection_behavior(d.selection_behavior)
        self.set_alternating_row_colors(d.alternating_row_colors)
        
        self.init_signals()

    def init_signals(self):
        """ Connect signals """
        self.widget.activated.connect(self.on_item_activated)
        self.widget.clicked.connect(self.on_item_clicked)
        self.widget.doubleClicked.connect(self.on_item_double_clicked)
        self.widget.entered.connect(self.on_item_entered)
        self.widget.pressed.connect(self.on_item_pressed)
        self.widget.customContextMenuRequested.connect(self.on_custom_context_menu_requested)
        self.selection_model = self.widget.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)
    
    
    def item_at(self,index):
        if not index.isValid():
            return
        return self.model.itemAt(index)
        
    def _refresh_layout(self):
        d = self.declaration
        self.set_scroll_to_bottom(d.scroll_to_bottom)
        
    def set_selection_mode(self,mode):
        self.widget.setSelectionMode(SELECTION_MODES[mode])
        
    def set_selection_behavior(self,behavior):
        self.widget.setSelectionBehavior(SELECTION_BEHAVIORS[behavior])
        
    def set_scroll_to_bottom(self,enabled):
        if enabled:
            self.widget.scrollToBottom()
            
    def set_alternating_row_colors(self,enabled):
        self.widget.setAlternatingRowColors(enabled)
        
    def set_model(self,model):
        self.widget.setModel(model)
        
    #--------------------------------------------------------------------------
    # Widget Events
    #--------------------------------------------------------------------------

    def on_item_activated(self, index):
        item = self.item_at(index)
        if not item:
            return
        item.parent().declaration.activated()
        item.declaration.activated()
        
    def on_item_clicked(self, index):
        item = self.item_at(index)
        if not item:
            return
        item.parent().declaration.clicked()
        item.declaration.clicked()
        
    def on_item_double_clicked(self, index):
        item = self.item_at(index)
        if not item:
            return
        item.parent().declaration.double_clicked()
        item.declaration.double_clicked()
        
    def on_item_pressed(self,index):
        item = self.item_at(index)
        if not item:
            return
        item.parent().declaration.pressed()
        item.declaration.pressed()
    
    def on_item_entered(self,index):
        item = self.item_at(index)
        if not item:
            return
        item.parent().declaration.entered()
        item.declaration.entered()
    
    def on_selection_changed(self,selected,deselected):
        return
        for index in selected.indexes():
            item = self.item_at(index)
            if not item:
                continue
            d = item.declaration
            if d.selected != True:
                d.selected = True
                d.selection_changed(d.selected)

        for index in deselected.indexes():
            item = self.item_at(index)
            if not item:
                continue
            d = item.declaration
            if d.selected != False:
                d.selected = False
                d.selection_changed(d.selected)                
    
    def on_custom_context_menu_requested(self,pos):
        item = self.item_at(self.widget.indexAt(pos))
        if not item:
            return
        
        if item.menu:
            item.menu.popup()
            return
        parent = item.parent()
        if parent and parent.menu:
            parent.menu.popup()
        
            
            


                                