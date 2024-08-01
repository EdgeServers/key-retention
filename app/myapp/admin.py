from django.contrib import admin
from django.http import HttpResponse
import csv
from io import StringIO
from .models import Driver, ParkingLocation, KeyHanger
from django import forms
from django.core.files.storage import default_storage

# Custom form for CSV upload
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

def export_as_csv(modeladmin, request, queryset):
    """
    Admin action to export selected objects to a CSV file.
    """
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name_plural}.csv'
    writer = csv.writer(response)

    # Write the header row
    writer.writerow([field.verbose_name for field in opts.get_fields()])

    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in opts.get_fields()])

    return response

def import_from_csv(modeladmin, request, queryset):
    """
    Admin action to import objects from a CSV file.
    """
    if 'csv_file' in request.FILES:
        csv_file = request.FILES['csv_file']
        if csv_file.name.endswith('.csv'):
            data_set = csv_file.read().decode('utf-8')
            io_string = StringIO(data_set)
            reader = csv.reader(io_string)
            next(reader)  # Skip header row

            for row in reader:
                # Process each row (update this part according to your model fields)
                try:
                    modeladmin.model.objects.create(
                        name=row[0],  # Update field names and indices as needed
                        truck_rego_number=row[1],
                        key_hanger_number=KeyHanger.objects.get(hanger_number=row[2]),  # Example, adjust as needed
                        parking_location=ParkingLocation.objects.get(name=row[3]),  # Example, adjust as needed
                        arrival_time=row[4],
                        departure_time=row[5],
                    )
                except Exception as e:
                    modeladmin.message_user(request, f'Error importing row: {row}. Error: {e}')
                    continue

            modeladmin.message_user(request, "CSV file has been imported successfully.")
        else:
            modeladmin.message_user(request, "Please upload a valid CSV file.")

    return redirect('admin:index')

# Custom Admin Classes
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'truck_rego_number', 'key_hanger_number', 'parking_location','rear_wheel_chocked', 'key_removed_from_ignition', 'arrival_time', 'departure_time')
    actions = [export_as_csv, import_from_csv]

class ParkingLocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [export_as_csv, import_from_csv]

class KeyHangerAdmin(admin.ModelAdmin):
    list_display = ('hanger_number', 'is_available')
    actions = [export_as_csv, import_from_csv]

admin.site.register(Driver, DriverAdmin)
admin.site.register(ParkingLocation, ParkingLocationAdmin)
admin.site.register(KeyHanger, KeyHangerAdmin)
