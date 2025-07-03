from rest_framework import viewsets
from .models import Frame, SingleVision, Bifocal, ContactLens, Progressive
from .serializers import FrameSerializer, SingleVisionSerializer, BifocalSerializer, ContactLensSerializer, ProgressiveSerializer

class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer

class SingleVisionViewSet(viewsets.ModelViewSet):
    queryset = SingleVision.objects.all()
    serializer_class = SingleVisionSerializer

class BifocalViewSet(viewsets.ModelViewSet):
    queryset = Bifocal.objects.all()
    serializer_class = BifocalSerializer

class ContactLensViewSet(viewsets.ModelViewSet):
    queryset = ContactLens.objects.all()
    serializer_class = ContactLensSerializer

class ProgressiveViewSet(viewsets.ModelViewSet):
    queryset = Progressive.objects.all()
    serializer_class = ProgressiveSerializer
