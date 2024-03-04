from django.conf import settings


# Serializers Error Messages Modified
def serailizer_errors(e):
    #checking if error is in dict
    
    if(isinstance(e.detail,dict)):
        error_detail = list(e.detail.items())[0]
        field_name, error_message = error_detail[0], str(error_detail[1][0])
        return field_name, error_message
    
    #checking if error is in list
    elif(isinstance(e.detail,list) ):
        error_detail = e.detail[0]
        return  "non_field_errors", error_detail
    
    else:
        return "Invalid data provided."
