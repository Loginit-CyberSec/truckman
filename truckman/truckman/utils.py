#utilies functions


#get request user company
def get_user_company(request):
    if request.user.is_authenticated:
        try:
            company = request.user.company
        except:
            company = None
        return company
    
        