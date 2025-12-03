import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = "Housing Filter"
        self.alias = "housing"
        self.tools = [FilterTool]

class FilterTool(object):
    def __init__(self):
        self.label = "Filter Housing"
        self.description = "Filter housing data"
        
    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="Input Housing",
            name="input_housing",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
            
        param1 = arcpy.Parameter(
            displayName="Min Price",
            name="min_price",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param1.value = 500
        
        param2 = arcpy.Parameter(
            displayName="Max Price", 
            name="max_price",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param2.value = 1000
        
        param3 = arcpy.Parameter(
            displayName="Bedrooms",
            name="bedrooms",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param3.value = 2
        
        param4 = arcpy.Parameter(
            displayName="Output",
            name="output",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")
            
        return [param0, param1, param2, param3, param4]
    
    def isLicensed(self):
        return True
        
    def updateParameters(self, parameters):
        return
        
    def updateMessages(self, parameters):
        return
    
    def execute(self, parameters, messages):
        housing = parameters[0].valueAsText
        min_price = parameters[1].value
        max_price = parameters[2].value
        bedrooms = parameters[3].value
        output = parameters[4].valueAsText
        
        arcpy.AddMessage("Starting filter...")
        arcpy.AddMessage("Min Price: " + str(min_price))
        arcpy.AddMessage("Max Price: " + str(max_price))
        arcpy.AddMessage("Bedrooms: " + str(bedrooms))
        
        # Use your specific field names
        where_clause = "USER_price >= " + str(min_price) + " AND USER_price <= " + str(max_price) + " AND USER_Beds = " + str(int(bedrooms))
        
        arcpy.AddMessage("Filter: " + where_clause)
        
        arcpy.MakeFeatureLayer_management(housing, "temp_layer", where_clause)
        arcpy.CopyFeatures_management("temp_layer", output)
        
        count = int(arcpy.GetCount_management(output).getOutput(0))
        arcpy.AddMessage("Found " + str(count) + " matching properties")
        
        arcpy.Delete_management("temp_layer")