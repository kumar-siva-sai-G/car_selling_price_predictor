from django.shortcuts import render
from .car_eval import predict_price 
from .car_eval import df

def index(request):
    context = {
        'names': df['name'].unique(),
        'fuels': df['fuel_type'].unique(),
        'companies': df['company'].unique(),
        'error': ''
    }

    if request.method == "POST":
        name = request.POST.get("name", "")
        year = request.POST.get("year", "")
        fuel = request.POST.get("fuel", "")
        kms = request.POST.get("kms", "")
        company = request.POST.get("company", "")

        # Validation for required fields
        if not all([name, year, fuel, kms, company]):
            context['error'] = "⚠️ Please fill in all fields before submitting!"
        else:
            try:
                year = int(year)
                kms = int(kms)
                result = predict_price(name, year, fuel, kms, company)
                context['result'] = result
            except ValueError:
                context['error'] = "⚠️ Please enter valid numeric values for Year and KMS Driven."

    return render(request, "index.html", context)