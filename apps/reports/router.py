from reports.views import ReportTypeViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()

router.register("report_types", ReportTypeViewSet)
