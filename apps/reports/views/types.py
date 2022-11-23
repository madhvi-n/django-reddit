from core.views import BaseReadOnlyViewSet

from reports.models import ReportType
from reports.serializers import ReportTypeSerializer


class ReportTypeViewSet(BaseReadOnlyViewSet):
    serializer_class = ReportTypeSerializer
    queryset = ReportType.objects.all()
