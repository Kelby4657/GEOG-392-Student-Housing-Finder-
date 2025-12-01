import arcpy
import os

# --- INPUTS ---
csv_path = r"C:\Users\lwil4_fz9hmxa\HousingProject\apartments.csv"
gdb_path = r"C:\Users\lwil4_fz9hmxa\HousingProject\Housing.gdb"
out_fc_name = "apartments_geocoded_final"

# ArcGIS World Geocoding Service 
locator = r"https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer"

arcpy.env.overwriteOutput = True

# --- Ensure GDB Exists ---
if not arcpy.Exists(gdb_path):
    folder = os.path.dirname(gdb_path)
    gdbname = os.path.basename(gdb_path)
    arcpy.management.CreateFileGDB(folder, gdbname)

out_fc = os.path.join(gdb_path, out_fc_name)

# --- Address field mapping ---
# "SingleLine" = locator input
# "address"    = CSV address
in_address_fields = "SingleLine address VISIBLE NONE"

print("Geocoding addresses...")
try:
    arcpy.geocoding.GeocodeAddresses(
        in_table=csv_path,
        address_locator=locator,
        in_address_fields=in_address_fields,
        out_feature_class=out_fc
    )

    print("Geocoding complete!")
    print("Output feature class:", out_fc)

except Exception:
    print("Geocoding failed.")
    print(arcpy.GetMessages())
    raise
