from django.contrib import admin

from .models import Hardware, Category, HardwareAmount, TakenHardware, TakenHardwareArchieve, Room

class HardwareAmountInline(admin.TabularInline):
    model = HardwareAmount

class TakenHardwareInline(admin.TabularInline):
    model = TakenHardware

@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'product_id', 'image_name', 'available', 'get_amount')
    
    inlines = [HardwareAmountInline, TakenHardwareInline]
    list_filter = ('category','available')
    
    fieldsets = (
        ('Main section', {
                'fields': ('name', 'category', 'available')
                }), 
        ('Information', {
                'fields':('product_id', 'image_name')
            }),
        )
    
    actions = []
    def get_actions(self, request):
        actions = super(HardwareAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
         
            
            
@admin.register(TakenHardware)
class TakenHardwareAdmin(admin.ModelAdmin):
    actions = ['overwritten_delete_selected']

    list_display = ('taker', 'hardware', 'quantity', 'date_from', 'date_to', 'room')
    
    list_filter = ['room']

    fieldsets = (
        ('Main section', {
                'fields': ('taker', 'hardware', 'quantity', 'room')
                }), 
        ('Information', {
                'fields':('description','date_to')
            }),
        )
    
    def get_actions(self, request):
        actions = super(TakenHardwareAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def overwritten_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
        
        message_bit = "Entries deleted and moved to archieve"
        
    overwritten_delete_selected.short_description = "Delete selected and move to archieve"
       
    
@admin.register(TakenHardwareArchieve)
class TakenHardwareArchieveAdmin(admin.ModelAdmin):
    actions = []
    
    def get_actions(self, request):
        actions = super(TakenHardwareArchieveAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
  
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    actions = []
    
    def get_actions(self, request):
        actions = super(CategoryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
admin.site.register(HardwareAmount)
admin.site.register(Room)