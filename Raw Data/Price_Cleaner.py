import arcpy

def price_cleaner(feature_class, input_field, output_field):

    try:
        # checks if the field name the user puts in is already a field in the table
        if arcpy.ListFields(feature_class, output_field):
            print(f"Field '{output_field}' already exists in the feature class, pick a different name.")
            return

        # creates the new double field that the prices will be put into
        print(f"Adding field '{output_field}' as a double")
        arcpy.management.AddField(
            in_table=feature_class,
            field_name=output_field,
            field_type="DOUBLE",
            field_precision=10,  
            field_scale=2         # sets to 2 decimal places
        )
        print("Double Field Added")


        # This is the code that defines the function for actually cleaning the price numbers.

        code_block_cleaner = """
def clean_price(price_string):

    if price_string is None:
        return 0.0
    
    price_string = str(price_string)
    
    cleaned_string = price_string.replace('$', '').replace(',', '').replace('+', '')
    
    try:
        return float(cleaned_string)

    except ValueError:
        return 0.0
"""
        
        # calculates new field vaues
        expression = f"clean_price(!{input_field}!)"
        
        print("Starting calculation")

        arcpy.management.CalculateField(
            in_table = feature_class,
            field = output_field,
            expression = expression,
            expression_type = "PYTHON3",
            code_block_cleaner = code_block_cleaner
        )
        print("Done")
        
    except arcpy.ExecuteError:
        print("Error with Arcpy")

        
    except Exception as e:
        print("Something went wrong")


if __name__ == '__main__':

    # If anyone else uses this to change fields in a shapefile make sure you change the variables below to match what you need. This is the code block that actually does the stuff

    # The shapefile being worked on
    input_feature_class = r"C:\Users\cthbi\OneDrive\Documents\GEOG 392\Project_Stuff\apartments_final - Copy\apartments_final.shp"
    
    # The field that has the prices that are currently in a string
    source_price_field = "USER_price" 
    
    # The name of the field this code will create as a double with the prices listed with no special characters.
    new_double_field = "PRICE_num"
    

    print("Starting process")

    price_cleaner(input_feature_class, source_price_field, new_double_field)
