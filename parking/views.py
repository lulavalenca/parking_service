from rest_framework.permissions import DjangoModelPermissions
from rest_framework import viewsets

from core.permissions import IsOwnerOfVehicleOrRecord
from parking.filters import ParkingSpotFilterClass, ParkingRecordFilterClass
from parking.models import ParkingSpot, ParkingRecord
from parking.serializers import ParkingSpotSerializer, ParkingRecordSerializer


class ParkingSpotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer
    rql_filter_class = ParkingSpotFilterClass
    permission_classes = [DjangoModelPermissions]
    
class ParkingRecordViewSet(viewsets.ModelViewSet):
    queryset = ParkingRecord.objects.all()
    serializer_class = ParkingRecordSerializer
    rql_filter_class = ParkingRecordFilterClass
    permission_classes = [DjangoModelPermissions, IsOwnerOfVehicleOrRecord]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ParkingRecord.objects.all()
        return ParkingRecord.objects.filter(Vehicle__owner__user=user)