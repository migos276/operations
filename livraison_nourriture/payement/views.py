from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import collect_money, deposit_money

class CollectMoneyView(APIView):
    def post(self, request):
        numero = request.data.get('numero')
        montant = request.data.get('montant')
        service = request.data.get('service', 'MTN')
        if not numero or not montant:
            return Response({"error": "numero et montant sont requis"}, status=status.HTTP_400_BAD_REQUEST)
        result = collect_money(numero, montant, service)
        return Response(result, status=status.HTTP_200_OK)


class DepositMoneyView(APIView):
    def post(self, request):
        numero = request.data.get('numero')
        montant = request.data.get('montant')
        service = request.data.get('service', 'MTN')
        if not numero or not montant:
            return Response({"error": "numero et montant sont requis"}, status=status.HTTP_400_BAD_REQUEST)
        result = deposit_money(numero, montant, service)
        return Response(result, status=status.HTTP_200_OK)

"""
@api_view(["POST"])
def webhook_pawapay(request):
    data = request.data
    reference = data.get("requestId")
    status = data.get("status")  # SUCCESS, FAILED, PENDING

    try:
        paiement = Paiement.objects.get(reference=reference)
        paiement.status = status.lower()
        paiement.save()
    except Paiement.DoesNotExist:
        pass

    return Response({"message": "ok"})

@api_view(["POST"])
def retirer_argent(request):
    numero = request.data.get("numero")
    montant = request.data.get("montant")
    reference = str(uuid.uuid4())

    headers = {"Authorization": f"Bearer {PAWAPAY_TOKEN}", "Content-Type": "application/json"}
    data = {
        "requestId": reference,
        "currency": "XAF",
        "amount": str(montant),
        "msisdn": numero,
        "country": "CM",  # Cameroun
        "service": "ORANGE"  # ou MTN
    }
    r = requests.post("https://api.sandbox.pawapay.io/payouts", json=data, headers=headers)

    if r.status_code == 200:
        return Response({"message": "Retrait en cours", "reference": reference})
    else:
        return Response({"message": "Erreur lors du retrait"}, status=400)
"""